#!/usr/bin/env python3
"""
Helper script to set up service account credentials
"""

import os
import json
import shutil

def setup_service_account():
    """Help user set up service account credentials"""
    
    print("🔧 Service Account Setup Helper")
    print("=" * 40)
    
    print("\n📋 Your Project Information:")
    print("Project ID: avid-life-464809-c3")
    print("Expected Service Account Email: dice-game-sheets@avid-life-464809-c3.iam.gserviceaccount.com")
    
    print("\n📥 Looking for downloaded service account file...")
    
    # Common download locations
    possible_locations = [
        os.path.expanduser("~/Downloads/"),
        os.path.expanduser("~/Desktop/"),
        "./",
        "../"
    ]
    
    service_account_files = []
    
    for location in possible_locations:
        if os.path.exists(location):
            for file in os.listdir(location):
                if file.endswith('.json') and ('service' in file.lower() or 'avid-life' in file):
                    full_path = os.path.join(location, file)
                    service_account_files.append(full_path)
    
    if service_account_files:
        print(f"\n✅ Found potential service account files:")
        for i, file_path in enumerate(service_account_files, 1):
            print(f"   {i}. {file_path}")
        
        # Try to validate and copy the first one
        for file_path in service_account_files:
            if validate_and_copy_service_account(file_path):
                return True
    
    print("\n❌ No service account file found automatically.")
    print("\n📋 Manual Setup Instructions:")
    print("1. Download your service account JSON file from Google Cloud Console")
    print("2. Move it to: dice_rolling_backend/src/credentials/service-account.json")
    print("3. Run: python test_credentials.py")
    
    return False

def validate_and_copy_service_account(file_path):
    """Validate and copy service account file"""
    try:
        # Read and validate the file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Check if it's a service account file
        if data.get('type') == 'service_account':
            print(f"\n✅ Valid service account file found: {file_path}")
            print(f"   Project ID: {data.get('project_id')}")
            print(f"   Service Account Email: {data.get('client_email')}")
            
            # Copy to the correct location
            target_path = os.path.join('src', 'credentials', 'service-account.json')
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(file_path, target_path)
            
            print(f"✅ Copied to: {target_path}")
            
            print("\n🎯 Next Steps:")
            print("1. Share your Google Sheet with this email:")
            print(f"   {data.get('client_email')}")
            print("2. Give it 'Editor' permissions")
            print("3. Run: python test_credentials.py")
            
            return True
        else:
            print(f"❌ {file_path} is not a service account file (type: {data.get('type')})")
            return False
            
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

if __name__ == "__main__":
    setup_service_account()
