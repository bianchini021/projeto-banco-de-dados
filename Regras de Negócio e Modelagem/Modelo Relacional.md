# Modelo Relacional - Gerenciador de Campeonato de Futebol

## 1. Informações do projeto

**Projeto:** Gerenciador de Campeonato de Futebol

**Banco de dados:** PostgreSQL

**Linguagem:** Python

**Objetivo:** Desenvolver um sistema para gerenciar clubes, jogadores, partidas e gols de um campeonato de futebol.

O sistema terá operações de cadastro, consulta, atualização e exclusão (CRUD), além de relatórios utilizando SQL.

Nesta primeira versão, o sistema trabalhará com apenas um campeonato, sem transferências de jogadores ou cadastro de temporadas.

O script responsável pela criação das tabelas está em src/sql/schema.sql.

## 2. Tabelas do banco de dados

O banco de dados possui quatro tabelas: CLUBES, JOGADORES, PARTIDAS e GOLS.

### 2.1. CLUBES

Armazena as informações dos clubes participantes do campeonato.

**Atributos:**

- `id_clube`: BIGINT, chave primária (PK), gerada automaticamente.
- `nome`: VARCHAR(100), obrigatório e único.
- `cidade`: VARCHAR(80), opcional.

**Restrições:**

- Cada clube possui um identificador único.
- Não é permitido cadastrar dois clubes com o mesmo nome.
- O nome do clube não pode ser nulo.
- A aplicação deverá impedir nomes vazios ou compostos apenas por espaços.

### 2.2. JOGADORES

Armazena os jogadores cadastrados e seus respectivos clubes.

**Atributos:**

- `id_jogador`: BIGINT, chave primária (PK), gerada automaticamente.
- `nome`: VARCHAR(100), obrigatório.
- `posicao`: VARCHAR(20), obrigatório.
- `id_clube`: BIGINT, chave estrangeira (FK), obrigatória.

**Restrições:**

- Cada jogador pertence a um clube existente.
- O nome e a posição são obrigatórios.
- O clube deve existir antes do cadastro do jogador.
- Não é permitido excluir um clube que possua jogadores cadastrados.

**Posições permitidas:**

- Goleiro
- Zagueiro
- Lateral
- Volante
- Meio-Campo
- Atacante

Essas posições já são validadas no banco por uma restrição `CHECK`.

### 2.3. PARTIDAS

Armazena os confrontos realizados ou programados entre os clubes.

**Atributos:**

- `id_partida`: BIGINT, chave primária (PK), gerada automaticamente.
- `id_mandante`: BIGINT, chave estrangeira (FK), obrigatória.
- `id_visitante`: BIGINT, chave estrangeira (FK), obrigatória.
- `rodada`: INTEGER, obrigatório.
- `data_partida`: DATE, obrigatório.
- `status`: VARCHAR(10), obrigatório, com valor padrão ABERTA.
- `gols_mandante`: INTEGER, preenchido quando a partida é finalizada.
- `gols_visitante`: INTEGER, preenchido quando a partida é finalizada.

**Restrições:**

- Um clube não pode enfrentar a si mesmo.
- Os clubes mandante e visitante devem estar cadastrados.
- A rodada deve ser maior que zero.
- O status pode ser apenas ABERTA ou FINALIZADA.
- Uma partida ABERTA não possui placar registrado.
- Uma partida FINALIZADA deve possuir placar.
- Os valores do placar não podem ser negativos.

Essas restrições já estão definidas no `schema.sql`.

### 2.4. GOLS

Armazena os gols marcados pelos jogadores durante as partidas.

**Atributos:**

- `id_gol`: BIGINT, chave primária (PK), gerada automaticamente.
- `id_partida`: BIGINT, chave estrangeira (FK), obrigatória.
- `id_jogador`: BIGINT, chave estrangeira (FK), obrigatória.
- `minuto`: SMALLINT, obrigatório.

**Restrições:**

- Cada gol pertence a uma partida existente.
- Cada gol está associado a um jogador existente.
- O minuto do gol deve estar entre 1 e 130.
- Um jogador pode marcar vários gols na mesma partida.
- A aplicação deverá verificar se o jogador pertence a um dos clubes participantes.

Para simplificar, os acréscimos serão armazenados como minutos absolutos. Por exemplo, um gol aos 45+2 será registrado como minuto 47.

## 3. Relacionamentos entre as tabelas

O banco possui cinco relacionamentos do tipo 1:N (um para muitos).

**CLUBES e JOGADORES**

- Um clube pode possuir vários jogadores.
- Cada jogador pertence a um único clube.

**CLUBES e PARTIDAS (mandante)**

- Um clube pode participar como mandante em várias partidas.
- Cada partida possui apenas um mandante.

**CLUBES e PARTIDAS (visitante)**

- Um clube pode participar como visitante em várias partidas.
- Cada partida possui apenas um visitante.

**PARTIDAS e GOLS**

- Uma partida pode possuir vários gols ou nenhum.
- Cada gol pertence a uma única partida.

**JOGADORES e GOLS**

- Um jogador pode marcar vários gols ou nenhum.
- Cada gol está associado a um único jogador.

Todas as chaves estrangeiras são obrigatórias e utilizam `ON DELETE RESTRICT`.

Isso impede que registros sejam excluídos enquanto estiverem sendo utilizados por outras tabelas.

O diagrama está no arquivo `Regras de Negócio e Modelagem/diagrama_relacional.mmd`.

## 4. Regras de negócio

Além das restrições do banco, o sistema Python precisará implementar algumas regras.

### 4.1. Cadastro de clubes

- Não permitir nomes vazios.
- Não permitir nomes duplicados.
- Impedir a exclusão de clubes que tenham jogadores ou partidas associados.

### 4.2. Cadastro de jogadores

- Cada jogador deve estar associado a um clube.
- A posição deve estar entre as opções permitidas.
- Não permitir alterar o clube de um jogador que já possua gols registrados.

Essa última regra evita problemas no histórico dos gols, já que não haverá sistema de transferências nesta versão.

### 4.3. Registro de partidas

- Mandante e visitante devem ser clubes diferentes.
- Não permitir o mesmo confronto duas vezes na mesma rodada, mesmo com mandante e visitante invertidos.
- O sistema permitirá cadastrar partidas abertas.
- Uma partida só receberá placar quando for finalizada.

A verificação de confrontos repetidos será feita na aplicação Python, pois ainda não existe uma restrição específica no SQL para isso.

### 4.4. Registro de gols

- O jogador que marcou deve pertencer a um dos clubes participantes.
- Só será permitido cadastrar, atualizar ou excluir gols em partidas abertas.
- Uma partida poderá terminar sem gols, com placar de 0 a 0.

### 4.5. Finalização das partidas

Quando uma partida for finalizada, o sistema deverá:

1. Consultar os gols cadastrados naquela partida.
2. Identificar a qual clube pertence cada jogador que marcou.
3. Contar os gols do mandante e do visitante.
4. Atualizar o placar da partida.
5. Alterar o status para FINALIZADA.

Essas alterações deverão ocorrer dentro de uma transação no banco de dados.

Caso seja necessário corrigir algum gol depois da finalização, a partida deverá ser reaberta antes da alteração.

### 4.6. Exclusão de registros

O sistema deverá informar quando um registro não puder ser excluído devido a relacionamentos com outras tabelas.

Não haverá exclusão automática de registros relacionados.

## 5. Relatórios do sistema

O projeto deverá possuir pelo menos dois relatórios utilizando consultas SQL.

### 5.1. Relatório de artilharia

Mostrará a quantidade de gols marcados por cada jogador.

**Informações apresentadas:**

- Nome do jogador.
- Clube do jogador.
- Quantidade de gols marcados.

**SQL utilizado:**

- `SELECT`
- `COUNT`
- `GROUP BY`
- `JOIN`
- `ORDER BY`

Serão considerados apenas gols de partidas finalizadas.

### 5.2. Relatório de partidas

Mostrará as partidas cadastradas no campeonato.

**Informações apresentadas:**

- Rodada.
- Data da partida.
- Clube mandante.
- Clube visitante.
- Status da partida.
- Placar, quando disponível.

**SQL utilizado:**

- `SELECT`
- `JOIN`
- `ORDER BY`

Esse relatório utilizará a tabela PARTIDAS e duas junções com a tabela CLUBES, uma para o mandante e outra para o visitante.

## 6. Funcionalidades do sistema

O sistema será executado pelo terminal e deverá possuir um menu principal.

**Menu previsto:**

1. Gerenciar clubes.
2. Gerenciar jogadores.
3. Gerenciar partidas.
4. Gerenciar gols.
5. Consultar relatórios.
6. Sair.

Cada opção de gerenciamento deverá permitir:

- Cadastrar registros.
- Listar registros.
- Atualizar registros.
- Excluir registros.

Na inicialização, o programa deverá mostrar o nome do sistema, os nomes dos integrantes do grupo e a quantidade de registros presentes em cada tabela.

## 7. Limitações da primeira versão

Para manter o projeto dentro do prazo, algumas funcionalidades não serão desenvolvidas inicialmente:

- Transferências de jogadores.
- Cadastro de várias temporadas.
- Gols contra.
- Disputas de pênaltis.
- Assistências.
- Cartões amarelos e vermelhos.
- Classificação completa do campeonato.

A classificação poderá ser implementada futuramente utilizando os resultados das partidas, sem precisar criar uma tabela específica.

Também poderá ser adicionada uma regra para impedir que um clube dispute mais de uma partida na mesma rodada.

## 8. Situação atual do projeto

**Já desenvolvido:**

- Definição do tema.
- Modelagem das quatro tabelas.
- Definição dos atributos e relacionamentos.
- Diagrama relacional em Mermaid.
- Definição das regras de negócio.
- Script SQL de criação das tabelas (`schema.sql`).

**Ainda precisamos fazer ou validar:**

1. Executar e testar o `schema.sql` no PostgreSQL.
2. Verificar o funcionamento das chaves estrangeiras e restrições.
3. Exportar o diagrama relacional em PDF, PNG ou JPEG.
4. Criar a conexão entre Python e PostgreSQL.
5. Desenvolver as classes e controladores.
6. Implementar as operações CRUD.
7. Implementar os relatórios SQL.
8. Criar os menus e a tela inicial.
9. Testar o funcionamento no Linux.
10. Completar o README e o PROMPTS.md.
11. Gravar o vídeo demonstrativo.

## 9. Próxima etapa

A próxima etapa será testar o script SQL já existente no PostgreSQL.

Depois da validação do banco, começaremos o desenvolvimento da aplicação Python, seguindo a estrutura das quatro entidades.

Todas as consultas e alterações serão realizadas com SQL explícito, sem utilização de ORM, conforme as exigências do professor.