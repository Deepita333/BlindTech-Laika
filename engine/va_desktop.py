import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import eel
import threading

engine = pyttsx3.init('sapi5')
vcs = engine.getProperty('voices')
engine.setProperty('voice', vcs[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
@eel.expose
def talk():
    hr = int(datetime.datetime.now().hour)
    if hr >= 0 and hr < 12:
        speak('Good morning!!')
    elif hr >= 12 and hr < 18:
        speak('Good afternoon')
    else:
        speak('Good evening/night')

    speak('Hello sir, Iam Laika how can I help you today?')

def inp_take():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query.lower()


@eel.expose
def allCommand():
    while True:
        query = inp_take()
        print(query)
        if "open" in query:
            from features import openCommand
            openCommand(query)
        elif "close" in query:
            from features import closeApplication
            closeApplication(query)
        elif "on youtube" in query:
            from features import playYoutube
            playYoutube(query)
        elif "shortcut" in query:
            from features import shortcut
            shortcut(query)
        elif "tell me what is on my screen" in query:
            from util import hover_text
            hover_text()
        elif "pointer to" in query:
            from util import process_voice_command
            process_voice_command(query)
        elif "stop hover" in query:
            from util import stop_hover
            stop_hover()

        else:
            print("Not run")
    

    
    
            
            
       
    
        

    
