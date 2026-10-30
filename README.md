# Gerenciador de Campeonato de Futebol

Aplicação de terminal desenvolvida em **Python** para cadastrar e gerenciar clubes, jogadores, partidas e gols em um banco de dados **PostgreSQL**.

- **Disciplina:** Banco de Dados – Semestre 2026/2
- **Professor:** Howard Roatti
- **Grupo:** Betânia, Eduardo, Gabriel, Vinícius e Vitor

## 1. Pré-requisitos

Instale os seguintes programas antes de executar o projeto:

| Programa | Para que serve | Verificação |
| --- | --- | --- |
| [Python](https://www.python.org/downloads/) **3.10+** | Executar o sistema e criar o ambiente virtual | `python --version` ou `python3 --version` |
| [Git](https://git-scm.com/downloads) | Clonar o repositório (opcional se baixar ZIP) | `git --version` |
| [PostgreSQL](https://www.postgresql.org/download/) | Servidor do banco de dados | `psql --version` (ver observação abaixo) |
| **psql** (cliente do PostgreSQL) | Executar os arquivos `.sql` | `psql --version` |

**Importante:** `psql` não é uma biblioteca Python e **não** é instalado por `pip` nem pelo `requirements.txt`. Ele vem com a instalação do PostgreSQL quando as ferramentas de linha de comando são selecionadas. O servidor PostgreSQL precisa estar instalado e em execução, localmente ou em outro ambiente acessível.

### Instalar PostgreSQL e psql no Windows

1. Acesse [postgresql.org/download/windows](https://www.postgresql.org/download/windows/) e siga o link para o instalador do PostgreSQL.
2. No instalador, selecione **PostgreSQL Server** e **Command Line Tools** (inclui `psql`). **pgAdmin** é opcional.
3. Defina e guarde a senha do usuário `postgres`; mantenha a porta padrão **5432**, se estiver livre.
4. Ao terminar, abra um novo PowerShell e execute `psql --version`.
5. Se o comando não for reconhecido, utilize o **SQL Shell (psql)** instalado junto ao PostgreSQL ou adicione a pasta `bin` do PostgreSQL ao `PATH` do Windows (por exemplo, `C:\Program Files\PostgreSQL\<versão>\bin`). Abra um novo terminal após alterar o `PATH`.

> O SQL Shell pode ser usado para comandos SQL interativos; para executar os comandos `psql -f ...` abaixo no diretório do projeto, é mais conveniente ter o `psql` disponível no PowerShell.

### Instalar PostgreSQL e psql no Ubuntu/Debian

```bash
sudo apt update
sudo apt install postgresql postgresql-client python3 python3-venv python3-pip git
sudo systemctl enable --now postgresql
psql --version
```

Em distribuições Linux diferentes, utilize o gerenciador de pacotes equivalente. No macOS, utilize a instalação do PostgreSQL disponibilizada em [postgresql.org/download/macosx](https://www.postgresql.org/download/macosx/).

**Alternativa — VM da disciplina:** caso esteja usando a VM original, que já possui PostgreSQL por Docker Compose, não instale outro servidor. Inicie o serviço existente:

```bash
cd ~/database_services
docker compose up -d
docker compose ps
```

Depois retorne ao diretório do projeto. Use o usuário, a senha, a porta e o banco configurados nessa VM. O cliente `psql` precisa estar disponível no terminal em que você executar os scripts (ou ser executado dentro do contêiner, conforme a configuração da VM).

## 2. Baixar o projeto e instalar bibliotecas Python

Clone o repositório (ou baixe e extraia o ZIP):

```bash
git clone https://github.com/bianchini021/projeto-banco-de-dados.git
cd projeto-banco-de-dados
```

Crie e ative um ambiente virtual **na raiz do projeto**.

**Windows (PowerShell):**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação, execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` no terminal atual e tente ativar novamente. Como alternativa, use diretamente `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, sem ativar o ambiente.

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### O que o `requirements.txt` instala?

O arquivo contém:

```text
psycopg[binary]>=3.2,<4
```

- **`psycopg` (versão 3):** biblioteca que conecta a aplicação Python ao PostgreSQL e executa comandos SQL.
- **`[binary]`:** instala o pacote binário compatível, simplificando a instalação do driver sem exigir compilação manual.
- **`>=3.2,<4`:** aceita versões da série 3 a partir de 3.2, sem atualizar para uma futura versão principal 4.

As demais importações do projeto fazem parte da biblioteca padrão do Python ou dos próprios arquivos de `src/`; não exigem instalação separada. Para verificar o driver:

```bash
python -m pip show psycopg
```

Sempre que abrir um novo terminal, ative novamente o `.venv` antes de executar o programa.

## 3. Configurar o acesso ao PostgreSQL

Por padrão, a aplicação conecta com os seguintes dados:

| Parâmetro | Valor padrão | Configuração opcional |
| --- | --- | --- |
| Servidor | `localhost` | `DB_HOST` |
| Porta | `5432` | `DB_PORT` |
| Banco | `postgres` | `DB_NAME` |
| Usuário e senha | Definidos pelo arquivo de credenciais ou pelo Psycopg | Veja as opções abaixo |

**O projeto utiliza o banco `postgres` por padrão**, já criado normalmente na instalação do PostgreSQL. Não é necessário criar um banco `campeonato`. Se quiser usar outro banco, crie-o primeiro e ajuste `DB_NAME` e `-d` no comando do `psql`.

### Opção A — arquivo de credenciais (mais simples)

Crie uma cópia de `src/utils/passphrase/authentication.postgres.example` com o nome `authentication.postgres` **na mesma pasta**.

**Windows (PowerShell):**

```powershell
Copy-Item src/utils/passphrase/authentication.postgres.example src/utils/passphrase/authentication.postgres
notepad src/utils/passphrase/authentication.postgres
```

**Linux/macOS:**

```bash
cp src/utils/passphrase/authentication.postgres.example src/utils/passphrase/authentication.postgres
chmod 600 src/utils/passphrase/authentication.postgres
nano src/utils/passphrase/authentication.postgres
```

Edite o arquivo para conter **uma única linha**, sem aspas:

```text
postgres,SUA_SENHA_DO_POSTGRESQL
```

Use a senha real definida durante a instalação ou disponibilizada pela disciplina. O arquivo é ignorado pelo Git; **não envie sua senha ao repositório**. Se o arquivo existir, ele tem prioridade sobre as variáveis `PGUSER` e `PGPASSWORD` na aplicação.

### Opção B — variáveis de ambiente (sem arquivo de credenciais)

Se o arquivo `authentication.postgres` não existir, o driver poderá usar `PGUSER` e `PGPASSWORD`.

**Windows (PowerShell):**

```powershell
$env:PGUSER = 'postgres'
$env:PGPASSWORD = Read-Host 'Senha do PostgreSQL'
```

**Linux/macOS:**

```bash
export PGUSER=postgres
read -r -s -p 'Senha do PostgreSQL: ' PGPASSWORD
printf '\n'
export PGPASSWORD
```

As variáveis acima valem para a sessão atual do terminal. Para servidores ou bancos diferentes, defina também `DB_HOST`, `DB_PORT` e `DB_NAME` no ambiente de execução da aplicação. A variável `DB_USER` **não** é utilizada.

## 4. Criar as tabelas com o psql

Certifique-se de que o serviço PostgreSQL está ativo. Na **raiz do projeto**, execute no terminal (PowerShell, Bash etc.):

```bash
psql -h localhost -p 5432 -U postgres -d postgres -W -v ON_ERROR_STOP=1 -f src/sql/schema.sql
```

Digite a senha do usuário `postgres` quando solicitado. Esse comando cria as tabelas `clubes`, `jogadores`, `partidas` e `gols`, caso ainda não existam.

**Atenção:** o `psql` não lê `authentication.postgres`, que é exclusivo da aplicação Python. Ele solicita sua própria autenticação; `-W` força a solicitação interativa da senha. Se o PostgreSQL estiver em outro servidor/porta/banco, ajuste `-h`, `-p` e `-d`.

**Opcional — inserir registros de demonstração:** execute apenas **uma vez** em um banco recém-preparado, porque os dados de exemplo têm valores e referências pré-definidos e não foram feitos para inserções repetidas:

```bash
psql -h localhost -p 5432 -U postgres -d postgres -W -v ON_ERROR_STOP=1 -f src/sql/dados_iniciais.sql
```

Para conferir as tabelas:

```bash
psql -h localhost -p 5432 -U postgres -d postgres -W -c '\dt'
```

## 5. Executar a aplicação

Com o PostgreSQL ativo, o esquema criado e o ambiente virtual preparado, execute **na raiz do projeto**:

```bash
python -m src.main
```

O programa abre menus para inserir, consultar, atualizar ou remover registros e gerar relatórios.

## Problemas comuns

| Problema | Como resolver |
| --- | --- |
| `psql` não é reconhecido | Instale as ferramentas de linha de comando do PostgreSQL e inclua a pasta `bin` no `PATH` (Windows), ou instale `postgresql-client` (Ubuntu/Debian). |
| `No module named 'psycopg'` | Ative o ambiente virtual e execute `python -m pip install -r requirements.txt`. |
| `No module named 'src'` | Entre na raiz do repositório e use `python -m src.main`, não `python src/main.py`. |
| `password authentication failed` / autenticação recusada | Confira a senha e o usuário no arquivo de credenciais ou nas variáveis de ambiente. |
| `connection refused` / conexão recusada | Inicie o PostgreSQL e confira host, porta e serviço (ou `docker compose ps` na VM). |
| `relation "clubes" does not exist` | Execute o arquivo `src/sql/schema.sql` no mesmo banco usado pela aplicação. |
| `python` / `py` não é reconhecido | Instale Python 3.10+ e configure o PATH; no Linux use `python3` para criar o ambiente. |
| `database ... does not exist` | Verifique `DB_NAME` e o argumento `-d`; o padrão do projeto é `postgres`. |

## Estrutura do projeto

```text
projeto-banco-de-dados/
├── Regras de Negócio e Modelagem/  # diagrama e regras de negócio
├── README.md                       # instruções de instalação e uso
├── PROMPTS.md                      # prompts utilizados durante o projeto
├── requirements.txt                # dependências Python
└── src/
    ├── main.py                     # ponto de entrada
    ├── controller/                  # operações CRUD
    ├── model/                       # entidades
    ├── reports/                     # relatórios
    ├── sql/                         # esquema, dados iniciais e consultas
    └── utils/                       # conexão, menus e tela inicial
```
