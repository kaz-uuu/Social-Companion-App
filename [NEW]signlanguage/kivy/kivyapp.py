from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button #for buttons
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen

kv = Builder.load_string('''
<MyMainWindow>:
    Label:
        font_size: 42
        text: root.name
    Button:
        text: 'Next screen'
        size_hint: None, None
        pos_hint: {'right': 1}
        size: 150, 50
        on_release: root.manager.current = root.manager.next()
    Button:
        text: 'Previous screen'
        size_hint: None, None
        size: 150, 50
        on_release: root.manager.current = root.manager.previous()

''')

class MyMainWindow(Screen):
    pass

class myApp(App):
    def build(self):
        root = ScreenManager()
        root.add_widget(MyMainWindow(name='SignLanguage'))
        root.add_widget(MyMainWindow(name='TrainingSignLanguage'))
        return root

if __name__ == '__main__':
    myApp().run()


# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button #for buttons
# from kivy.lang import Builder 
# from kivy.uix.screenmanager import ScreenManager, Screen

# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.config import Config
# from kivy.graphics.texture import Texture
# from kivy.core.window import Window

# import cv2

# Config.set('graphics', 'height', '2340')
# Config.set('graphics', 'width', '1080')

# class MyMainWindow(GridLayout):
#     pass

# class SecondWindow(Screen):
#     pass

# class ThirdWindow(Screen):
#     def build(self):
#         self.img1=Image()
#         layout = BoxLayout()
#         layout.add_widget(self.img1)
#         #opencv2 stuffs
#         self.capture = cv2.VideoCapture(0)
#         cv2.namedWindow("CV2 Image")
#         Clock.schedule_interval(self.update, 1.0/33.0)
#         return layout

#     def update(self, dt):
#         # display image from cam in opencv window
#         ret, frame = self.capture.read()
#         cv2.imshow("CV2 Image", frame)
#         # convert it to texture
#         buf1 = cv2.flip(frame, 0)
#         buf = buf1.tostring()
#         texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
#         texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         # display image from the texture
#         self.img1.texture = texture1
#     pass

# class FourthWindow(Screen):
#     pass

# class WindowManager(ScreenManager):
#     pass


# class myApp(App):
#     def build(self):
#         return MyMainWindow()

# if __name__ == '__main__':
#     Window.clearcolor = (1, 1, 1, 1)
#     myApp().run()
#     cv2.destroyAllWindows()