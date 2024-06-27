import time
import traceback
from threading import Thread

import re

import requests
import sseclient  # pip install sseclient-py
import json

from colorama import Fore

from src.processors import silero_processor

assistant_role_name = "xenia"

prompt = f"""
name: xenia
greeting: How can I help you today?
context: | 
  You a super-duper voice assistant, you really want to help anyone who asks you about anything.
  Cause you are a voice assistant you MUST answer briefly
  You don't use number symbols, only words
  Dont give any notes.

  {{user}}: Who are you?
  {{xenia}}: I'm super-duper voice assistant.
  {{user}}: When did USSR collapsed.
  {{xenia}}: In one thousand nine hundred and ninety-one.
  {{user}}: How many days in Jule
  {{xenia}}: Thirty one.
  {{user}}: How to wash the plates?
  {{xenia}}: Wash plates with warm soapy water, scrub off food residue, and rinse thoroughly. Dry with a towel or let air dry to prevent water spots.
  {{user}}: How to create a directory in linux using terminal?
  {{xenia}}: mkdir and your directoty name after.
  {{user}}: When bluetooth was developed?
  {{xenia}}: In nineteen ninety four.
"""

greeting = "Hello! I'am here to help you"


class NeuralProcessor:
    history_start_time = time.time()

    thread: Thread = None

    client: sseclient.SSEClient

    history = [{"role": "xenia", "content": greeting}]

    url = "http://127.0.0.1:9001/v1/chat/completions"

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
        current_history_start = self.history_start_time

        print(Fore.MAGENTA + "Neural network is answering!" + Fore.RESET)

        self.history.append({"role": "user", "content": user_message})

        hist = json.dumps(self.history)
        print(Fore.MAGENTA + f"history : {hist}" + Fore.RESET)

        data = {
            "messages": self.history,
            ##
            "prompt": prompt,
            "mode": "chat",
            "character": "xenia",
            ##
            "instruction_template": "Alpaca",
            "stream": True,
            "max_tokens": 500
        }

        try:
            stream_response = requests.post(self.url, headers=self.headers,
                                            json=data, verify=False, stream=True)
            # print(f"Server response: {stream_response.json()}")

            self.client = sseclient.SSEClient(stream_response)

            if current_history_start != self.history_start_time:
                self.client.close()

            assistant_message = ''

            temporal_message = ''
            try:
                for event in self.client.events():
                    payload = json.loads(event.data)
                    print(json.dumps(payload))
                    chunk = payload['choices'][0]['delta']['content']

                    if chunk is not None:
                        assistant_message += chunk
                        temporal_message += chunk

                        text, temporal_message = process_new_chunk_dots(temporal_message)
                        if len(text) != 0:
                            on_data_callback(text)
                        if "\n" in temporal_message or "\n" in chunk:
                            self.stop()
                    print(Fore.MAGENTA + chunk + Fore.RESET, end='')
            except:
                pass

            if len(temporal_message) > 1:
                on_data_callback(temporal_message)

            self.client = None

            print(Fore.MAGENTA + assistant_message + Fore.RESET)
            self.history.append({"role": assistant_role_name, "content": assistant_message})
        except Exception as e:
            print(Fore.YELLOW + f"Some errors occupied during streaming nural response" + Fore.RESET)
            traceback.print_exc()

    def is_alive(self) -> bool:
        if self.thread is None:
            return False

        return self.thread.is_alive()

    def clear(self) -> None:
        self.history_start_time = time.time()

        self.stop()
        self.history = [{"role": assistant_role_name, "content": greeting}]

    def stop(self):

        if self.client is not None:
            self.client.close()


def process_new_chunk_spaces(temporal_message):
    split = temporal_message.split()
    text = ""
    chunk_len = 10
    if len(split) > chunk_len:
        text = " ".join(split[:chunk_len])

        temporal_message = " ".join(split[chunk_len:])

    return text, temporal_message


def process_new_chunk_dots(temporal_message):
    pattern = r'[.?,:]'

    if re.search(pattern, temporal_message):
        result = re.split(pattern, temporal_message, maxsplit=1)
        return result[0], "".join(result[1:])

    return "", temporal_message


if __name__ == '__main__':
    tm = "1 2 3 4 5? 6 7. ?aboba?fdfdf"

    txt, tm = process_new_chunk_dots(tm)

    print(txt)
    print(tm)
