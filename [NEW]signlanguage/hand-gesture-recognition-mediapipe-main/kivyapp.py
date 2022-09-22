from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2 as cv
import app
import time

import copy
from collections import Counter


KV = '''
MDScreen:
    MDBottomNavigation:
        #panel_color: "#eeeaea"
        selected_color_background: "orange"
        text_color_active: "lightgrey"

        MDBottomNavigationItem:
            id: screen1
            name: 'screen1'
            text: 'Sign Language'
            MDBoxLayout:
                orientation: "vertical"
                MDRectangleFlatIconButton:
                    id: mdbu
                    text: "on/off camera"
                    on_press: app.main()
                    adaptive_size: True
                    pos_hint: {"center_x": .5, "center_y": .5}
        
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Training Sign Language'
            MDTextField:
                hint_text: "Name"
                helper_text: "Name of Sign Language"
                helper_text_mode: "persistent"
'''

class myCam(MDApp):

    def build(self):
        self.camera = 0
        self.layout = MDBoxLayout(orientation='vertical')
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string( KV ) 


    def main(self):
        if self.camera == 0:
            self.image = Image()
            # self.cap = cv.VideoCapture(0)
            self.mode, self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap, self.number = app.main()
            self.root.ids.screen1.add_widget(self.image)
            # while True:
                # Process Key (ESC: end) #################################################
                # key = cv.waitKey(10)
                # if key == 27:  # ESC
                #     cap.release()
                #     cv.destroyAllWindows()
                # number, mode = app.select_mode(key, mode)
            Clock.schedule_interval(self.load_video, 1.0/33.0)
        elif self.camera == 1:
            self.camera = 0
            self.root.ids.screen1.remove_widget(self.image)
            # self.cap.release()
        
    def load_video(self, *args):
        img = app.loading(self.mode, self.use_brect, self.hands, self.keypoint_classifier, self.cvFpsCalc, self.point_history, self.finger_gesture_history, self.keypoint_classifier_labels, self.cap, self.number)
        # cv.imshow('Hand Gesture Recognition', img)
        buffer = cv.flip(img,0).tostring()
        texture1 = Texture.create(size=(img.shape[1],img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture1

myCam().run()