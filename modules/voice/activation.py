import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import os
import subprocess


model = Model(r"modules\voice\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_for_wake_word():
    # print("Listening for 'Syrex'...")
    activation_words_list = ["hello"]

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                print("Heard:", text)
                if text.lower() in activation_words_list:
                    print("Listening!! Please tell your command!")
                    run_script()

def run_script():
    subprocess.Popen(["python", "your_script.py"])



listen_for_wake_word()
