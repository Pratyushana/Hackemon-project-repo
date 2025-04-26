#!/usr/bin/env python3
"""
Test for opening Camera and Calculator after the fix
"""

import subprocess
import time
import os
from system_control import SystemControl

def test_app_opening():
    """Test that Camera and Calculator can now be opened"""
    print("=== Testing Fixed App Opening ===")
    
    # Create a system control instance
    control = SystemControl()
    
    # Test Camera and Calculator
    apps_to_test = [
        "calculator",
        "camera"
    ]
    
    for app in apps_to_test:
        print(f"\nTesting application: {app}")
        result = control.open_application(app)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(3)  # Give some time for the app to open
        
    print("\n=== Test Complete ===")
    print("If the apps opened successfully, the fix worked!")
    print("You can now use voice commands like 'listen open camera' and 'listen open calculator'")

if __name__ == "__main__":
    test_app_opening() 