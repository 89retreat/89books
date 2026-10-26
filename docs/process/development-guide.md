# Local Development Guide

Contrato operacional deste repositório para desenvolvimento com agentes.

O Ariad é o método canônico (https://github.com/mirror-mind-ai/ariad). Este
arquivo é a instância local do método: diz como Driver e Navigator trabalham
aqui, quais comandos importam, o que conta como validação e quais regras locais
prevalecem sobre o método genérico.

## Relationship to Ariad

Este projeto usa o Ariad como método de desenvolvimento humano-agente.

Quando o Ariad e este guia divergirem, vale este guia para o trabalho do
projeto. A divergência deve aparecer no coherence check.

Colaboradores podem usar qualquer agente de código. O ponto de entrada é o
`AGENTS.md` na raiz (o `CLAUDE.md` aponta para ele). Quem usa Mirror Mind
trabalha pelo Builder Mode da jornada `89-livros`, que segue os mesmos
arquivos. **O estado do projeto vive nos arquivos deste repositório**, não em
nenhum banco de dados local de agente.

## Driver and Navigator

O agente é o **Driver**. A pessoa que conduz a sessão é o **Navigator**.

O Driver lê o contexto, propõe planos, muda arquivos, roda checks, prepara
rotas de validação, atualiza a documentação e para nos checkpoints.

O Navigator detém a intenção, os trade-offs, o julgamento de produto e o
aceite.

> **Decisão aberta:** quem é o Navigator quando um colaborador trabalha.
> Ver `docs/project/decisions/records/2026-10-24T2013Z-navigator-dos-colaboradores.md`.
> Até a decisão, vale o padrão do Ariad: quem conduz a sessão é o Navigator
> dela, e nada entra na branch principal sem review de outra pessoa do grupo.

## Project Commands

Stack decidida na `CV1.DS1.TS2`
([registro](../project/decisions/records/2026-10-26T1332Z-stack-e-hospedagem.md)):
Python + Django + HTMX, SQLite, Fly.io. Os comandos abaixo são os previstos e
passam a valer quando a `CV1.DS1.TS3` criar o app; a TS3 corrige o que mudar.

```bash
# install dependencies
uv sync

# run tests
uv run pytest

# run lint or formatting checks
uv run ruff check . && uv run ruff format --check .

# run the app locally
uv run python manage.py migrate && uv run python manage.py runserver
```

Hoje só existe o spike, com comandos próprios em
`spikes/reconhecimento/README.md`. Segredos (chave do OpenRouter, token do
bot) nunca entram no repositório: localmente vêm do ambiente; em produção,
dos segredos do Fly.io.

## Verification

Trabalho verificado neste projeto significa:

- checks automatizados passando, quando houver código;
- para User Stories, uma rota de validação executada pelo Navigator num
  celular, já que a entrada (foto da estante) e a visita acontecem no celular;
- para mensagens no Telegram, validação num grupo de teste antes do grupo real;
- nunca usar fotos ou dados reais do grupo em fixtures públicas ou commits sem
  consentimento da pessoa.

## Documentation Rules

Superfícies de documentação:

- `AGENTS.md`: ponto de entrada dos agentes. Muda quando o modo de trabalhar
  muda.
- `docs/project/briefing.md`: premissas estáveis.
- `docs/product/principles.md`: princípios de produto que orientam trade-offs.
- `docs/project/decisions/records/`: uma decisão por arquivo.
- `docs/project/roadmap/`: CVs, Delivery Stories e stories, com status no
  próprio item.
- `docs/project/debt/items/`: um item de dívida técnica por arquivo.
- `docs/process/worklog/entries/`: um marco por arquivo.
- `docs/project/exploration/`: Exploratory Stories e seus artefatos.
- `canvas.md`: projeção visual derivada do roadmap, mantida segundo
  `canvas-instructions.md`. Nunca é fonte de verdade. Em conflito de merge,
  regenere a partir das fontes em vez de mesclar à mão.

## Conflict-Resistant Project Memory

Como várias pessoas e agentes vão editar o projeto, cada artefato durável tem
seu próprio arquivo:

- marcos do worklog em `docs/process/worklog/entries/`;
- decisões em `docs/project/decisions/records/`, com `status`;
- dívida técnica em `docs/project/debt/items/`;
- itens do roadmap com `status` no próprio arquivo.

Arquivos de índice explicam estrutura, nomes e templates. Não mantêm listas
completas, com as exceções registradas em Local Exceptions.

Nomes de arquivos com timestamp usam UTC: `YYYY-MM-DDTHHMMZ-slug.md`.

## Roadmap Taxonomy

Taxonomia padrão do Ariad:

- **Value / CV**: etapa do produto com impacto visível para os leitores.
- **Delivery Story (DS)**: arco de entrega coerente dentro de uma CV. Nunca é
  implementada diretamente; expande-se em User e Technical Stories.
- **User Story (US)**: entrega atômica verificável de ponta a ponta por
  comportamento observável.
- **Technical Story (TS)**: capacidade interna necessária a uma DS, verificada
  por evidência automatizada ou interna.
- **Task**: trabalho concreto dentro de uma story. Não vira item de roadmap.
- **Maintenance**: trabalho legítimo fora da hierarquia.

Códigos: `CV1`, `CV1.DS2`, `CV1.DS2.US1`, `CV1.DS1.TS3`. Pastas em
minúsculas: `cv1-primeira-estante-viva/cv1-ds2-entrada-sem-vazio/cv1-ds2-us1-entrar-pela-foto/`.

Estados: `Planned`, `Active`, `Blocked`, `Validated`, `Done`, `Deferred`,
`Dropped`. Quando o trabalho não pode seguir, use `Blocked` com
`status_reason`.

## Expand and Collapse

Expanda quando o trabalho estiver travado por ambiguidade: separar
preocupações, nomear opções, esclarecer escopo, desdobrar uma DS nas suas
stories.

Colapse quando o trabalho estiver perdido em fragmentos: relacionar partes,
atualizar status, nomear o valor que emergiu, fechar uma story ou uma DS.

## User and Technical Story Lifecycle

Para trabalho não trivial, siga o ciclo do Ariad descrito no `AGENTS.md`:
planejar, nomear o comportamento de aceite em Given / When / Then / And,
implementar, testar e validar, documentar, revisar com coherence check e
registrar o histórico.

Regras locais:

- O plano vive em `<pasta-da-story>/plan.md` e a rota de validação em
  `test-guide.md`, usando `docs/project/roadmap/templates/`.
- A aprovação do plano é registrada no próprio `plan.md` (quem, quando).
- Stories que tocam a experiência de leitura (estante, movimentos, mensagens)
  devem citar no plano qual princípio de produto estão preservando.

## Technical Debt Tracking

Use `docs/project/debt/items/`, um arquivo por item, quando a dívida precisar
sobreviver à review de uma story. Na Review, nomeie: dívida paga, dívida nova,
dívida carregada, gatilho de revisita e se um item deve ser criado ou
atualizado.

## Checkpoints

Pare para confirmação do Navigator:

- depois de mostrar o plano; criar o `plan.md` não substitui o checkpoint
  visível;
- depois dos checks automatizados, com uma rota de validação concreta para o
  Navigator (observações esperadas, condição de sucesso, condição de falha);
- depois da review e da avaliação de refatoração;
- antes de qualquer push (ver Commit and Release Rules).

O commit não é checkpoint: acontece ao fim de cada turno, sem pedir
confirmação.

## Navigator Preferences

- **Commit policy:** um commit por turno. Ao fim de todo turno que mudou
  arquivos, o Driver faz commit do que mudou, sem pedir confirmação.
  Mensagens em inglês, explicando o porquê.
- **Push policy:** push só sob comando explícito do Navigator.
- **Checkpoint compression:** checkpoints completos para trabalho não trivial;
  comprimidos só para mudanças triviais de baixo risco.
- **Documentation detail:** a menor atualização que mantenha o projeto
  coerente.
- **Worklog policy:** um arquivo por marco relevante, não por edição.
- **Branch/PR habits:** uma branch por story (`cv1-ds2-us1-entrar-pela-foto`)
  e PR para a branch principal. Nenhum merge sem review de outra pessoa do
  grupo. (A confirmar junto com a decisão sobre o Navigator dos
  colaboradores.)

## Commit and Release Rules

### Commit por turno

- Ao fim de cada turno em que arquivos mudaram, faça um commit com todas as
  mudanças do turno, incluindo o `canvas.md` atualizado.
- Um commit por turno, mesmo que o turno avance só parte de uma story. O
  histórico registra o caminho; o fechamento da story aparece no commit do
  turno em que ela chega a `Done`.
- Turno sem mudança de arquivo não gera commit.
- Mensagem em inglês: uma linha de resumo e, quando ajudar, um corpo curto
  explicando o porquê. Cite o código da story quando houver
  (`CV1.DS1.TS1: ...`).
- Nunca faça commit de arquivos ignorados pelo `.gitignore` nem de fotos ou
  dados reais do grupo sem consentimento.
- Ao fim do turno, informe o commit: `Commit <hash>: <resumo>.`

### Push sob comando

- Nunca faça push por conta própria, nem ao fechar uma story.
- Faça push apenas quando o Navigator pedir explicitamente ("push", "suba",
  "publique no remoto").
- Antes do push, confira se a branch está atualizada com o remoto. Se houver
  divergência ou conflito, pare e mostre a situação ao Navigator.
- Depois do push, informe a branch e o hash publicado.

### Releases

Ainda não há releases. O fim da CV1 é um marco de produto (o experimento com o
grupo), não uma versão pública. Se uma Delivery Story criar uma fronteira de
release, isso deve ser declarado na DS.

## Local Exceptions

### Status duplicado por compatibilidade com o Mirror

O Ariad recomenda que o status de um item do roadmap viva só no próprio item,
sem tabelas centrais. Aqui, por compatibilidade com o runtime do Mirror Mind
(usado por parte do grupo), o status aparece em três lugares:

1. o frontmatter `status:` do item, que é a **fonte canônica**;
2. uma linha `**Status:**` logo abaixo do título do mesmo arquivo, que o
   runtime do Mirror lê;
3. a linha do item na tabela `Candidate Stories` da Delivery Story mãe, que o
   Expand e o fechamento da DS no Mirror leem.

A tabela de CVs em `docs/project/roadmap/index.md` também repete o status de
cada CV, porque o snapshot do roadmap no Mirror a lê.

Regra: mudou o status, mude os três no mesmo commit. Em divergência, vale o
frontmatter.

Revisitar quando o runtime do Mirror passar a ler o frontmatter. Ver
`docs/project/debt/items/2026-10-24T2013Z-status-duplicado-por-compatibilidade-com-mirror.md`.
