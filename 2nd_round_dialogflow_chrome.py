#import speech_recognition as sr
from gtts import gTTS
from pygame import mixer # Load the required library
import os
import os.path
import sys
import datetime
import json
#from mtranslate import translate
import apiai
#import threading
import random
import VoiceUsingChrome
import mySqlite
import label_image
import time

#CLIENT_ACCESS_TOKEN = 'f8dc0f9ac21a445e95eb0ed6af888198'#shop
CLIENT_ACCESS_TOKEN = '67d03b977e32456d89d1e4e84613cac5'#bangla
#CLIENT_ACCESS_TOKEN = 'dde3d7f999434732a56d9887b7c43d09'#robot
#CLIENT_ACCESS_TOKEN = '332da3ed83324895993de3f7f7ca5f91'#asad
#CLIENT_ACCESS_TOKEN ='1a62a0de8e1a42bdb544334977437567 '#joke

mixer.init()
response_json =''

def dialog(text):
    global response_json
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.session_id = "<robot>"
    request.query = text
    response = request.getresponse()
    a=str(response.read(), 'utf-8')
    response_json =json.loads(a)
    print(response_json)
    print(response_json['result']['metadata']['intentName'])
    return (response_json["result"]["fulfillment"]["messages"][0]["speech"])#["textToSpeech"])

def random_sound():
    random_sounds=["a","b"]
    i=random.randint(0,len(random_sounds)-1)
    try:
        mixer.music.load("sound/"+str(random_sounds[i])+".mp3")
        mixer.music.play()
        while(mixer.music.get_busy()):
            pass
        mixer.music.load("test2.mp3")
    except:
        pass

def save_and_load_speech(text):
    
    try: # Load local
        a = datetime.datetime.now()
        mixer.music.load("sound/"+ text +".mp3")
        b = datetime.datetime.now()
        print("local load time: ",b-a)
    except: # load from gtts
        a = datetime.datetime.now()
        tts = gTTS(text= text , lang='bn')
        b = datetime.datetime.now()
        print("TTS time: ",b-a)
    
        try: # save with variable name
            a = datetime.datetime.now()
            tts.save("sound/"+ text +".mp3")
            b = datetime.datetime.now()
            print("Saveing time: ",b-a)
            a = datetime.datetime.now()
            mixer.music.load("sound/"+text+".mp3")
            b = datetime.datetime.now()
            print("load time: ",b-a)
        except:
            try: # save using test name
                a = datetime.datetime.now()
                tts.save("test.mp3")
                b = datetime.datetime.now()
                print("Saveing time: ",b-a)
                a = datetime.datetime.now()
                mixer.music.load("test.mp3")
                b = datetime.datetime.now()
                print("load time: ",b-a)
            except:
                print("can't save")

def take_action(intent):
    print('Taking Action')
    data_from_db=['','']
    
    if(intent=='analyze_disease - custom - yes'):
        data_from_db= mySqlite.read_from_db(response_json['result']['contexts'][1]['parameters']['plant'],response_json['result']['contexts'][0]['parameters']['disease'])
    
    if(intent=='analyze_disease'):
        plant, disease = label_image.start_process()
        if disease =='সুস্থ':
            data_from_db[1]=" আপনার "+plant+"ক্ষেতে কোন সমস্যা হয় নাই"
        else:
            dialog(str(plant)+' '+str(disease)+' পরীক্ষা ফলাফল')
            data_from_db[1]=" আপনার "+plant+"ক্ষেতে "+disease+" হয়েছে, আপনি কি এর প্রতিকারের উপায় জানতে চান"
       
#        data_from_db= mySqlite.read_from_db(plant, disease)
    
    if(intent=='treatment_for_disease_context_plant'):
        data_from_db= mySqlite.read_from_db(response_json['result']['contexts'][1]['parameters']['plant'],response_json['result']['parameters']['disease'])
        
    if(intent=='treatment_for_disease'):
        print(response_json['result']['parameters']['plant'],response_json['result']['parameters']['disease'])
        data_from_db= mySqlite.read_from_db(response_json['result']['parameters']['plant'],response_json['result']['parameters']['disease'])
    
    print(data_from_db[0],data_from_db[1])
    return data_from_db[1]
#                mixer.music.load("sound/jokes_"+str(random.randint(1,2))+".mp3")
def conversation():
    while True:
        user_said=None
        while (user_said==None):
            user_said=VoiceUsingChrome.chrome_detect()
        print('\n\n')
        print(user_said)
        try:
            a = datetime.datetime.now()
            dialogflow_response=dialog(user_said)
            b = datetime.datetime.now()
            print("dialogflow time: ",b-a)
            
            save_and_load_speech(dialogflow_response)
            
            mixer.music.play()
            if not response_json["result"]['actionIncomplete']:
                local_response=take_action(response_json['result']['metadata']['intentName'])
                while(mixer.music.get_busy()):
                    time.sleep(.1)
                mixer.music.load("test2.mp3")
                if local_response!='':
                    save_and_load_speech(local_response)
                    mixer.music.play()
                    while(mixer.music.get_busy()):
                        time.sleep(.1)
                    mixer.music.load("test2.mp3")

            while(mixer.music.get_busy()):
                time.sleep(.1)
            mixer.music.load("test2.mp3")
                
            print("end")
        except KeyboardInterrupt:
            raise
        except:
            pass

if __name__== '__main__':
    while True:
        conversation()
