from src.processors.silero_processor import SileroProcessor
from src.processors.vosk_processor import VoskProcessor


class MainLooper:

    voskProcessor: VoskProcessor

    sileroProcessor: SileroProcessor

    def __init__(self, config):
        self.voskProcessor = VoskProcessor()
        self.sileroProcessor = SileroProcessor(config.model, config.cores)

    def startMainLoop(self):

        while True:

            recognized = self.voskProcessor.listen()
            print(recognized)

            self.sileroProcessor.say(f"Вы сказали: {recognized}")
