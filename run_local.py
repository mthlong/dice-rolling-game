#!/usr/bin/env python3
"""
Local development script for the dice rolling game
"""

import os
import sys

# Add current directory and src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Set environment variables for local development
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('PORT', '5001')

# Import and run the Flask app
try:
    from src.main import app
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5001))
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        print("🎲 DICE ROLLING GAME - LOCAL DEVELOPMENT")
        print("=" * 50)
        print(f"🌐 Server: http://localhost:{port}")
        print(f"🔧 Debug mode: {debug}")
        print(f"📁 Working directory: {current_dir}")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print()
        
        app.run(
            host='127.0.0.1',  # localhost only for development
            port=port, 
            debug=debug,
            use_reloader=True  # Auto-reload on file changes
        )
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"📁 Current directory: {current_dir}")
    print(f"🐍 Python path: {sys.path}")
    print(f"📂 Files in current directory: {os.listdir(current_dir)}")
    if os.path.exists('src'):
        print(f"📂 Files in src directory: {os.listdir('src')}")
    print("\n💡 Make sure you're in the correct directory and have installed dependencies:")
    print("   pip3 install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
