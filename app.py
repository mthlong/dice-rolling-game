#!/usr/bin/env python3
"""
Simple startup script for Railway deployment
"""

import os
import sys

# Add current directory and src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Set environment variables
os.environ.setdefault('FLASK_ENV', 'production')

# Import and run the Flask app
try:
    from src.main import app
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5001))
        print(f"Starting Flask app on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    print(f"Files in current directory: {os.listdir(current_dir)}")
    if os.path.exists('src'):
        print(f"Files in src directory: {os.listdir('src')}")
    sys.exit(1)
