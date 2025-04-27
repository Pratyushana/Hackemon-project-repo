#!/usr/bin/env python3
"""
Test script for WhatsApp messaging functionality
"""

import os
import time
from system_control import SystemControl

def test_whatsapp_messaging():
    """Test the WhatsApp messaging functionality"""
    print("=== Testing WhatsApp Messaging ===")
    
    # Create a system control instance
    control = SystemControl()
    
    # Ask for contact name
    contact = input("Enter contact name or number to message: ")
    
    # Ask for message
    message = input("Enter message to send: ")
    
    # Test sending WhatsApp message
    print(f"\nSending WhatsApp message to {contact}...")
    result = control.send_whatsapp_message(contact, message)
    print(f"Result: {'Success' if result else 'Failed'}")
    
    # Show action history
    print("\nAction history:")
    for action in control.get_action_history():
        print(f"- {action}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_whatsapp_messaging() 