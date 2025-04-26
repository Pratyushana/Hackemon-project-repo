#!/usr/bin/env python3

"""
Improved GRACE Voice Agent Launcher

This script serves as a launcher for the GRACE Voice Agent application.
It can be used to start the application directly from the website
and also includes functionality to stop background processes.
"""

import os
import sys
import subprocess
import platform
import traceback
import time
import signal
import atexit

# Global dictionary to store process IDs
processes = {
    "hand_gesture": None,
    "voice_agent": None
}

def cleanup_processes():
    """Clean up any running processes on exit"""
    for name, process in processes.items():
        if process is not None and process.poll() is None:
            try:
                print(f"Terminating {name} process (PID: {process.pid})...")
                if platform.system() == 'Windows':
                    subprocess.run(f"taskkill /F /PID {process.pid} /T", shell=True)
                else:
                    # Linux/Mac
                    os.kill(process.pid, signal.SIGTERM)
                    # Give it a moment to terminate
                    time.sleep(0.5)
                    if process.poll() is None:
                        os.kill(process.pid, signal.SIGKILL)
            except Exception as e:
                print(f"Error terminating {name} process: {e}")

# Register cleanup function to be called on exit
atexit.register(cleanup_processes)

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
                
            process = subprocess.Popen([python_exe, main_script], 
                             creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # Linux/Mac - launch in background
            process = subprocess.Popen([sys.executable, main_script], 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             start_new_session=True)
        
        # Store the process ID for later cleanup
        processes["voice_agent"] = process
        
        print(f"GRACE Voice Agent launched successfully! (PID: {process.pid})")
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
            # Use python.exe to show console window instead of pythonw.exe for better control
            python_exe = sys.executable  # Use regular python
            
            print(f"Using Python executable: {python_exe}")
            print(f"Command: {python_exe} {gesture_script}")
            
            process = subprocess.Popen([python_exe, gesture_script])
        else:
            # Linux/Mac - launch but keep track of the process
            process = subprocess.Popen([sys.executable, gesture_script])
        
        # Store the process ID for later cleanup
        processes["hand_gesture"] = process
        
        print(f"Hand Gesture module launched successfully! (PID: {process.pid})")
        return True
    except Exception as e:
        print(f"Error launching Hand Gesture module: {e}")
        traceback.print_exc()
        return False

def stop_hand_gesture():
    """Stop the running Hand Gesture module."""
    print("Stopping Hand Gesture module...")
    
    if processes["hand_gesture"] is not None and processes["hand_gesture"].poll() is None:
        try:
            print(f"Terminating Hand Gesture process (PID: {processes['hand_gesture'].pid})...")
            if platform.system() == 'Windows':
                subprocess.run(f"taskkill /F /PID {processes['hand_gesture'].pid} /T", shell=True)
            else:
                # Linux/Mac
                os.kill(processes["hand_gesture"].pid, signal.SIGTERM)
                # Give it a moment to terminate
                time.sleep(0.5)
                if processes["hand_gesture"].poll() is None:
                    os.kill(processes["hand_gesture"].pid, signal.SIGKILL)
            
            print("Hand Gesture module stopped!")
            processes["hand_gesture"] = None
            return True
        except Exception as e:
            print(f"Error stopping Hand Gesture module: {e}")
            traceback.print_exc()
            return False
    else:
        # Process not found in our tracking - try to find by window title or similar command line
        try:
            if platform.system() == 'Windows':
                # Try to kill by window title
                subprocess.run("taskkill /F /FI \"WINDOWTITLE eq Hand Gesture Control\" /T", shell=True)
                # Try to kill by image name and command line
                subprocess.run("taskkill /F /FI \"IMAGENAME eq pythonw.exe\" /FI \"COMMANDLINE eq *Hand_Gesture.py*\" /T", shell=True)
            else:
                # Linux/Mac
                os.system("pkill -f Hand_Gesture.py")
            
            print("Hand Gesture module stopped!")
            return True
        except Exception as e:
            print(f"Error stopping Hand Gesture module: {e}")
            traceback.print_exc()
            return False

def stop_voice_agent():
    """Stop the running Voice Agent."""
    print("Stopping Voice Agent...")
    
    if processes["voice_agent"] is not None and processes["voice_agent"].poll() is None:
        try:
            print(f"Terminating Voice Agent process (PID: {processes['voice_agent'].pid})...")
            if platform.system() == 'Windows':
                subprocess.run(f"taskkill /F /PID {processes['voice_agent'].pid} /T", shell=True)
            else:
                # Linux/Mac
                os.kill(processes["voice_agent"].pid, signal.SIGTERM)
                # Give it a moment to terminate
                time.sleep(0.5)
                if processes["voice_agent"].poll() is None:
                    os.kill(processes["voice_agent"].pid, signal.SIGKILL)
            
            print("Voice Agent stopped!")
            processes["voice_agent"] = None
            return True
        except Exception as e:
            print(f"Error stopping Voice Agent: {e}")
            traceback.print_exc()
            return False
    else:
        # Process not found in our tracking - try to find by command line
        try:
            if platform.system() == 'Windows':
                # Try to kill by image name and command line
                subprocess.run("taskkill /F /FI \"IMAGENAME eq pythonw.exe\" /FI \"COMMANDLINE eq *main.py*\" /T", shell=True)
            else:
                # Linux/Mac
                os.system("pkill -f main.py")
            
            print("Voice Agent stopped!")
            return True
        except Exception as e:
            print(f"Error stopping Voice Agent: {e}")
            traceback.print_exc()
            return False

def stop_all():
    """Stop all running modules."""
    voice_result = stop_voice_agent()
    gesture_result = stop_hand_gesture()
    return voice_result and gesture_result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "gesture":
            launch_hand_gesture()
        elif command == "voice":
            launch_app()
        elif command == "stop-gesture":
            stop_hand_gesture()
        elif command == "stop-voice":
            stop_voice_agent()
        elif command == "stop-all":
            stop_all()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: gesture, voice, stop-gesture, stop-voice, stop-all")
    else:
        # Default - launch voice agent
        launch_app()
    
    # Keep process running to maintain tracking until killed
    if any(p is not None for p in processes.values()):
        print("\nPress Ctrl+C to exit and stop all processes...\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping all processes and exiting...")
            stop_all()
    else:
        print("No processes to track. Exiting...") 