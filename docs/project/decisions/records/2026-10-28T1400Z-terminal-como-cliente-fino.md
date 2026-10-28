---
status: Decided
raised: 2026-10-28
decided: 2026-10-28
deciders:
  - Navigator (Alisson)
supersedes:
related:
  - CV2
  - CV4
  - 2026-10-24T2013Z-interface-principal.md
  - ../../../product/direction.md
---

# O terminal é um cliente fino sobre um núcleo que um servidor também roda

## Question

O roadmap segue o valor para a comunidade: fundadores técnicos, depois amigos
técnicos, depois pessoas não técnicas, pelo Telegram ou por uma aplicação web.
Resolver primeiro pelo terminal ajuda ou atrapalha lá na frente?

## Decision

**O terminal é um protótipo barato do produto, não o produto.** Ele vale
enquanto o público é técnico, e tudo o que se aprende nele deve passar para a
porta dos não técnicos. Para isso:

1. **Núcleo sem terminal.** Cada operação da estante (gerar, desenhar,
   guardar versão, restaurar, pedir outro retrato) é uma função que recebe
   dados e devolve resultado, sem perguntar e sem imprimir. O comando só
   pergunta, confirma e mostra. Um servidor chama as mesmas funções.
2. **O `shelf.yaml` é o modelo de dados.** Tem versão e uma única validação,
   que um servidor reaproveita para o mesmo registro guardado num banco.
3. **Edições são operações com nome.** Esconder, pôr de frente, mover de
   prateleira, trocar capa e reescrever texto são operações do núcleo, não só
   campos soltos. Na web ou no bot, cada uma vira um botão.
4. **Medir o que é editado.** Com o consentimento de cada fundador, a
   retrospectiva da CV2 compara as versões em `history/`.
5. **Gatilho de saída.** O primeiro amigo não técnico que queira a própria
   estante puxa a decisão sobre
   [a porta para quem não usa o terminal](2026-10-28T1400Z-a-porta-para-quem-nao-usa-o-terminal.md),
   mesmo com a CV2 em andamento.

## Rationale

- Descobrir o que as pessoas querem mudar na estante custa dias com um
  arquivo editável e semanas com uma interface, talvez a errada.
- A separação entre gerar (caro, lento) e desenhar (grátis, instantâneo) é a
  mesma de um servidor: o reconhecimento vira tarefa em segundo plano e a
  página se redesenha a cada edição.
- As estantes dos fundadores e amigos já estarão prontas quando os não
  técnicos chegarem: eles encontram uma comunidade habitada.

## Options Considered

- **Terminal como cliente fino sobre um núcleo** (escolhida).
- **Ir direto para o bot ou a aplicação web:** mais caro, sem saber ainda
  quais edições importam.
- **Investir no terminal como produto** (validação sofisticada, atalhos,
  plugins de editor): nada disso passa para a web.

## Consequences

- Regra de desenvolvimento: lógica de produto não mora no módulo do comando;
  ver o [guia local](../../../process/development-guide.md#núcleo-e-terminal).
- O investimento no terminal se limita a perguntar, confirmar, mostrar e
  ajudar. Mensagens claras e o painel cabem; o que só serve ao terminal, não.
- O que os fundadores editam guia a versão para não técnicos, sabendo que
  técnicos usam mais controle que a média.
- A promessa "as fotos nunca saem da sua máquina" vale para o terminal, mas
  não será verdade quando houver servidor. Não reforçá-la como valor central
  do produto.
- No terminal, cada pessoa paga com a própria chave; para não técnicos,
  alguém paga por elas. Essa decisão vem junto com a da porta.

## Review Trigger

O gatilho de saída acima, ou a retrospectiva da CV2.
