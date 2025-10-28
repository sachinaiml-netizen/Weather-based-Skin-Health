// Weather icon mapping
const weatherIcons = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'drizzle': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
    'fog': '🌫️',
    'haze': '🌫️',
    'default': '🌤️'
};

// Concern type icons
const concernIcons = {
    'Dryness': '🏜️',
    'Acne': '🔴',
    'Sunburn': '☀️',
    'Sensitivity': '⚠️',
    'Oiliness': '💧'
};

// Get weather icon based on condition
function getWeatherIcon(condition) {
    const lowerCondition = condition.toLowerCase();
    return weatherIcons[lowerCondition] || weatherIcons['default'];
}

// Handle Enter key press in city input
document.getElementById('cityInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        getRecommendations();
    }
});

// Main function to get recommendations
async function getRecommendations() {
    const city = document.getElementById('cityInput').value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }

    // Hide previous results and errors
    hideElement('results');
    hideElement('error');
    showElement('loading');

    try {
        const response = await fetch('/get_recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city: city })
        });

        const data = await response.json();

        hideElement('loading');

        if (data.error) {
            showError(data.error);
            return;
        }

        displayResults(data);
    } catch (error) {
        hideElement('loading');
        showError('An error occurred while fetching data. Please try again.');
        console.error('Error:', error);
    }
}

// Display results on the page
function displayResults(data) {
    // Display weather information
    document.getElementById('cityName').textContent = `${data.city}, ${data.country}`;
    document.getElementById('weatherDescription').textContent = data.weather_description;
    document.getElementById('temperature').textContent = `${Math.round(data.temperature)}°C`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
    
    // Display UV Index
    if (data.uv_index !== undefined) {
        document.getElementById('uvIndex').textContent = data.uv_index;
        document.getElementById('uvRisk').textContent = `UV: ${data.uv_risk}`;
    }
    
    // Set weather icon
    const weatherIcon = getWeatherIcon(data.weather_condition);
    document.getElementById('weatherIconLarge').textContent = weatherIcon;

    // Display AI-predicted concerns
    displayPredictedConcerns(data.predicted_concerns);

    // Display skincare tips
    displaySkincareTips(data.skincare_tips);

    // Display product recommendations
    displayProducts(data.products_recommended);

    // Display warnings
    displayWarnings(data.warnings);

    // Show results with animation
    showElement('results');
    
    // Smooth scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display AI-predicted skin concerns
function displayPredictedConcerns(concerns) {
    const concernsContainer = document.getElementById('predictedConcerns');
    concernsContainer.innerHTML = '';

    if (!concerns || concerns.length === 0) {
        concernsContainer.innerHTML = '<p class="no-concerns">✅ No significant skin concerns predicted for current weather conditions!</p>';
        return;
    }

    concerns.forEach(concern => {
        const card = document.createElement('div');
        card.className = `concern-card ${concern.severity}`;
        
        const icon = concernIcons[concern.type] || '🔍';
        
        card.innerHTML = `
            <div class="concern-header">
                <div class="concern-type">${icon} ${concern.type}</div>
                <span class="concern-badge ${concern.severity}">${concern.risk}</span>
            </div>
            <div class="concern-details">
                <div class="concern-score">
                    <span>Risk Score:</span>
                    <span><strong>${Math.round(concern.score)}/100</strong></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${concern.score}%"></div>
                </div>
                <div class="confidence-text">
                    🤖 AI Confidence: ${Math.round(concern.confidence)}%
                </div>
            </div>
        `;
        
        concernsContainer.appendChild(card);
        
        // Animate progress bar
        setTimeout(() => {
            const fill = card.querySelector('.progress-fill');
            fill.style.width = `${concern.score}%`;
        }, 100);
    });
}

// Display skincare tips
function displaySkincareTips(tips) {
    const tipsContainer = document.getElementById('skincareTips');
    tipsContainer.innerHTML = '';

    if (!tips || tips.length === 0) {
        tips = ['Continue with your regular skincare routine.'];
    }

    tips.forEach(tip => {
        const card = document.createElement('div');
        card.className = 'tip-card';
        card.textContent = tip;
        tipsContainer.appendChild(card);
    });
}

// Display product recommendations
function displayProducts(products) {
    const productsContainer = document.getElementById('productsRecommended');
    productsContainer.innerHTML = '';

    if (!products || products.length === 0) {
        products = ['Continue with your regular skincare products.'];
    }

    // Remove duplicates
    const uniqueProducts = [...new Set(products)];

    uniqueProducts.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-icon">🧴</div>
            <div class="product-name">${product}</div>
        `;
        productsContainer.appendChild(card);
    });
}

// Display warnings
function displayWarnings(warnings) {
    const warningsContainer = document.getElementById('warnings');
    const warningsSection = document.getElementById('warningsSection');
    warningsContainer.innerHTML = '';

    if (!warnings || warnings.length === 0) {
        hideElement('warningsSection');
        return;
    }

    warnings.forEach(warning => {
        const card = document.createElement('div');
        card.className = 'warning-card';
        card.innerHTML = `
            <div class="warning-icon">⚠️</div>
            <div>${warning}</div>
        `;
        warningsContainer.appendChild(card);
    });

    showElement('warningsSection');
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    showElement('error');
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        hideElement('error');
    }, 5000);
}

// Helper function to show element
function showElement(id) {
    const element = document.getElementById(id);
    if (element) {
        element.classList.remove('hidden');
    }
}

// Helper function to hide element
function hideElement(id) {
    const element = document.getElementById(id);
    if (element) {
        element.classList.add('hidden');
    }
}

// Add smooth animations on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🧬 AI Weather-based Skin Health App Loaded');
    
    // Add fade-in animation to hero
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.animation = 'fadeInUp 0.8s ease';
    }
});

// Add particle effect on button click
document.getElementById('searchBtn').addEventListener('click', function(e) {
    createRipple(e);
});

function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');

    const ripple = button.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }

    button.appendChild(circle);
}
