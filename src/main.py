import json
import sys
from dataclasses import dataclass

from src.lopper import MainLooper
from src.processors import neural_processor


@dataclass
class Config:
    silero_model: str
    cores: int
    name: str


def read_configuration():
    file = open('configuration.json')

    json_str = file.read()
    data = json.loads(json_str)
    return Config(data["silero_model"], data["cores"], data["name"])


if __name__ == '__main__':
    try:
        config = read_configuration()
    except Exception as e:
        print(f"Some problems with configuration reading: {e}")
        sys.exit(1)

    neural_processor.assistant_role_name = config.name

    prompt = open("prompt.txt", "r")
    neural_processor.prompt = prompt.read()
    prompt.close()

    looper = MainLooper(config)

    looper.start_main_loop()
