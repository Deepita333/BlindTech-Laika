# BlindTech : Laika, virtual voice assistant

BlindTech is an AI-powered virtual assistant specifically designed for blind individuals, utilizing voice interaction and gesture recognition to create a personalized and accessible learning experience. By interpreting voice commands and recognizing gestures, the assistant can guide users through educational content, daily tasks, and more.

![WhatsApp Image 2024-06-30 at 6 34 51 AM](https://github.com/Shib-Sankar-Das/C-Programming/assets/136646947/af41385a-c1aa-46e9-8bc1-f6b45f7d6276)


## Features

1. *Voice Interaction: Customizable Voice Commands*
   - Users can set personalized commands for specific actions.
   
2. *Gesture Recognition: Touch-Free Navigation*
   - Allows users to navigate menus and interfaces without physical contact.
   
3. *Educational Content Accessibility: Interactive Learning Modules*
   - Provides audio-guided lessons and activities.
   
4. *Daily Task Assistance*
   - Voice commands to perform tasks like opening desktop applications and managing activities.

## Prerequisites

Before running the code, make sure you have the following dependencies installed:

- Python 3.x
- OpenCV: pip install opencv-python
- MediaPipe: pip install mediapipe
- PyAutoGUI: pip install pyautogui
- os
- re
- eel: pip install eel
- webbrowser
- pywhatkit: pip install pywhatkit
- time
- datetime
- pptsx3: pip install pptsx3
- mss: pip install mss
- pytesseract: pip install pytesseract
- numpy: pip install numpy
- speech_recognition: pip install SpeechRecognition

## How to Use

1. Clone this repository:
    sh
    git clone https://github.com/Deepita333/BlindTech-Laika.git
    
2. Navigate to the project directory:
    sh
    cd BlindTech-Laika
    
3. Run the code:
    sh
    python app.py
    

A window will open showing the webcam feed. Move your hand in front of the camera to control the cursor and perform gestures. To exit the program, press 'q' in the OpenCV window.

## Hand Gestures and Actions

### Left Hand (Mouse Control)

- Move your left hand to control the mouse cursor.
- When the index finger tip is above the index finger middle, it simulates a left mouse click.

### Right Hand (Keyboard Control)

- Move your right hand to control the keyboard.
- Swipe right or left to simulate arrow key presses ('right' or 'left').
- Swipe up or down to simulate arrow key presses ('up' or 'down').

## Cursor Actions

### Cursor Position Recognition

- When the user says to our voice assistant "tell me what is on my screen", the voice assistant says the cursor's nearby elements and hover element.

### Cursor Movement

- When the user says to our voice assistant "pointer to" followed by a location, the cursor moves to that location automatically.

## Screenshots and Videos



https://github.com/Shib-Sankar-Das/C-Programming/assets/136646947/aebfb827-5e96-4d0d-b2ed-524108fee6fa


##Authors:
Co-authored-by:Anushka Mukherjee <mukherjeeanushka376@gmail.com>
