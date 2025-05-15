from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        NEWS_API_KEY=os.environ.get('NEWS_API_KEY', ''),
        OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY', '')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Register API endpoints
    from app.api import stock_routes
    app.register_blueprint(stock_routes.bp)
    
    # Register error handlers
    from app.api import error_handlers
    app.register_blueprint(error_handlers.bp)

    # Register a simple index route
    @app.route('/')
    def index():
        return {
            "name": "AI Stock Analyst API",
            "version": "0.1.0",
            "status": "running"
        }

    return app
