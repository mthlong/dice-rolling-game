#!/usr/bin/env python3
"""
Build script to create static files for Cloudflare Pages deployment
"""

import os
import shutil

def build_static():
    """Build static version of the dice rolling game"""
    
    # Create build directory
    build_dir = "dist"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    # Copy static HTML file
    if os.path.exists("static_build/index.html"):
        shutil.copy2("static_build/index.html", os.path.join(build_dir, "index.html"))
        print("✅ Copied index.html to dist/")
    else:
        print("❌ static_build/index.html not found")
        return False
    
    # Create a simple 404 page
    with open(os.path.join(build_dir, "404.html"), "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>404 - Page Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #333; }
        a { color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">← Back to Dice Game</a>
</body>
</html>
        """)
    
    print("✅ Created 404.html")
    print(f"✅ Static build complete! Files are in {build_dir}/")
    return True

if __name__ == "__main__":
    build_static()
