from re import U
from tkinter import Image
from turtle import Screen, Turtle
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager, Screen
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from multiprocessing import Process
#from jnius import autoclass
import random
import speech_recognition
import pyttsx3
import threading
import time
import cv2 
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.android.antispamservice',
    servicename=u'antispam'
)



colors = {
    "Purple": {
        "200": "#6100FF",
        "500": "#6100FF",
        "700": "#6100FF",
    },
    "Red": {
        "200": "#C25554",
        "500": "#C25554",
        "700": "#C25554",
        "A700": "#C25554",
    },
    "Light": {
        "Background": "#FFFFFF",
        "StatusBar": "FFFFFF",
        "AppBar": "#F5F5F5",
    }
}

KV = '''
WindowManager:
    HomePage:
    TrainingPage:
    ResultsPage:

<HomePage>:
    name: 'home'
    MDScreen:
        MDRaisedButton:
            markup: True
            text: "[b]Start Training Scenario[/b]"
            on_release: app.loadTrainingPage()
            font_size:40
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .2}
        MDRaisedButton:
            text: "[b]Sign Language Translator[/b]"
            font_size: 40
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .13}
        MDLabel:
            markup: True
            font_size: 128
            text: '[b][color=#6100ff]Friend[/color]ly[/b]'
            pos_hint: {"center_x": .8, "center_y": .8}
            theme_text_color: "Custom"
            text_color: 97, 0, 255, 1 
            

<TrainingPage>:
    name: 'training'
    MDScreen:
        id: mdscreen
        BoxLayout:
            id: layout
            orientation: 'vertical'
            adaptive_size: True

        MDTopAppBar:
            title: "Training Simulator"
            pos_hint: {"center_y": 0.97}
        MDLabel:
            markup: True
            text: "[b]Scenario: Come Up With A Suitable Response![/b]"
            halign: 'center'
            pos_hint: {"center_y": 0.8}
        MDLabel:
            id: scenariolabel
            text: "Loading..."
            font_size: 60
            halign: 'center'
            pos_hint: {"center_y": .7}
        MDRaisedButton:
            id: recordbutton
            text: "Record Answer"
            on_release: app.voice2text()
            pos_hint: {"center_x": .5, "center_y": .3}

<ResultsPage>:
    name: 'results'
    MDScreen:
        MDTopAppBar:
            markup: True
            title: "[b]Results[/b]"
            pos_hint: {'center_y': .97}
        MDLabel:
            markup: True
            id: resultlabel
            text: "Loading..."
            halign: 'center'
            pos_hint: {'center_y': .6}
            font_size: 64

        MDLabel:
            id: emotionlabel
            text: "Loading..."
            halign: 'center'
            pos_hint: {'center_y': .4}
            font_size: 40
        MDRaisedButton:
            id: nextscenario
            text: "NEXT SCENARIO"
            on_release: app.root.current = 'training'
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .2}
        MDRaisedButton:
            id: homebutton
            text: "HOME PAGE"
            on_release: app.root.current = 'home'
            pos_hint: {"center_x": .5, "center_y": .2}
            font_size:40
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .13}
'''

class HomePage(Screen):
    pass

class TrainingPage(Screen):
    pass

class ResultsPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class trainingApp(MDApp): #this is the main training app that is going to be downloaded into the user's phone
    #add code for training app here, free to change name


    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.thread = None
        self.fps_monitor_start()
        Window.size = (450,975)
        self.toggle = False
        self.listen = False
        # self.image = Image()

        # layout.add_widget(self.image)
        # self.startListeningButton = MDRaisedButton(
        #     text="Click Here",
        #     pos_hint={'center_x': .5, 'center_y': .5},
        #     size_hint=(None,None))
        # self.startListeningButton.bind(on_press=self.recognizeSpeech)
        # layout.add_widget(self.startListeningButton)

        # self.capture = cv2.VideoCapture(1)
        # Clock.schedule_interval(self.load_video, 1.0/30.0)
        return Builder.load_string(KV)
    
    def loadTrainingPage(self):
        self.root.current = 'training'
        self.getPrompt()
        self.startcam()

    def startcam(self):
        self.image = Image()
        print("cam started")
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        self.root.get_screen('training').ids.layout.add_widget(self.image)
        
    def load(self):
        Clock.schedule_interval(self.load_video, 1.0/30.0)

    def load_video(self, *args):
        ret, frame = self.capture.read()
        #load frame
        self.image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture

    def voice2text(self):
        if self.toggle == False:
            self.toggle = True
            self.listen = True
            self.root.get_screen('training').ids.recordbutton.text = 'Press to stop recording and submit response'
            if not self.thread:
                print('[voice2text] starting thread')
                self.thread = threading.Thread(target=self.recognizeSpeech)  # function's name without ()
                self.thread.daemon = True  # kill thread at the end of program
                self.thread.start()
            else:
                print('[voice2text] thread is already running')
        elif self.listen == True: #submitted response
            print("Loading")
            self.listen = False
            self.thread = None
            self.loadResults()


    def recognizeSpeech(self, *args):
        while self.listen == True:
            self.answer = ""
            print("Starting Recording")
            recognizer = speech_recognition.Recognizer() #start recognizing speech
            print("speak anything")
            while self.listen:
                print("listening...")
                try:
                    with speech_recognition.Microphone() as mic:
                        recognizer.adjust_for_ambient_noise(mic,duration=1)
                        audio = recognizer.listen(mic)
                        text = recognizer.recognize_google(audio)
                        text = text.lower()
                        self.answer = self.answer + " " + text
                        print(self.answer)
                except speech_recognition.UnknownValueError:
                    recognizer = speech_recognition.Recognizer()
                    continue
            

    def loadResults(self):
        print('[gradePrompt] starting thread')
        self.thread = threading.Thread(target=self.gradePrompt)  # function's name without ()
        self.thread.daemon = True  # kill thread at the end of program
        self.thread.start()
        self.root.current = 'results'
        print("10")
        print("done")
        self.thread.join()
        self.root.get_screen('results').ids.resultlabel.text = self.result
        self.root.get_screen('results').ids.emotionlabel.text = "Emotion Detected: " + self.emotion
    
    def getPrompt(self): #pull random scenario from dictionary
        self.prompts = {
            "I recently got a job offer for my dream job!"
            :['admiration curiosity excitement joy caring optimism hopeful','neutral'],
            "My pet died yesterday."
            :['remorse caring surprise','neutral curiosity']
            }
        random_key = random.sample(self.prompts.keys(), 1)[0]
        self.currentprompt = random_key
        print(self.prompts[self.currentprompt])
        self.root.get_screen('training').ids.scenariolabel.text = random_key
        return random_key
    
    def gradePrompt(self):
        good = False
        okay = False  
        bad = False
        print(self.prompts[self.currentprompt])
        goodans = self.prompts[self.currentprompt][0].split()
        okans = self.prompts[self.currentprompt][1].split()
        print(goodans)
        print(okans)
        tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
        model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
        
        emotion = pipeline('sentiment-analysis',model='arpanghoshal/EmoRoBERTa')

        emotion_labels = emotion(self.answer)
        
        print(emotion_labels)
        
        self.emotion = emotion_labels[0]['label']

        print(self.emotion)

        if self.emotion in goodans:
            self.result = '[b]Great Answer![/b]'
        elif self.emotion in okans:
            self.result = '[b]Not Bad, Still Room To Improve![/b]'
        else:
            self.result = '[b]Needs Work![/b]'
        
    

    # def startantispam(self): #this function starts the antispam and language corrector as a background service
    #     antispamservice = autoclass(SERVICE_NAME)
    #     mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
    #     antispamservice.start(mActivity,'')
    #     return antispamservice

    #mainsim.recognizeSpeech()

if __name__=="__main__":
    app = trainingApp()
    app.run()



