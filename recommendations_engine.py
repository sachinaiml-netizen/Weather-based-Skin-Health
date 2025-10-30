"""
Comprehensive Recommendations Engine
Combines weather data + skin conditions + air quality to generate personalized advice
"""

def generate_comprehensive_recommendations(weather_data, skin_conditions):
    """
    Generate personalized skincare recommendations
    Based on:
    - Weather (temp, humidity, wind)
    - UV index
    - Air Quality (AQI, PM2.5, PM10)
    - Detected skin conditions
    """
    recommendations = {
        'skincare_routine': [],
        'products': {
            'cleanser': [],
            'moisturizer': [],
            'sunscreen': [],
            'treatment': [],
            'other': []
        },
        'lifestyle_tips': [],
        'warnings': [],
        'priority_actions': []
    }
    
    # Extract weather info
    temp = weather_data['weather']['temperature']
    humidity = weather_data['weather']['humidity']
    wind_speed = weather_data['wind']['speed']
    uv_index = weather_data['uv']['index']
    uv_risk = weather_data['uv']['risk']
    weather_condition = weather_data['weather']['main'].lower()
    
    # Extract air quality
    aqi = weather_data['air_quality']['aqi']
    aqi_category = weather_data['air_quality']['category']
    pm2_5 = weather_data['air_quality']['pm2_5']
    
    # ================== WEATHER-BASED RECOMMENDATIONS ==================
    
    # Temperature-based
    if temp < 10:
        recommendations['skincare_routine'].append(
            "🥶 Cold Weather Protocol: Apply rich, protective barrier cream"
        )
        recommendations['products']['moisturizer'].extend([
            "Heavy emollient moisturizer with ceramides",
            "Facial oil (argan, rosehip, or jojoba)",
            "Barrier repair cream with petrolatum"
        ])
        recommendations['warnings'].append(
            "⚠️ Cold temperatures can damage skin barrier. Layer moisturizers for protection."
        )
    elif temp > 30:
        recommendations['skincare_routine'].append(
            "🌡️ Hot Weather Protocol: Use lightweight, oil-free products"
        )
        recommendations['products']['moisturizer'].extend([
            "Gel-based moisturizer",
            "Oil-free hydrating serum",
            "Water-based lightweight lotion"
        ])
        recommendations['lifestyle_tips'].append(
            "Stay hydrated! Drink at least 8 glasses of water daily in hot weather."
        )
    
    # Humidity-based
    if humidity < 30:
        recommendations['skincare_routine'].append(
            "💧 Low Humidity Alert: Extra hydration needed"
        )
        recommendations['products']['treatment'].append(
            "Hyaluronic acid serum (holds 1000x its weight in water)"
        )
        recommendations['products']['other'].append(
            "Indoor humidifier to maintain skin moisture"
        )
        recommendations['warnings'].append(
            "⚠️ Dry air accelerates moisture loss. Apply moisturizer within 60 seconds of washing."
        )
    elif humidity > 70:
        recommendations['skincare_routine'].append(
            "💦 High Humidity: Control excess oil and prevent breakouts"
        )
        recommendations['products']['cleanser'].append(
            "Foaming gel cleanser with salicylic acid"
        )
        recommendations['products']['other'].extend([
            "Clay mask (use 2-3x per week)",
            "Blotting papers for oil control"
        ])
    
    # UV Index recommendations
    if uv_index >= 8:
        recommendations['priority_actions'].append(
            f"🚨 URGENT: UV Index is {uv_index} ({uv_risk}) - High sun damage risk!"
        )
        recommendations['products']['sunscreen'].append(
            "SPF 50+ broad-spectrum sunscreen (PA++++)"
        )
        recommendations['products']['sunscreen'].append(
            "Reapply sunscreen every 90 minutes"
        )
        recommendations['products']['other'].extend([
            "Wide-brimmed hat",
            "UV-protective sunglasses",
            "UPF-rated clothing for prolonged exposure"
        ])
        recommendations['warnings'].append(
            "⚠️ Extreme UV! Seek shade between 10 AM - 4 PM."
        )
    elif uv_index >= 6:
        recommendations['skincare_routine'].append(
            f"☀️ High UV Index ({uv_index}): Sun protection critical"
        )
        recommendations['products']['sunscreen'].append(
            "SPF 40-50 broad-spectrum sunscreen"
        )
        recommendations['products']['treatment'].append(
            "Antioxidant serum (Vitamin C or E) for UV defense"
        )
    elif uv_index >= 3:
        recommendations['products']['sunscreen'].append(
            f"SPF 30+ daily sunscreen (UV: {uv_index} - {uv_risk})"
        )
    else:
        recommendations['products']['sunscreen'].append(
            "SPF 15-30 daily moisturizer with sun protection"
        )
    
    # Wind protection
    if wind_speed > 15:
        recommendations['warnings'].append(
            f"💨 Strong winds ({wind_speed} m/s) can cause windburn and dehydration."
        )
        recommendations['products']['other'].append(
            "Windproof barrier cream or balm"
        )
    elif wind_speed > 10:
        recommendations['skincare_routine'].append(
            "🌬️ Windy conditions: Protect skin barrier"
        )
        recommendations['products']['moisturizer'].append(
            "Occlusive barrier cream"
        )
    
    # Weather condition specific
    if 'rain' in weather_condition or 'drizzle' in weather_condition:
        recommendations['lifestyle_tips'].append(
            "☔ Rainy weather can carry pollutants. Cleanse thoroughly after being outdoors."
        )
        recommendations['products']['sunscreen'].append(
            "Water-resistant sunscreen (clouds don't block UV)"
        )
    elif 'snow' in weather_condition:
        recommendations['warnings'].append(
            "❄️ Snow reflects up to 80% of UV rays! Double sun protection needed."
        )
        recommendations['products']['sunscreen'].append(
            "SPF 50+ (snow amplifies UV exposure)"
        )
    
    # ================== AIR QUALITY RECOMMENDATIONS ==================
    
    if aqi >= 4:  # Poor or Very Poor
        recommendations['priority_actions'].append(
            f"🚨 Poor Air Quality (AQI: {aqi_category}) - Skin protection essential!"
        )
        recommendations['skincare_routine'].extend([
            "Double cleanse to remove pollution particles",
            "Apply antioxidant serum before sunscreen",
            "Use barrier repair cream at night"
        ])
        recommendations['products']['cleanser'].append(
            "Micellar water or oil cleanser (1st cleanse)"
        )
        recommendations['products']['cleanser'].append(
            "Gentle foaming cleanser (2nd cleanse)"
        )
        recommendations['products']['treatment'].extend([
            "Vitamin C serum (antioxidant protection)",
            "Niacinamide serum (barrier strengthening)",
            "Pollution defense cream"
        ])
        recommendations['warnings'].append(
            f"⚠️ PM2.5: {pm2_5} μg/m³ - Fine particles can penetrate skin and accelerate aging."
        )
        recommendations['lifestyle_tips'].append(
            "Minimize outdoor exposure during peak pollution hours."
        )
    elif aqi == 3:  # Moderate
        recommendations['skincare_routine'].append(
            f"🌫️ Moderate Air Quality: Antioxidant protection recommended"
        )
        recommendations['products']['treatment'].append(
            "Antioxidant serum (Vitamin C, E, or Ferulic Acid)"
        )
        recommendations['products']['cleanser'].append(
            "Thorough cleansing after outdoor activities"
        )
    else:  # Good or Fair
        recommendations['lifestyle_tips'].append(
            f"✅ Good air quality ({aqi_category}) - Normal skincare routine sufficient."
        )
    
    # ================== SKIN CONDITION RECOMMENDATIONS ==================
    
    for condition in skin_conditions:
        condition_type = condition['type'].lower()
        severity = condition['severity']
        score = condition['score']
        
        if condition_type == 'acne':
            recommendations['priority_actions'].append(
                f"🔴 Acne Detected (Score: {score:.1f}, Severity: {severity.upper()})"
            )
            recommendations['skincare_routine'].extend([
                "Morning: Gentle cleanser → Spot treatment → Light moisturizer → Sunscreen",
                "Evening: Cleanser → Acne treatment → Moisturizer",
                "Use non-comedogenic products only"
            ])
            recommendations['products']['cleanser'].append(
                "Salicylic acid cleanser (2%) or Benzoyl peroxide (2.5-5%)"
            )
            recommendations['products']['treatment'].extend([
                "Benzoyl peroxide spot treatment",
                "Niacinamide serum (reduces inflammation)",
                "Retinoid cream (evening) - start slow"
            ])
            recommendations['products']['moisturizer'].append(
                "Oil-free, non-comedogenic gel moisturizer"
            )
            recommendations['warnings'].append(
                "⚠️ Avoid picking or squeezing acne - can cause scarring and infection."
            )
            recommendations['lifestyle_tips'].extend([
                "Change pillowcases every 2-3 days",
                "Avoid touching your face throughout the day",
                "Remove makeup before sleeping"
            ])
            
        elif condition_type == 'pigmentation':
            recommendations['priority_actions'].append(
                f"⚫ Pigmentation Detected (Score: {score:.1f})"
            )
            recommendations['skincare_routine'].extend([
                "Morning: Cleanser → Vitamin C serum → Sunscreen (ESSENTIAL)",
                "Evening: Cleanser → Treatment serum → Retinol → Moisturizer",
                "Consistency is key - results take 6-12 weeks"
            ])
            recommendations['products']['treatment'].extend([
                "Vitamin C serum 15-20% (morning)",
                "Niacinamide 10% (reduces pigmentation)",
                "Retinol 0.5-1% (evening - builds tolerance)",
                "Alpha arbutin or kojic acid serum",
                "Azelaic acid 10-20%"
            ])
            recommendations['products']['sunscreen'].append(
                "SPF 50+ (NON-NEGOTIABLE - prevents darkening)"
            )
            recommendations['warnings'].append(
                "⚠️ Sun exposure will worsen pigmentation! Sunscreen is mandatory daily."
            )
            recommendations['lifestyle_tips'].append(
                "Wear hats and seek shade - physical protection helps"
            )
            
        elif condition_type == 'sunburn':
            recommendations['priority_actions'].append(
                f"☀️ Sunburn Detected (Score: {score:.1f}) - Immediate care needed!"
            )
            recommendations['skincare_routine'].extend([
                "🚨 IMMEDIATE: Apply cool compress for 10-15 minutes",
                "Apply aloe vera gel or hydrocortisone cream",
                "Avoid further sun exposure until healed",
                "Take ibuprofen if painful (reduces inflammation)"
            ])
            recommendations['products']['treatment'].extend([
                "Pure aloe vera gel (refrigerate for cooling effect)",
                "Hydrocortisone cream 1% (for inflammation)",
                "Hyaluronic acid serum (hydration)",
                "Gentle, fragrance-free moisturizer"
            ])
            recommendations['products']['other'].append(
                "Oral antihistamine if itching is severe"
            )
            recommendations['warnings'].extend([
                "⚠️ Do NOT pop blisters if present - risk of infection",
                "⚠️ Stay out of sun completely until healed",
                "⚠️ Drink extra water - sunburn dehydrates body"
            ])
            recommendations['lifestyle_tips'].extend([
                "Wear loose, breathable clothing",
                "Avoid hot showers - use cool/lukewarm water",
                "Sleep on your back to avoid pressure on burns"
            ])
            
        elif condition_type == 'fungal infection' or condition_type == 'fungal_infection':
            recommendations['priority_actions'].append(
                f"🦠 Possible Fungal Infection (Score: {score:.1f}) - Consult dermatologist!"
            )
            recommendations['skincare_routine'].extend([
                "Keep affected area clean and dry",
                "Apply antifungal cream as prescribed",
                "Avoid sharing towels or personal items"
            ])
            recommendations['products']['treatment'].extend([
                "Antifungal cream (clotrimazole, miconazole) - OTC",
                "Tea tree oil (diluted) - natural antifungal",
                "Gentle, pH-balanced cleanser"
            ])
            recommendations['warnings'].extend([
                "⚠️ See a dermatologist for proper diagnosis",
                "⚠️ Don't self-treat if unsure - incorrect treatment worsens condition",
                "⚠️ Fungal infections are contagious - hygiene is critical"
            ])
            recommendations['lifestyle_tips'].extend([
                "Wash clothes and bedding in hot water",
                "Dry skin thoroughly after bathing",
                "Avoid excessive sweating (change clothes promptly)"
            ])
            
        elif condition_type == 'eczema':
            recommendations['priority_actions'].append(
                f"🟥 Eczema Detected (Score: {score:.1f})"
            )
            recommendations['skincare_routine'].extend([
                "Morning: Gentle cleanser → Moisturizer → Sunscreen",
                "Evening: Gentle cleanser → Treatment → Heavy moisturizer",
                "Apply moisturizer immediately after bathing (within 3 min)",
                "Moisturize at least 2-3 times daily"
            ])
            recommendations['products']['cleanser'].append(
                "Fragrance-free, gentle cream cleanser (avoid soap)"
            )
            recommendations['products']['treatment'].extend([
                "Colloidal oatmeal cream (soothing)",
                "Ceramide-rich barrier repair cream",
                "Hydrocortisone 1% (short-term flare-ups)",
                "Calamine lotion (for itching)"
            ])
            recommendations['products']['moisturizer'].extend([
                "Thick ointment or cream (not lotion)",
                "Petroleum jelly or CeraVe Healing Ointment",
                "Aveeno Eczema Therapy or Eucerin Original"
            ])
            recommendations['warnings'].extend([
                "⚠️ Avoid hot water - lukewarm only",
                "⚠️ Don't scratch! Trim nails short",
                "⚠️ Avoid fragrances, dyes, and harsh ingredients"
            ])
            recommendations['lifestyle_tips'].extend([
                "Wear soft, breathable cotton fabrics",
                "Use fragrance-free laundry detergent",
                "Identify and avoid triggers (stress, allergens)",
                "Use a humidifier in dry environments"
            ])
            
        elif condition_type == 'dryness':
            recommendations['priority_actions'].append(
                f"🏜️ Dryness Detected (Score: {score:.1f})"
            )
            recommendations['skincare_routine'].extend([
                "Apply moisturizer within 60 seconds of washing",
                "Layer products: serum → moisturizer → facial oil (optional)",
                "Use gentle, cream-based cleansers (avoid foaming)"
            ])
            recommendations['products']['cleanser'].append(
                "Creamy, hydrating cleanser (no sulfates)"
            )
            recommendations['products']['treatment'].extend([
                "Hyaluronic acid serum (deep hydration)",
                "Glycerin-based serum",
                "Urea cream 5-10% (exfoliates + hydrates)"
            ])
            recommendations['products']['moisturizer'].extend([
                "Rich cream with ceramides and fatty acids",
                "Overnight sleeping mask or heavy cream",
                "Facial oil: rosehip, argan, or jojoba"
            ])
            recommendations['products']['other'].append(
                "Room humidifier (especially winter months)"
            )
            recommendations['lifestyle_tips'].extend([
                "Drink 8+ glasses of water daily",
                "Limit hot showers (5-10 minutes max)",
                "Avoid alcohol-based products",
                "Eat omega-3 rich foods (fish, nuts, avocado)"
            ])
            
        elif condition_type == 'healthy':
            recommendations['lifestyle_tips'].append(
                "✅ Skin appears healthy! Maintain your routine."
            )
    
    # ================== GENERAL RECOMMENDATIONS ==================
    
    recommendations['lifestyle_tips'].extend([
        "💧 Stay hydrated - drink 8-10 glasses of water daily",
        "😴 Get 7-9 hours of quality sleep for skin regeneration",
        "🥗 Eat antioxidant-rich foods (berries, leafy greens, nuts)",
        "🚭 Avoid smoking and excessive alcohol - damages skin",
        "💆 Manage stress - cortisol affects skin health"
    ])
    
    # Add general disclaimer
    recommendations['warnings'].append(
        "📋 This is AI-generated advice. Consult a dermatologist for persistent or severe concerns."
    )
    
    # Remove duplicates and sort
    for key in recommendations:
        if isinstance(recommendations[key], list):
            recommendations[key] = list(dict.fromkeys(recommendations[key]))
    
    # Flatten products dict for easier display
    all_products = []
    for category, items in recommendations['products'].items():
        all_products.extend(items)
    recommendations['products_list'] = list(dict.fromkeys(all_products))
    
    return recommendations
