[< Story](index.md)

# Plan — CV1.DS1.TS2

## Objective

Fechar as decisões técnicas da CV1 (interface principal, acesso do grupo,
stack e hospedagem) a partir do relatório da TS1, para que a TS3 monte o
esqueleto sem rediscutir a base.

## Pull

Puxada em 2026-10-26, logo depois do fechamento da TS1, em cadência
`accelerated`: o Navigator delegou ao Driver propor e registrar as decisões
sem parada de aprovação do plano. O aceite das decisões acontece na Validação.

## Prepare

- Relatório da TS1: Sonnet 5.5 para reconhecer; revisão obrigatória; ~7–16 s
  de modelo por imagem; Open Library acha ~72% das obras e tem capa para ~60%.
- Princípios: a estante é o centro (visual de capas); a conversa acontece no
  Telegram; uso "de pronta", sem instalação pesada.
- Grupo de ~10 pessoas, no celular. Colaboradores com perfis mistos (Python,
  TypeScript); o código será escrito majoritariamente por agentes.
- O código do spike (OpenRouter, Open Library, casamento de títulos) é Python.

## Scope

- Registro `interface-principal` → `Decided`, com opções e consequências.
- Registro `acesso-do-grupo` → `Decided`, com opções e consequências.
- Novo registro `stack-e-hospedagem` (`Decided`): linguagem e framework,
  banco, armazenamento das fotos, tarefas em segundo plano, hospedagem, deploy,
  custo mensal esperado e fonte de metadados.
- Medir o Google Books como segunda fonte de metadados com os itens já
  extraídos no spike (`spikes/reconhecimento/segunda_fonte.py`), sem chamar o
  modelo de visão.
- Atualizar `docs/project/briefing.md` (Architecture Premises) e
  `docs/process/development-guide.md` (Project Commands previstos).
- Atualizar roadmap e canvas.

## Non-Goals

- Não implementar o esqueleto (`CV1.DS1.TS3`) nem qualquer código de produto.
- Não decidir grupo do Telegram, privacidade dos insights nem Navigator dos
  colaboradores.
- Não criar contas, bots, chaves ou recursos pagos.
- Não tocar nas DS2, DS3 e DS4 além de citar consequências nos registros.

## Acceptance Behavior

```text
Given o relatório do spike TS1
When o Navigator lê os registros de interface principal, acesso do grupo e stack/hospedagem
Then os três estão Decided, com opções consideradas, justificativa e consequências
And o briefing (Architecture Premises) e o guia local refletem as decisões
And a avaliação da segunda fonte de metadados está registrada com o que foi ou não medido
```

## Validation Route

- Automático: `cd spikes/reconhecimento && uv run pytest` continua passando;
  `grep -l "status: Open"` não lista mais os registros de interface e acesso.
- Navigator: ler os três registros e aceitar ou ajustar as decisões.
  - Observação esperada: cada registro com decisão, justificativa ligada ao
    relatório da TS1 e consequências para TS3, DS2, DS3 e DS4.
  - Passa: o Navigator reconhece a justificativa e aceita.
  - Falha: decisão sem justificativa, conflito com os princípios ou com o
    relatório, ou uma escolha que o Navigator não sustenta.

E2E decision: not required. A story só produz registros e documentação; não
há superfície de produto.

## Implementation Contract

- Decisões escritas em português, seguindo o template de registro do projeto.
- Números citados só se medidos; o que não foi medido fica explícito.
- Status atualizado nos três lugares (frontmatter, linha `**Status:**`,
  tabela da DS).
- Use uv run for Python commands and tests.
- Commit apenas arquivos da story; mensagem em inglês explicando o porquê.
  Sem push sem comando do Navigator.

## Stop Conditions

- scope_change_detected
- plan_rule_conflict
- failing_required_check_without_clear_fix
- navigator_decision_needed

## Approval Gate

- active checkpoint: `after_plan`
- pending confirmation: `navigator_approval`, satisfeita pela autoridade de
  plano da cadência `accelerated` (2026-10-26).
