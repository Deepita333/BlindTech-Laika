import re
import webbrowser
import os
import pywhatkit as kit
import pyautogui
import time
import subprocess

# Assuming these are custom modules from your project
from va_desktop import speak
from config import ASSISTANT_NME

def openCommand(query):
    """Opens applications or websites based on the user's query."""
    website_dict = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "github": "https://www.github.com",
        "spotify": "https://www.spotify.com",
        "instagram": "https://www.instagram.com",
        "chatgpt": "https://www.chatgpt.com"
    }
    
    if "open" in query and "website" not in query:
        # Handle opening local applications
        app_name = query.replace(ASSISTANT_NME, "").replace("open", "").lower().strip()
        try:
            speak(f"Opening {app_name}")
            pyautogui.press('win')
            time.sleep(0.3)
            pyautogui.write(app_name)
            time.sleep(0.3)
            pyautogui.press('enter')
        except Exception as e:
            speak("Sorry, something went wrong while trying to open the application.")
            print(f"Error in openCommand: {e}")

    elif "website" in query:
        # Handle opening websites
        site_name = query.replace(ASSISTANT_NME, "").replace("open website", "").lower().strip()
        try:
            if site_name in website_dict:
                url = website_dict[site_name]
                speak(f"Opening website: {url}")
                webbrowser.open(url)
            else:
                speak(f"I don't have a specific URL for {site_name}, but I will search for it.")
                kit.search(site_name)
        except Exception as e:
            speak("Sorry, something went wrong while trying to open the website.")
            print(f"Error in openCommand (website): {e}")
            
def closeApplication(query):
    """Closes a running application using the taskkill command for reliability."""
    app_name_query = query.replace(ASSISTANT_NME, "").replace("close", "").strip().lower()

    # Dictionary to map common names to their executable process names
    app_process_map = {
        "visual studio code": "Code.exe",
        "vscode": "Code.exe",
        "command prompt": "cmd.exe",
        "google chrome": "chrome.exe",
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe", # For Windows 10/11 calculator
        "file explorer": "explorer.exe" # Warning: closing this restarts the Windows shell
    }

    process_name = app_process_map.get(app_name_query)

    # If the app name is not in our map, we'll guess the process name
    if not process_name:
        # Remove spaces and add .exe as a fallback
        process_name = f"{app_name_query.replace(' ', '')}.exe"

    speak(f"Attempting to close {app_name_query}")

    try:
        # The 'taskkill' command is a robust way to close applications on Windows
        # /f: Forcefully terminate the process
        # /im: Specify the image name (process name) of the process to be terminated
        # We capture output to prevent messages from printing to the console and to check for errors
        result = subprocess.run(
            ["taskkill", "/f", "/im", process_name],
            check=True,
            capture_output=True,
            text=True
        )
        speak(f"{app_name_query} closed successfully.")

    except FileNotFoundError:
        # This error occurs if 'taskkill' command itself is not found (highly unlikely on Windows)
        speak("I couldn't find the 'taskkill' command. This feature may not work on your system.")
    except subprocess.CalledProcessError as e:
        # This error occurs if taskkill fails, for example, if the process isn't running.
        if "process not found" in e.stderr.lower():
            speak(f"Sorry, I could not find the application '{app_name_query}' running.")
        else:
            speak(f"Failed to close {app_name_query}. It might require administrative privileges.")
            print(f"Error: {e.stderr}")
    except Exception as e:
        speak("An unexpected error occurred while trying to close the application.")
        print(f"An unexpected error in closeApplication: {e}")
    
def playYoutube(query):
    """Extracts a search term and plays the corresponding video on YouTube."""
    search_term = extract_yt_term(query)
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I didn't catch what you want to play.")

def extract_yt_term(command):
    """Extracts the search term from a 'play on youtube' command using regex."""
    # Define a regular expression pattern to capture the content between 'play' and 'on youtube'
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else None

def shortcut(query):
    """Provides keyboard shortcuts for common commands and applications."""
    application_shortcuts = {
        "file explorer": "Windows key plus E",
        "calculator": "press the Windows key and type calculator",
        "notepad": "press the Windows key and type notepad",
        "command prompt": "press the Windows key, type cmd, and press enter"
    }
    
    shortcuts_dict = {
        "copy": "control plus C",
        "paste": "control plus V",
        "print": "control plus P",
        "cut": "control plus X",
        "undo": "control plus Z",
        "redo": "control plus Y",
        "select all": "control plus A",
        "save": "control plus S",
        "find": "control plus F"
    }
    
    parts = query.lower().split("shortcut for ", 1)
    if len(parts) > 1:
        shortcut_name = parts[1].strip()
        if shortcut_name in shortcuts_dict:
            speak(f"The shortcut for {shortcut_name} is {shortcuts_dict[shortcut_name]}")
        elif shortcut_name in application_shortcuts:
            speak(f"To open {shortcut_name}, you can use this shortcut: {application_shortcuts[shortcut_name]}")
        else:
            speak(f"Sorry, I don't know the shortcut for {shortcut_name}.")
    else:
        speak("Sorry, I didn't understand which shortcut you're asking for.")
