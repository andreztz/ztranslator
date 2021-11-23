import pytest
from translator import Translator
from translator.translate import SourceNotFound
from translator.translate import SourceManager
from translator.translate import TranslatorBase


def test_translator_hello_world():
    translator = Translator(from_lang="en", to_lang="pt", source="google")
    assert translator.translate('Hello World') == 'Olá Mundo'


def test_translator_source_not_found():

    with pytest.raises(SourceNotFound) as excinfo:
        Translator(from_lang="en", to_lang="pt", source="googles")

    error_message = "The source does not exist. Try `google` or `mymemory`."
    assert error_message in str(excinfo.value)


def test_source_manager():
    source = SourceManager('google').get(from_lang='pt', to_lang="eng")
    assert isinstance(source, TranslatorBase)
