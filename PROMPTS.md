## Betânia – Clubes

**Fonte:** Claude  – claude.ai

**Prompts utilizados:**
1. Colei o `clube_controller.py` e o `_base.py` pedi para a IA me ensinar, com exercícios, como funcionam as consultas com
   `COUNT`, os parâmetros `%s` e a lógica do `if` usados na verificação. Depois, e pedi uma revisão comparando com as exigências do edital.
2. Colei o `schema.sql` para  verificar se usava os nomes exatos das colunas.
3. Perguntas sobre como usar o GitHub Desktop (fetch, pull, commit e push).
3. Colei o `main.py` e o `database.py` e pedi pra me ir explicando como executar
o projeto no Linux para criar o README.

**O que fiz com a resposta:**
- A revisão apontou que o `excluir_clube` não verificava se o clube tinha
  jogadores ou partidas antes de excluir 
- Com ajuda do Claude, criei o método `contar_dependentes`, que conta os jogadores (`id_clube`) e as
  partidas (`id_mandante` / `id_visitante`) ligados ao clube. O `excluir_clube` que agora mostra uma mensagem e não exclui quando existe algum vínculo.
- A IA também sugeriu uma classe `Clube`, mas ela já tinha sido criada pelo Eduardo, então não usei.

## Eduardo – Autenticação PostgreSQL

**Ferramentas utilizadas:** ChatGPT.

**Objetivo:** Adaptar a autenticação do PostgreSQL para funcionar na VM da disciplina, utilizando uma abordagem semelhante à do projeto de exemplo do professor.

**Uso da IA:** Solicitei auxílio para implementar a leitura das credenciais por meio do arquivo `authentication.postgres`, criar um arquivo de exemplo, configurar o `.gitignore` para proteger a senha real e atualizar as instruções de configuração no `README.md`.

**Validação:** Testei a implementação na VM disponibilizada pelo professor. A conexão com o PostgreSQL funcionou corretamente, e a consulta `SELECT 1` retornou `(1,)`.

## Gabriel – Dados de Teste

**Ferramentas utilizadas:** IA (Gemini).

**Objetivo:** Gerar a massa de dados inicial.

**Uso da IA:** Solicitei a criação de um script SQL (`dados_iniciais.sql`) contendo inserts de clubes, jogadores, partidas e gols para viabilizar os testes dos relatórios feitos pela equipe.

## Vitor – Arquivo Principal e Diagrama Relacional

**Ferramenta utilizada:** ChatGPT (OpenAI).

**Objetivo:** Auxiliar na elaboração da estrutura inicial do arquivo `main.py` e na representação visual do banco de dados por meio de um diagrama entidade-relacionamento em Mermaid.

**Prompts utilizados:**

1. Solicitei à IA um esboço para o arquivo `main.py`, considerando um sistema de gerenciamento de campeonato de futebol desenvolvido em Python, com um menu principal para acessar relatórios e operações de inserção, atualização, remoção e consulta de registros.
2. Pedi auxílio para estruturar o código Mermaid de um diagrama entidade-relacionamento, representando as tabelas `clubes`, `jogadores`, `partidas` e `gols`, com seus respectivos atributos, chaves primárias, chaves estrangeiras e relacionamentos.

**O que fiz com as respostas:**

- Utilizei o esboço gerado pela IA como referência para a estruturação do `main.py`, organizando o fluxo de execução do programa e o acesso às funcionalidades pelos menus.
- Utilizei o código Mermaid como base para a representação visual das tabelas e de seus relacionamentos.
- Comparei o diagrama com a estrutura definida no `schema.sql` e solicitei ajustes para representar corretamente os campos, as chaves e as restrições do banco.
- Mantive o diagrama alinhado à implementação existente, sem adicionar entidades ou atributos que não fazem parte do projeto.

**Participação:** A IA foi utilizada como ferramenta de apoio para produzir esboços e revisar a representação do banco de dados. Minha participação envolveu definir o que deveria ser representado, orientar os ajustes e conferir a correspondência entre o diagrama e a estrutura SQL do projeto.