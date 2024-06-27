import time
import re

from num2words import num2words

from googletrans import Translator


class LanguageTranslator:

    translator = Translator()

    def translate_to_english(self, russian_text):
        if len(russian_text) == 0:
            return ''
        result = self.translator.translate(russian_text, src='ru', dest='en')
        return result.text

    def translate_to_russian(self, english_text):
        english_text = self.replace_numbers_with_words(english_text)
        if len(english_text) == 0:
            return ''
        result = self.translator.translate(english_text, src='en', dest='ru')
        return result.text

    def replace_numbers_with_words(self, text):
        pattern = r'\d+'

        result = re.sub(pattern, lambda x: num2words(int(x.group())), text)

        return result


if __name__ == '__main__':
    russian = ''

    t = LanguageTranslator()

    start = time.time()
    english = t.translate_to_english(russian)
    print(f"time: {time.time() - start} {english}")

    start = time.time()
    russian = t.translate_to_russian(english)
    print(f"time: {time.time() - start} {russian}")
