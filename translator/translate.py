"""
This is a simple, yet powerful command line translator with
mymemory.translated.net translate and google translator behind it. 
You can also use it as a Python module in your code.
"""
from abc import ABC
from abc import abstractmethod

from textwrap import wrap

from requests import get
from requests.utils import quote

import googletrans


class TranslatorBase(ABC):
    @abstractmethod
    def translate(self, text):
        pass


class MyMemoryTranslator(TranslatorBase):
    """mymemory.translated.net"""

    base_url = "http://mymemory.translated.net"

    def __init__(self, from_lang, to_lang):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        if self.from_lang != self.to_lang:
            self.source_list = wrap(source, 1000, replace_whitespace=False)
            source = " ".join(
                self._get_translation(s) for s in self.source_list
            )
            return source
        return source

    def _get_translation(self, source):
        data = self._get_json(source)
        translation = data["responseData"]["translatedText"]
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data["matches"]
            for match in matches:
                if not isinstance(match["translation"], bool):
                    next_best_match = match["translation"]
                    break
            return next_best_match

    def _get_json(self, source):
        escaped_source = quote(source, "")
        query = (
            f"/api/get?q={escaped_source}"
            f"&langpair={self.from_lang}|{self.to_lang}"
        )
        url = self.base_url + query
        resp = get(url)
        return resp.json()


class GoogleTranslator(TranslatorBase):
    def __init__(self, from_lang, to_lang):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.__translator = googletrans.Translator()

    def translate(self, text):
        text = self.__translator.translate(
            text, src=self.from_lang, dest=self.to_lang
        )
        return text.text


class Translator:
    options = {
        "google": GoogleTranslator,
        "mymemory": MyMemoryTranslator,
    }

    def __init__(self, from_lang, to_lang, source):
        self.__translator = self.set_translator(source)(from_lang, to_lang)

    def translate(self, text):
        return self.__translator.translate(text)

    def set_translator(self, option):
        _translator = self.options.get(option, None)

        if _translator is None:
            raise Exception(
                "The source does not exist. Try `google` or `mymemory`."
            )
        return _translator
