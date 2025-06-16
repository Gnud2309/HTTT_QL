import pymysqlreplication
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    WriteRowsEvent,
    UpdateRowsEvent,
    DeleteRowsEvent,
)
import pymysql
import pyodbc
import logging
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='mysql_replication.log'
)

# Load environment variables for connection settings only
load_dotenv()

class MySQLReplicator:
    def __init__(self, table_mappings, column_mappings=None, source_db_config=None, target_db_config=None):
        """
        Initialize the replicator with table mappings and database configurations
        
        Args:
            table_mappings (dict): Mapping of source tables to target tables
                Format: {
                    'source_db.table_name': 'target_db.schema.table_name',
                    'source_db.another_table': 'target_db.schema.another_table'
                }
            column_mappings (dict): Mapping of columns for each table
            source_db_config (dict, optional): Source MySQL database connection settings
            target_db_config (dict, optional): Target SQL Server database connection settings
        """
        # Source database configuration (MySQL)
        self.source_config = source_db_config or {
            'host': os.getenv('SOURCE_DB_HOST', 'localhost'),
            'port': int(os.getenv('SOURCE_DB_PORT', 3306)),
            'user': os.getenv('SOURCE_DB_USER', 'root'),
            'password': os.getenv('SOURCE_DB_PASSWORD', ''),
        }
        
        # Target database configuration (SQL Server)
        self.target_config = target_db_config or {
            'host': os.getenv('TARGET_DB_HOST', 'localhost'),
            'port': int(os.getenv('TARGET_DB_PORT', 1433)),
            'user': os.getenv('TARGET_DB_USER', 'sa'),
            'password': os.getenv('TARGET_DB_PASSWORD', ''),
            'driver': '{ODBC Driver 17 for SQL Server}',
            'database': 'DataWarehouse'  # Main database name
        }
        
        # Table mappings
        self.table_mappings = table_mappings
        # Reverse mapping for quick lookup
        self.reverse_mappings = {v: k for k, v in self.table_mappings.items()}
        
        # Column mappings
        self.column_mappings = column_mappings or {}
        
        # Extract database names (handle multi-dot table names)
        self.source_databases = set(table.split('.')[0] for table in self.table_mappings.keys())
        
        # For SQL Server, we only need the main database name
        self.target_database = self.target_config['database']
        
        # Initialize target connection
        self.target_conn = None
        self.target_cursor = None
        
        logging.info(f"Initialized replicator with {len(self.table_mappings)} table mappings")
        logging.info(f"Source databases: {', '.join(self.source_databases)}")
        logging.info(f"Target database: {self.target_database}")
        
        # Log column mappings for debugging
        for source_table, mapping in self.column_mappings.items():
            logging.info(f"Column mapping for {source_table}: {mapping}")

    def _get_sqlserver_connection_string(self):
        """Generate SQL Server connection string"""
        return (
            f"DRIVER={self.target_config['driver']};"
            f"SERVER={self.target_config['host']},{self.target_config['port']};"
            f"DATABASE={self.target_database};"
            f"UID={self.target_config['user']};"
            f"PWD={self.target_config['password']};"
            "TrustServerCertificate=yes;"
        )

    def _get_target_table_parts(self, target_table):
        """Split target table name into schema and table parts"""
        # Format: database.schema.table
        parts = target_table.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid target table format: {target_table}. Expected format: database.schema.table")
        # Return schema and table name
        return parts[1], parts[2]

    def _get_mapped_columns_and_values(self, source_table, row_values):
        """Get mapped columns and their values based on column mapping"""
        if source_table not in self.column_mappings:
            return list(row_values.keys()), list(row_values.values())
        
        mapping = self.column_mappings[source_table]
        mapped_columns = []
        mapped_values = []
        
        for source_col, value in row_values.items():
            if source_col in mapping:
                mapped_columns.append(mapping[source_col])
                mapped_values.append(value)
        
        return mapped_columns, mapped_values

    def connect_to_target(self):
        """Establish connection to target SQL Server database"""
        try:
            conn_str = self._get_sqlserver_connection_string()
            self.target_conn = pyodbc.connect(conn_str)
            self.target_cursor = self.target_conn.cursor()
            logging.info(f"Successfully connected to target database {self.target_database}")
        except Exception as e:
            logging.error(f"Failed to connect to target database: {str(e)}")
            raise

    def close_target_connection(self):
        """Close target database connection"""
        if self.target_cursor:
            self.target_cursor.close()
        if self.target_conn:
            self.target_conn.close()
        logging.info("Closed target database connection")

    def apply_insert(self, event):
        """Apply INSERT events to target database"""
        try:
            source_table = f"{event.schema}.{event.table}"
            target_table = self.get_target_table(source_table)
            
            if target_table not in self.table_mappings.values():
                logging.info(f"Skipping INSERT for unmapped table {source_table}")
                return

            schema, table_name = self._get_target_table_parts(target_table)

            for row in event.rows:
                # Get mapped columns and values
                mapped_columns, mapped_values = self._get_mapped_columns_and_values(
                    source_table, row["values"]
                )
                
                if not mapped_columns:
                    logging.warning(f"No mapped columns found for {source_table}, skipping row")
                    continue
                
                placeholders = ", ".join(["?"] * len(mapped_values))
                columns_str = ", ".join(mapped_columns)
                
                query = f"INSERT INTO [{schema}].[{table_name}] ({columns_str}) VALUES ({placeholders})"
                self.target_cursor.execute(query, mapped_values)
            
            self.target_conn.commit()
            logging.info(f"Applied INSERT from {source_table} to {target_table}")
        except Exception as e:
            self.target_conn.rollback()
            logging.error(f"Error applying INSERT from {source_table} to {target_table}: {str(e)}")
            raise

    def apply_update(self, event):
        """Apply UPDATE events to target database"""
        try:
            source_table = f"{event.schema}.{event.table}"
            target_table = self.get_target_table(source_table)
            
            if target_table not in self.table_mappings.values():
                logging.info(f"Skipping UPDATE for unmapped table {source_table}")
                return

            schema, table_name = self._get_target_table_parts(target_table)

            for row in event.rows:
                # Get mapped columns and values for both before and after states
                before_columns, before_values = self._get_mapped_columns_and_values(
                    source_table, row["before_values"]
                )
                after_columns, after_values = self._get_mapped_columns_and_values(
                    source_table, row["after_values"]
                )
                
                if not before_columns or not after_columns:
                    logging.warning(f"No mapped columns found for {source_table}, skipping row")
                    continue
                
                set_clause = ", ".join([f"{col} = ?" for col in after_columns])
                where_clause = " AND ".join([f"{col} = ?" for col in before_columns])
                
                values = after_values + before_values
                query = f"UPDATE [{schema}].[{table_name}] SET {set_clause} WHERE {where_clause}"
                
                self.target_cursor.execute(query, values)
            
            self.target_conn.commit()
            logging.info(f"Applied UPDATE from {source_table} to {target_table}")
        except Exception as e:
            self.target_conn.rollback()
            logging.error(f"Error applying UPDATE from {source_table} to {target_table}: {str(e)}")
            raise

    def apply_delete(self, event):
        """Apply DELETE events to target database"""
        try:
            source_table = f"{event.schema}.{event.table}"
            target_table = self.get_target_table(source_table)
            
            if target_table not in self.table_mappings.values():
                logging.info(f"Skipping DELETE for unmapped table {source_table}")
                return

            schema, table_name = self._get_target_table_parts(target_table)

            for row in event.rows:
                # Get mapped columns and values
                mapped_columns, mapped_values = self._get_mapped_columns_and_values(
                    source_table, row["values"]
                )
                
                if not mapped_columns:
                    logging.warning(f"No mapped columns found for {source_table}, skipping row")
                    continue
                
                where_clause = " AND ".join([f"{col} = ?" for col in mapped_columns])
                query = f"DELETE FROM [{schema}].[{table_name}] WHERE {where_clause}"
                
                self.target_cursor.execute(query, mapped_values)
            
            self.target_conn.commit()
            logging.info(f"Applied DELETE from {source_table} to {target_table}")
        except Exception as e:
            self.target_conn.rollback()
            logging.error(f"Error applying DELETE from {source_table} to {target_table}: {str(e)}")
            raise

    def get_target_table(self, source_table):
        """Get the target table name for a source table"""
        return self.table_mappings.get(source_table, source_table)

    def get_source_table(self, target_table):
        """Get the source table name for a target table"""
        return self.reverse_mappings.get(target_table, target_table)
    def run_silver_transformations(self):
        """Execute all bronze-to-silver transformation stored procedures."""
        self.clear_silver_tables()
        procedures = [
            "TransformBronzeCustEventToSilver",
            "TransformBronzeProductInfoToSilver",
            "TransformBronzeSaleOrderProductToSilver",

            "TransformBronzeSaleOrderToSilver",
            "TransformBronzeSalePaymentToSilver",
            "TransformCustInfoBronzeToSilver"
        ]
        try:
            for proc in procedures:
                logging.info(f"Executing stored procedure: {proc}")
                self.target_cursor.execute(f"EXEC {proc}")
                self.target_conn.commit()
                logging.info(f"Successfully executed: {proc}")
        except Exception as e:
            logging.error(f"Error executing stored procedures: {str(e)}")
            raise
    def clear_silver_tables(self):
        """Delete all records from the silver tables before transformation."""
        tables = [
            "silver.sale_order_product",
            "silver.sale_order",
            "silver.sale_payment",
            "silver.crm_cust_event",
            "silver.crm_cust_info",
            "silver.product_info"
        ]
        try:
            for table in tables:
                logging.info(f"Deleting all records from: {table}")
                self.target_cursor.execute(f"DELETE FROM {table}")
                self.target_conn.commit()
                logging.info(f"Successfully cleared: {table}")
        except Exception as e:
            logging.error(f"Error clearing silver tables: {str(e)}")
            raise
    def start_replication(self):
        """Start reading and applying binary logs"""
        try:
            # Connect to target database
            self.connect_to_target()
            
            # Get list of source tables to monitor (without database names)
            source_tables = [table.split('.')[1] for table in self.table_mappings.keys()]
            
            # Configure binary log stream
            stream = BinLogStreamReader(
                connection_settings=self.source_config,
                server_id=100,  # Unique server ID for this replicator
                only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent],
                only_tables=source_tables,  # Only monitor mapped tables
                resume_stream=True,
                blocking=True
            )
            
            logging.info(f"Starting binary log replication for tables: {', '.join(source_tables)}")
            
            for binlogevent in stream:
                try:
                    if isinstance(binlogevent, WriteRowsEvent):
                        self.apply_insert(binlogevent)
                    elif isinstance(binlogevent, UpdateRowsEvent):
                        self.apply_update(binlogevent)
                    elif isinstance(binlogevent, DeleteRowsEvent):
                        self.apply_delete(binlogevent)
                    # self.run_silver_transformations()
                except Exception as e:
                    logging.error(f"Error processing event: {str(e)}")
                    continue
                
        except Exception as e:
            logging.error(f"Replication error: {str(e)}")
            raise
        finally:
            stream.close()
            self.close_target_connection()

if __name__ == "__main__":
    # Define your table mappings here
    # Format: 'source_db.table_name': 'database.schema.table_name'
    table_mappings = {
        'ShopApp.accounts_userprofile': 'DataWarehouse.bronze.crm_cust_info',
        'ShopApp.store_product': 'DataWarehouse.bronze.product_info',
        'ShopApp.accounts_eventuser': 'DataWarehouse.bronze.crm_cust_event',
        'ShopApp.orders_order': 'DataWarehouse.bronze.sale_order',
        'ShopApp.orders_payment': 'DataWarehouse.bronze.sale_payment',
        'ShopApp.orders_orderproduct': 'DataWarehouse.bronze.sale_order_product',
    }
    
    # Define column mappings for each table
    # Only include columns that exist in both source and target tables
    column_mappings = {
        # Add mappings for your tables here
        'ShopApp.accounts_eventuser': {
            'id': 'event_id',
            'event_timestamp': 'event_time',
            'event_type': 'event_type',
            'user_id': 'user_id',
            'frequency': 'frequency',
            'product_id': 'product_id',
            'rating': 'rating',
        },
        'ShopApp.accounts_userprofile': {
            'id': 'cst_id',
            'user_id': 'cst_username',
            'profile_picture': 'profile_picture',
            'bio': 'bio',
            'date_of_birth': 'date_of_birth',
            'district': 'district',
            'road': 'road',
            'sex': 'sex',
            'ward': 'ward',
            'city': 'city'
        },
        'ShopApp.store_product': {
            'id': 'product_id',
            'product_name': 'product_name',
            'slug': 'slug',
            'short_desp': 'short_description',
            'description': 'description',
            'price': 'price',
            'mrp_price': 'mrp_price',
            'stock': 'stock',
            'is_available': 'is_available',
            'rating': 'rating',
            'brand_name': 'brand_name',
            'season': 'season',
            'year': 'year',
            'gender': 'gender',
            'category_main_id': 'category_main_id',
            'sub_category_id': 'sub_category_id',
            'created_date': 'created_date',
            'modified_date': 'modified_date'
        },
        'ShopApp.orders_order': {
            'id': 'order_id',
            'order_number': 'order_number',
            'user_id': 'user_id',
            'full_name': 'full_name',
            'phone': 'phone',
            'email': 'email',
            'city': 'city',
            'district': 'district',
            'ward': 'ward',
            'road': 'road',
            'order_note': 'order_note',
            'order_total': 'order_total',
            'tax': 'tax',
            'total_items': 'total_items',
            'payment_id': 'payment_id',
            'payment_method': 'payment_method',
            'status': 'status',
            'order_status': 'order_status',
            'ip': 'ip_address',
            'is_ordered': 'is_ordered',
            'is_view': 'is_viewed',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        },
        'ShopApp.orders_payment': {
            'id': 'payment_id',
            'payment_id': 'payment_code',
            'payment_method': 'payment_method',
            'amount_paid': 'amount_paid',
            'status': 'status',
            'user_id': 'user_id',
            'created_at': 'created_at'
        },
        'ShopApp.orders_orderproduct': {
            'id': 'order_product_id',
            'order_id': 'order_id',
            'user_id': 'user_id',
            'product_id': 'product_id',
            'quantity': 'quantity',
            'price': 'product_price',
            'discount_amount': 'discount_amount',
            'ordered': 'ordered',
            'payment_id': 'payment_id',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }
    }
    
    # Source MySQL database configuration
    source_db_config = {
        'host': 'localhost',
        'port': 3310,
        'user': 'root',
        'password': '123'
    }
    
    # Target SQL Server database configuration
    target_db_config = {
        'host': 'localhost',
        'port': 1433,
        'user': 'sa',
        'password': 'ShopApp@DW2025',
        'driver': '{ODBC Driver 17 for SQL Server}',
        'database': 'DataWarehouse'  # Main database name
    }
    
    try:
        # Initialize replicator with table mappings, column mappings, and connection settings
        replicator = MySQLReplicator(
            table_mappings=table_mappings,
            column_mappings=column_mappings,
            source_db_config=source_db_config,
            target_db_config=target_db_config
        )
        replicator.start_replication()
    except KeyboardInterrupt:
        logging.info("Replication stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
