#!/usr/bin/env python3

import argparse
import locale

from translator import clip
from notify import Notification

from translator.translate import Translator

default_locale = locale.getdefaultlocale()[0]
to_lang = default_locale.split(".")[0].lower().replace("_", "-")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", nargs="?", default=to_lang, help="to lang")
    parser.add_argument("--notify", nargs="?", const=True, help="notify")
    parser.add_argument("--text", help="text")
    args = parser.parse_args()

    text = args.text if args.text else clip.get()

    translator = Translator(to_lang=args.lang)
    translated = translator.translate(text)
    if args.notify:
        Notification("Translator", translated).notify()
    else:
        print(translated)

    clip.set(translated)
