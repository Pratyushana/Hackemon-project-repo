#!/usr/bin/env python3
"""
Test script for opening Windows 10/11 apps directly using PowerShell
"""

import subprocess
import time
import os

def open_windows_app(app_name):
    """Open a Windows 10/11 app using PowerShell
    
    Args:
        app_name (str): Name of the app as it appears in Windows
            
    Returns:
        bool: Success status
    """
    # PowerShell command to open app - properly escaped and wrapped
    powershell_cmd = f'powershell.exe -Command "Start-Process (Get-AppxPackage *{app_name}* | Select-Object -First 1).PackageFamilyName!App"'
    
    try:
        print(f"Attempting to open {app_name} using PowerShell...")
        subprocess.run(powershell_cmd, shell=True, check=True)
        print(f"Successfully launched {app_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening {app_name} with method 1: {e}")
        
        # Try alternate method
        try:
            # Alternate method - use explorer protocol for Windows apps
            alt_cmd = f'explorer.exe shell:appsFolder\\Microsoft.{app_name}_8wekyb3d8bbwe!App'
            subprocess.run(alt_cmd, shell=True, check=True)
            print(f"Successfully launched {app_name} using alternate method")
            return True
        except subprocess.CalledProcessError as alt_e:
            print(f"Error opening {app_name} with alternate method: {alt_e}")
            return False

def main():
    """Test script main function"""
    print("=== Testing Windows 10/11 App Opening ===")
    
    # Apps to test
    apps_to_test = [
        "Calculator",
        "Camera"
    ]
    
    for app in apps_to_test:
        print(f"\nTesting app: {app}")
        result = open_windows_app(app)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(2)  # Give some time for the app to open
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main() 