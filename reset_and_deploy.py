#!/usr/bin/env python3
"""
Reset all data and prepare for clean deployment
"""

import os
import sys
import shutil
import requests

# Add current directory and src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

def clear_local_database():
    """Clear local database files"""
    print("🗄️ Clearing local database...")
    
    db_path = os.path.join('src', 'database', 'app.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Removed {db_path}")
    else:
        print(f"ℹ️ Database file {db_path} doesn't exist")

def clear_local_data():
    """Clear local data files"""
    print("📁 Clearing local data files...")
    
    data_path = os.path.join('src', 'data')
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
        print(f"✅ Removed {data_path}")
    
    # Recreate empty data directory
    os.makedirs(data_path, exist_ok=True)
    print(f"✅ Created empty {data_path}")

def clear_cache_files():
    """Clear Python cache files"""
    print("🧹 Clearing Python cache...")
    
    for root, dirs, files in os.walk('.'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(cache_path)
            print(f"✅ Removed {cache_path}")
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                os.remove(pyc_path)
                print(f"✅ Removed {pyc_path}")

def test_local_reset():
    """Test local reset by starting the app briefly"""
    print("🧪 Testing local reset...")
    
    try:
        # Import and test the app
        from src.main import app
        
        with app.app_context():
            from src.models.user import db, User, DiceRoll, Ranking
            
            # Check if tables are empty
            user_count = User.query.count()
            roll_count = DiceRoll.query.count()
            ranking_count = Ranking.query.count()
            
            print(f"📊 Current counts:")
            print(f"   Users: {user_count}")
            print(f"   Dice Rolls: {roll_count}")
            print(f"   Rankings: {ranking_count}")
            
            if user_count == 0 and roll_count == 0 and ranking_count == 0:
                print("✅ Local database is clean!")
                return True
            else:
                print("⚠️ Local database still has data")
                return False
                
    except Exception as e:
        print(f"❌ Error testing local reset: {e}")
        return False

def reset_remote_via_api(base_url):
    """Reset remote data via API"""
    print(f"🌐 Resetting remote data at {base_url}...")
    
    try:
        # First check current counts
        response = requests.get(f"{base_url}/api/reset/confirm", timeout=10)
        if response.status_code == 200:
            counts = response.json()
            print(f"📊 Remote data before reset:")
            for key, value in counts.items():
                print(f"   {key}: {value}")
        
        # Perform reset
        response = requests.post(f"{base_url}/api/reset", timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Remote reset successful!")
            print(f"   Database cleared: {result.get('database_cleared')}")
            print(f"   Deleted users: {result.get('deleted_users')}")
            print(f"   Deleted rolls: {result.get('deleted_rolls')}")
            print(f"   Deleted rankings: {result.get('deleted_rankings')}")
            print(f"   Sheets cleared: {result.get('sheets_cleared')}")
            if result.get('sheets_error'):
                print(f"   Sheets error: {result.get('sheets_error')}")
            return True
        else:
            print(f"❌ Remote reset failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error resetting remote data: {e}")
        return False

def main():
    """Main reset and deploy process"""
    print("🎲 DICE ROLLING GAME - RESET & DEPLOY")
    print("=" * 50)
    
    # Step 1: Clear local data
    print("\n1️⃣ CLEARING LOCAL DATA")
    clear_local_database()
    clear_local_data()
    clear_cache_files()
    
    # Step 2: Test local reset
    print("\n2️⃣ TESTING LOCAL RESET")
    local_clean = test_local_reset()
    
    # Step 3: Ask about remote reset
    print("\n3️⃣ REMOTE RESET")
    remote_url = input("Enter your Railway URL (or press Enter to skip): ").strip()
    
    if remote_url:
        if not remote_url.startswith('http'):
            remote_url = f"https://{remote_url}"
        
        remote_clean = reset_remote_via_api(remote_url)
    else:
        print("⏭️ Skipping remote reset")
        remote_clean = True
    
    # Step 4: Summary
    print("\n4️⃣ SUMMARY")
    print("=" * 30)
    if local_clean:
        print("✅ Local data cleared")
    else:
        print("⚠️ Local data may not be fully cleared")
    
    if remote_url and remote_clean:
        print("✅ Remote data cleared")
    elif remote_url:
        print("❌ Remote data reset failed")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Commit and push changes to GitHub")
    print("2. Railway will automatically redeploy")
    print("3. Test the clean deployment")
    
    print("\n📋 COMMANDS TO RUN:")
    print("git add .")
    print('git commit -m "Reset all data for clean deployment"')
    print("git push")

if __name__ == "__main__":
    main()
