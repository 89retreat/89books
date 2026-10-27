---
code: CV1.DS2.US3
level: User Story
status: Done
status_reason: validada pelo Navigator em 2026-10-27; débitos adiados para a US4, a TS1 e a página por URL
updated: 2026-10-27
related:
  - ../cv1-ds2-us2-uma-estante-bonita/index.md
  - ../../../../decisions/records/2026-10-24T2013Z-reconhecimento-de-livros.md
---

[< Parent](../index.md)

# CV1.DS2.US3 — Os livros certos, com quem os escreveu

**Status:** Done
**Type:** User Story

---

## User Story

As uma pessoa do grupo que abriu a própria estante,
I want que cada livro apareça com o título exato e com quem o escreveu,
So that eu me reconheça nos meus livros, sem ter de corrigir à mão o que o
sistema poderia conferir sozinho.

## Origem

Feedback do Lula sobre a estante dele (2026-10-26):

> Gostei muito! Só não gostei do último: VII Quando não procuro nada em
> particular - Os outros 16 livros que moram comigo, esperando a sua vez.
>
> Uma coisa boba que me incomodou foi o título de alguns livros não estar
> muito exato, e não ter a autoria nas lombadas ilustradas. Acho que daria
> pra conferir qual o livro mesmo e quem escreveu... Exemplo: Continuo Preta,
> de Sueli Carneiro, está como Continuo Preto, no masculino.

Na estante dele, "Continuo Preto" chegou sem autor e a Open Library não o
encontrou, então o erro de leitura foi direto para a página. Há casos do
mesmo tipo: "Carla Akotirene", nome de autora lido como título, e "O Pai
Prezado" ao lado de "Ó pa í, Prezada!", provavelmente o mesmo livro.

## Outcome

Depois de reconhecer as fotos, a estante passa por uma conferência
automática: o modelo revisa a lista inteira, com o contexto de toda a
estante, e o Google Books confirma título e autoria onde a Open Library não
achou. Cada lombada mostra o autor. A prateleira das sobras deixa de dizer
"sobra" e passa a dizer que são mais livros que já me acompanharam.

## Acceptance Behavior

```text
Given uma estante em que o modelo leu "Continuo Preto", sem autor
When gero a estante
Then o livro aparece como "Continuo Preta", de Sueli Carneiro
And um nome de autor lido como título é corrigido ou vira autoria de um livro
And o mesmo livro lido duas vezes aparece uma vez só
```

```text
Given um livro com autor conhecido
When ele aparece como lombada
Then a lombada mostra o sobrenome do autor, menor, embaixo do título
```

```text
Given livros que não entraram em nenhum tema
When abro a estante
Then eles aparecem no fim, numa prateleira sem numeral e mais leve,
     com o título "E mais livros que já me acompanharam"
```

## Scope

- Conferência pelo modelo, só texto, depois da Open Library.
- Google Books como segunda fonte, com chave gratuita.
- Autor em primeiro plano nas lombadas (decisão do Navigator em 2026-10-27:
  "é mais importante eu ver que você leu Kant ou Platão do que qual o livro
  específico deles"): o autor no topo, grande; o título embaixo, menor.
- Livros do mesmo autor juntos e da mesma cor dentro de cada prateleira.
- Uma linha "Quem mais mora aqui" abaixo da lente, com os autores de dois ou
  mais livros.
- Prateleira das sobras sem numeral, mais leve, com título fixo.

## Out Of Scope

- Ler as fotos em faixas para melhorar o reconhecimento na origem (fica como
  próximo passo se a conferência não bastar).
- Corrigir à mão pelo `books.yaml`, cache do reconhecimento e retrato novo
  (CV1.DS2.US4).

## Validation

Navigator, com o Lula: gerar de novo a estante dele e conferir "Continuo
Preta", os autores nas lombadas e a última prateleira.
