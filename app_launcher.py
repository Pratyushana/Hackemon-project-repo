#!/usr/bin/env python3

"""
GRACE Voice Agent Launcher

This script serves as a launcher for the GRACE Voice Agent application.
It can be used to start the application directly from the website.
"""

import os
import sys
import subprocess
import platform
import traceback

def launch_app():
    """Launch the GRACE Voice Agent application."""
    print("Launching GRACE Voice Agent...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to main.py
    main_script = os.path.join(script_dir, "main.py")
    
    # Check if main.py exists
    if not os.path.exists(main_script):
        print(f"Error: Could not find {main_script}")
        return False
    
    try:
        # Launch the application
        if platform.system() == 'Windows':
            # Use pythonw.exe on Windows to avoid showing a console window
            python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
            if not os.path.exists(python_exe):
                # Fall back to regular python if pythonw doesn't exist
                python_exe = sys.executable
                
            subprocess.Popen([python_exe, main_script], 
                             creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # Linux/Mac - launch in background
            subprocess.Popen([sys.executable, main_script], 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             start_new_session=True)
        
        print("GRACE Voice Agent launched successfully!")
        return True
    except Exception as e:
        print(f"Error launching GRACE Voice Agent: {e}")
        traceback.print_exc()
        return False

def launch_hand_gesture():
    """Launch only the Hand Gesture module."""
    print("Launching Hand Gesture module...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    
    # Path to Hand_Gesture.py
    gesture_script = os.path.join(script_dir, "Hand_Gesture.py")
    print(f"Gesture script path: {gesture_script}")
    
    # Check if Hand_Gesture.py exists
    if not os.path.exists(gesture_script):
        print(f"Error: Could not find {gesture_script}")
        
        # List files in the directory to help debug
        print("Files in directory:")
        for file in os.listdir(script_dir):
            if file.lower().find('hand') >= 0 or file.lower().find('gesture') >= 0:
                print(f"  - {file} (possible match)")
            elif file.endswith('.py'):
                print(f"  - {file}")
        
        return False
    
    try:
        # Launch the hand gesture module
        if platform.system() == 'Windows':
            # Use pythonw.exe on Windows to avoid showing a console window
            python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
            if not os.path.exists(python_exe):
                # Fall back to regular python if pythonw doesn't exist
                python_exe = sys.executable
            
            print(f"Using Python executable: {python_exe}")
            print(f"Command: {python_exe} {gesture_script}")
            
            subprocess.Popen([python_exe, gesture_script], 
                             creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # Linux/Mac - launch in background
            subprocess.Popen([sys.executable, gesture_script], 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             start_new_session=True)
        
        print("Hand Gesture module launched successfully!")
        return True
    except Exception as e:
        print(f"Error launching Hand Gesture module: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gesture":
        launch_hand_gesture()
    else:
        launch_app()
    # Exit immediately since the main app is now running
    sys.exit(0) 