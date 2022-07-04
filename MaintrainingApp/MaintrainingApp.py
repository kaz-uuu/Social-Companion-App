from re import U
from kivy.app import App


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.android.antispamservice',
    servicename=u'antispam'
)
class trainingApp(App): #this is the main training app that is going to be downloaded into the user's phone
    #add code for training app here, free to change name

    def startantispam(): #this function starts the antispam and language corrector as a background service
        from jnius import autoclass
        antispamservice = autoclass(SERVICE_NAME)
        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        antispamservice.start(mActivity,'')
        return antispamservice

if __name__=="__main__":
    app = trainingApp()
    app.run()