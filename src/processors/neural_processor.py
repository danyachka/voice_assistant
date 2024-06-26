import time
from threading import Thread

import requests
import sseclient  # pip install sseclient-py
import json

from colorama import Fore

from src.processors import silero_processor

prompt = f"""
    You a super-duper voice assistant, you really want to help anyone who asks you about anything.
    
    Cause you are a voice assistant you should try to be short with your answers.
    
    You also should spell any number like it is a word, for example:
    You must not say 21, you answer twenty one.
    
    Your name is {silero_processor.speaker}
"""

greeting = "Hello! I'am here to help you"


class NeuralProcessor:
    history_start_time = time.time()

    thread: Thread = None

    client: sseclient.SSEClient

    history = [{"role": silero_processor.speaker, "content": greeting}]

    url = "http://127.0.0.1:7860/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    def process(self, user_message, on_data_callback):
        if self.thread is not None:
            if self.thread.is_alive():
                self.client.close()

        self.thread = Thread(target=self.__process, args=[user_message, on_data_callback])
        self.thread.start()

    def __process(self, user_message, on_data_callback) -> None:
        current_history_start = time.time()

        print(Fore.MAGENTA + "Neural network is answering!" + Fore.RESET)

        self.history.append({"role": "user", "content": user_message})
        data = {
            "mode": "instruct",
            "stream": True,
            "messages": self.history,
            "prompt": prompt,
            "character": silero_processor.speaker
        }

        try:
            stream_response = requests.post(self.url, headers=self.headers, json=data, verify=False, stream=True)

            self.client = sseclient.SSEClient(stream_response)

            if current_history_start != self.history_start_time:
                self.client.close()

            assistant_message = ''
            for event in self.client.events():
                payload = json.loads(event.data)
                chunk = payload['choices'][0]['message']['content']

                on_data_callback(chunk)

                assistant_message += chunk
                print(Fore.MAGENTA + chunk + Fore.RESET, end='')

            self.client = None

            print()
            self.history.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            print(Fore.RED + f"Some errors occupied during streaming nural response: {e}" + Fore.RESET)

    def is_alive(self) -> bool:
        if self.thread is None:
            return False

        return self.thread.is_alive()

    def clear(self) -> None:
        self.stop()
        self.history = [{"role": silero_processor.speaker, "content": greeting}]

    def stop(self):
        self.history_start_time = time.time()

        if self.client is not None:
            self.client.close()
