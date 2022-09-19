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

    cam = 0

    def build(self):
        self.layout = MDBoxLayout(orientation="vertical")
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        print("----------------------------------------------------------------")
        return Builder.load_string( KV ) 


    def cam(self):
        self.image = Image()
        self.capture = cv2.VideoCapture(0)
        self.layout.add_widget(self.image)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.load_video, 1/60)

       
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