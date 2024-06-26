import time

from googletrans import Translator


class LanguageTranslator:

    translator = Translator()

    def translate_to_english(self, russian_text):
        result = self.translator.translate(russian_text, src='ru', dest='en')
        return result.text

    def translate_to_russian(self, english_text):
        result = self.translator.translate(english_text, src='en', dest='ru')
        return result.text


if __name__ == '__main__':
    russian = 'Кто ты?'

    t = LanguageTranslator()

    start = time.time()
    english = t.translate_to_english(russian)
    print(f"time: {time.time() - start} {english}")

    start = time.time()
    russian = t.translate_to_russian(english)
    print(f"time: {time.time() - start} {russian}")