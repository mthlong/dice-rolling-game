#!/usr/bin/env python3
"""
Robust startup script for deployment
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the environment for deployment"""
    logger.info("Setting up environment...")

    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # Also add src directory to path
    src_dir = os.path.join(current_dir, 'src')
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'production')

    logger.info(f"Python path: {sys.path}")
    logger.info(f"Current directory: {current_dir}")
    logger.info(f"Files in current directory: {os.listdir(current_dir)}")
    if os.path.exists(src_dir):
        logger.info(f"Files in src directory: {os.listdir(src_dir)}")
    logger.info(f"PORT: {os.environ.get('PORT', 'Not set')}")
    logger.info(f"FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}")

def create_directories():
    """Create necessary directories"""
    directories = [
        'src/database',
        'src/data',
        'src/credentials'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

def start_app():
    """Start the Flask application"""
    try:
        setup_environment()
        create_directories()
        
        logger.info("Starting Flask application...")
        
        # Import and run the app
        from src.main import app
        
        port = int(os.environ.get('PORT', 5001))
        debug = os.environ.get('FLASK_ENV') != 'production'
        
        logger.info(f"Starting server on port {port}, debug={debug}")
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=False  # Disable reloader in production
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    start_app()
