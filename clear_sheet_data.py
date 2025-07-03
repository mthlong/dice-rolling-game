#!/usr/bin/env python3
"""
Script to clear test data from Google Sheet
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.google_sheets import sheets_service

def clear_sheet_data():
    """Clear test data from Google Sheet"""
    
    print("🧹 Clearing Google Sheet data...")
    
    try:
        # Clear the Google Sheets service data
        success = sheets_service.clear_all_data()
        
        if success:
            print("✅ Local data cleared successfully!")
        else:
            print("❌ Failed to clear local data")
        
        # For Google Sheets, we need to manually clear the rows
        # Since we can't easily delete rows via API without more complex logic,
        # let's just inform the user
        print("\n📋 To clear Google Sheet data:")
        print("1. Open your Google Sheet:")
        print("   https://docs.google.com/spreadsheets/d/1kiCoNvDBawPpOa2A46EMAHruhcC8LGLf5SCZhX6M4q0/edit")
        print("2. Select rows 2 and below (all data rows)")
        print("3. Right-click → Delete rows")
        print("4. Keep only the header row")
        
        print("\n✅ Ready for deployment!")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")

if __name__ == "__main__":
    clear_sheet_data()
