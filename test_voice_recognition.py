#!/usr/bin/env python3
"""
Test script for voice recognition and command processing
"""

import time
from speech_recognition_module import SpeechRecognizer
from tts import TextToSpeech

def test_voice_recognition():
    """Test voice recognition functionality"""
    print("=== Testing Voice Recognition ===")
    
    # Initialize speech recognizer and text-to-speech
    recognizer = SpeechRecognizer(api="google")
    tts = TextToSpeech()
    
    # Provide test instructions
    print("This test will check voice recognition and command parsing.")
    tts.speak("This is a voice recognition test. I'll listen for your commands in 3 seconds.")
    time.sleep(3)
    
    # Test basic recognition
    print("\n=== Test 1: Basic Recognition ===")
    print("Please say something when prompted...")
    tts.speak("Please say something now.")
    text = recognizer.listen_once()
    print(f"Recognized text: '{text}'")
    
    # Test command recognition with longer phrases
    print("\n=== Test 2: Command Recognition ===")
    print("Please say a command like 'open chrome' or 'open youtube' when prompted...")
    tts.speak("Please say a command now.")
    command = recognizer.listen_for_command(phrase_time_limit=8)
    print(f"Recognized command: '{command}'")
    
    # Test handling website commands
    print("\n=== Test 3: Website Opening Command ===")
    print("Please say 'open youtube' or 'open google' when prompted...")
    tts.speak("Please say a website opening command now.")
    web_command = recognizer.listen_for_command(phrase_time_limit=8)
    print(f"Recognized web command: '{web_command}'")
    
    # Test special case with 'execute'
    print("\n=== Test 4: Execute Command ===")
    print("Please say 'open chrome execute' when prompted...")
    tts.speak("Please say a command with execute now.")
    execute_command = recognizer.listen_for_command(phrase_time_limit=8)
    print(f"Recognized execute command: '{execute_command}'")
    
    print("\n=== Test Complete ===")
    print("These tests only verify voice recognition, not command execution.")
    tts.speak("Voice recognition test complete. Thank you.")

if __name__ == "__main__":
    test_voice_recognition() 