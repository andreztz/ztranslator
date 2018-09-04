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

## Usage example as Script

```sh
    $ python -m translator --help
```

or

```sh
    $ ztranslator --help
```

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

```sh
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Release History

- 0.0.3
  - Work in progress

## Meta

André Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com

Distributed under the XYZ license. See `LICENSE` for more information.

[https://github.com/andreztz/ztranslator](https://github.com/andreztz/)

## Contributing

1. Fork it (<https://github.com/andreztz/ztranslator/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->

[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
