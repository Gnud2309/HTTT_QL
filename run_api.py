#!/usr/bin/env python3
"""
Main entry point for the Data Warehouse API
"""

import os
import sys
from api.app import app

if __name__ == '__main__':
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting Data Warehouse API...")
    print("API will be available at: http://localhost:5000")
    print("API Documentation: http://localhost:5000")
    print("Health Check: http://localhost:5000/api/v1/health")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\nShutting down API server...")
    except Exception as e:
        print(f"Error starting API server: {str(e)}")
        sys.exit(1) 