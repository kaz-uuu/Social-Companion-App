from re import U
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
#from jnius import autoclass
import speech_recognition
import pyttsx3
import pyaudio


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.android.antispamservice',
    servicename=u'antispam'
)
class trainingApp(App): #this is the main training app that is going to be downloaded into the user's phone
    #add code for training app here, free to change name
    
    class mainsimulator():
        def recognizeSpeech(self):
            print("Starting Recording")
            recognizer = speech_recognition.Recognizer() #start recognizing speech
            print("speak anything")
            try: 
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic,duration=1)
                    audio = recognizer.listen(mic)
                    text = recognizer.recognize_google(audio)
                    text = text.lower()
                    print(text)
            except speech_recognition.UnknownValueError():
                recognizer.adjust_for_ambient_noise(mic,duration=)
                print("could not recognize your voice")
                
    
    def startantispam(self): #this function starts the antispam and language corrector as a background service
        antispamservice = autoclass(SERVICE_NAME)
        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        antispamservice.start(mActivity,'')
        return antispamservice

    def build(self):
        return Button(text='hello world')
    
    mainsim = mainsimulator()
    mainsim.recognizeSpeech()

if __name__=="__main__":
    app = trainingApp()
    app.run()

