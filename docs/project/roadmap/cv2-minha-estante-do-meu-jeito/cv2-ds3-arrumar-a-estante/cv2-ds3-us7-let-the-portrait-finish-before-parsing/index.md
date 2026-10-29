---
code: CV2.DS3.US7
level: User Story
status: Active
status_reason: o retry real preservou 237 livros, mas Claude Sonnet 5.5 consumiu o limite compartilhado de 4k tokens e cortou o JSON no terceiro tema
updated: 2026-10-29
related:
  - ../index.md
  - ../cv2-ds3-us6-keep-paid-work-after-a-failed-portrait/index.md
---

[< CV2.DS3](../index.md)

# CV2.DS3.US7 — Let the portrait finish before parsing

**Status:** Active

## User Story

Como fundador que já tem o trabalho pago salvo,
quero que o retrato receba espaço suficiente para pensar e terminar o JSON,
para que o retry de centavos conclua a estante em vez de falhar novamente.

## Outcome

As chamadas ao Claude Sonnet 5.5 seguem o contrato atual do modelo: sem
parâmetros de amostragem removidos, com esforço baixo explícito e com limite
suficiente para raciocínio e resposta compartilharem tokens. O retrato de uma
estante grande chega completo antes de ser validado pelo parser.

## Evidence That Pulled This Story

O arquivo privado autorizado pelo Navigator termina no meio da frase
`"*A Arte da Guerra ...* cuidam`, sem fechar a string, o tema, a lista ou o
objeto JSON. Tem 1.725 caracteres e é um prefixo estruturalmente válido, não um
JSON com pontuação interna defeituosa.

A documentação de migração do Claude Sonnet 5.5 informa que:

- raciocínio adaptativo é obrigatório e usa esforço `high` por padrão;
- raciocínio e resposta compartilham `max_tokens`;
- limites herdados de modelos sem thinking podem terminar em
  `stop_reason: max_tokens` sem resposta completa;
- `temperature`, `top_p` e `top_k` não padrão foram removidos.

O código atual envia `max_tokens=4000` e `temperature=0.7` para o retrato. A
proteção da US6 funcionou e preservou os 237 livros; esta story corrige a causa
da resposta truncada.
