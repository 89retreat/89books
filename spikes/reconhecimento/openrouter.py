"""Extração de livros de uma imagem por um modelo de visão via OpenRouter."""

import base64
import json
import os
import time
from pathlib import Path

import httpx

URL = "https://openrouter.ai/api/v1/chat/completions"
ENV_MIRROR = Path.home() / "mirror" / ".env"


def carregar_chave() -> str:
    """Lê OPENROUTER_API_KEY do ambiente ou, se ausente, só essa linha do .env do Mirror."""
    chave = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if chave:
        return chave
    if ENV_MIRROR.exists():
        for linha in ENV_MIRROR.read_text(encoding="utf-8").splitlines():
            if linha.strip().startswith("OPENROUTER_API_KEY="):
                return linha.split("=", 1)[1].strip().strip("'\"")
    raise SystemExit("OPENROUTER_API_KEY não encontrada no ambiente nem em ~/mirror/.env")


def interpretar_resposta(texto: str) -> list[dict]:
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio == -1 or fim == -1:
        return []
    dados = json.loads(texto[inicio : fim + 1])
    livros = dados.get("livros", []) if isinstance(dados, dict) else dados
    return [
        livro
        for livro in livros
        if isinstance(livro, dict) and isinstance(livro.get("titulo"), str) and livro["titulo"].strip()
    ]


def extrair(imagem: Path, modelo: str, prompt: str, chave: str) -> dict:
    conteudo = base64.b64encode(imagem.read_bytes()).decode()
    corpo = {
        "model": modelo,
        "temperature": 0,
        "max_tokens": 8000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{conteudo}"}},
                ],
            }
        ],
        # Só provedores que não guardam os dados para treino.
        "provider": {"data_collection": "deny"},
        "usage": {"include": True},
    }
    cabecalhos = {
        "Authorization": f"Bearer {chave}",
        "HTTP-Referer": "https://github.com/89retreat/89books",
        "X-Title": "89books recognition spike",
    }
    inicio = time.monotonic()
    resposta = httpx.post(URL, json=corpo, headers=cabecalhos, timeout=300)
    segundos = time.monotonic() - inicio
    resposta.raise_for_status()
    dados = resposta.json()
    texto = dados["choices"][0]["message"].get("content") or ""
    uso = dados.get("usage", {})
    try:
        itens = interpretar_resposta(texto)
        erro = None
    except json.JSONDecodeError as exc:
        itens, erro = [], f"JSON inválido: {exc}"
    return {
        "itens": itens,
        "erro": erro,
        "texto": texto,
        "segundos": segundos,
        "custo": float(uso.get("cost") or 0.0),
        "tokens_entrada": uso.get("prompt_tokens"),
        "tokens_saida": uso.get("completion_tokens"),
        "provedor": dados.get("provider"),
        "fim": dados["choices"][0].get("finish_reason"),
    }
