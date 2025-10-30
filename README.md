# Weather-based Skin Health Application

## 🧬 AI/ML-Powered Weather-Aware Skincare Intelligence

A comprehensive web application that uses **AI/ML algorithms** to predict potential skin concerns and provides personalized skincare recommendations based on real-time weather conditions.

## 🎯 Problem Statement

Weather conditions such as temperature, humidity, and UV index greatly influence skin health, often leading to issues like dryness, acne, or sunburn. However, users lack personalized insights to protect their skin based on changing weather.

This project develops an **AI/ML-based weather-aware skincare system** that analyzes real-time weather data to **predict potential skin concerns** and provide **personalized skincare recommendations**, promoting better skin health and awareness.

## ✨ Key Features

### AI/ML Predictions
- **🤖 Intelligent Skin Concern Prediction**: Machine learning model that analyzes multiple weather factors
- **📊 Risk Scoring System**: Calculates risk scores (0-100) for different skin concerns
- **🎯 Confidence Metrics**: Displays AI confidence levels for each prediction
- **🔍 Multi-factor Analysis**: Evaluates temperature, humidity, UV index, wind speed, and weather conditions

### Predicted Skin Concerns
- **🏜️ Dryness**: Predicts dry skin risk based on low humidity, cold temperature, and wind
- **🔴 Acne**: Analyzes high humidity and temperature for breakout risk
- **☀️ Sunburn**: UV index-based sun damage prediction
- **⚠️ Sensitivity**: Extreme weather and wind impact assessment
- **💧 Oiliness**: High humidity and temperature oil production analysis

### Real-time Weather Integration
- Current temperature, humidity, and wind speed
- **UV Index monitoring** with risk categorization
- Weather condition analysis (sunny, rainy, snowy, etc.)
- Location-based data from any city worldwide

### Personalized Recommendations
- Customized skincare tips based on predicted concerns
- Specific product recommendations (cleansers, moisturizers, sunscreens, serums)
- Health warnings for extreme conditions
- Dermatologist-backed advice

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

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter your city name to get personalized skincare recommendations!

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
- **Python 3.11+**: Core programming language
- **OpenWeatherMap API**: Real-time weather data
- **Custom ML Algorithms**: Skin concern prediction models

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations and gradients
- **JavaScript (ES6+)**: Interactive functionality
- **Google Fonts**: Inter typography

### AI/ML Model
- **Multi-factor Analysis**: Temperature, humidity, UV, wind, conditions
- **Weighted Scoring System**: Risk calculation algorithms
- **Confidence Metrics**: Prediction reliability scoring
- **Real-time Processing**: Instant analysis and recommendations

## Project Structure

```
Weather-based-Skin-Health/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore file
├── README.md              # This file
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── script.js      # Frontend JavaScript
│
└── templates/
    └── index.html         # Main HTML template
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

## 📸 Image-Based Skin Analysis

In addition to weather-based predictions, the app now supports **AI-powered image analysis**:

### Features
- **📤 Drag & Drop Upload**: Easy image upload with preview
- **🔬 AI Skin Analysis**: Detects potential skin conditions from photos
- **📊 Confidence Scoring**: Shows reliability of each prediction
- **💡 Personalized Tips**: Recommendations based on detected concerns

### Detected Conditions
- Acne and breakouts
- Redness and sensitivity
- Dryness and dehydration
- Dark spots and pigmentation
- Oiliness

### Usage
1. Click the upload area or drag an image (JPG, PNG, JPEG)
2. Maximum file size: 5MB
3. Click "Analyze Skin Condition"
4. View results with confidence scores and recommendations

## 🚀 Deployment

This application is ready to deploy on multiple platforms:

### Deploy to Vercel ▲

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/sachinaiml-netizen/Weather-based-Skin-Health)

```bash
# Using Vercel CLI
npm install -g vercel
vercel login
vercel
```

**Environment Variables**: Set `WEATHER_API_KEY` in Vercel dashboard

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Configuration**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Add environment variable: `WEATHER_API_KEY`

### Deploy to Heroku

```bash
heroku create weather-skin-health
heroku config:set WEATHER_API_KEY=your_api_key_here
git push heroku main
```

📖 **Detailed deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📋 Requirements

```
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
Pillow==12.0.0
```

## 🔧 Configuration Files

- **vercel.json**: Vercel deployment configuration
- **Procfile**: Process configuration for Heroku/Render
- **runtime.txt**: Python version specification
- **.env.example**: Example environment variables

## Future Enhancements

- [x] UV Index API integration ✅
- [x] Image-based skin analysis ✅
- [x] AI/ML prediction models ✅
- [x] Dark theme UI ✅
- [ ] User accounts and preferences
- [ ] Weekly forecast and skincare planning
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Air quality index integration
- [ ] Advanced AI models (CNN, transfer learning)
