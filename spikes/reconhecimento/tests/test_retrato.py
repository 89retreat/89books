from retrato import montar_lista


def test_montar_lista_usa_titulo_da_open_library_e_autores():
    itens = [
        {"titulo": "Quarto de despejo", "titulo_ol": "Quarto de Despejo", "autores": ["Carolina Maria de Jesus"]},
        {"titulo": "Cynefin", "autores": []},
    ]
    assert montar_lista(itens) == "- Quarto de Despejo — Carolina Maria de Jesus\n- Cynefin"


def test_montar_lista_remove_repetidos():
    itens = [{"titulo": "Pensando em Sistemas", "autores": ["Donella Meadows"]}] * 2
    assert montar_lista(itens).count("Pensando em Sistemas") == 1
