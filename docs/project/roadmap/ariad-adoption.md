[< Roadmap](index.md)

# Ariad Adoption

Este projeto segue o **Ariad** (https://github.com/mirror-mind-ai/ariad).

- Ponto de entrada para qualquer agente: [AGENTS.md](../../../AGENTS.md).
- Contrato local: [development-guide.md](../../process/development-guide.md).

## Method

- adopted method: ariad
- adoption date: 2026-10-24
- adoption mode: desde o início, seguindo os modelos públicos do Ariad
  (`docs/project-templates/`)
- runtimes: qualquer agente de código via `AGENTS.md`; Mirror Mind Builder
  Mode pela jornada `89-livros`

## Source of Truth

O estado do projeto vive nos arquivos deste repositório. O estado de execução
que o Mirror Mind guarda localmente (cursor de entrega, checkpoint ativo) serve
só para retomar sessões no Mirror. Quando divergir dos arquivos, valem os
arquivos.

## Runtime State (Mirror Mind)

- delivery cursor: sincronizado na adoção
- cadence: `stepwise` (padrão do runtime)
- navigator flow unit: `story_by_story`
- active item: none
- recomendação: `CV1.DS1` (Fundação)

## Known Gaps

- A transcrição integral da exploração fica fora do repositório (`.gitignore`)
  até o grupo concordar em compartilhá-la.
- O status do roadmap aparece em três lugares por compatibilidade com o
  Mirror; ver o item de dívida
  [status duplicado](../debt/items/2026-10-24T2013Z-status-duplicado-por-compatibilidade-com-mirror.md).
- O Mirror gera os `index.md` das stories durante o Expand sem frontmatter. O
  Driver precisa acrescentá-lo ao materializar cada story.

## Boundaries

Adoção, preparação de templates e sincronização do cursor não executam
trabalho de story, não mudam status, não fazem commit, push ou release.
