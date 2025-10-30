# 🚀 Deployment Guide

This guide will help you deploy the AI Skin Health Advisor application to various cloud platforms.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Deploy to Vercel](#deploy-to-vercel)
- [Deploy to Render](#deploy-to-render)
- [Deploy to Heroku](#deploy-to-heroku)
- [Environment Variables](#environment-variables)
- [Post-Deployment Configuration](#post-deployment-configuration)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

1. ✅ A GitHub account with this repository forked/pushed
2. ✅ OpenWeatherMap API key ([Get it here](https://openweathermap.org/api))
3. ✅ Git installed on your local machine
4. ✅ Python 3.8+ installed locally (for testing)

---

## Deploy to Vercel

### Method 1: Using Vercel Dashboard (Recommended)

1. **Sign up/Login to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**
   - Click "Add New Project"
   - Select "Import Git Repository"
   - Choose `Weather-based-Skin-Health` repository

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

4. **Set Environment Variables**
   - Click "Environment Variables"
   - Add: `WEATHER_API_KEY` = `your_api_key_here`
   - Apply to: Production, Preview, and Development

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build completion
   - Your app will be live at: `https://your-project-name.vercel.app`

### Method 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd Weather-based-Skin-Health
vercel

# Follow prompts:
# Set up and deploy? Yes
# Which scope? Your account
# Link to existing project? No
# What's your project's name? weather-skin-health
# In which directory is your code located? ./
# Want to override settings? No

# Set environment variable
vercel env add WEATHER_API_KEY production
# Paste your API key when prompted

# Deploy to production
vercel --prod
```

### Vercel Configuration File

The `vercel.json` file is already configured:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

---

## Deploy to Render

### Step-by-Step Instructions

1. **Sign up/Login to Render**
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select `Weather-based-Skin-Health` repository

3. **Configure Service**
   - **Name**: `weather-skin-health` (or your choice)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app
     ```

4. **Set Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Key: `WEATHER_API_KEY`
   - Value: Your OpenWeatherMap API key
   - Click "Add"

5. **Configure Instance Type**
   - **Instance Type**: Free (or paid for better performance)
   - **Auto-Deploy**: Enable (recommended)

6. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for initial deployment
   - Your app will be live at: `https://weather-skin-health.onrender.com`

### Render Configuration Files

**Procfile** (already included):
```
web: gunicorn app:app
```

**runtime.txt** (already included):
```
python-3.9.16
```

---

## Deploy to Heroku

### Prerequisites
- Heroku CLI installed: [Download here](https://devcenter.heroku.com/articles/heroku-cli)

### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create new app
cd Weather-based-Skin-Health
heroku create weather-skin-health

# Set environment variable
heroku config:set WEATHER_API_KEY=your_api_key_here

# Push to Heroku
git push heroku main

# Open app in browser
heroku open

# View logs
heroku logs --tail
```

### Required Files (Already Included)

**Procfile**:
```
web: gunicorn app:app
```

**runtime.txt**:
```
python-3.9.16
```

**requirements.txt**: Includes `gunicorn==21.2.0`

---

## Environment Variables

### Required Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `WEATHER_API_KEY` | OpenWeatherMap API key | [openweathermap.org/api](https://openweathermap.org/api) |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `PORT` | Application port | Platform-specific |

### Setting Environment Variables

**Vercel:**
```bash
vercel env add WEATHER_API_KEY production
```

**Render:**
- Dashboard → Service → Environment → Add Environment Variable

**Heroku:**
```bash
heroku config:set WEATHER_API_KEY=your_key_here
```

---

## Post-Deployment Configuration

### 1. Verify Deployment

Test these endpoints:

```bash
# Health check
curl https://your-app-url.com/health

# Should return: {"status": "healthy"}
```

### 2. Test Features

1. **Weather Analysis**
   - Visit your deployed URL
   - Enter a city name (e.g., "London")
   - Click "Get Recommendations"
   - Verify weather data and recommendations appear

2. **Image Analysis**
   - Upload a sample image (< 5MB)
   - Click "Analyze Skin Condition"
   - Verify analysis results appear

### 3. Custom Domain (Optional)

**Vercel:**
```bash
vercel domains add yourdomain.com
```
Follow DNS configuration instructions

**Render:**
- Dashboard → Service → Settings → Custom Domains
- Add your domain and configure DNS

**Heroku:**
```bash
heroku domains:add yourdomain.com
```

---

## Troubleshooting

### Common Issues

#### 1. Build Fails - Module Not Found

**Error**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
- Ensure module is in `requirements.txt`
- Check Python version compatibility
- Rebuild:
  ```bash
  vercel --prod  # Vercel
  # or
  git push heroku main  # Heroku
  ```

#### 2. Application Error / 503

**Solution**:
- Check logs:
  ```bash
  vercel logs  # Vercel
  heroku logs --tail  # Heroku
  ```
- Verify environment variables are set
- Check `Procfile` and `runtime.txt`

#### 3. Weather API Not Working

**Error**: "Unable to fetch weather data"

**Solution**:
- Verify `WEATHER_API_KEY` is set correctly
- Check API key is active on OpenWeatherMap
- Test API key manually:
  ```bash
  curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
  ```

#### 4. Image Upload Fails

**Solution**:
- Ensure `uploads/` directory exists
- Check file size limits (5MB default)
- Verify Pillow is installed:
  ```bash
  pip list | grep Pillow
  ```

#### 5. Static Files Not Loading

**Solution**:
- Verify `static/` directory structure
- Check `vercel.json` routes configuration
- Clear browser cache
- Check Content-Type headers in browser DevTools

#### 6. CORS Errors

**Solution**:
- Already handled in `app.py` with proper CORS headers
- If issues persist, check browser console for specific errors

### Platform-Specific Issues

#### Vercel

**Issue**: Function size too large

**Solution**: Optimize dependencies in `requirements.txt`

#### Render

**Issue**: Build timeout

**Solution**:
- Increase build timeout in settings
- Optimize `requirements.txt`

#### Heroku

**Issue**: Dyno sleeping (free tier)

**Solution**:
- Upgrade to paid tier, or
- Use uptime monitoring service (e.g., UptimeRobot)

---

## Performance Optimization

### 1. Caching

Add caching for API responses:

```python
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
```

### 2. CDN for Static Files

Use Vercel/Render's built-in CDN for static files

### 3. Database Caching

For production, consider Redis for weather data caching

### 4. Image Compression

Compress uploaded images before processing:

```python
from PIL import Image
img = Image.open(file)
img = img.resize((800, 800), Image.LANCZOS)
```

---

## Monitoring

### Recommended Tools

1. **Uptime Monitoring**
   - UptimeRobot (free)
   - Pingdom
   - StatusCake

2. **Error Tracking**
   - Sentry
   - Rollbar
   - LogRocket

3. **Analytics**
   - Google Analytics
   - Plausible Analytics
   - Fathom Analytics

### Setting Up Monitoring

**Example: UptimeRobot**

1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add New Monitor
   - Type: HTTP(s)
   - URL: `https://your-app-url.com/health`
   - Interval: 5 minutes
3. Set up email/SMS alerts

---

## Scaling

### Vertical Scaling (Single Server)

**Render:**
- Upgrade to paid plan
- Increase instance size

**Heroku:**
```bash
heroku ps:scale web=1:standard-1x
```

### Horizontal Scaling (Multiple Servers)

**Render:**
- Increase instance count in dashboard

**Heroku:**
```bash
heroku ps:scale web=3
```

---

## Security Checklist

- [x] Environment variables for sensitive data
- [x] File upload validation (size, type)
- [x] CORS headers configured
- [x] No hardcoded secrets
- [x] HTTPS enabled (platform default)
- [ ] Rate limiting (optional, add if needed)
- [ ] Input sanitization (optional, add if needed)

---

## Continuous Deployment

### Auto-Deploy from GitHub

**Vercel:**
- Enabled by default
- Push to `main` branch triggers deployment

**Render:**
- Enable "Auto-Deploy" in settings
- Push to `main` branch triggers deployment

**Heroku:**
- Connect to GitHub in dashboard
- Enable automatic deploys

---

## Rollback

### Vercel

```bash
vercel rollback
```

Or use dashboard → Deployments → Previous deployment → Promote to Production

### Render

Dashboard → Service → Deploys → Previous deploy → "Redeploy"

### Heroku

```bash
heroku releases
heroku rollback v123  # Replace with version number
```

---

## Cost Estimates

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Vercel** | 100GB bandwidth/month | $20/month | Serverless, fast deploys |
| **Render** | 750 hours/month | $7/month | Simple deployment, good docs |
| **Heroku** | 550 hours/month | $7/month | Established platform, add-ons |

---

## Support

For deployment issues:

- **Vercel**: [vercel.com/support](https://vercel.com/support)
- **Render**: [render.com/docs](https://render.com/docs)
- **Heroku**: [help.heroku.com](https://help.heroku.com)

For application issues:
- Open issue on [GitHub](https://github.com/sachinaiml-netizen/Weather-based-Skin-Health/issues)

---

## Next Steps

After successful deployment:

1. ✅ Test all features thoroughly
2. ✅ Set up monitoring
3. ✅ Configure custom domain (optional)
4. ✅ Add analytics (optional)
5. ✅ Set up error tracking
6. ✅ Update README with live URL
7. ✅ Share with users!

---

Made with ❤️ for better skin health
