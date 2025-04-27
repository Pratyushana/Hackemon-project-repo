#!/usr/bin/env python3
"""
Test Stop Functionality for GRACE Voice Agent

This script tests the ability to stop running GRACE Voice Agent processes
by launching components and then attempting to stop them using different methods.
"""

import os
import time
import platform
import subprocess
import sys

def test_launch_and_stop():
    """Test launching and stopping GRACE components"""
    print("=" * 60)
    print("GRACE Voice Agent Stop Functionality Test")
    print("=" * 60)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to components
    main_script = os.path.join(script_dir, "main.py")
    gesture_script = os.path.join(script_dir, "Hand_Gesture.py")
    
    # Check if files exist
    if not os.path.exists(main_script):
        print(f"Error: Could not find {main_script}")
        return False
        
    if not os.path.exists(gesture_script):
        print(f"Error: Could not find {gesture_script}")
        print("Will only test voice agent functionality")
    
    # Test Voice Agent
    try:
        print("\n[TEST 1] Launching Voice Agent...")
        
        # Launch Voice Agent
        if platform.system() == 'Windows':
            python_exe = sys.executable
            process = subprocess.Popen([python_exe, main_script])
        else:
            process = subprocess.Popen([sys.executable, main_script])
        
        print(f"Voice Agent launched with PID: {process.pid}")
        time.sleep(5)  # Wait for startup
        
        print("\nTesting stop method 1: Direct process termination")
        try:
            if platform.system() == 'Windows':
                subprocess.run(f"taskkill /F /PID {process.pid}", shell=True)
            else:
                subprocess.run(f"kill -9 {process.pid}", shell=True)
            print("Direct process termination completed")
        except Exception as e:
            print(f"Error with direct termination: {e}")
        
        time.sleep(2)  # Wait for cleanup
        
        # Check if process is still running
        if process.poll() is not None:
            print("SUCCESS: Process terminated successfully")
        else:
            print("WARNING: Process may still be running")
            
    except Exception as e:
        print(f"Error during Voice Agent test: {e}")
    
    # Wait a bit before testing Hand Gesture
    time.sleep(3)
    
    # Test Hand Gesture if available
    if os.path.exists(gesture_script):
        try:
            print("\n[TEST 2] Launching Hand Gesture module...")
            
            # Launch Hand Gesture
            if platform.system() == 'Windows':
                python_exe = sys.executable
                gesture_process = subprocess.Popen([python_exe, gesture_script])
            else:
                gesture_process = subprocess.Popen([sys.executable, gesture_script])
            
            print(f"Hand Gesture launched with PID: {gesture_process.pid}")
            time.sleep(5)  # Wait for startup
            
            print("\nTesting stop method 2: Using taskkill with command line filter")
            try:
                if platform.system() == 'Windows':
                    subprocess.run("taskkill /F /FI \"IMAGENAME eq python.exe\" /FI \"COMMANDLINE eq *Hand_Gesture.py*\"", shell=True)
                else:
                    subprocess.run("pkill -f Hand_Gesture.py", shell=True)
                print("Command line filter termination completed")
            except Exception as e:
                print(f"Error with command line filter termination: {e}")
            
            time.sleep(2)  # Wait for cleanup
            
            # Check if process is still running
            if gesture_process.poll() is not None:
                print("SUCCESS: Hand Gesture process terminated successfully")
            else:
                print("WARNING: Hand Gesture process may still be running")
                
        except Exception as e:
            print(f"Error during Hand Gesture test: {e}")
    
    # Test the /api/stop endpoint
    try:
        print("\n[TEST 3] Testing /api/stop endpoint...")
        
        # First launch both components again
        if platform.system() == 'Windows':
            python_exe = sys.executable
            process1 = subprocess.Popen([python_exe, main_script])
            
            if os.path.exists(gesture_script):
                process2 = subprocess.Popen([python_exe, gesture_script])
            else:
                process2 = None
        else:
            process1 = subprocess.Popen([sys.executable, main_script])
            
            if os.path.exists(gesture_script):
                process2 = subprocess.Popen([sys.executable, gesture_script])
            else:
                process2 = None
        
        print(f"Voice Agent launched with PID: {process1.pid}")
        if process2:
            print(f"Hand Gesture launched with PID: {process2.pid}")
        
        time.sleep(5)  # Wait for startup
        
        # Use curl to call the /api/stop endpoint
        print("\nCalling /api/stop endpoint...")
        if platform.system() == 'Windows':
            result = subprocess.run("curl -X POST http://localhost:5000/api/stop", shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run("curl -X POST http://localhost:5000/api/stop", shell=True, capture_output=True, text=True)
        
        print(f"API Response: {result.stdout}")
        
        time.sleep(2)  # Wait for cleanup
        
        # Check if processes are still running
        if process1.poll() is not None:
            print("SUCCESS: Voice Agent process terminated successfully")
        else:
            print("WARNING: Voice Agent process may still be running")
            
        if process2 and process2.poll() is not None:
            print("SUCCESS: Hand Gesture process terminated successfully")
        elif process2:
            print("WARNING: Hand Gesture process may still be running")
            
    except Exception as e:
        print(f"Error during API test: {e}")
    
    print("\nStop functionality test completed.")
    print("Check the results above to see if all stop methods worked as expected.")

if __name__ == "__main__":
    test_launch_and_stop() 