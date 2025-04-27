#!/usr/bin/env python3
"""
Test script for WhatsApp integration functionality
Tests both opening WhatsApp desktop app and sending messages
"""

import os
import time
import sys
from system_control import SystemControl
from main import GraceVoiceAgent

def test_system_control_methods():
    """Test the SystemControl methods for WhatsApp functionality"""
    print("=== Testing SystemControl WhatsApp Methods ===")
    
    # Create a system control instance
    control = SystemControl()
    
    # Test 1: Open WhatsApp application
    print("\nTest 1: Opening WhatsApp desktop application...")
    result1 = control.open_application("whatsapp")
    print(f"Result: {'Success' if result1 else 'Failed'}")
    time.sleep(3)  # Wait for WhatsApp to open
    
    # Test 2: Send a WhatsApp message
    print("\nTest 2: Sending a WhatsApp message...")
    contact = input("Enter contact name or number to message: ")
    message = input("Enter message to send: ")
    result2 = control.send_whatsapp_message(contact, message)
    print(f"Result: {'Success' if result2 else 'Failed'}")
    
    # Show action history
    print("\nAction history:")
    for action in control.get_action_history():
        print(f"- {action}")
    
    print("\n=== SystemControl Tests Complete ===")
    return result1 and result2

def test_voice_agent_commands():
    """Test the Voice Agent command handlers for WhatsApp functionality"""
    print("\n=== Testing Voice Agent WhatsApp Commands ===")
    
    # Create a voice agent instance
    agent = GraceVoiceAgent()
    
    # Test 1: Simulate a voice command to open WhatsApp
    print("\nTest 1: Simulating voice command 'open whatsapp'...")
    agent._handle_open_command("whatsapp")
    time.sleep(3)  # Wait for WhatsApp to open
    
    # Test 2: Simulate a voice command to send a WhatsApp message
    print("\nTest 2: Simulating voice command to send a WhatsApp message...")
    contact = input("Enter contact name to message: ")
    message = input("Enter message to send: ")
    command = f"{contact} {message}"
    agent._handle_message_command(command)
    
    print("\n=== Voice Agent Tests Complete ===")

if __name__ == "__main__":
    print("WhatsApp Integration Test")
    print("-------------------------")
    
    # Choose which tests to run
    choice = input("What would you like to test?\n1. SystemControl methods\n2. Voice Agent commands\n3. Both\nEnter choice (1-3): ")
    
    if choice == "1":
        test_system_control_methods()
    elif choice == "2":
        test_voice_agent_commands()
    elif choice == "3":
        system_success = test_system_control_methods()
        if system_success:
            test_voice_agent_commands()
        else:
            print("Skipping Voice Agent tests since SystemControl tests failed.")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    
    print("\nAll tests completed!") 