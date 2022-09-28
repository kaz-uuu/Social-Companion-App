# Importing Kivy Packages #####################################################
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivyoav.delayed import delayable
from kivy.graphics.texture import Texture

# Importing Packages #####################################################
import cv2 as cv
import app
import keypoint


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

# KV #####################################################
KV = '''
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
'''

class myCam(MDApp):

    # Initial Set-Up #####################################################
    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Purple"
        Window.size = (450,975)
        self.camera = 0
        self.key = 0
        self.layout = MDBoxLayout(orientation='vertical')
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string( KV ) 

    # Main Image Reconition #####################################################
    def main(self):
        # On #####################################################
        if self.camera == 0:
            self.image = Image()
            self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap = app.main()
            self.number = None
            self.data = None
            self.mode = 0
            self.root.ids.screen1.add_widget(self.image)
            Clock.schedule_interval(self.load_video, 1.0/33.0)
            self.camera = 1
        # Off #####################################################
        elif self.camera == 1:
            self.camera = 0
            self.key = 1
            Clock.unschedule(self.load_video)
            Clock.schedule_once(self.load_video, -1)
            Clock.schedule_once(self.keyReseter)
            self.root.ids.screen1.remove_widget(self.image)

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
                self.mode = 1
                self.data = 0
                self.root.ids.screen2.add_widget(self.image)
                Clock.schedule_interval(self.load_video, 1.0/10.0)
                self.camera = 1
            else:
                self.root.ids.name.error = True
                self.root.ids.slot.error = True

        
        elif self.camera == 1:
            # Off #####################################################
            self.camera = 0
            self.key = 1
            Clock.unschedule(self.load_video)
            Clock.schedule_once(self.load_video, -1)
            self.root.ids.screen2.remove_widget(self.image)
            Clock.schedule_once(self.keyReseter)
            self.root.ids.notification.text = "Training in Progress!\nPlease do not switch off the app\nETA: 30s"
            # Train!! #####################################################
            self.training()
            
    
    @delayable
    def training(self, *args):
        yield 1 
        report = keypoint.train()
        popup = Popup(title='Results',
                content=MDLabel(text=str(report),halign="center",
                    theme_text_color="Error",),
                size_hint=(None, None), size=(800, 1400))
        self.root.ids.notification.text = ""
        popup.open()

    def keyReseter(self, *args):
        self.key = 0

    def load_video(self, *args):
        img, self.data = app.loading(self.mode, self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap, self.number, self.key, self.data)
        buffer = cv.flip(img,0).tostring()
        texture1 = Texture.create(size=(img.shape[1],img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture1
        self.root.ids.label.text = "Number of data collected: {}".format(str(self.data))
        

myCam().run()