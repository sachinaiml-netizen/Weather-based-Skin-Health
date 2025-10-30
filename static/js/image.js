// Image Analysis Page JavaScript

// Upload elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('uploadSection');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const previewImage = document.getElementById('previewImage');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const resultsDiv = document.getElementById('results');

// Camera elements
const cameraSection = document.getElementById('cameraSection');
const cameraVideo = document.getElementById('cameraVideo');
const cameraCanvas = document.getElementById('cameraCanvas');
const startCameraBtn = document.getElementById('startCameraBtn');
const captureBtn = document.getElementById('captureBtn');
const stopCameraBtn = document.getElementById('stopCameraBtn');
const modeBtns = document.querySelectorAll('.mode-btn');

let selectedFile = null;
let stream = null;
let currentMode = 'upload';

// Mode toggle
modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;
        switchMode(mode);
    });
});

function switchMode(mode) {
    currentMode = mode;
    
    // Update button states
    modeBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    
    // Show/hide sections
    if (mode === 'upload') {
        uploadSection.classList.remove('hidden');
        cameraSection.classList.add('hidden');
        stopCamera();
    } else {
        uploadSection.classList.add('hidden');
        cameraSection.classList.remove('hidden');
        previewContainer.classList.add('hidden');
    }
    
    // Reset results
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

// Camera controls
startCameraBtn.addEventListener('click', startCamera);
captureBtn.addEventListener('click', capturePhoto);
stopCameraBtn.addEventListener('click', stopCamera);

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        cameraVideo.srcObject = stream;
        
        // Update UI
        startCameraBtn.classList.add('hidden');
        captureBtn.classList.remove('hidden');
        stopCameraBtn.classList.remove('hidden');
        errorDiv.classList.add('hidden');
        
    } catch (error) {
        console.error('Camera error:', error);
        showError('Unable to access camera. Please check permissions.');
    }
}

function capturePhoto() {
    // Set canvas size to video size
    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;
    
    // Draw video frame to canvas
    const ctx = cameraCanvas.getContext('2d');
    ctx.drawImage(cameraVideo, 0, 0);
    
    // Convert canvas to blob
    cameraCanvas.toBlob((blob) => {
        selectedFile = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        
        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            cameraSection.classList.add('hidden');
            previewContainer.classList.remove('hidden');
            stopCamera();
        };
        reader.readAsDataURL(selectedFile);
    }, 'image/jpeg', 0.95);
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        cameraVideo.srcObject = null;
    }
    
    // Reset UI
    startCameraBtn.classList.remove('hidden');
    captureBtn.classList.add('hidden');
    stopCameraBtn.classList.add('hidden');
}

// Click upload box to select file
uploadBox.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'var(--accent)';
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = 'var(--border)';
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'var(--border)';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        handleFile(file);
    }
});

// Remove image
removeBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    uploadSection.classList.remove('hidden');
    previewContainer.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
});

// Analyze image
analyzeBtn.addEventListener('click', analyzeImage);

function handleFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please upload an image file (PNG, JPG, JPEG)');
        return;
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('File size must be less than 5MB');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadSection.classList.add('hidden');
        previewContainer.classList.remove('hidden');
        errorDiv.classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

async function analyzeImage() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }
    
    // Show loading, hide results and errors
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    // Create form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/api/analyze-image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'Failed to analyze image');
        }
    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        loadingDiv.classList.add('hidden');
    }
}

function displayResults(data) {
    // Display analysis info
    document.getElementById('analysisDate').textContent = new Date().toLocaleDateString();
    document.getElementById('analysisTime').textContent = new Date().toLocaleTimeString();
    
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
        li.textContent = '✓ No major concerns detected. Maintain your regular skincare routine.';
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
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
