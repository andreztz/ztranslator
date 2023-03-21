import argparse

from unittest.mock import MagicMock
from unittest.mock import patch

import translator
from translator import Translator
from translator.__main__ import main

text = "Hello World!"
source_lang = "en"
target_lang = "pt"
provider_api = "mymemory"
expected_text = "H e l l o   W o r l d !"


NAMESPACE = {
    "text": text,
    "source_lang": source_lang,
    "target_lang": target_lang,
    "provider_api": provider_api,
    "notify": False,
}


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(**NAMESPACE),
)
def test_cli_is_callled_with_correct_params(_):
    translator_mock = MagicMock(spec=Translator)
    translator_mock.translate.return_value = "Olá Mundo!!"
    with patch.object(
        translator.__main__, "Translator", return_value=translator_mock
    ) as _mock:
        translator.__main__.main()
        _mock.assert_called_once_with(
            source_lang=source_lang,
            target_lang=target_lang,
            provider_api=provider_api,
        )
        translator_mock.translate.assert_called_once_with(expected_text)
