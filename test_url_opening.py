#!/usr/bin/env python3
"""
Test script for URL opening functionality
"""

import os
import time
from system_control import SystemControl

def test_url_opening():
    """Test the URL opening functionality"""
    print("=== Testing URL Opening Functionality ===")
    
    # Create a system control instance
    control = SystemControl()
    
    # Test various URL formats
    urls_to_test = [
        "google.com",
        "youtube.com",
        "www.github.com",
        "https://amazon.com",
        "twitter.com/home",
        "linkedin.com",
        "wikipedia.org"
    ]
    
    for url in urls_to_test:
        print(f"\nTesting URL: {url}")
        result = control.open_url(url)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(2)  # Give some time for the browser to open
    
    # Test special cases with URL formatting
    print("\n=== Testing Special URL Cases ===")
    special_cases = [
        "google",  # No TLD
        "youtube without dots",  # Common website name with spaces
        "nytimes",  # Site that might not be in the direct mapping
    ]
    
    for case in special_cases:
        print(f"\nTesting special case: {case}")
        # Use open_application since it has the website dictionary
        result = control.open_application(case)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(2)
    
    print("\n=== Test Complete ===")
    print("Action history:")
    for action in control.get_action_history():
        print(f"- {action}")

if __name__ == "__main__":
    test_url_opening()