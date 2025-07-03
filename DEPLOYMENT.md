# 🚀 Deployment Guide - Dice Rolling Game

## 📋 Pre-Deployment Checklist

✅ **Data Cleared**: All test data has been reset
✅ **Google Sheets Integration**: Working with service account
✅ **Dependencies**: Updated requirements.txt
✅ **Configuration**: Environment-ready main.py

## 🌐 Deployment Options

### Option 1: Railway (Recommended - Free & Easy)

1. **Create Railway Account**: https://railway.app/
2. **Connect GitHub**: Link your GitHub account
3. **Deploy from GitHub**:
   - Create a new GitHub repository
   - Push your code to GitHub
   - Connect Railway to your repository
   - Railway will auto-deploy using `railway.json`

4. **Add Environment Variables**:
   - `FLASK_ENV=production`
   - Upload your `service-account.json` as a file

### Option 2: Render (Free Tier Available)

1. **Create Render Account**: https://render.com/
2. **Create Web Service**:
   - Connect your GitHub repository
   - Use `render.yaml` configuration
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python src/main.py`

### Option 3: Heroku (Easy but Paid)

1. **Create Heroku Account**: https://heroku.com/
2. **Install Heroku CLI**
3. **Deploy**:
   ```bash
   heroku create your-dice-game
   git push heroku main
   ```

### Option 4: Vercel (Serverless)

1. **Create Vercel Account**: https://vercel.com/
2. **Connect GitHub repository**
3. **Uses `vercel.json` configuration**

## 🔧 Environment Setup for Deployment

### Required Files (Already Created):
- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration
- `runtime.txt` - Python version
- `railway.json` - Railway configuration
- `render.yaml` - Render configuration
- `vercel.json` - Vercel configuration

### Service Account Credentials:
- Upload `src/credentials/service-account.json` to your deployment platform
- Or set as environment variable (base64 encoded)

## 📱 Quick Deploy with Railway (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app/
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically deploy!

3. **Upload Credentials**:
   - In Railway dashboard, go to your service
   - Go to "Variables" tab
   - Upload `service-account.json` file

4. **Get Your URL**:
   - Railway will provide a URL like: `https://your-app.railway.app`

## 🎯 Post-Deployment

1. **Test the deployment**:
   - Visit your deployed URL
   - Roll some dice
   - Check your Google Sheet for data

2. **Share your game**:
   - Your game will be live at the provided URL
   - Players can access it from anywhere!

## 🔒 Security Notes

- Service account credentials are securely stored
- Google Sheet is only accessible via your service account
- No sensitive data is exposed in the frontend

## 📊 Monitoring

- Check your Google Sheet for real-time data
- Monitor deployment logs on your chosen platform
- Use the `/api/sheets/history` endpoint to verify data flow

Your dice rolling game is now ready for the world! 🎲✨
