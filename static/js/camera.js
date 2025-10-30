// Camera Module for Real-time Face Analysis
// Handles webcam access, face detection, and snapshot capture

class CameraManager {
    constructor() {
        this.stream = null;
        this.videoElement = null;
        this.canvasElement = null;
        this.isActive = false;
        this.facingMode = 'user'; // 'user' for front camera, 'environment' for back camera
    }

    async initialize(videoElement, canvasElement) {
        this.videoElement = videoElement;
        this.canvasElement = canvasElement;
    }

    async startCamera() {
        try {
            // Check if camera is already active
            if (this.isActive && this.stream) {
                console.log('Camera already active');
                return true;
            }

            // Request camera access with constraints
            const constraints = {
                video: {
                    facingMode: this.facingMode,
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            };

            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            
            // Attach stream to video element
            this.videoElement.srcObject = this.stream;
            
            // Wait for video to load metadata
            await new Promise((resolve) => {
                this.videoElement.onloadedmetadata = () => {
                    this.videoElement.play();
                    resolve();
                };
            });

            this.isActive = true;
            console.log('Camera started successfully');
            return true;

        } catch (error) {
            console.error('Error accessing camera:', error);
            
            // Provide user-friendly error messages
            let errorMessage = 'Unable to access camera. ';
            
            if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                errorMessage += 'Please allow camera access in your browser settings.';
            } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
                errorMessage += 'No camera found on your device.';
            } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
                errorMessage += 'Camera is already in use by another application.';
            } else {
                errorMessage += error.message || 'Unknown error occurred.';
            }
            
            throw new Error(errorMessage);
        }
    }

    stopCamera() {
        if (this.stream) {
            // Stop all tracks
            this.stream.getTracks().forEach(track => {
                track.stop();
            });
            
            // Clear video source
            if (this.videoElement) {
                this.videoElement.srcObject = null;
            }
            
            this.stream = null;
            this.isActive = false;
            console.log('Camera stopped');
        }
    }

    async switchCamera() {
        // Toggle between front and back camera
        this.facingMode = this.facingMode === 'user' ? 'environment' : 'user';
        
        // Restart camera with new facing mode
        if (this.isActive) {
            this.stopCamera();
            await this.startCamera();
        }
    }

    captureSnapshot() {
        if (!this.isActive || !this.videoElement || !this.canvasElement) {
            throw new Error('Camera not active or elements not initialized');
        }

        // Set canvas dimensions to match video
        this.canvasElement.width = this.videoElement.videoWidth;
        this.canvasElement.height = this.videoElement.videoHeight;

        // Draw current video frame to canvas
        const context = this.canvasElement.getContext('2d');
        context.drawImage(
            this.videoElement, 
            0, 0, 
            this.canvasElement.width, 
            this.canvasElement.height
        );

        // Convert canvas to blob
        return new Promise((resolve, reject) => {
            this.canvasElement.toBlob((blob) => {
                if (blob) {
                    // Create file from blob
                    const file = new File(
                        [blob], 
                        `face_snapshot_${Date.now()}.jpg`, 
                        { type: 'image/jpeg' }
                    );
                    resolve(file);
                } else {
                    reject(new Error('Failed to capture snapshot'));
                }
            }, 'image/jpeg', 0.95);
        });
    }

    getSnapshot() {
        if (!this.isActive || !this.videoElement || !this.canvasElement) {
            throw new Error('Camera not active or elements not initialized');
        }

        // Set canvas dimensions to match video
        this.canvasElement.width = this.videoElement.videoWidth;
        this.canvasElement.height = this.videoElement.videoHeight;

        // Draw current video frame to canvas
        const context = this.canvasElement.getContext('2d');
        context.drawImage(
            this.videoElement, 
            0, 0, 
            this.canvasElement.width, 
            this.canvasElement.height
        );

        // Return data URL
        return this.canvasElement.toDataURL('image/jpeg', 0.95);
    }

    isSupported() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    }

    async getAvailableCameras() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            return devices.filter(device => device.kind === 'videoinput');
        } catch (error) {
            console.error('Error enumerating devices:', error);
            return [];
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CameraManager;
}
