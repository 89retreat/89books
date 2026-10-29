---
code: CV2.DS3
level: Delivery Story
status: Active
status_reason: capacidade agregada entregue por US1–US4; falta um fundador usar as quatro escolhas na própria estante e mostrá-la a alguém
updated: 2026-10-29
related:
  - ../index.md
  - ../cv2-ds1-a-estante-num-arquivo-meu/index.md
---

[< CV2](../index.md)

# CV2.DS3 — Arrumar a estante

**Status:** Active

---

## Outcome

A pessoa organiza a estante do jeito dela: em que prateleira cada livro fica
e em que ordem, quais ficam de frente, qual foto abre a página e o que dizem
os títulos e textos das prateleiras e a abertura. As regras automáticas da
CV1 (quem fica de frente, quais fileiras recolhem) valem só para o que ela não
decidiu.

Preserva o princípio "cada leitor revela a própria lógica": a organização
autoral, que estava fora da CV1, entra aqui.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV2.DS3.US1](cv2-ds3-us1-put-each-book-on-the-shelf-i-choose/index.md) | Put each book on the shelf I choose | User Story | Mover as linhas de um livro no arquivo muda a prateleira e a ordem dele na página; posso criar, apagar e reordenar prateleiras. | Done |
| [CV2.DS3.US2](cv2-ds3-us2-face-out-or-spine-my-choice/index.md) | Face out or spine, my choice | User Story | Com `face: true`, o livro fica de frente; com `face: false`, mostra a lombada; sem o campo, segue a regra automática. Uma prateleira com livros demais de frente quebra em mais fileiras. | Done |
| [CV2.DS3.US3](cv2-ds3-us3-choose-the-photo-that-represents-my-shelf/index.md) | Choose the photo that represents my shelf | User Story | `cover_photo` no `shelf.yaml` escolhe a foto em destaque no mosaico, a que representa a estante; sai do `config.toml`. | Done |
| [CV2.DS3.US4](cv2-ds3-us4-write-my-own-shelf-titles-and-texts/index.md) | Write my own shelf titles and texts | User Story | Reescrevo a abertura (`lens`) e o título e o texto de cada prateleira; a página mostra o que escrevi, com itálico em `*título*` como hoje. | Done |
| [CV2.DS3.US5](cv2-ds3-us5-ask-for-another-portrait/index.md) | Ask for another portrait | User Story | `portrait` guarda uma versão, confirma o custo (centavos) e reescreve a abertura e as prateleiras a partir dos livros que ficaram, sem ler as fotos. Puxada só se os fundadores sentirem falta depois de editar à mão. Era parte da antiga CV2.DS1.US1. | Planned · conditional |

## Aggregate Evaluation — 2026-10-29

### Scope proposed for closure

- US1: ordem, prateleiras e livros autorais — Done e validada.
- US2: frente, lombada e automático — Done e validada.
- US3: foto principal — Done e validada.
- US4: abertura, títulos e textos — Done e validada.
- US5 não é requisito de fechamento: continua condicional a evidência de uso.

### Result

A capacidade técnica e o comportamento observável do outcome estão presentes.
As quatro escolhas foram validadas separadamente em fixtures descartáveis e
compartilham a mesma fonte, `shelf.yaml`. Isso prova as partes, mas ainda não
prova o marco de produto da Delivery Story.

### Missing founder evidence

Ainda não há registro de **um fundador usando as quatro escolhas juntas na
própria estante e mostrando o resultado a alguém como sendo sua estante**.
Fixtures e páginas de validação não substituem esse gesto. Por isso, a DS
permanece `Active` e não deve ser fechada apenas por cobertura técnica.

### Navigator route

1. Em uma estante real de fundador, guardar/desenhar a fonte atual.
2. Mover pelo menos um livro ou prateleira.
3. Escolher frente/lombada de pelo menos um livro.
4. Escolher `cover_photo`.
5. Reescrever `lens` e ao menos um título ou texto de prateleira.
6. Rodar `check`, `draw` e `open`, todos gratuitos.
7. Mostrar a página a outra pessoa e confirmar que o fundador a reconhece como
   “minha estante”.

**Passa:** as quatro decisões aparecem juntas, nada some ou volta ao automático
contra a vontade da pessoa, e ela apresenta a página como sua. **Falha:** a
pessoa evita editar, não reconhece o resultado, precisa de outra proposta da IA
antes de mostrar ou encontra uma lacuna que exige nova story.

## Done Condition

Um fundador arrumou a própria estante (prateleiras, frente ou lombada, foto,
textos) e a mostrou a alguém como sendo a sua.
