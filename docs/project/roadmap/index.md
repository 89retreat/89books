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
| [CV1](cv1-primeira-estante-viva/index.md) | A Primeira Estante Viva | Planned |

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
