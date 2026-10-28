---
code: CV2
level: Value
status: Planned
status_reason: reescrita pelo Navigator em 2026-10-28; pronta para puxar a DS1
updated: 2026-10-28
related:
  - ../cv1-primeira-estante-viva/index.md
  - ../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md
  - ../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md
  - ../../../product/direction.md
---

[< Roadmap](../index.md)

# CV2 — Minha estante, do meu jeito

**Status:** Planned

---

## Intent

**Capacidade:** a pessoa ajusta a estante gerada até ela ter a sua cara,
editando um arquivo e redesenhando a página, sem pagar de novo e sem medo de
perder o que fez.

A CV1 entregou uma estante que o modelo decide quase inteira: os livros, as
prateleiras, os títulos "Quando…", quais ficam de frente. Na CV2, a última
palavra passa a ser de quem lê. A pessoa pode:

- escolher a foto que fica em destaque no mosaico;
- esconder livros;
- corrigir títulos, autores e capas;
- decidir em que prateleira cada livro fica e em que ordem;
- escolher quais livros ficam de frente e quais mostram a lombada;
- reescrever o título e o texto de cada prateleira e a abertura.

Tudo isso por edição direta de um arquivo, o `my-bookshelf/shelf.yaml`, que
passa a ser a fonte da estante. Comandos com nomes explícitos separam o que
custa (gerar a partir das fotos) do que é grátis (desenhar a página), e todo
comando que reescreve o arquivo guarda uma versão antes.

Pergunta: **com a última palavra, a pessoa se reconhece na própria estante e
quer mostrá-la?**

Origem: avaliação do Navigator em 2026-10-28, depois da CV1. As decisões que a
sustentam estão em
[o arquivo da estante como fonte](../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md)
e
[o terminal como cliente fino](../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md).

## Por que pelo terminal, e o que isso exige

Os fundadores e os amigos que vêm a seguir são técnicos: editar um arquivo é
natural para eles e não exige construir interface. A CV2 é também o protótipo
barato do produto para quem não é técnico: o que os fundadores mais editarem
vira a lista de botões daquela versão. Ver a
[direção de produto](../../../product/direction.md).

Para o terminal ajudar e não atrapalhar o que vem depois:

- cada comando chama uma função de um núcleo que não pergunta nem imprime; o
  terminal só pergunta, confirma e mostra;
- o `shelf.yaml` tem versão (`version: 1`) e uma única validação, que um
  servidor reaproveita;
- cada edição é uma operação com nome no núcleo (esconder, pôr de frente,
  mover de prateleira, trocar capa), não só um campo solto.

## Commands

| Situação da pessoa | Comando | Custo | O que acontece com o `shelf.yaml` |
| --- | --- | --- | --- |
| Não sei em que pé estou | `uv run shelf` | grátis | Nada; mostra o estado e sugere o próximo comando |
| Primeira vez, só tenho as fotos | `uv run shelf create` | pago | Cria o arquivo; recusa se ele já existir |
| Editei o arquivo e quero ver | `uv run shelf draw` | grátis | Só lê; guarda uma versão se ele mudou |
| Quero conferir se o arquivo está certo | `uv run shelf check` | grátis | Só lê; aponta erros com o número da linha |
| Mudei a estante, tirei fotos novas | `uv run shelf recreate` | pago | Guarda uma versão e refaz tudo a partir das fotos |
| Fiz besteira e quero voltar | `uv run shelf history`, `uv run shelf restore <versão>` | grátis | Lista as versões; devolve a escolhida, guardando antes a atual |
| Quero abrir a estante | `uv run shelf open` | grátis | Nada |
| Trocar nome ou chave | `uv run shelf setup` | grátis | Nada; mexe só no `config.toml` |
| Não me reconheci no texto | `uv run shelf portrait` | centavos | Guarda uma versão e reescreve só o retrato (só se a DS3.US5 for puxada) |

Opções comuns: `--folder <pasta>` e `--yes`.

## Delivery Arc

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV2.DS1](cv2-ds1-a-estante-num-arquivo-meu/index.md) | A estante num arquivo meu | O `shelf.yaml` é a fonte da estante: gerar uma vez, desenhar de graça, saber onde estou e nunca perder uma edição |
| [CV2.DS2](cv2-ds2-corrigir-a-estante/index.md) | Corrigir a estante | Escondo livros e corrijo títulos, autores e capas no arquivo |
| [CV2.DS3](cv2-ds3-arrumar-a-estante/index.md) | Arrumar a estante | Decido prateleiras, ordem, frente ou lombada, a foto em destaque e os textos |

A DS1 vem primeiro: sem ela, cada edição se perde na próxima rodada.

## Scope

Volta aqui o que foi adiado ao fechar a CV1: gerar de novo relê e paga todas
as fotos (DS1); o pipeline aceita duas formas de resposta da revisão (DS1.TS1);
nomes curtos mantêm iniciais do catálogo e capas que são páginas amareladas
do miolo (DS2).

Fora desta CV:

- juntar fotos novas a uma estante já editada (algo como `add-photos`): por
  ora, `recreate` com versão guardada;
- abrir o arquivo num editor pelo comando (`edit`);
- publicar por link e reunir as estantes do grupo:
  [CV3](../cv3-a-estante-visitavel/index.md);
- bot do Telegram ou aplicação web para quem não é técnico:
  [CV4](../cv4-a-estante-no-telegram/index.md) e a decisão aberta sobre
  [a porta para quem não usa o terminal](../../decisions/records/2026-10-28T1400Z-a-porta-para-quem-nao-usa-o-terminal.md).

## Acceptance / Done Condition

Um ou mais fundadores ajustaram a própria estante editando o `shelf.yaml` e
redesenhando a página, sem pedir ajuda e sem perder edições.

Na retrospectiva, registrada no worklog, e com o consentimento de cada
fundador, comparar as versões em `my-bookshelf/history/` e responder:

- Quais edições as pessoas fizeram, e quantas?
- O que ninguém usou?
- O que pediram e não havia?

**Gatilho de saída:** o primeiro amigo não técnico que queira a própria
estante puxa a decisão sobre a porta para quem não usa o terminal, mesmo que
a CV2 não tenha terminado.

## Validation Route

O Navigator primeiro, com a própria estante; depois os outros fundadores.
