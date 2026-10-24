# Instruções do Canvas — 89 Livros

## Finalidade

`canvas.md` é a projeção visual do roadmap: onde a construção está, o que trava o próximo passo e o que espera no horizonte. Tem três vistas: **Caminho de construção**, **Decisões em aberto** e **Próximas opções de trabalho**, seguidas de **Fundações assentadas** e **Horizonte**. Não é fonte canônica, inventário completo nem substituto do roadmap. Nenhum fato é registrado aqui primeiro.

## Fontes de verdade

| Situação | Fonte principal |
| --- | --- |
| CVs, Delivery Stories e stories | frontmatter `status:` em `docs/project/roadmap/**/index.md` e tabela `Candidate Stories` de cada DS |
| Ordem das entregas | `Delivery Arc` em `docs/project/roadmap/cv<N>-*/index.md` |
| Decisões | `docs/project/decisions/records/*.md`, campo `status` |
| Exploração promovida e sinais guardados | `docs/project/exploration/es-*/index.md`, seções `Candidate / Promotion` e `Kept-for-Later Signals` |
| Marcos concluídos | `docs/process/worklog/entries/` |
| Mudanças no turno | comandos, resultados e arquivos alterados no turno atual |

Quando as fontes divergirem, vale o frontmatter do item. Não inferir estado a partir de conversa, memória, nomes de pastas ou do cursor local do Mirror.

## Atualização ao final de cada turno

1. Ao fim de todo turno que tenha mudado o roadmap, uma decisão, a exploração ou o worklog, compare o que mudou com as linhas de `canvas.md`.
2. Consulte somente as fontes necessárias para confirmar a mudança.
3. Atualize apenas as linhas afetadas. Não reescreva o canvas inteiro sem necessidade.
4. Quando nada tiver mudado no panorama, não altere o arquivo.
5. Informe ao Navigator: `Canvas atualizado: <linhas alteradas>.` ou `Canvas sem alterações.`

Quando o Navigator pedir `status` ou `canvas`, releia as fontes, atualize o que for necessário e apresente o conteúdo de `canvas.md` como resposta.

## Gramática visual obrigatória

- Markdown puro. Sem HTML, bullets ou parágrafos explicativos. A única exceção é a citação de uma linha abaixo do título, com a pergunta que a CV ativa responde.
- Tabelas com três colunas em todas as seções.
- Estados do roadmap: ✅ `Done` · 🔵 `Validated` · 🟢 `Active` · 🟡 `Planned` · 🔴 `Blocked` · ⏸ `Deferred`. Itens `Dropped` saem do canvas.
- Decisões: 🟡 `Open` · ✅ `Decided`. Decisões `Decided`, `Superseded` ou `Dropped` saem de `Decisões em aberto` no turno seguinte à sua resolução.
- 🧭 marca uma opção de trabalho; ⚪ marca o horizonte, que ainda não é roadmap.
- O ícone vem seguido de uma palavra em português (`planejada`, `ativa`, `validada`, `concluída`, `bloqueada`, `adiada`, `aberta`) e, se útil, de uma nota curta após `·`.
- Não inserir legenda para os ícones.
- Barras com exatamente dez caracteres em código inline, combinando `█` e `░`, seguidas da contagem `feitas/total`.
- Uma story conta como feita só quando está `Done`. A barra de uma DS mostra suas stories `Done` sobre o total da tabela `Candidate Stories`. A barra da CV soma as stories de todas as suas DS.
- `↳` para Delivery Stories sob a CV; `　　↳` para stories sob a DS.

## Regras de expansão

- Mostrar todas as CVs que não estejam `Done`, em ordem, e todas as suas DS, na ordem do `Delivery Arc`, com o nome da DS em negrito.
- Expandir as stories de todas as DS, na ordem da tabela `Candidate Stories` de cada uma.
- Notas curtas após `·` podem indicar dependências ou decisões em aberto que afetam a story.
- Uma CV concluída sai do `Caminho de construção` e vai para `Fundações assentadas`.

## Próximas opções de trabalho

Oferecer até quatro escolhas reais de curto prazo, cada uma com um `Próximo gesto` concreto. Incluir sempre o próximo item recomendado do roadmap e as decisões que bloqueiam o trabalho imediato. Não mover itens do Horizonte para cá sem decisão do Navigator.

## Fronteira de escopo

O canvas mostra o presente e uma distância curta à frente. O `Horizonte` reflete apenas os sinais guardados da exploração e capacidades adiadas explicitamente pelo Navigator. Um sinal só sai do Horizonte quando virar CV ou DS no roadmap.

## Evolução da visualização

Se o Navigator mudar a estrutura, os ícones, as barras, as seções ou a intenção do canvas, atualizar `canvas.md` e este arquivo no mesmo turno. Estas instruções descrevem sempre a visualização em uso.
