#!/usr/bin/env python3

"""
GRACE Voice Agent Web API

This script provides a simple API interface for the GRACE Voice Agent website.
It allows the website to request the application to launch.
"""

import os
import inspect
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import app_launcher

# Create Flask app
app = Flask(__name__, static_folder='website')
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/api/launch', methods=['GET', 'POST'])
def launch():
    """API endpoint to launch the GRACE Voice Agent."""
    print(f"Received request to launch Voice Agent: {request.method}")
    # Launch the application
    success = app_launcher.launch_app()
    print(f"Launch success: {success}")
    
    # Return success/failure as JSON
    return jsonify({
        'success': success,
        'message': 'GRACE Voice Agent launched successfully!' if success else 'Failed to launch GRACE Voice Agent.'
    })

@app.route('/api/launch-gesture', methods=['GET', 'POST'])
def launch_gesture():
    """API endpoint to launch the Hand Gesture module."""
    print(f"Received request to launch Hand Gesture: {request.method}")
    # Print available functions in app_launcher for debugging
    print(f"Available functions in app_launcher: {[f for f in dir(app_launcher) if not f.startswith('_') and callable(getattr(app_launcher, f))]}")
    
    try:
        # Launch the hand gesture module
        success = app_launcher.launch_hand_gesture()
        print(f"Launch gesture success: {success}")
        
        # Return success/failure as JSON
        return jsonify({
            'success': success,
            'message': 'Hand Gesture module launched successfully!' if success else 'Failed to launch Hand Gesture module.'
        })
    except Exception as e:
        print(f"Error in launch_gesture: {e}")
        return jsonify({
            'success': False,
            'message': f'Error launching Hand Gesture module: {str(e)}'
        }), 500

@app.route('/test')
def test_page():
    """Serve the test API page."""
    return send_file('test_api.html')

@app.route('/')
def index():
    """Serve the website index page."""
    return send_from_directory('website', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files from the website directory."""
    return send_from_directory('website', path)

if __name__ == '__main__':
    # Get the port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    print(f"Starting GRACE Voice Agent Web API on port {port}...")
    print(f"Open http://localhost:{port} in your browser to access the website.")
    print(f"Open http://localhost:{port}/test in your browser to test the API.")
    app.run(host='0.0.0.0', port=port, debug=True) 