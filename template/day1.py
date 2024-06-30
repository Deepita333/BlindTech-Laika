import speech_recognition as sr
import pyttsx3
import cv2
import mediapipe as mp
import threading
import time
import eel
import os

# Initialize Eel with the directory containing the web files
eel.init('www')
os.system('start chrome.exe --app="http://localhost:8000/index.html"')

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speech rate for better clarity

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."
        except sr.WaitTimeoutError:
            return "Timeout. Please try again."

# Gesture Recognition Setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

gesture_detected = False

def detect_gesture(image):
    global gesture_detected
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            y_coords = [landmark.y for landmark in hand_landmarks.landmark]
            if min(y_coords) < 0.2:  # Example condition for raised hand
                gesture_detected = True
    return image


def gesture_recognition():
    global gesture_detected
    gesture_detected = False
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera index out of range or not accessible.")
        return
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        frame = detect_gesture(frame)
        cv2.imshow('Gesture Recognition', frame)
        if gesture_detected:
            print("Gesture detected")
            break
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def talk_bbg():
    speak("Hey, I am Laika, your computer tutor! Welcome to the course.")
    speak("If you can hear me, raise your hand.")
    
@eel.expose
def lesson():
    global gesture_detected
    speak("Hey, I am Laika, your computer tutor! Welcome to the course.")
    speak("If you can hear me, raise your hand.")
    
    # Start gesture recognition in a separate thread
    gesture_thread = threading.Thread(target=gesture_recognition)
    gesture_thread.start()
    
    # Start listening for response
    response = listen()
    
    # Wait for gesture thread to complete
    gesture_thread.join()

    if gesture_detected:
        speak("Great! Let's start with today's lesson.")
    else:
        speak("I couldn't detect your gesture. Let's start anyway.")

    # Course details
    course_details = [
        "Our world is made up of wonderful things.",
        "Some things are natural and some are man-made. Things like ships, swings, and chairs are man-made things.",
        "Man-made things are made by humans. Machines are man-made. They make our work easy and save our precious time.",
        "We use many machines at home. Some machines need electricity to work and some do not.",
        "A COMPUTER is a man-made machine used to store information, draw pictures, write letters, do sums, listen to music, play games, and much more.",
        "A desktop computer is kept in one place. It is not moved around much.",
        "A laptop is a computer that we can carry anywhere.",
        "A computer is a very useful machine. It helps us do many things.",
        "Using a computer, we can perform various tasks.",
        "Computers are used in different places for different kinds of work.",
        "At home: You can do your homework and projects using a computer. You can use it to write letters and to play games.",
        "At hospitals: Computers keep track of patients and medical information.",
        "At airports: Computers help in keeping records of all the passengers.",
        "At banks: Computers are used for keeping records of account holders.",
        "At schools: Computers are used for teaching.",
        "At railways: Computers help in giving information about ticket reservations and bookings."
    ]
    
    for detail in course_details:
        speak(detail)
        time.sleep(2)  # Pause to give time to comprehend

    speak("If you understand, say yes or raise your hand.")
    
    response = listen()
    if 'yes' in response or gesture_detected:
        speak("Great! Let's move on to the next topic.")
    else:
        speak("I'm sorry, I didn't get that. Please try again.")

    # Wait for gesture thread to complete or user to raise hand again
    gesture_thread = threading.Thread(target=gesture_recognition)
    gesture_thread.start()
    gesture_thread.join()

    if gesture_detected:
        speak("You raised your hand. See you the next day where we will learn more about computers!!")
    else:
        speak("I couldn't detect your gesture. Let's continue anyway.")

if __name__ == "__main__":
    eel.start("index.html", mode=None, host='localhost', block=True)
