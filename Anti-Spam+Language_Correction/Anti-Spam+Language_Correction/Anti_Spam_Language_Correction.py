
#note: this script runs in the background, and only works on android, mac or windows
from PIL import ImageGrab
import kivy #importing necessary libraries for OCR and screen recording
from kivy.utils import platform
import numpy as np
import cv2
import pytesseract

if platform == 'win':
    import pyautogui
    width, height = pyautogui.size()
if platform == 'macosx':
    from tkinter import Tk

    root = Tk()
    height = root.winfo_screenheight()
    wdith = root.winfo_screenwidth()

if platform == 'android':
    from kivy.core.window import Window
    width = Window.size(0)
    height = Window.size(1)


testimage = cv2.imread('assets/testimage.png', 0)
desktoptemplateimage = cv2.imread('assets/win_template_img.png', 0) #load all template images from assets folder in greyscale
mobiletemplateimage = cv2.imread('assets/android_light_template_img.png', 0)   

didlaunchwhatsapp = False

if __name__ == '__main__':
    while True:
        #setup screen recording
        img = ImageGrab.grab(bbox=(0, 0, width, height)) #using PIllow to take an image of the user's screen
        img_np = np.array(img) #converts image to numpy array to be processed by opencv
        finalimg = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY) #converts image to RGB

        #OCR
        if platform == 'win' or platform == 'macosx':
            
            h, w = desktoptemplateimage.shape
        if platform == 'android':
            h, w = mobiletemplateimage.shape
        
        imagechecked = finalimg.copy()
        result = cv2.matchTemplate(imagechecked, desktoptemplateimage, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.8)
        print(list(zip(*locations[::-1])))
        if list(zip(*locations[::-1])).count > 0:
            didlaunchwhatsapp = True
        
        