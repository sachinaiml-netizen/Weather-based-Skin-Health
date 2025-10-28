# Weather-based Skin Health Application

A comprehensive web application that provides personalized skincare recommendations based on real-time weather conditions in your location.

## Features

- **Real-time Weather Data**: Fetches current weather information using OpenWeatherMap API
- **Personalized Recommendations**: Provides customized skincare tips based on:
  - Temperature
  - Humidity levels
  - Weather conditions (sunny, rainy, snowy, etc.)
  - Wind speed
  - UV index considerations
- **Product Suggestions**: Recommends specific skincare products for current weather
- **Health Warnings**: Alerts users about potential skin health risks
- **Beautiful UI**: Modern, responsive web interface

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

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: OpenWeatherMap API
- **Styling**: Custom CSS with modern design

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

## Future Enhancements

- [ ] UV Index API integration
- [ ] User accounts and preferences
- [ ] Weekly forecast and skincare planning
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Air quality index integration
- [ ] Personalized skin type analysis
