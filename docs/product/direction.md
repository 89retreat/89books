# Product Direction

Para onde o produto vai e por que caminho. Diferente dos
[princípios](principles.md), que dizem como o produto se comporta, aqui ficam
inclinações de design: apostas que orientam o roadmap e devem ser revistas
quando a evidência mudar. Registrado em 2026-10-28, depois da CV1.

## Círculos que se abrem

O roadmap segue o valor para a comunidade, de dentro para fora:

1. **Fundadores, todos técnicos** (CV1, CV2): pelo terminal, cada um gera a
   própria estante e a ajusta editando um arquivo.
2. **Amigos técnicos**: o mesmo caminho, sem mudança de produto. Basta o
   repositório público e o guia.
3. **Quem recebe a estante** (CV3): visita por um link, sem precisar ser
   técnico.
4. **Pessoas não técnicas** (CV4): entram por uma porta sem terminal, o bot
   do Telegram ou uma aplicação web
   ([decisão aberta](../project/decisions/records/2026-10-28T1400Z-a-porta-para-quem-nao-usa-o-terminal.md)).

Cada círculo deve deixar estantes prontas para o próximo: quem chega encontra
uma comunidade habitada, não um produto vazio.

## O terminal é um protótipo do produto

O terminal não é o produto, é o jeito mais barato de aprender o que o produto
deve fazer
([decisão](../project/decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md)).
O que ele precisa produzir para o círculo 4:

- **um núcleo** que um servidor roda sem mudança: gerar, desenhar, editar,
  guardar e restaurar versões;
- **um modelo de dados**: o `shelf.yaml`, com versão, que vira o registro de
  cada estante num banco;
- **uma lista de edições que importam**: o que os fundadores mais editarem
  vira um botão para quem não é técnico; o que ninguém usar não vira;
- **situações nomeadas**: criar, desenhar, refazer com fotos novas, pedir
  outro retrato, voltar a uma versão. Elas existem no terminal, no bot e na
  web, com nomes diferentes.

## Inclinações de design

- **A IA propõe, a pessoa decide.** A primeira estante sai pronta, sem
  formulário. Depois, toda decisão da pessoa prevalece sobre a da IA.
- **Edições pequenas antes de controle total.** Técnicos vão querer editar
  tudo; não técnicos talvez queiram esconder três livros e trocar uma capa.
  A versão para não técnicos começa pelas edições mais usadas, não por todas.
- **O caro acontece uma vez, o barato sempre.** Ler fotos e escrever o
  retrato custam e demoram; desenhar e editar são grátis e instantâneos. Num
  servidor, o caro vira tarefa em segundo plano.
- **A estante se compartilha por link.** O arquivo HTML é um artefato da
  validação entre fundadores; fora do grupo, a estante vive num endereço.

## O que o terminal adia, e não resolve

- **Quem paga.** No terminal, cada pessoa usa a própria chave do OpenRouter.
  Para não técnicos, alguém paga por elas.
- **Onde ficam as fotos.** No terminal, as fotos não saem da máquina da
  pessoa. Com uma porta sem terminal, elas vão para um servidor. Por isso
  essa garantia não deve virar o valor central do produto.
- **Tempo.** Cada semana a mais no terminal é uma semana sem amigos não
  técnicos. O gatilho de saída da CV2 (o primeiro amigo não técnico que queira
  uma estante) traz a decisão da porta para a frente.

## Sinais que mudam esta direção

- Os fundadores não editam quase nada na CV2: a estante gerada já basta, e
  vale ir mais cedo para a porta dos não técnicos.
- Os fundadores editam muito e pedem o que o arquivo não permite: a lista de
  edições está incompleta antes de virar botões.
- Amigos não técnicos aparecendo antes do fim da CV2.
