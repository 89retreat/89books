from texto import normalizar_titulo, similaridade, sobrenomes


def test_normalizar_remove_acentos_caixa_e_pontuacao():
    assert normalizar_titulo("O que é Estratégia?") == "o que e estrategia"


def test_normalizar_remove_subtitulo_e_parenteses():
    assert normalizar_titulo("How to Read the Room: The Art and Science") == "how to read the room"
    assert normalizar_titulo("Estudo de Caso (5ª ed.)") == "estudo de caso"


def test_normalizar_remove_marcas_de_edicao():
    assert normalizar_titulo("Team Topologies, 2nd Edition") == "team topologies"
    assert normalizar_titulo("Team Topologies, 2nd Editio…") == "team topologies"


def test_normalizar_preserva_volume():
    assert normalizar_titulo("Mil Platôs, vol. 3") == "mil platos vol 3"


def test_similaridade_identica_e_truncada():
    assert similaridade("Joy, Inc.", "Joy Inc") == 1.0
    assert similaridade("Making Work Visible", "Making Work Visible: Exposing Time Theft") == 1.0
    assert similaridade("Holacracy", "Holacracy: The New Management System") == 1.0


def test_similaridade_titulos_diferentes_fica_baixa():
    assert similaridade("Mil Platôs, vol. 1", "Mil Platôs, vol. 2") < 0.82
    assert similaridade("A Elite do Atraso", "A Tolice da Inteligência Brasileira") < 0.5


def test_trecho_curto_contido_nao_conta_como_igual():
    assert similaridade("Scrum", "Essential Scrum") < 1.0


def test_sobrenomes():
    assert sobrenomes(["Matthew Skelton", "Manuel Pais"]) == {"skelton", "pais"}
    assert sobrenomes(["bell hooks"]) == {"hooks"}
    assert sobrenomes([]) == set()


def test_titulo_para_busca_mantem_acentos_e_tira_edicao_subtitulo_e_reticencias():
    from texto import titulo_para_busca

    assert titulo_para_busca("Team Topologies, 2nd Edition") == "Team Topologies"
    assert titulo_para_busca("Estudo de Caso (5ª ed.)") == "Estudo de Caso"
    assert titulo_para_busca("Coisa de Rico: A Vida dos Endinheirados") == "Coisa de Rico"
    assert titulo_para_busca("Making Work Visible: Exposi…") == "Making Work Visible"
    assert titulo_para_busca("O que é Estratégia?") == "O que é Estratégia?"


def test_similaridade_considera_a_parte_depois_dos_dois_pontos():
    assert similaridade("Mário Schenberg: Pensando a Arte", "Pensando a Arte") >= 0.82


def test_similaridade_aceita_leitura_parcial_longa_no_fim_do_titulo():
    assert similaridade("Algoritmos", "Entendendo Algoritmos") >= 0.82
    assert similaridade("Kanban", "Practical Kanban") < 0.82
