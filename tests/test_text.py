from shelf.text import THRESHOLD, normalize_title, search_title, similarity


def test_normalize_title_drops_accents_subtitle_and_edition():
    assert normalize_title("Pensando em Sistemas: um guia (2ª edição)") == "pensando em sistemas"


def test_search_title_keeps_accents_and_case():
    assert search_title("Tornar-se Negro (Coleção X): as vicissitudes") == "Tornar-se Negro"


def test_similarity_accepts_partial_reads_and_rejects_different_numbers():
    assert similarity("Algoritmos", "Entendendo Algoritmos") >= THRESHOLD
    assert similarity("Accelerate 2", "Accelerate 3") < THRESHOLD
