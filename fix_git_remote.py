#!/usr/bin/env python3
"""
Script to help fix git remote URL
"""

import subprocess
import sys

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_current_remote():
    """Check current git remote"""
    success, stdout, stderr = run_command("git remote -v")
    
    if success and stdout:
        print("📍 Current git remotes:")
        print(stdout)
        return True
    else:
        print("❌ No git remotes found or git not initialized")
        return False

def fix_remote():
    """Help user fix the git remote"""
    print("🔧 GIT REMOTE FIXER")
    print("=" * 30)
    
    # Check current status
    if not check_current_remote():
        print("\n❌ Git not properly initialized")
        return
    
    print("\n🛠️  SOLUTIONS:")
    print("-" * 20)
    
    print("\n1. 📝 Update existing remote:")
    print("   git remote set-url origin https://github.com/YOUR_USERNAME/dice-rolling-game.git")
    
    print("\n2. 🗑️  Remove and re-add remote:")
    print("   git remote remove origin")
    print("   git remote add origin https://github.com/YOUR_USERNAME/dice-rolling-game.git")
    
    print("\n3. 🆕 Create new repository:")
    print("   - Go to https://github.com/new")
    print("   - Repository name: dice-rolling-game")
    print("   - Copy the repository URL")
    print("   - Use solution 1 or 2 above")
    
    print("\n4. 🚀 Push to new repository:")
    print("   git push -u origin main")
    
    # Interactive fix
    print("\n" + "=" * 50)
    response = input("Would you like me to help you fix this interactively? (y/n): ").lower()
    
    if response == 'y':
        interactive_fix()

def interactive_fix():
    """Interactive git remote fixing"""
    print("\n🔧 Interactive Fix")
    print("-" * 20)
    
    # Get the correct repository URL
    repo_url = input("\n📝 Enter your correct GitHub repository URL: ").strip()
    
    if not repo_url:
        print("❌ No URL provided")
        return
    
    if not repo_url.startswith("https://github.com/"):
        print("❌ Invalid GitHub URL format")
        return
    
    print(f"\n✅ Using repository: {repo_url}")
    
    # Remove existing remote
    print("\n🗑️  Removing existing remote...")
    success, stdout, stderr = run_command("git remote remove origin")
    
    if success:
        print("✅ Old remote removed")
    else:
        print(f"⚠️  Warning: {stderr}")
    
    # Add new remote
    print(f"\n➕ Adding new remote: {repo_url}")
    success, stdout, stderr = run_command(f"git remote add origin {repo_url}")
    
    if success:
        print("✅ New remote added successfully!")
        
        # Verify
        success, stdout, stderr = run_command("git remote -v")
        if success:
            print("\n📍 Updated remotes:")
            print(stdout)
        
        print("\n🚀 Ready to push! Run:")
        print("   git push -u origin main")
        
    else:
        print(f"❌ Failed to add remote: {stderr}")

if __name__ == "__main__":
    fix_remote()
