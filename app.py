from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Weather API configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
AIR_QUALITY_API_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'

class SkinHealthAdvisor:
    """Core logic for analyzing weather conditions and providing skin health advice"""
    
    @staticmethod
    def analyze_uv_risk(uvi, weather_desc):
        """Analyze UV radiation risks"""
        risks = []
        tips = []
        severity = "low"
        
        if uvi >= 8:
            severity = "extreme"
            risks.append("Extremely high UV radiation - severe sunburn risk in minutes")
            risks.append("Increased risk of skin cancer with prolonged exposure")
            risks.append("Risk of photoaging and DNA damage to skin cells")
            tips.extend([
                "Avoid sun exposure between 10 AM - 4 PM",
                "Wear wide-brimmed hat and UV-protective clothing",
                "Apply broad-spectrum SPF 50+ sunscreen every 2 hours",
                "Seek shade whenever possible",
                "Wear UV-blocking sunglasses"
            ])
        elif uvi >= 6:
            severity = "high"
            risks.append("High UV radiation - sunburn possible in 15-20 minutes")
            risks.append("Risk of premature aging and skin damage")
            tips.extend([
                "Limit sun exposure during peak hours (10 AM - 4 PM)",
                "Apply SPF 30+ sunscreen every 2-3 hours",
                "Wear protective clothing and sunglasses",
                "Seek shade when outdoors"
            ])
        elif uvi >= 3:
            severity = "moderate"
            risks.append("Moderate UV radiation - sunburn possible in 30 minutes")
            tips.extend([
                "Apply SPF 30 sunscreen if outdoors for extended periods",
                "Wear sunglasses and consider a hat",
                "Be cautious during midday hours"
            ])
        else:
            tips.append("UV levels are low, but protection is still recommended for sensitive skin")
        
        return {
            "severity": severity,
            "risks": risks,
            "tips": tips,
            "uv_index": uvi
        }
    
    @staticmethod
    def analyze_humidity_risk(humidity, temp):
        """Analyze humidity-related skin risks"""
        risks = []
        tips = []
        severity = "low"
        
        if humidity >= 70:
            severity = "high"
            risks.append("High humidity promotes fungal and bacterial growth")
            risks.append("Increased risk of fungal infections (athlete's foot, ringworm, candidiasis)")
            risks.append("Acne breakouts due to excess moisture and oil production")
            risks.append("Heat rash and skin irritation")
            tips.extend([
                "Keep skin clean and dry, especially in skin folds",
                "Wear breathable, moisture-wicking fabrics",
                "Use antifungal powder in prone areas",
                "Shower immediately after sweating",
                "Change wet or damp clothing promptly",
                "Use oil-free, non-comedogenic skincare products"
            ])
        elif humidity >= 50:
            severity = "moderate"
            risks.append("Moderate humidity may cause increased sweating")
            risks.append("Possible acne or skin irritation")
            tips.extend([
                "Maintain good hygiene",
                "Use lightweight, breathable clothing",
                "Keep skin clean throughout the day"
            ])
        elif humidity < 30:
            severity = "moderate"
            risks.append("Low humidity causes skin dehydration and dryness")
            risks.append("Risk of eczema flare-ups and skin cracking")
            risks.append("Increased skin sensitivity and irritation")
            tips.extend([
                "Use a humidifier indoors (aim for 40-50% humidity)",
                "Apply fragrance-free moisturizer frequently",
                "Avoid hot showers - use lukewarm water",
                "Drink plenty of water to stay hydrated",
                "Use gentle, soap-free cleansers"
            ])
        
        return {
            "severity": severity,
            "risks": risks,
            "tips": tips,
            "humidity": humidity
        }
    
    @staticmethod
    def analyze_temperature_risk(temp):
        """Analyze temperature-related skin risks"""
        risks = []
        tips = []
        severity = "low"
        
        if temp >= 30:
            severity = "high"
            risks.append("Heat-related skin conditions: heat rash, prickly heat")
            risks.append("Increased sweating leading to dehydration")
            risks.append("Sun exposure combined with heat increases skin damage")
            risks.append("Risk of heat exhaustion affecting skin health")
            tips.extend([
                "Stay hydrated - drink 8-10 glasses of water daily",
                "Wear light, loose-fitting clothing",
                "Use cooling skincare products (aloe vera gel)",
                "Take cool showers to prevent heat rash",
                "Avoid heavy makeup and occlusive products"
            ])
        elif temp <= 5:
            severity = "high"
            risks.append("Cold weather causes severe skin dryness and chapping")
            risks.append("Risk of eczema and dermatitis flare-ups")
            risks.append("Frostbite risk on exposed skin")
            risks.append("Windburn and cracked skin")
            tips.extend([
                "Apply thick, emollient moisturizers",
                "Protect exposed skin with scarves and gloves",
                "Use petroleum jelly on extremely dry areas",
                "Avoid harsh soaps and hot water",
                "Consider using a humidifier indoors"
            ])
        elif temp <= 15:
            severity = "moderate"
            risks.append("Cool temperatures can cause dryness")
            risks.append("Possible eczema triggers")
            tips.extend([
                "Moisturize regularly",
                "Protect skin from cold wind",
                "Use gentle skincare products"
            ])
        
        return {
            "severity": severity,
            "risks": risks,
            "tips": tips,
            "temperature": temp
        }
    
    @staticmethod
    def analyze_pollution_risk(aqi):
        """Analyze air pollution impact on skin"""
        risks = []
        tips = []
        severity = "low"
        
        if aqi >= 151:  # Unhealthy
            severity = "extreme"
            risks.append("Severe pollution causes premature aging and wrinkles")
            risks.append("Increased risk of pigmentation and dark spots")
            risks.append("Free radical damage leading to collagen breakdown")
            risks.append("Clogged pores and acne breakouts")
            risks.append("Inflammation and skin sensitivity")
            tips.extend([
                "Cleanse face thoroughly twice daily",
                "Use antioxidant serums (Vitamin C, E)",
                "Apply broad-spectrum sunscreen daily",
                "Use air purifiers indoors",
                "Minimize outdoor exposure during peak pollution",
                "Consider wearing a mask outdoors",
                "Use barrier repair creams"
            ])
        elif aqi >= 101:  # Unhealthy for sensitive groups
            severity = "high"
            risks.append("Pollution accelerates skin aging")
            risks.append("Risk of skin inflammation and irritation")
            risks.append("Clogged pores leading to breakouts")
            tips.extend([
                "Double cleanse in the evening",
                "Use antioxidant skincare products",
                "Apply sunscreen even on cloudy days",
                "Limit outdoor activities during rush hours"
            ])
        elif aqi >= 51:  # Moderate
            severity = "moderate"
            risks.append("Moderate pollution may cause minor skin issues")
            tips.extend([
                "Cleanse skin properly before bed",
                "Use antioxidant products periodically",
                "Maintain regular skincare routine"
            ])
        else:
            tips.append("Air quality is good - maintain regular skincare routine")
        
        return {
            "severity": severity,
            "risks": risks,
            "tips": tips,
            "aqi": aqi
        }
    
    @staticmethod
    def analyze_rain_risk(is_raining, humidity):
        """Analyze rain and moisture-related risks"""
        if not is_raining:
            return None
        
        risks = [
            "Prolonged moisture exposure increases fungal infection risk",
            "Wet clothing can cause skin maceration and irritation",
            "Increased risk of athlete's foot and other fungal conditions"
        ]
        
        tips = [
            "Dry off immediately after getting wet",
            "Change out of wet clothes promptly",
            "Keep feet dry and use antifungal powder",
            "Avoid staying in wet shoes or socks",
            "Dry skin folds thoroughly"
        ]
        
        return {
            "severity": "moderate",
            "risks": risks,
            "tips": tips
        }

def get_weather_data(location):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None

def get_air_quality_data(lat, lon):
    """Fetch air quality data from OpenWeatherMap API"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY
        }
        response = requests.get(AIR_QUALITY_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Air Quality API Error: {e}")
        return None

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_skin_health():
    """Analyze skin health based on weather conditions"""
    data = request.get_json()
    
    # Check if using manual input or location
    if data.get('manual'):
        # Manual weather input
        temp = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 50))
        uvi = float(data.get('uvi', 5))
        aqi = int(data.get('aqi', 50))
        weather_desc = data.get('weather', 'Clear')
        location = "Manual Input"
        
        weather_info = {
            'temp': temp,
            'humidity': humidity,
            'weather': weather_desc,
            'location': location
        }
    else:
        # Fetch real weather data
        location = data.get('location', 'London')
        weather_data = get_weather_data(location)
        
        if not weather_data:
            return jsonify({'error': 'Unable to fetch weather data. Please check location or try manual input.'}), 400
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_desc = weather_data['weather'][0]['description']
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        
        # Simulate UV index (OpenWeatherMap requires separate API call in paid plans)
        # In production, use UV Index API or OneCall API
        uvi = 5 if 'clear' in weather_desc.lower() else 3
        if temp > 25:
            uvi = min(uvi + 2, 11)
        
        # Get air quality data
        air_quality = get_air_quality_data(lat, lon)
        aqi = air_quality['list'][0]['main']['aqi'] * 50 if air_quality else 50
        
        weather_info = {
            'temp': temp,
            'humidity': humidity,
            'weather': weather_desc,
            'location': weather_data['name']
        }
    
    # Analyze all risk factors
    advisor = SkinHealthAdvisor()
    
    uv_analysis = advisor.analyze_uv_risk(uvi, weather_desc)
    humidity_analysis = advisor.analyze_humidity_risk(humidity, temp)
    temp_analysis = advisor.analyze_temperature_risk(temp)
    pollution_analysis = advisor.analyze_pollution_risk(aqi)
    
    is_raining = 'rain' in weather_desc.lower()
    rain_analysis = advisor.analyze_rain_risk(is_raining, humidity)
    
    # Compile comprehensive report
    report = {
        'weather': weather_info,
        'analyses': {
            'uv': uv_analysis,
            'humidity': humidity_analysis,
            'temperature': temp_analysis,
            'pollution': pollution_analysis
        },
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if rain_analysis:
        report['analyses']['rain'] = rain_analysis
    
    # Calculate overall risk level
    severities = [
        uv_analysis['severity'],
        humidity_analysis['severity'],
        temp_analysis['severity'],
        pollution_analysis['severity']
    ]
    
    if 'extreme' in severities:
        overall_severity = 'extreme'
    elif 'high' in severities:
        overall_severity = 'high'
    elif 'moderate' in severities:
        overall_severity = 'moderate'
    else:
        overall_severity = 'low'
    
    report['overall_severity'] = overall_severity
    
    return jsonify(report)

@app.route('/api/locations', methods=['GET'])
def get_popular_locations():
    """Return popular locations for quick access"""
    locations = [
        {'name': 'New York', 'country': 'USA'},
        {'name': 'London', 'country': 'UK'},
        {'name': 'Tokyo', 'country': 'Japan'},
        {'name': 'Mumbai', 'country': 'India'},
        {'name': 'Dubai', 'country': 'UAE'},
        {'name': 'Sydney', 'country': 'Australia'},
        {'name': 'Paris', 'country': 'France'},
        {'name': 'Singapore', 'country': 'Singapore'}
    ]
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
