# Seed

Aqui são criados alguns dados para facilitar o desenvolvimento
e alguns testes manuais. Dados como universidade, unidades consumidoras, 
contratos e etc. Leia o script para entender como eles se relacionam.

O seed de demonstração popula o banco com dados da UNB e da
UFMG.

Os comandos a seguir também devem ser executados dentro do container da api 
(mepa-api).


## Comandos

Exemplo:
```sh
docker exec mepa-api bash -c "./scripts/seed.sh"
```

Super User + Seed Demo:
```sh
./scripts/seed.sh
```

Super User:
```sh
./scripts/create-superuser.sh
```

Seed Demo:
```sh
./scripts/seed_demo.sh
```

Seed Teste de Usabilidade
```sh
./scripts/seed_ut.sh
```
Exemplo: Criar 20 universidades para teste
```sh
docker exec mepa-api bash -c "./scripts/seed_ut.sh 20"
```
 
Apagar os dados do banco de dados:

```sh
./scripts/dbflush.sh
```
