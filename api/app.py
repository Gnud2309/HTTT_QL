from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .routes import api_bp
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Application factory pattern for creating Flask app"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Data Warehouse API',
            'version': Config.API_VERSION,
            'description': Config.API_DESCRIPTION,
            'endpoints': {
                'health': '/api/v1/health',
                'gold_views': '/api/v1/gold/views',
                'top_product': '/api/v1/gold/top-product',
                'top_provider': '/api/v1/gold/top-provider',
                'top_new_user_province': '/api/v1/gold/top-new-user-province',
                'view_data': '/api/v1/gold/views/<view_name>',
                'view_schema': '/api/v1/gold/views/<view_name>/schema',
                'view_count': '/api/v1/gold/views/<view_name>/count'
            },
            'examples': {
                'get_all_views': 'GET /api/v1/gold/views',
                'get_top_products': 'GET /api/v1/gold/top-product?limit=10',
                'get_view_data': 'GET /api/v1/gold/views/top_product?limit=5&offset=0'
            }
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'message': 'The requested resource was not found on this server'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An internal server error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    logger.info("Flask application created successfully")
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    ) 