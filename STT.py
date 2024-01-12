import soundfile as sf
import numpy as np
import speech_recognition as sr
from os import path
from pathlib import Path

# need
# google-cloud-speech
# soundfile
# SpeechRecognition
# numpy


def STT(path_to_file: str) -> str:
    data, samplerate = sf.read(path_to_file)
    out = "cur_STT.wav"
    sf.write(out, data, samplerate)
    adress = path.join(path.dirname(path.realpath(__file__)), out)
    rec = sr.Recognizer()

    with sr.AudioFile(adress) as source:
        rec.adjust_for_ambient_noise(source)
        audio = rec.record(source)
        # cleaned_audio=rec.listen(source)

    try:
        ret = rec.recognize_google(audio, language="ru-RU")
        print(ret)
        return ret
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


# STT('input4.ogg')
