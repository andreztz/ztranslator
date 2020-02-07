# ztranslator

Simples tradutor de linha de comando, com mymemory.translated.net por trás. Você pode configurar uma combinação de teclas de atalho para que execute o ztranslator. Para isso basta passar --notify como parametro, que o ztranslator se encarrega de pegar a última entrada na área de transferência e exibir o texto traduzido em um simpático balãozinho no seu desktop.

![](header.gif)

## Instalação:

```sh
$ pip install ztranslator
```

## Exemplos de uso:

#### Na linha de comando:

```sh
$ ztranslator --help
```

```sh
$ python -m translator --help
```

#### Como um módulo python:

```python
In [1]: from translator import Translator

In [2]: t = Translator(to_lang='pt-br')

In [3]: t.translate("Type copyright, credits or license for more information")
Out[3]: 'Digite copyright, créditos ou licença para mais informações'
```

## Configuração para Desenvolvimento

```sh
$ git clone https://github.com/andreztz/ztranslator.git
$ cd ztranslator
$ virtualenv venv
$ source venv/bin/activate
$ pip install -e .
```

## Histórico de lançamento

-   0.0.7 - O primeiro lançamento adequado.
    -   Trabalho em andamento

André Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com

[https://github.com/andreztz/ztranslator](https://github.com/andreztz/)

## Contribua

1. Fork it (<https://github.com/andreztz/ztranslator/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
