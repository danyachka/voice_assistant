import os
import time

import torch
import pyaudio

import numpy as np


class SileroProcessor:
    model = None

    sample_rate = 24000

    speaker = 'xenia'

    device = torch.device('cpu')

    threads = 6

    model_name = "v3"

    def __init__(self, model_name, threads):
        self.__setup()

        self.threads = threads
        self.model_name = model_name

    def say(self, text):
        start = time.time()
        audio = self.model.apply_tts(text=text,
                                     speaker=self.speaker,
                                     sample_rate=self.sample_rate)
        start_2 = time.time()
        print(f"Audio generation took: {start_2 - start}")

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True)

        audio = audio.detach().cpu().numpy()
        audio = audio.transpose()

        stream.write(audio.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(f"Audio playing took: {time.time() - start_2}")

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
