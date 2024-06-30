import pyautogui
import cv2
import numpy as np
import pytesseract
import mss
import time
from va_desktop import speak
from config import ASSISTANT_NME
from va_desktop import *

# Configure tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def capture_screen():
    """Capture the screen in real time."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Use the first monitor
        screen = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
    return frame

def detect_hovered_feature(frame):
    """Detect the feature at the current mouse position using OCR."""
    x, y = pyautogui.position()
    # Define the region around the mouse position
    region = frame[max(0, y - 50):min(frame.shape[0], y + 50), max(0, x - 100):min(frame.shape[1], x + 100)]
    # Convert the region to grayscale
    gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    # Use OCR to extract text
    text = pytesseract.image_to_string(gray_region)
    return text.strip()


hover_active = True

def hover_text():
    global hover_active
    previous_hover_text = ""
    hover_active = True
    while hover_active:
        frame = capture_screen()
        hovered_text = detect_hovered_feature(frame)
        if hovered_text and hovered_text != previous_hover_text:
            speak(f"You are hovering over {hovered_text}")
            time.sleep(1)
            previous_hover_text = hovered_text
        time.sleep(2)
        allCommand()
    
    print("Hover text terminated")
    

def stop_hover():
    global hover_active
    hover_active = False

def move_cursor_to_text(target_text):
    """Move the cursor to the location of the specified text on the screen."""
    frame = capture_screen()
    # Convert the entire screen to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use OCR to get all text positions
    data = pytesseract.image_to_data(gray_frame, output_type=pytesseract.Output.DICT)
    
    for i, text in enumerate(data['text']):
        if text.strip().lower() == target_text.strip().lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            # Move the cursor to the center of the detected text region
            pyautogui.moveTo(x + w / 2, y + h / 2)
            speak(f"Cursor moved to {text}")
            return
    speak(f"Could not find the text {target_text} on the screen")

def hover_over_text(target_text):
    frame = capture_screen()
    # Convert the entire screen to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use OCR to get all text positions
    data = pytesseract.image_to_data(gray_frame, output_type=pytesseract.Output.DICT)
    
    for i, text in enumerate(data['text']):
        if text.strip().lower() == target_text.strip().lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            # Move the cursor to the center of the detected text region
            pyautogui.moveTo(x + w / 2, y + h / 2)
            # Hover over the text for a short duration
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            speak(f"Hovered over {text}")
            return
    speak(f"Could not find the text {target_text} on the screen")

def process_voice_command(command):
    if "pointer to" in command:
        target_text = command.replace("pointer to", "").strip()
        move_cursor_to_text(target_text)
    elif "hover over" in command:
        target_text = command.replace("hover over", "").strip()
        hover_over_text(target_text)
    elif "stop hover" in command:
        stop_hoverr()

def stop_hoverr():
    """Stop the hovering action."""
    pyautogui.mouseUp()
    speak("Hover stopped")


    

    


