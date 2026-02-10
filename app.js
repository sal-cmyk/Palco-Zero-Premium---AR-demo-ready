/**
 * PALCO ZERO - MAIN APPLICATION
 * Orchestrates all components and initializes the experience
 */

(function() {
    'use strict';

    // Configuration
    // SKU Configuration
    const PRODUCTS = {
        'can': {
            name: 'NEON FLOW',
            subtitle: 'Bebida Energética Premium',
            description: 'Refrescância. Identidade. Canal vivo.',
            glbPath: './models/can.glb',
            usdzPath: './models/can.usdz',
            posterPath: './models/can-poster.webp'
        },
        'cookie-pack': {
            name: 'Biscoito Premium',
            subtitle: 'Crocância. Sabor. Experiência viva.',
            description: 'Ingredientes em destaque. Benefícios claros. Conteúdo e receitas.',
            glbPath: './models/cookie-pack.glb',
            usdzPath: './models/cookie-pack.usdz',
            posterPath: './models/cookie-pack-poster.webp'
        }
    };

    // Get SKU from URL or default to 'can'
    const urlParams = new URLSearchParams(window.location.search);
    const currentSKU = urlParams.get('sku') || 'can';
    const currentProduct = PRODUCTS[currentSKU] || PRODUCTS['can'];

    const APP_CONFIG = {
        product: currentProduct,
        analytics: {
            enabled: false, // Set to true when implementing analytics
            debugMode: true
        }
    };

    // Global instances
    let arManager = null;
    let photoMode = null;

    /**
     * Initialize application
     */
    function init() {
        console.log('%c🚀 Palco Zero Initialized', 'color: #0071e3; font-size: 16px; font-weight: bold;');
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', startApp);
        } else {
            startApp();
        }
    }

    /**
     * Start application
     */
    async function startApp() {
        // Transition to loading state
        window.stateMachine.transition('loading');

        // Populate product info
        populateProductInfo();

        // Initialize AR Manager
        initARManager();

        // Initialize Photo Mode (optional feature)
        initPhotoMode();

        // Set up global listeners
        setupGlobalListeners();

        // Initialize analytics if enabled
        if (APP_CONFIG.analytics.enabled) {
            initAnalytics();
        }

        console.log('✓ App started successfully');
    }

    /**
     * Populate product information in UI
     */
    function populateProductInfo() {
        const { name, subtitle, description } = APP_CONFIG.product;

        const titleEl = document.getElementById('productTitle');
        const subtitleEl = document.getElementById('productSubtitle');
        const descriptionEl = document.getElementById('productDescription');

        if (titleEl) titleEl.textContent = name;
        if (subtitleEl) subtitleEl.textContent = subtitle;
        if (descriptionEl) descriptionEl.textContent = description;
    }

    /**
     * Initialize AR Manager
     */
    function initARManager() {
        arManager = new window.ARManager({
            glbPath: APP_CONFIG.product.glbPath,
            usdzPath: APP_CONFIG.product.usdzPath,
            productName: APP_CONFIG.product.name,
            autoRotate: true
        });

        console.log('✓ AR Manager initialized');
    }

    /**
     * Initialize Photo Mode
     */
    function initPhotoMode() {
        photoMode = new window.PhotoMode();
        console.log('✓ Photo Mode initialized');
    }

    /**
     * Set up global event listeners
     */
    function setupGlobalListeners() {
        // Listen for state changes
        window.stateMachine.subscribe((oldState, newState) => {
            onStateChange(oldState, newState);
        });

        // Handle visibility change (pause/resume)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                onAppPause();
            } else {
                onAppResume();
            }
        });

        // Handle orientation change
        window.addEventListener('orientationchange', () => {
            onOrientationChange();
        });

        // Handle online/offline
        window.addEventListener('online', () => {
            console.log('✓ Connection restored');
        });

        window.addEventListener('offline', () => {
            console.warn('✗ Connection lost');
        });
    }

    /**
     * Handle state changes
     */
    function onStateChange(oldState, newState) {
        console.log(`State: ${oldState} → ${newState}`);

        // Track state changes
        if (APP_CONFIG.analytics.enabled && window.analytics) {
            window.analytics.track('state_change', {
                from: oldState,
                to: newState,
                timestamp: new Date().toISOString()
            });
        }

        // Handle specific state transitions
        switch (newState) {
            case 'ready':
                onReadyState();
                break;
            case 'ar':
                onARState();
                break;
            case 'photo':
                onPhotoState();
                break;
        }
    }

    /**
     * Handle ready state
     */
    function onReadyState() {
        console.log('✓ Experience ready');
    }

    /**
     * Handle AR state
     */
    function onARState() {
        console.log('✓ AR session active');
    }

    /**
     * Handle photo state
     */
    function onPhotoState() {
        console.log('✓ Photo mode active');
    }

    /**
     * Handle app pause (tab hidden)
     */
    function onAppPause() {
        console.log('App paused');
        
        // Pause animations or reduce activity
        const modelViewer = document.getElementById('modelViewer');
        if (modelViewer) {
            modelViewer.pause();
        }
    }

    /**
     * Handle app resume (tab visible)
     */
    function onAppResume() {
        console.log('App resumed');
        
        // Resume animations
        const modelViewer = document.getElementById('modelViewer');
        if (modelViewer) {
            modelViewer.play();
        }
    }

    /**
     * Handle orientation change
     */
    function onOrientationChange() {
        console.log('Orientation changed:', window.orientation);
        
        // You can adjust UI based on orientation here
        // For example, show/hide certain elements
    }

    /**
     * Initialize analytics (placeholder)
     */
    function initAnalytics() {
        // Implement your analytics here
        // Example: Google Analytics, Mixpanel, etc.
        
        window.analytics = {
            track: (event, properties = {}) => {
                if (APP_CONFIG.analytics.debugMode) {
                    console.log(`[Analytics] ${event}`, properties);
                }
                // Send to your analytics service
            },
            page: (name, properties = {}) => {
                if (APP_CONFIG.analytics.debugMode) {
                    console.log(`[Analytics] Page: ${name}`, properties);
                }
                // Track page view
            }
        };

        // Track initial page load
        window.analytics.page('Palco Zero', {
            product: APP_CONFIG.product.name,
            timestamp: new Date().toISOString()
        });

        console.log('✓ Analytics initialized');
    }

    /**
     * Update product dynamically
     * @param {Object} productData - New product data
     */
    function updateProduct(productData) {
        // Update config
        Object.assign(APP_CONFIG.product, productData);

        // Update UI
        populateProductInfo();

        // Update AR Manager
        if (arManager && productData.glbPath && productData.usdzPath) {
            arManager.updateModel(productData.glbPath, productData.usdzPath);
        }

        console.log('✓ Product updated');
    }

    /**
     * Error handler
     */
    function handleError(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        // Track errors
        if (APP_CONFIG.analytics.enabled && window.analytics) {
            window.analytics.track('error', {
                context,
                error: error.message,
                stack: error.stack,
                timestamp: new Date().toISOString()
            });
        }

        // Show user-friendly error
        // showErrorToast(error.message);
    }

    /**
     * Global error handlers
     */
    window.addEventListener('error', (event) => {
        handleError(event.error, 'global');
    });

    window.addEventListener('unhandledrejection', (event) => {
        handleError(event.reason, 'promise');
    });

    // Expose public API
    window.PalcoZero = {
        updateProduct,
        getState: () => window.stateMachine.getState(),
        resetAR: () => arManager?.reset(),
        clearPhoto: () => photoMode?.clearPhoto(),
        config: APP_CONFIG
    };

    // Initialize app
    init();

})();
