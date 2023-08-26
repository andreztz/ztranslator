# ztranslator

[English version](https://github.com/andreztz/ztranslator/blob/main/README.en.md)

**ztranslator** é uma ferramenta de linha de comando que traduz texto entre diferentes idiomas. Com ele, é possível traduzir texto da área de transferência, inserir o texto traduzido na área de transferência, traduzir texto fornecido pela linha de comando e escolher o provedor de API de tradução. Por padrão, o ztranslator utiliza a API do Goolge Translate.

## Funcionalidades


As principais funcionalidades do ztranslator são:

- Tradução de texto da área de transferência
- Inserção do texto traduzido na área de transferência
- Tradução de texto fornecido pela linha de comando 
- Escolha do provedor de API de tradução (Google Translate ou MyMemory)

## Requisitos:


É necessário ter o python 3.8 ou superior instalado no computador.

## Instalação:


Para instalar o ztranslator, basta executar o seguinte comando no terminal:

```ruby
$ pip install ztranslator
```

## Opções da linha de comando 


- `--target-lang`: Especifica o idioma de destino para a tradução. O padrão é o 
idioma definido como padrão no seu sistema operacional. 
- `--source-lang`: Especifica o idioma de origem para a tradução.
- `--notify`: Traduz o texto da área de transferência, exibe-o como uma notificação.
- `--text`: Traduz o texto especificado.
- `--provider-api`: Define o provedor de API para tradução. O padrão é o `google`.

## Exemplos de uso:


A seguir, temos alguns exemplos de uso do ztranslator:

### Linha de comando:


Traduzir texto da área de transferência e exibir como notificação:

```
ztranslator --notify
``` 

Traduzir um texto fornecido pela linha de comando: 

```
ztranslator --text "Olá, como vai você?" --source-lang pt --target-lang en
```

Traduzir um texto fornecido pela linha de comando usando um provedor de API específico: 

```
ztranslator --text "Bonjour" --provider-api mymemory --source-lang fr --target-lang en
```

**Observações:**

- A opção `--source-api` foi descontinuada nessa versão. É recomendado usar `--provider-api` ao invés.
- Se nenhum texto é dado como entrada, a primeira opção da área de transferência é usada como entrada.
- O programa sempre colocará o texto traduzido na área de transferência.


### Exemplo de uso em python:


A seguir podemos ver como é fácil e intuitivo usar a biblioteca do ztranslator para tradução de textos em diferentes idiomas. 


```python
# Importe a classe Translator da biblioteca translator
from translator import Translator

# Crie uma instância da classe Translator com os parâmetros de 
# idioma de origem, idioma de destino e provedor de API
t = Translator(source_lang="pt", target_lang='en', provider_api="google")

# Chame o método translate() da instância criada e passe o texto a ser traduzido como parâmetro
text = t.translate("Type copyright, credits or license for more information")

# Imprima o resultado da tradução
print(text)
```

## Configuração para Desenvolvimento


```sh
# Clone o repositorio do ztranslator
$ git clone https://github.com/andreztz/ztranslator.git

# Entre na pasta do projeto
$ cd ztranslator

# Crie um ambiente virtual Python
$ virtualenv venv

# Ative o ambiente virtual 
$ source venv/bin/activate

# Instale o ztranslator em modo desenvolvimento
$ pip install -e .
```

## Histórico de lançamento


-   1.1.0 - Altera nome do parâmetro `--source-api` para `-provider-api`
-   1.0.0 - Altera interface da API e linha de comando.
-   0.1.0 - Adiciona acesso a API do Google Translate via googletrans.
-   0.0.7 - O primeiro lançamento adequado.
    -   Trabalho em andamento

André P. Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com

[https://github.com/andreztz/ztranslator](https://github.com/andreztz/)

## Contribua

Gostou do ztranslator e quer ajudar a torná-lo ainda melhor? Contribua com o projeto enviando suas sugestões e melhorias através de Pull Requests no GitHub. Sua contribuição pode ser uma funcionalidade nova, correção de bugs, melhoria da documentação ou tradução do projeto para outras línguas. Contribuir para projetos de código aberto é uma ótima maneira de aprender, desenvolver suas habilidades técnicas, construir sua reputação e contribuir para a comunidade de desenvolvimento de software. Siga os passos abaixo para enviar sua contribuição:


1. Faça um fork do repositório em <https://github.com/andreztz/ztranslator/fork>
2. Crie um branch para sua contribuição `git checkout -b feature/sua_contribuicao`
3. Faça as alterações necessárias
4. Commit suas alterações `git commit -am 'Adiciona nova contribuição'`
5. Faça um push para o branch (`git push origin feature/sua_contribuicao`)
6. Abra um Pull Request em https://github.com/andreztz/ztranslator/pulls e aguarde a revisão da sua contribuição;
