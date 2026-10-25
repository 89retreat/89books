from gabarito import ler_linhas
from openrouter import interpretar_resposta

RASCUNHO = """
| # | Foto | Título | Autor(es) | Confiança | Notas |
|---|------|--------|-----------|-----------|-------|
| 1 | 01 | Quarto de Despejo | Carolina Maria de Jesus | visível | |
| 10 | 01, 02 | The Advantage | Patrick Lencioni | visível | cortado |
| 13 | 01 | Maracanã | Luiz Antonio Simas (?) | parcial | |
| 16 | 02 | MyPrism | Maribel Aleman, Douglas Choo et al. | visível | |
| 31 | 03 | ? | ? | não identificado | |
| 59 | 03 | Goya | — | parcial | coleção |
| 40 | 02 | Manual de Filosofia Política | Flamarion Caldeira Ramos et al. | visível | |
| 43 | 02 | Cynefin | Dave Snowden & Friends | visível | |
"""


def test_ler_linhas_do_rascunho():
    livros = ler_linhas(RASCUNHO)
    assert len(livros) == 8
    assert livros[0] == {
        "titulo": "Quarto de Despejo",
        "autores": ["Carolina Maria de Jesus"],
        "confianca": "visível",
        "imagens": ["01"],
    }
    assert livros[1]["imagens"] == ["01", "02"]
    assert livros[2]["autores"] == ["Luiz Antonio Simas"]
    assert livros[3]["autores"] == ["Maribel Aleman", "Douglas Choo"]
    assert livros[4]["confianca"] == "não identificado"
    assert livros[5]["autores"] == []
    assert livros[7]["autores"] == ["Dave Snowden"]


def test_ignora_tabelas_sem_coluna_de_titulo():
    texto = "| Foto | O que mostra |\n|---|---|\n| 01 | Prateleira |\n"
    assert ler_linhas(texto) == []


def test_interpretar_resposta_json_puro():
    texto = '{"livros": [{"titulo": "Joy, Inc.", "autores": ["Richard Sheridan"], "status": "lido"}]}'
    assert interpretar_resposta(texto)[0]["titulo"] == "Joy, Inc."


def test_interpretar_resposta_com_cerca_de_codigo_e_texto_em_volta():
    texto = 'Aqui está:\n```json\n{"livros": [{"titulo": "Powerful", "autores": []}]}\n```\nfim'
    assert interpretar_resposta(texto) == [{"titulo": "Powerful", "autores": []}]


def test_interpretar_resposta_descarta_itens_sem_titulo():
    texto = '{"livros": [{"titulo": ""}, {"autores": ["X"]}, {"titulo": "Ok"}]}'
    assert [i["titulo"] for i in interpretar_resposta(texto)] == ["Ok"]
