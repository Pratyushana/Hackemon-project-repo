#!/usr/bin/env python3
"""
Environment Setup Script for GRACE Voice Agent

This script helps create a proper .env file with your API keys.
"""

import os
import shutil
import sys

def setup_env():
    """Set up the .env file with required API keys"""
    
    # Check if .env file already exists
    if os.path.exists(".env"):
        overwrite = input(".env file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Setup canceled.")
            return
    
    # Try to copy from template
    if os.path.exists("env_template"):
        shutil.copy("env_template", ".env")
        print("Created .env file from template.")
    else:
        # Create file from scratch
        with open(".env", "w") as f:
            f.write("# GRACE Voice Agent Environment Variables\n\n")
            f.write("# Google Gemini API Key (Required)\n")
            f.write("GEMINI_KEY=\n\n")
            f.write("# OpenAI API Key (Optional)\n")
            f.write("OPENAI_KEY=\n\n")
            f.write("# Stability API Key (Optional)\n")
            f.write("STABILITY_KEY=\n\n")
            f.write("# HuggingFace Token (Optional)\n")
            f.write("HF_TOKEN=\n")
        print("Created new .env file.")
    
    # Get API keys from user
    print("\nPlease enter your API keys (leave blank to skip):")
    
    # Try to read existing .env file to get current values
    current_keys = {}
    try:
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    current_keys[key] = value
    except:
        pass
    
    # Get the Gemini API key (adding the hardcoded one as default)
    default_gemini = current_keys.get("GEMINI_KEY", "")
    gemini_key = input(f"Gemini API Key [current: {default_gemini if default_gemini else 'None'}]: ")
    gemini_key = gemini_key if gemini_key else default_gemini
    
    # Get the OpenAI API key
    default_openai = current_keys.get("OPENAI_KEY", "")
    openai_key = input(f"OpenAI API Key [current: {default_openai if default_openai else 'None'}]: ")
    openai_key = openai_key if openai_key else default_openai
    
    # Get the Stability API key
    default_stability = current_keys.get("STABILITY_KEY", "")
    stability_key = input(f"Stability API Key [current: {default_stability if default_stability else 'None'}]: ")
    stability_key = stability_key if stability_key else default_stability
    
    # Get the HuggingFace token
    default_hf = current_keys.get("HF_TOKEN", "")
    hf_token = input(f"HuggingFace Token [current: {default_hf if default_hf else 'None'}]: ")
    hf_token = hf_token if hf_token else default_hf
    
    # Write the updated .env file
    with open(".env", "w") as f:
        f.write("# GRACE Voice Agent Environment Variables\n\n")
        f.write("# Google Gemini API Key (Required)\n")
        f.write(f"GEMINI_KEY={gemini_key}\n\n")
        f.write("# OpenAI API Key (Optional)\n")
        f.write(f"OPENAI_KEY={openai_key}\n\n")
        f.write("# Stability API Key (Optional)\n")
        f.write(f"STABILITY_KEY={stability_key}\n\n")
        f.write("# HuggingFace Token (Optional)\n")
        f.write(f"HF_TOKEN={hf_token}\n")
    
    print("\n.env file has been updated successfully!")
    
    # Verify environment setup
    if not gemini_key:
        print("\nWarning: Gemini API key is required for code analysis and AI features.")
    else:
        print("\nYour environment is set up with:")
        print(f"- Gemini API Key: {'✓ Set' if gemini_key else '✗ Missing'}")
        print(f"- OpenAI API Key: {'✓ Set' if openai_key else '✗ Missing (optional)'}")
        print(f"- Stability API Key: {'✓ Set' if stability_key else '✗ Missing (optional)'}")
        print(f"- HuggingFace Token: {'✓ Set' if hf_token else '✗ Missing (optional)'}")
    
    print("\nYou can now run GRACE Voice Agent with:")
    print("python main.py")

if __name__ == "__main__":
    print("=" * 60)
    print("GRACE Voice Agent - Environment Setup")
    print("=" * 60)
    setup_env() 