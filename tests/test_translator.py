import pytest
from translator import Translator
from translator.translate import SourceNotFound
from translator.translate import SourceManager
from translator.translate import TranslatorBase


def test_translator_hello_world():
    translator = Translator(source_lang="en", target_lang="pt", source_api="google")
    assert translator.translate("Hello World") == "Olá Mundo"


def test_translator_source_api_not_found():

    with pytest.raises(SourceNotFound) as excinfo:
        Translator(source_lang="en", target_lang="pt", source_api="googles")

    error_message = "The source API does not exist. Try `google` or `mymemory`."
    assert error_message in str(excinfo.value)


def test_api_manager():
    source = SourceManager("google").get(source_lang="pt", target_lang="eng")
    assert isinstance(source, TranslatorBase)
