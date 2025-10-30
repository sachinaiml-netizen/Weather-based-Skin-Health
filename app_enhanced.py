"""
Weather-Based Skin Analyzer
Advanced AI/ML-powered skin condition detection with weather integration
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
from dotenv import load_dotenv

# Import custom modules
from weather_api import get_comprehensive_weather, get_aqi_category
from skin_model import analyze_skin_condition
from recommendations_engine import generate_comprehensive_recommendations

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('analyzer.html')

@app.route('/api/weather', methods=['POST'])
def api_weather():
    """
    Get weather data for a city
    Includes: temperature, humidity, UV index, air quality (AQI)
    """
    data = request.get_json()
    city = data.get('city', '').strip()
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    weather_data = get_comprehensive_weather(city)
    
    if not weather_data:
        return jsonify({'error': f'Unable to fetch weather data for "{city}". Please check the city name.'}), 404
    
    return jsonify(weather_data)

@app.route('/api/analyze-skin', methods=['POST'])
def api_analyze_skin():
    """
    Analyze skin condition from uploaded image
    Uses TensorFlow/OpenCV for detection
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload JPG, PNG, or JPEG'}), 400
    
    try:
        # Analyze the image using ML model
        detected_conditions = analyze_skin_condition(file.stream)
        
        if not detected_conditions:
            return jsonify({'error': 'Unable to analyze image. Please try another image.'}), 400
        
        # Format response
        response = {
            'conditions': []
        }
        
        for condition in detected_conditions:
            response['conditions'].append({
                'type': condition['type'],
                'score': round(condition['score'], 1),
                'confidence': round(condition['confidence'], 1),
                'severity': condition['severity'],
                'indicators': condition.get('indicators', [])
            })
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing image: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while processing the image.'}), 500

@app.route('/api/analyze-complete', methods=['POST'])
def api_analyze_complete():
    """
    Complete analysis combining weather + skin image
    Provides personalized recommendations based on both factors
    """
    # Get weather data
    city = request.form.get('city', '').strip()
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    weather_data = get_comprehensive_weather(city)
    
    if not weather_data:
        return jsonify({'error': f'Unable to fetch weather data for "{city}".'}), 404
    
    # Get skin analysis
    skin_conditions = []
    
    if 'file' in request.files:
        file = request.files['file']
        
        if file and file.filename != '' and allowed_file(file.filename):
            try:
                skin_conditions = analyze_skin_condition(file.stream)
            except Exception as e:
                print(f"Error analyzing skin: {e}")
                skin_conditions = []
    
    # Generate comprehensive recommendations
    recommendations = generate_comprehensive_recommendations(
        weather_data,
        skin_conditions
    )
    
    response = {
        'weather': weather_data,
        'skin_analysis': {
            'conditions': [
                {
                    'type': c['type'],
                    'score': round(c['score'], 1),
                    'confidence': round(c['confidence'], 1),
                    'severity': c['severity'],
                    'indicators': c.get('indicators', [])
                }
                for c in skin_conditions
            ]
        },
        'recommendations': recommendations
    }
    
    return jsonify(response)

@app.route('/api/geolocation', methods=['POST'])
def api_geolocation():
    """
    Get weather data based on geolocation coordinates
    """
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    try:
        from weather_api import get_weather_data, get_uv_index, get_air_quality
        
        # Get weather by coordinates (reverse geocoding)
        WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
        import requests
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        weather_data = response.json()
        
        uv_index = get_uv_index(lat, lon)
        air_quality = get_air_quality(lat, lon)
        
        result = {
            'city': weather_data.get('name', 'Your Location'),
            'country': weather_data['sys'].get('country', ''),
            'coordinates': {'lat': lat, 'lon': lon},
            'weather': {
                'temperature': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'description': weather_data['weather'][0]['description'],
                'main': weather_data['weather'][0]['main']
            },
            'wind': {
                'speed': weather_data['wind']['speed']
            },
            'uv': {
                'index': round(uv_index, 1),
                'risk': 'Low' if uv_index < 3 else 'Moderate' if uv_index < 6 else 'High' if uv_index < 8 else 'Very High'
            }
        }
        
        if air_quality:
            result['air_quality'] = {
                'aqi': air_quality['aqi'],
                'category': get_aqi_category(air_quality['aqi']),
                'pm2_5': round(air_quality['pm2_5'], 2),
                'pm10': round(air_quality['pm10'], 2)
            }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error getting geolocation weather: {e}")
        return jsonify({'error': 'Unable to fetch weather for your location'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': [
            'Weather Analysis',
            'UV Index Monitoring',
            'Air Quality (AQI) Detection',
            'AI/ML Skin Condition Detection',
            'Personalized Recommendations',
            'Geolocation Support'
        ]
    })

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 5MB.'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🧬 Weather-Based Skin Analyzer v2.0")
    print("=" * 60)
    print("Features:")
    print("  ✅ AI/ML Skin Condition Detection")
    print("  ✅ Weather + UV + Air Quality Integration")
    print("  ✅ Personalized Skincare Recommendations")
    print("  ✅ Geolocation Support")
    print("=" * 60)
    print("Starting server at http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
