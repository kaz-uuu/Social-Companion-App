
#note: this script runs in the background, and only works on android dev
from curses import window
from typing import final
from PIL import ImageGrab
from kivy.core.window import Window
import numpy as np
import cv2

width = Window.size[0]
height = Window.size[1]

if __name__ == '__main__':
    while True:
        #setup OCR and check if whatsapp is open
        print("checking if whatsapp is open")
        img = ImageGrab.grab(bbox=(0, 0, width, height))
        img_np = np.array(img)
        finalimg = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.namedWindow("Not OBS")
        cv2.imshow("Not OBS", finalimg)
        
        