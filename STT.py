import soundfile as sf
import requests
import speech_recognition as sr
import os
import json
from pathlib import Path
# need
# google-cloud-speech
# soundfile
# SpeechRecognition
# requests

# Взятие токена из json файла
with open("tokens.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)
# Сам токен
STT_token = tokens["STT_token"]
Punct_token=tokens["Punct_token"]


# whisper
def STT_whisper(filename):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": f"Bearer {STT_token}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()["text"]


def STT(path_to_file: str) -> str:
    # Чтение оригинального файла
    data, samplerate = sf.read(path_to_file)
    out = "cur_STT.wav"

    # временный wav файл
    sf.write(out, data, samplerate)

    # адресс временного файла
    adress = os.path.join(Path(__file__).parent, out)

    # узнаватель текст
    rec = sr.Recognizer()

    # аудио записывается через узнаватель
    with sr.AudioFile(adress) as source:
        # rec.adjust_for_ambient_noise(source)
        audio = rec.record(source)
        # cleaned_audio=rec.listen(source)

    # вывод
    try:
        ret = rec.recognize_google(audio, language="ru-RU")
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


#Пунктуация. Принимает текст str
def Punct(text):
    #апи
    response = requests.post("https://api-inference.huggingface.co/models/1-800-BAD-CODE/xlm-roberta_punctuation_fullstop_truecase", headers= {"Authorization": f"Bearer {Punct_token}"}, json={"inputs":text,})

    #Ответ
    output=response.json()
    
    #вывод
    try:
        return output[0]["generated_text"].replace(r"\n ",'\n')
    except KeyError:
        print(output)
        return Punct(text)
