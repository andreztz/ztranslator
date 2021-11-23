#!/usr/bin/env python3

import argparse
import locale

from translator import clip
from notify import notification

from translator.translate import Translator

default_locale = locale.getdefaultlocale()[0]
to_lang = default_locale.split(".")[0].lower().replace("_", "-")


help_notify = """translates text from the clipboard, displays it \
as notification, and places the translated text in the clipboard.
"""

help_source = """Translation source may be google or mymemory. Default is google.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--to-lang", default="pt", help="to language")
    parser.add_argument("--from-lang", default="en", help="from language")
    parser.add_argument(
        "--notify", action="store_const", const=True, help=help_notify
    )
    parser.add_argument(
        "--text", nargs="+", help="translates command line input text"
    )
    parser.add_argument(
        "--source",
        choices=["google", "mymemory"],
        default="google",
        help=help_source,
    )

    args = parser.parse_args()

    text = " ".join(args.text) if args.text else clip.get()

    translator = Translator(
        from_lang=args.from_lang, to_lang=args.to_lang, source=args.source
    )

    translated = translator.translate(text)

    if args.notify:
        notification(translated, app_name="ztranslation")
    else:
        print(translated)

    clip.set(translated)
