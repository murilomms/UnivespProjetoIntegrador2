from gtts import gTTS 
import os  
from io import BytesIO
import pyttsx3
from playsound import playsound


class TextToSpeachConverterGtts:
       
    def ConvertAndPlay(self, textToConvert : str, language : str = 'pt-br'):

        outputFileName = 'output.mp3'
        myObj = gTTS(text=textToConvert, lang= str(language), slow=False)   
        myObj.save(outputFileName)       

        playsound(outputFileName)
        os.remove(outputFileName)
       
        
class TextToSpeachConverterPyttsx3:
    
    def ConvertAndPlay(self, textToConvert : str):
        
        engine = pyttsx3.init() 
        engine.say(textToConvert)

        engine.runAndWait()
        

#Converter = TextToSpeachConverterGtts()
#Converter.ConvertAndPlay('Teste conversão texto')

#Converter = TextToSpeachConverterPyttsx3()
#Converter.ConvertAndPlay('Teste conversão texto')    
        