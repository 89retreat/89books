---
status: Decided
raised: 2026-10-24
decided: 2026-10-26
deciders:
  - Navigator (Alisson), por delegação ao Driver em cadência accelerated; aceite na validação da CV1.DS1.TS2
supersedes:
related:
  - CV2.DS2
  - CV3.DS1
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

# Como o grupo acessa o produto

## Question

O acesso fechado do grupo usa links mágicos por e-mail, identidade do Telegram
ou outro mecanismo?

## Decision

**Na CV1 não há acesso a controlar.** A estante é um arquivo HTML na máquina
da pessoa. Ela decide se manda o arquivo a alguém, se publica um link no
GitHub Pages, as duas coisas ou nenhuma. O link usa um endereço difícil de
adivinhar; quem o tiver vê a estante.

**Na CV3**, a identidade vem do Telegram: quem conversa com o bot é
identificado pelo ID do Telegram, e o acesso pode se apoiar numa lista de
membros ou no grupo dedicado. Decidir ao planejar a CV3.

## Rationale

- Sem servidor, não há login a construir; compartilhar vira um gesto
  explícito da pessoa, o que respeita o caráter pessoal das fotos.
- Arquivo e link servem a situações diferentes: o arquivo não sai do controle
  de quem manda; o link abre melhor no celular e facilita a visita.
- Endereço difícil de adivinhar não é segredo forte. É aceitável para estantes
  que a pessoa escolheu mostrar, e a escolha é dela.

## Options Considered

- **Arquivo ou link, à escolha da pessoa, sem login** (escolhida para a CV1).
- **Link de uso único enviado pelo bot, com lista de membros**: proposta
  inicial da TS2; volta a fazer sentido na CV3.
- **Link mágico por e-mail** e **widget de login do Telegram**: descartados.
- **Página protegida por senha**: dá falsa segurança num HTML estático.

## Consequences

- A CV2.DS2.US1 publica no GitHub Pages só sob comando explícito.
- Onde publicar (repositório da org 89retreat ou repositório pessoal) está em
  [publicação no GitHub Pages](2026-10-26T1830Z-publicacao-no-github-pages.md).
- O HTML não deve incluir nada além do que a pessoa vê: sem a chave, sem
  caminhos locais, sem metadados das fotos (EXIF).

## Revisão de 2026-10-26

O Navigator definiu que o arquivo HTML é um artefato temporário, para a
validação entre os fundadores. Quando o produto sair do grupo de fundadores,
a estante será compartilhada sempre por URL. Consequências:

- O GitHub Pages da CV2.DS2 é o primeiro passo rumo ao compartilhamento por
  URL, não uma alternativa equivalente ao arquivo.
- A página pode depender de JavaScript; a pré-visualização do Mac e a do
  WhatsApp não são critério de aceite.
- Fotos e fontes embutidas no arquivo são provisórias: numa URL elas podem
  ser servidas à parte.

## Review Trigger

Início da CV3, ou estantes que as pessoas queiram mostrar só a alguns.
