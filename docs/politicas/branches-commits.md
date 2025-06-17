## Política de Branches

### Fluxo de Trabalho

- Toda nova **branch** criada e desenvolvida deve estar **linkada a uma issue**;
- O projeto seguirá o básico do **gitflow** para gerenciar a versão e funcionalidades testadas, validadas e entregues.

#### 1. Master
Essa é a branch que contém o código em nível de **produção**, ou seja, versão versão estável e disponível para o usuário final.

#### 3. Develop
É a branch principal de **desenvolvimento**. Contém a versão mais atualizada do código, integrando as novas funcionalidades finalizadas.

#### 4. Feature, Bug Fix ou Hotfix
É a branch destinada ao desenvolvimento de uma nova **funcionalidade e correção de bugs ou erros** do produto.


### Nome da Branch

```
<id_issue>/<descrição_funcionalidade>
```

```
999/criar_componente_editar_usuario
```

---

## Política de Commits

- Os commits devem ser claros e diretos, descrevendo as alterações feitas;
- Devem ser escritos em português no gerúndio.

### Conventional Commits

A especificação do Conventional Commits é uma convenção simples para utilizar nas mensagens de commit. Ela define um conjunto de regras para criar um histórico de commit explícito, o que facilita a criação de ferramentas automatizadas baseadas na especificação.

O commit contém os seguintes elementos estruturais, para comunicar a intenção ao utilizador da sua biblioteca:

- fix: um commit do tipo fix soluciona um problema na sua base de código (isso se correlaciona com PATCH do versionamento semântico);
- feat: um commit do tipo feat inclui um novo recurso na sua base de código (isso se correlaciona com MINOR do versionamento semântico);
- Para mais tipos de commits, acessar: [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/).


### Nome do Commit

```
<tipo>: <id_issue> <descrição>
```

```
feat: #5 Criando Documento de Visão
```