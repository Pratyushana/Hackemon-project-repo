#!/usr/bin/env python3
"""
Test script for the GRACE Voice Agent with improved settings
"""

import sys
import time
import threading
from main import GraceVoiceAgent

def test_voice_agent():
    """Test the GRACE Voice Agent with improved settings"""
    print("=== Testing GRACE Voice Agent ===")
    print("This test will run the voice agent with improved settings for app/website opening.")
    
    # Create the voice agent with a clear wake word
    agent = GraceVoiceAgent(
        wake_word="listen",  # Using the default wake word
        gemini_api_key="AIzaSyD1VukpoEj4XVryusQckN7JnNl9y2EoQNM"  # Using the default API key
    )
    
    # Print test instructions
    print("\n=== Test Instructions ===")
    print("1. Say 'listen' to activate the voice agent")
    print("2. Try the following commands:")
    print("   - 'open chrome'")
    print("   - 'open youtube'")
    print("   - 'open notepad'")
    print("   - 'open google'")
    print("   - 'open calculator'")
    print("3. Try with 'execute' format:")
    print("   - 'listen open chrome execute'")
    print("   - 'listen execute open youtube'")
    print("4. Press Ctrl+C to exit the test")
    
    # Add a timeout to automatically stop the test after 5 minutes
    def timeout_handler():
        time.sleep(300)  # 5 minutes
        print("\n=== Test timeout reached (5 minutes) ===")
        print("Stopping the voice agent...")
        agent.is_running = False
    
    # Start the timeout thread
    timeout_thread = threading.Thread(target=timeout_handler)
    timeout_thread.daemon = True
    timeout_thread.start()
    
    # Start the voice agent (this will block until Ctrl+C or timeout)
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n=== Test stopped by user ===")
    
    print("\n=== Test Complete ===")
    print("Recent command history:")
    for cmd in agent.command_history[-10:]:
        print(f"- {cmd}")

if __name__ == "__main__":
    test_voice_agent()