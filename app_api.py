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
app = Flask(__name__, static_folder='.')
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
    return send_file('index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files from the root directory."""
    if os.path.exists(path):
        return send_file(path)
    else:
        return "File not found", 404

@app.route('/api/stop', methods=['POST'])
def stop_processes():
    """API endpoint to stop all running GRACE processes."""
    print("Received request to stop all GRACE processes")
    
    try:
        # Try to kill python processes running main.py or Hand_Gesture.py
        import subprocess
        import platform
        
        success = False
        message = "No processes to stop"
        
        if platform.system() == 'Windows':
            success_messages = []
            
            # Try multiple approaches for maximum effectiveness
            
            # 1. Stop the Hand Gesture module - look for pythonw.exe processes running Hand_Gesture.py
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/FI', 'IMAGENAME eq pythonw.exe', '/FI', 'COMMANDLINE eq *Hand_Gesture.py*'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0 and b"SUCCESS" in result.stdout:
                    success = True
                    success_messages.append("Stopped Hand Gesture process")
                    print("Successfully terminated Hand Gesture process")
            except Exception as e:
                print(f"Error trying to kill Hand Gesture process: {e}")
                
            # 2. Stop the Voice Agent - look for python.exe processes running main.py
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/FI', 'IMAGENAME eq python.exe', '/FI', 'COMMANDLINE eq *main.py*'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0 and b"SUCCESS" in result.stdout:
                    success = True
                    success_messages.append("Stopped Voice Agent process")
                    print("Successfully terminated Voice Agent process")
            except Exception as e:
                print(f"Error trying to kill Voice Agent process: {e}")
                
            # 3. Fallback - try by window title if specific process filtering fails
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/FI', 'WINDOWTITLE eq GRACE Voice Agent*'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0 and b"SUCCESS" in result.stdout:
                    success = True
                    success_messages.append("Stopped GRACE Voice Agent process by window title")
                    print("Successfully terminated GRACE Voice Agent process by window title")
            except Exception as e:
                print(f"Error trying to kill by window title: {e}")
                
            # 4. More aggressive approach - try to kill any command window running Python with GRACE-related commands
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/FI', 'WINDOWTITLE eq *Python*', '/FI', 'COMMANDLINE eq *GRACE*'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0 and b"SUCCESS" in result.stdout:
                    success = True
                    success_messages.append("Stopped additional GRACE processes")
                    print("Successfully terminated additional GRACE processes")
            except Exception as e:
                print(f"Error trying additional kill method: {e}")
                
            # 5. Very aggressive fallback - just kill any cmd window with "python" in the title
            # (this is a last resort and might affect other Python processes)
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/FI', 'WINDOWTITLE eq *python*'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0 and b"SUCCESS" in result.stdout:
                    success = True
                    success_messages.append("Stopped Python command windows")
                    print("Successfully terminated Python command windows")
            except Exception as e:
                print(f"Error trying to kill Python command windows: {e}")
            
            # Generate a combined message
            if success_messages:
                message = "Successfully stopped: " + ", ".join(success_messages)
            else:
                # If nothing worked but we didn't get errors, we probably had no processes to stop
                message = "No running GRACE processes found to stop"
                
        else:
            # Linux/Mac - more targeted approach
            success_messages = []
            
            try:
                # Stop Hand Gesture process
                hand_gesture_result = subprocess.run(
                    ['pkill', '-f', 'Hand_Gesture.py'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Stop Voice Agent process
                voice_agent_result = subprocess.run(
                    ['pkill', '-f', 'main.py'], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if hand_gesture_result.returncode == 0:
                    success = True
                    success_messages.append("Hand Gesture module")
                    
                if voice_agent_result.returncode == 0:
                    success = True
                    success_messages.append("Voice Agent")
                
                if success_messages:
                    message = "Successfully stopped: " + ", ".join(success_messages)
                else:
                    # If nothing worked but we didn't get errors, we probably had no processes to stop
                    message = "No running GRACE processes found to stop"
            except Exception as e:
                print(f"Error stopping processes: {e}")
                message = f"Error stopping processes: {str(e)}"
                
        # Return success/failure as JSON
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        print(f"Error in stop_processes: {e}")
        return jsonify({
            'success': False,
            'message': f'Error stopping processes: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Get the port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    print(f"Starting GRACE Voice Agent Web API on port {port}...")
    print(f"Open http://localhost:{port} in your browser to access the website.")
    print(f"Open http://localhost:{port}/test in your browser to test the API.")
    app.run(host='0.0.0.0', port=port, debug=True) 