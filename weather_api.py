"""
Enhanced Weather API with Pollution Data
Integrates OpenWeatherMap Weather + UV Index + Air Quality (AQI)
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your_api_key_here')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
UV_INDEX_URL = 'https://api.openweathermap.org/data/2.5/uvi'
AIR_POLLUTION_URL = 'https://api.openweathermap.org/data/2.5/air_pollution'
GEOCODING_URL = 'https://api.openweathermap.org/geo/1.0/direct'

def get_weather_data(city):
    """
    Fetch comprehensive weather data including:
    - Temperature, humidity, pressure
    - Wind speed and direction
    - Weather conditions
    - Coordinates for additional API calls
    """
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_uv_index(lat, lon):
    """
    Fetch UV index data for given coordinates
    Returns float value (0-11+)
    """
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY
        }
        response = requests.get(UV_INDEX_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('value', 5)  # Default to moderate if unavailable
    except:
        # Fallback UV estimation based on time of day
        from datetime import datetime
        hour = datetime.now().hour
        if 10 <= hour <= 16:  # Peak hours
            return 7
        elif 8 <= hour <= 18:  # Moderate hours
            return 4
        else:  # Early morning/evening/night
            return 1

def get_air_quality(lat, lon):
    """
    Fetch air quality index (AQI) and pollutant data
    
    AQI Categories (from API):
    1 = Good
    2 = Fair
    3 = Moderate
    4 = Poor
    5 = Very Poor
    
    Returns:
    {
        'aqi': int (1-5),
        'pm2_5': float,  # Fine particulate matter
        'pm10': float,   # Coarse particulate matter
        'no2': float,    # Nitrogen dioxide
        'o3': float,     # Ozone
        'co': float      # Carbon monoxide
    }
    """
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY
        }
        response = requests.get(AIR_POLLUTION_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and 'list' in data and len(data['list']) > 0:
            pollution_data = data['list'][0]
            
            return {
                'aqi': pollution_data['main']['aqi'],
                'pm2_5': pollution_data['components'].get('pm2_5', 0),
                'pm10': pollution_data['components'].get('pm10', 0),
                'no2': pollution_data['components'].get('no2', 0),
                'o3': pollution_data['components'].get('o3', 0),
                'co': pollution_data['components'].get('co', 0)
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching air quality data: {e}")
        return None

def get_aqi_category(aqi):
    """Convert AQI number to category name"""
    categories = {
        1: 'Good',
        2: 'Fair',
        3: 'Moderate',
        4: 'Poor',
        5: 'Very Poor'
    }
    return categories.get(aqi, 'Unknown')

def get_aqi_skin_impact(aqi):
    """Get skin impact description for AQI level"""
    impacts = {
        1: 'Minimal impact on skin. Normal skincare routine is sufficient.',
        2: 'Low impact. Basic cleansing recommended after outdoor activities.',
        3: 'Moderate impact. Antioxidant skincare recommended. Cleanse thoroughly.',
        4: 'Poor air quality can accelerate aging. Use protective barrier creams and antioxidants.',
        5: 'Very poor air quality. Minimize outdoor exposure. Use strong antioxidants and barrier repair products.'
    }
    return impacts.get(aqi, 'Unknown impact')

def get_comprehensive_weather(city):
    """
    Get all weather-related data in one call:
    - Basic weather
    - UV index
    - Air quality/pollution
    """
    weather_data = get_weather_data(city)
    
    if not weather_data:
        return None
    
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    
    uv_index = get_uv_index(lat, lon)
    air_quality = get_air_quality(lat, lon)
    
    comprehensive_data = {
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'coordinates': {
            'lat': lat,
            'lon': lon
        },
        'weather': {
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'temp_min': weather_data['main']['temp_min'],
            'temp_max': weather_data['main']['temp_max'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'description': weather_data['weather'][0]['description'],
            'main': weather_data['weather'][0]['main'],
            'icon': weather_data['weather'][0]['icon']
        },
        'wind': {
            'speed': weather_data['wind']['speed'],
            'deg': weather_data['wind'].get('deg', 0)
        },
        'uv': {
            'index': round(uv_index, 1),
            'risk': calculate_uv_risk(uv_index)
        }
    }
    
    # Add air quality if available
    if air_quality:
        comprehensive_data['air_quality'] = {
            'aqi': air_quality['aqi'],
            'category': get_aqi_category(air_quality['aqi']),
            'pm2_5': round(air_quality['pm2_5'], 2),
            'pm10': round(air_quality['pm10'], 2),
            'skin_impact': get_aqi_skin_impact(air_quality['aqi'])
        }
    else:
        comprehensive_data['air_quality'] = {
            'aqi': 2,  # Default to Fair
            'category': 'Fair',
            'pm2_5': 0,
            'pm10': 0,
            'skin_impact': 'Air quality data unavailable. Proceed with normal skincare.'
        }
    
    return comprehensive_data

def calculate_uv_risk(uv_index):
    """Categorize UV index risk level"""
    if uv_index < 3:
        return 'Low'
    elif uv_index < 6:
        return 'Moderate'
    elif uv_index < 8:
        return 'High'
    elif uv_index < 11:
        return 'Very High'
    else:
        return 'Extreme'

def get_coordinates_from_city(city):
    """
    Get lat/lon coordinates from city name
    Useful for direct coordinate-based queries
    """
    try:
        params = {
            'q': city,
            'limit': 1,
            'appid': WEATHER_API_KEY
        }
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            return {
                'lat': data[0]['lat'],
                'lon': data[0]['lon'],
                'name': data[0]['name'],
                'country': data[0].get('country', '')
            }
        return None
    except:
        return None
