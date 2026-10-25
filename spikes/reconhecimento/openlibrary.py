"""Normalização de livros na Open Library, ligando cada um à obra (work)."""

import json
import time
from pathlib import Path

import httpx

from texto import normalizar_titulo, similaridade, sobrenomes, titulo_para_busca

URL = "https://openlibrary.org/search.json"
CAMPOS = "key,title,author_name,cover_i,first_publish_year"
AGENTE = "89books-spike/0.1 (+https://github.com/89retreat/89books)"
INTERVALO = 0.4  # a Open Library pede no máximo ~3 requisições por segundo


class OpenLibrary:
    def __init__(self, cache: Path):
        self.cache_path = cache
        self.cache = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
        self.cliente = httpx.Client(headers={"User-Agent": AGENTE}, timeout=30)
        self._ultima = 0.0

    def salvar(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.cache, ensure_ascii=False, indent=1), encoding="utf-8")

    def _get(self, params: dict) -> list[dict]:
        espera = INTERVALO - (time.monotonic() - self._ultima)
        if espera > 0:
            time.sleep(espera)
        for tentativa in range(3):
            try:
                resposta = self.cliente.get(URL, params={**params, "fields": CAMPOS, "limit": 5})
                self._ultima = time.monotonic()
                if resposta.status_code == 200:
                    return resposta.json().get("docs", [])
            except httpx.HTTPError:
                pass
            time.sleep(2 * (tentativa + 1))
        return []

    def buscar(self, titulo: str, autores: list[str]) -> dict | None:
        chave = normalizar_titulo(titulo) + "|" + ",".join(sorted(sobrenomes(autores)))
        if chave in self.cache:
            return self.cache[chave]
        titulo_busca = titulo_para_busca(titulo)
        tentativas = []
        if autores:
            tentativas.append({"title": titulo_busca, "author": autores[0]})
        tentativas.append({"title": titulo_busca})
        tentativas.append({"q": titulo_busca})
        achado = None
        for params in tentativas:
            for doc in self._get(params):
                if similaridade(titulo, doc.get("title", "")) >= 0.6:
                    achado = {
                        "obra": doc.get("key"),
                        "titulo_ol": doc.get("title"),
                        "autores_ol": doc.get("author_name", [])[:3],
                        "capa": bool(doc.get("cover_i")),
                        "ano": doc.get("first_publish_year"),
                    }
                    break
            if achado:
                break
        self.cache[chave] = achado
        return achado
