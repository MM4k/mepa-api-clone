# Testes

Os testes da API foram feitos com [Pytest](https://docs.pytest.org/en/7.2.x/) 
como base para testes e 
[pytest-django](https://pytest-django.readthedocs.io/en/latest/)  para acesso
ao banco de dados.

## Execução dos testes

Vamos passar por alguns comandos básicos.

Para executar **todos** os testes, dentro do container, execute simplesmente:

```sh
docker exec mepa-api bash -c "python -m pytest"
```

Para executar alguns casos de teste específicos segundo uma expressão, execute:

```sh
docker exec mepa-api bash -c "python -m pytest -k <expressao>
```

`<expressao>` é uma string que deve combinar com parte do nome de algum 
arquivo, caso ou método/função de teste. Para rodar os testes de endpoint de
tarifa, por exemplo, você poderia usar

```sh
docker exec mepa-api bash -c "python -m pytest -k tariffs_endpoint
```

Além disso, ainda é possível selecionar um dado de entrada específico para um caso
de teste parametrizado. Observe `tests/test_cnpj_validator.py`. Para testar
`test_accepts_valid_cnpj` com o CNPJ `58577114000189`, você poderia rodar:

```sh
pytest -k test_accepts_valid_cnpj[58577114000189]
# ou simplesmente
pytest -k 58577114000189
```

O primeiro comando é mais específico e mais seguro de rodar o teste desejado.
O segundo assume que o teste desejado é o único caso de teste com o dado CNPJ
no nome. Leia mais sobre parametrização no Pytest 
[aqui](https://docs.pytest.org/en/6.2.x/parametrize.html).

## Flags úteis

Se você tá rodando todos os testes várias vezes, pode ser que a execução fique 
lenta. Isso acontece por que o comportamento padrão é destruir o banco de dados
ao fim da execução. Assim, para manter o banco, use o seguinte:

```
pytest --reuse-db
```

Nesse caso, você pode notar que os IDs que usam auto increment **não são resetados**. 
Você deve fazer
os seus testes de maneira que os IDs _não estejam hard coded_, mas sim 
parametrizados. Leia os testes já implementados para ter uma ideia.

Além disso, as flags podem ser combinadas:

```
pytest --reuse-db -k tariffs_endpoint
```

## Útil se você usa VSCode 

Se você montou o seu [ambiente de desenvolvimento](./ambiente-desenvolvimento.md)
com VSCode e gosta de atalhos, essa parte é pra você.

### Configuração

Instale a extensão 
[Test Explorer UI](https://github.com/hbenl/vscode-test-explorer) no container 
da API.

No seu `.vscode/settings.json` adicione o seguinte:

```js
{
    "python.testing.pytestArgs": [
        "--reuse-db"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    // configure como quiser
    "testExplorer.mergeSuites": true,
    "testExplorer.sort": "byLocation",
}
```

Veja mais opções de configuração da extensão 
[aqui](https://github.com/hbenl/vscode-test-explorer#configuration).

### Atalhos VSCode

Abra a palheta de comandos com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> e 
digite "Test run" ou "Test debug". A palheta deve filtrar os comandos do VSCode 
relacionados à execução ou à depuração de testes. Então observe o atalho à 
direita da linha.

Alguns dos mais úteis (esses atalhos foram tirados do VSCode em Linux. Os atalhos
reais podem ser encontrados na palheta de comandos como explicado no parágrafo
anterior):

- <kbd>Ctrl</kbd>+<kbd>;</kbd>+<kbd>A</kbd>: executar todos os testes
- <kbd>Ctrl</kbd>+<kbd>;</kbd>+<kbd>L</kbd>: executar os testes executados na última sessão
- <kbd>Ctrl</kbd>+<kbd>;</kbd>+<kbd>C</kbd>: executar teste no cursor
- <kbd>Ctrl</kbd>+<kbd>;</kbd> <kbd>Ctrl</kbd>+<kbd>C</kbd>: depurar teste no cursor

De maneira geral, note que nos comandos que iniciam uma sessão de depuração, a 
segunda letra é precedida por um segundo <kbd>Ctrl</kbd>. 


## `pytest.django_db`
Em vários lugares, você pode notar que várias suites de testes estão decoradas
com `@pytest.django_db`. Esse decorador indica que a respectiva suite de testes
precisa se conectar com o banco de dados "direta" ou indiremente. 

A conexão com o banco de dados acontece **"diretamente"** quando o teste usa 
`Contract.objects.create(...)` em algum lugar das suas funções. 

Por outro lado, o uso **indireto** se dá quando o teste usa o cliente HTTP do 
Django REST para enviar requisições à API que podem ocasionar consultas ao 
banco de dados.

Se o seu teste precisar se conectar com o banco de dados, use 
`@pytest.django_db`. Se você esquecer, o Pytest vai te avisar.

Leia mais na documentação do 
[pytest-django](https://pytest-django.readthedocs.io/en/latest/database.html).

---

Volte para o [README](../README.md) principal.
