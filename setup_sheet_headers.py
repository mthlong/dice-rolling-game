#!/usr/bin/env python3
"""
Script to show the headers and sample data for your Google Sheet
"""

def show_sheet_setup():
    """Show the recommended setup for your Google Sheet"""
    
    print("🎲 GOOGLE SHEET SETUP INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. Open your Google Sheet:")
    print("   https://docs.google.com/spreadsheets/d/1kiCoNvDBawPpOa2A46EMAHruhcC8LGLf5SCZhX6M4q0/edit")
    
    print("\n2. Add these headers in Row 1 (A1 to H1):")
    headers = ["Timestamp", "Username", "Dice1", "Dice2", "Dice3", "Total Score", "Date", "Time"]
    
    for i, header in enumerate(headers, 1):
        col_letter = chr(64 + i)  # A, B, C, etc.
        print(f"   {col_letter}1: {header}")
    
    print("\n3. Sample data format (Row 2):")
    sample_data = [
        "2025-07-03T08:30:00.000000",
        "player1", 
        "3", 
        "4", 
        "5", 
        "12", 
        "2025-07-03", 
        "08:30:00"
    ]
    
    for i, data in enumerate(sample_data, 1):
        col_letter = chr(64 + i)
        print(f"   {col_letter}2: {data}")
    
    print("\n4. Make sure your sheet is shared:")
    print("   - Click 'Share' button")
    print("   - Change to 'Anyone with the link can view'")
    print("   - Copy the link (should be the same as above)")
    
    print("\n5. Test the integration:")
    print("   - Run the dice rolling game")
    print("   - Roll some dice")
    print("   - Check if data appears in your sheet")
    
    print("\n" + "=" * 50)
    print("Once you've set up the headers, the app will:")
    print("✅ Read existing data from your Google Sheet")
    print("✅ Write new rolls to local storage (fallback)")
    print("✅ Show you the data to manually add to your sheet")

if __name__ == "__main__":
    show_sheet_setup()
