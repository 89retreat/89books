---
code: CV1
level: Value
status: Active
status_reason: reorganizada pela ES-002 em torno do MVP local; CV1.DS1 em andamento
updated: 2026-10-26
related:
  - ../../exploration/es-001-a-estante-como-retrato/index.md
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

[< Roadmap](../index.md)

# CV1 — A Primeira Estante Viva

**Status:** Active

---

## Intent

Cada pessoa do grupo põe fotos da própria estante numa pasta, roda um script
e recebe uma estante bonita num arquivo HTML: as fotos, os livros reconhecidos
e um **retrato de si** (a lente que a estante revela e os temas que se
repetem). Ela corrige aos poucos, gera o retrato de novo se não se reconhecer
e decide se manda o arquivo, publica um link ou as duas coisas.

Não há bot, servidor, login nem hospedagem. A estante é o prêmio pelo esforço
do input.

O experimento responde a uma pergunta: **uma estante bonita, com um retrato de
si, dá vontade de ser mostrada e desperta visitas e conversas?**

Origem: [ES-001](../../exploration/es-001-a-estante-como-retrato/index.md),
reorganizada pela
[ES-002](../../exploration/es-002-a-estante-num-arquivo/index.md) em
2026-10-26. A entrada pelo Telegram e os movimentos foram para a
[CV2](../cv2-a-estante-no-telegram/index.md).

## Delivery Arc

Navegação. O status de cada DS vive no próprio `index.md`.

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV1.DS1](cv1-ds1-fundacao/index.md) | Fundação: reconhecimento de livros e decisões técnicas | Sabemos que foto e print viram lista de livros; decisões técnicas do MVP local registradas |
| [CV1.DS2](cv1-ds2-a-estante-num-arquivo/index.md) | A estante num arquivo | Cada pessoa roda o script sobre as próprias fotos e recebe uma estante bonita, com o retrato de si, que pode corrigir |
| [CV1.DS3](cv1-ds3-estante-visitavel/index.md) | Estante visitável | A pessoa escolhe mandar o arquivo ou publicar um link, e outras pessoas visitam a estante |

Ordem: DS1 → DS2 → DS3. A DS2 começa pela estante feia e completa (US1) e
depois cuida da beleza (US2), porque o retrato já mostrou valor no
experimento com o Lula.

## Scope

Fora desta CV até o uso real pedir:

- bot do Telegram, grupo dedicado e movimentos ("comecei a ler", insight):
  ficam na CV2;
- print do Kindle e seleção manual como portas de entrada;
- sinalização do que a IA não teve certeza;
- servidor, contas, login ou banco de dados;
- feed, mensagens, resenhas, metas, estrelas;
- organização espacial autoral, várias estantes por pessoa;
- afinidade entre leitores, perfil público, descoberta de desconhecidos;
- importação de Readwise, Goodreads ou highlights do Kindle.

## Open Decisions

Registros com `status: Open` em
[decisions/records/](../../decisions/records/): onde publicar no GitHub Pages
e Navigator dos colaboradores.

## Acceptance / Done Condition

Todos do grupo inicial geraram a própria estante e a mostraram a alguém, por
arquivo ou link. Os sinais abaixo foram respondidos numa retrospectiva
registrada no worklog, que decide se a CV2 começa.

Sinais a observar (perguntas ao uso, não métricas a otimizar):

- Rodar o script foi simples para todos? Onde travou?
- As pessoas se reconheceram no retrato? Quantas pediram outro?
- Quanto custou corrigir a estante?
- As pessoas mostraram a estante sem serem lembradas? Para quem?
- Quem recebeu uma estante a visitou, respondeu ou puxou conversa?
- Que necessidade nova aparece primeiro?

## Validation Route

Retrospectiva com o grupo, registrada em `docs/process/worklog/entries/`.
