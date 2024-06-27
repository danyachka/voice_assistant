import json

import pyaudio
import pyttsx3
import vosk


class VoskProcessor:
    stream = None

    record = None

    pa = None

    def __init__(self):
        self.__setup()

    def __setup(self):
        print("Starting vosk setup")

        model = vosk.Model('vosk-model')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()

        print("Vosk has been setup successfully!")

    def listen(self) -> str:
        while True:
            print("Listening...")
            data = self.stream.read(8000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                print("Analysing...")
                answer = json.loads(self.record.Result())['text']
                print("You said: " + str(answer))
                return answer

    def release(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
