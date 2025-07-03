#!/usr/bin/env python3
"""
Complete git setup script for deployment
"""

import subprocess
import os

def run_command(command, show_output=True):
    """Run a shell command"""
    try:
        if show_output:
            print(f"🔧 Running: {command}")
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            if show_output and result.stdout:
                print(f"✅ {result.stdout.strip()}")
            return True, result.stdout.strip()
        else:
            if show_output:
                print(f"❌ Error: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        if show_output:
            print(f"❌ Exception: {e}")
        return False, str(e)

def setup_git():
    """Complete git setup"""
    print("🎲 DICE ROLLING GAME - GIT SETUP")
    print("=" * 40)
    
    # Check if git is installed
    success, _ = run_command("git --version", show_output=False)
    if not success:
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    print("✅ Git is installed")
    
    # Initialize git if not already done
    if not os.path.exists('.git'):
        print("\n📁 Initializing git repository...")
        success, _ = run_command("git init")
        if not success:
            return False
    else:
        print("✅ Git repository already initialized")
    
    # Check git config
    print("\n👤 Checking git configuration...")
    success, email = run_command("git config user.email", show_output=False)
    if not success or not email:
        print("⚠️  Git user email not set")
        email = input("📧 Enter your email: ").strip()
        if email:
            run_command(f'git config user.email "{email}"')
    
    success, name = run_command("git config user.name", show_output=False)
    if not success or not name:
        print("⚠️  Git user name not set")
        name = input("👤 Enter your name: ").strip()
        if name:
            run_command(f'git config user.name "{name}"')
    
    # Add files
    print("\n📦 Adding files to git...")
    run_command("git add .")
    
    # Commit
    print("\n💾 Creating initial commit...")
    success, _ = run_command('git commit -m "Initial commit - Dice Rolling Game"')
    if not success:
        print("ℹ️  Files might already be committed")
    
    # Get repository URL
    print("\n" + "=" * 50)
    print("🔗 GITHUB REPOSITORY SETUP")
    print("=" * 50)
    
    print("\n📋 Steps to create GitHub repository:")
    print("1. Go to: https://github.com/new")
    print("2. Repository name: dice-rolling-game")
    print("3. Make it Public")
    print("4. Don't initialize with README (we already have files)")
    print("5. Click 'Create repository'")
    print("6. Copy the repository URL")
    
    repo_url = input("\n🔗 Paste your GitHub repository URL here: ").strip()
    
    if not repo_url:
        print("❌ No repository URL provided")
        print("\n📋 Manual commands to run later:")
        print("git remote add origin YOUR_REPO_URL")
        print("git branch -M main")
        print("git push -u origin main")
        return False
    
    # Validate URL
    if not repo_url.startswith("https://github.com/"):
        print("❌ Invalid GitHub URL. Should start with https://github.com/")
        return False
    
    # Add remote
    print(f"\n🔗 Adding remote repository: {repo_url}")
    success, _ = run_command(f"git remote add origin {repo_url}")
    if not success:
        print("⚠️  Remote might already exist, trying to update...")
        run_command(f"git remote set-url origin {repo_url}")
    
    # Set main branch
    print("\n🌿 Setting main branch...")
    run_command("git branch -M main")
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    success, output = run_command("git push -u origin main")
    
    if success:
        print("\n🎉 SUCCESS! Your code is now on GitHub!")
        print(f"📍 Repository: {repo_url}")
        
        # Show deployment options
        show_deployment_options(repo_url)
        return True
    else:
        print(f"\n❌ Failed to push to GitHub")
        print("📋 Try running manually:")
        print("git push -u origin main")
        return False

def show_deployment_options(repo_url):
    """Show deployment options"""
    print("\n" + "=" * 50)
    print("🚀 READY FOR DEPLOYMENT!")
    print("=" * 50)
    
    print(f"\n📍 Your repository: {repo_url}")
    
    print("\n🚂 Deploy on Railway (Recommended):")
    print("1. Go to: https://railway.app/")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'Deploy from GitHub repo'")
    print("4. Select: dice-rolling-game")
    print("5. Upload service-account.json in Variables tab")
    print("6. Set FLASK_ENV=production")
    
    print("\n🎨 Deploy on Render:")
    print("1. Go to: https://render.com/")
    print("2. Connect GitHub account")
    print("3. Create new Web Service")
    print("4. Select your repository")
    
    print("\n▲ Deploy on Vercel:")
    print("1. Go to: https://vercel.com/")
    print("2. Import Git Repository")
    print("3. Select your repository")

if __name__ == "__main__":
    setup_git()
