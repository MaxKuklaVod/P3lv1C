import soundfile as sf
import numpy as np
import requests
import speech_recognition as sr
from os import path
from pathlib import Path

# need
# google-cloud-speech
# soundfile
# SpeechRecognition
# numpy
#requests





#whisper
def STT_whisper(filename):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()['text']
#пример
print(STT_whisper("audio.ogg"))




def STT(path_to_file: str) -> str:
    #Чтение оригинального файла
    data, samplerate = sf.read(path_to_file)
    out = "cur_STT.wav"
    
    #временный wav файл 
    sf.write(out, data, samplerate)
    
    #адресс временного файла
    adress = path.join(path.dirname(path.realpath(__file__)), out)
    
    #узнаватель текст
    rec = sr.Recognizer()


    #аудио записывается через узнаватель
    with sr.AudioFile(adress) as source:
        # rec.adjust_for_ambient_noise(source)
        audio = rec.record(source)
        # cleaned_audio=rec.listen(source)


    #вывод
    try:
        ret = rec.recognize_google(audio, language="ru-RU")
        print(ret)
        return ret
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Речь не распознана"
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


STT('audio.ogg')

