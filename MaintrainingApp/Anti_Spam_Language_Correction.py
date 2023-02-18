
#note: this script runs in the background, and only works on mac or windows
import threading
from time import time
from screeninfo import get_monitors
from urllib.parse import urlencode
from PIL import ImageGrab
import kivy #importing necessary libraries for OCR and screen recording
from kivy.utils import platform
import numpy as np
import cv2
from threading import Event
import keyboard as Keyboard
import pyautogui
from pynput import keyboard
import imutils
AntiSpamEnabled = True #Check if the script has been enable
didlaunchwhatsapp = False
def startscreenrecorder():
        global didlaunchwhatsapp
        while AntiSpamEnabled:
            #setup screen recording
            if platform == 'win': #detect the platform that this script is being run on ,and set the width and height of the image to be captured accordingly.
                width, height = pyautogui.size() # pyautogui is used because it is meant for windows
                print("width: {}, height: {}".format(width, height))
                desktoptemplates = [cv2.imread('assets/win_template_img.png', 0), cv2.imread('assets/win_template_typing_img.png', 0)]
            if platform == 'macosx':
                screen = get_monitors()[0]
                width = screen.width
                height = screen.height
                print("width: {}, height: {}".format(width, height)) # intermittent print statement for debugging
                mactemplates = [cv2.imread('macosx_template_img.png', 0)] #reading the template image for mac from the assets file using opencv, and resize the image to fit the actual dimensions on the screen(2880 x 1880)

            #android is still a work in progress, not ready yet
            if platform == 'android':
                from kivy.core.window import Window
                width = Window.size(0)
                height = Window.size(1)
                mobiletemplateimages = [cv2.resize(cv2.imread('assets/android_template_idle_img.png'), (0, 0), fx=(width * 0.875), fy=(width * 0.875))]
                sendbuttontemplate = cv2.resize(cv2.imread('assets/android_send_button.png', 0), (0, 0), fx=(width * 0.125), fy=(width * 0.125))
            #reading template images from assets, desktop templates are best stored in an array since there are two of them.


            messagecounter = 0 #counter for how many messages the user has sent in a short period of time
            messagestring = "" #string varaible to store what message the user is typing in whatsapp
            didFinishTimer = False #status variables to store 
            didtypemessage = False
            from pynput import keyboard
            img = ImageGrab.grab(bbox=(0, 0, width, height)) #using PIllow to take an image of the user's screen
            img_np = np.array(img) #converts image to numpy array to be processed by opencv
            finalimg = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY) #converts image to GrayScale

            #Detect if whatsap is open
            imagechecked = finalimg.copy() # take a copy of the image from the screen recorder
            if platform == 'win': #if this script is being run on a desktop/laptop, get the width and height of the template image
                for template in desktoptemplates: 
                    template = cv2.Canny(template, 50, 200)
                    h, w = template.shape
                    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                        resized = imutils.resize(imagechecked, width=int(imagechecked.shape[1] * scale))
                        r = imagechecked.shape[1] / float(resized.shape[1])

                        if resized.shape[0] < h or resized.shape[1] < w:
                            break
                        edged = cv2.Canny(resized, 50, 200)
                        results = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED) #match templates for the copy of the image, TM_CCOEFFF_NORMED is the algorithm of choice as it has been tested by me to be the most reliable 
                        locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
            if platform == "macosx":
                for template in mactemplates:
                    template = cv2.Canny(template, 50, 200)
                    h,w = template.shape[:2] #getting the height and width of the template that currently being checked for based off their "shape" property
                    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                        resized = imutils.resize(imagechecked, width = int(imagechecked.shape[1] * scale))
                        r = imagechecked.shape[1] / float(resized.shape[1])

                        if resized.shape[0] < h or resized.shape[1] < w:
                            break
                        edged = cv2.Canny(resized, 50, 200)
                        results = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF) #use template matching to check for a copy of the template image within the screenshot of the user's screen
                        locations = np.where(results >= 0.75) #getting the coordinates of the matches with a confidence score greater than equals to 0.9
            #android is still a work in progress
            if platform == 'android':
                for template in mobiletemplateimages: 
                    h, w = template.shape
                    results = cv2.matchTemplate(imagechecked, template, cv2.TM_CCOEFF) #match templates for the copy of the image
                    locations = np.where(results >= 0.75) # threshold is used so as to ensure that detection is accurate.
        
            if (list(zip(*locations[::-1])) != []): #if there are matches of the template found in the orignal image
                print("Whatsapp detected")
                if platform == "win" or platform == "macosx":
                    listener = keyboard.Listener(on_release=on_release) #start a keylogger on a seperate thread to track what the user is typing, and if he has sent a message etc
                #android is still a work in progress
                if platform == "android":
                    from AndroidKeyboardListener import keyboardlistener
                    listener = keyboardlistener()
                    buttonresults = cv2.matchTemplate(imagechecked, sendbuttontemplate, cv2.TM_CCOEFF_NORMED)
                    buttonlocations = np.where(buttonresults > 0.8)
                    if (list(zip(*buttonlocations[::-1])) != []):
                        h, w = sendbuttontemplate.shape
                        textfieldbox = ImageGrab.grab(bbox=(buttonlocations[0] + w, buttonlocations[1] + h, (width * 0.87), h))
                        textfieldnp = np.array(textfieldbox)
                        finaltxtfieldimg = cv2.cvtColor(textfieldnp, cv2.COLOR_BGR2RGB)
                        messagestring = pytesseract.image_to_string(finaltxtfieldimg)
                        if messagestring != "|Message" or messagestring != "Message":
                            didtypemessage = True
                        if (messagestring == "|Message" or messagestring == "Message") and didtypemessage:
                            didtypemessage = False
                            import time
                            timeleft = 10
                            while timeleft:
                                time.sleep(0.1)
                                if timeleft <= 0:

                                    break
                                timeleft -= 0.1
                        
                #start and join the keyboard listener thread        
                listener.daemon = True
                listener.start()
                listener.join()
                
            if (list(zip(*locations[::-1])) == []):
                didlaunchwhatsapp = False
#function to execute when a key is pressed and released(when a new letter is pressed)
def on_release(key):
    #global messagestring #set the messagestring and didlaucnhwhatsapp variables as global variables to access them from inside the function
    global didlaunchwhatsapp

    # #This is to update the messagestring variable according to what the user would have typed in the whatsapp 
    # if hasattr(key, 'char') and key.char != None: #if the key pressed is a character
    #     messagestring += key.char #add the character pressed into the entire message string variable
    # if key == keyboard.Key.backspace: #if the user pressed backspace
    #     messagestring = messagestring[:-1]#remove the last character from the messagestring
    # if key == keyboard.Key.space: #if the user pressed space
    #     messagestring += " "#add a space to the messagestring
    if key == keyboard.Key.enter:
        #if the user has pressed the enter key
        if platform == "macosx":

            import time
            timeleft = 10#set the timeleft on the timer in seconds to 10
            controller = keyboard.Controller() #Starting a keyboard controller object to delete any key the user presses during that 10 seconds
            while timeleft:
                time.sleep(0.001)#sleep for 0.001 seconds
                print("Second passed")
                controller.press(keyboard.Key.backspace)#every 1 milisecond press the backspace key to prevent the user from sending 
                if timeleft <= 0: #if the time left is up, break out the loop, and set the status variable didFinishTimer to true
                    global didFinishTimer
                    didFinishTimer = True
                    break
                timeleft -= 0.001 #remove 1 milisecond from the time varaible
                print("Timeleft: {}".format(timeleft))
        if platform == "win":
            #for windows, the "hook" function fo the keyboard module is not blocekd, so we can use that to stop the enter key from being pressed
            import time
            timeleft = 10

            while timeleft:
                time.sleep(0.1)
                Keyboard.hook_key("ENTER", lambda e: False, suppress=True) #while the 10 second timer is still active, use the hook function to suppress any inputs from the Enter key(block the enter key)
                if timeleft <= 0:
                    Keyboard.unhook_all() #unhook the enter key and allow the user to send messages again
                    break
                timeleft -= 0.1 #remove 0.1 seconds from the timer variable
    
    

    if not didlaunchwhatsapp: #stop the thread if whatsapp isn't detected
        return False

#function for checking the message for toxicity, still work in progress

    
    
if __name__ == '__main__':
    from threading import Thread
    from threading import Event

    didlaunchwhatsapp = Event()
    
    

    screenrecorder = Thread(target=startscreenrecorder)
    screenrecorder.daemon = True   
    screenrecorder.start()
    screenrecorder.join()  


            
        
        
            
        