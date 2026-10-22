# Etapa 1: Modelagem Relacional

#### Projeto: Gerenciador de Campeonato de Futebol
#### Tecnologias: PostgreSQL (SGBD) e Python (Aplicação)
#### Escopo da primeira entrega: CRUD de CLUBES, JOGADORES, PARTIDAS e GOLS. Dois relatórios de SQL obrigatórios.
#### Modelo: um campeonato, sem cadastro de temporadas ou transferência de atletas

## 1. Dicionário de Dados

### CLUBES:

| Coluna | Tipo PostgreSQL | Obrigatório? | Restrições |
|---|---|---|---|
| id_clube | BIGINT | Sim | PK, GENERATED ALWAYS AS IDENTITY |
| nome | VARCHAR(100) | Sim | UNIQUE, não vazio após trim (validação na aplicação) |
| cidade | VARCHAR(80) | Não | Opcional |

### PARTIDAS: 

| Coluna | Tipo PostgreSQL | Obrigatório? | Restrições |
|---|---|---|---|
| id_partida | BIGINT | Sim | PK, GENERATED ALWAYS AS IDENTITY |
| id_mandante | BIGINT | Sim | FK -> CLUBES(id_clube); ON DELETE RESTRICT |
| id_visitante | BIGINT | Sim | FK -> CLUBES(id_clube); ON DELETE RESTRICT |
| rodada | INTEGER | Sim | CHECK (rodada > 0) |
| data_partida | DATE | Sim | Data da partida |
| status | VARCHAR(10) | Sim | DEFAULT 'ABERTA'; CHECK IN ('ABERTA','FINALIZADA') |
| gols_mandante | INTEGER | Condicional | NULL quando ABERTA; >=0 quando FINALIZADA |
| gols_visitante | INTEGER | Condicional | NULL quando ABERTA; >=0 quando FINALIZADA |

#### CHECK adicional: id_mandante <> id_visitante
#### CHECK de estado: quando status = 'ABERTA', ambos os campos de placar são NULL. Quando status = 'FINALIZADA' ambos são NOT NULL e >= 0.

### GOLS:

| Coluna | Tipo PostgreSQL | Obrigatório? | Restrições |
|---|---|---|---|
| id_gol | BIGINT | Sim | PK, GENERATED ALWAYS AS IDENTITY |
| id_partida | BIGINT | Sim | FK -> PARTIDAS(id_partida); ON DELETE RESTRICT |
| id_jogador | BIGINT | Sim | FK -> JOGADORES(id_jogador); ON DELETE RESTRICT |
| minuto | SMALLINT | Sim | CHECK (minuto BETWEEN 1 AND 130); minuto decorrido absoluto |

#### Nota: o minuto de acréscimo pode ser representado pelo minuto decorrido absoluto (por exemplo, 47), sem formato '45+2'

## 2. Cardinalidades e integridade referencial

| Relação | Cardinalidade | Significado |
|---|---|---|
| CLUBES -> JOGADORES | 1:N | Cada jogador deve pertencer a exatamente um clube; um clube pode ter zero ou muitos jogadores. |
| CLUBES -> PARTIDAS (mandante) | 1:N | Cada partida tem exatamente um mandante; um clube pode ser mandante em muitas partidas. |
| CLUBES -> PARTIDAS (visitante) | 1:N | Cada partida tem exatamente um visitante; um clube pode ser visitante em muitas partidas. |
| PARTIDAS -> GOLS | 1:N | Cada gol pertence a exatamente uma partida; uma partida pode ter nenhum ou muitos gols. |
| JOGADORES -> GOLS | 1:N | Cada gol tem exatamente um autor; um jogador pode ter nenhum ou muitos gols. |

#### Todas as chaves estrangeiras são obrigatórias (NOT NULL). As referências são protegidas sem exclusão em cascata (RESTRICT ou NO ACTION), com mensagens amigáveis na aplicação

## 3. Regras de negócio

#### 1. Campeonato único: as quatro tabelas representam um campeonato em andamento; não há CAMPEONATOS ou TEMPORADAS nesta versão

#### 2. Clube único: nomes de clubes devem ser únicos. Um clube não pode jogar contra si mesmo

#### 3. Partidas: rodada > 0. A aplicação deve impedir a duplicação da mesma partida na mesma rodada, inclusive invertendo mandante e visitante. Uma regra adicional de cada clube jogar no máximo uma vez por rodada pode ser adotada no CRUD

#### 4. Elenco: cada jogador possui um id_clube; não há transferência nesta versão. Se existir gol associado, o clube do jogador não pode ser alterado (para preservar o histórico)

#### 5. Autor de gol: o jogador deve pertencer ao clube mandante ou visitante da partida. Esse teste envolve múltiplas tabelas e será executado pela aplicação Python

#### 6. luxo da partida: criar partida com status = 'ABERTA' e placar NULL. Com a partida aberta, cadastrar ou alterar os gols. Ao finalizar, contar os gols por clube, gravar o placar resultante e definir status = 'FINALIZADA' na mesma transação

#### 7. Empate sem gols: uma partida sem gols pode ser finalizada com placar 0 x 0

#### 8. Edição após finalizar: para alterar ou excluir gols de uma partida finalizada, primeiro reabrir a partida (status ABERTA e placar NULL); após os ajustes, finalizar novamente. A aplicação deve tratar essas mudanças em transação

#### 9. Exclusão: não excluir clubes que tenham jogadores ou partidas, jogadores com gols, nem partidas com gols. Exibir mensagem informando as dependências

#### 10. Relatórios: considerar somente partidas FINALIZADAS para resultados e estatísticas de gols. A pontuação/classificação poderá ser implementada numa etapa posterior, sem alteração das quatro entidades.

#### 11. Limites da versão inicial: não há gols contra, disputas de pênaltis, transferências, várias temporadas, assistências ou cartões. Caso essas funções sejam necessárias, a modelagem deverá ser ampliada.

## 4. Relatórios obrigatórios previstos

#### Relatório 1 - Artilharia (GROUP BY): quantificar gols por jogador (COUNT(id_gol)), agrupados por jogador, usando GOLS, JOGADORES e PARTIDAS e filtrando partidas finalizadas. Serve como relatório agregado do edital

#### Relatório 2 - Partidas com clubes (JOIN): listar rodada, data, clube mandante, clube visitante, status e placar a partir de PARTIDAS com duas junções à tabela CLUBES (uma por papel). Serve como relatório de junção do edital

## 5. Requisitos gerais do edital associados

#### - Gerar diagrama relacional com atributos, tipos, chaves primárias/estrangeiras, obrigatoriedades e cardinalidades
#### - Criar o script SQL no PostgreSQL na próxima etapa
#### - Implementar CRUD com submenus para cada uma das quatro entidades
#### - Exibir o nome do sistema, integrantes e contagem de registros em cada tabela na tela inicial
#### - Criar os dois relatórios SQL, mantendo consultas SQL explícitas e sem ORM
#### - Executar em Linux, documentar no README.md, gravar vídeo e incluir PROMPTS.md para registrar o uso de IA (caso tenha)

## 6. Próxima etapa

#### Etapa 2 do projeto: criar schema.sql com as quatro tabelas: PK, FK, CHECK, UNIQUE e integridade referencial: executar no PostgreSQL e testar com registros de exemplo
