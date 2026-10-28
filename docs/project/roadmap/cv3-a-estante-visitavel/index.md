---
code: CV3
level: Value
status: Planned
status_reason: criada na renumeração de 2026-10-28 com a antiga CV2.DS2; depende da CV2
updated: 2026-10-28
related:
  - ../cv2-minha-estante-do-meu-jeito/index.md
  - ../../decisions/records/2026-10-26T1830Z-publicacao-no-github-pages.md
---

[< Roadmap](../index.md)

# CV3 — A Estante Visitável

**Status:** Planned

---

## Intent

**Capacidade:** a estante que a pessoa ajustou chega a quem ela quiser por um
link, e as estantes do grupo se encontram num só lugar.

O arquivo HTML é temporário, para a validação entre os fundadores; quando o
produto sair do grupo, a estante será compartilhada por URL
([acesso do grupo](../../decisions/records/2026-10-24T2013Z-acesso-do-grupo.md)).
Publicar é sempre um gesto explícito da pessoa.

Até 2026-10-28 era a CV2.DS2, dentro de "A Estante Cuidada e Visitável".

## Delivery Arc

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV3.DS1](cv3-ds1-estante-visitavel/index.md) | Estante visitável | A pessoa publica a estante num link e as estantes do grupo se encontram num só lugar |

## Scope

Publicar lê o `shelf.yaml` da CV2 e o mesmo núcleo que desenha a página. Testes
do layout no navegador entram quando a estante for servida por URL.

Depende da decisão aberta sobre
[onde publicar no GitHub Pages](../../decisions/records/2026-10-26T1830Z-publicacao-no-github-pages.md).

## Acceptance / Done Condition

A definir quando a CV3 for puxada.
