
#note: this script runs in the background, and only works on android dev
from PIL import ImageGrab
from kivy.core.window import Window
import numpy as np
import cv2

if __name__ == '__main__':
    while True:
        #setup OCR and check if whatsapp is open
        print("checking if whatsapp is open")
