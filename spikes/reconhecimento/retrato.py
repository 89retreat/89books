"""Gera o "retrato de si" a partir dos livros já extraídos de uma estante.

Experimento da ES "O Telegram como Porta da Estante": testar à mão, antes do
MVP, se o retrato faz a pessoa se reconhecer. Depois do teste com o Lula
(2026-10-26), a pergunta final saiu: ele se reconheceu, mas a pergunta não
ajudou. Usa os itens da última rodada
do modelo de visão, com os erros de leitura incluídos, como o produto faria.
O retrato é pessoal e fica em resultados/retratos/, fora do git.

Uso: uv run python retrato.py --amostra estante [--modelo anthropic/claude-sonnet-5.5]
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

from openrouter import URL, carregar_chave
from reconhecer import TETO_USD, _gasto_total, _registrar_gasto

RAIZ = Path(__file__).parent

PROMPT = """Você recebe a lista de livros de uma estante pessoal, reconhecidos automaticamente a partir de fotos. Pode haver erros de leitura e itens que não são livros; ignore o que não fizer sentido.

Escreva um retrato curto, em português do Brasil, dirigido à própria pessoa ("você"), com exatamente duas partes:

**A lente**: uma frase sobre o modo de olhar o mundo que esta estante revela.
**Temas que se repetem**: de três a cinco temas, cada um com dois ou três livros da lista como exemplo.

Tom: observação atenta e generosa, de quem gosta de livros e de gente. Nada de elogio, julgamento, diagnóstico de personalidade ou frases genéricas que serviriam para qualquer leitor. Seja específico a esta estante. Não mencione que a lista veio de fotos nem os possíveis erros.

Livros:
{livros}"""


def montar_lista(itens: list[dict]) -> str:
    linhas: list[str] = []
    for item in itens:
        titulo = item.get("titulo_ol") or item["titulo"]
        autores = ", ".join(item.get("autores") or [])
        linha = f"- {titulo} — {autores}" if autores else f"- {titulo}"
        if linha not in linhas:
            linhas.append(linha)
    return "\n".join(linhas)


def gerar(lista: str, modelo: str, chave: str) -> dict:
    corpo = {
        "model": modelo,
        "temperature": 0.7,
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": PROMPT.format(livros=lista)}],
        # Só provedores que não guardam os dados para treino.
        "provider": {"data_collection": "deny"},
        "usage": {"include": True},
    }
    cabecalhos = {
        "Authorization": f"Bearer {chave}",
        "HTTP-Referer": "https://github.com/89retreat/89books",
        "X-Title": "89books portrait experiment",
    }
    inicio = time.monotonic()
    resposta = httpx.post(URL, json=corpo, headers=cabecalhos, timeout=300)
    resposta.raise_for_status()
    dados = resposta.json()
    return {
        "texto": dados["choices"][0]["message"].get("content") or "",
        "custo": float(dados.get("usage", {}).get("cost") or 0.0),
        "segundos": time.monotonic() - inicio,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--amostra", required=True, choices=["kindle", "estante"])
    p.add_argument("--modelo", default="anthropic/claude-sonnet-5.5")
    p.add_argument("--fonte", default="anthropic/claude-sonnet-5.5", help="modelo da rodada de extração")
    args = p.parse_args()

    if _gasto_total() >= TETO_USD:
        raise SystemExit(f"Teto de US$ {TETO_USD} atingido; parando.")
    rodada = sorted((RAIZ / "resultados" / args.fonte.replace("/", "_")).glob(f"*-{args.amostra}-*"))[-1]
    itens = json.loads((rodada / "itens.json").read_text(encoding="utf-8"))
    lista = montar_lista(itens)
    r = gerar(lista, args.modelo, carregar_chave())
    total = _registrar_gasto(r["custo"])

    pasta = RAIZ / "resultados" / "retratos"
    pasta.mkdir(parents=True, exist_ok=True)
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destino = pasta / f"{carimbo}-{args.amostra}.md"
    destino.write_text(
        f"<!-- fonte: {rodada.name} · {lista.count(chr(10)) + 1} livros · modelo: {args.modelo} -->\n\n{r['texto']}\n",
        encoding="utf-8",
    )
    print(f"{destino.relative_to(RAIZ)} · US$ {r['custo']:.4f} · {r['segundos']:.0f}s · gasto total US$ {total:.3f}")


if __name__ == "__main__":
    main()
