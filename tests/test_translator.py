import pytest
from translator import Translator


def test_translator_hello_world():
    translator = Translator(from_lang="en", to_lang="pt", source="google")
    assert translator.translate('Hello World') == 'Olá Mundo'


def test_translator_source_not_found():

    with pytest.raises(Exception) as excinfo:
        Translator(from_lang="en", to_lang="pt", source="googles")

    error_message = "The source does not exist. Try `google` or `mymemory`."
    assert error_message in str(excinfo.value)


