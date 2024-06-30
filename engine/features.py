import re
import webbrowser
import eel
import os
import pywhatkit as kit
import pyautogui
import time

from va_desktop import speak
from config import ASSISTANT_NME

def openCommand(query):
    website_dict = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "github": "https://www.github.com",
    "spotify": "https://www.spotify.com",
    "instagram" : "https://www.instagram.com",
    "chatgpt":"https://www.chatgpt.com"
}
    
    if "open" in query:
        query = query.replace(ASSISTANT_NME, "")
        query = query.replace("open", "")
        query = query.lower().strip()
        try:
            speak("Opening " + query)
            pyautogui.press('win')
            time.sleep(0.3)
            pyautogui.write(query)
            time.sleep(0.3)
            pyautogui.press('enter')
        except Exception as e:
            speak("Something went wrong")
            print(e)
    elif "website" in query:
        itm= query.replace(ASSISTANT_NME, "")
        itm = query.replace("open website", "")
        itm = query.lower().strip()
        try:
            if itm in website_dict:
                    url = website_dict[itm]
                    speak(f"Opening website: {url}")
                    webbrowser.open(url)
            else:
                speak("Opening " + itm)
                pyautogui.press('win')
                pyautogui.write(itm)
                pyautogui.press('enter')
                
        except Exception as e:
            speak("Something went wrong")
            print(e)
            
def closeApplication(query):
    query = query.replace(ASSISTANT_NME, "").replace("close", "").strip().lower()
    speak(f"Attempting to close {query}")

    try:
        # Open Task Manager
        pyautogui.hotkey('ctrl', 'shift', 'esc')
        time.sleep(1)

        # Search for the application in Task Manager
        pyautogui.press('tab', presses=3, interval=0.1)
        pyautogui.typewrite(query)
        time.sleep(1)

        # Navigate to the application
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('delete')
        time.sleep(0.5)
        pyautogui.press('enter')

        speak(f"{query} closed successfully.")
    except Exception as e:
        speak("Something went wrong while closing the application.")
        print(e)
    
        
def playYoutube(query):
    search_term=extract_yt_term(query)
    speak("playing"+search_term+"on Youtube")
    kit.playonyt(search_term)
    
        

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None




def shortcut(query):
    application_shortcuts = {
    "file explorer": "win+e",
    "calculator": "win+q and type calculator",
    "notepad": "win+q and type notepad",
    "command prompt": "win+r and type cmd"}
    
    shortcuts_dict = {
    "copy": "ctrl+c",
    "paste": "ctrl+v",
    "print": "ctrl+p",
    "cut": "ctrl+x",
    "undo": "ctrl+z",
    "redo": "ctrl+y",
    "select all": "ctrl+a",
    "save": "ctrl+s",
    "find": "ctrl+f"}
    
    parts = query.split("shortcut for ", 1)
    if len(parts) > 1:
        shortcut_name = parts[1].strip()
        print(f"Shortcut name: {shortcut_name}")
        if shortcut_name in shortcuts_dict:
            speak(f"The shortcut for {shortcut_name} is {shortcuts_dict[shortcut_name]}")
        elif shortcut_name in application_shortcuts:
            speak(f"The shortcut for {shortcut_name} is {application_shortcuts[shortcut_name]}")
                        
        else:
            speak("Sorry, I don't know that shortcut.")
    else:
        speak("Sorry, I didn't understand which shortcut you want.")

    