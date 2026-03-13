"""
KoreaPolicySim backend Flask app factory.
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings from third-party libraries.
# This must run before other imports.
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask app factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Keep JSON output human-readable.
    # Flask >= 2.3 uses app.json.ensure_ascii; older versions rely on JSON_AS_ASCII.
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # Configure logging.
    logger = setup_logger('koreapolicysim')
    
    # Only log startup once when the reloader is active.
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("Starting KoreaPolicySim backend...")
        logger.info("=" * 50)
    
    # Enable CORS.
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register simulation-process cleanup to stop all child processes on shutdown.
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Registered simulation cleanup handler")
    
    # Request logging middleware.
    @app.before_request
    def log_request():
        logger = get_logger('koreapolicysim.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")
    
    @app.after_request
    def log_response(response):
        logger = get_logger('koreapolicysim.request')
        logger.debug(f"Response: {response.status_code}")
        return response
    
    # Register blueprints.
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # Health check.
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'KoreaPolicySim Backend'}
    
    if should_log_startup:
        logger.info("KoreaPolicySim backend started")
    
    return app
