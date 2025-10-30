# 🚀 Deployment Guide - Weather-Based Skin Analyzer

## Quick Start: Deploy to the Web in 5 Minutes

### ✅ Prerequisites
- GitHub account (you have this ✅)
- OpenWeatherMap API key
- Your code pushed to GitHub (done ✅)

---

## 🎯 Recommended: Render (100% Free & Easy)

### Step-by-Step Instructions:

#### 1. Sign Up for Render
- Go to **[https://render.com](https://render.com)**
- Click "Get Started" or "Sign Up"
- Sign up with your GitHub account (easiest)

#### 2. Connect Your Repository
- After logging in, click **"New +"** button
- Select **"Web Service"**
- Click **"Connect a repository"**
- Find and select: **`Weather-based-Skin-Health`**
- Click **"Connect"**

#### 3. Configure Your Service
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `weather-skin-analyzer` (or your choice) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app_enhanced:app` |
| **Instance Type** | `Free` |

#### 4. Add Environment Variables
- Scroll down to **"Environment Variables"**
- Click **"Add Environment Variable"**
- Add this:
  ```
  Key: WEATHER_API_KEY
  Value: [paste your OpenWeatherMap API key]
  ```

#### 5. Deploy!
- Click **"Create Web Service"** button
- Wait 2-3 minutes while Render:
  - Clones your repository
  - Installs dependencies
  - Starts your application
- Once done, you'll see: **"Your service is live at https://weather-skin-analyzer.onrender.com"**

#### 6. Access Your Live Website
- Click the provided URL
- Share it with anyone! 🎉
- Your app is now accessible worldwide

### 🔄 Automatic Updates
Render will automatically redeploy whenever you push changes to GitHub!

---

## 🌐 Alternative: Vercel (Very Fast)

### Quick Deploy:

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to project
cd Weather-based-Skin-Health

# Deploy
vercel

# Follow the prompts:
# - Setup and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? weather-skin-analyzer
# - Directory? ./
# - Override settings? No

# Done! You'll get: https://weather-skin-analyzer.vercel.app
```

### Add Environment Variable:
```bash
vercel env add WEATHER_API_KEY production
# Then paste your API key when prompted
```

---

## 🎈 Alternative: Heroku

### Deploy with Heroku CLI:

```bash
# Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create weather-skin-analyzer

# Add environment variable
heroku config:set WEATHER_API_KEY=your_api_key_here

# Deploy
git push heroku main

# Open your app
heroku open

# Your app is live at: https://weather-skin-analyzer.herokuapp.com
```

---

## 🔧 Alternative: Manual Deployment (VPS)

### Using DigitalOcean, AWS EC2, or Google Cloud:

```bash
# SSH into your server
ssh root@your-server-ip

# Clone repository
git clone https://github.com/sachinaiml-netizen/Weather-based-Skin-Health.git
cd Weather-based-Skin-Health

# Install Python and dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variable
echo "WEATHER_API_KEY=your_api_key" > .env

# Install and configure Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app_enhanced:app

# Configure Nginx (reverse proxy)
# Create: /etc/nginx/sites-available/skin-analyzer
sudo nano /etc/nginx/sites-available/skin-analyzer

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/skin-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup systemd service for auto-restart
sudo nano /etc/systemd/system/skin-analyzer.service

# Add:
[Unit]
Description=Weather Skin Analyzer
After=network.target

[Service]
User=root
WorkingDirectory=/root/Weather-based-Skin-Health
Environment="PATH=/root/Weather-based-Skin-Health/venv/bin"
ExecStart=/root/Weather-based-Skin-Health/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app_enhanced:app

[Install]
WantedBy=multi-user.target

# Start service
sudo systemctl start skin-analyzer
sudo systemctl enable skin-analyzer
```

---

## 📱 Quick Share (Temporary - No Deployment)

### Using ngrok (for testing/demos):

```bash
# Download from: https://ngrok.com/download
# Install and authenticate

# Start your Flask app locally
python app_enhanced.py

# In another terminal:
ngrok http 5000

# You'll get a URL like: https://abc123.ngrok.io
# Share this URL with anyone (valid for 2 hours on free plan)
```

---

## 🔐 Important: Environment Variables

All deployment methods need your OpenWeatherMap API key:

```
WEATHER_API_KEY=your_api_key_here
```

Get your free API key:
1. Go to: https://openweathermap.org/api
2. Sign up
3. Navigate to: https://home.openweathermap.org/api_keys
4. Copy your API key

---

## 🐛 Troubleshooting

### Build Fails on Render/Heroku:
- Check `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt`
- Check build logs for specific errors

### App Crashes After Deployment:
- Verify environment variables are set
- Check start command: `gunicorn app_enhanced:app`
- Review application logs

### Camera Not Working on Deployed Site:
- Ensure site uses HTTPS (camera requires secure connection)
- Render/Vercel/Heroku provide HTTPS automatically
- For custom domains, setup SSL certificate

### Weather API Errors:
- Verify API key is correctly set in environment variables
- Check API key is active on OpenWeatherMap dashboard
- Ensure API key has required permissions (weather, UV, air pollution)

---

## 📊 Monitoring Your Deployed App

### Render Dashboard:
- View real-time logs
- Monitor CPU/memory usage
- Check deployment history
- See visitor analytics

### Health Check Endpoint:
Visit: `https://your-app-url.com/health`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-30T...",
  "version": "2.0.0",
  "features": [...]
}
```

---

## 🎉 Success!

Your Weather-Based Skin Analyzer is now live and accessible worldwide!

Share your URL:
- ✅ Render: `https://weather-skin-analyzer.onrender.com`
- ✅ Vercel: `https://weather-skin-analyzer.vercel.app`
- ✅ Heroku: `https://weather-skin-analyzer.herokuapp.com`

---

## 💡 Pro Tips

1. **Custom Domain**: Most platforms allow custom domain setup (yourdomain.com)
2. **SSL Certificate**: Free HTTPS with Let's Encrypt on all platforms
3. **Auto Deploy**: Enable GitHub integration for automatic deployments
4. **Monitoring**: Setup uptime monitoring with services like UptimeRobot
5. **Analytics**: Add Google Analytics or Plausible for visitor tracking

---

## 📞 Need Help?

If you encounter issues:
1. Check the platform-specific logs
2. Review the troubleshooting section above
3. Open an issue on GitHub
4. Contact platform support (Render, Vercel, Heroku)

Happy Deploying! 🚀
