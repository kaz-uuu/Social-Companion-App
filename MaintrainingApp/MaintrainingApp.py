##/ MISC PACKAGES /############################################################
import os
import time
import threading
import random
import threading
import numpy as np
import warnings
import cv2
#from jnius import autoclass

##/ KIVY PACKAGES /#############################################################
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton

##/ EMOTION RECOGNITION PACKAGES /################################################
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from multiprocessing import Process
import speech_recognition
import pyttsx3
import tensorflow
from keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array


##/ PACKAGE CONFIGURATIONS /###################################################
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = load_model("/Users/jerde/Downloads/Emotion-detection-main/best_model.h5")
face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.android.antispamservice',
    servicename=u'antispam'
)



colors = {
    "Purple": {
        "200": "#650DF2",
        "500": "#650DF2",
        "700": "#650DF2",
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
        Image:
            source: 'homepageimage.png'
            pos_hint: {'center_y': .5}
        MDRaisedButton:
            markup: True
            text: "[b]Start Training Scenario[/b]"
            on_release: app.loadTrainingPage()
            font_name: 'gothmedium'
            font_size:40
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .24}
        MDRaisedButton:
            text: "[b]Sign Language Translator[/b]"
            font_size: 40
            font_name: 'gothmedium'
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .17}
        MDLabel:
            markup: True
            font_name: "gothbold"
            font_size: 128
            text: '[color=#6100ff]Friend[/color]ly'
            halign: 'center'
            pos_hint: {"center_y": .9}
            theme_text_color: "Custom"
            text_color: 97, 0, 255, 1 
        MDLabel:
            text: 'Your Social Companion App'
            halign: 'center'
            pos_hint: {'center_y': .84}
            font_size: 45
            font_name: 'gothbold'
        MDLabel:
            text: 'Enable Anti-Spam Engine:              '
            font_size: 40
            font_name: 'gothmedium'
            halign: 'center'
            pos_hint: {'center_y': .1}
        MDSwitch:
            pos_hint: {'center_y': .1}
            on_active: app.antispam()



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
            font_name: 'gothbold'
        MDLabel:
            markup: True
            text: "[b]Scenario: Come Up With A Suitable Response![/b]"
            halign: 'center'
            pos_hint: {"center_y": 0.8}
            font_name: 'gothmedium'
        MDLabel:
            id: scenariolabel
            text: "Loading..."
            font_size: 60
            halign: 'center'
            pos_hint: {"center_y": .7}
            font_name: 'gothmedium'
        MDRaisedButton:
            id: recordbutton
            text: "Record Answer"
            on_release: app.voice2text()
            pos_hint: {"center_x": .5, "center_y": .3}
            font_name: 'gothmedium'

<ResultsPage>:
    name: 'results'
    MDScreen:
        MDTopAppBar:
            markup: True
            title: "Results"
            pos_hint: {'center_y': .97}
            font_name: 'gothbold'
        MDLabel:
            markup: True
            font_name: 'gothmedium'
            id: resultlabel
            text: "Loading..."
            halign: 'center'
            pos_hint: {'center_y': .6}
            font_size: 64

        MDLabel:
            id: emotionlabel
            font_name: 'gothmedium'
            text: "Loading..."
            halign: 'center'
            pos_hint: {'center_y': .4}
            font_size: 40
        MDRaisedButton:
            id: nextscenario
            text: "Next Scenario"
            font_name: 'gothmedium'
            font_size: 40
            on_release: app.root.current = 'training'
            size_hint: .7, .05
            pos_hint: {"center_x": .5, "center_y": .2}
        MDRaisedButton:
            id: homebutton
            text: "Home Page"
            font_name: 'gothmedium'
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
        self.firsttimeantispam = False
        self.thread = None
        self.startedcam = False
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
        if self.startedcam == False:
            self.startcam()

    def startcam(self):
        self.image = Image()
        print("cam started")
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.loadVideo, 1.0/30.0)
        self.root.get_screen('training').ids.layout.add_widget(self.image)
        self.startedcam = True
        
    def load_video(self, *args):
        ret, frame = self.capture.read()
        #load frame
        self.image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture

    def loadVideo(self, *args):
        ret, test_img = self.capture.read()  # captures frame and returns boolean value and captured image
    
        gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

        for (x, y, w, h) in faces_detected:
            cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
            roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
            roi_gray = cv2.resize(roi_gray, (224, 224))
            img_pixels = tensorflow.keras.utils.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255
            predictions = model.predict(img_pixels)
            # find max indexed array
            max_index = np.argmax(predictions[0])
            emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]
            cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        buffer = cv2.flip(test_img,0).tostring()
        texture = Texture.create(size=(test_img.shape[1],test_img.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture

    def voice2text(self):
        if self.toggle == False:
            self.toggle = True
            self.listen = True
            self.root.get_screen('training').ids.recordbutton.text = 'Press to stop recording and submit response'
            print('[voice2text] starting thread')
            self.thread = threading.Thread(target=self.recognizeSpeech)  # function's name without ()
            self.thread.daemon = True  # kill thread at the end of program
            self.thread.start()
        elif self.listen == True: #submitted response
            print("Loading")
            self.listen = False
            self.thread = None
            self.toggle = False
            self.root.get_screen('training').ids.recordbutton.text = 'Press to record response'
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
                        print('listening...')
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
        if self.result == 'not detected':
            self.root.get_screen('results').ids.resultlabel.text = 'No input was recognized. Please try again.'
            self.root.get_screen('results').ids.emotionlabel.text = ''
        else:
            self.root.get_screen('results').ids.resultlabel.text = self.result
            self.root.get_screen('results').ids.emotionlabel.text = "Emotion Detected: " + self.emotion
    
    def getPrompt(self): #pull random scenario from dictionary
        self.prompts = {
            "I recently got a job offer for my dream job!"
            :['admiration curiosity excitement joy caring optimism hopeful','neutral'],
            "My pet died yesterday."
            :['remorse caring surprise','neutral curiosity'],
            "I am going to Australia for a two week holiday!"
            :['caring curiousity optimism admiration approval','desire']
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
        if not self.emotion:
            self.result = 'not detected'
        elif self.emotion in goodans:
            self.result = '[b]Great Answer![/b]'
        elif self.emotion in okans:
            self.result = '[b]Not Bad, Still Room To Improve![/b]'
        else:
            self.result = '[b]Needs Work![/b]'
    def antispam(self):
        if self.firsttimeantispam == False:
            snackbar = Snackbar(
                text="This is a snackbar!",
                snackbar_x="10dp",
                snackbar_y="10dp",
            )
            snackbar.size_hint_x = (
                Window.width - (snackbar.snackbar_x * 2)
            ) / Window.width
            snackbar.buttons = [
                MDFlatButton(
                    text="UPDATE",
                    text_color=(1, 1, 1, 1),
                    on_release=snackbar.dismiss,
                ),
                MDFlatButton(
                    text="CANCEL",
                    text_color=(1, 1, 1, 1),
                    on_release=snackbar.dismiss,
                ),
            ]
            snackbar.open()
            self.firsttimeantispam = True
    

    # def startantispam(self): #this function starts the antispam and language corrector as a background service
    #     antispamservice = autoclass(SERVICE_NAME)
    #     mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
    #     antispamservice.start(mActivity,'')
    #     return antispamservice

    #mainsim.recognizeSpeech()

LabelBase.register(name='gothbold', fn_regular='GothamBold.otf')
LabelBase.register(name='gothmedium', fn_regular='GothamMedium.ttf')


if __name__=="__main__":
    app = trainingApp()
    app.run()


