"""Deduplicação, casamento com o gabarito e métricas do spike."""

from texto import LIMIAR, similaridade, sobrenomes

NAO_IDENTIFICADO = "não identificado"
INCERTO = "incerto"


def deduplicar(itens):
    """Remove repetições entre imagens da mesma pessoa.

    Dois itens são o mesmo livro quando os títulos são equivalentes, ou quando
    apontam para a mesma obra da Open Library com títulos próximos. Exigir
    títulos próximos evita fundir volumes que a Open Library junta numa obra só.
    """
    unicos = []
    for item in itens:
        repetido = False
        for visto in unicos:
            sim = similaridade(item["titulo"], visto["titulo"])
            mesma_obra = item.get("obra") and item.get("obra") == visto.get("obra")
            if sim >= LIMIAR or (mesma_obra and sim >= 0.6):
                repetido = True
                break
        if not repetido:
            unicos.append(item)
    return unicos, len(itens) - len(unicos)


def casar(previstos, gabarito):
    """Casamento um para um, do par mais parecido para o menos parecido."""
    candidatos = []
    for i, previsto in enumerate(previstos):
        for j, esperado in enumerate(gabarito):
            if esperado.get("confianca") == NAO_IDENTIFICADO:
                continue
            sim = similaridade(previsto["titulo"], esperado["titulo"])
            if sim < LIMIAR:
                continue
            if sobrenomes(previsto.get("autores")) & sobrenomes(esperado.get("autores")):
                sim += 0.05
            candidatos.append((sim, i, j))
    candidatos.sort(key=lambda c: c[0], reverse=True)
    usados_p, usados_g, pares = set(), set(), []
    for _, i, j in candidatos:
        if i in usados_p or j in usados_g:
            continue
        usados_p.add(i)
        usados_g.add(j)
        pares.append((previstos[i], gabarito[j]))
    return pares


def calcular(previstos, gabarito):
    firmes = [g for g in gabarito if g.get("confianca") not in (INCERTO, NAO_IDENTIFICADO)]
    incertos = [g for g in gabarito if g.get("confianca") == INCERTO]
    pares = casar(previstos, gabarito)
    casados_g = {id(g) for _, g in pares}
    casados_p = {id(p) for p, _ in pares}
    encontrados_firmes = sum(1 for g in firmes if id(g) in casados_g)
    encontrados_incertos = sum(1 for g in incertos if id(g) in casados_g)
    extras = [p for p in previstos if id(p) not in casados_p]
    return {
        "gabarito_firmes": len(firmes),
        "gabarito_incertos": len(incertos),
        "encontrados_firmes": encontrados_firmes,
        "encontrados_incertos": encontrados_incertos,
        "cobertura": encontrados_firmes / len(firmes) if firmes else 0.0,
        "devolvidos": len(previstos),
        "fora_do_gabarito": len(extras),
        "com_obra": sum(1 for p in previstos if p.get("obra")),
        "com_capa": sum(1 for p in previstos if p.get("capa")),
        "faltantes": [g for g in firmes if id(g) not in casados_g],
        "extras": extras,
    }
