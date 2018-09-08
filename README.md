# ZTranslator

> ztranslator

This is a simple, yet powerful command line translator with mymemory.translated.net translate behind it. You can also use it as a Python module in your code.

![](header.png)

## Installation

```sh
    $ pip install ztranslator
```

## Usage as module

```sh
    In [1]: from translator import Translator

    In [2]: t = Translator(to_lang='pt-br')

    In [3]: t.translate("Type copyright, credits or license for more information")
    Out[3]: 'Digite copyright, créditos ou licença para mais informações'
```

## Usage as Script

```sh
    $ python -m translator --help
```

or

```sh
    $ ztranslator --help
```

## Release History

- 0.0.3
  - Work in progress

## Meta

André Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com

[https://github.com/andreztz/ztranslator](https://github.com/andreztz/)

## Contributing

1. Fork it (<https://github.com/andreztz/ztranslator/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
