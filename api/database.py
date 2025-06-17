import pyodbc
import logging
import asyncio
import concurrent.futures
from typing import List, Dict, Any, Optional
from .config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Database connection manager for SQL Server"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.connection = None
        self.cursor = None
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    
    def get_connection_string(self) -> str:
        """Generate SQL Server connection string"""
        return (
            f"DRIVER={self.config.SQL_SERVER_CONFIG['driver']};"
            f"SERVER={self.config.SQL_SERVER_CONFIG['host']},{self.config.SQL_SERVER_CONFIG['port']};"
            f"DATABASE={self.config.SQL_SERVER_CONFIG['database']};"
            f"UID={self.config.SQL_SERVER_CONFIG['user']};"
            f"PWD={self.config.SQL_SERVER_CONFIG['password']};"
            "TrustServerCertificate=yes;"
        )
    
    def connect(self):
        """Establish connection to SQL Server"""
        try:
            conn_str = self.get_connection_string()
            self.connection = pyodbc.connect(conn_str)
            self.cursor = self.connection.cursor()
            logger.info(f"Successfully connected to database {self.config.SQL_SERVER_CONFIG['database']}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Database connection closed")
    
    async def execute_query_async(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query asynchronously and return results as a list of dictionaries"""
        try:
            if not self.connection:
                self.connect()
            
            # Run the database operation in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._execute_query_sync,
                query,
                params
            )
            return result
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def _execute_query_sync(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Synchronous version of execute_query for use in thread pool"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in self.cursor.description]
            
            # Fetch all rows and convert to list of dictionaries
            rows = self.cursor.fetchall()
            results = []
            
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            return results
            
        except Exception as e:
            logger.error(f"Error in synchronous query execution: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query synchronously and return results as a list of dictionaries"""
        return self._execute_query_sync(query, params)
    
    async def execute_procedure_async(self, procedure_name: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a stored procedure asynchronously and return results"""
        query = f"EXEC {procedure_name}"
        if params:
            placeholders = ", ".join(["?"] * len(params))
            query += f" {placeholders}"
        
        return await self.execute_query_async(query, params)
    
    def execute_procedure(self, procedure_name: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a stored procedure synchronously and return results"""
        query = f"EXEC {procedure_name}"
        if params:
            placeholders = ", ".join(["?"] * len(params))
            query += f" {placeholders}"
        
        return self.execute_query(query, params)
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
        self.executor.shutdown(wait=True)
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        self.disconnect()
        self.executor.shutdown(wait=True) 