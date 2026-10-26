# Handoff Info: A Estante num Arquivo

## Handoff Summary

Reorganizar a CV1 em torno de um MVP local: cada pessoa põe as fotos da estante ou das prateleiras numa pasta, configura a chave do OpenRouter num arquivo e roda um script Python. O resultado é um HTML autocontido e bonito da sua estante, com as fotos, a capa escolhida, os livros (com visual próprio para os ~40% sem capa na Open Library) e o retrato de si em duas partes, a lente e os temas que se repetem. A pessoa corrige apagando linhas de um arquivo de livros e rodando de novo, com o reconhecimento em cache, e pode gerar o retrato outra vez. Ela escolhe compartilhar o arquivo, publicar no GitHub Pages ou as duas coisas. Sem bot, servidor, login ou hospedagem. O Telegram (bot como porta, grupo dedicado, movimentos) passa para uma CV seguinte, já com as respostas desta exploração.

## Handoff Completeness Checklist

- [x] continuous exploratory thickening
- [ ] source evidence list
- [x] surfaces and story state
- [x] phases or evolution narrative
- [ ] examples or simulations
- [x] product decisions
- [ ] user conversation flows
- [x] transition rules
- [x] risks
- [x] boundaries
- [x] open questions
- [x] what Builder should preserve
- [x] what Builder should not assume

Missing or weak evidence before Builder should treat this as complete:
- source evidence list
- examples or simulations
- user conversation flows

## What Builder Should Preserve

- The exploration is not only a feature request. It carries discovery context and product judgment.
- The attractor and experiment proposal should guide Builder's first roadmap framing.
- The product design proposal should be translated into roadmap/story docs only after Builder reads the project.

## Risks

- Builder may over-treat exploratory material as settled delivery scope.
- Builder may flatten open questions into implementation assumptions.
- Builder may focus on mechanism before preserving the user-facing product shape.

## Open Questions

- Which parts of this exploration should become roadmap stories?
- What validation route proves the product behavior externally?
- What should remain outside the first delivery slice?

## Boundaries

- This handoff is not a delivery plan.
- Builder must still read the project, create or update roadmap/story docs, and validate with the Navigator.
- Explorer preserved uncertainty; Builder should not erase it prematurely.

## Non-Assumptions

- Do not assume implementation architecture from this handoff.
- Do not assume all open questions are in scope.
- Do not assume the experiment proposal has already been validated.

## Attractors

_No attractors recorded._

## Experiment Status

**O retrato do Lula, feito à mão** (`proposed`)

Gerar o retrato de si (frase sobre a lente, temas que se repetem, pergunta que a estante desperta) a partir dos livros que o Sonnet 5.5 extraiu das fotos do Lula no spike, com os erros de leitura incluídos, como o produto faria. O Alisson envia o texto ao Lula, sem página nem bot. Observar: se ele reconhece a si ('é isso mesmo'), se corrige ou contesta algo, se o tom soa como horóscopo ou julgamento, e se ele espontaneamente quer mostrar a alguém. Se possível, repetir com o Raphael (Kindle) para ter dois leitores. Custo: centavos. Resultado orienta o prompt do retrato e confirma se o centro do MVP se sustenta antes de construir.

## Promotion Boundary

Builder executes only after explicit confirmation from the Navigator.
