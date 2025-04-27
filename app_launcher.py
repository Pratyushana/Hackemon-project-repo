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
import time

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
    
    # Check for the .env file and create it if it doesn't exist
    env_file = os.path.join(script_dir, ".env")
    if not os.path.exists(env_file):
        print("Creating .env file with default API key")
        with open(env_file, "w") as f:
            f.write("# GRACE Voice Agent Environment Variables\n\n")
            f.write("# Google Gemini API Key\n")
            f.write("GEMINI_KEY=AIzaSyD1VukpoEj4XVryusQckN7JnNl9y2EoQNM\n\n")
            f.write("# OpenAI API Key (optional, for Whisper)\n")
            f.write("# OPENAI_KEY=your_openai_api_key_here\n\n")
            f.write("# Stability AI API Key (for image generation)\n")
            f.write("# STABILITY_KEY=your_stability_api_key_here\n\n")
            f.write("# HuggingFace Token (for image generation and AI features)\n")
            f.write("# HF_TOKEN=your_huggingface_token_here\n")
    
    try:
        # Always use visible console window to see errors when launched from website
        python_exe = sys.executable
        
        # Show what we're running
        print(f"Using Python executable: {python_exe}")
        print(f"Command: {python_exe} {main_script}")
        
        # Launch in a visible console window
        if platform.system() == 'Windows':
            # Start in a visible command window to see errors
            os.system(f'start cmd /K "cd {script_dir} && {python_exe} {main_script}"')
            
            # Wait a bit to give the process time to start
            time.sleep(1)
            print("GRACE Voice Agent launched successfully!")
            return True
        else:
            # For Linux/Mac, open in a terminal
            os.system(f'gnome-terminal -- {python_exe} {main_script}')
            time.sleep(1)
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
        # Always use visible console window to see errors when launched from website
        python_exe = sys.executable
        
        # Show what we're running
        print(f"Using Python executable: {python_exe}")
        print(f"Command: {python_exe} {gesture_script}")
        
        # Launch in a visible console window
        if platform.system() == 'Windows':
            # Start in a visible command window to see errors
            os.system(f'start cmd /K "cd {script_dir} && {python_exe} {gesture_script}"')
            
            # Wait a bit to give the process time to start
            time.sleep(1)
            print("Hand Gesture module launched successfully!")
            return True
        else:
            # For Linux/Mac, open in a terminal
            os.system(f'gnome-terminal -- {python_exe} {gesture_script}')
            time.sleep(1)
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