from re import U
from tkinter import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
#from jnius import autoclass
import speech_recognition
import pyttsx3
import cv2 
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')

emotion_labels = emotion("oh im sorry to hear that")
print(emotion_labels)

SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.android.antispamservice',
    servicename=u'antispam'
)


KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Training Scenarios"
        MDRaisedButton:
            id: togglebutton
            text: "Start Listening"
            on_press: app.recognizeSpeech()
'''

class trainingApp(MDApp): #this is the main training app that is going to be downloaded into the user's phone
    #add code for training app here, free to change name


    def build(self):
        self.fps_monitor_start()
        Window.size = (450,975)
        layout = MDBoxLayout(orientation="vertical")
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
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
        return Builder.load_string(KV)
    

    def load_video(self, *args):
        ret, frame = self.capture.read()
        #load frame
        self.image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture


    def recognizeSpeech(self, *args):
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

