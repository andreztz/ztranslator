import argparse

from unittest.mock import MagicMock
from unittest.mock import patch

import translator
from translator import Translator
from translator.cli import main

text = "Hello World!"
source_lang = "en"
target_lang = "pt"
provider_api = "mymemory"
expected_text = "Hello World!"


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
        translator.cli, "Translator", return_value=translator_mock
    ) as _mock:
        translator.cli.main()
        _mock.assert_called_once_with(
            source_lang=source_lang,
            target_lang=target_lang,
            provider_api=provider_api,
        )
        translator_mock.translate.assert_called_once_with(expected_text)


def test_main(capfd):
    text = "Hello World!"
    source_lang = "en"
    target_lang = "pt"
    provider_api = "google"
    expected_text = "Olá Mundo!"


    NAMESPACE = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "provider_api": provider_api,
        "notify": False
    }

    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(**NAMESPACE)):
        main()
        out, _ = capfd.readouterr()
        assert out.strip() == expected_text
