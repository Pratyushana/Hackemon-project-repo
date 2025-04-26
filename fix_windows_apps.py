#!/usr/bin/env python3
"""
Script to add support for Windows modern apps to GRACE Voice Agent
"""

import os
import sys

def fix_system_control():
    """Add support for Windows modern apps to system_control.py"""
    # Check if system_control.py exists
    if not os.path.exists("system_control.py"):
        print("Error: system_control.py not found in the current directory")
        return False
    
    print("Updating system_control.py with improved Windows app support...")
    
    # Read the current content
    with open("system_control.py", "r") as f:
        content = f.read()
    
    # Check if we've already patched the file
    if "modern_apps" in content:
        print("The system_control.py file has already been patched.")
        return True
    
    # Find where applications dictionary is defined
    if "self.applications = {" not in content:
        print("Error: Could not find applications dictionary in system_control.py")
        return False
    
    # Add Windows modern apps to the applications dictionary
    applications_update = """
        # Windows Modern Apps Dictionary - added for better UWP app support
        self.modern_apps = {
            "calculator": "calc.exe",
            "camera": "explorer.exe shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App",
            "photos": "explorer.exe shell:AppsFolder\\Microsoft.Windows.Photos_8wekyb3d8bbwe!App",
            "maps": "explorer.exe shell:AppsFolder\\Microsoft.WindowsMaps_8wekyb3d8bbwe!App",
            "store": "explorer.exe shell:AppsFolder\\Microsoft.WindowsStore_8wekyb3d8bbwe!App",
            "settings": "explorer.exe shell:AppsFolder\\windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel",
            "mail": "explorer.exe shell:AppsFolder\\microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.mail",
            "weather": "explorer.exe shell:AppsFolder\\Microsoft.BingWeather_8wekyb3d8bbwe!App",
            "news": "explorer.exe shell:AppsFolder\\Microsoft.BingNews_8wekyb3d8bbwe!AppexNews",
        }"""
    
    # Update the open_application method to check for modern apps
    open_app_update = """
    def open_application(self, app_name):
        \"\"\"Open an application by name
        
        Args:
            app_name (str): Name of the application to open
            
        Returns:
            bool: Success status
        \"\"\"
        app_name = app_name.lower()
        
        # Special handling for common websites
        websites = {
            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "instagram": "https://instagram.com",
            "linkedin": "https://linkedin.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "amazon": "https://amazon.com",
            "netflix": "https://netflix.com",
            "whatsapp": "https://web.whatsapp.com",
            "spotify": "https://open.spotify.com",
        }
        
        # Check if it's a website
        if app_name in websites:
            return self.open_url(websites[app_name])
        
        # Check if it's a modern Windows app
        if app_name in self.modern_apps:
            app_command = self.modern_apps[app_name]
            try:
                import subprocess
                subprocess.Popen(app_command, shell=True)
                self.action_history.append(f"Opened modern app: {app_name}")
                print(f"Successfully launched modern app: {app_name}")
                return True
            except Exception as e:
                print(f"Error opening modern app {app_name}: {e}")
                return False
        
        # Check if app name is in our dictionary
        if app_name in self.applications:
            app_command = self.applications[app_name]
            try:
                import subprocess
                subprocess.Popen(app_command, shell=True)
                self.action_history.append(f"Opened {app_name}")
                print(f"Successfully launched {app_name}")
                return True
            except Exception as e:
                print(f"Error opening {app_name}: {e}")
                
                # Try alternate methods for common applications
                try:
                    os.system(f"start {app_command}")
                    self.action_history.append(f"Opened {app_name} (alternative method)")
                    print(f"Successfully launched {app_name} using alternative method")
                    return True
                except Exception as alt_error:
                    print(f"Alternative method also failed: {alt_error}")
                    return False
        
        # If app name contains a dot, treat it as a URL
        if '.' in app_name:
            return self.open_url(app_name)
        
        # If we don't have a predefined command, try to open it directly
        try:
            os.system(f"start {app_name}")
            self.action_history.append(f"Opened {app_name}")
            print(f"Opened {app_name} using generic method")
            return True
        except Exception as e:
            print(f"Generic open method failed: {e}")
            return False"""
    
    # Replace the original open_application method with our updated version
    content = content.replace("def open_application(self, app_name):", open_app_update)
    
    # Add modern apps dictionary after applications dictionary
    content = content.replace("# Add more applications as needed", 
                             "# Add more applications as needed" + applications_update)
    
    # Write the updated content
    with open("system_control.py", "w") as f:
        f.write(content)
    
    print("Successfully updated system_control.py with improved Windows app support.")
    print("\nNow you can open Windows modern apps like Camera and Calculator using:")
    print("- 'listen open camera'")
    print("- 'listen open calculator'")
    return True

if __name__ == "__main__":
    fix_system_control() 