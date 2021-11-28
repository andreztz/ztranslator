#!/usr/bin/env python3

import argparse
import locale

from translator import clip
from notify import notification

from translator.translate import Translator

default_locale = locale.getdefaultlocale()[0]
to_lang = default_locale.split(".")[0].lower().replace("_", "-")


help_notify = """Translates text from the clipboard, displays it \
as notification, and places the translated text in the clipboard.
"""

help_source = """The API translation can be from google or mymemory. \
Default is google.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-lang", default="pt", help="Target language.")
    parser.add_argument("--source-lang", default="en", help="Source language.")
    parser.add_argument("--notify", action="store_const", const=True, help=help_notify)
    parser.add_argument("--text", nargs="+", help="Translates command line input text.")
    parser.add_argument(
        "--source-api",
        choices=["google", "mymemory"],
        default="google",
        help=help_source,
    )

    args = parser.parse_args()

    text = " ".join(args.text) if args.text else clip.get()

    translator = Translator(
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        source_api=args.source_api,
    )

    translated_text = translator.translate(text)

    if args.notify:
        notification(translated_text, app_name="ztranslation")
    else:
        print(translated_text)

    clip.set(translated_text)
