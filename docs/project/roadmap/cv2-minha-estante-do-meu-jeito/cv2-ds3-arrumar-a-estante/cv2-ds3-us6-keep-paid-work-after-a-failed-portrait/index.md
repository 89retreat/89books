---
code: CV2.DS3.US6
level: User Story
status: Done
status_reason: recuperação gratuita validada pelo Navigator e story fechada em 2026-10-29
updated: 2026-10-29
related:
  - ../index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/index.md
---

[< CV2.DS3](../index.md)

# CV2.DS3.US6 — Keep paid work after a failed portrait

**Status:** Done

## User Story

Como fundador que já pagou para reconhecer e revisar a estante,
quero preservar esse trabalho quando o retrato final vier inválido,
para concluir ou retomar a criação sem pagar novamente pelas fotos.

## Outcome

O fim da criação deixa de ser tudo-ou-nada: antes do retrato, o núcleo guarda
um rascunho privado dos livros finais. Se a resposta do retrato não puder ser
lida, a pessoa pode criar uma fonte inicial gratuita a partir desse rascunho ou
pedir somente outro retrato, com novo custo explícito.

## Evidence That Pulled This Story

No primeiro uso real após CV2.DS3.US4, 12 fotos chegaram a 237 livros
reconhecidos, 20 correções, 58 confirmações no Google Books e 129 capas. A
resposta final do retrato falhou em `json.loads` e nenhum `shelf.yaml` foi
criado. O cache atual preserva catálogos e capas, mas não preserva com fidelidade
a lista revisada nem a associação dos livros às fotos.
