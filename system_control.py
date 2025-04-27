import subprocess
import os
import pyautogui
import time
import pyperclip
import webbrowser

class SystemControl:
    def __init__(self):
        """Initialize system control module"""
        # Default applications dictionary
        self.applications = {
            "chrome": "chrome",
            "edge": "msedge",
            "firefox": "firefox",
            "notepad": "notepad",
            "calculator": "calc",
            "explorer": "explorer",
            "file explorer": "explorer",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "code": "code",
            "visual studio code": "code",
            "visual studio": "devenv",
            "terminal": "cmd",
            "command prompt": "cmd",
            "powershell": "powershell",
            # Add more applications as needed
        }
        
        # Windows Modern Apps Dictionary - for UWP app support
        self.modern_apps = {
            "calculator": "calc",
            "camera": "explorer.exe shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App",
            "photos": "explorer.exe shell:AppsFolder\\Microsoft.Windows.Photos_8wekyb3d8bbwe!App",
            "maps": "explorer.exe shell:AppsFolder\\Microsoft.WindowsMaps_8wekyb3d8bbwe!App",
            "store": "explorer.exe shell:AppsFolder\\Microsoft.WindowsStore_8wekyb3d8bbwe!App",
            "settings": "explorer.exe shell:AppsFolder\\windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel",
            "mail": "explorer.exe shell:AppsFolder\\microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.mail",
            "weather": "explorer.exe shell:AppsFolder\\Microsoft.BingWeather_8wekyb3d8bbwe!App",
            "news": "explorer.exe shell:AppsFolder\\Microsoft.BingNews_8wekyb3d8bbwe!AppexNews"
        }
        
        # Store actions history
        self.action_history = []
        
    def open_application(self, app_name):
        """Open an application by name
        
        Args:
            app_name (str): Name of the application to open
            
        Returns:
            bool: Success status
        """
        app_name = app_name.lower()
        
        # Special handling for WhatsApp Desktop
        if app_name == "whatsapp":
            # Try multiple possible WhatsApp locations
            whatsapp_locations = [
                # Microsoft Store version (path may vary)
                r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2354.0.0_x64__cv1g1gvanyjgm\WhatsApp.exe", 
                # Standard installation path
                r"C:\Program Files\WhatsApp\WhatsApp.exe",
                # Another common location
                os.path.join(os.environ.get('LOCALAPPDATA', ''), r"WhatsApp\WhatsApp.exe"),
                # Simple command that might work if WhatsApp is in PATH
                "WhatsApp.exe"
            ]
            
            for location in whatsapp_locations:
                try:
                    print(f"Trying WhatsApp location: {location}")
                    if os.path.exists(location):
                        subprocess.Popen(location, shell=True)
                        self.action_history.append(f"Opened WhatsApp desktop app")
                        print(f"Successfully launched WhatsApp desktop app")
                        return True
                except Exception as e:
                    print(f"Error with WhatsApp location {location}: {e}")
                    continue
            
            # If reached here, try Windows App URI launch for Microsoft Store apps
            try:
                # Use Windows App URI to launch WhatsApp
                subprocess.Popen(["explorer.exe", "whatsapp:"])
                self.action_history.append(f"Opened WhatsApp using Windows App URI")
                print(f"Opened WhatsApp using Windows App URI")
                return True
            except Exception as e:
                print(f"Windows App URI launch failed: {e}")
                
            # If that fails, try the generic approach
            try:
                os.system("start WhatsApp")
                self.action_history.append(f"Opened WhatsApp using generic method")
                print(f"Opened WhatsApp using generic method")
                return True
            except Exception as e:
                print(f"Generic WhatsApp open method failed: {e}")
                return False
        
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
            # "whatsapp": "https://web.whatsapp.com",  # Removed to use desktop app instead
            "spotify": "https://open.spotify.com",
        }
        
        # Check if it's a website
        if app_name in websites:
            return self.open_url(websites[app_name])
        
        # Check if it's a modern Windows app
        if app_name in self.modern_apps:
            app_command = self.modern_apps[app_name]
            try:
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
            return False
    
    def open_url(self, url):
        """Open a URL in the default browser
        
        Args:
            url (str): URL to open
            
        Returns:
            bool: Success status
        """
        # Add http:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        try:
            webbrowser.open(url)
            self.action_history.append(f"Opened URL: {url}")
            return True
        except Exception as e:
            print(f"Error opening URL: {e}")
            return False
    
    def type_text(self, text):
        """Type text using keyboard
        
        Args:
            text (str): Text to type
        """
        try:
            # Try to use pyautogui's write function
            pyautogui.write(text)
            print(f"Typed text: {text[:20]}..." if len(text) > 20 else f"Typed text: {text}")
            
            # Alternative approach using clipboard for reliability with special characters
            if not text.isascii():
                # Backup current clipboard
                old_clipboard = pyperclip.paste()
                
                # Set new content and paste
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                
                # Restore clipboard after a small delay
                time.sleep(0.5)
                pyperclip.copy(old_clipboard)
                print("Used clipboard method for non-ASCII text")
                
            self.action_history.append(f"Typed: {text[:20]}..." if len(text) > 20 else f"Typed: {text}")
        except Exception as e:
            print(f"Error typing text: {e}")
            
            # Fallback method
            try:
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                print("Used fallback clipboard method for typing")
            except Exception as fallback_error:
                print(f"Fallback typing method also failed: {fallback_error}")
    
    def press_key(self, key):
        """Press a keyboard key
        
        Args:
            key (str): Key to press
        """
        pyautogui.press(key)
        self.action_history.append(f"Pressed key: {key}")
    
    def press_key_combination(self, *keys):
        """Press a combination of keys
        
        Args:
            *keys: Keys to press simultaneously
        """
        pyautogui.hotkey(*keys)
        self.action_history.append(f"Pressed keys: {'+'.join(keys)}")
    
    def press_keyboard_shortcut(self, shortcut):
        """Press a common keyboard shortcut by name
        
        Args:
            shortcut (str): Name of the shortcut
            
        Returns:
            bool: Success status
        """
        shortcuts = {
            "copy": ["ctrl", "c"],
            "paste": ["ctrl", "v"],
            "cut": ["ctrl", "x"],
            "undo": ["ctrl", "z"],
            "redo": ["ctrl", "y"],
            "save": ["ctrl", "s"],
            "select all": ["ctrl", "a"],
            "find": ["ctrl", "f"],
            "new": ["ctrl", "n"],
            "print": ["ctrl", "p"],
            "refresh": ["f5"],
            "close tab": ["ctrl", "w"],
            "close window": ["alt", "f4"],
            "switch window": ["alt", "tab"],
            "window left": ["win", "left"],
            "window right": ["win", "right"],
            "maximize": ["win", "up"],
            "minimize": ["win", "down"],
            "start menu": ["win"],
            "task view": ["win", "tab"],
            "screenshot": ["win", "shift", "s"],
        }
        
        shortcut_lower = shortcut.lower()
        
        # Check for exact matches
        if shortcut_lower in shortcuts:
            try:
                keys = shortcuts[shortcut_lower]
                self.press_key_combination(*keys)
                print(f"Executed keyboard shortcut: {shortcut} ({'+'.join(keys)})")
                return True
            except Exception as e:
                print(f"Error executing shortcut {shortcut}: {e}")
                
                # Try individual key presses as fallback
                try:
                    for key in shortcuts[shortcut_lower]:
                        pyautogui.keyDown(key)
                    time.sleep(0.2)
                    for key in reversed(shortcuts[shortcut_lower]):
                        pyautogui.keyUp(key)
                    print(f"Used fallback method for shortcut: {shortcut}")
                    return True
                except Exception as fallback_error:
                    print(f"Fallback shortcut method also failed: {fallback_error}")
                    return False
        
        # Check for partial matches
        for name, keys in shortcuts.items():
            if name in shortcut_lower or shortcut_lower in name:
                try:
                    self.press_key_combination(*keys)
                    print(f"Executed similar keyboard shortcut: {name} ({'+'.join(keys)})")
                    return True
                except Exception as e:
                    print(f"Error executing similar shortcut {name}: {e}")
        
        print(f"Unknown shortcut: {shortcut}")
        return False
    
    def mouse_click(self, x=None, y=None, button="left"):
        """Click the mouse
        
        Args:
            x (int, optional): X coordinate, or None for current position
            y (int, optional): Y coordinate, or None for current position
            button (str): Button to click ("left", "right", "middle")
        """
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button)
                self.action_history.append(f"{button.capitalize()} clicked at ({x}, {y})")
            else:
                pyautogui.click(button=button)
                current_pos = pyautogui.position()
                print(f"{button.capitalize()} click at position {current_pos}")
                self.action_history.append(f"{button.capitalize()} clicked at current position {current_pos}")
        except Exception as e:
            print(f"Error clicking mouse: {e}")
            
            # Fallback for click
            try:
                if button == "left":
                    pyautogui.mouseDown(button=button)
                    time.sleep(0.1)
                    pyautogui.mouseUp(button=button)
                    print("Used fallback method for mouse click")
                elif button == "right":
                    self.press_key_combination('shift', 'f10')
                    print("Used keyboard shortcut for right click")
            except Exception as fallback_error:
                print(f"Fallback click method also failed: {fallback_error}")
    
    def double_click(self, x=None, y=None):
        """Double-click the mouse
        
        Args:
            x (int, optional): X coordinate, or None for current position
            y (int, optional): Y coordinate, or None for current position
        """
        try:
            if x is not None and y is not None:
                pyautogui.doubleClick(x, y)
                self.action_history.append(f"Double clicked at ({x}, {y})")
            else:
                pyautogui.doubleClick()
                current_pos = pyautogui.position()
                print(f"Double click at position {current_pos}")
                self.action_history.append(f"Double clicked at current position {current_pos}")
        except Exception as e:
            print(f"Error double clicking: {e}")
            
            # Fallback with two single clicks
            self.mouse_click(x, y)
            time.sleep(0.1)
            self.mouse_click(x, y)
    
    def right_click(self, x=None, y=None):
        """Right-click the mouse
        
        Args:
            x (int, optional): X coordinate, or None for current position
            y (int, optional): Y coordinate, or None for current position
        """
        self.mouse_click(x, y, button="right")
    
    def scroll(self, amount):
        """Scroll the mouse wheel
        
        Args:
            amount (int): Scroll amount, positive is up, negative is down
        """
        # Set the scroll speed factor (adjust as needed)
        scroll_speed = 1
        
        # Apply the speed adjustment
        adjusted_amount = amount * scroll_speed
        
        try:
            # Try scrolling with pyautogui
            pyautogui.scroll(adjusted_amount)
            
            # Add to action history
            if amount > 0:
                direction = "up"
            else:
                direction = "down"
            
            self.action_history.append(f"Scrolled {direction} ({abs(amount)})")
            print(f"Scrolled {direction} ({abs(amount)})")
        except Exception as e:
            print(f"Error scrolling: {e}")
            
            # Fallback approach using Page Up/Down keys
            try:
                if amount > 0:
                    for _ in range(abs(int(amount / 120))):
                        pyautogui.press('pageup')
                else:
                    for _ in range(abs(int(amount / 120))):
                        pyautogui.press('pagedown')
                
                print("Used fallback method for scrolling")
            except Exception as fallback_error:
                print(f"Fallback scrolling method also failed: {fallback_error}")
    
    def move_mouse(self, x, y):
        """Move the mouse cursor to a position
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        try:
            pyautogui.moveTo(x, y)
            self.action_history.append(f"Moved mouse to ({x}, {y})")
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    def get_mouse_position(self):
        """Get the current mouse position
        
        Returns:
            tuple: (x, y) coordinates
        """
        return pyautogui.position()
    
    def copy_to_clipboard(self):
        """Copy currently selected text to clipboard
        
        Returns:
            str: Copied text
        """
        self.press_keyboard_shortcut("copy")
        time.sleep(0.2)  # Wait for the clipboard to update
        
        try:
            text = pyperclip.paste()
            if text:
                print(f"Copied to clipboard: {text[:50]}..." if len(text) > 50 else f"Copied to clipboard: {text}")
            return text
        except Exception as e:
            print(f"Error accessing clipboard: {e}")
            return ""
    
    def paste_from_clipboard(self):
        """Paste content from clipboard"""
        self.press_keyboard_shortcut("paste")
    
    def set_clipboard(self, text):
        """Set clipboard content
        
        Args:
            text (str): Text to set in clipboard
        """
        try:
            pyperclip.copy(text)
            print(f"Set clipboard: {text[:50]}..." if len(text) > 50 else f"Set clipboard: {text}")
        except Exception as e:
            print(f"Error setting clipboard: {e}")
    
    def take_screenshot(self, filename=None):
        """Take a screenshot
        
        Args:
            filename (str, optional): Output filename, or None for auto-generated name
            
        Returns:
            str: Path to the saved screenshot file
        """
        try:
            if filename is None:
                filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
            
            # Ensure we have a folder for screenshots
            os.makedirs("screenshots", exist_ok=True)
            filepath = os.path.join("screenshots", filename)
            
            # Take the screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            print(f"Screenshot saved to {filepath}")
            self.action_history.append(f"Took screenshot: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def get_action_history(self, limit=10):
        """Get recent action history
        
        Args:
            limit (int): Maximum number of actions to return
            
        Returns:
            list: Recent actions
        """
        return self.action_history[-limit:] if self.action_history else []
    
    def send_whatsapp_message(self, contact, message):
        """Send a WhatsApp message to a contact
        
        Args:
            contact (str): Contact name or number to send message to
            message (str): Message to send
            
        Returns:
            bool: Success status
        """
        # First try WhatsApp desktop app
        desktop_result = self._send_whatsapp_message_desktop(contact, message)
        
        # If desktop app fails, try WhatsApp Web as fallback
        if not desktop_result:
            print("Desktop app failed, trying WhatsApp Web as fallback...")
            return self._send_whatsapp_message_web(contact, message)
        
        return desktop_result
        
    def _send_whatsapp_message_desktop(self, contact, message):
        """Send a WhatsApp message using the desktop application
        
        Args:
            contact (str): Contact name or number
            message (str): Message to send
            
        Returns:
            bool: Success status
        """
        # First make sure WhatsApp is open
        self.open_application("whatsapp")
        
        # Wait longer for WhatsApp to load fully
        time.sleep(8)
        
        try:
            # Get screen size to calculate relative positions
            screen_width, screen_height = pyautogui.size()
            
            # Calculate positions as percentages of screen size
            # Search box is usually in the top-left portion of WhatsApp
            search_x = int(screen_width * 0.2)  # 20% from left
            search_y = int(screen_height * 0.1)  # 10% from top
            
            # Message box is usually in the bottom portion of WhatsApp
            message_x = int(screen_width * 0.5)  # Center horizontally
            message_y = int(screen_height * 0.8)  # 80% from top (near bottom)
            
            # Click on the search bar
            pyautogui.moveTo(search_x, search_y, duration=0.5)
            pyautogui.click()
            time.sleep(1)
            
            # Type the contact name
            pyautogui.write(contact, interval=0.1)
            time.sleep(2)
            
            # Press Down and Enter to select the first contact
            pyautogui.press('down')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2)
            
            # Click on the message box
            pyautogui.moveTo(message_x, message_y, duration=0.5)
            pyautogui.click()
            time.sleep(1)
            
            # Type and send the message
            pyautogui.write(message, interval=0.05)
            pyautogui.press('enter')
            
            self.action_history.append(f"Sent WhatsApp message to {contact}")
            print(f"Successfully sent WhatsApp message to {contact}")
            return True
            
        except Exception as e:
            print(f"Error sending WhatsApp message via desktop app: {e}")
            
            # Try alternative method using clipboard for the message
            try:
                # Try to locate and click the message box by tab navigation
                pyautogui.hotkey('ctrl', 'f')  # Focus search
                time.sleep(0.5)
                pyautogui.write(contact, interval=0.1)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                
                # Try to focus the message area with tab
                pyautogui.press('tab')
                time.sleep(0.5)
                
                # Send message using clipboard
                pyperclip.copy(message)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                pyautogui.press('enter')
                
                self.action_history.append(f"Sent WhatsApp message to {contact} (alternative method)")
                print(f"Successfully sent WhatsApp message to {contact} using alternative method")
                return True
            except Exception as alt_error:
                print(f"Alternative desktop method also failed: {alt_error}")
                return False
    
    def _send_whatsapp_message_web(self, contact, message):
        """Send a WhatsApp message using WhatsApp Web
        
        Args:
            contact (str): Contact name or phone number
            message (str): Message to send
            
        Returns:
            bool: Success status
        """
        try:
            # Check if contact is a phone number
            is_phone_number = all(c.isdigit() or c == '+' for c in contact)
            
            if is_phone_number:
                # For phone numbers, we can use the direct API
                # Make sure phone number is in international format without + sign
                if contact.startswith('+'):
                    contact = contact[1:]
                
                # Open WhatsApp Web with the phone number
                url = f"https://web.whatsapp.com/send?phone={contact}&text={message}"
                webbrowser.open(url)
                
                # Wait for page to load
                time.sleep(10)
                
                # Press Enter to send the message
                pyautogui.press('enter')
                
                self.action_history.append(f"Sent WhatsApp Web message to {contact}")
                print(f"Successfully sent WhatsApp Web message to {contact}")
                return True
            else:
                # For contact names, we need to open WhatsApp Web, search and select the contact
                webbrowser.open("https://web.whatsapp.com")
                time.sleep(10)  # Wait for WhatsApp Web to load
                
                # Get screen dimensions
                screen_width, screen_height = pyautogui.size()
                
                # Search box is typically in the top left
                search_x = int(screen_width * 0.15)
                search_y = int(screen_height * 0.1)
                
                # Click on search
                pyautogui.moveTo(search_x, search_y, duration=0.5)
                pyautogui.click()
                time.sleep(1)
                
                # Type contact name
                pyautogui.write(contact, interval=0.1)
                time.sleep(2)
                
                # Click on the first result (assuming it's the correct contact)
                first_result_y = int(screen_height * 0.2)
                pyautogui.moveTo(search_x, first_result_y, duration=0.5)
                pyautogui.click()
                time.sleep(2)
                
                # Type message in the message box (typically at the bottom)
                message_y = int(screen_height * 0.9)
                pyautogui.moveTo(int(screen_width * 0.5), message_y, duration=0.5)
                pyautogui.click()
                time.sleep(1)
                
                # Type and send message
                pyautogui.write(message, interval=0.05)
                pyautogui.press('enter')
                
                self.action_history.append(f"Sent WhatsApp Web message to {contact}")
                print(f"Successfully sent WhatsApp Web message to {contact}")
                return True
                
        except Exception as e:
            print(f"Error sending WhatsApp message via web: {e}")
            return False 