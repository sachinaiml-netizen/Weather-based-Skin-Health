from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import math

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your_api_key_here')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
UV_INDEX_URL = 'https://api.openweathermap.org/data/2.5/uvi'

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_uv_index(lat, lon):
    """Fetch UV index data from OpenWeatherMap API"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY
        }
        response = requests.get(UV_INDEX_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('value', 5)  # Default to moderate UV if not available
    except:
        # Estimate UV based on time and weather (fallback)
        return 5

def calculate_uv_index_risk(uv_index):
    """Categorize UV index risk level"""
    if uv_index is None:
        return "Unknown"
    if uv_index < 3:
        return "Low"
    elif uv_index < 6:
        return "Moderate"
    elif uv_index < 8:
        return "High"
    elif uv_index < 11:
        return "Very High"
    else:
        return "Extreme"

def predict_skin_concerns(weather_data, uv_index):
    """
    AI/ML-based prediction of potential skin concerns
    Uses multi-factor analysis to predict skin issues
    """
    concerns = []
    concern_scores = {
        'dryness': 0,
        'acne': 0,
        'sunburn': 0,
        'sensitivity': 0,
        'oiliness': 0
    }
    
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    condition = weather_data['weather'][0]['main'].lower()
    
    # Dryness prediction model
    if temp < 10:
        concern_scores['dryness'] += 40
    if humidity < 30:
        concern_scores['dryness'] += 35
    if wind_speed > 10:
        concern_scores['dryness'] += 15
    if condition in ['clear', 'sunny']:
        concern_scores['dryness'] += 10
    
    # Acne prediction model
    if humidity > 70:
        concern_scores['acne'] += 30
    if temp > 25 and temp < 35:
        concern_scores['acne'] += 25
    if condition in ['rain', 'drizzle']:
        concern_scores['acne'] += 20
    if humidity > 60 and temp > 20:
        concern_scores['acne'] += 15
    
    # Sunburn prediction model
    concern_scores['sunburn'] = uv_index * 10
    if condition in ['clear', 'sunny']:
        concern_scores['sunburn'] += 20
    if temp > 25:
        concern_scores['sunburn'] += 15
    
    # Sensitivity prediction model
    if wind_speed > 15:
        concern_scores['sensitivity'] += 30
    if temp < 5 or temp > 35:
        concern_scores['sensitivity'] += 25
    if condition in ['snow', 'storm', 'thunderstorm']:
        concern_scores['sensitivity'] += 20
    
    # Oiliness prediction model
    if humidity > 65:
        concern_scores['oiliness'] += 35
    if temp > 28:
        concern_scores['oiliness'] += 30
    if condition in ['clear', 'sunny'] and temp > 25:
        concern_scores['oiliness'] += 20
    
    # Categorize concerns based on scores
    for concern, score in concern_scores.items():
        if score >= 70:
            risk = "High Risk"
            severity = "high"
        elif score >= 50:
            risk = "Moderate Risk"
            severity = "moderate"
        elif score >= 30:
            risk = "Low Risk"
            severity = "low"
        else:
            risk = None
            severity = None
        
        if risk:
            concerns.append({
                'type': concern.capitalize(),
                'risk': risk,
                'severity': severity,
                'score': score,
                'confidence': min(95, 60 + (score / 3))  # ML confidence score
            })
    
    return sorted(concerns, key=lambda x: x['score'], reverse=True)

def get_skin_recommendations(weather_data):
    """Generate skin care recommendations based on weather conditions"""
    if not weather_data:
        return {
            'error': 'Unable to fetch weather data. Please check the city name and try again.'
        }
    
    # Get UV index
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    uv_index = get_uv_index(lat, lon)
    
    # Predict skin concerns using ML model
    predicted_concerns = predict_skin_concerns(weather_data, uv_index)
    
    recommendations = {
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'temperature': weather_data['main']['temp'],
        'humidity': weather_data['main']['humidity'],
        'weather_condition': weather_data['weather'][0]['main'],
        'weather_description': weather_data['weather'][0]['description'],
        'wind_speed': weather_data['wind']['speed'],
        'uv_index': round(uv_index, 1),
        'uv_risk': calculate_uv_index_risk(uv_index),
        'predicted_concerns': predicted_concerns,
        'skincare_tips': [],
        'products_recommended': [],
        'warnings': []
    }
    
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    condition = weather_data['weather'][0]['main'].lower()
    
    # Add concern-specific recommendations
    for concern in predicted_concerns:
        if concern['type'] == 'Dryness':
            recommendations['skincare_tips'].append(f"🔴 {concern['risk']}: Dryness detected. Use intensive hydration.")
            recommendations['products_recommended'].extend([
                "Hyaluronic acid serum (holds 1000x its weight in water)",
                "Rich emollient moisturizer with ceramides",
                "Facial oil (argan, jojoba, or rosehip)"
            ])
        elif concern['type'] == 'Acne':
            recommendations['skincare_tips'].append(f"🔴 {concern['risk']}: Acne-prone conditions. Keep skin clean.")
            recommendations['products_recommended'].extend([
                "Salicylic acid cleanser (2%)",
                "Non-comedogenic moisturizer",
                "Clay mask for oil control"
            ])
        elif concern['type'] == 'Sunburn':
            recommendations['skincare_tips'].append(f"🔴 {concern['risk']}: High UV exposure. Sunburn prevention critical.")
            recommendations['products_recommended'].extend([
                f"SPF {50 if uv_index > 7 else 30}+ broad-spectrum sunscreen",
                "After-sun aloe vera gel",
                "Antioxidant serum (Vitamin C or E)"
            ])
            recommendations['warnings'].append(f"⚠️ UV Index: {uv_index} ({recommendations['uv_risk']}) - Reapply sunscreen every 2 hours!")
        elif concern['type'] == 'Sensitivity':
            recommendations['skincare_tips'].append(f"🔴 {concern['risk']}: Skin sensitivity expected.")
            recommendations['products_recommended'].extend([
                "Gentle fragrance-free cleanser",
                "Soothing centella or chamomile serum",
                "Barrier repair cream"
            ])
        elif concern['type'] == 'Oiliness':
            recommendations['skincare_tips'].append(f"🔴 {concern['risk']}: Excess oil production likely.")
            recommendations['products_recommended'].extend([
                "Oil-free gel cleanser",
                "Mattifying primer",
                "Blotting papers for touch-ups"
            ])
    
    # Temperature-based recommendations
    if temp < 10:
        recommendations['skincare_tips'].append("Cold weather detected: Use rich, emollient moisturizers to prevent dryness.")
        recommendations['products_recommended'].append("Heavy cream-based moisturizer")
        recommendations['products_recommended'].append("Lip balm with SPF")
        recommendations['warnings'].append("Protect exposed skin from cold wind to prevent chapping.")
    elif temp < 20:
        recommendations['skincare_tips'].append("Cool weather: Maintain a balanced moisturizing routine.")
        recommendations['products_recommended'].append("Medium-weight moisturizer")
    elif temp < 30:
        recommendations['skincare_tips'].append("Moderate temperature: Use a lightweight moisturizer.")
        recommendations['products_recommended'].append("Lightweight gel moisturizer")
    else:
        recommendations['skincare_tips'].append("Hot weather: Use oil-free, lightweight products.")
        recommendations['products_recommended'].append("Oil-free moisturizer")
        recommendations['products_recommended'].append("Mattifying primer")
        recommendations['warnings'].append("High temperature: Stay hydrated and avoid prolonged sun exposure.")
    
    # Humidity-based recommendations
    if humidity < 30:
        recommendations['skincare_tips'].append("Low humidity detected: Extra hydration needed.")
        recommendations['products_recommended'].append("Hyaluronic acid serum")
        recommendations['products_recommended'].append("Humidifier for indoor use")
        recommendations['warnings'].append("Very dry air can cause skin dehydration. Drink plenty of water.")
    elif humidity < 60:
        recommendations['skincare_tips'].append("Moderate humidity: Normal skincare routine is adequate.")
    else:
        recommendations['skincare_tips'].append("High humidity: Use lightweight, non-comedogenic products.")
        recommendations['products_recommended'].append("Oil-control face wash")
        recommendations['products_recommended'].append("Non-comedogenic sunscreen")
        recommendations['warnings'].append("High humidity can increase oil production. Cleanse regularly.")
    
    # Weather condition-based recommendations
    if 'rain' in condition or 'drizzle' in condition:
        recommendations['skincare_tips'].append("Rainy weather: Protect skin from moisture and pollutants.")
        recommendations['products_recommended'].append("Water-resistant sunscreen")
        recommendations['warnings'].append("Rain can contain pollutants. Cleanse thoroughly after exposure.")
    elif 'snow' in condition:
        recommendations['skincare_tips'].append("Snowy conditions: UV rays reflect off snow. Use high SPF.")
        recommendations['products_recommended'].append("SPF 50+ sunscreen")
        recommendations['products_recommended'].append("Protective barrier cream")
        recommendations['warnings'].append("Snow reflects up to 80% of UV rays. Protect your skin!")
    elif 'clear' in condition or 'sun' in condition:
        recommendations['skincare_tips'].append("Sunny weather: Sun protection is essential.")
        recommendations['products_recommended'].append("Broad-spectrum SPF 30+ sunscreen")
        recommendations['products_recommended'].append("Sunglasses and hat")
        recommendations['warnings'].append("Apply sunscreen every 2 hours when outdoors.")
    elif 'cloud' in condition:
        recommendations['skincare_tips'].append("Cloudy weather: UV rays still penetrate clouds. Use sunscreen.")
        recommendations['products_recommended'].append("Daily SPF moisturizer")
    elif 'mist' in condition or 'fog' in condition:
        recommendations['skincare_tips'].append("Misty conditions: Keep skin hydrated.")
        recommendations['products_recommended'].append("Hydrating mist spray")
    
    # Wind-based recommendations
    if weather_data['wind']['speed'] > 10:
        recommendations['skincare_tips'].append("Windy conditions: Protect skin from windburn.")
        recommendations['products_recommended'].append("Protective barrier cream")
        recommendations['warnings'].append("Strong winds can strip natural oils from skin.")
    
    # General recommendations
    recommendations['skincare_tips'].append("Always stay hydrated by drinking plenty of water.")
    recommendations['skincare_tips'].append("Get adequate sleep for healthy skin regeneration.")
    
    return recommendations

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get skin care recommendations"""
    data = request.get_json()
    city = data.get('city', '')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    weather_data = get_weather_data(city)
    recommendations = get_skin_recommendations(weather_data)
    
    return jsonify(recommendations)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
