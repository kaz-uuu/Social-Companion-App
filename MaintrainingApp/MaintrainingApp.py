##/ MISC PACKAGES /############################################################
import os
import time
import threading
import random
import threading
import numpy as np
import warnings
import cv2
import csv
import argparse
import copy
import itertools
from collections import deque 
from collections import Counter
import mediapipe as mp
from Anti_Spam_Language_Correction import AntiSpamEnabled
from Anti_Spam_Language_Correction import startscreenrecorder
#from Anti_Spam_Language_Correction import on_release
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
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import NoTransition
from kivy.uix.dropdown import DropDown
from kivyoav.delayed import delayable 

##/ EMOTION RECOGNITION PACKAGES /################################################
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
import speech_recognition
import pyttsx3
import tensorflow
from keras.models import load_model
from keras.utils import load_img, img_to_array

##/ SIGN LANGUAGES PACKAGES /################################################
import signlanguage.app as app
import signlanguage.keypoint as keypoint
from signlanguage.utils.cvfpscalc import CvFpsCalc
from signlanguage.model.keypoint_classifier.keypoint_classifier import KeyPointClassifier



##/ PACKAGE CONFIGURATION /#####################################################
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = load_model("best_model.h5")
face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
#    packagename=u'org.kivy.android.antispamservice',
#    servicename=u'antispam'
#)


##/ COLORS USED BY KIVY /#############################################################
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

##/ KIVY UI CODE /#############################################################
KV = '''
WindowManager:
    SettingPage:
    HomePage:
    TrainingPage:
    ResultsPage:
    LoadingPage:
    TranslatingPage:


<SettingPage>
    name: 'setting'
    MDScreen:
        Image:
            source: 'setting.png'
            pos_hint: {'center_y': .8}
        MDLabel:
            font_name: 'gothmedium'
            text: "Hello!"
            font_size: 90
            pos_hint: {'center_y': .55}
            halign: 'center'
        MDLabel:
            font_name: 'gothmedium'
            text: "Before we start using Friendly, please answer a few  questions..."
            pos_hint: {'center_y': .5}
            halign: 'center'
        MDLabel:
            font_name: 'gothmedium'
            text: "Select Camera: "
            pos_hint: {'center_x': 0.65,'center_y': .45}
        MDRaisedButton:
            font_name: 'gothmedium'
            text: "Next"
            pos_hint: {'center_y':.03,'center_x':.9}
            on_release: app.loadHomePage()
        MDRectangleFlatButton:
            id: searchCamera
            font_name: 'gothmedium'
            text: "Search for all cameras "
            pos_hint: {'center_x': 0.5,'center_y': .4}
            on_release: app.setting()

<HomePage>:
    name: 'home'
    MDScreen:
        MDFlatButton:
            pos_hint: {'center_x':.05,'center_y': .95}
            on_release: app.setting()
            Image:
                source:'setting.png'
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
            on_release: app.loadTranslatingPage()
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
            left_action_items: [["home", lambda x: app.loadHomePage()]]
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
        MDTextField:
            id: showwords
            required: True
            multiline: True
            halign: 'center'
            pos_hint: {"center_y": 0.2}
            mode: "fill"
            fill_color: 0, 0, 0, .4
            text: "Record answer to show words recognized."
        MDRaisedButton:
            id: submitbutton
            text: "Submit Answer"
            on_release: app.loadResults()
            pos_hint: {"center_x": .5, "center_y": .1}
            font_name: 'gothmedium'

<TranslatingPage>:
    name: 'translating'
    MDScreen:
        MDBottomNavigation:
            #panel_color: "#eeeaea"
            selected_color_background: "lightgrey"
            text_color_active: "#6100FF"
            MDBottomNavigationItem:
                id: screen1
                name: 'screen1'
                text: 'Sign Language'
                MDTopAppBar:
                    title: "Sign Language"
                    pos_hint: {"center_y": 0.97}
                    font_name: 'gothbold'
                    left_action_items: [["home", lambda x: app.loadHomePage()]]
                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {'center_y':0.1}
                    adaptive_height: True
                    MDRectangleFlatIconButton:
                        id: mdbu
                        text: "on/off camera"
                        on_press: app.main()
                        adaptive_size: True
                        pos_hint: {"center_x": .5, "center_y": .5}
        
            MDBottomNavigationItem:
                id: screen2
                name: 'screen2'
                text: 'Training Sign Language'
                MDLabel:
                    id: notification
                    pos_hint: {'center_y':0.5}
                    pos_hint: {'center_x':0.5} 
                MDTopAppBar:
                    title: "Sign Language Trainer"
                    pos_hint: {"center_y": 0.97}
                    font_name: 'gothbold'
                    left_action_items: [["home", lambda x: app.loadHomePage()]]
                MDBoxLayout:
                    id: box
                    orientation: "vertical"
                    pos_hint: {'center_y':0.2}
                    adaptive_height: True
                    spacing: 10
                    padding: 20
                    MDTextField:
                        id: name
                        hint_text: "Name"
                        helper_text: "Name of Sign Language"
                        helper_text_mode: "persistent"
                    MDTextField:
                        id: slot
                        hint_text: "Slot"
                        helper_text: "Pick a slot (1~10)"
                        helper_text_mode: "persistent"
                    MDRectangleFlatIconButton:
                        id: mdbu
                        text: "Start Training!"
                        on_press: app.train()
                        adaptive_size: True
                        pos_hint: {'center_x':0.5}   
                    MDLabel:
                        id: label
                        halign: 'center'    
                        pos_hint: {'center_x':0.5}   

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
            on_release: app.loadTrainingPage()
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

<LoadingPage>:
    name: 'loading'
    MDScreen:
        MDLabel:
            id: loadinglabel
            font_name: 'gothmedium'
            text: "Loading..."
            halign: 'center'
            pos_hint: {'center_y': .5}
            font_size: 40

'''

class SettingPage(Screen):
    pass

class HomePage(Screen):
    pass

class TrainingPage(Screen):
    pass

class ResultsPage(Screen):
    pass

class LoadingPage(Screen):
    pass

class TranslatingPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

##/ PROMPT DATABASE /########################################################
prompts = { #prompt format: "prompt":['good emotions','okay emotions']
            "I recently got a job offer for my dream job!"
            :['admiration curiosity excitement joy caring optimism hopeful','neutral'],
            "My pet died yesterday."
            :['remorse caring surprise grief fear','neutral curiosity'],
            "I am going to Australia for a two week holiday!"
            :['caring curiousity optimism admiration approval amusement','desire']
            }

##/ MAIN CLASS /#############################################################
class App(MDApp): 

    # INITIALIZATION ######################################################
    def build(self): #intialize color themes and variables
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.spamon = False
        self.oncam = False
        Window.size = (450,975) #set window size
        self.toggle = False
        self.listen = False
        self.camera = 0
        self.key = 0  
        return Builder.load_string(KV) #load kivy UI
    
    # TRAING SIMULATOR ######################################################
    def loadTrainingPage(self): #load training page and camera
        self.root.transition = NoTransition()
        self.root.current = 'training' #change page to training
        self.getPrompt() #retrieve a random prompt
        #self.vidthread = threading.Thread(target=self.startcam) # assign video camera to a new thread
        if self.oncam == False: #check if camera has been started already
            self.oncam = True #toggle camera state
            self.startcam()    

    def startcam(self): #Load Camera
        self.image = Image() #Initialize image
        print("cam started") 
        self.capture = cv2.VideoCapture(int(self.CAMERA)) #select camera input
        Clock.schedule_interval(self.loadVideo, 1.0/30.0) #load camera view at 30 frames per second
        self.root.get_screen('training').ids.layout.add_widget(self.image) #add image view to training page
        self.oncam = True
        print('got here')
        #self.capture.release()

    def loadVideo(self, *args): #load frame
        ret, test_img = self.capture.read()  # captures frame and returns boolean value and captured image
    
        gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB) 

        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

        for (x, y, w, h) in faces_detected: #finds face and puts emotion label
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

    def voice2text(self): #making the record response button toggleable 
        if self.toggle == False: # pressed to record
            print('toggle is false now true')
            self.toggle = True
            self.listen = True
            self.root.get_screen('training').ids.recordbutton.text = 'Press to stop recording and edit response'
            print('[voice2text] starting thread')
            self.thread = threading.Thread(target=self.recognizeSpeech)  # create a thread to run two functions at once
            self.thread.start()
        elif self.listen == True: # pressed to stop recording
            self.listen = False
            self.toggle = False
            self.root.get_screen('training').ids.recordbutton.text = 'Press to record response'
            self.root.get_screen('training').ids.showwords.text = self.answer
            self.root.get_screen('training').ids.showwords.helper_text = 'Tap on your answer to edit it.'
      
    def recognizeSpeech(self, *args): # speech recognition function. run on second thread which means it cant change graphics
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
                    self.answer = self.answer + " " + text.lower()
            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                continue
            if not self.listen:
                break
        print("LISTEN ENDED")

    def loadResults(self): # triggered when submit answer button is pressed
        self.answer = self.root.get_screen('training').ids.showwords.text
        self.root.current = 'results' #switch page to results page
        Clock.unschedule(self.loadVideo) # stop clock from loading video frames
        self.root.get_screen('training').ids.layout.remove_widget(self.image) #add image view to training page
        self.oncam = False
        self.capture.release() # turn off camera
        self.listen = False # stop speech recognition
        # reset recording button
        self.toggle = False  
        self.root.get_screen('training').ids.recordbutton.text = 'Press to record response'
        self.isloading = True
        #self.thread = threading.Thread(target=self.gradePrompt)  #start a thread to grade the prompt
        #self.thread.start()
        self.result = self.gradePrompt()
        print("10")
        print("done")
        if self.result == 'not detected':
            self.root.get_screen('results').ids.resultlabel.text = 'No input was recognized. Please try again.'
            self.root.get_screen('results').ids.emotionlabel.text = ''
        else:
            self.root.get_screen('results').ids.resultlabel.text = self.result
            self.root.get_screen('results').ids.emotionlabel.text = "Emotion Detected: " + self.emotion

    def getPrompt(self): #pull random scenario from dictionary
        print("getPrompt called")
        print("generating random key............")
        random_key = random.sample(prompts.keys(), 1)[0]
        print(random_key)
        self.currentprompt = random_key
        print(prompts[self.currentprompt])
        self.root.get_screen('training').ids.scenariolabel.text = random_key
    
    def gradePrompt(self):
        print(prompts[self.currentprompt])
        goodans = prompts[self.currentprompt][0].split()
        okans = prompts[self.currentprompt][1].split()
        print(goodans)
        print(okans)
        tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
        model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
        emotion = pipeline('sentiment-analysis',model='arpanghoshal/EmoRoBERTa')
        emotion_labels = emotion(self.answer)
        print(emotion_labels)
        self.emotion = emotion_labels[0]['label']
        print(self.emotion)
        if not self.emotion.isalpha():
            return 'not detected'
        elif self.emotion in goodans:
            return '[b]Great Answer![/b]'
        elif self.emotion in okans:
            return '[b]Not Bad, Still Room To Improve![/b]'
        else:
            return '[b]Needs Work![/b]'

    def antispam(self):
        if self.spamon == False:
            self.spamon = True
            snacktext = "Anti-spam Engine Enabled!"
            AntiSpamEnabled = True
            self.spamthread = threading.Thread(target=startscreenrecorder)
            self.spamthread.start()
        else:
            self.spamon = False
            snacktext = "Anti-spam Engine Disabled!"
            AntiSpamEnabled = False

        snackbar = Snackbar(text=snacktext, snackbar_x="10dp", snackbar_y="10dp",)
        snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
        snackbar.buttons = [MDFlatButton(text="OK", text_color=(1, 1, 1, 1),on_release=snackbar.dismiss,)]
        snackbar.open()
    

    ##/ SIGN LANGUAGE TRANSLATOR ######################################################
    def loadTranslatingPage(self):
        self.root.transition = NoTransition()
        self.root.current = 'translating'

    def loadHomePage(self):
        if self.root.current == 'setting':
            try:
                print(self.CAMERA)
                self.root.transition = NoTransition()
                self.root.current = 'home' 
            except:
                print("No Camera Selected")
        else:
            self.root.current = 'home' 
                
    def setting(self):
        self.root.transition = NoTransition()
        self.root.current = 'setting' 
        arr = []
        self.dropdown = DropDown()
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap is None or not cap.isOpened():
                pass
            else:
                self.btn = MDRaisedButton(text='Camera %d' % i, size_hint_y=None, height=44)
                self.btn.bind(on_press=self.cameraSelect)
                self.dropdown.add_widget(self.btn)
        self.mainbutton = MDFlatButton(text='Choose Camera', size_hint=(None, None), pos_hint ={'x':.5, 'y':.43}, id='camera')
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.root.get_screen('setting').add_widget(self.mainbutton)

    def cameraSelect(self, *args):
        self.dropdown.select(self.btn.text)
        self.CAMERA = self.btn.text[-1]

    def main(self):
        if self.camera == 0: # When Camera On
            self.image = Image() #Get image
            # going to app.py for the function main(), which initialises variables to open camera
            self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap = self.Init()
            self.number = None 
            self.data = None
            self.mode = 0
            self.root.get_screen('translating').ids.screen1.add_widget(self.image)
            Clock.schedule_interval(self.load_video, 1.0/33.0) #scheduling image widget to be updated every 1.0/33.0 seconds
            self.camera = 1
 
        elif self.camera == 1: # When Camera Off
            self.camera = 0
            self.key = 1
            Clock.unschedule(self.load_video) #stop updating image widget
            Clock.schedule_once(self.load_video, -1) #update image widget one last time before next frame
            Clock.schedule_once(self.keyReseter)
            self.root.get_screen('translating').ids.screen1.remove_widget(self.image) #remove widget image
    
    def Init(self): #Initialising of camera
        args = self.get_args() # Argument parsing

        cap_width = args.width
        cap_height = args.height

        use_static_image_mode = args.use_static_image_mode
        min_detection_confidence = args.min_detection_confidence
        min_tracking_confidence = args.min_tracking_confidence

        use_brect = True

        cap = cv2.VideoCapture(int(self.CAMERA))  # Camera preparation
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

        mp_hands = mp.solutions.hands # Model load
        hands = mp_hands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        keypoint_classifier = KeyPointClassifier()
        # point_history_classifier = PointHistoryClassifier()

        with open('signlanguage/model/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ] # Read labels
        # with open(
        #         'model/point_history_classifier/point_history_classifier_label.csv',
        #         encoding='utf-8-sig') as f:
        #     point_history_classifier_labels = csv.reader(f)
        #     point_history_classifier_labels = [
        #         row[0] for row in point_history_classifier_labels
        #     ]

        cvFpsCalc = CvFpsCalc(buffer_len=10) # FPS Measurement
        
        history_length = 16 # Coordinate history
        point_history = deque(maxlen=history_length)

        finger_gesture_history = deque(maxlen=history_length) # Finger gesture history

        mode = 0
        number = 0

        return use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap
        
    def train(self): # Training SL Model
        try: 
            name = str(self.root.get_screen('translating').ids.name.text)
            slot = int(self.root.get_screen('translating').ids.slot.text)
        except:
            self.root.get_screen('translating').ids.name.error = True #invalid input
            self.root.get_screen('translating').ids.slot.error = True 
        if self.camera == 0:
            if name != "" and 0<slot<11: # Validation
                # On #####################################################
                self.image = Image()
                self.newLandmarks = []
                self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap = app.Init()
                self.number = slot
                self.mode = 1 #new data mode
                self.data = 0
                self.root.get_screen('translating').ids.screen2.add_widget(self.image) #adding widget
                Clock.schedule_interval(self.load_video, 1.0/10.0) #updating image widget per 1.0/10.0seconds (slower than previously to save procesing power)
                self.camera = 1
                self.cancleButton = MDFlatButton(text='Cancel', on_press=app.cancel)
                self.root.get_screen('translating').ids.screen2.add_widget(self.cancleButton)
            else:
                self.root.get_screen('translating').ids.name.error = True #invalid input, error = true
                self.root.get_screen('translating').ids.slot.error = True 
        elif self.camera == 1: # Off
            self.camera = 0
            self.key = 1
            Clock.unschedule(self.load_video)
            Clock.schedule_once(self.load_video, -1)
            self.root.get_screen('translating').ids.screen2.remove_widget(self.image)
            Clock.schedule_once(self.keyReseter)
            self.root.get_screen('translating').ids.notification.text = "Training in Progress!\nPlease do not switch off the app\nEstimated time taken: 30s"
            self.logging_csv(self.newLandmarks, slot, name)
            self.root.get_screen('translating').ids.name.text = ""
            self.root.get_screen('translating').ids.slot.text = ""
            self.training() # Train
            
    def cancel(self, *args):
        self.camera = 0
        self.key = 1
        Clock.unschedule(self.load_video)
        Clock.schedule_once(self.load_video, -1)
        self.root.get_screen('translating').ids.screen2.remove_widget(self.image)
        Clock.schedule_once(self.keyReseter)
        self.newLandmarks = []
        self.root.get_screen('translating').ids.name.text = ""
        self.root.get_screen('translating').ids.slot.text = ""
    
    @delayable
    def training(self, *args):
        self.root.get_screen('translating').ids.screen2.remove_widget(self.cancleButton)
        yield 1 
        report = keypoint.train() #goes to keypoint.py for train() function to train ml model, returns report with accuracy, precision ect. ect.
        #UI for popup
        popup = Popup(title='Results',
                content=MDLabel(text=str(report),halign="center",
                    theme_text_color="Error",),
                size_hint=(None, None), size=(800, 1400))
        self.root.get_screen('translating').ids.notification.text = ""
        popup.open() #Open pop-up

    def keyReseter(self, *args):
        self.key = 0

    def load_video(self, *args):
        #after initialisation in line 125, it uses the variables to go to app.py's loading() function to edit current image, and returns edited image
        img, self.data = app.loading(self.mode, self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap, self.number, self.key, self.data)
        buffer = cv2.flip(img,0).tostring() 
        texture1 = Texture.create(size=(img.shape[1],img.shape[0]), colorfmt='bgr') # translating returned edited image to KIVY UI's texture
        texture1.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture1
        self.root.get_screen('translating').ids.label.text = "Number of data collected: {}".format(str(self.data))
    
    def loading(self, mode, use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap, number, key, data):
        fps = cvFpsCalc.get()

        # Camera capture #####################################################
        ret, image = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
        image = cv2.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Process Key (ESC: end) #################################################
        if key == 1:  # ESC
            cap.release()
        # number, mode = select_mode(key, mode)

        # Detection implementation #############################################################
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        #  ####################################################################
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                    results.multi_handedness):
                # Bounding box calculation
                brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                # Landmark calculation
                landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = self.pre_process_landmark(
                    landmark_list)
                # pre_processed_point_history_list = pre_process_point_history(
                #     debug_image, point_history)
                # Write to the dataset file
                data = self.appending_data(number, mode, pre_processed_landmark_list, data)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == "Not Applicable":  # Point gesture
                    point_history.append(landmark_list[8])
                else:
                    point_history.append([0, 0])

                # # Finger gesture classification
                # finger_gesture_id = 0
                # point_history_len = len(pre_processed_point_history_list)
                # if point_history_len == (history_length * 2):
                #     finger_gesture_id = point_history_classifier(
                #         pre_processed_point_history_list)

                # Calculates the gesture IDs in the latest detection
                # finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(
                    finger_gesture_history).most_common()

                # Drawing part
                debug_image = self.draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = self.draw_landmarks(debug_image, landmark_list)
                debug_image = self.draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    keypoint_classifier_labels[hand_sign_id],
                    "Hand Motion Detected"
                    # point_history_classifier_labels[most_common_fg_id[0][0]],
                )
        else:
            point_history.append([0, 0])

        debug_image = self.draw_point_history(debug_image, point_history)
        debug_image = self.draw_info(debug_image, fps, mode, number)

        # cv2.imshow('Hand Gesture Recognition', debug_image) # Screen reflection 
        return debug_image, data
    
    def draw_info_text(self, image, brect, handedness, hand_sign_text,
                   finger_gesture_text):
        cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                    (0, 0, 0), -1)

        info_text = handedness.classification[0].label[0:]
        if hand_sign_text != "":
            info_text = info_text + ':' + hand_sign_text
        cv2.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        if finger_gesture_text != "":
            cv2.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                    cv2.LINE_AA)

        return image
    
    def draw_landmarks(self, image, landmark_point):
        if len(landmark_point) > 0:
            # Thumb
            cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (255, 255, 255), 2)

            # Index finger
            cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (255, 255, 255), 2)

            # Middle finger
            cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (255, 255, 255), 2)

            # Ring finger
            cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (255, 255, 255), 2)

            # Little finger
            cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (255, 255, 255), 2)

            # Palm
            cv2.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (255, 255, 255), 2)
            cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (0, 0, 0), 6)
            cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (255, 255, 255), 2)

        # Key Points
        for index, landmark in enumerate(landmark_point):
            if index == 0:  # hand 1
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 1:  # hand 2
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 2:  # thumb: root
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 3:  # thumb: 1st joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 4:  # thumb: fingertip
                cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 5:  # Index finger: root
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 6:  # Index finger: 2nd joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 7:  # Index finger: 1st joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 8:  # index finger: fingertip
                cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 9:  # Middle finger: root
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 10:  # Middle finger: 2nd joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 11:  # Middle finger: 1st joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 12:  # Middle finger: finger first
                cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 13:  # Ring finger: base
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 14:  # Ring finger: 2nd joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 15:  # Ring finger: 1st joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 16:  # Ring finger: fingertip
                cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 17:  # Little finger: root
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 18:  # Little finger: 2nd joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 19:  # Little finger: 1st joint
                cv2.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 20:  # little finger: finger first
                cv2.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv2.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        return image

    def draw_bounding_rect(self, use_brect, image, brect):
        if use_brect:
            # Outer rectangle
            cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                        (0, 0, 0), 1)

        return image
    
    def draw_point_history(self, image, point_history):
        for index, point in enumerate(point_history):
            if point[0] != 0 and point[1] != 0:
                cv2.circle(image, (point[0], point[1]), 1 + int(index / 2),
                        (152, 251, 152), 2)

        return image

    def draw_info(self, image, fps, mode, number):
        cv2.putText(image, "FPS:" + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(image, "FPS:" + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2, cv2.LINE_AA)

        mode_string = ['Logging Key Point', 'Logging Point History']
        if 1 <= mode <= 2:
            cv2.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                    cv2.LINE_AA)
            if 0 <= number <= 9:
                cv2.putText(image, "NUM:" + str(number), (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                        cv2.LINE_AA)
        return image

    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point
    
    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def appending_data(self, number, mode, landmark_list, data):
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 9):
            self.newLandmarks.append([number+23, *landmark_list])
            return data + 1
        
    def logging_csv(self, data, slot, name):
        label = []
        file = "signlanguage/model/keypoint_classifier/keypoint_classifier_label.csv"
        with open(file, "r") as fin: # New SL name in slot
            for _ in range(34):
                label.append(fin.readline().strip("\n"))      
        label[5+slot-1] = name
        with open(file, "w") as fout: #logging label name
            fout.write("\n".join(label))

        csv_path = 'signlanguage/model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            for i in data: #logging new landmark data
                writer = csv.writer(f)
                writer.writerow(i) 

    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv2.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def get_args(self, *args):
        parser = argparse.ArgumentParser()

        parser.add_argument("--device", type=int, default=0)
        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height', type=int, default=540)

        parser.add_argument('--use_static_image_mode', action='store_true')
        parser.add_argument("--min_detection_confidence",
                            help='min_detection_confidence',
                            type=float,
                            default=0.7)
        parser.add_argument("--min_tracking_confidence",
                            help='min_tracking_confidence',
                            type=int,
                            default=0.5)

        args = parser.parse_args()

        return args

LabelBase.register(name='gothbold', fn_regular='GothamBold.otf')
LabelBase.register(name='gothmedium', fn_regular='GothamMedium.ttf')


if __name__=="__main__":
    app = App()
    app.run()


