# Gerenciador de Campeonato de Futebol

Aplicação de linha de comando em Python para gerenciar clubes, jogadores,
partidas e gols em PostgreSQL.

- **Disciplina:** Banco de Dados – Semestre 2026/2
- **Professor:** Howard Roatti
- **Grupo:** Betânia, Eduardo, Gabriel, Vinícius e Vitor

Este guia utiliza a VM original da disciplina, cujo PostgreSQL já está
configurado em Docker Compose. Não é necessário instalar outro PostgreSQL
nem alterar a senha do serviço.

## 1. Iniciar os serviços da VM

```bash
cd ~/database_services
docker compose up -d
docker compose ps
```

Confira se o serviço PostgreSQL está em execução e com a porta 5432 publicada.
Os padrões são host `localhost`, porta `5432` e banco `postgres`. O usuário da
VM é `postgres` e deve ser informado por uma das opções abaixo.
Utilize a senha já configurada no ambiente da disciplina; consulte
a configuração local do serviço ou o professor para obtê-la.

## 2. Clonar e preparar o projeto

São necessários Python 3.10 ou superior, suporte a `venv`, Git e o cliente
`psql` para executar o script SQL. Confira as ferramentas disponíveis na VM:

```bash
python3 --version
git --version
psql --version
```

```bash
git clone https://github.com/bianchini021/projeto-banco-de-dados.git
cd projeto-banco-de-dados
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Execute os próximos comandos na raiz do projeto. Ao abrir outro terminal,
volte à pasta e ative o ambiente com `source .venv/bin/activate`.

## 3. Configurar a autenticação

Há duas opções. Se o arquivo local existir, suas credenciais têm prioridade.
Se estiver ausente, o Psycopg resolve as credenciais pelo ambiente.

### Opção A: arquivo local

Copie o modelo versionado e restrinja o acesso ao arquivo local:

```bash
cp src/utils/passphrase/authentication.postgres.example src/utils/passphrase/authentication.postgres
chmod 600 src/utils/passphrase/authentication.postgres
nano src/utils/passphrase/authentication.postgres
```

Substitua o marcador pela senha já configurada na VM, mantendo uma única linha
no formato `usuario,senha`:

```text
postgres,SUBSTITUA_PELA_SENHA_DA_VM
```

Não coloque aspas em torno dos valores. A primeira vírgula separa o usuário da
senha; vírgulas adicionais fazem parte da senha. O arquivo armazena somente
usuário e senha e é ignorado pelo Git. Nunca versione credenciais reais.

A aplicação encontra esse arquivo a partir da localização de `database.py` e
fornece as credenciais diretamente ao driver. Um arquivo inválido deve ser
corrigido: não há tentativa automática com outras credenciais nesse caso.

### Opção B: variáveis de ambiente

Sem `src/utils/passphrase/authentication.postgres`, a aplicação não passa
`user` nem `password` ao Psycopg. O driver utiliza sua resolução padrão de
credenciais, incluindo `PGUSER` e `PGPASSWORD`. Para configurar no terminal
da VM sem digitar a senha diretamente no histórico de comandos do Bash:

```bash
export PGUSER=postgres
read -r -s -p 'Senha do PostgreSQL da VM: ' PGPASSWORD
printf '\n'
export PGPASSWORD
```

Inicie o programa nesse mesmo terminal. Ao fechar o terminal, configure as
variáveis novamente. Não é necessário criar um `.pgpass`; outras fontes
padrão do driver continuam disponíveis. `DB_USER` não é utilizado.
Para deixar de fornecer a senha nesse terminal, execute `unset PGPASSWORD`.

O atributo `PostgresQueries.user` reflete `PGUSER` antes da conexão, ou o usuário
do arquivo quando ele é lido. Após conectar, reflete o usuário efetivo informado
pelo Psycopg, inclusive quando resolvido por outras fontes padrão do driver.

Falhas de conexão exibem uma orientação e, quando reconhecido, o motivo:
autenticação, serviço recusando conexão, tempo limite, endereço não resolvido,
banco inexistente ou SSL. O texto original do erro não é exibido, evitando
expor senhas; o tipo da exceção e seu SQLSTATE são preservados para diagnóstico.

### Host, porta e banco

Os demais parâmetros continuam aceitando variáveis de ambiente opcionais:

| Variável | Padrão | Função |
|---|---|---|
| `DB_HOST` | `localhost` | Endereço do servidor |
| `DB_PORT` | `5432` | Porta do PostgreSQL |
| `DB_NAME` | `postgres` | Nome do banco |

Na VM original, não é necessário definir essas variáveis. Caso estejam
configuradas para outro ambiente, remova-as do terminal com:

```bash
unset DB_HOST DB_PORT DB_NAME
```

## 4. Criar as tabelas

Com o serviço ativo, execute o esquema no banco `postgres` existente:

```bash
psql -h localhost -p 5432 -U postgres -d postgres -W -v ON_ERROR_STOP=1 -f src/sql/schema.sql
```

Digite a senha da VM quando solicitada. Esse comando usa o cliente `psql`,
que não lê o arquivo de autenticação da aplicação. A opção `-W` solicita a
senha interativamente mesmo com `PGPASSWORD` definido. Não é necessário criar
um banco chamado `campeonato`. Se usar outros parâmetros de conexão, ajuste
também os argumentos do comando `psql`.

## 5. Executar

Na raiz do projeto, com o ambiente virtual ativo:

```bash
python -m src.main
```

Use os menus para consultar e cadastrar registros e acessar os relatórios.
Se a conexão falhar, confira o estado do serviço com `docker compose ps` em
`~/database_services`, as credenciais do arquivo local ou `PGUSER`/`PGPASSWORD`
(quando o arquivo estiver ausente) e as variáveis `DB_*`.

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| "Conexão recusada" | Os serviços da VM não foram iniciados | Rodar `docker compose up -d` na pasta `~/database_services` |
| "Autenticação recusada" | Senha errada no arquivo de credenciais | Corrija a senha em `src/utils/passphrase/authentication.postgres` e execute o programa de novo |
| `relation "clubes" does not exist` | As tabelas não foram criadas | Execute o passo 4 (Criar as tabelas) |
| `No module named 'psycopg'` | O ambiente virtual não foi ativado | Rodar `source .venv/bin/activate` na pasta do projeto |
| `No module named 'src'` | O programa foi iniciado com `python src/main.py` | Usar `python -m src.main` na pasta do projeto |

## Estrutura do projeto

```
projeto-banco-de-dados/
├── Regras de Negócio e Modelagem/   # diagrama e regras de negócio
├── README.md                        # explica como rodar o projeto
├── PROMPTS.md                       # prompts utilizados durante o projeto
├── requirements.txt                 # bibliotecas Python que o projeto usa
└── src/
    ├── main.py                      # programa principal
    ├── controller/                  # CRUD de cada tabela
    ├── model/                       # classes das entidades
    ├── reports/                     # relatórios
    ├── sql/                         # criação das tabelas e consultas dos relatórios
    └── utils/                       # conexão com o banco, menus e tela de abertura
```

## 🎥 Apresentação do Projeto

Confira no vídeo abaixo a demonstração completa do sistema em funcionamento, incluindo a execução das operações de CRUD integradas ao PostgreSQL e a geração de relatórios dinâmicos:

[![Apresentação do Projeto - Banco de Dados FAESA](https://img.youtube.com/vi/oRQJuGfXQvQ/0.jpg)](https://youtu.be/oRQJuGfXQvQ)