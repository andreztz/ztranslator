# !/usr/bin/env python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <andreztz@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return to Terry Yin.
#
# The original idea of this is borrowed from <terry.yinzhe@gmail.com>'s
# ----------------------------------------------------------------------------

'''
This is a simple, yet powerful command line translator with
mymemory.translated.net translate behind it. You can also
use it as a Python module in your code.
'''

import json
from textwrap import wrap

from requests import get
from requests.utils import quote


class Translator:
    '''mymemory.translated.net'''

    def __init__(self, to_lang, from_lang='eng'):
        self.to_lang = to_lang
        self.from_lang = from_lang

    def translate(self, source):
        if self.from_lang != self.to_lang:
            self.source_list = wrap(source, 1000, replace_whitespace=False)
            source = ' '.join(
                self._get_translation(s) for s in self.source_list)
            return source
        return source

    def _get_translation(self, source):
        data = self._get_json(source)
        translation = data['responseData']['translatedText']
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data['matches']
            for match in matches:
                if not isinstance(match['translation'], bool):
                    next_best_match = match['translation']
                    break
            return next_best_match

    def _get_json(self, source):
        _escaped_source = quote(source, '')
        _base_url = 'http://mymemory.translated.net'
        _api_url = (
            f'/api/get?q={_escaped_source}'  # join f strings
            f'&langpair={self.from_lang}|{self.to_lang}')
        _headers = {}
        _url = _base_url + _api_url
        resp = get(_url)
        return resp.json()