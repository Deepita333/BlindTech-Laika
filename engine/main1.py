import cv2
import mediapipe as mp
import pyautogui
import pyttsx3
import eel
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to provide voice guidance
def voice_guide(message):
    engine.say(message)
    engine.runAndWait()

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Open webcam
cap = cv2.VideoCapture(0)
prev_x = None
prev_y = None

'''
# Voice guidance instructions
voice_guide("Left Hand Mouse Control: Move your left hand to control the mouse cursor. "
            "When the index finger tip is above the index finger middle, it simulates a left mouse click.")
voice_guide("Right Hand Keyboard Control: Move your right hand to control the keyboard. "
            "Swipe right or left to simulate arrow key presses right or left. "
            "Swipe up or down to simulate arrow key presses up or down.")
'''

@eel.expose
def start_gesture_recognition():
    global prev_x, prev_y
    while cap.isOpened():
        ret, frame = cap.read()

        # Mirror image
        frame = cv2.flip(frame, 1)

        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Check handedness
                handedness = results.multi_handedness[results.multi_hand_landmarks.index(landmarks)].classification[0].label

                # Draw landmarks
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_mid = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

                if handedness == "Left":  # Mouse control
                    mcp_x = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                    mcp_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

                    cursor_x = int(mcp_x * screen_width)
                    cursor_y = int(mcp_y * screen_height)

                    pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

                    if index_tip.y >= index_mid.y:
                        pyautogui.click()

                elif handedness == "Right":  # Keyboard control
                    x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
                    if prev_x is not None and prev_y is not None:
                        dx = x - prev_x
                        dy = y - prev_y

                        if abs(dx) > abs(dy):
                            if dx > 50:  # Right swipe
                                pyautogui.press('right')
                            elif dx < -50:  # Left swipe
                                pyautogui.press('left')
                        else:  # Vertical swipe
                            if dy > 50:  # Down swipe
                                pyautogui.press('down')
                            elif dy < -50:  # Up swipe
                                pyautogui.press('up')

                    prev_x = x
                    prev_y = y

        
        cv2.imshow("Gesture Recognition", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

start_gesture_recognition()