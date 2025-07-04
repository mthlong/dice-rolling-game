# 🔧 Google Sheets Integration Setup

## 📋 Quick Setup Checklist

- [ ] Create Google Cloud Project
- [ ] Enable Google Sheets API
- [ ] Create Service Account
- [ ] Download Service Account JSON
- [ ] Share Google Sheet with Service Account
- [ ] Add Credentials to Railway

## 🚀 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create New Project** or select existing one
3. **Note your Project ID**

### Step 2: Enable Google Sheets API

1. **Go to APIs & Services** → **Library**
2. **Search for "Google Sheets API"**
3. **Click "Enable"**

### Step 3: Create Service Account

1. **Go to APIs & Services** → **Credentials**
2. **Click "Create Credentials"** → **Service Account**
3. **Fill in details**:
   - Name: `dice-game-sheets`
   - Description: `Service account for dice rolling game`
4. **Click "Create and Continue"**
5. **Skip role assignment** (click "Continue")
6. **Click "Done"**

### Step 4: Download Service Account JSON

1. **Find your service account** in the list
2. **Click on it** to open details
3. **Go to "Keys" tab**
4. **Click "Add Key"** → **Create New Key**
5. **Select "JSON"** format
6. **Download the file** (keep it secure!)

### Step 5: Share Google Sheet

1. **Open your Google Sheet**: https://docs.google.com/spreadsheets/d/1kiCoNvDBawPpOa2A46EMAHruhcC8LGLf5SCZhX6M4q0/edit
2. **Click "Share" button**
3. **Add the service account email**:
   - Find the email in your JSON file: `"client_email": "dice-game-sheets@your-project.iam.gserviceaccount.com"`
   - Paste this email in the share dialog
4. **Set permission to "Editor"**
5. **Click "Send"**

### Step 6: Add Credentials to Railway

1. **Go to Railway Dashboard** → Your Project → **Variables**
2. **Add new variable**:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value**: Copy the ENTIRE content of your JSON file
   
   Example:
   ```json
   {"type": "service_account", "project_id": "your-project-123", "private_key_id": "abc123", "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n", "client_email": "dice-game-sheets@your-project.iam.gserviceaccount.com", "client_id": "123456789", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dice-game-sheets%40your-project.iam.gserviceaccount.com"}
   ```

3. **Save the variable**
4. **Redeploy your application**

## 🧪 Testing the Setup

### Test Endpoints

After deployment, test these URLs:

```bash
# Check Google Sheets status
https://your-app.railway.app/api/sheets/status

# Test dice roll (should write to sheets)
POST https://your-app.railway.app/api/dice/roll
Body: {"username": "testuser"}

# Check if data appears in sheets
https://your-app.railway.app/api/sheets/history
```

### Expected Results

1. **`/api/sheets/status`** should return:
   ```json
   {
     "service_available": true,
     "fallback_mode": false,
     "has_env_credentials": true,
     "test_read_success": true
   }
   ```

2. **Dice roll** should return:
   ```json
   {
     "roll": {...},
     "ranking": {...},
     "sheets_success": true,
     "sheets_error": null
   }
   ```

3. **Google Sheet** should show new rows with dice roll data

## 🔍 Troubleshooting

### Common Issues

1. **"Service account credentials not available"**
   - Check that `GOOGLE_APPLICATION_CREDENTIALS_JSON` is set in Railway
   - Verify the JSON is valid (no extra spaces/characters)

2. **"Permission denied"**
   - Make sure you shared the sheet with the service account email
   - Check the service account has "Editor" permissions

3. **"Sheets API not enabled"**
   - Go to Google Cloud Console → APIs & Services → Library
   - Search for "Google Sheets API" and enable it

4. **"Invalid credentials"**
   - Re-download the service account JSON
   - Make sure you're using the correct project

### Debug Commands

```bash
# Check environment variable is set
echo $GOOGLE_APPLICATION_CREDENTIALS_JSON

# Test API endpoints
curl https://your-app.railway.app/api/sheets/status
```

## 📞 Need Help?

If you're still having issues:
1. Check the Railway deployment logs
2. Test the `/api/sheets/status` endpoint
3. Verify your Google Sheet is publicly accessible
4. Make sure the service account email is added to the sheet

Your Google Sheet URL: https://docs.google.com/spreadsheets/d/1kiCoNvDBawPpOa2A46EMAHruhcC8LGLf5SCZhX6M4q0/edit
