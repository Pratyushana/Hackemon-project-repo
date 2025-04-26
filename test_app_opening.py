#!/usr/bin/env python3
"""
Test script for application opening functionality
"""

import os
import time
from system_control import SystemControl

def test_app_opening():
    """Test the application opening functionality"""
    print("=== Testing Application Opening Functionality ===")
    
    # Create a system control instance
    control = SystemControl()
    
    # Test common applications
    apps_to_test = [
        "notepad",
        "calculator",
        "chrome",
        "firefox",
        "edge"
    ]
    
    for app in apps_to_test:
        print(f"\nTesting application: {app}")
        result = control.open_application(app)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(2)  # Give some time for the app to open
        
    # Test common websites
    websites_to_test = [
        "google",
        "youtube",
        "github.com",
        "amazon"
    ]
    
    for site in websites_to_test:
        print(f"\nTesting website: {site}")
        result = control.open_application(site)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(2)  # Give some time for the website to open
    
    print("\n=== Test Complete ===")
    print("Action history:")
    for action in control.get_action_history():
        print(f"- {action}")

if __name__ == "__main__":
    test_app_opening() 