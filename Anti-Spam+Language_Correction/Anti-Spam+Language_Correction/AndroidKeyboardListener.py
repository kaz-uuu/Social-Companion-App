from threading import Thread
import kivy
from kivy.core.window import Window
from kivy.uix.widget import Widget
#android is still a work in progress
from Anti_Spam_Language_Correction import messagestring
class keyboardlistener(Thread):
    
    def __init__(self, **kwargs):
        Thread.__init__(self)
        super(keyboardlistener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self.on_key_down)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard = None
    def on_key_down(self,keyboard, keycode, text, modifiers):
        global messagestring
        messagestring += keycode[1]
        if keycode[1] == "backspace":
            messagestring = messagestring[:-1]
        
        if keycode[1] == "enter":
            keyboard.release()
        return True