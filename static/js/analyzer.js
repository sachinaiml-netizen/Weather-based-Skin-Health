// Weather-Based Skin Analyzer - JavaScript

let weatherData = null;
let selectedFile = null;

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const geolocateBtn = document.getElementById('geolocateBtn');
const weatherResults = document.getElementById('weatherResults');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImageBtn = document.getElementById('removeImageBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const dismissError = document.getElementById('dismissError');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    searchBtn.addEventListener('click', searchWeather);
    geolocateBtn.addEventListener('click', getGeolocation);
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchWeather();
    });
    
    // File upload
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);
    removeImageBtn.addEventListener('click', removeImage);
    
    // Analyze button
    analyzeBtn.addEventListener('click', analyzeComplete);
    
    // Error dismiss
    dismissError.addEventListener('click', () => {
        errorMessage.classList.add('hidden');
    });
}

// Weather Functions
async function searchWeather() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<span class="btn-icon">⏳</span> Loading...';
    
    try {
        const response = await fetch('/api/weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ city })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            weatherData = data;
            displayWeather(data);
            checkAnalyzeButton();
        } else {
            showError(data.error || 'Failed to fetch weather data');
        }
    } catch (error) {
        showError('Network error. Please check your connection.');
        console.error('Error:', error);
    } finally {
        searchBtn.disabled = false;
        searchBtn.innerHTML = '<span class="btn-icon">🔍</span> Get Weather';
    }
}

async function getGeolocation() {
    if (!navigator.geolocation) {
        showError('Geolocation is not supported by your browser');
        return;
    }
    
    geolocateBtn.disabled = true;
    geolocateBtn.innerHTML = '<span class="btn-icon">⏳</span> Getting Location...';
    
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            try {
                const response = await fetch('/api/geolocation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ lat, lon })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    weatherData = data;
                    cityInput.value = data.city;
                    displayWeather(data);
                    checkAnalyzeButton();
                } else {
                    showError(data.error || 'Failed to fetch weather data');
                }
            } catch (error) {
                showError('Network error. Please check your connection.');
                console.error('Error:', error);
            } finally {
                geolocateBtn.disabled = false;
                geolocateBtn.innerHTML = '<span class="btn-icon">📍</span> Use My Location';
            }
        },
        (error) => {
            showError('Unable to retrieve your location. Please enter city manually.');
            geolocateBtn.disabled = false;
            geolocateBtn.innerHTML = '<span class="btn-icon">📍</span> Use My Location';
        }
    );
}

function displayWeather(data) {
    document.getElementById('temperature').textContent = `${Math.round(data.weather.temperature)}°C`;
    document.getElementById('humidity').textContent = `${data.weather.humidity}%`;
    document.getElementById('uvIndex').textContent = data.uv.index;
    
    const uvRisk = document.getElementById('uvRisk');
    uvRisk.textContent = data.uv.risk;
    uvRisk.className = 'weather-badge';
    
    if (data.uv.risk === 'Low') {
        uvRisk.classList.add('badge-low');
    } else if (data.uv.risk === 'Moderate') {
        uvRisk.classList.add('badge-moderate');
    } else {
        uvRisk.classList.add('badge-high');
    }
    
    document.getElementById('aqi').textContent = data.air_quality.category;
    
    const aqiCategory = document.getElementById('aqiCategory');
    aqiCategory.textContent = `AQI: ${data.air_quality.aqi}`;
    aqiCategory.className = 'weather-badge';
    
    if (data.air_quality.aqi <= 2) {
        aqiCategory.classList.add('badge-good');
    } else if (data.air_quality.aqi === 3) {
        aqiCategory.classList.add('badge-moderate');
    } else {
        aqiCategory.classList.add('badge-poor');
    }
    
    weatherResults.classList.remove('hidden');
}

// File Upload Functions
function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG, PNG, or JPEG');
        return;
    }
    
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('File too large. Maximum size is 5MB');
        return;
    }
    
    selectedFile = file;
    
    // Display preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = formatFileSize(file.size);
        
        dropZone.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        
        checkAnalyzeButton();
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    selectedFile = null;
    fileInput.value = '';
    
    imagePreview.classList.add('hidden');
    dropZone.classList.remove('hidden');
    
    checkAnalyzeButton();
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function checkAnalyzeButton() {
    if (weatherData && selectedFile) {
        analyzeBtn.disabled = false;
    } else {
        analyzeBtn.disabled = true;
    }
}

// Analysis Functions
async function analyzeComplete() {
    if (!weatherData || !selectedFile) {
        showError('Please provide both weather data and skin image');
        return;
    }
    
    analyzeBtn.disabled = true;
    loadingIndicator.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    errorMessage.classList.add('hidden');
    
    const formData = new FormData();
    formData.append('city', weatherData.city);
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/api/analyze-complete', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'Analysis failed. Please try again.');
        }
    } catch (error) {
        showError('Network error. Please check your connection.');
        console.error('Error:', error);
    } finally {
        loadingIndicator.classList.add('hidden');
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    // Display detected conditions
    const conditionsGrid = document.getElementById('conditionsGrid');
    conditionsGrid.innerHTML = '';
    
    if (data.skin_analysis.conditions.length > 0) {
        data.skin_analysis.conditions.forEach(condition => {
            const card = createConditionCard(condition);
            conditionsGrid.appendChild(card);
        });
    } else {
        conditionsGrid.innerHTML = '<p>No specific conditions detected. Skin appears healthy!</p>';
    }
    
    // Display weather risks
    const weatherRisks = document.getElementById('weatherRisks');
    weatherRisks.innerHTML = '';
    
    if (data.recommendations.warnings.length > 0) {
        data.recommendations.warnings.slice(0, 5).forEach(warning => {
            const alert = document.createElement('div');
            alert.className = 'alert alert-warning';
            alert.innerHTML = `
                <div class="alert-icon">⚠️</div>
                <div class="alert-content">${warning}</div>
            `;
            weatherRisks.appendChild(alert);
        });
    }
    
    // Display recommendations
    if (data.recommendations.priority_actions.length > 0) {
        const priorityActions = document.getElementById('priorityActions');
        priorityActions.innerHTML = data.recommendations.priority_actions
            .map(action => `<div class="priority-item">${action}</div>`)
            .join('');
    }
    
    const routineList = document.getElementById('routineList');
    routineList.innerHTML = data.recommendations.skincare_routine
        .map(tip => `<li>${tip}</li>`)
        .join('');
    
    const productsList = document.getElementById('productsList');
    productsList.innerHTML = data.recommendations.products_list
        .slice(0, 15)  // Limit to 15 products
        .map(product => `<li>🛒 ${product}</li>`)
        .join('');
    
    const lifestyleTips = document.getElementById('lifestyleTips');
    lifestyleTips.innerHTML = data.recommendations.lifestyle_tips
        .map(tip => `<li>${tip}</li>`)
        .join('');
    
    const warningsList = document.getElementById('warningsList');
    warningsList.innerHTML = data.recommendations.warnings
        .map(warning => `<div class="warning-item">${warning}</div>`)
        .join('');
    
    // Show results
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

function createConditionCard(condition) {
    const card = document.createElement('div');
    card.className = 'condition-card';
    
    const severityClass = `severity-${condition.severity}`;
    
    card.innerHTML = `
        <div class="condition-header">
            <span class="condition-name">${condition.type}</span>
            <span class="condition-severity ${severityClass}">${condition.severity}</span>
        </div>
        <div class="condition-scores">
            <div class="score-item">
                <div class="score-label">Score</div>
                <div class="score-value">${condition.score}</div>
            </div>
            <div class="score-item">
                <div class="score-label">Confidence</div>
                <div class="score-value">${condition.confidence}%</div>
            </div>
        </div>
        ${condition.indicators && condition.indicators.length > 0 ? `
            <div class="condition-indicators">
                ${condition.indicators.map(indicator => 
                    `<span class="indicator-tag">${indicator}</span>`
                ).join('')}
            </div>
        ` : ''}
    `;
    
    return card;
}

// Error Handling
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    
    // Scroll to error
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}
