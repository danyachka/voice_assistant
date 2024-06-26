import os
import time
from threading import Thread

import torch
import pyaudio

import numpy as np
from colorama import Fore


class SileroProcessor:
    model = None

    sample_rate = 24000

    speaker = 'xenia'

    device = torch.device('cpu')

    threads = 6

    model_name = "v3"

    playing_thread: Thread = None

    generating_thread: Thread = None

    text_queue = []

    audio_queue = []

    def __init__(self, model_name, threads):
        self.__setup()

        self.threads = threads
        self.model_name = model_name

    def say(self, long_string):
        words = long_string.split()
        arrays = [words[i:i + 10] for i in range(0, len(words), 10)]

        for text in arrays:
            self.text_queue.append(text)

        self.__call_generating_thread()

    def __call_generating_thread(self):
        if self.generating_thread is None:
            start_thread = True
        else:
            start_thread = not self.generating_thread.is_alive()

        if not start_thread:
            return

        print(Fore.BLUE + "Starting silero generation thread" + Fore.RESET)
        self.generating_thread = Thread(target=self.__generate)
        self.generating_thread.start()

    def __generate(self):
        while len(self.text_queue) != 0:
            print(Fore.GREEN + f"Continue silero generation thread: {len(self.text_queue)}" + Fore.RESET)
            start = time.time()
            text = self.text_queue.pop(0)
            text = "".join(text)

            audio = self.model.apply_tts(text=text,
                                         speaker=self.speaker,
                                         sample_rate=self.sample_rate)
            self.audio_queue.append(audio)
            self.__call_playing_thread()

            print(f"Audio generation took: {time.time() - start}")

    def is_playing_thread_alive(self) -> bool:
        if self.playing_thread is None:
            is_alive = False
        else:
            is_alive = self.playing_thread.is_alive()

        return is_alive

    def stop(self):
        self.text_queue = []
        self.audio_queue = []

    def __call_playing_thread(self):
        if self.is_playing_thread_alive():
            return

        print(Fore.BLUE + "Starting silero playing thread" + Fore.RESET)
        self.playing_thread = Thread(target=self.__play)
        self.playing_thread.start()

    def __play(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True)

        while len(self.audio_queue) != 0:
            print(Fore.GREEN + f"Continue silero playing thread: {len(self.audio_queue)}" + Fore.RESET)
            audio = self.audio_queue.pop(0)

            audio = audio.detach().cpu().numpy()
            audio = audio.transpose()

            stream.write(audio.tobytes())

        stream.stop_stream()
        stream.close()
        p.terminate()

    def __setup(self):
        torch.set_num_threads(6)
        local_file = f'model_{self.model_name}.pt'

        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/ru_v3.pt' if self.model == 'v3'
                                           else 'https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                           local_file)

        self.model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")

        self.model.to(self.device)
        print(f"{type(self.model)}")

    def release(self):
        pass
