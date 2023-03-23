import argparse
import locale

from translator import clip
from notify import notification

from translator.translate import Translator

default_locale = locale.getdefaultlocale()[0]
to_lang = default_locale.split(".")[0].lower().replace("_", "-")


help_description = """
ZTranslator is a command-line tool that translates text between different languages.

You can use it to translate text from the clipboard, input text from the command line,
and choose the translation API provider. By default, ZTranslator uses Google Translate API.
"""

help_epilog = """
Examples:
  Translate text from the clipboard and display as notification:
    ztranslator --notify

  Translate specific text:
    ztranslator --text "Hello, how are you?" --source-lang en --target-lang pt

  Translate specific text with a specific API provider:
    ztranslator --text "Bonjour" --provider-api mymemory --source-lang fr --target-lang en

Note:
  - The '--source-api' option has been deprecated in this version, and it is recommended to use '--provider-api' instead.
  - If neither the '--notify' nor '--text' options are used, the program will wait for input from the user.
  - If the '--target-lang' option is not specified, the default target language is the language set as default on your system.
  - If the '--provider-api' option is not specified, the default provider is 'google'.
"""

help_notify = (
    "Translates text from the clipboard, displays it "
    "as a notification, and places the translated text in the clipboard."
)

help_provider_api = (
    "The API provider for translation. The available options are `google` and `mymemory`. "
    "The default option is google."
)
help_source_api = (
    "WARNING: The --source-api argument will be removed in the next version. "
    "Please use --provider-api instead."
)



def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=help_description,
        epilog=help_epilog,
    )
    parser.add_argument("--target-lang", default="pt", help="Specifies the target language for the translation.")
    parser.add_argument("--source-lang", default="en", help="Specifies the source language for the translation.")
    parser.add_argument(
        "--notify", action="store_const", const=True, help=help_notify
    )
    parser.add_argument(
        "--text", nargs="+", help="Translates the specified text."
    )
    parser.add_argument(
        "--source-api",
        choices=["google", "mymemory"],
        default="google",
        dest="provider_api",
        help=help_source_api,
    )
    parser.add_argument(
        "--provider-api",
        choices=["google", "mymemory"],
        default="google",
        help=help_provider_api,
    )

    args = parser.parse_args()

    text = "".join(args.text) if args.text else clip.get()

    translator = Translator(
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        provider_api=args.provider_api,
    )

    translated_text = translator.translate(text)

    if args.notify:
        notification(translated_text, app_name="ztranslation")
    else:
        print(translated_text)

    clip.set(translated_text)
