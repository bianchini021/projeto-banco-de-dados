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