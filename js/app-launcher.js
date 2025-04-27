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
    launchGestureEndpoint: '/api/launch-gesture',
    stopEndpoint: '/api/stop'
};

// Class to handle application launching
class GraceAppLauncher {
    constructor(config = API_CONFIG) {
        this.config = config;
        this.isRunning = false;
        console.log('GraceAppLauncher initialized with config:', this.config);
        this.initEventListeners();
        
        // Check if we're running on GitHub Pages
        this.isGitHubPages = window.location.hostname.includes('github.io') || 
                            window.location.hostname !== 'localhost';
        console.log('Running on GitHub Pages:', this.isGitHubPages);
        
        // Create stop button
        this.createStopButton();
    }
    
    /**
     * Initialize event listeners for launch buttons
     */
    initEventListeners() {
        console.log('Initializing event listeners for launch buttons');
        
        // Find launch button
        const launchButton = document.getElementById('launch-app');
        if (launchButton) {
            console.log('Launch app button found, adding listener');
            launchButton.addEventListener('click', this.handleRunClick.bind(this));
        } else {
            console.warn('Launch app button not found');
        }
        
        // Find gesture button
        const gestureButton = document.getElementById('launch-gesture');
        if (gestureButton) {
            console.log('Launch gesture button found, adding listener');
            gestureButton.addEventListener('click', this.handleRunGestureClick.bind(this));
        } else {
            console.warn('Launch gesture button not found');
        }
        
        // Find existing stop button (in case it's already in the HTML)
        const stopButton = document.getElementById('stop-grace');
        if (stopButton) {
            console.log('Stop button found in DOM, adding listener');
            stopButton.addEventListener('click', this.handleStopClick.bind(this));
        } else {
            console.log('Stop button not found in DOM, will create it');
            // It will be created by createStopButton method
        }
        
        // Find download button
        const downloadButton = document.getElementById('download-app');
        if (downloadButton) {
            console.log('Download button found, adding listener');
            // No special handling for download button as it's just a link
        }
    }
    
    /**
     * Create stop button
     */
    createStopButton() {
        // Check if stop button already exists
        if (document.getElementById('stop-grace')) {
            return;
        }
        
        // Find container for the stop button
        const stopButtonContainer = document.querySelector('.stop-buttons');
        
        // If container doesn't exist, try to find run-buttons to add after it
        if (!stopButtonContainer) {
            const runButtons = document.querySelector('.run-buttons');
            if (runButtons) {
                // Create container if it doesn't exist
                const container = document.createElement('div');
                container.className = 'stop-buttons';
                container.style.marginTop = '10px';
                container.style.width = '100%';
                
                // Insert after run-buttons
                runButtons.parentNode.insertBefore(container, runButtons.nextSibling);
                
                // Create stop button
                const stopButton = document.createElement('a');
                stopButton.id = 'stop-grace';
                stopButton.className = 'btn primary-btn stop-btn';
                stopButton.href = '#';
                stopButton.innerHTML = '<i class="fas fa-stop"></i> Stop Running Programs';
                stopButton.style.backgroundColor = '#e53e3e';
                stopButton.style.display = 'none';
                stopButton.style.width = '100%';
                stopButton.style.textAlign = 'center';
                stopButton.style.fontWeight = 'bold';
                
                // Add button to container
                container.appendChild(stopButton);
                
                // Add event listener
                stopButton.addEventListener('click', this.handleStopClick.bind(this));
            }
        } else {
            // Container exists, just add the button
            const stopButton = document.createElement('a');
            stopButton.id = 'stop-grace';
            stopButton.className = 'btn primary-btn stop-btn';
            stopButton.href = '#';
            stopButton.innerHTML = '<i class="fas fa-stop"></i> Stop Running Programs';
            stopButton.style.backgroundColor = '#e53e3e';
            stopButton.style.display = 'none';
            
            // Add button to container
            stopButtonContainer.appendChild(stopButton);
            
            // Add event listener
            stopButton.addEventListener('click', this.handleStopClick.bind(this));
        }
    }
    
    /**
     * Handle stop button click
     * @param {Event} event - The click event
     */
    async handleStopClick(event) {
        event.preventDefault();
        
        // Show loading state with a more explicit message
        const button = event.currentTarget;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Stopping...';
        button.disabled = true;
        button.style.backgroundColor = '#999';
        
        // Show a message indicating we're stopping processes
        this.showLaunchMessage(true, 'Stopping all GRACE processes... Please wait.');
        
        try {
            console.log('Attempting to stop all GRACE processes...');
            // Call stop API
            const response = await fetch(`${this.config.baseUrl}${this.config.stopEndpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Stop API response:', data);
            
            if (data.success) {
                this.showLaunchMessage(true, data.message || 'Successfully stopped all running GRACE programs');
                this.toggleStopButton(false);
            } else {
                this.showLaunchMessage(false, data.message || 'Could not stop GRACE programs. Try manually closing them.');
            }
        } catch (error) {
            console.error('Error stopping processes:', error);
            this.showLaunchMessage(false, 'Error stopping GRACE programs. Try manually closing them.');
        } finally {
            // Reset button state
            button.innerHTML = '<i class="fas fa-stop"></i> Stop Running Programs';
            button.disabled = false;
            button.style.backgroundColor = '#e53e3e';
        }
    }
    
    /**
     * Set button loading state
     * @param {HTMLElement} button - The button element
     * @param {boolean} isLoading - Whether the button is loading
     */
    setButtonLoadingState(button, isLoading) {
        if (!button) return;
        
        const originalText = button.getAttribute('data-original-text') || button.textContent;
        
        if (isLoading) {
            // Save original text if not already saved
            if (!button.getAttribute('data-original-text')) {
                button.setAttribute('data-original-text', button.textContent);
            }
            
            // Update button text and disable it
            button.textContent = 'Processing...';
            button.disabled = true;
            button.classList.add('loading');
        } else {
            // Restore original text and enable button
            button.textContent = originalText;
            button.disabled = false;
            button.classList.remove('loading');
        }
    }
    
    /**
     * Toggle stop button visibility
     * @param {boolean} show - Whether to show the stop button
     */
    toggleStopButton(show) {
        const stopButton = document.getElementById('stop-grace');
        if (stopButton) {
            if (show) {
                // Make the button visible
                stopButton.style.display = 'block';
                
                // Add a pulse animation to draw attention to the button
                stopButton.classList.add('pulse-animation');
                
                // Remove the animation after a few seconds
                setTimeout(() => {
                    stopButton.classList.remove('pulse-animation');
                }, 3000);
                
                // Also scroll to make sure the button is visible
                const stopButtonRect = stopButton.getBoundingClientRect();
                if (stopButtonRect.bottom > window.innerHeight) {
                    stopButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                // Hide the button
                stopButton.style.display = 'none';
            }
            this.isRunning = show;
        }
    }
    
    /**
     * Handle run button click
     * @param {Event} event - The click event
     */
    async handleRunClick(event) {
        // Prevent default navigation
        event.preventDefault();
        
        // Show loading state
        this.setButtonLoadingState(event.currentTarget, true);
        
        // If we're on GitHub Pages, show a special message and return early
        if (this.isGitHubPages) {
            this.showGitHubPagesMessage();
            this.setButtonLoadingState(event.currentTarget, false);
            return;
        }
        
        try {
            // Try to launch the app via our API
            const launched = await this.launchApp();
            
            if (launched) {
                // App successfully launched - show success message
                this.showLaunchMessage(true, 'GRACE Voice Agent launched successfully!');
                // Show stop button
                this.toggleStopButton(true);
            } else {
                // If API call failed, show error message
                this.showLaunchMessage(false, 'Could not launch GRACE Voice Agent. Please make sure the API server is running.');
            }
        } catch (error) {
            // In case of error
            console.error('Error launching app:', error);
            this.showLaunchMessage(false, 'Error launching GRACE Voice Agent. Please try downloading instead.');
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
        
        // If we're on GitHub Pages, show a special message and return early
        if (this.isGitHubPages) {
            this.showGitHubPagesMessage();
            this.setButtonLoadingState(event.currentTarget, false);
            return;
        }
        
        try {
            // Try to launch the hand gesture module via our API
            const launched = await this.launchGesture();
            
            if (launched) {
                // Gesture module successfully launched - show success message
                this.showLaunchMessage(true, 'Hand Gesture module launched successfully!');
                // Show stop button
                this.toggleStopButton(true);
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
     * Show launch message to the user
     * @param {boolean} success - Whether the launch was successful
     * @param {string} message - The message to show
     */
    showLaunchMessage(success, message) {
        const messageContainer = document.getElementById('launch-message');
        if (!messageContainer) {
            console.warn('Launch message container not found');
            alert(message); // Fallback to alert
            return;
        }
        
        // Update message container
        messageContainer.innerHTML = message;
        messageContainer.classList.remove('success', 'error');
        messageContainer.classList.add(success ? 'success' : 'error');
        messageContainer.style.display = 'block';
        
        // Auto-hide after 8 seconds
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 8000);
    }
    
    /**
     * Show GitHub Pages specific message
     */
    showGitHubPagesMessage() {
        this.showLaunchMessage(false, 
            'This feature requires the desktop application. Please download the app from the GitHub repository.');
    }
    
    /**
     * Launch the app via API
     * @returns {Promise<boolean>} True if launch was successful
     */
    async launchApp() {
        try {
            console.log('Attempting to launch app...');
            const url = `${this.config.baseUrl}${this.config.launchEndpoint}`;
            console.log('Requesting URL:', url);
            
            // Call the launch API endpoint
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
            console.error('Error calling launch API:', error);
            console.error('Full error details:', error.message, error.stack);
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
     * Stop all running GRACE processes via API
     * @returns {Promise<boolean>} True if stop was successful
     */
    async stopProcesses() {
        try {
            console.log('Attempting to stop GRACE processes...');
            const url = `${this.config.baseUrl}${this.config.stopEndpoint}`;
            console.log('Requesting URL:', url);
            
            // Call the stop API endpoint
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
            console.error('Error calling stop API:', error);
            console.error('Full error details:', error.message, error.stack);
            return false;
        }
    }
}

// Initialize the app launcher when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing GraceAppLauncher');
    window.graceAppLauncher = new GraceAppLauncher();
}); 