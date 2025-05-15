from flask import jsonify, Blueprint
import traceback

bp = Blueprint('errors', __name__)

@bp.app_errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    return jsonify({
        'error': 'Bad Request',
        'message': str(error.description)
    }), 400

@bp.app_errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({
        'error': 'Not Found',
        'message': str(error.description)
    }), 404

@bp.app_errorhandler(500)
def server_error(error):
    """Handle 500 Internal Server Error."""
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error.description)
    }), 500

@bp.app_errorhandler(Exception)
def handle_unexpected_error(error):
    """Handle unexpected exceptions."""
    # Log the error
    traceback.print_exc()
    
    return jsonify({
        'error': 'Unexpected Error',
        'message': str(error)
    }), 500 