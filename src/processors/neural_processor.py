import requests
import sseclient  # pip install sseclient-py
import json


class NeuralProcessor:

    history = []

    url = "http://127.0.0.1:5000/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    def process(self) -> None:
        pass

    def is_alive(self) -> bool:
        return False
