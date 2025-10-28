# Weather-based Skin Health Application - Setup Guide

## Project Overview
This application provides personalized skincare recommendations based on real-time weather conditions.

## Features Implemented ✅
- ✅ Real-time weather data integration using OpenWeatherMap API
- ✅ Temperature-based skincare recommendations (cold, cool, moderate, hot)
- ✅ Humidity-based product suggestions
- ✅ Weather condition analysis (sunny, rainy, snowy, cloudy, windy)
- ✅ Personalized product recommendations
- ✅ Health warnings for extreme conditions
- ✅ Beautiful, responsive web interface
- ✅ RESTful API endpoints

## Quick Start

### 1. Get OpenWeatherMap API Key
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### 2. Configure the Application
Edit the `.env` file and add your API key:
```
WEATHER_API_KEY=your_actual_api_key_here
```

### 3. Run the Application
```powershell
# Make sure you're in the project directory
cd d:\mini_project_5thsem\Weather-based-Skin-Health

# Activate virtual environment (if using venv)
D:/mini_project_5thsem/.venv/Scripts/python.exe

# Run the Flask app
D:/mini_project_5thsem/.venv/Scripts/python.exe app.py
```

### 4. Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. **Enter Your City**: Type your city name in the search box
2. **Get Recommendations**: Click "Get Recommendations" button
3. **View Results**: The app will display:
   - Current weather conditions
   - Temperature, humidity, and wind speed
   - Personalized skincare tips
   - Recommended products
   - Important warnings (if any)

## Project Structure
```
Weather-based-Skin-Health/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API key)
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
├── Procfile                   # For deployment (Heroku)
├── runtime.txt                # Python version for deployment
│
├── static/
│   ├── css/
│   │   └── style.css          # Application styles
│   └── js/
│       └── script.js          # Frontend JavaScript
│
└── templates/
    └── index.html             # Main HTML template
```

## API Endpoints

### GET /
Returns the main application page.

### POST /get_recommendations
Request body:
```json
{
  "city": "New York"
}
```

Response:
```json
{
  "city": "New York",
  "country": "US",
  "temperature": 15.5,
  "humidity": 65,
  "weather_condition": "Clear",
  "weather_description": "clear sky",
  "wind_speed": 3.5,
  "skincare_tips": [...],
  "products_recommended": [...],
  "warnings": [...]
}
```

### GET /health
Health check endpoint for monitoring.

## Skincare Recommendation Logic

### Temperature-Based
- **< 10°C (Cold)**: Rich moisturizers, lip balm, protection from wind
- **10-20°C (Cool)**: Medium-weight moisturizers
- **20-30°C (Moderate)**: Lightweight gel moisturizers
- **> 30°C (Hot)**: Oil-free products, mattifying primers

### Humidity-Based
- **< 30% (Low)**: Hyaluronic acid, extra hydration
- **30-60% (Moderate)**: Standard routine
- **> 60% (High)**: Oil-control, non-comedogenic products

### Weather Conditions
- **Sunny**: SPF 30+ sunscreen, reapply every 2 hours
- **Rainy**: Water-resistant products, thorough cleansing
- **Snowy**: SPF 50+ (snow reflects 80% UV), barrier creams
- **Cloudy**: Daily SPF (UV penetrates clouds)
- **Windy (>10 m/s)**: Protective barrier creams

## Technologies Used
- **Backend**: Flask 3.0.0 (Python)
- **API Integration**: OpenWeatherMap API
- **HTTP Client**: Requests library
- **Environment Management**: python-dotenv
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: Custom CSS with gradient backgrounds
- **Deployment Ready**: Gunicorn, Procfile for Heroku

## Troubleshooting

### Issue: "Unable to fetch weather data"
**Solution**: 
- Check your API key is correct in `.env` file
- Verify the city name spelling
- Ensure internet connection is active
- Check API key has been activated (takes ~10 minutes after signup)

### Issue: Module not found
**Solution**:
```powershell
D:/mini_project_5thsem/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

### Issue: Port already in use
**Solution**: Change port in app.py or kill the process using port 5000

## Git Repository
The project has been successfully pushed to:
https://github.com/sachinaiml-netizen/Weather-based-Skin-Health

## Future Enhancements
- [ ] UV Index real-time data
- [ ] Air Quality Index integration
- [ ] User accounts and preferences
- [ ] 7-day forecast with skincare planning
- [ ] Skin type personalization
- [ ] Multi-language support
- [ ] Mobile responsive improvements
- [ ] Progressive Web App (PWA)

## Contributing
Feel free to fork the repository and submit pull requests!

## License
MIT License - Open source project

## Author
Sachin
GitHub: @sachinaiml-netizen

---
**Last Updated**: October 2025
**Status**: Production Ready ✅
