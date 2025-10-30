// Weather Page JavaScript

const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const resultsDiv = document.getElementById('results');

// Event listeners
searchBtn.addEventListener('click', analyzeWeather);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyzeWeather();
    }
});

async function analyzeWeather() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    // Show loading, hide results and errors
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city: city })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'Failed to fetch weather data');
        }
    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        loadingDiv.classList.add('hidden');
    }
}

function displayResults(data) {
    // Display weather information
    document.getElementById('cityName').textContent = data.city;
    document.getElementById('temperature').textContent = `${Math.round(data.weather.temperature)}°C`;
    document.getElementById('weatherDescription').textContent = data.weather.description;
    document.getElementById('weatherIcon').textContent = getWeatherEmoji(data.weather.description);
    
    // Display weather details
    document.getElementById('humidity').textContent = `${data.weather.humidity}%`;
    document.getElementById('feelsLike').textContent = `${Math.round(data.weather.feels_like)}°C`;
    document.getElementById('windSpeed').textContent = `${data.weather.wind_speed} m/s`;
    document.getElementById('uvIndex').textContent = data.weather.uv_index || 'N/A';
    document.getElementById('pressure').textContent = `${data.weather.pressure} hPa`;
    
    // Display skin concerns
    displayConcerns(data.predictions);
    
    // Display recommendations
    displayRecommendations(data.recommendations);
    
    // Display products
    displayProducts(data.products);
    
    // Display warnings
    displayWarnings(data.warnings);
    
    // Show results
    resultsDiv.classList.remove('hidden');
}

function displayConcerns(predictions) {
    const grid = document.getElementById('concernsGrid');
    grid.innerHTML = '';
    
    Object.entries(predictions).forEach(([type, data]) => {
        const riskLevel = data.risk_level;
        const score = Math.round(data.score);
        const confidence = Math.round(data.confidence);
        
        const card = document.createElement('div');
        card.className = 'concern-card';
        card.innerHTML = `
            <div class="concern-header">
                <div class="concern-type">${capitalizeFirst(type)}</div>
                <span class="concern-badge ${riskLevel.toLowerCase()}">${riskLevel}</span>
            </div>
            <div class="concern-score">Risk Score: ${score}/100</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${score}%"></div>
            </div>
            <div class="confidence-text">Confidence: ${confidence}%</div>
        `;
        grid.appendChild(card);
    });
}

function displayRecommendations(recommendations) {
    const list = document.getElementById('tipsList');
    list.innerHTML = '';
    
    recommendations.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        list.appendChild(li);
    });
}

function displayProducts(products) {
    const list = document.getElementById('productsList');
    list.innerHTML = '';
    
    products.forEach(product => {
        const li = document.createElement('li');
        li.textContent = product;
        list.appendChild(li);
    });
}

function displayWarnings(warnings) {
    const list = document.getElementById('warningsList');
    list.innerHTML = '';
    
    if (warnings.length === 0) {
        const li = document.createElement('li');
        li.textContent = '✓ No major warnings. Weather conditions are favorable for skin health.';
        li.style.borderColor = '#10b981';
        li.style.background = 'rgba(16, 185, 129, 0.1)';
        li.style.color = '#6ee7b7';
        list.appendChild(li);
    } else {
        warnings.forEach(warning => {
            const li = document.createElement('li');
            li.textContent = warning;
            list.appendChild(li);
        });
    }
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function getWeatherEmoji(description) {
    const desc = description.toLowerCase();
    if (desc.includes('clear')) return '☀️';
    if (desc.includes('cloud')) return '☁️';
    if (desc.includes('rain')) return '🌧️';
    if (desc.includes('thunder')) return '⛈️';
    if (desc.includes('snow')) return '❄️';
    if (desc.includes('mist') || desc.includes('fog')) return '🌫️';
    return '🌤️';
}
