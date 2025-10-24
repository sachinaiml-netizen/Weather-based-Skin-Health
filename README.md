# SkinGuard - Weather-Based Skin Health Advisory

A comprehensive web application that provides weather-based skin health advisories to help users understand and prevent environmental impacts on their skin.

## 🌟 Features

### Core Functionality
- **Real-time Weather Analysis**: Fetches current weather data based on user location
- **Manual Weather Input**: Allows users to input custom weather parameters
- **Comprehensive Risk Assessment**: Analyzes multiple environmental factors:
  - UV radiation and skin cancer risks
  - Humidity-related fungal infections
  - Temperature impact on eczema and skin dryness
  - Air pollution and premature aging
  - Rain and moisture-related conditions

### Health-Focused Approach
- Medical education over product marketing
- Science-based dermatological recommendations
- Prevention-focused lifestyle tips
- Awareness of serious skin conditions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- OpenWeatherMap API key (free tier available)

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd project_sachin
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   ```bash
   copy .env.example .env
   ```
   - Edit `.env` and add your OpenWeatherMap API key:
   ```
   WEATHER_API_KEY=your_actual_api_key_here
   SECRET_KEY=change_this_to_random_string
   ```

5. **Get your free API key**
   - Visit: https://openweathermap.org/api
   - Sign up for a free account
   - Navigate to API keys section
   - Copy your API key to the `.env` file

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   - Navigate to: http://localhost:5000
   - The application should now be running!

## 📁 Project Structure

```
project_sachin/
├── app.py                 # Flask backend with API routes and analysis logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── dashboard.html    # Analysis dashboard
│   └── about.html        # About page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Modern responsive styling
    └── js/
        ├── main.js       # Core JavaScript utilities
        └── dashboard.js  # Dashboard functionality
```

## 🎯 How It Works

### 1. Location-Based Analysis
- Enter your city name
- System fetches real-time weather data
- Analyzes environmental factors
- Provides personalized health advisories

### 2. Manual Input Analysis
- Input temperature, humidity, UV index, and air quality
- Useful for planning trips or checking specific conditions
- Same comprehensive analysis as location-based

### 3. Risk Assessment Categories

#### UV Radiation
- Monitors UV index levels
- Warns about skin cancer risks
- Provides sun protection guidelines

#### Humidity
- Detects fungal infection risks
- Identifies acne-prone conditions
- Offers moisture management tips

#### Temperature
- Identifies eczema triggers
- Warns about heat rash conditions
- Provides cold weather protection

#### Air Pollution
- Monitors air quality index
- Warns about premature aging
- Recommends antioxidant protection

## 🔒 Privacy & Safety

- **No data collection**: Your queries are not stored
- **No tracking**: We don't track user behavior
- **No product sales**: Pure educational platform
- **Medical Disclaimer**: This is not medical advice - consult dermatologists for serious concerns

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: OpenWeatherMap API
- **Styling**: Custom CSS with modern gradients and animations
- **Icons**: Font Awesome 6

## 🎨 Design Features

- Modern gradient-based UI
- Fully responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Accessible color schemes
- Intuitive user interface

## 📋 API Endpoints

### GET `/`
Home page with feature overview

### GET `/dashboard`
Analysis dashboard interface

### GET `/about`
Information about the platform

### POST `/api/analyze`
Main analysis endpoint
```json
// Location-based request
{
  "location": "London"
}

// Manual input request
{
  "manual": true,
  "temperature": 25,
  "humidity": 60,
  "uvi": 5,
  "aqi": 50,
  "weather": "Clear"
}
```

### GET `/api/locations`
Returns popular city locations for quick access

## 🔮 Future Development Goals

- **AI-Powered Skin Detection**: Upload photos for condition analysis
- **Machine Learning Personalization**: Adaptive recommendations based on skin type
- **Smart Notifications**: Proactive alerts for risky conditions
- **Long-term Tracking**: Monitor exposure patterns and skin health over time
- **Multi-language Support**: Reach global audiences
- **Mobile App**: Native iOS and Android applications

## ⚠️ Important Notes

### Medical Disclaimer
This application provides **educational information only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified dermatologists or healthcare providers for:
- Diagnosis of skin conditions
- Treatment recommendations
- Persistent skin problems
- Suspected serious conditions (skin cancer, severe infections, etc.)

### API Usage
- Free tier of OpenWeatherMap allows 1,000 API calls/day
- For production use, consider upgrading to paid plans
- Current implementation simulates UV index (requires paid API for accurate data)

## 🤝 Contributing

This is an educational project. Suggestions for improvements are welcome!

## 📄 License

This project is created for educational and health awareness purposes. Not for commercial use.

## 🆘 Troubleshooting

### Common Issues

**Issue**: "Unable to fetch weather data"
- **Solution**: Check your API key in `.env` file
- Verify internet connection
- Ensure location name is spelled correctly

**Issue**: Application won't start
- **Solution**: Verify Python version (3.8+)
- Check all dependencies are installed: `pip install -r requirements.txt`
- Ensure port 5000 is not in use

**Issue**: CSS/JavaScript not loading
- **Solution**: Clear browser cache
- Check browser console for errors
- Verify file paths in templates

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in `app.py`
3. Consult Flask and OpenWeatherMap documentation

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Font Awesome for icons
- Flask framework and community
- Dermatological research for health information

---

**Built with ❤️ for skin health awareness**

Remember: Healthy skin starts with awareness! 🌞🛡️
