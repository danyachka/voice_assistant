import json
import sys
from dataclasses import dataclass

from src.lopper import MainLooper


@dataclass
class Config:
    model: str
    cores: int


def read_configuration():
    file = open('configuration.json')

    json_str = file.read()
    data = json.loads(json_str)
    return Config(data["model"], data["cores"])


if __name__ == '__main__':
    try:
        config = read_configuration()
    except Exception as e:
        print(f"Some problems with configuration reading: {e}")
        sys.exit(1)

    looper = MainLooper(config)

    looper.startMainLoop()

