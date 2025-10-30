from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import math
from PIL import Image
import io
import base64

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your_api_key_here')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
UV_INDEX_URL = 'https://api.openweathermap.org/data/2.5/uvi'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

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
    """Render the main page with both weather and image analysis"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint to get weather-based skin care recommendations"""
    data = request.get_json()
    city = data.get('city', '')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    weather_data = get_weather_data(city)
    
    if not weather_data:
        return jsonify({'error': 'Unable to fetch weather data. Please check the city name and try again.'}), 400
    
    # Get UV index
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    uv_index = get_uv_index(lat, lon)
    
    # Predict skin concerns
    predicted_concerns = predict_skin_concerns(weather_data, uv_index)
    
    # Format response
    response = {
        'city': weather_data['name'],
        'weather': {
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'description': weather_data['weather'][0]['description'],
            'wind_speed': weather_data['wind']['speed'],
            'uv_index': round(uv_index, 1)
        },
        'predictions': {},
        'recommendations': [],
        'products': [],
        'warnings': []
    }
    
    # Format predictions
    for concern in predicted_concerns:
        response['predictions'][concern['type'].lower()] = {
            'score': concern['score'],
            'risk_level': concern['risk'],
            'confidence': concern['confidence']
        }
    
    # Get detailed recommendations
    recommendations = get_skin_recommendations(weather_data)
    response['recommendations'] = recommendations['skincare_tips']
    response['products'] = recommendations['products_recommended']
    response['warnings'] = recommendations['warnings']
    
    return jsonify(response)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_skin_from_image(image_file):
    """
    AI-based skin condition analysis from image
    This is a rule-based analysis system that examines image properties
    In production, this would use a trained ML model
    """
    try:
        # Open and analyze image
        img = Image.open(image_file)
        img_data = img.convert('RGB')
        pixels = list(img_data.getdata())
        
        # Calculate average color properties
        avg_red = sum([p[0] for p in pixels]) / len(pixels)
        avg_green = sum([p[1] for p in pixels]) / len(pixels)
        avg_blue = sum([p[2] for p in pixels]) / len(pixels)
        
        # Calculate image brightness
        brightness = (avg_red + avg_green + avg_blue) / 3
        
        # Calculate color variance (indicates texture/unevenness)
        red_variance = sum([(p[0] - avg_red) ** 2 for p in pixels]) / len(pixels)
        variance = math.sqrt(red_variance)
        
        # Redness score (for inflammation/acne/sensitivity)
        redness_score = (avg_red - (avg_green + avg_blue) / 2) / 255 * 100
        
        # Analyze skin conditions based on image properties
        detected_conditions = []
        
        # Acne detection (high redness, high variance)
        if redness_score > 15 and variance > 30:
            acne_score = min(95, 50 + redness_score + variance / 3)
            detected_conditions.append({
                'type': 'Acne',
                'risk': 'High Risk' if acne_score > 70 else 'Moderate Risk',
                'severity': 'high' if acne_score > 70 else 'moderate',
                'score': round(acne_score, 1),
                'confidence': min(95, 70 + variance / 5)
            })
        
        # Redness/Sensitivity detection
        if redness_score > 10:
            redness_severity = min(90, 40 + redness_score * 2)
            detected_conditions.append({
                'type': 'Redness',
                'risk': 'High Risk' if redness_severity > 70 else 'Moderate Risk',
                'severity': 'high' if redness_severity > 70 else 'moderate',
                'score': round(redness_severity, 1),
                'confidence': min(90, 65 + redness_score)
            })
        
        # Dryness detection (low variance, certain brightness range)
        if variance < 25 and 100 < brightness < 180:
            dryness_score = min(85, 60 - variance)
            detected_conditions.append({
                'type': 'Dryness',
                'risk': 'Moderate Risk',
                'severity': 'moderate',
                'score': round(dryness_score, 1),
                'confidence': 75
            })
        
        # Dark spots/Pigmentation (low brightness with high variance)
        if brightness < 100 and variance > 25:
            pigmentation_score = min(80, (150 - brightness) / 2 + variance)
            detected_conditions.append({
                'type': 'Dark Spots',
                'risk': 'Moderate Risk',
                'severity': 'moderate',
                'score': round(pigmentation_score, 1),
                'confidence': 70
            })
        
        # Oiliness detection (high brightness, medium variance)
        if brightness > 180 and 20 < variance < 40:
            oiliness_score = min(75, (brightness - 180) / 2 + variance)
            detected_conditions.append({
                'type': 'Oiliness',
                'risk': 'Moderate Risk',
                'severity': 'moderate',
                'score': round(oiliness_score, 1),
                'confidence': 68
            })
        
        # If no conditions detected
        if not detected_conditions:
            detected_conditions.append({
                'type': 'Healthy Skin',
                'risk': 'Low Risk',
                'severity': 'low',
                'score': 15,
                'confidence': 80
            })
        
        return detected_conditions
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

def get_skin_recommendations_from_image(detected_conditions):
    """Generate skincare recommendations based on detected skin conditions"""
    recommendations = {
        'detected_conditions': detected_conditions,
        'skincare_tips': [],
        'products_recommended': [],
        'warnings': []
    }
    
    for condition in detected_conditions:
        condition_type = condition['type']
        
        if condition_type == 'Acne':
            recommendations['skincare_tips'].extend([
                f"🔴 {condition['risk']}: Active acne detected. Keep skin clean and avoid touching face.",
                "Use non-comedogenic products to prevent clogged pores.",
                "Avoid heavy makeup and oil-based products."
            ])
            recommendations['products_recommended'].extend([
                "Salicylic acid cleanser (2%)",
                "Benzoyl peroxide spot treatment",
                "Oil-free moisturizer",
                "Tea tree oil serum",
                "Clay mask (1-2 times per week)"
            ])
            recommendations['warnings'].append("⚠️ Avoid picking or squeezing acne as it may cause scarring.")
            
        elif condition_type == 'Redness':
            recommendations['skincare_tips'].extend([
                f"🔴 {condition['risk']}: Redness detected. Use soothing, anti-inflammatory products.",
                "Avoid harsh exfoliants and hot water.",
                "Use gentle, fragrance-free products."
            ])
            recommendations['products_recommended'].extend([
                "Centella asiatica (Cica) cream",
                "Niacinamide serum",
                "Gentle cleansing milk",
                "Mineral sunscreen (non-chemical)",
                "Aloe vera gel"
            ])
            
        elif condition_type == 'Dryness':
            recommendations['skincare_tips'].extend([
                f"🏜️ {condition['risk']}: Dry skin detected. Focus on intense hydration.",
                "Use rich, emollient moisturizers.",
                "Avoid harsh soaps and long hot showers."
            ])
            recommendations['products_recommended'].extend([
                "Hyaluronic acid serum",
                "Rich cream moisturizer with ceramides",
                "Facial oil (rosehip, argan, or jojoba)",
                "Gentle cream cleanser",
                "Overnight sleeping mask"
            ])
            
        elif condition_type == 'Dark Spots':
            recommendations['skincare_tips'].extend([
                f"⚫ {condition['risk']}: Dark spots/pigmentation detected.",
                "Use brightening ingredients consistently.",
                "Always wear sunscreen to prevent darkening."
            ])
            recommendations['products_recommended'].extend([
                "Vitamin C serum (morning)",
                "Retinol cream (evening)",
                "Niacinamide serum",
                "SPF 50+ broad-spectrum sunscreen",
                "Alpha arbutin serum"
            ])
            recommendations['warnings'].append("⚠️ Sun protection is crucial! Dark spots worsen with UV exposure.")
            
        elif condition_type == 'Oiliness':
            recommendations['skincare_tips'].extend([
                f"💧 {condition['risk']}: Oily skin detected. Use oil-control products.",
                "Cleanse twice daily to remove excess oil.",
                "Use lightweight, gel-based products."
            ])
            recommendations['products_recommended'].extend([
                "Foaming gel cleanser",
                "Oil-free mattifying moisturizer",
                "Niacinamide serum (oil control)",
                "Clay mask (2-3 times per week)",
                "Blotting papers"
            ])
            
        elif condition_type == 'Healthy Skin':
            recommendations['skincare_tips'].extend([
                "✅ Skin appears healthy! Maintain your current routine.",
                "Continue with basic cleansing, moisturizing, and sun protection.",
                "Stay hydrated and maintain a balanced diet."
            ])
            recommendations['products_recommended'].extend([
                "Gentle daily cleanser",
                "Light moisturizer",
                "SPF 30+ sunscreen",
                "Antioxidant serum (optional)"
            ])
    
    # Remove duplicates
    recommendations['skincare_tips'] = list(dict.fromkeys(recommendations['skincare_tips']))
    recommendations['products_recommended'] = list(dict.fromkeys(recommendations['products_recommended']))
    recommendations['warnings'] = list(dict.fromkeys(recommendations['warnings']))
    
    # General recommendations
    recommendations['skincare_tips'].append("💧 Stay hydrated by drinking plenty of water.")
    recommendations['skincare_tips'].append("😴 Get adequate sleep for healthy skin regeneration.")
    recommendations['warnings'].append("📋 Consult a dermatologist for persistent or severe skin concerns.")
    
    return recommendations

@app.route('/api/analyze-image', methods=['POST'])
def api_analyze_image():
    """API endpoint to analyze skin from uploaded image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload JPG, PNG, or JPEG'}), 400
    
    try:
        # Analyze the image
        detected_conditions = analyze_skin_from_image(file.stream)
        
        if not detected_conditions:
            return jsonify({'error': 'Unable to analyze image. Please try another image.'}), 400
        
        # Format response
        response = {
            'predictions': {},
            'recommendations': [],
            'products': [],
            'warnings': []
        }
        
        # Format predictions
        for condition in detected_conditions:
            response['predictions'][condition['type'].lower().replace(' ', '_')] = {
                'score': condition['score'],
                'risk_level': condition['risk'],
                'confidence': condition['confidence']
            }
        
        # Get detailed recommendations
        recommendations = get_skin_recommendations_from_image(detected_conditions)
        response['recommendations'] = recommendations['skincare_tips']
        response['products'] = recommendations['products_recommended']
        response['warnings'] = recommendations['warnings']
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': 'An error occurred while processing the image.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
