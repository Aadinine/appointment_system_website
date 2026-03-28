# Railway Deployment Guide

## Step 1: Prepare Your Repository
Your project is already configured with the necessary files:
- `pyproject.toml` - Python dependencies
- `Procfile` - Railway process configuration  
- `runtime.txt` - Python version specification
- `railway.json` - Railway deployment settings

## Step 2: Deploy to Railway

### Option A: GitHub Integration (Recommended)
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository: `Aadinine/appointment_system_website`
4. Railway will automatically detect it's a Python project

### Option B: CLI Deployment
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. In your project folder: `railway init`
4. Deploy: `railway up`

## Step 3: Configure Environment Variables
In Railway dashboard, add these environment variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
ATLAS_CONNECTION_STRING=your_mongodb_connection_string_here
```

**Get your API keys from:**
- Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys
- Groq: https://console.groq.com/keys
- MongoDB Atlas: https://cloud.mongodb.com/

## Step 4: Deploy
- Click "Deploy" or Railway will auto-deploy on push
- Wait for deployment to complete (2-3 minutes)
- Your app will be available at: `https://your-app-name.railway.app`

## Step 5: Verify Deployment
1. Visit your Railway URL
2. Test symptom analysis
3. Check debug endpoint: `https://your-app-name.railway.app/debug`
4. Verify MongoDB connection

## Troubleshooting
- **Build fails**: Check Python version in runtime.txt
- **App crashes**: Check environment variables in Railway dashboard
- **Database connection**: Verify MongoDB Atlas allows Railway IP (0.0.0.0/0)

## Features Deployed
✅ Groq AI integration (primary)
✅ OpenAI & Gemini fallback
✅ MongoDB Atlas database
✅ Multi-tier symptom analysis
✅ Doctor booking system
✅ Location-based search
✅ Real-time availability
