from tkinter import Widget
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
import cv2

KV = '''
MDScreen:

    MDBottomNavigation:
        #panel_color: "#eeeaea"
        selected_color_background: "orange"
        text_color_active: "lightgrey"

        MDBottomNavigationItem:
            name: 'screen1'
            text: 'Sign Language'
        
        MDRectangleFlatIconButton:
            id: mdbu
            text: "press me to start camera"
            on_press: app.cam()
            pos: self.pos

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Training Sign Language'

'''

class myCam(MDApp):

    def build(self):
        self.camera = 0
        self.layout = Widget()
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string( KV ) 


    def cam(self):
        if self.camera == 0:
            print("hi")
            self.layout.add_widget(MDRaisedButton(text='Hello 1'))
            # self.image = Image()
            # self.layout = BoxLayout()
            # self.layout.add_widget(self.image)
            # self.capture = cv2.VideoCapture(0)
            # cv2.namedWindow("CV2 Image")
            # Clock.schedule_interval(self.load_video, 1/60)
            self.camera = 1
        elif self.camera == 1:
            print("-")
            self.camera = 0
            # self.capture.release()
            # cv2.destroyAllWindows()

        

       
    def load_video(self, *args):
        ret, frame = self.capture.read()
        cv2.imshow("CV2 Image", frame)
        #load frame
        self.image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture


myCam().run()