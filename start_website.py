#!/usr/bin/env python3

"""
GRACE Voice Agent Website Launcher

This script starts the web server that hosts the GRACE Voice Agent website
and API for launching the application.
"""

import os
import sys
import webbrowser
import time
import threading
import subprocess

def open_browser():
    """Open the default web browser to the website after a short delay."""
    time.sleep(2)  # Give the server a moment to start
    url = "http://localhost:5000"
    print(f"Opening {url} in your default browser...")
    webbrowser.open(url)

def main():
    """Start the web server and open the browser."""
    print("Starting GRACE Voice Agent Website...")
    
    # Check if Flask and Flask-CORS are installed
    try:
        import flask
        import flask_cors
    except ImportError:
        print("Required packages not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.3", "Flask-CORS==4.0.0"])
    
    # Start the browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Import and run the Flask application
    try:
        import app_api
        app_api.app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"Error starting the website: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 