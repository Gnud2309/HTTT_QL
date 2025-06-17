from flask import Blueprint, jsonify, request, abort
from .models import GoldViews
import logging
import asyncio

logger = logging.getLogger(__name__)

# Create blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Data Warehouse API is running'
    })

@api_bp.route('/gold/views', methods=['GET'])
def get_available_views():
    """Get list of available gold views"""
    try:
        views = asyncio.run(GoldViews.get_available_views())
        return jsonify({
            'success': True,
            'data': views,
            'count': len(views)
        })
    except Exception as e:
        logger.error(f"Error getting available views: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/gold/views/<view_name>/schema', methods=['GET'])
def get_view_schema(view_name):
    """Get schema information for a specific gold view"""
    try:
        schema = asyncio.run(GoldViews.get_view_schema(view_name))
        return jsonify({
            'success': True,
            'data': schema,
            'view': view_name
        })
    except Exception as e:
        logger.error(f"Error getting schema for view {view_name}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/gold/views/<view_name>', methods=['GET'])
def get_view_data(view_name):
    """Get data from any gold view with pagination"""
    try:
        # Get query parameters for pagination
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int, default=0)
        
        # Get data
        data = asyncio.run(GoldViews.get_view_data(view_name, limit=limit, offset=offset))
        total_count = asyncio.run(GoldViews.get_view_count(view_name))
        
        return jsonify({
            'success': True,
            'data': data,
            'view': view_name,
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'count': len(data)
            }
        })
    except Exception as e:
        logger.error(f"Error fetching data from gold view {view_name}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/gold/views/<view_name>/count', methods=['GET'])
def get_view_count(view_name):
    """Get total count of records in a gold view"""
    try:
        count = asyncio.run(GoldViews.get_view_count(view_name))
        return jsonify({
            'success': True,
            'data': {
                'count': count,
                'view': f'gold.{view_name}'
            }
        })
    except Exception as e:
        logger.error(f"Error getting count from gold view {view_name}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Specific view endpoints for convenience
@api_bp.route('/gold/top-product', methods=['GET'])
def get_top_product():
    """Get top products from gold view"""
    try:
        limit = request.args.get('limit', type=int)
        data = asyncio.run(GoldViews.get_top_product(limit=limit))
        
        return jsonify({
            'success': True,
            'data': data,
            'view': 'gold.top_product',
            'count': len(data)
        })
    except Exception as e:
        logger.error(f"Error fetching top products: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/gold/top-provider', methods=['GET'])
def get_top_provider():
    """Get top providers from gold view"""
    try:
        limit = request.args.get('limit', type=int)
        data = asyncio.run(GoldViews.get_top_provider(limit=limit))
        
        return jsonify({
            'success': True,
            'data': data,
            'view': 'gold.top_provider',
            'count': len(data)
        })
    except Exception as e:
        logger.error(f"Error fetching top providers: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/gold/top-new-user-province', methods=['GET'])
def get_top_new_user_province():
    """Get top new user province from gold view"""
    try:
        limit = request.args.get('limit', type=int)
        data = asyncio.run(GoldViews.get_top_new_user_province(limit=limit))
        
        return jsonify({
            'success': True,
            'data': data,
            'view': 'gold.top_new_user_province',
            'count': len(data)
        })
    except Exception as e:
        logger.error(f"Error fetching top new user province: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500 