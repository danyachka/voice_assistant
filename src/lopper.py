from src.processors.silero_processor import SileroProcessor
from src.processors.vosk_processor import VoskProcessor

super_long_text = "один, два, три, четыре, пять, шесть, семь, восемь, девять, десять"

class MainLooper:

    voskProcessor: VoskProcessor

    sileroProcessor: SileroProcessor

    def __init__(self, config):
        self.voskProcessor = VoskProcessor()
        self.sileroProcessor = SileroProcessor(config.silero_model, config.cores)

    def startMainLoop(self):

        while True:

            recognized = self.voskProcessor.listen()
            if len(recognized) == 0:
                continue

            text = self.processText(recognized)

            self.sileroProcessor.say(f"Вы сказали: {text} {super_long_text}")
            while self.sileroProcessor.is_playing_thread_alive():
                recognized = self.voskProcessor.listen()
                if len(recognized) == 0:
                    continue

                if recognized == "стоп":
                    self.sileroProcessor.stop()

    def processText(self, text: str) -> str:
        match text.split(" ")[0]:
            case "загугли":
                # process command
                return "Гуглю как бы"

        return text

