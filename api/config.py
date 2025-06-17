import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Flask API"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # SQL Server configuration
    SQL_SERVER_CONFIG = {
        'host': os.environ.get('SQL_SERVER_HOST', 'localhost'),
        'port': int(os.environ.get('SQL_SERVER_PORT', 1433)),
        'user': os.environ.get('SQL_SERVER_USER', 'sa'),
        'password': os.environ.get('SQL_SERVER_PASSWORD', 'ShopApp@DW2025'),
        'driver': os.environ.get('SQL_SERVER_DRIVER', '{ODBC Driver 17 for SQL Server}'),
        'database': os.environ.get('SQL_SERVER_DATABASE', 'DataWarehouse')
    }
    
    # API configuration
    API_TITLE = 'Data Warehouse API'
    API_VERSION = '1.0.0'
    API_DESCRIPTION = 'API for accessing Data Warehouse gold tables' 