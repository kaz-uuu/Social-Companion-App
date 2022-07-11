from pyexpat.errors import messages
import pytesseract

class language_Corrector(object):
    def __init__(self):
        self._messagedata = pytesseract.Output.DICT

    @property
    def messagetyped(self):
        return self._messagedata
    

    @messagetyped.setter
    def messagetyped(self, message):
        #check if the message contians any taboo words, and perform sentiment analysis on the message
        self._messagetyped = message
        wordlist = list(enumerate(self._messagetyped["text"]))
        del wordlist[:4] #remove all spaces in front of the text
        
        

        
        