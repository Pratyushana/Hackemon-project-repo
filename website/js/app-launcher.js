/**
 * GRACE Voice Agent - Application Launcher
 * 
 * This script provides functionality to launch the GRACE Voice Agent application
 * from the website interface.
 */

// Configuration for API connection
const API_CONFIG = {
    // Default to same host as website, with port 5000
    baseUrl: 'http://localhost:5000',
    launchEndpoint: '/api/launch',
    launchGestureEndpoint: '/api/launch-gesture'
};

// Class to handle application launching
class GraceAppLauncher {
    constructor(config = API_CONFIG) {
        this.config = config;
        console.log('GraceAppLauncher initialized with config:', this.config);
        this.initEventListeners();
    }

    /**
     * Initialize event listeners
     */
    initEventListeners() {
        // Find all download buttons
        const downloadButtons = document.querySelectorAll('.download-btn');
        
        // Add click event to all download buttons
        downloadButtons.forEach(button => {
            button.addEventListener('click', this.handleDownloadClick.bind(this));
        });
        
        // Find the run voice agent button
        const runAppButton = document.getElementById('run-app-btn');
        if (runAppButton) {
            runAppButton.addEventListener('click', this.handleRunAppClick.bind(this));
        }
        
        // Find the run hand gesture button
        const runGestureButton = document.getElementById('run-gesture-btn');
        if (runGestureButton) {
            runGestureButton.addEventListener('click', this.handleRunGestureClick.bind(this));
        }
    }

    /**
     * Handle download button click
     * @param {Event} event - The click event
     */
    async handleDownloadClick(event) {
        // For download button, we just let the default behavior happen
        // which will download the ZIP file
    }
    
    /**
     * Handle run app button click
     * @param {Event} event - The click event
     */
    async handleRunAppClick(event) {
        // Prevent default navigation
        event.preventDefault();
        
        // Show loading state
        this.setButtonLoadingState(event.currentTarget, true);
        
        try {
            // Try to launch the app via our API
            const launched = await this.launchApp();
            
            if (launched) {
                // App successfully launched - show success message
                this.showLaunchMessage(true, 'GRACE Voice Agent launched successfully!');
            } else {
                // If API call failed, show error message
                this.showLaunchMessage(false, 'Could not launch the application. Please make sure the API server is running.');
            }
        } catch (error) {
            // In case of error
            console.error('Error launching app:', error);
            this.showLaunchMessage(false, 'Error launching application. Please try downloading instead.');
        } finally {
            // Reset button state
            this.setButtonLoadingState(event.currentTarget, false);
        }
    }
    
    /**
     * Handle run gesture button click
     * @param {Event} event - The click event
     */
    async handleRunGestureClick(event) {
        // Prevent default navigation
        event.preventDefault();
        
        // Show loading state
        this.setButtonLoadingState(event.currentTarget, true);
        
        try {
            // Try to launch the hand gesture module via our API
            const launched = await this.launchGesture();
            
            if (launched) {
                // Gesture module successfully launched - show success message
                this.showLaunchMessage(true, 'Hand Gesture module launched successfully!');
            } else {
                // If API call failed, show error message
                this.showLaunchMessage(false, 'Could not launch the Hand Gesture module. Please make sure the API server is running.');
            }
        } catch (error) {
            // In case of error
            console.error('Error launching hand gesture module:', error);
            this.showLaunchMessage(false, 'Error launching Hand Gesture module. Please try downloading instead.');
        } finally {
            // Reset button state
            this.setButtonLoadingState(event.currentTarget, false);
        }
    }

    /**
     * Launch the application via API
     * @returns {Promise<boolean>} True if launch was successful
     */
    async launchApp() {
        try {
            // Call the launch API endpoint
            const response = await fetch(`${this.config.baseUrl}${this.config.launchEndpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data.success;
        } catch (error) {
            console.error('Error calling launch API:', error);
            return false;
        }
    }
    
    /**
     * Launch the hand gesture module via API
     * @returns {Promise<boolean>} True if launch was successful
     */
    async launchGesture() {
        try {
            console.log('Attempting to launch hand gesture module...');
            const url = `${this.config.baseUrl}${this.config.launchGestureEndpoint}`;
            console.log('Requesting URL:', url);
            
            // Call the launch gesture API endpoint
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                console.error('Response not OK:', response.status, response.statusText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Response data:', data);
            return data.success;
        } catch (error) {
            console.error('Error calling launch gesture API:', error);
            console.error('Full error details:', error.message, error.stack);
            return false;
        }
    }

    /**
     * Set button loading state
     * @param {HTMLElement} button - The button element
     * @param {boolean} isLoading - Whether the button is in loading state
     */
    setButtonLoadingState(button, isLoading) {
        if (isLoading) {
            // Store original text
            button.dataset.originalText = button.innerHTML;
            // Show loading spinner
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Launching...';
            button.classList.add('loading');
        } else {
            // Restore original text
            if (button.dataset.originalText) {
                button.innerHTML = button.dataset.originalText;
            }
            button.classList.remove('loading');
        }
    }

    /**
     * Show launch message
     * @param {boolean} success - Whether the launch was successful
     * @param {string} message - Message to display
     */
    showLaunchMessage(success, message) {
        // Create message element
        const messageEl = document.createElement('div');
        messageEl.className = success ? 'launch-message success' : 'launch-message error';
        messageEl.innerHTML = `
            <i class="fas fa-${success ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        
        // Add to document
        document.body.appendChild(messageEl);
        
        // Show message
        setTimeout(() => {
            messageEl.classList.add('show');
        }, 10);
        
        // Auto-hide after delay
        setTimeout(() => {
            messageEl.classList.remove('show');
            // Remove from DOM after fade out
            setTimeout(() => {
                document.body.removeChild(messageEl);
            }, 500);
        }, 5000);
    }
}

// Initialize the launcher when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create launcher instance
    window.graceAppLauncher = new GraceAppLauncher();
}); 