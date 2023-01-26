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
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivyoav.delayed import delayable 

##/ EMOTION RECOGNITION PACKAGES /################################################
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
import speech_recognition
import pyttsx3
import tensorflow
from keras.models import load_model
from keras.utils import load_img, img_to_array

##/ SIGN LANGUAGES CODE /################################################
import signlanguage.app as app
import signlanguage.keypoint as keypoint


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
    HomePage:
    TrainingPage:
    ResultsPage:
    LoadingPage:
    TranslatingPage:

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
            required: True
            multiline: True
            halign: 'center'
            pos_hint: {"center_y": 0.2}
            mode: "fill"
            fill_color: 0, 0, 0, .4
            text: "Record answer to show words recognized."

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
                transition_direction: 'Left'
                MDTopAppBar:
                    title: "Sign Language"
                    pos_hint: {"center_y": 0.97}
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
                transition_direction: 'Right'
                MDLabel:
                    id: notification
                    pos_hint: {'center_y':0.5}
                    pos_hint: {'center_x':0.5} 
                MDTopAppBar:
                    title: "Sign Language Trainer"
                    pos_hint: {"center_y": 0.97}
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
            
'''


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
            :['remorse caring surprise grief','neutral curiosity'],
            "I am going to Australia for a two week holiday!"
            :['caring curiousity optimism admiration approval amusement','desire']
            }

##/ MAIN CLASS /#############################################################
class trainingApp(MDApp): 

    def build(self): #intialize color themes and variables
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.firsttimeantispam = False
        self.thread = None
        self.startedcam = False
        Window.size = (450,975) #set window size
        self.toggle = False
        self.listen = False
        self.camera = 0
        self.key = 0  
        return Builder.load_string(KV) #load kivy UI
    
    def loadTrainingPage(self): #load training page and camera
        self.root.current = 'training' #change page to training
        self.getPrompt() #retrieve a random prompt
        if self.startedcam == False: #check if camera has been started already
            self.startcam()
    
    def loadTranslatingPage(self):
        self.root.current = 'translating'

    def startcam(self): #Load Camera
        self.image = Image() #Initialize image
        print("cam started") 
        self.capture = cv2.VideoCapture(1) #select camera input
        Clock.schedule_interval(self.loadVideo, 1.0/30.0) #load camera view at 30 frames per second
        self.root.get_screen('training').ids.layout.add_widget(self.image) #add image view to training page
        self.startedcam = True 

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
        if self.toggle == False:
            self.toggle = True
            self.listen = True
            self.root.get_screen('training').ids.recordbutton.text = 'Press to stop recording and submit response'
            print('[voice2text] starting thread')
            self.thread = threading.Thread(target=self.recognizeSpeech)  # create a thread to run two functions at once
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
        print("--- Thread Ended --------------------------")

    def loadResults(self):
        print('[gradePrompt] starting tehread')
        self.thread = threading.Thread(target=self.gradePrompt)  # function's name without ()
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
        print("getPrompt called")
        print("generating random key............")
        random_key = random.sample(prompts.keys(), 1)[0]
        print(random_key)
        self.currentprompt = random_key
        print(prompts[self.currentprompt])
        self.root.get_screen('training').ids.scenariolabel.text = random_key
        return random_key
    
    def gradePrompt(self):
        good = False
        okay = False  
        bad = False
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


    # Main Image Reconition #####################################################
    def main(self):
        # When Camera On #####################################################
        if self.camera == 0:
            self.image = Image() #Get image
            # going to app.py for the function main(), which initialises variables to open camera
            print("1")
            self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap = app.main()
            print("2")
            self.number = None 
            self.data = None
            self.mode = 0
            print("2")
            self.root.ids.screen1.add_widget(self.image) #adding image widget
            Clock.schedule_interval(self.load_video, 1.0/33.0) #scheduling image widget to be updated every 1.0/33.0 seconds
            self.camera = 1
            print("3")
        # When Camera Off #####################################################
        elif self.camera == 1:
            self.camera = 0
            self.key = 1
            Clock.unschedule(self.load_video) #stop updating image widget
            Clock.schedule_once(self.load_video, -1) #update image widget one last time before next frame
            Clock.schedule_once(self.keyReseter)
            self.root.ids.screen1.remove_widget(self.image) #remove widget image

    # Training SL Model #####################################################
    def train(self):
        if self.camera == 0:
            name = self.root.ids.name.text
            slot = int(self.root.ids.slot.text)
            # Validation #####################################################
            if name != "" and 0<slot<11:
                label = []
                # New SL name in slot #####################################################
                file = "/Users/liuyanzhao/Documents/GitHub/Tech4Good/[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/model/keypoint_classifier/keypoint_classifier_label.csv"
                with open(file, "r") as fin:
                    for _ in range(34):
                        label.append(fin.readline().strip("\n"))      
                label[24+slot-1] = name
                with open(file, "w") as fout:
                    fout.write("\n".join(label))
                self.root.ids.name.text = ""
                self.root.ids.slot.text = ""
                # On #####################################################
                self.image = Image()
                self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap = app.main()
                self.number = slot
                self.mode = 1 #new data mode
                self.data = 0
                self.root.ids.screen2.add_widget(self.image) #adding widget
                Clock.schedule_interval(self.load_video, 1.0/10.0) #updating image widget per 1.0/10.0seconds (slower than previously to save procesing power)
                self.camera = 1
            else:
                self.root.ids.name.error = True #invalid input, error = true
                self.root.ids.slot.error = True 

        
        elif self.camera == 1:
            # Off #####################################################
            self.camera = 0
            self.key = 1
            Clock.unschedule(self.load_video)
            Clock.schedule_once(self.load_video, -1)
            self.root.ids.screen2.remove_widget(self.image)
            Clock.schedule_once(self.keyReseter)
            self.root.ids.notification.text = "Training in Progress!\nPlease do not switch off the app\nEstimated time taken: 30s"
            # Train!! #####################################################
            self.training()
            
    
    @delayable
    def training(self, *args):
        yield 1 
        report = keypoint.train() #goes to keypoint.py for train() function to train ml model, returns report with accuracy, precision ect. ect.
        #UI for popup
        popup = Popup(title='Results',
                content=MDLabel(text=str(report),halign="center",
                    theme_text_color="Error",),
                size_hint=(None, None), size=(800, 1400))
        self.root.ids.notification.text = ""
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
        self.root.ids.label.text = "Number of data collected: {}".format(str(self.data))

LabelBase.register(name='gothbold', fn_regular='GothamBold.otf')
LabelBase.register(name='gothmedium', fn_regular='GothamMedium.ttf')


if __name__=="__main__":
    app = trainingApp()
    app.run()


