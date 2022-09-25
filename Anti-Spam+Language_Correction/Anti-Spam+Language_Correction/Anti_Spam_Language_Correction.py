
#note: this script runs in the background, and only works on android, mac or windows
import threading
from time import time
from tkinter import Tk
from types import NoneType
from PIL import ImageGrab
import kivy #importing necessary libraries for OCR and screen recording
from kivy.utils import platform
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from threading import Event, Timer
import keyboard as Keyboard
AntiSpamEnabled = True #Check if the script has been enabled



if platform == 'win': #detect the platform that this script is being run on ,and set the width and height of the image to be captured accordingly.
    import pyautogui
    width, height = pyautogui.size() # pyautogui is used because it is meant for windows, so goes for tkinter and kivy.Window
if platform == 'macosx':
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    print("width: {}, height: {}".format(width, height))

if platform == 'android':
    from kivy.core.window import Window
    width = Window.size(0)
    height = Window.size(1)

#reading template images from assets, desktop templates are best stored in an array since there are two of them.
desktoptemplates = [cv2.imread('assets/win_template_img.png', 0), cv2.imread('assets/win_template_typing_img.png', 0)]
mobiletemplateimages = [cv2.resize(cv2.imread('assets/android_template_idle_img.png'), (0, 0), fx=(width * 0.875), fy=(width * 0.875))]
mactemplates = [cv2.resize(cv2.imread('assets/macosx_template_img.png', 0), (0, 0), fx= (width / 2880), fy=(height / 1880))]
sendbuttontemplate = cv2.resize(cv2.imread('assets/android_send_button.png', 0), (0, 0), fx=(width * 0.125), fy=(width * 0.125))

messagecounter = 0 #counter for how many messages the user has sent in a short period of time
messagestring = ""
didFinishTimer = False
from pynput import keyboard
def startscreenrecorder():
        global didlaunchwhatsapp
        while AntiSpamEnabled:
            #setup screen recording
            img = ImageGrab.grab(bbox=(0, 0, width, height)) #using PIllow to take an image of the user's screen
            img_np = np.array(img) #converts image to numpy array to be processed by opencv
            finalimg = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY) #converts image to GrayScale

            #Detect if whatsap is open
            imagechecked = finalimg.copy() # take a copy of the image from the screen recorder
            if platform == 'win': #if this script is being run on a desktop/laptop, get the width and height of the template image
                for template in desktoptemplates: 
                    h, w = template.shape
                    results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF_NORMED) #match templates for the copy of the image
                    locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
            if platform == "macosx":
                for template in mactemplates:
                    
                    h,w = template.shape
                    results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF_NORMED)
                    locations = np.where(results >= 0.9)
            if platform == 'android':
                for template in mobiletemplateimages: 
                    h, w = template.shape
                    results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF_NORMED) #match templates for the copy of the image
                    locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
        
            if (list(zip(*locations[::-1])) != []): #if there are matches of the template found in the orignal image
                if platform == "win" or platform == "macosx":
                    listener = keyboard.Listener(on_release=on_release)
                if platform == "android":
                    from AndroidKeyboardListener import keyboardlistener
                    listener = keyboardlistener()
                    buttonresults = cv2.matchTemplate(imagechecked, sendbuttontemplate, cv2.TM_CCOEFF_NORMED)
                    buttonlocations = np.where(buttonresults > 0.8)
                    if (list(zip(*buttonlocations[::-1])) != []):
                        h, w = sendbuttontemplate.shape
                        bottom_right = (buttonlocations[0] + w, buttonlocations[1] + h)

                listener.daemon = True
                listener.start()
                listener.join()
                
            if (list(zip(*locations[::-1])) == []):
                didlaunchwhatsapp = False
                
def on_release(key):
    global messagestring
    if hasattr(key, 'char') and key.char != None:
        messagestring += key.char
    if key == keyboard.Key.backspace: 
        messagestring = messagestring[:-1]
    if key == keyboard.Key.space:
        messagestring += " "
    if key == keyboard.Key.enter:
        if platform == "macosx":

            import time
            timeleft = 10
            controller = keyboard.Controller()
            while timeleft:
                mins, sec = divmod(timeleft, 60)
                time.sleep(0.001)
                print("Second passed")
                controller.press(keyboard.Key.backspace)
                if timeleft <= 0:
                    break
                timeleft -= 0.001
                print("Timeleft: {}".format(timeleft))
        if platform == "win":
            import time
            timeleft = 10

            while timeleft:
                mins, sec = divmod(timeleft, 60)
                time.sleep(0.1)
                print("Second passed")
                Keyboard.block_key("ENTER")
                if timeleft <= 0:
                    break
                timeleft -= 0.1
                print("Timeleft: {}".format(timeleft))
            Keyboard.unblock_key("ENTER")
    print(messagestring)        
def releasekeyboard():
    global didFinishTimer
    didFinishTimer = True
if __name__ == '__main__':
    from threading import Thread
    from threading import Event

    didlaunchwhatsapp = Event()
    
    

    screenrecorder = Thread(target=startscreenrecorder)
    screenrecorder.daemon = True   
    screenrecorder.start()
    screenrecorder.join()  


            
        
        
            
        