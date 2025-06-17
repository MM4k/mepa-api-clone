# Ambiente de desenvolvimento

Vamos assumir que você seguiu os passos do [README](/README.md) e que 
`.env.dev` foi copiado para `.env`.

Lembre-se que você deve ter 
[Docker Compose](https://docs.docker.com/compose/install/) instalado  em sua
máquina.

## Docker Compose

O projeto da API é conteinerizado com Docker e possui dois serviços: API e 
banco de dados.

### API

Para verificar se os containeres estão de pé

```sh
docker ps
```

Devem aparecer listados os containeres da API e do banco de dados.

Para se conectar ao terminal da API

```sh
docker exec -it mepa-api bash
```

Note que o prompt mudou e está mais ou menos assim:

```
dev@bee825eebbb9:~/mepa-api-api$
```

O comando abre uma conexão com o container da API e com ela você consegue
executar comandos como em um terminal normal. Mas note que o que está 
disponível nesse terminal é o que foi definido e configurado no 
[Dockerfile](../Dockerfile) da API. Experimente executar 

```
./manage.py shell
```

Você também pode executar os testes com

```
python -m pytest
```

Para sair use `exit` ou <kbd>Ctrl</kbd>+<kbd>D</kbd>. Você deve voltar para
o prompt normal da _sua_ máquina.

Alternativamente, você pode apenas executar um comando dentro do container
sem abrir um terminal para o container:

```
docker exec mepa-api bash -c "python -m pytest"
```

Assim que o comando terminar de executar, o prompt deve voltar ao normal da sua
máquina. Note o uso do `-c` e que a flag `-it` não é necessária.

### Banco de dados

Semelhantemente, para conectar ao banco de dados, execute:

```
docker exec -it mec-energia-db bash -c "psql -U postgres -W"
```

Digite a senha que está em `.env.dev` na variável `POSTGRES_PASSWORD`. O seu 
prompt deve estar algo assim:


```
psql (<Alguma versão aí>)
Type "help" for help.

postgres=# 
```

Você está dentro de `psql`, dentro de `bash` e dentro do container do banco de 
dados. Para saber mais como o banco de dados está configurado consulte 
`docker-compose.yml` no serviço `mec-energia-db`.

Outra maneira de se conectar ao banco de dados é por um programa cliente
de banco de dados relacional como [DBeaver](https://dbeaver.io/), 
[Beekeeper Studio](https://www.beekeeperstudio.io/) ou 
[pgAdmin 4](https://www.pgadmin.org/). Esses clientes são open source e cross
platform. Para qualquer cliente desses, quando for criar a conexão, use 
`localhost` (ou `127.0.0.1`) como _host_ e o valor da variável ambiente
`POSTGRES_PASSWORD` como _password_.

### Outros comandos

Outros comandos comumente usados em projetos com docker são `logs`, `volume`, 
`system prune` etc. Você pode ler mais sobre eles na documentação 
[Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/).


## Django

O servidor é iniciado com `./manage.py runserver 0.0.0.0`. Você não precisa
executar esse comando porque ele já é usado em `scripts/start.sh`. Além disso,
`start.sh` executa outros comandos:

- `./manage.py makemigrations`: cria arquivos de migração
- `./manage.py migrate`: executa migrações descritas nos arquivos de migração

Se você mudou alguma coisa em `models.py` de algum app do Django, você deve
executar `./manage.py makemigrations` e depois `./manage.py migrate`.

Para reverter todas as migrações de um app: `./manage.py migrate <app> zero`


## Padrões de Código

Ruff utilizado para garantir os padrões de qualidade de código adotados no projeto

**Para executar localmente:**

```bash
# Verificar problemas
ruff check .

# Formatar código
ruff format .

# Corrigir problemas automaticamente
ruff check . --fix
```

**Configurando o código VSCode:**

Configurar o Ruff para formatar o código Python ao salvar ativando o editor.formatOnSave 
ação em settings.json e definindo Ruff como seu formatador padrão:

```json
# precisa 
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff"
    "editor.codeActionsOnSave": {
        "source.fixAll.ruff": "explicit",           // ruff check --fix . (Corrigir violações de lint ao salvar)
    }
  }
}

```

## VSCode

Se você usa [VSCode](https://code.visualstudio.com/) como editor de código, 
essas extensões podem ser úteis:

- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers): 
permite que você use um container Docker como um ambiente de desenvolvimento 
completo com VSCode
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python):
intellisense e autocomplete para Python
- [Test Explorer UI](https://marketplace.visualstudio.com/items?itemName=hbenl.vscode-test-explorer):
Lista e executa testes pelo VSCode (com atalhos. Leia [testes](testes.md#útil-se-você-usa-vscode))

- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff):
Uma ferramenta extremamente rápida Linter Python e formatador de código, escrito em Rust.
