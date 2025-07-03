"""
Google Sheets integration service for dice rolling history.
Real implementation using Google Sheets API.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
import logging
import requests

# Google Sheets API imports
try:
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials
    from google.auth.exceptions import DefaultCredentialsError
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    logging.warning("Google Sheets API libraries not available. Using fallback mode.")

class GoogleSheetsService:
    def __init__(self):
        # Your Google Sheet ID from the URL
        self.SPREADSHEET_ID = '1kiCoNvDBawPpOa2A46EMAHruhcC8LGLf5SCZhX6M4q0'
        self.RANGE_NAME = 'Sheet1!A1:H1000'  # Fixed range format

        # CSV export URL for public reading
        self.CSV_EXPORT_URL = f'https://docs.google.com/spreadsheets/d/{self.SPREADSHEET_ID}/export?format=csv&gid=0'

        # Fallback to mock data storage if Google Sheets API is not available
        self.data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sheets_data.json')
        self.ensure_data_directory()

        # Initialize Google Sheets service
        self.service = None
        self.use_fallback = True

        try:
            self._initialize_sheets_service()
        except Exception as e:
            logging.warning(f"Could not initialize Google Sheets service: {e}. Using fallback mode.")
            self.use_fallback = True
            self.service = None

    def _initialize_sheets_service(self):
        """Initialize Google Sheets service with authentication"""
        if not GOOGLE_SHEETS_AVAILABLE:
            raise Exception("Google Sheets API libraries not installed")

        # Try different authentication methods
        try:
            # Method 1: Try to use service account credentials from environment variable
            credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if credentials_json:
                import json
                from google.oauth2.service_account import Credentials
                creds_info = json.loads(credentials_json)
                creds = Credentials.from_service_account_info(
                    creds_info,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.service = build('sheets', 'v4', credentials=creds)
                self.use_fallback = False
                logging.info("Google Sheets service initialized with service account credentials from environment")
                return
        except Exception as e:
            logging.info(f"Service account credentials from environment not available: {e}")

        try:
            # Method 2: Try to use service account credentials file
            credentials_path = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'service-account.json')
            if os.path.exists(credentials_path):
                from google.oauth2.service_account import Credentials
                creds = Credentials.from_service_account_file(
                    credentials_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.service = build('sheets', 'v4', credentials=creds)
                self.use_fallback = False
                logging.info("Google Sheets service initialized with service account credentials from file")
                return
        except Exception as e:
            logging.info(f"Service account credentials file not available: {e}")

        try:
            # Method 2: Try to use default credentials
            from google.auth import default
            creds, _ = default()
            self.service = build('sheets', 'v4', credentials=creds)
            self.use_fallback = False
            logging.info("Google Sheets service initialized with default credentials")
            return
        except Exception as e:
            logging.info(f"Default credentials not available: {e}")

        try:
            # Method 3: Try without credentials for public sheets (read-only)
            # This will only work for reading publicly shared sheets
            self.service = build('sheets', 'v4', developerKey=None)
            self.use_fallback = False
            logging.info("Using public Google Sheets access (read-only)")
            return
        except Exception as e:
            logging.error(f"Failed to initialize Google Sheets service: {e}")
            raise e

    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        data_dir = os.path.dirname(self.data_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _read_from_public_sheet(self) -> List[Dict[str, Any]]:
        """Read data from publicly accessible Google Sheet via CSV export"""
        try:
            response = requests.get(self.CSV_EXPORT_URL, timeout=10)
            response.raise_for_status()

            # Parse CSV content
            import csv
            import io

            csv_content = response.text
            reader = csv.reader(io.StringIO(csv_content))

            records = []
            headers = None

            for i, row in enumerate(reader):
                if i == 0:
                    # Assume first row is headers or skip if empty
                    if row and any(cell.strip() for cell in row):
                        headers = row
                    continue

                if len(row) >= 6:  # Ensure we have enough columns
                    try:
                        record = {
                            'timestamp': row[0] if len(row) > 0 else '',
                            'username': row[1] if len(row) > 1 else '',
                            'dice1': int(row[2]) if len(row) > 2 and row[2].strip() else 0,
                            'dice2': int(row[3]) if len(row) > 3 and row[3].strip() else 0,
                            'dice3': int(row[4]) if len(row) > 4 and row[4].strip() else 0,
                            'total_score': int(row[5]) if len(row) > 5 and row[5].strip() else 0,
                            'date': row[6] if len(row) > 6 else '',
                            'time': row[7] if len(row) > 7 else ''
                        }
                        records.append(record)
                    except (ValueError, IndexError) as e:
                        logging.warning(f"Skipping invalid row: {row}, error: {e}")
                        continue

            logging.info(f"Successfully read {len(records)} records from public Google Sheet")
            return records

        except Exception as e:
            logging.error(f"Failed to read from public Google Sheet: {e}")
            return []
            
    def load_data(self) -> List[Dict[str, Any]]:
        """Load existing data from mock storage"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_data(self, data: List[Dict[str, Any]]):
        """Save data to mock storage"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_dice_roll_record(self, username: str, dice1: int, dice2: int, dice3: int,
                           total_score: int, timestamp: str = None) -> bool:
        """
        Add a dice roll record to the Google Sheet

        Args:
            username: Player's username
            dice1, dice2, dice3: Individual dice values
            total_score: Sum of all dice
            timestamp: When the roll occurred (ISO format)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if timestamp is None:
                timestamp = datetime.utcnow().isoformat()

            # Parse timestamp for date and time
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            date_str = dt.strftime('%Y-%m-%d')
            time_str = dt.strftime('%H:%M:%S')

            # Try to write to Google Sheets first
            if not self.use_fallback and self.service:
                try:
                    # Prepare the row data
                    row_data = [timestamp, username, dice1, dice2, dice3, total_score, date_str, time_str]

                    # Append to the sheet
                    body = {
                        'values': [row_data]
                    }

                    # Try different range formats
                    ranges_to_try = ['A:H', 'Sheet1!A:H', 'A1:H']

                    for range_name in ranges_to_try:
                        try:
                            result = self.service.spreadsheets().values().append(
                                spreadsheetId=self.SPREADSHEET_ID,
                                range=range_name,
                                valueInputOption='RAW',
                                insertDataOption='INSERT_ROWS',
                                body=body
                            ).execute()
                            break  # Success, exit the loop
                        except Exception as range_error:
                            if range_name == ranges_to_try[-1]:  # Last attempt
                                raise range_error  # Re-raise the error
                            continue  # Try next range format

                    logging.info(f"Successfully added row to Google Sheets: {result.get('updates', {}).get('updatedRows', 0)} rows updated")

                    # Also save to fallback for consistency
                    self._save_to_fallback(username, dice1, dice2, dice3, total_score, timestamp)
                    return True

                except Exception as e:
                    logging.error(f"Failed to write to Google Sheets: {e}")
                    # Fall back to local storage
                    return self._save_to_fallback(username, dice1, dice2, dice3, total_score, timestamp)
            else:
                # Use fallback method
                logging.info("Using fallback storage (Google Sheets service not available)")
                return self._save_to_fallback(username, dice1, dice2, dice3, total_score, timestamp)

        except Exception as e:
            logging.error(f"Error in add_dice_roll_record: {e}")
            return False

    def _save_to_fallback(self, username: str, dice1: int, dice2: int, dice3: int,
                         total_score: int, timestamp: str) -> bool:
        """Save to local JSON file as fallback"""
        try:
            # Load existing data
            data = self.load_data()

            # Create new record
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            new_record = {
                'timestamp': timestamp,
                'username': username,
                'dice1': dice1,
                'dice2': dice2,
                'dice3': dice3,
                'total_score': total_score,
                'date': dt.strftime('%Y-%m-%d'),
                'time': dt.strftime('%H:%M:%S')
            }

            # Add to data
            data.append(new_record)

            # Save updated data
            self.save_data(data)

            return True

        except Exception as e:
            logging.error(f"Error in fallback save: {e}")
            return False
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """Get all dice roll records from the Google Sheet"""
        # First try to read from public Google Sheet
        public_records = self._read_from_public_sheet()
        if public_records:
            return public_records

        # If public access fails, try authenticated API
        if not self.use_fallback and self.service:
            try:
                # Try different range formats for reading
                ranges_to_try = ['A:H', 'Sheet1!A:H', 'A1:H1000']
                result = None

                for range_name in ranges_to_try:
                    try:
                        result = self.service.spreadsheets().values().get(
                            spreadsheetId=self.SPREADSHEET_ID,
                            range=range_name
                        ).execute()
                        break  # Success, exit the loop
                    except Exception as range_error:
                        if range_name == ranges_to_try[-1]:  # Last attempt
                            raise range_error  # Re-raise the error
                        continue  # Try next range format

                values = result.get('values', [])
                if not values:
                    return self.load_data()

                # Convert to our expected format
                records = []
                for row in values[1:]:  # Skip header row if present
                    if len(row) >= 6:  # Ensure we have enough columns
                        try:
                            record = {
                                'timestamp': row[0] if len(row) > 0 else '',
                                'username': row[1] if len(row) > 1 else '',
                                'dice1': int(row[2]) if len(row) > 2 and row[2] else 0,
                                'dice2': int(row[3]) if len(row) > 3 and row[3] else 0,
                                'dice3': int(row[4]) if len(row) > 4 and row[4] else 0,
                                'total_score': int(row[5]) if len(row) > 5 and row[5] else 0,
                                'date': row[6] if len(row) > 6 else '',
                                'time': row[7] if len(row) > 7 else ''
                            }
                            records.append(record)
                        except (ValueError, IndexError) as e:
                            logging.warning(f"Skipping invalid row: {row}, error: {e}")
                            continue

                return records

            except Exception as e:
                logging.error(f"Failed to read from Google Sheets API: {e}")
                # Fall back to local data
                return self.load_data()
        else:
            # Use local fallback data
            return self.load_data()
    
    def get_records_by_username(self, username: str) -> List[Dict[str, Any]]:
        """Get all records for a specific username"""
        data = self.load_data()
        return [record for record in data if record.get('username') == username]
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top players by highest score"""
        data = self.load_data()
        
        # Group by username and find highest score for each
        user_scores = {}
        for record in data:
            username = record.get('username')
            score = record.get('total_score', 0)
            
            if username not in user_scores or score > user_scores[username]['highest_score']:
                user_scores[username] = {
                    'username': username,
                    'highest_score': score,
                    'timestamp': record.get('timestamp')
                }
        
        # Sort by highest score and return top results
        leaderboard = sorted(user_scores.values(), key=lambda x: x['highest_score'], reverse=True)
        return leaderboard[:limit]
    
    def clear_all_data(self) -> bool:
        """Clear all data (for testing purposes)"""
        try:
            self.save_data([])
            return True
        except Exception as e:
            return False

    def export_for_google_sheets(self) -> str:
        """Export current data in a format suitable for copy-pasting to Google Sheets"""
        data = self.load_data()
        if not data:
            return "No data to export"

        # Create CSV format
        lines = []
        # Add header
        lines.append("Timestamp,Username,Dice1,Dice2,Dice3,Total Score,Date,Time")

        # Add data rows
        for record in data:
            line = f"{record.get('timestamp', '')},{record.get('username', '')},{record.get('dice1', 0)},{record.get('dice2', 0)},{record.get('dice3', 0)},{record.get('total_score', 0)},{record.get('date', '')},{record.get('time', '')}"
            lines.append(line)

        return "\n".join(lines)

    def get_latest_rolls_for_sheets(self, limit: int = 10) -> List[List[str]]:
        """Get latest rolls formatted for Google Sheets (as rows)"""
        data = self.load_data()
        if not data:
            return []

        # Sort by timestamp (newest first) and limit
        sorted_data = sorted(data, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]

        # Convert to rows format
        rows = []
        for record in sorted_data:
            row = [
                record.get('timestamp', ''),
                record.get('username', ''),
                str(record.get('dice1', 0)),
                str(record.get('dice2', 0)),
                str(record.get('dice3', 0)),
                str(record.get('total_score', 0)),
                record.get('date', ''),
                record.get('time', '')
            ]
            rows.append(row)

        return rows

# Global instance
sheets_service = GoogleSheetsService()

