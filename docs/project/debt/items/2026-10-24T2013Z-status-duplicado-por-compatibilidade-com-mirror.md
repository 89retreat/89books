---
id:
status: Carried
kind: process
severity: low
source: adoção do Ariad (2026-10-24)
revisit_trigger: o runtime do Mirror Mind passar a ler o status do frontmatter, ou duas divergências de status encontradas num coherence check
closure_condition: o status de cada item do roadmap vive só no frontmatter, e as tabelas centrais deixam de repetir o status
---

# Status do roadmap duplicado por compatibilidade com o Mirror

## Description

O Ariad recomenda que o status de um item do roadmap viva só no próprio item.
Aqui o status aparece em três lugares: no frontmatter do item, numa linha
`**Status:**` no mesmo arquivo e na tabela `Candidate Stories` da DS mãe. A
tabela de CVs no índice do roadmap também repete o status de cada CV.

## Carrying Reason

O runtime do Mirror Mind, usado por parte do grupo, não lê o frontmatter. O
pull-candidates lê a linha `**Status:**`, o Expand e o fechamento da DS leem a
tabela `Candidate Stories`, e o snapshot lê a tabela de CVs. Sem a duplicação,
o Builder Mode do Mirror deixaria de enxergar o roadmap.

## Impact

Risco de divergência entre os três lugares quando alguém atualiza só um deles,
o que causaria conflitos de merge e confusão sobre o estado real. Mitigado pela
regra "em divergência, vale o frontmatter".

## Revisit Trigger

O runtime do Mirror passar a ler o frontmatter (sugestão a registrar no
desenvolvimento do Mirror, `mirror-dev`), ou divergências de status aparecerem
em coherence checks.

## Closure Condition

Status apenas no frontmatter; tabelas como navegação, sem coluna de status.

## Notes

Ver [development-guide.md → Local Exceptions](../../../process/development-guide.md#local-exceptions).
