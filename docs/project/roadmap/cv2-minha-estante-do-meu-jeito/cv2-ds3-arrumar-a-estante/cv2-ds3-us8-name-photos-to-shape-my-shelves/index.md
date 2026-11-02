---
code: CV2.DS3.US8
level: User Story
status: Active
status_reason: o Navigator nomeou fotos de seções como entrada autoral para a primeira composição do shelf.yaml
updated: 2026-11-01
related:
  - ../index.md
  - ../../../../../product/principles.md
---

[< CV2.DS3](../index.md)

# CV2.DS3.US8: Name photos to shape my shelves

**Status:** Active

## Story Statement

Como leitora ou leitor que fotografou separadamente cada parte organizada da
estante,
quero nomear as fotos com a ordem e o título das prateleiras,
para que a primeira versão do `shelf.yaml` preserve a lógica que já dei aos
livros antes de pedir uma leitura da IA.

## Outcome

Fotos com nomes no formato `NN_Título.ext` definem prateleiras autorais. O
prefixo numérico define a ordem, o restante define literalmente o título, a
foto fica associada à prateleira e os livros reconhecidos nela começam ali. A
IA pode escrever a abertura e os textos, mas não renomeia nem reorganiza essas
escolhas. Fotos sem a convenção continuam disponíveis e seus livros chegam à
prateleira de fechamento.

## Acceptance Behavior

```text
Given photos named 01_Tecnologia.jpg and 02_Literatura.jpg
And books recognized from each photo
When create writes the first shelf.yaml
Then version 2 contains Tecnologia and Literatura in that order
And each section keeps its photo and the books recognized from it
And the generated page shows the associated photo in its section
And the portrait may write lens and section text but cannot rename or move the named shelves
```

## Out Of Scope

- Mais de uma foto por prateleira.
- Pastas aninhadas ou um arquivo separado de configuração.
- Inferir intenção de nomes automáticos de câmera, WhatsApp ou celular.
- Renomear fotos depois que `shelf.yaml` já existe e sincronizar a fonte.
- Legenda, recorte ou posição focal da foto.
- Puxar `CV2.DS3.US5`.

## Artifacts

- [Plan](plan.md)
- [Test Guide](test-guide.md)
