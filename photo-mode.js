/**
 * PALCO ZERO - PHOTO MODE
 * Optional feature: Capture environment photo as background
 * Gracefully degrades if camera not available
 */

class PhotoMode {
    constructor() {
        this.stream = null;
        this.isSupported = false;
        this.photoModeBtn = null;
        this.captureBtn = null;
        this.exitBtn = null;
        this.cameraStream = null;
        this.photoBackground = null;

        this._init();
    }

    /**
     * Initialize Photo Mode
     */
    _init() {
        // Check camera support
        this.isSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);

        // Get DOM elements
        this.photoModeBtn = document.getElementById('photoModeBtn');
        this.captureBtn = document.getElementById('capturePhoto');
        this.exitBtn = document.getElementById('exitPhotoMode');
        this.cameraStream = document.getElementById('cameraStream');
        this.photoBackground = document.getElementById('photoBackground');

        if (!this.isSupported) {
            console.log('Photo Mode not supported on this device');
            this._hidePhotoModeCard();
            return;
        }

        // Show Photo Mode card
        this._showPhotoModeCard();

        // Set up event listeners
        this._setupEventListeners();
    }

    /**
     * Set up event listeners
     */
    _setupEventListeners() {
        if (this.photoModeBtn) {
            this.photoModeBtn.addEventListener('click', () => {
                this.enterPhotoMode();
            });
        }

        if (this.captureBtn) {
            this.captureBtn.addEventListener('click', () => {
                this.capturePhoto();
            });
        }

        if (this.exitBtn) {
            this.exitBtn.addEventListener('click', () => {
                this.exitPhotoMode();
            });
        }
    }

    /**
     * Enter Photo Mode
     */
    async enterPhotoMode() {
        try {
            // Request camera access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'environment', // Use back camera
                    width: { ideal: 1920 },
                    height: { ideal: 1080 }
                }
            });

            // Set stream to video element
            if (this.cameraStream) {
                this.cameraStream.srcObject = this.stream;
            }

            // Show Photo Mode UI
            const photoModeUI = document.getElementById('photoModeUI');
            if (photoModeUI) {
                photoModeUI.style.display = 'flex';
            }

            // Transition state
            if (window.stateMachine) {
                window.stateMachine.transition('photo');
            }

            console.log('Photo Mode activated');

            // Track event
            if (window.analytics) {
                window.analytics.track('photo_mode_entered', {
                    timestamp: new Date().toISOString()
                });
            }

        } catch (error) {
            console.error('Failed to access camera:', error);
            this._showError('Não foi possível acessar a câmera. Verifique as permissões.');
        }
    }

    /**
     * Capture photo from stream
     */
    capturePhoto() {
        if (!this.cameraStream || !this.cameraStream.videoWidth) {
            console.error('No video stream available');
            return;
        }

        // Create canvas to capture frame
        const canvas = document.createElement('canvas');
        canvas.width = this.cameraStream.videoWidth;
        canvas.height = this.cameraStream.videoHeight;

        const context = canvas.getContext('2d');
        context.drawImage(this.cameraStream, 0, 0, canvas.width, canvas.height);

        // Convert to data URL
        const photoDataUrl = canvas.toDataURL('image/jpeg', 0.9);

        // Set as background
        if (this.photoBackground) {
            this.photoBackground.style.backgroundImage = `url(${photoDataUrl})`;
        }

        // Exit photo mode UI but stay in photo state
        this._hidePhotoModeUI();

        console.log('Photo captured');

        // Track event
        if (window.analytics) {
            window.analytics.track('photo_captured', {
                timestamp: new Date().toISOString()
            });
        }
    }

    /**
     * Exit Photo Mode
     */
    exitPhotoMode() {
        // Stop camera stream
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }

        // Clear video source
        if (this.cameraStream) {
            this.cameraStream.srcObject = null;
        }

        // Hide Photo Mode UI
        this._hidePhotoModeUI();

        // Clear background if transitioning to ready
        if (window.stateMachine && window.stateMachine.getState() === 'photo') {
            if (this.photoBackground && !this.photoBackground.style.backgroundImage) {
                // No photo was captured, go back to ready
                window.stateMachine.transition('ready');
            }
            // If photo exists, stay in photo state but hide UI
        }

        console.log('Photo Mode exited');
    }

    /**
     * Clear photo background and return to normal
     */
    clearPhoto() {
        if (this.photoBackground) {
            this.photoBackground.style.backgroundImage = '';
        }

        if (window.stateMachine && window.stateMachine.getState() === 'photo') {
            window.stateMachine.transition('ready');
        }
    }

    /**
     * Show Photo Mode card
     */
    _showPhotoModeCard() {
        const photoModeCard = document.getElementById('photoModeCard');
        if (photoModeCard) {
            photoModeCard.style.display = 'block';
        }
    }

    /**
     * Hide Photo Mode card
     */
    _hidePhotoModeCard() {
        const photoModeCard = document.getElementById('photoModeCard');
        if (photoModeCard) {
            photoModeCard.style.display = 'none';
        }
    }

    /**
     * Hide Photo Mode UI
     */
    _hidePhotoModeUI() {
        const photoModeUI = document.getElementById('photoModeUI');
        if (photoModeUI) {
            photoModeUI.style.display = 'none';
        }
    }

    /**
     * Show error message
     */
    _showError(message) {
        console.error(message);
        alert(message); // Replace with better UI
    }

    /**
     * Check if currently in photo mode
     */
    isActive() {
        return this.stream !== null;
    }
}

// Export for use in app.js
window.PhotoMode = PhotoMode;
