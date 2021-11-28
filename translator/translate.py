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


class Error(Exception):
    pass


class SourceNotFound(Error):
    def __init__(self):
        message = "The source API does not exist. Try `google` or `mymemory`."
        super().__init__(message)


class TranslatorBase(ABC):
    @abstractmethod
    def translate(self, text):
        pass


class MyMemoryTranslator(TranslatorBase):
    """mymemory.translated.net"""

    base_url = "http://mymemory.translated.net"

    def __init__(self, source_lang, target_lang):
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate(self, source):
        if self.source_lang != self.target_lang:
            self.source_list = wrap(source, 1000, replace_whitespace=False)
            source = " ".join(self._get_translation(s) for s in self.source_list)
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
            f"&langpair={self.source_lang}|{self.target_lang}"
        )
        url = self.base_url + query
        resp = get(url)
        return resp.json()


class GoogleTranslator(TranslatorBase):
    def __init__(self, source_lang, target_lang):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.__translator = googletrans.Translator()

    def translate(self, text):
        text = self.__translator.translate(
            text, src=self.source_lang, dest=self.target_lang
        )
        return text.text


class SourceManager:
    sources = {"google": GoogleTranslator, "mymemory": MyMemoryTranslator}

    def __init__(self, source_api):
        self.api = source_api

    def get(self, source_lang, target_lang):
        translator = self.sources.get(self.api, None)
        if translator is None:
            raise SourceNotFound()
        return translator(source_lang, target_lang)


class Translator:
    def __init__(self, source_lang, target_lang, source_api):
        self._translator = SourceManager(source_api).get(source_lang, target_lang)

    def translate(self, text):
        return self._translator.translate(text)
