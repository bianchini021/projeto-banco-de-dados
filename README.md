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