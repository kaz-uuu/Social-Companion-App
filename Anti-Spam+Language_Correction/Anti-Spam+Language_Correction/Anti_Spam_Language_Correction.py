
#note: this script runs in the background, and only works on android dev
from jnius import autoclass


antispamservice = autoclass('org.kivy.android.antispamservice')
antispamservice.mService.setAutoRestartService(True)

while True:
    print("checking if whatsapp is open")
    
