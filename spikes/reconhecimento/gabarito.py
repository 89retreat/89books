"""Converte um rascunho de gabarito (Markdown) em gabarito.json.

Uso: uv run python gabarito.py amostras/kindle/gabarito-rascunho.md
"""

import json
import re
import sys
from pathlib import Path

_DESCARTAR_AUTOR = {"", "?", "—", "friends"}


def _autores(celula: str) -> list[str]:
    texto = re.sub(r"\((?:\?|org\.?)\)", " ", celula)
    texto = re.sub(r"\bet al\.?", " ", texto)
    nomes = []
    for parte in re.split(r"[,&]", texto):
        nome = " ".join(parte.split()).strip(" ?")
        if nome.lower() not in _DESCARTAR_AUTOR:
            nomes.append(nome)
    return nomes


def ler_linhas(texto: str) -> list[dict]:
    livros = []
    colunas = None
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha.startswith("|"):
            colunas = None
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if colunas is None:
            nomes = [c.lower() for c in celulas]
            colunas = {n: i for i, n in enumerate(nomes)} if "título" in nomes else {}
            continue
        if not colunas or set("".join(celulas)) <= set("-: "):
            continue
        imagem_col = colunas.get("foto", colunas.get("print"))
        titulo = re.sub(r"\s*\(\?\)\s*$", "", celulas[colunas["título"]])
        livros.append(
            {
                "titulo": titulo,
                "autores": _autores(celulas[colunas["autor(es)"]]),
                "confianca": celulas[colunas["confiança"]],
                "imagens": [i.strip() for i in celulas[imagem_col].split(",") if i.strip()],
            }
        )
    return livros


def main(caminho: str) -> None:
    origem = Path(caminho)
    livros = ler_linhas(origem.read_text(encoding="utf-8"))
    destino = origem.with_name("gabarito.json")
    destino.write_text(json.dumps(livros, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{destino}: {len(livros)} livros")


if __name__ == "__main__":
    main(sys.argv[1])
