---
date: 2026-10-28T17:49:00Z
author: Mirror Builder (Driver) com Alisson (Navigator)
kind: milestone
related:
  - CV2
  - CV2.DS1
  - CV2.DS1.US1
verification:
  - docs/project/roadmap/cv2-minha-estante-do-meu-jeito/cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us1-create-once-draw-for-free/test-guide.md
---

# A primeira estante que pode ser minha

O Alisson validou a primeira fatia da CV2 numa cópia descartável de uma foto
nova da própria estante. `create` reconheceu 11 livros, criou o `shelf.yaml` e
custou US$ 0,03 (estimativa: US$ 0,09). `draw` e `open` funcionaram sem novo
custo.

Ele reescreveu a lente diretamente no arquivo, desenhou de novo e viu a frase
na página. Ao trocar `version: 1` por `version: one`, recebeu um erro claro na
linha 1 e a página anterior continuou abrindo. Restaurou o arquivo, desenhou
novamente e abriu a estante no computador e no celular.

Evidência para a continuação:

- um dos 11 livros foi identificado incorretamente: confirma a necessidade da
  DS2, de corrigir livros, autores e capas;
- o custo efetivo da criação com uma foto foi bem menor que a estimativa;
- o Navigator perguntou se o padrão deveria ser `my-bookshelf/` ou a pasta
  atual. A pergunta fica como decisão de UX de comandos, sem mudar o
  comportamento durante esta story.
