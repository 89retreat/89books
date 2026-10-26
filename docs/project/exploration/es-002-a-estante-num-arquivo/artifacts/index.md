# Exploration Handoff: A Estante num Arquivo

## Editorial Synthesis

A exploração começou durante a validação da CV1.DS1.TS2, quando o Navigator se inclinou a desfazer a decisão proposta pelo Driver (web app como interface, bot só para enviar) e levar toda a entrada para o Telegram. Uma correção de premissa mudou o eixo: a amizade do grupo vive no WhatsApp, e o Telegram entrou na ES-001 como ferramenta fácil de construir, não como lugar social. O Navigator deixou de lado a ideia de levar os movimentos a grupos sociais já instituídos e passou a julgar tudo por um critério só, a remoção de atritos. Daí vieram três decisões que sobrevivem ao MVP: o Telegram é requisito aceitável para o grupo e para futuros usuários; a estante aparece na hora com a leitura da IA e é corrigida aos poucos, o que dissolve a revisão obrigatória registrada na TS1; e a primeira leitura da IA vai além dos títulos e devolve um retrato de si. Na forma com Telegram, o bot vive em dois lugares, a conversa privada com cada pessoa (entrada, retrato, insights, comecei a ler) e um grupo dedicado onde publica só o que a pessoa escolhe; apresentar a estante ao grupo é um gesto dela. Isso responde às decisões abertas de grupo do Telegram (dedicado) e de privacidade dos insights (compartilhar é sempre escolha), e fica guardado para a CV seguinte. Um experimento de Mágico de Oz testou o centro do produto antes de qualquer construção: o retrato gerado com Sonnet 5.5 a partir dos 146 itens extraídos das fotos do Lula no spike, com os erros de leitura incluídos, custou US$ 0,016. O Lula se reconheceu. A pergunta final não ajudou e saiu; o retrato ficou com a lente e os temas que se repetem. O Navigator então simplificou o MVP partindo do prêmio que a pessoa recebe pelo esforço do input: uma pasta de fotos, uma chave de API, um script Python e, como resultado, um HTML muito bonito da sua estante. Como todos os colaboradores são técnicos, cada um roda o seu; o modo concierge foi descartado. O HTML é autocontido, com fotos comprimidas e embutidas. A estante circula como arquivo, como link no GitHub Pages ou das duas formas, e a pessoa decide. A Open Library não tem capa para cerca de 40% das obras, então o visual dos livros sem capa é o centro do trabalho de beleza, não acabamento. A correção acontece num arquivo de livros editável com reconhecimento em cache, a capa vem da primeira foto ou da configuração, e uma opção gera o retrato de novo. Ficam fora do MVP: bot, grupo dedicado, movimentos, print do Kindle, seleção manual e sinalização da incerteza da IA. Para o Builder: fechar a TS2 sem aceitar as decisões de interface, acesso e stack/hospedagem, substituindo-as por registros coerentes com o MVP local; trocar a consequência revisão obrigatória por correção gradual no registro de reconhecimento; reorganizar a CV1 em torno do script e mover o Telegram para uma CV seguinte; decidir onde a publicação no GitHub Pages acontece (repositório da org 89retreat ou repositório pessoal de cada um), o que pode ficar como decisão aberta porque a primeira entrega é o HTML local. Ponto não testado: o comprimento do retrato quando lido no celular.

## Durable Story

- Story id: `d6435720`
- Journey: `89-livros`
- Status: `active`

## Source Evidence

_No source conversations were attached to this handoff._

## What Was Decided

O Telegram como Porta da Estante

Durante a validação da CV1.DS1.TS2, o Navigator moveu a entrada para o Telegram (bot como porta, estante como página, grupo dedicado, estante que aparece na hora com a leitura da IA e é corrigida aos poucos). Experimento de 2026-10-26: o Lula se reconheceu no retrato gerado à mão a partir dos livros do spike; a pergunta saiu e o retrato ficou com a lente e os temas que se repetem. Depois o Navigator simplificou o MVP partindo do output de valor: cada pessoa põe as fotos numa pasta, configura a chave de API num arquivo e roda um script Python; o resultado é um HTML muito bonito da sua estante (fotos, livros, retrato). Decisões do Navigator: cada colaborador roda o seu, porque todos são técnicos (modo concierge descartado); o HTML é autocontido, com fotos comprimidas e embutidas; a estante circula como arquivo ou como link, e a própria pessoa escolhe; o link é uma publicação opcional no GitHub Pages (por exemplo da org 89retreat, com endereço difícil de adivinhar); livros sem capa na Open Library (~40%) ganham visual próprio, tratado como centro do trabalho de beleza e não como acabamento. Melhorias de fluxo propostas pelo Driver e não contestadas: correção por um arquivo de livros editável e nova execução com reconhecimento em cache; capa pela primeira foto ou indicada na configuração; opção para gerar o retrato de novo. Sem bot, servidor, acesso ou hospedagem no MVP; Telegram, grupo dedicado, movimentos, print do Kindle e seleção manual ficam para depois. A TS2 segue parada na Validação; o handoff precisa rever as decisões de interface, acesso, stack e hospedagem, grupo do Telegram, privacidade dos insights e a revisão obrigatória, e reorganizar a CV1 em torno do MVP do script.

## Transfer Documents

- [Exploratory Story](exploratory-story.md): discovery narrative and continuous thickening.
- [Handoff Info](handoff-info.md): risks, open questions, boundaries, and non-assumptions for Builder.
- [Product Design Proposal](product-design-proposal.md): user-facing product behavior, without implementation detail.
- Full conversation evidence was not included in this handoff.

## Current Attractors

_No attractors recorded._

## Current Experiment Proposal

**O retrato do Lula, feito à mão** (`accepted`)

Feito em 2026-10-26. Retrato gerado com Sonnet 5.5 a partir dos 146 itens extraídos das fotos do Lula no spike, com os erros de leitura incluídos (US$ 0,016, 9 s), e enviado pelo Alisson sem página nem bot, com consentimento do Lula. Resultado: o Lula se reconheceu no retrato. A pergunta final não foi útil e saiu do prompt; o retrato fica com a lente e os temas que se repetem. Não testado: o comprimento do retrato lido no celular e um segundo leitor (Raphael).

## Builder Reading Order

Read this `index.md` first, then `exploratory-story.md`, then `handoff-info.md`, then `product-design-proposal.md`. If `full-conversation.md` exists, read it as source evidence, not as a delivery plan. Treat the set as exploration output, not as a completed delivery plan.
