# projeto-banco-de-dados
# Gerenciador de Campeonato de Futebol

Aplicação de linha de comando em Python que gerencia um campeonato de futebol
(clubes, jogadores, partidas e gols) sobre um banco de dados PostgreSQL.

- **Disciplina:** Banco de Dados – Semestre 2026/2
- **Professor:** Howard Roatti
- **Grupo:** Betânia, Eduardo, Gabriel, Vinícius e Vitor

Este guia explica como executar o projeto no **Linux** (ambiente da VM da
disciplina). Os comandos são para distribuições baseadas em Debian/Ubuntu (`apt`).

---

## 1. Pré-requisitos

| Item | Versão mínima |
|---|---|
| Python | 3.10 (o código usa `match`/`case`) |
| PostgreSQL | 12 ou superior |
| Git | qualquer versão recente |

Confira o que já está instalado:

```bash
python3 --version
psql --version
git --version
```

## 2. Instalar as dependências do sistema

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib python3 python3-venv python3-pip git
```

Inicie o PostgreSQL e deixe-o ligado sempre que a máquina iniciar:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 3. Preparar o banco de dados

Defina uma senha para o usuário `postgres` (o exemplo usa `postgres`; troque se quiser):

```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

Crie o banco do projeto:

```bash
sudo -u postgres createdb campeonato
```

## 4. Baixar o projeto

```bash
git clone https://github.com/bianchini021/projeto-banco-de-dados.git
cd projeto-banco-de-dados
```

> Todos os comandos a partir daqui devem ser executados **dentro da pasta
> `projeto-banco-de-dados`**.

## 5. Configurar a conexão

A aplicação lê a conexão das variáveis de ambiente abaixo. Execute-as no mesmo
terminal em que o programa será iniciado:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=campeonato
export DB_USER=postgres
export PGPASSWORD=postgres
```

| Variável | Padrão | Função |
|---|---|---|
| `DB_HOST` | `localhost` | Endereço do servidor |
| `DB_PORT` | `5432` | Porta do PostgreSQL |
| `DB_NAME` | `postgres` | Nome do banco |
| `DB_USER` | `postgres` | Usuário |
| `PGPASSWORD` | — | Senha do usuário (lida diretamente pelo driver) |

> As variáveis valem só para o terminal aberto. Se fechar o terminal, rode os
> `export` de novo antes de iniciar o programa.
## 6. Criar as tabelas

```bash
psql -h localhost -U postgres -d campeonato -f src/SQL/schema.sql
```

O script cria as tabelas `clubes`, `jogadores`, `partidas` e `gols`. Ele pode
ser executado mais de uma vez sem erro (`CREATE TABLE IF NOT EXISTS`).

<!-- TODO (Gabriel): incluir aqui o comando para carregar os dados de teste,
     por exemplo:
     psql -h localhost -U postgres -d campeonato -f src/SQL/<arquivo_de_dados>.sql -->

## 7. Instalar as bibliotecas Python

Crie um ambiente virtual (necessário nas versões recentes do Ubuntu/Debian,
que bloqueiam `pip install` direto no sistema):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Sempre que abrir um terminal novo, ative o ambiente com
> `source .venv/bin/activate` antes de executar o programa.

## 8. Executar

Dentro da pasta do projeto, com o ambiente virtual ativo e as variáveis do
passo 5 definidas:

```bash
python3 -m src.main
```

> Use `python3 -m src.main`, e **não** `python3 src/main.py`: os imports do
> projeto começam com `src.` e só funcionam quando o programa é iniciado a
> partir da pasta raiz.

### Resumo para as próximas execuções

```bash
cd projeto-banco-de-dados
source .venv/bin/activate
export DB_NAME=campeonato PGPASSWORD=postgres
python3 -m src.main
```

---

## Estrutura do projeto

```
projeto-banco-de-dados/
├── README.md
├── PROMPTS.md                  # registro do uso de IA
├── requirements.txt
├── Regras de Negócio e Modelagem/   # diagrama relacional e regras
└── src/
    ├── main.py                 # ponto de entrada (menu principal)
    ├── Controlador/            # CRUD de cada tabela
    ├── Modelo/                 # classes das entidades
    ├── Relatórios/             # consultas dos relatórios
    ├── SQL/schema.sql          # criação das tabelas
    └── utils/                  # conexão, menus e configurações
```

## Problemas comuns

| Mensagem | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Programa iniciado fora da pasta raiz ou com `python3 src/main.py` | Entrar na pasta do projeto e usar `python3 -m src.main` |
| `ModuleNotFoundError: No module named 'psycopg'` | Ambiente virtual não ativado ou bibliotecas não instaladas | `source .venv/bin/activate` e `pip install -r requirements.txt` |
| `password authentication failed for user "postgres"` | `PGPASSWORD` não definido ou diferente da senha do passo 3 | Rodar `export PGPASSWORD=<senha>` |
| `database "campeonato" does not exist` | Banco não criado | Repetir o passo 3 |
| `relation "clubes" does not exist` | Tabelas não criadas ou `DB_NAME` errado | Repetir o passo 6 e conferir `export DB_NAME=campeonato` |
| `Connection refused` | PostgreSQL parado | `sudo systemctl start postgresql` |
| `SyntaxError` perto de `match` | Python anterior ao 3.10 | Instalar Python 3.10 ou superior |