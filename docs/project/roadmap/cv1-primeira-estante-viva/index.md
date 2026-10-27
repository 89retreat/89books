---
code: CV1
level: Value
status: Active
status_reason: DS1, DS2 e DS3 concluídas; falta cada fundador sair de um clone limpo com a própria estante
updated: 2026-10-27
related:
  - ../../exploration/es-001-a-estante-como-retrato/index.md
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

[< Roadmap](../index.md)

# CV1 — A Primeira Estante Viva

**Status:** Active

---

## Intent

**Capacidade:** uma pessoa do grupo, sozinha, sai de um clone do repositório
com a própria estante pronta para compartilhar.

O caminho, sem fricção, pelo terminal:

1. clona o repositório e lê o guia de primeiros passos;
2. põe as fotos da estante na pasta `my-bookshelf/`;
3. roda um comando. Se o ambiente não estiver configurado, o comando explica
   como obter as chaves, pede as chaves e o nome da estante, testa e grava a
   configuração;
4. recebe a estante num arquivo HTML: fotos, livros com autores e um
   **retrato de si**, pronta para mandar a quem quiser.

Toda a superfície do terminal (comandos, perguntas, mensagens, guia) é em
inglês. A estante gerada é em português do Brasil.

Origem: [ES-001](../../exploration/es-001-a-estante-como-retrato/index.md),
reorganizada pela
[ES-002](../../exploration/es-002-a-estante-num-arquivo/index.md) em
2026-10-26 e pelo Navigator em 2026-10-27, que reescreveu a CV1 como uma
capacidade verificável: o que não serve a ela foi para outras CVs.

## Delivery Arc

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV1.DS1](cv1-ds1-fundacao/index.md) | Fundação: reconhecimento de livros e decisões técnicas | Sabemos que foto e print viram lista de livros; decisões técnicas do MVP local registradas |
| [CV1.DS2](cv1-ds2-a-estante-num-arquivo/index.md) | A estante num arquivo | O comando transforma uma pasta de fotos numa estante bonita, com o retrato de si, títulos e autores conferidos |
| [CV1.DS3](cv1-ds3-minha-estante-pronta-para-compartilhar/index.md) | Minha estante pronta para compartilhar | Uma pessoa sai de um clone limpo com a própria estante, guiada pelo guia e pelo terminal, sem pedir ajuda |

## Scope

Fora desta CV:

- corrigir a estante, pedir outro retrato e medir a leitura em faixas:
  [CV2.DS1](../cv2-a-estante-visitavel/cv2-ds1-corrigir-a-estante/index.md);
- publicar no GitHub Pages e reunir as estantes do grupo:
  [CV2.DS2](../cv2-a-estante-visitavel/cv2-ds2-estante-visitavel/index.md);
- bot do Telegram, grupo dedicado e movimentos:
  [CV3](../cv3-a-estante-no-telegram/index.md);
- print do Kindle, servidor, contas, login, feed, várias estantes por pessoa,
  afinidade entre leitores, importações.

A primeira estante pode sair com alguns erros de leitura: "pronta para
compartilhar" quer dizer gerada e bonita, não perfeita.

## Acceptance / Done Condition

O Navigator, e depois cada fundador, parte de um clone limpo numa máquina sem
a configuração do projeto, segue só o guia e gera a própria estante sem pedir
ajuda.

Sinais a observar na retrospectiva, registrada no worklog:

- Onde a pessoa hesitou ou travou?
- Quanto tempo do clone à estante? Quanto custou?
- A pessoa mostrou a estante a alguém?

## Validation Route

O Navigator, num clone limpo, primeiro; depois os outros fundadores.
