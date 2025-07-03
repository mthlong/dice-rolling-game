#!/usr/bin/env python3
"""
Quick deployment helper script
"""

import os
import subprocess
import json

def check_git_status():
    """Check if git is initialized and files are ready"""
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git not initialized. Run: git init")
            return False
        
        print("✅ Git repository detected")
        return True
    except FileNotFoundError:
        print("❌ Git not installed")
        return False

def check_credentials():
    """Check if service account credentials exist"""
    creds_path = os.path.join('src', 'credentials', 'service-account.json')
    if os.path.exists(creds_path):
        print("✅ Service account credentials found")
        return True
    else:
        print("❌ Service account credentials missing")
        print("   Please add: src/credentials/service-account.json")
        return False

def show_deployment_options():
    """Show deployment options"""
    print("\n🚀 DEPLOYMENT OPTIONS")
    print("=" * 40)
    
    print("\n1. 🚂 Railway (Recommended)")
    print("   - Free tier available")
    print("   - Easy GitHub integration")
    print("   - Auto-deploys on push")
    print("   - URL: https://railway.app/")
    
    print("\n2. 🎨 Render")
    print("   - Free tier available")
    print("   - Good for static sites")
    print("   - URL: https://render.com/")
    
    print("\n3. 🟣 Heroku")
    print("   - Paid plans only")
    print("   - Very reliable")
    print("   - URL: https://heroku.com/")
    
    print("\n4. ▲ Vercel")
    print("   - Great for serverless")
    print("   - Free tier available")
    print("   - URL: https://vercel.com/")

def show_next_steps():
    """Show next steps for deployment"""
    print("\n📋 NEXT STEPS")
    print("=" * 40)
    
    print("\n1. Create GitHub Repository:")
    print("   - Go to https://github.com/new")
    print("   - Create a new repository")
    print("   - Copy the repository URL")
    
    print("\n2. Push Your Code:")
    print("   git remote add origin YOUR_REPO_URL")
    print("   git add .")
    print("   git commit -m 'Deploy dice rolling game'")
    print("   git push -u origin main")
    
    print("\n3. Deploy on Railway (Recommended):")
    print("   - Go to https://railway.app/")
    print("   - Click 'Deploy from GitHub repo'")
    print("   - Select your repository")
    print("   - Upload service-account.json in Variables tab")
    
    print("\n4. Test Your Deployment:")
    print("   - Visit the provided URL")
    print("   - Roll some dice")
    print("   - Check your Google Sheet")

def main():
    """Main deployment helper"""
    print("🎲 DICE ROLLING GAME - DEPLOYMENT HELPER")
    print("=" * 50)
    
    # Check prerequisites
    print("\n🔍 Checking Prerequisites...")
    
    git_ready = check_git_status()
    creds_ready = check_credentials()
    
    if not git_ready or not creds_ready:
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        return
    
    print("\n✅ All prerequisites met!")
    
    # Show deployment options
    show_deployment_options()
    
    # Show next steps
    show_next_steps()
    
    print("\n🎉 Your dice rolling game is ready for deployment!")
    print("📖 For detailed instructions, see: DEPLOYMENT.md")

if __name__ == "__main__":
    main()
