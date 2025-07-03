#!/usr/bin/env python3
"""
Simple script to help move your downloaded service account JSON file
"""

import os
import shutil
import json

def find_and_move_credentials():
    """Find and move the service account credentials file"""
    
    print("🔍 Looking for your downloaded service account JSON file...")
    
    # Check Downloads folder
    downloads_path = os.path.expanduser("~/Downloads")
    
    if os.path.exists(downloads_path):
        print(f"📁 Checking Downloads folder: {downloads_path}")
        
        json_files = []
        for file in os.listdir(downloads_path):
            if file.endswith('.json') and 'avid-life-464809-c3' in file:
                json_files.append(os.path.join(downloads_path, file))
        
        if json_files:
            # Use the most recent file
            latest_file = max(json_files, key=os.path.getctime)
            print(f"✅ Found: {latest_file}")
            
            # Validate it's a service account file
            try:
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                
                if data.get('type') == 'service_account':
                    print(f"✅ Valid service account file!")
                    print(f"   Email: {data.get('client_email')}")
                    
                    # Move to correct location
                    target_dir = os.path.join('src', 'credentials')
                    target_path = os.path.join(target_dir, 'service-account.json')
                    
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.copy2(latest_file, target_path)
                    
                    print(f"✅ Moved to: {target_path}")
                    print("\n🎉 Setup complete! Now run: python test_credentials.py")
                    return True
                else:
                    print(f"❌ This is not a service account file")
                    return False
                    
            except Exception as e:
                print(f"❌ Error reading file: {e}")
                return False
        else:
            print("❌ No matching JSON files found in Downloads")
    
    print("\n📋 Manual Instructions:")
    print("1. Download the JSON key from Google Cloud Console:")
    print("   https://console.cloud.google.com/iam-admin/serviceaccounts?project=avid-life-464809-c3")
    print("2. Click on: dice-game-sheets@avid-life-464809-c3.iam.gserviceaccount.com")
    print("3. Go to 'Keys' tab → 'Add Key' → 'Create new key' → 'JSON'")
    print("4. The file will download automatically")
    print("5. Run this script again: python move_credentials.py")
    
    return False

if __name__ == "__main__":
    find_and_move_credentials()
