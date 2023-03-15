import pytest
from translator import Translator
from translator.translate import ProviderNotFound
from translator.translate import ProviderManager
from translator.translate import ProviderBase


def test_translator_hello_world():
    translator = Translator(
        source_lang="en", target_lang="pt", provider_api="google"
    )
    assert translator.translate("Hello World") == "Olá Mundo"


def test_translator_provider_api_not_found():

    with pytest.raises(ProviderNotFound) as excinfo:
        Translator(source_lang="en", target_lang="pt", provider_api="googles")

    error_message = "The provider does not exist. Try `google` or `mymemory`."
    assert error_message in str(excinfo.value)


def test_api_manager():
    source = ProviderManager("google").get(source_lang="pt", target_lang="eng")
    assert isinstance(source, ProviderBase)
