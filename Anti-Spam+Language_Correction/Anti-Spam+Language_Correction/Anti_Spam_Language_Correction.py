
#note: this script runs in the background, and only works on android, mac or windows
from curses import window
from logging.config import listen
from multiprocessing.connection import Listener
from socket import timeout
from PIL import ImageGrab
import kivy #importing necessary libraries for OCR and screen recording
from kivy.utils import platform
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from threading import Event
AntiSpamEnabled = True #Check if the script has been enabled


if platform == 'win': #detect the platform that this script is being run on ,and set the width and height of the image to be captured accordingly.
    import pyautogui
    width, height = pyautogui.size() # pyautogui is used because it is meant for windows, so goes for tkinter and kivy.Window
if platform == 'macosx':
    from tkinter import Tk

    root = Tk()
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()

if platform == 'android':
    from kivy.core.window import Window
    width = Window.size(0)
    height = Window.size(1)

#reading template images from assets, desktop templates are best stored in an array since there are two of them.
desktoptemplates = [cv2.imread('assets/win_template_img.png', 0), cv2.imread('assets/win_template_typing_img.png', 0)]
mobiletemplateimages = [cv2.imread('assets/android_template_idle_img.png'), cv2.imread('assets/android_template_typing.png'), cv2.imread('assets/android_textfield_template.png')]
mactemplates = [cv2.imread('assets/macosx_template_idle_img.png', 0), cv2.imread('assets/macosx_template_img.png', 0)]


messagecounter = 0 #counter for how many messages the user has sent in a short period of time
messagestring = ""
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
                    locations = np.where(results >= 0.75)
            if platform == 'android':
                for template in mobiletemplateimages: 
                    h, w = template.shape
                    results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF_NORMED) #match templates for the copy of the image
                    locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
        
            if (list(zip(*locations[::-1])) != []): #if there are matches of the template found in the orignal image
                if platform == "win" or platform == "mac":
                    listener = keyboard.Listener(on_release=on_release)
                if platform == "android":
                    from AndroidKeyboardListener import keyboardlistener
                    listener = keyboardlistener()
                listener.daemon = True
                listener.start()
                listener.join()
            
            if (list(zip(*locations[::-1])) == []):
                didlaunchwhatsapp = False
            print(list(zip(*locations[::-1])))
def on_release(key):
    global messagestring
    if hasattr(key, 'char'):
        messagestring += key.char
    if key == keyboard.Key.backspace: 
        messagestring = messagestring[:-1]
    if key == keyboard.Key.space:
        messagestring += " "
    if key == keyboard.Key.enter or key == keyboard.Key.alt:
        return False
    print(messagestring)        
        
if __name__ == '__main__':
    from threading import Thread
    from threading import Event

    didlaunchwhatsapp = Event()
    
    

    screenrecorder = Thread(target=startscreenrecorder)
    screenrecorder.daemon = True   
    screenrecorder.start()
    screenrecorder.join()  


            
        
        
            
        