import os
import eel
from va_desktop import *
#from main1 import start_gesture_recognition


eel.init("template")

os.system('start chrome.exe --app="http://localhost:8000/index.html"')


eel.start("index.html",mode=None,host='localhost',block=True)  