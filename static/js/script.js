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
    document.getElementById('temperature').textContent = `${Math.round(data.temperature)}°C`;
    document.getElementById('weatherDescription').textContent = data.weather_description;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
    
    // Set weather icon
    const weatherIcon = getWeatherIcon(data.weather_condition);
    document.getElementById('weatherIcon').textContent = weatherIcon;

    // Display skincare tips
    const tipsList = document.getElementById('skincareTips');
    tipsList.innerHTML = '';
    data.skincare_tips.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        tipsList.appendChild(li);
    });

    // Display product recommendations
    const productsList = document.getElementById('productsRecommended');
    productsList.innerHTML = '';
    
    if (data.products_recommended && data.products_recommended.length > 0) {
        data.products_recommended.forEach(product => {
            const li = document.createElement('li');
            li.textContent = product;
            productsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'Continue with your regular skincare routine.';
        productsList.appendChild(li);
    }

    // Display warnings
    const warningsList = document.getElementById('warnings');
    const warningsCard = document.getElementById('warningsCard');
    warningsList.innerHTML = '';
    
    if (data.warnings && data.warnings.length > 0) {
        data.warnings.forEach(warning => {
            const li = document.createElement('li');
            li.textContent = warning;
            warningsList.appendChild(li);
        });
        showElement('warningsCard');
    } else {
        hideElement('warningsCard');
    }

    // Show results
    showElement('results');
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    showElement('error');
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

// Add smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Weather-based Skin Health App Loaded');
});
