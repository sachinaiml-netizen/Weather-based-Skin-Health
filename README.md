# Weather-based Skin Health Application

## 🧬 AI/ML-Powered Weather-Aware Skincare Intelligence

A comprehensive web application that uses **AI/ML algorithms** to predict potential skin concerns and provides personalized skincare recommendations based on real-time weather conditions.

## 🎯 Problem Statement

Weather conditions such as temperature, humidity, and UV index greatly influence skin health, often leading to issues like dryness, acne, or sunburn. However, users lack personalized insights to protect their skin based on changing weather.

This project develops an **AI/ML-based weather-aware skincare system** that analyzes real-time weather data to **predict potential skin concerns** and provide **personalized skincare recommendations**, promoting better skin health and awareness.

## ✨ Key Features

### 🎥 Real-time Camera Analysis
- **📷 Live Webcam Capture**: Capture skin images directly from your device camera
- **🎯 Face Positioning Guide**: Animated guide circle for perfect photo alignment
- **🔄 Camera Switching**: Toggle between front and back camera (mobile devices)
- **� Instant Snapshot**: One-click photo capture for immediate analysis
- **💡 Smart Lighting Tips**: Guidance for optimal photo conditions

### 🧬 Advanced AI/ML Skin Detection
- **🤖 Computer Vision Analysis**: OpenCV-based multi-factor skin condition detection
- **📊 7 Condition Types**: Detects Acne, Pigmentation, Sunburn, Fungal Infection, Eczema, Dryness, Healthy
- **🎯 Confidence Scores**: Each detection includes confidence percentage (55-95%)
- **🔍 Multi-Color Space Analysis**: RGB, HSV, and LAB color space feature extraction
- **📈 Severity Classification**: High, Moderate, and Low severity levels
- **🏷️ Visual Indicators**: Shows specific indicators like "Redness", "Texture Irregularity", etc.

### 🌍 Precise GPS-Based Weather Integration
- **📍 Exact Location Detection**: Uses GPS coordinates (not just city names)
- **🌡️ Micro-Climate Data**: Weather specific to your exact position (±11 meters)
- **☀️ UV Index Monitoring**: Real-time UV risk categorization
- **💨 Air Quality (AQI)**: PM2.5 and PM10 pollution levels
- **🗺️ Reverse Geocoding**: Shows detailed location (neighborhood, state, coordinates)
- **🌤️ Real-time Updates**: Temperature, humidity, pressure, wind speed

### 💡 Personalized Skincare Recommendations
- **🎯 Priority Actions**: Top 3 immediate actions based on your skin + weather
- **🧴 Custom Routine**: Step-by-step morning/evening skincare routine
- **🛒 Product Suggestions**: 15+ specific product recommendations
- **🌟 Lifestyle Tips**: Diet, hydration, sleep advice for better skin
- **⚠️ Weather Warnings**: Alerts for UV exposure, pollution, extreme conditions
- **📊 Risk Analysis**: Combined skin condition + environmental factor assessment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sachinaiml-netizen/Weather-based-Skin-Health.git
cd Weather-based-Skin-Health
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
   - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
   - Create a `.env` file in the project root:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

## Usage

### Local Development

1. Start the Flask application:
```bash
python app_enhanced.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Use the application:
   - Get weather data using "Use My Location" or enter a city name
   - Upload a skin image or use your camera to capture one
   - Get AI-powered skin analysis and personalized recommendations

### Deploy to Web (Make it Accessible Online)

#### Option 1: Render (Recommended - Free & Easy)

1. **Push your code to GitHub** (already done ✅)

2. **Go to [Render.com](https://render.com)** and sign up

3. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select repository: `Weather-based-Skin-Health`
   - Configure:
     - **Name**: `weather-skin-analyzer`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app_enhanced:app`
   
4. **Add Environment Variable**:
   - Go to "Environment" tab
   - Add: `WEATHER_API_KEY` = `your_openweathermap_api_key`

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://weather-skin-analyzer.onrender.com`

#### Option 2: Vercel (Fast Deployment)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd Weather-based-Skin-Health
vercel

# Follow the prompts, your app will be live at: https://your-app.vercel.app
```

#### Option 3: Heroku

```bash
# Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli

# Login and deploy
heroku login
heroku create your-skin-analyzer
git push heroku main
heroku config:set WEATHER_API_KEY=your_api_key_here
heroku open
```

#### Option 4: Quick Share (Temporary - ngrok)

For quick temporary sharing without deployment:

```bash
# Download ngrok from https://ngrok.com
# Start your Flask app, then in another terminal:
ngrok http 5000

# Share the https://xxx.ngrok.io URL with anyone
# Works only while your server is running
```

## API Endpoints

- `GET /` - Main application page
- `POST /get_recommendations` - Get skincare recommendations for a city
- `GET /health` - Health check endpoint

## Weather-based Recommendations

The application analyzes multiple weather factors:

### Temperature-based
- **Cold (<10°C)**: Rich moisturizers, protective creams
- **Cool (10-20°C)**: Balanced moisturizing routine
- **Moderate (20-30°C)**: Lightweight moisturizers
- **Hot (>30°C)**: Oil-free, lightweight products

### Humidity-based
- **Low (<30%)**: Extra hydration, hyaluronic acid
- **Moderate (30-60%)**: Standard skincare routine
- **High (>60%)**: Oil-control, non-comedogenic products

### Weather Condition-based
- **Sunny**: High SPF sunscreen, sun protection
- **Rainy**: Water-resistant products, deep cleansing
- **Snowy**: Extra sun protection (UV reflection), barrier creams
- **Cloudy**: Daily SPF (UV penetrates clouds)
- **Windy**: Protective barrier creams, windburn prevention

### Modern Dark-Themed UI
- 🌙 **Aesthetic Dark Theme**: Professional dark mode design
- ✨ **Animated Background**: Twinkling stars and smooth animations
- 🎨 **Gradient Accents**: Cyberpunk-inspired color scheme
- 📱 **Fully Responsive**: Works on desktop, tablet, and mobile
- 🎭 **Interactive Elements**: Smooth transitions and hover effects
- 🚀 **Modern Typography**: Clean Inter font family

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0**: Python web framework
- **Python 3.14+**: Core programming language
- **OpenWeatherMap API**: Real-time weather data with reverse geocoding
- **Gunicorn 21.2.0**: Production WSGI server

### AI/ML & Computer Vision
- **OpenCV 4.11.0**: Advanced image processing and analysis
- **NumPy 2.3.4**: Numerical computing for feature extraction
- **scikit-learn 1.7.2**: Machine learning utilities
- **Pillow 12.0.0**: Image handling and preprocessing
- **Multi-Color Space Analysis**: RGB, HSV, LAB feature extraction
- **Edge Detection**: Canny edge detection for texture analysis
- **Statistical Analysis**: Mean, variance, standard deviation calculations

### Frontend
- **HTML5**: Semantic markup with modern accessibility
- **CSS3**: Gradient backgrounds, animations, responsive design
- **Vanilla JavaScript (ES6+)**: Camera API, geolocation, async operations
- **MediaDevices API**: WebRTC camera access
- **Canvas API**: Image capture and processing
- **Geolocation API**: GPS coordinate detection
- **Google Fonts**: Inter typography

### APIs & Services
- **OpenWeatherMap Weather API**: Current weather conditions
- **OpenWeatherMap UV API**: Real-time UV index
- **OpenWeatherMap Air Pollution API**: AQI and PM2.5/PM10 data
- **OpenWeatherMap Geocoding API**: Reverse geocoding for precise location names

### Development Tools
- **python-dotenv**: Environment variable management
- **Werkzeug 3.0.1**: WSGI utilities
- **Git & GitHub**: Version control and collaboration

## Project Structure

```
Weather-based-Skin-Health/
│
├── app_enhanced.py           # Main Flask application with AI/ML integration
├── skin_model.py            # OpenCV-based skin condition classifier
├── weather_api.py           # Weather API integration (UV, AQI, geocoding)
├── recommendations_engine.py # AI recommendation generation (500+ lines)
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python version for deployment
├── Procfile                # Heroku deployment config
├── render.yaml             # Render deployment config
├── vercel.json             # Vercel deployment config
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
├── README.md              # Documentation
│
├── static/
│   ├── css/
│   │   ├── style.css      # Original styles
│   │   └── analyzer.css   # Modern gradient UI with dark theme
│   └── js/
│       ├── main.js        # Original JavaScript
│       ├── analyzer.js    # Enhanced analyzer with camera support
│       └── camera.js      # Camera manager module (190+ lines)
│
├── templates/
│   ├── index.html         # Original home page
│   ├── home.html          # Landing page
│   ├── weather.html       # Weather display
│   ├── image_analysis.html # Image upload page
│   └── analyzer.html      # Main AI analyzer interface (camera + upload)
│
└── uploads/              # Temporary image uploads (auto-created)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Developed by Sachin

## Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Skincare recommendations based on dermatological best practices

## Future Enhancements

- [x] UV Index API integration
- [x] Air quality index integration
- [x] Real-time webcam face analysis
- [x] Advanced AI/ML skin condition detection
- [x] GPS-based precise location detection
- [ ] User accounts and preferences
- [ ] Skin condition tracking history
- [ ] Weekly forecast and skincare planning
- [ ] Mobile app version (React Native)
- [ ] Multi-language support
- [ ] Dermatologist consultation API
- [ ] Product purchase integration
- [ ] Social sharing features
- [ ] Skin type quiz and personalization
