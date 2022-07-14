
#note: this script runs in the background, and only works on android, mac or windows
from PIL import ImageGrab
import kivy #importing necessary libraries for OCR and screen recording
from kivy.utils import platform
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

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
desktoptemplates = [cv2.imread('assets/win_template_img.png', 0), cv2.imread('assets/win_template_typing_img.png', 0), cv2.imread('assets/macosx_template_idle_img.png', 0), cv2.imread('assets/macosx_template_img.png', 0)]
mobiletemplateimages = [cv2.imread('assets/android_template_idle_img.png'), cv2.imread('assets/android_template_typing.png'), cv2.imread('assets/android_textfield_template.png')]


didlaunchwhatsapp = False
messagecounter = 0 #counter for how many messages the user has sent in a short period of time

if __name__ == '__main__':


    while AntiSpamEnabled:
        #setup screen recording
        img = ImageGrab.grab(bbox=(0, 0, width, height)) #using PIllow to take an image of the user's screen
        img_np = np.array(img) #converts image to numpy array to be processed by opencv
        finalimg = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY) #converts image to RGB

        #Detect if whatsap is open
        imagechecked = finalimg.copy() # take a copy of the image from the screen recorder
        if platform == 'win' or platform == 'macosx': #if this script is being run on a desktop/laptop, get the width and height of the template image
            for template in desktoptemplates: 
                h, w = template.shape
                results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF_NORMED) #match templates for the copy of the image
                locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
        
        if platform == 'android':
            for template in mobiletemplateimages: 
                h, w = template.shape
                results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF_NORMED) #match templates for the copy of the image
                locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
        
        print(list(zip(*locations[::-1]))) 
        if (list(zip(*locations[::-1])) != []): #if there are matches of the template found in the orignal image
            didlaunchwhatsapp = True
            break
        if (list(zip(*locations[::-1])) == []):
            didlaunchwhatsapp = False
        print(didlaunchwhatsapp)
    
    while didlaunchwhatsapp == True:

        #if the user has whatsapp open and is typing, locate the textfield and begin OCR on the text being typed
        textfieldlocation = list(zip(*locations[::-1]))[0]
        textfieldimg = ImageGrab.grab(bbox=(textfieldlocation[0], textfieldlocation[1], textfieldlocation[0] + w, textfieldlocation[1] + h))
        textfieldimgnp = np.array(textfieldimg)
        textfieldimgnp = cv2.cvtColor(textfieldimgnp, cv2.COLOR_RGB2GRAY)
        textfieldimgnp = cv2.GaussianBlur(textfieldimgnp, (3, 3), 0) # change image captured from textfield to grayscale and blur out all nearby objects to maximise OCR accuracy
            
        messagestring = pytesseract.image_to_string(textfieldimgnp)
        print("message detected:{}".format(messagestring))
        if messagestring != "Type a message" or messagestring != "message":
            from language_corrector import language_Corrector
            #create an instance of the language corrrector and store the data from OCR for sentiment analysis
            LanguageCorrector = language_Corrector()
            LanguageCorrector.messagetyped = pytesseract.image_to_data(textfieldimgnp, output_type=pytesseract.Output.DICT)
            istyping = True

            #check if the user has finished typing a line:
            
            

            
        
        
            
        