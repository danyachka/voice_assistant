from colorama import Fore

from src.processors.neural_processor import NeuralProcessor
from src.processors.silero_processor import SileroProcessor
from src.processors.vosk_processor import VoskProcessor
from src.translator import LanguageTranslator


class MainLooper:

    name = "ксения"

    voskProcessor: VoskProcessor

    sileroProcessor: SileroProcessor

    translator: LanguageTranslator

    neural: NeuralProcessor

    def __init__(self, config):
        self.voskProcessor = VoskProcessor()
        self.sileroProcessor = SileroProcessor(config.silero_model, config.cores)
        self.translator = LanguageTranslator()
        self.neural = NeuralProcessor()

    def start_main_loop(self):

        while True:

            recognized = self.voskProcessor.listen()

            recognized, is_call = self.check_if_call(recognized)
            if not is_call:
                continue

            if len(recognized) == 0:
                continue

            text, is_command = self.process_text_if_command(recognized)

            if is_command:
                self.sileroProcessor.say(f"Вы сказали: {recognized}")

            while self.sileroProcessor.is_processing() or self.neural.is_alive():
                recognized = self.voskProcessor.listen()
                if len(recognized) == 0:
                    continue

                if recognized == "стоп":
                    print(Fore.YELLOW + "Process stopped" + Fore.RESET)
                    self.sileroProcessor.stop()
                    self.neural.stop()

    def check_if_call(self, string) -> tuple[str, bool]:
        if len(string) == 0:
            return "", False

        words = string.split()

        is_call = words[0] in ["ксения", "ксении", "ксюша"]

        if is_call:
            string = " ".join(words[1:])

        return string, is_call

    def process_text_if_command(self, text: str) -> tuple[str, bool]:
        match text.split()[0]:
            case "загугли":
                return "Гуглю как бы", True
            case "адресс":
                return '127.0.0.1:7860', True

        english = self.translator.translate_to_english(text)

        self.neural.process(english,
                            lambda data: self.sileroProcessor.say(self.translator.translate_to_russian(data)))

        return "", False

