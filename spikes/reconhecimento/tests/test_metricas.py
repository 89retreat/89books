from metricas import calcular, casar, deduplicar


def livro(titulo, autores=(), confianca="visível", obra=None, imagem="01", capa=False):
    return {
        "titulo": titulo,
        "autores": list(autores),
        "confianca": confianca,
        "obra": obra,
        "capa": capa,
        "imagem": imagem,
    }


def test_deduplicar_pela_obra_da_open_library():
    itens = [
        livro("The Advantage", obra="/works/OL1W", imagem="01"),
        livro("The Advantage: Why Organizational Health", obra="/works/OL1W", imagem="02"),
        livro("Coisa de Rico", obra="/works/OL2W", imagem="02"),
    ]
    unicos, removidos = deduplicar(itens)
    assert [i["titulo"] for i in unicos] == ["The Advantage", "Coisa de Rico"]
    assert removidos == 1


def test_deduplicar_sem_obra_usa_titulo_normalizado():
    itens = [
        livro("A Sociedade em Rede", ["Manuel Castells"], imagem="02"),
        livro("A sociedade em rede", ["Castells"], imagem="06"),
    ]
    unicos, removidos = deduplicar(itens)
    assert len(unicos) == 1 and removidos == 1


def test_deduplicar_preserva_volumes_diferentes():
    itens = [livro("Mil Platôs, vol. 1"), livro("Mil Platôs, vol. 2")]
    unicos, removidos = deduplicar(itens)
    assert len(unicos) == 2 and removidos == 0


def test_casar_um_para_um_com_desempate_pelo_autor():
    gabarito = [
        livro("Kanban", ["David J. Anderson"]),
        livro("Kanban from the Inside", ["Mike Burrows"]),
    ]
    previstos = [livro("Kanban from the Inside", ["Mike Burrows"]), livro("Kanban", ["David Anderson"])]
    pares = casar(previstos, gabarito)
    assert {(p["titulo"], g["titulo"]) for p, g in pares} == {
        ("Kanban from the Inside", "Kanban from the Inside"),
        ("Kanban", "Kanban"),
    }


def test_casar_ignora_itens_nao_identificados_do_gabarito():
    gabarito = [livro("?", confianca="não identificado")]
    assert casar([livro("Qualquer Livro")], gabarito) == []


def test_calcular_metricas():
    gabarito = [
        livro("Joy, Inc.", ["Richard Sheridan"]),
        livro("Powerful", ["Patty McCord"]),
        livro("Funk sem Cortes", confianca="incerto"),
        livro("?", confianca="não identificado"),
    ]
    previstos = [
        livro("Joy, Inc.", ["Richard Sheridan"], obra="/works/A", capa=True),
        livro("Funk sem Cortes", obra="/works/B"),
        livro("Livro Inventado"),
    ]
    m = calcular(previstos, gabarito)
    assert m["gabarito_firmes"] == 2
    assert m["gabarito_incertos"] == 1
    assert m["encontrados_firmes"] == 1
    assert m["encontrados_incertos"] == 1
    assert m["cobertura"] == 0.5
    assert m["devolvidos"] == 3
    assert m["fora_do_gabarito"] == 1
    assert m["com_obra"] == 2
    assert m["com_capa"] == 1
    assert [i["titulo"] for i in m["faltantes"]] == ["Powerful"]
    assert [i["titulo"] for i in m["extras"]] == ["Livro Inventado"]
