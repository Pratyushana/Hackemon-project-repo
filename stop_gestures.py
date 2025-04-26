#!/usr/bin/env python3
"""
Stop Hand Gesture Processes

This script will stop all running instances of the Hand_Gesture.py application
that might still be running in the background.
"""

import os
import sys
import subprocess
import platform

def stop_gesture_processes():
    """Find and terminate all running Hand_Gesture processes."""
    print("Stopping all Hand Gesture processes...")
    
    try:
        if platform.system() == 'Windows':
            # Find all pythonw.exe processes running Hand_Gesture.py
            output = subprocess.check_output(
                "wmic process where \"name='pythonw.exe'\" get commandline", 
                shell=True
            ).decode('utf-8')
            
            # Look for processes running Hand_Gesture.py
            gesture_processes = []
            for line in output.splitlines():
                if 'Hand_Gesture.py' in line:
                    # Extract the PID using another command
                    cmd_part = line.strip()
                    try:
                        # Get the PID of this process
                        pid_output = subprocess.check_output(
                            f"wmic process where \"commandline like '%{cmd_part[-20:]}%' and name='pythonw.exe'\" get processid",
                            shell=True
                        ).decode('utf-8')
                        
                        for pid_line in pid_output.splitlines():
                            if pid_line.strip() and pid_line.strip().isdigit():
                                gesture_processes.append(pid_line.strip())
                    except:
                        # If we can't get the PID, we'll use a more general approach
                        pass
            
            if gesture_processes:
                # Kill the processes by PID
                for pid in gesture_processes:
                    try:
                        print(f"Terminating Hand Gesture process with PID: {pid}")
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True)
                    except Exception as e:
                        print(f"Error terminating process {pid}: {e}")
            
            # As a fallback, attempt to kill all pythonw.exe processes related to Hand_Gesture
            try:
                subprocess.run("taskkill /F /FI \"WINDOWTITLE eq Hand Gesture Control\" /T", shell=True)
                subprocess.run("taskkill /F /FI \"IMAGENAME eq pythonw.exe\" /FI \"WINDOWTITLE eq Hand Gesture Control\" /T", shell=True)
            except:
                pass
                
            # Final fallback - allow user to kill all pythonw processes if needed
            if input("Do you want to stop ALL pythonw.exe processes? (y/n): ").lower() == 'y':
                subprocess.run("taskkill /F /IM pythonw.exe /T", shell=True)
                print("All pythonw.exe processes have been terminated.")
                
        else:
            # Linux/Mac
            print("Finding and terminating Hand Gesture processes on Linux/Mac...")
            # Use pkill to find and kill processes by name
            os.system("pkill -f Hand_Gesture.py")
            
        print("Hand Gesture processes terminated successfully!")
        return True
    except Exception as e:
        print(f"Error stopping Hand Gesture processes: {e}")
        return False

if __name__ == "__main__":
    stop_gesture_processes()
    input("Press Enter to exit...") 