#!/usr/bin/env python3
"""
Direct fix for Windows modern app support in GRACE Voice Agent
"""

import os

# Check if system_control.py exists
if not os.path.exists("system_control.py"):
    print("Error: system_control.py not found!")
    exit(1)

# Read the current system_control.py content
with open("system_control.py", "r") as f:
    content = f.readlines()

# Find where the application dictionary is defined
app_dict_start = -1
for i, line in enumerate(content):
    if "self.applications = {" in line:
        app_dict_start = i
        break

if app_dict_start == -1:
    print("Could not find applications dictionary in system_control.py!")
    exit(1)

# Find where the dictionary ends
app_dict_end = -1
open_braces = 0
for i in range(app_dict_start, len(content)):
    line = content[i]
    open_braces += line.count('{')
    open_braces -= line.count('}')
    if open_braces == 0:
        app_dict_end = i
        break

if app_dict_end == -1:
    print("Could not find end of applications dictionary!")
    exit(1)

# Update the applications dictionary
updated_dict = content[app_dict_start:app_dict_end+1]
# Add camera and calculator (or update them if they exist)
camera_found = False
calculator_found = False

for i, line in enumerate(updated_dict):
    if '"camera":' in line:
        updated_dict[i] = '            "camera": "explorer.exe shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App",\n'
        camera_found = True
    elif '"calculator":' in line:
        updated_dict[i] = '            "calculator": "calc",\n'
        calculator_found = True

# Add the entries if they don't exist
if not camera_found:
    updated_dict.insert(-1, '            "camera": "explorer.exe shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App",\n')
if not calculator_found:
    updated_dict.insert(-1, '            "calculator": "calc",\n')

# Create the updated content
updated_content = content[:app_dict_start] + updated_dict + content[app_dict_end+1:]

# Write the updated content back to system_control.py
with open("system_control.py", "w") as f:
    f.writelines(updated_content)

print("Successfully updated system_control.py to handle Windows Camera and Calculator apps!")
print("\nTry using these voice commands:")
print("- \"listen open camera\"")
print("- \"listen open calculator\"") 