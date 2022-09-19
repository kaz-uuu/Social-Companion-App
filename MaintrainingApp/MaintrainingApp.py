from email.mime import image
from re import U
from tkinter import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
#from jnius import autoclass
import speech_recognition
import pyttsx3
import cv2 



SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.android.antispamservice',
    servicename=u'antispam'
)

class trainingApp(MDApp): #this is the main training app that is going to be downloaded into the user's phone
    #add code for training app here, free to change name

    def build(self):
        layout = MDBoxLayout(orientation="vertical")
        self.image = Image()
        layout.add_widget(self.image)
        self.startListeningButton = MDRaisedButton(
            text="Click Here",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None,None))
        self.startListeningButton.bind(on_press=self.recognizeSpeech)
        layout.add_widget(self.startListeningButton)

        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        return layout
    
    def load_video(self, *args):
        ret, frame = self.capture.read()
        #load frame
        self.image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture

    def recognizeSpeech(self):
        self.listen = True
        print("Starting Recording")
        recognizer = speech_recognition.Recognizer() #start recognizing speech
        print("speak anything")
        while self.listen:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=1)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(text)       
    
    def stopSpeech(self):
        self.listen = False
                
    
    def startantispam(self): #this function starts the antispam and language corrector as a background service
        antispamservice = autoclass(SERVICE_NAME)
        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        antispamservice.start(mActivity,'')
        return antispamservice

    #mainsim.recognizeSpeech()

if __name__=="__main__":
    app = trainingApp()
    app.run()

