---
code: CV1
level: Value
status: Active
status_reason: CV1.DS1 em andamento
updated: 2026-10-25
related:
  - ../../exploration/es-001-a-estante-como-retrato/index.md
---

[< Roadmap](../index.md)

# CV1 — A Primeira Estante Viva

**Status:** Active

---

## Intent

O grupo inicial de amigos consegue entrar sem começar vazio, ter uma estante
visitável com a foto da estante física como presença e fazer a leitura circular
no grupo do Telegram por dois movimentos: **comecei a ler** e **insight**.

O experimento responde a uma pergunta: **uma estante visível e movimentos
simples já fazem conversas nascerem?**

Origem: [ES-001](../../exploration/es-001-a-estante-como-retrato/index.md).

## Delivery Arc

Navegação. O status de cada DS vive no próprio `index.md`.

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV1.DS1](cv1-ds1-fundacao/index.md) | Fundação: reconhecimento de livros e decisões técnicas | Sabemos se foto e print viram lista confiável de livros; decisões técnicas registradas; esqueleto no ar |
| [CV1.DS2](cv1-ds2-entrada-sem-vazio/index.md) | Entrada sem estado vazio | Cada pessoa entra por foto, print do Kindle ou seleção e termina com uma estante revisada |
| [CV1.DS3](cv1-ds3-estante-visitavel/index.md) | Estante visitável | Cada estante se apresenta pela foto e pode ser visitada por qualquer membro do grupo |
| [CV1.DS4](cv1-ds4-movimentos-que-circulam/index.md) | Movimentos que circulam | "Comecei a ler" e insights chegam ao grupo do Telegram com link para a estante |

Ordem sugerida: DS1 primeiro, porque reconhecer livros numa foto é o maior
risco técnico e condiciona a entrada. Depois DS2 → DS3 → DS4. Se o
reconhecimento se mostrar fraco, a DS2 começa pela seleção manual e o spike
orienta o que fazer.

## Scope

Fora desta CV até o uso real pedir (vindo direto da exploração):

- feed próprio, mensagens ou conversa dentro do produto;
- resenhas completas, metas, estrelas;
- timeline ou reconstrução da jornada de leitura;
- organização espacial autoral (regiões, cabeceira, arrastar livros);
- várias fotos ou lugares da casa por pessoa;
- histórico de mudanças da estante física;
- compatibilidade ou afinidade entre leitores;
- perfil público, seguidores, descoberta de desconhecidos;
- importação de Readwise, Goodreads ou highlights do Kindle.

## Open Decisions

Registros com `status: Open` em
[decisions/records/](../../decisions/records/): interface principal,
reconhecimento de livros, acesso do grupo, grupo do Telegram, privacidade dos
insights e Navigator dos colaboradores.

## Acceptance / Done Condition

O grupo inicial usou a estante e os dois movimentos por um período combinado
(sugestão: 3 a 4 semanas). Os sinais abaixo foram respondidos numa
retrospectiva registrada no worklog, que decide a próxima CV.

Sinais a observar (perguntas ao uso, não métricas a otimizar):

- Todos conseguiram entrar sem começar vazios? Quanto custou corrigir o
  reconhecimento?
- As pessoas visitam as estantes umas das outras sem serem lembradas?
- Os movimentos no Telegram geram perguntas, comentários e recomendações, ou
  silêncio?
- Registrar insight é natural ou vira obrigação?
- A frequência dá vida ao grupo ou vira ruído?
- Que necessidade nova aparece primeiro?

## Validation Route

Retrospectiva com o grupo ao fim do período, registrada em
`docs/process/worklog/entries/`.
