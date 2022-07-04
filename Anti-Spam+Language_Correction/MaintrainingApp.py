from kivy import app

class trainingApp(App): #this is the main training app that is going to be downloaded into the user's phone
    #add code for training app here, free to change name

    def startantispam(): #this function starts the antispam and language corrector as a background service
        from jnius import autoclass
        antispamservice = autoclass('org.trainingapp.antispam')
        mActivity = autoclass('org.kivy.android.antispamActivity')
        antispamservice.start(mActivity,"")
        return antispamservice

if __name__=="__main__":
    app = trainingApp()
    app.run()