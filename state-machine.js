/**
 * PALCO ZERO - STATE MACHINE
 * Simple state management for AR experience
 * States: idle → loading → ready → ar → photo
 */

class StateMachine {
    constructor(initialState = 'idle') {
        this.state = initialState;
        this.listeners = [];
        this.transitions = {
            idle: ['loading'],
            loading: ['ready', 'idle'],
            ready: ['ar', 'photo', 'loading'],
            ar: ['ready'],
            photo: ['ready']
        };
    }

    /**
     * Get current state
     */
    getState() {
        return this.state;
    }

    /**
     * Transition to new state
     * @param {string} newState - Target state
     * @returns {boolean} - Success status
     */
    transition(newState) {
        const allowedTransitions = this.transitions[this.state];
        
        if (!allowedTransitions || !allowedTransitions.includes(newState)) {
            console.warn(`Invalid transition from ${this.state} to ${newState}`);
            return false;
        }

        const oldState = this.state;
        this.state = newState;
        
        // Update DOM
        this._updateDOM();
        
        // Notify listeners
        this._notifyListeners(oldState, newState);
        
        console.log(`State transition: ${oldState} → ${newState}`);
        return true;
    }

    /**
     * Subscribe to state changes
     * @param {Function} callback - Called with (oldState, newState)
     */
    subscribe(callback) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(cb => cb !== callback);
        };
    }

    /**
     * Update DOM data-state attribute
     */
    _updateDOM() {
        const appContainer = document.getElementById('app');
        if (appContainer) {
            appContainer.setAttribute('data-state', this.state);
        }
    }

    /**
     * Notify all listeners of state change
     */
    _notifyListeners(oldState, newState) {
        this.listeners.forEach(callback => {
            try {
                callback(oldState, newState);
            } catch (error) {
                console.error('Error in state listener:', error);
            }
        });
    }

    /**
     * Check if can transition to state
     */
    canTransition(newState) {
        const allowedTransitions = this.transitions[this.state];
        return allowedTransitions && allowedTransitions.includes(newState);
    }
}

// Create global instance
window.stateMachine = new StateMachine('idle');

// Log state changes in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.stateMachine.subscribe((oldState, newState) => {
        console.log(`%c[StateMachine] %c${oldState} → ${newState}`, 
            'color: #0071e3; font-weight: bold',
            'color: #30d158; font-weight: bold'
        );
    });
}
