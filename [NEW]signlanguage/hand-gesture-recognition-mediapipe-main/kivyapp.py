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
            self.root.ids.screen1.add_widget(self.image)
            # self.cap = cv.VideoCapture(0)
            mode, use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap = app.main()
            while True:
                # self.load_video(mode, use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap)
                image = app.loading(mode, use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap)
                self.image_frame = image
                buffer = cv.flip(image,0).tostring()
                texture = Texture.create(size=(image.shape[1],image.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
                self.image.texture = texture
                time.sleep(1)
   
        elif self.camera == 1:
            self.camera = 0
            self.root.ids.screen1.remove_widget(self.image)
            # self.cap.release()
        
    def load_video(self, mode, use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap):
        print()
        # image = app.loading(mode, use_brect, hands, keypoint_classifier, cvFpsCalc, point_history, finger_gesture_history, keypoint_classifier_labels, cap)
        # self.image_frame = image
        # buffer = cv.flip(image,0).tostring()
        # texture = Texture.create(size=(image.shape[1],image.shape[0]), colorfmt='bgr')
        # texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        # self.image.texture = texture



myCam().run()