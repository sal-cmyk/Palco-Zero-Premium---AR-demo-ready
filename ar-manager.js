/**
 * PALCO ZERO - AR MANAGER
 * Handles AR functionality with cross-platform support
 * Features: USDZ validation, AR tracking, iOS/Android support
 */

class ARManager {
    constructor(config = {}) {
        this.config = {
            glbPath: config.glbPath || '',
            usdzPath: config.usdzPath || '',
            productName: config.productName || 'Product',
            autoRotate: config.autoRotate !== false,
            ...config
        };

        this.modelViewer = null;
        this.arButton = null;
        this.arStatus = null;
        this.isARSupported = false;
        this.isUsdzValid = false;
        
        this._init();
    }

    /**
     * Initialize AR Manager
     */
    async _init() {
        this.modelViewer = document.getElementById('modelViewer');
        this.arButton = document.getElementById('arButton');
        this.arStatus = document.getElementById('arStatus');

        if (!this.modelViewer) {
            console.error('model-viewer element not found');
            return;
        }

        // Set up model viewer
        this._setupModelViewer();

        // Validate USDZ for AR
        if (this.config.usdzPath) {
            this.isUsdzValid = await this._validateUSDZ(this.config.usdzPath);
        }

        // Check AR support
        this._checkARSupport();

        // Set up event listeners
        this._setupEventListeners();
    }

    /**
     * Configure model-viewer element
     */
    _setupModelViewer() {
        // Set GLB source
        if (this.config.glbPath) {
            this.modelViewer.setAttribute('src', this.config.glbPath);
        }

        // Set USDZ for iOS AR
        if (this.config.usdzPath) {
            this.modelViewer.setAttribute('ios-src', this.config.usdzPath);
        }

        // Set alt text
        this.modelViewer.setAttribute('alt', this.config.productName);

        // Auto-rotate configuration
        if (this.config.autoRotate) {
            this.modelViewer.setAttribute('auto-rotate', '');
            this.modelViewer.setAttribute('auto-rotate-delay', '3000');
        }
    }

    /**
     * Validate USDZ file exists and is accessible
     * @param {string} usdzPath - Path to USDZ file
     * @returns {Promise<boolean>}
     */
    async _validateUSDZ(usdzPath) {
        try {
            const response = await fetch(usdzPath, { 
                method: 'HEAD',
                cache: 'no-cache'
            });
            
            const isValid = response.ok && response.status === 200;
            
            if (isValid) {
                console.log('✓ USDZ file validated:', usdzPath);
            } else {
                console.warn('✗ USDZ validation failed:', response.status);
            }
            
            return isValid;
        } catch (error) {
            console.error('USDZ validation error:', error);
            return false;
        }
    }

    /**
     * Check if AR is supported on this device
     */
    _checkARSupport() {
        // iOS Quick Look support
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
        
        // Android Scene Viewer support
        const isAndroid = /Android/.test(navigator.userAgent);
        
        this.isARSupported = (isIOS || isAndroid) && this.isUsdzValid;

        if (this.isARSupported) {
            console.log('✓ AR supported on this device');
        } else {
            console.log('✗ AR not supported or USDZ invalid');
        }
    }

    /**
     * Set up event listeners for model viewer
     */
    _setupEventListeners() {
        // Model loaded - show AR button
        this.modelViewer.addEventListener('load', () => {
            console.log('✓ 3D model loaded');
            this._onModelLoaded();
        });

        // Loading progress
        this.modelViewer.addEventListener('progress', (event) => {
            const percent = event.detail.totalProgress * 100;
            this._onLoadingProgress(percent);
        });

        // AR status tracking
        this.modelViewer.addEventListener('ar-status', (event) => {
            this._onARStatusChange(event.detail.status);
        });

        // AR button click
        if (this.arButton) {
            this.arButton.addEventListener('click', () => {
                this._trackARClick();
            });
        }

        // Model error handling
        this.modelViewer.addEventListener('error', (error) => {
            console.error('Model viewer error:', error);
            this._onModelError(error);
        });
    }

    /**
     * Handle model loaded event
     */
    _onModelLoaded() {
        // Transition to ready state
        if (window.stateMachine) {
            window.stateMachine.transition('ready');
        }

        // Show AR button if supported
        if (this.isARSupported && this.arButton) {
            setTimeout(() => {
                this.arButton.classList.add('ready');
                this.arButton.style.display = 'flex';
                
                // Show AR instructions
                const instructions = document.getElementById('arInstructions');
                if (instructions) {
                    instructions.style.display = 'block';
                }
            }, 300);
        }
    }

    /**
     * Handle loading progress
     */
    _onLoadingProgress(percent) {
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = `${percent}%`;
        }

        // Log every 25%
        if (percent % 25 === 0) {
            console.log(`Loading: ${Math.round(percent)}%`);
        }
    }

    /**
     * Handle AR status changes
     * @param {string} status - AR session status
     */
    _onARStatusChange(status) {
        console.log('AR Status:', status);

        // Track with analytics if available
        if (window.analytics) {
            window.analytics.track('ar_status', {
                status: status,
                product: this.config.productName,
                timestamp: new Date().toISOString()
            });
        }

        // Update UI based on status
        switch (status) {
            case 'session-started':
                this._showARStatus('Sessão AR iniciada');
                if (window.stateMachine) {
                    window.stateMachine.transition('ar');
                }
                break;
            
            case 'object-placed':
                this._showARStatus('Objeto posicionado');
                break;
            
            case 'failed':
                this._showARStatus('Erro ao iniciar AR', true);
                setTimeout(() => this._hideARStatus(), 3000);
                break;
            
            case 'not-presenting':
                this._hideARStatus();
                if (window.stateMachine && window.stateMachine.getState() === 'ar') {
                    window.stateMachine.transition('ready');
                }
                break;
        }
    }

    /**
     * Track AR button click
     */
    _trackARClick() {
        console.log('AR button clicked');
        
        if (window.analytics) {
            window.analytics.track('ar_click', {
                product: this.config.productName,
                device: this._getDeviceType(),
                timestamp: new Date().toISOString()
            });
        }
    }

    /**
     * Handle model error
     */
    _onModelError(error) {
        console.error('Model error:', error);
        
        // Reset to idle state
        if (window.stateMachine) {
            window.stateMachine.transition('idle');
        }

        // Show error message to user
        this._showError('Erro ao carregar modelo 3D. Tente novamente.');
    }

    /**
     * Show AR status indicator
     */
    _showARStatus(text, isError = false) {
        if (!this.arStatus) return;

        this.arStatus.querySelector('.status-text').textContent = text;
        this.arStatus.style.display = 'flex';

        const indicator = this.arStatus.querySelector('.status-indicator');
        if (isError) {
            indicator.style.background = '#ff3b30';
        } else {
            indicator.style.background = '#30d158';
        }
    }

    /**
     * Hide AR status indicator
     */
    _hideARStatus() {
        if (!this.arStatus) return;
        this.arStatus.style.display = 'none';
    }

    /**
     * Show error message
     */
    _showError(message) {
        // You can implement custom error UI here
        console.error(message);
        alert(message); // Replace with better UI
    }

    /**
     * Get device type for analytics
     */
    _getDeviceType() {
        const ua = navigator.userAgent;
        if (/iPad|iPhone|iPod/.test(ua)) return 'iOS';
        if (/Android/.test(ua)) return 'Android';
        return 'Desktop';
    }

    /**
     * Update model sources
     */
    updateModel(glbPath, usdzPath) {
        this.config.glbPath = glbPath;
        this.config.usdzPath = usdzPath;

        if (this.modelViewer) {
            this.modelViewer.setAttribute('src', glbPath);
            if (usdzPath) {
                this.modelViewer.setAttribute('ios-src', usdzPath);
            }
        }

        // Revalidate USDZ
        if (usdzPath) {
            this._validateUSDZ(usdzPath).then(isValid => {
                this.isUsdzValid = isValid;
                this._checkARSupport();
            });
        }
    }

    /**
     * Reset AR state
     */
    reset() {
        if (this.modelViewer) {
            // Reset camera
            this.modelViewer.resetTurntableRotation();
            this.modelViewer.cameraOrbit = this.modelViewer.getAttribute('camera-orbit');
        }

        this._hideARStatus();

        if (window.stateMachine && window.stateMachine.getState() === 'ar') {
            window.stateMachine.transition('ready');
        }
    }
}

// Export for use in app.js
window.ARManager = ARManager;
