// Main JavaScript for Weather-based Skin Health App

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadContainer = document.getElementById('uploadContainer');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const removeBtn = document.getElementById('removeBtn');
const analyzeImageBtn = document.getElementById('analyzeImageBtn');
const loadingDiv = document.getElementById('loading');
const loadingText = document.getElementById('loadingText');
const errorDiv = document.getElementById('error');
const resultsDiv = document.getElementById('results');
const weatherCard = document.getElementById('weatherCard');

let selectedFile = null;
let currentAnalysisType = 'weather'; // 'weather' or 'image'

// Event Listeners
searchBtn.addEventListener('click', analyzeWeather);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzeWeather();
});

uploadBox.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleFile(e.target.files[0]);
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = '#00d4ff';
    uploadBox.style.transform = 'scale(1.02)';
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    uploadBox.style.transform = 'scale(1)';
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    uploadBox.style.transform = 'scale(1)';
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

removeBtn.addEventListener('click', removeImage);
analyzeImageBtn.addEventListener('click', analyzeImage);

// Weather Analysis
async function analyzeWeather() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    currentAnalysisType = 'weather';
    showLoading('Analyzing weather conditions...');
    hideError();
    resultsDiv.classList.add('hidden');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city: city })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data, 'weather');
        } else {
            showError(data.error || 'Failed to fetch weather data. Please check the city name.');
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Image Upload Handling
function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please upload an image file (PNG, JPG, JPEG)');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        showError('File size must be less than 5MB');
        return;
    }
    
    selectedFile = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadContainer.classList.add('hidden');
        previewSection.classList.remove('hidden');
        hideError();
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    selectedFile = null;
    fileInput.value = '';
    previewImage.src = '';
    uploadContainer.classList.remove('hidden');
    previewSection.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    hideError();
}

// Image Analysis
async function analyzeImage() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }
    
    currentAnalysisType = 'image';
    showLoading('Analyzing skin condition from image...');
    hideError();
    resultsDiv.classList.add('hidden');
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/api/analyze-image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data, 'image');
        } else {
            showError(data.error || 'Failed to analyze image. Please try another photo.');
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Display Results
function displayResults(data, type) {
    // Show/hide weather card based on analysis type
    if (type === 'weather') {
        weatherCard.style.display = 'block';
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('temperature').textContent = `${Math.round(data.weather.temperature)}°C`;
        document.getElementById('weatherDescription').textContent = data.weather.description;
        document.getElementById('weatherIcon').textContent = getWeatherEmoji(data.weather.description);
        document.getElementById('humidity').textContent = `${data.weather.humidity}%`;
        document.getElementById('feelsLike').textContent = `${Math.round(data.weather.feels_like)}°C`;
        document.getElementById('windSpeed').textContent = `${data.weather.wind_speed} m/s`;
        document.getElementById('uvIndex').textContent = data.weather.uv_index || 'N/A';
        document.getElementById('pressure').textContent = `${data.weather.pressure} hPa`;
        document.getElementById('analysisType').textContent = 'weather conditions';
    } else {
        weatherCard.style.display = 'none';
        document.getElementById('analysisType').textContent = 'uploaded image analysis';
    }
    
    // Display predictions
    displayConcerns(data.predictions);
    
    // Display recommendations
    displayRecommendations(data.recommendations);
    
    // Display products
    displayProducts(data.products);
    
    // Display warnings
    displayWarnings(data.warnings);
    
    // Show results with smooth scroll
    resultsDiv.classList.remove('hidden');
    setTimeout(() => {
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function displayConcerns(predictions) {
    const grid = document.getElementById('concernsGrid');
    grid.innerHTML = '';
    
    Object.entries(predictions).forEach(([type, data]) => {
        const riskLevel = data.risk_level.toLowerCase().replace(' risk', '');
        const score = Math.round(data.score);
        const confidence = Math.round(data.confidence);
        
        const card = document.createElement('div');
        card.className = 'concern-card';
        card.innerHTML = `
            <div class="concern-header">
                <div class="concern-type">${capitalizeFirst(type.replace('_', ' '))}</div>
                <span class="concern-badge ${riskLevel}">${data.risk_level}</span>
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
    
    if (recommendations.length === 0) {
        const li = document.createElement('li');
        li.textContent = '✓ No specific recommendations at this time. Maintain your regular skincare routine.';
        list.appendChild(li);
        return;
    }
    
    recommendations.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        list.appendChild(li);
    });
}

function displayProducts(products) {
    const list = document.getElementById('productsList');
    list.innerHTML = '';
    
    if (products.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No specific products recommended at this time.';
        list.appendChild(li);
        return;
    }
    
    // Remove duplicates
    const uniqueProducts = [...new Set(products)];
    
    uniqueProducts.forEach(product => {
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
        li.textContent = '✓ No major warnings. Conditions are favorable for skin health.';
        li.style.borderColor = '#10b981';
        li.style.background = 'rgba(16, 185, 129, 0.1)';
        li.style.color = '#6ee7b7';
        list.appendChild(li);
        return;
    }
    
    warnings.forEach(warning => {
        const li = document.createElement('li');
        li.textContent = warning;
        list.appendChild(li);
    });
}

// Helper Functions
function showLoading(text = 'Loading...') {
    loadingText.textContent = text;
    loadingDiv.classList.remove('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function showError(message) {
    errorDiv.textContent = '❌ ' + message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => {
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

function hideError() {
    errorDiv.classList.add('hidden');
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
