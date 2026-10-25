"""Normalização e comparação de títulos e autores."""

import re
import unicodedata
from difflib import SequenceMatcher

LIMIAR = 0.82

_EDICAO = re.compile(r"\b\d+\s*(?:a|o|st|nd|rd|th)?\s*(?:ed|edicao|edition|editio)\w*\b")
_IGNORAR_NOMES = {"et", "al", "org", "friends", "jr", "junior", "filho", "neto"}


def _sem_acentos(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def _normalizar(texto: str) -> str:
    t = _EDICAO.sub(" ", texto)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def _preparar(titulo: str) -> str:
    t = _sem_acentos(titulo or "").lower()
    t = t.replace("…", " ").replace("...", " ")
    return re.sub(r"\([^)]*\)", " ", t)


def normalizar_titulo(titulo: str) -> str:
    t = _preparar(titulo)
    principal = t.split(":", 1)[0]
    return _normalizar(principal if principal.strip() else t)


def _variantes(titulo: str) -> set[str]:
    """Título sem subtítulo, título inteiro e a parte depois dos dois-pontos."""
    t = _preparar(titulo)
    partes = {normalizar_titulo(titulo), _normalizar(t)}
    if ":" in t:
        partes.add(_normalizar(t.split(":", 1)[1]))
    return {p for p in partes if p}


_EDICAO_ORIGINAL = re.compile(
    r"[,\s]*\b\d+\s*(?:ª|º|a|o|st|nd|rd|th)?\s*(?:ed|edição|edicao|edition|editio)\w*\.?", re.IGNORECASE
)


def titulo_para_busca(titulo: str) -> str:
    """Título limpo para consultar a Open Library, preservando acentos e caixa."""
    t = re.sub(r"\([^)]*\)", " ", titulo or "")
    t = t.replace("…", " ").replace("...", " ")
    principal = t.split(":", 1)[0]
    t = principal if principal.strip() else t
    t = _EDICAO_ORIGINAL.sub(" ", t)
    return " ".join(t.split()).strip(" ,;-")


def _comparar(na: str, nb: str) -> float:
    if na == nb:
        return 1.0
    curto, longo = sorted((na, nb), key=len)
    if len(curto) >= 8 and longo.startswith(curto + " "):
        return 0.95
    if len(curto) >= 10 and longo.endswith(" " + curto):
        return 0.9
    razao = SequenceMatcher(None, na, nb).ratio()
    numeros_a, numeros_b = set(re.findall(r"\d+", na)), set(re.findall(r"\d+", nb))
    if numeros_a and numeros_b and numeros_a != numeros_b:
        return min(razao, 0.5)
    return razao


def similaridade(a: str, b: str) -> float:
    va, vb = _variantes(a), _variantes(b)
    if not va or not vb:
        return 0.0
    return max(_comparar(x, y) for x in va for y in vb)


def sobrenomes(autores) -> set[str]:
    resultado = set()
    for autor in autores or []:
        partes = [p for p in re.split(r"[^a-z]+", _sem_acentos(autor).lower()) if p]
        partes = [p for p in partes if p not in _IGNORAR_NOMES]
        if partes:
            resultado.add(partes[-1])
    return resultado
