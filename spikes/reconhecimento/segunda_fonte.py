"""Mede o Google Books como segunda fonte de metadados (CV1.DS1.TS2).

Reaproveita os itens da última rodada de cada amostra com o modelo indicado e
pergunta: quantos a Google Books acha, com capa, em especial entre os que a
Open Library não achou ou achou sem capa. Não chama o modelo de visão.

Exige a chave gratuita da Books API em GOOGLE_BOOKS_API_KEY: sem ela, a cota
anônima responde 429 já na primeira consulta (verificado em 2026-10-26).

Uso: uv run python segunda_fonte.py [--modelo anthropic/claude-sonnet-5.5]
"""

import argparse
import json
import os
import time
from pathlib import Path

import httpx

from texto import LIMIAR, similaridade, titulo_para_busca

RAIZ = Path(__file__).parent
CACHE = RAIZ / "resultados" / "cache-googlebooks.json"
URL = "https://www.googleapis.com/books/v1/volumes"


def buscar(cliente: httpx.Client, cache: dict, titulo: str, autores: list[str]) -> dict:
    chave = f"{titulo}|{autores[0] if autores else ''}"
    if chave not in cache:
        q = f'intitle:"{titulo_para_busca(titulo)}"'
        if autores:
            q += f' inauthor:"{autores[0].split()[-1]}"'
        for tentativa in range(4):
            params = {"q": q, "maxResults": 5}
            if os.environ.get("GOOGLE_BOOKS_API_KEY"):
                params["key"] = os.environ["GOOGLE_BOOKS_API_KEY"]
            r = cliente.get(URL, params=params)
            if r.status_code != 429:
                break
            time.sleep(2 ** tentativa)
        r.raise_for_status()
        cache[chave] = r.json().get("items", [])
        time.sleep(0.3)
    for item in cache[chave]:
        info = item.get("volumeInfo", {})
        if similaridade(titulo, info.get("title", "")) >= LIMIAR:
            return {"achou": True, "capa": "imageLinks" in info}
    return {"achou": False, "capa": False}


def medir(modelo: str) -> None:
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    pasta_modelo = RAIZ / "resultados" / modelo.replace("/", "_")
    with httpx.Client(timeout=20) as cliente:
        for amostra in ("kindle", "estante"):
            rodada = sorted(pasta_modelo.glob(f"*-{amostra}-*"))[-1]
            itens = json.loads((rodada / "itens.json").read_text(encoding="utf-8"))
            c = {"itens": len(itens), "ol_obra": 0, "ol_capa": 0, "gb_achou": 0, "gb_capa": 0,
                 "sem_ol_gb_achou": 0, "sem_ol": 0, "sem_capa_ol_gb_capa": 0, "sem_capa_ol": 0,
                 "alguma_capa": 0}
            for i in itens:
                gb = buscar(cliente, cache, i["titulo"], i.get("autores") or [])
                c["ol_obra"] += bool(i.get("obra"))
                c["ol_capa"] += bool(i.get("capa"))
                c["gb_achou"] += gb["achou"]
                c["gb_capa"] += gb["capa"]
                if not i.get("obra"):
                    c["sem_ol"] += 1
                    c["sem_ol_gb_achou"] += gb["achou"]
                if not i.get("capa"):
                    c["sem_capa_ol"] += 1
                    c["sem_capa_ol_gb_capa"] += gb["capa"]
                c["alguma_capa"] += bool(i.get("capa")) or gb["capa"]
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            n = c["itens"]
            print(f"\n{amostra} ({n} itens, {rodada.name})")
            print(f"  Open Library: obra {c['ol_obra']/n:.0%} · capa {c['ol_capa']/n:.0%}")
            print(f"  Google Books: achou {c['gb_achou']/n:.0%} · capa {c['gb_capa']/n:.0%}")
            print(f"  Sem obra na OL que a GB achou: {c['sem_ol_gb_achou']}/{c['sem_ol']}")
            print(f"  Sem capa na OL que a GB tem capa: {c['sem_capa_ol_gb_capa']}/{c['sem_capa_ol']}")
            print(f"  Com capa em alguma das duas: {c['alguma_capa']/n:.0%}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--modelo", default="anthropic/claude-sonnet-5.5")
    medir(p.parse_args().modelo)
