# Google Sheets API Credentials Setup

## Step 1: Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Enable Google Sheets API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

## Step 2: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: `dice-game-sheets`
4. Click "Create and Continue"
5. Skip optional steps and click "Done"

## Step 3: Generate JSON Key

1. Click on your new service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose "JSON" format
5. Download the JSON file
6. **Rename it to `service-account.json`**
7. **Place it in this directory** (`src/credentials/service-account.json`)

## Step 4: Share Your Google Sheet

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1kiCoNvDBawPpOa2A46EMAHruhcC8LGLf5SCZhX6M4q0/edit
2. Click "Share"
3. Add the service account email (from the JSON file)
   - It looks like: `dice-game-sheets@your-project-id.iam.gserviceaccount.com`
4. Give it "Editor" permissions
5. Click "Send"

## Step 5: Test

Once you've placed the `service-account.json` file here, restart the Flask application and test rolling dice. The data should automatically appear in your Google Sheet!

## Security Note

- Never commit the `service-account.json` file to version control
- Keep it secure and private
- The file contains sensitive credentials

## File Structure

```
src/credentials/
├── README.md (this file)
└── service-account.json (your credentials file)
```
