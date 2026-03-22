# Deployment Guide

This guide will help you deploy your appointment system to make it available for everyone to use.

## 🚀 Quick Deployment Options

### Option 1: Vercel (Recommended - Free & Easiest)

**Steps:**
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Add environment variables:
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY`
   - `ATLAS_CONNECTION_STRING`
6. Deploy!

**Benefits:**
- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Custom domain
- ✅ Global CDN
- ✅ Auto-deploy on git push

### Option 2: Render (Free Tier)

**Steps:**
1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Click "New Web Service"
4. Connect your GitHub repository
5. Set build command: `pip install -r requirements.txt && python app.py`
6. Add environment variables
7. Deploy!

**Benefits:**
- ✅ Free tier available
- ✅ Persistent storage
- ✅ Background workers
- ✅ Custom domains

### Option 3: Railway (Free Tier)

**Steps:**
1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project"
4. Deploy from GitHub
5. Add environment variables
6. Deploy!

**Benefits:**
- ✅ Free tier with credits
- ✅ Easy deployment
- ✅ Good performance
- ✅ Database add-ons

## 🔧 Environment Variables Setup

You need to set these environment variables on your chosen platform:

### Required Variables
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ATLAS_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/dbname
```

### How to Get API Keys

**OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up/login
3. Click "Create new secret key"
4. Copy the key

**Google Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

**MongoDB Atlas Connection:**
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a free cluster
3. Click "Connect" → "Connect your application"
4. Choose "Python" and copy the connection string

## 📋 Pre-Deployment Checklist

### ✅ Code Ready
- [x] All deployment files created (Procfile, vercel.json, runtime.txt)
- [x] Environment variables documented
- [x] Dependencies updated in requirements.txt

### ✅ Testing
- [x] Test locally: `python app.py`
- [x] Test all endpoints work
- [x] Test database connection

### ✅ Git Ready
- [x] Code committed to repository
- [x] Ready to push to GitHub

## 🌐 Deployment URLs

After deployment, your app will be available at:
- **Vercel**: `https://your-app-name.vercel.app`
- **Render**: `https://your-app-name.onrender.com`
- **Railway**: `https://your-app-name.up.railway.app`

## 🛠️ Troubleshooting

### Common Issues

**Build Failures:**
- Check all requirements are in requirements.txt
- Verify Python version compatibility
- Check for syntax errors

**Runtime Errors:**
- Verify environment variables are set
- Check database connection
- Review logs for errors

**Database Issues:**
- Ensure IP whitelist includes your deployment platform
- Check connection string format
- Verify database user permissions

## 📞 Support

If you encounter issues:
1. Check the platform logs
2. Verify environment variables
3. Test locally first
4. Check this deployment guide

## 🎉 Success!

Once deployed, your appointment system will be:
- 🌐 Available globally
- 🤖 AI-powered with OpenAI + Gemini
- 🏥 27 doctors across 11 specialties
- 📅 Real-time booking system
- 💾 Connected to MongoDB Atlas

**Your appointment system will be ready for users worldwide!**
