#!/usr/bin/env python3
"""
Test script for WhatsApp opening functionality
"""

import os
import time
from system_control import SystemControl

def test_whatsapp_opening():
    """Test the WhatsApp desktop application opening functionality"""
    print("=== Testing WhatsApp Desktop Application Opening ===")
    
    # Create a system control instance
    control = SystemControl()
    
    # Test opening WhatsApp desktop application
    print("\nTesting WhatsApp desktop application:")
    result = control.open_application("whatsapp")
    print(f"Result: {'Success' if result else 'Failed'}")
    
    # Show action history
    print("\nAction history:")
    for action in control.get_action_history():
        print(f"- {action}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_whatsapp_opening() 