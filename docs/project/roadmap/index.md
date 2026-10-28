# Roadmap

O roadmap descreve progresso significativo, não cada tarefa.

Este índice explica a estrutura e as convenções do roadmap. Cada item vive na
própria pasta e carrega o próprio `status`.

## Taxonomy

Taxonomia padrão do Ariad (detalhes em
[development-guide.md](../../process/development-guide.md#roadmap-taxonomy)):

- **Value / CV** (Capability Value): etapa do produto com impacto visível.
- **Delivery Story (DS)**: arco de entrega dentro de uma CV, com condição de
  pronto. Expande-se em User e Technical Stories antes de qualquer plano.
- **User Story (US)**: entrega atômica verificável por comportamento
  observável.
- **Technical Story (TS)**: capacidade interna necessária a uma DS.
- **Task**: trabalho dentro de uma story. Não vira item de roadmap.
- **Maintenance**: trabalho legítimo fora da hierarquia.

## Codes and Folders

```text
docs/project/roadmap/
  index.md
  cv<N>-<value-slug>/
    index.md
    cv<N>-ds<M>-<delivery-story-slug>/
      index.md
      cv<N>-ds<M>-us<K>-<user-story-slug>/
        index.md
        plan.md
        test-guide.md
      cv<N>-ds<M>-ts<K>-<technical-story-slug>/
        index.md
        plan.md
        test-guide.md
```

A pasta de uma User ou Technical Story nasce quando ela é puxada para
execução. Antes disso, a story existe só como linha na tabela
`Candidate Stories` da DS.

## State Representation

Estados: `Planned`, `Active`, `Blocked`, `Validated`, `Done`, `Deferred`,
`Dropped`.

Cada item carrega o estado no frontmatter (fonte canônica) e repete o mesmo
estado numa linha `**Status:**` abaixo do título:

```markdown
---
code: CV<N>.DS<M>
level: Delivery Story
status: Active
status_reason: puxada para a entrega atual
updated: YYYY-MM-DD
---

[< CV<N>](../index.md)

# CV<N>.DS<M> — Título

**Status:** Active
```

A tabela `Candidate Stories` de cada DS também repete o estado de cada filho.
Essa duplicação existe por compatibilidade com o runtime do Mirror Mind; ver
[Local Exceptions](../../process/development-guide.md#local-exceptions). Mudou
o estado, mude os três no mesmo commit.

## Capability Values

Única tabela central do roadmap, também mantida por compatibilidade com o
Mirror. As CVs mudam raramente.

| Code | Capability Value | Status |
|------|-----------------|--------|
| [CV1](cv1-primeira-estante-viva/index.md) | A Primeira Estante Viva | Done |
| [CV2](cv2-minha-estante-do-meu-jeito/index.md) | Minha estante, do meu jeito | Active |
| [CV3](cv3-a-estante-visitavel/index.md) | A Estante Visitável | Planned |
| [CV4](cv4-a-estante-no-telegram/index.md) | A Estante no Telegram | Planned |

Renumeração de 2026-10-27: a CV1 passou a ser a capacidade de ir do clone à
estante. A antiga CV1.DS3 virou CV2.DS2; a antiga CV1.DS2.US4 e a CV1.DS2.TS1
viraram CV2.DS1.US1 e CV2.DS1.TS1; a antiga CV2 (Telegram) virou CV3.
Registros de stories concluídas antes dessa data mantêm os códigos antigos.

Renumeração de 2026-10-28: a CV2 passou a ser "Minha estante, do meu jeito",
ajustar a estante editando o `shelf.yaml`. A antiga CV2.DS1 (corrigir) virou
CV2.DS2, e a sua TS1 virou CV2.DS2.TS1; o "pedir outro retrato" da antiga
CV2.DS1.US1 virou CV2.DS3.US5. A antiga CV2.DS2 (estante visitável) virou
CV3.DS1, numa CV3 própria. O Telegram, antes CV3, virou CV4.

## Product Path

O roadmap segue o valor para a comunidade, em círculos que se abrem:

1. **Fundadores, todos técnicos** (CV1, CV2): pelo terminal, cada um gera e
   ajusta a própria estante.
2. **Amigos técnicos**: o mesmo caminho, sem mudança de produto.
3. **Estantes visitáveis por link** (CV3): quem recebe não precisa ser
   técnico.
4. **Pessoas não técnicas** (CV4): uma porta sem terminal, pelo bot do
   Telegram ou por uma aplicação web, em decisão aberta.

O terminal é um cliente fino sobre um núcleo que um servidor também roda: o
que se constrói nos círculos 1 e 2 é a base do círculo 4. Ver a
[direção de produto](../../product/direction.md) e
[o terminal como cliente fino](../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md).

## How to Find Work

- Trabalho ativo: busque `status: Active`.
- Trabalho bloqueado: busque `status: Blocked`.
- Trabalho concluído: busque `status: Done`.
- Mudanças recentes: as entradas em
  [worklog/entries/](../../process/worklog/entries/).

## Item Template

Modelos em [templates/](templates/): `delivery-story-index.md`,
`user-story-index.md`, `technical-story-index.md`, `plan.md`, `test-guide.md`,
`review.md`, `coherence.md`.
