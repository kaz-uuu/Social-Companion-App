
#note: this script runs in the background, and only works on android dev
from jnius import autoclass
from PIL import ImageGrab
from kivy.core.window import Window
import numpy as np
import cv2

antispamservice = autoclass('org.kivy.android.antispamservice')
antispamservice.mService.setAutoRestartService(True)

while True:
    print("checking if whatsapp is open")
    print(Window.size)
