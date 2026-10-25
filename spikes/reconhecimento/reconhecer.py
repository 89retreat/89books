"""Roda o pipeline do spike: extrair → normalizar → deduplicar → comparar.

Uso:
  uv run python reconhecer.py --modelo anthropic/claude-sonnet-5.5
  uv run python reconhecer.py --modelo anthropic/claude-haiku-5.5 --amostra kindle --imagens 01
"""

import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from metricas import calcular, deduplicar
from openlibrary import OpenLibrary
from openrouter import carregar_chave, extrair
from prompts import PROMPTS

RAIZ = Path(__file__).parent
AMOSTRAS = RAIZ / "amostras"
RESULTADOS = RAIZ / "resultados"
GASTOS = RESULTADOS / "gastos.json"
TETO_USD = 3.0

# Fotos gerais da estante servem como capa, não para reconhecer livros.
AMOSTRA = {
    "kindle": {"padrao": "kindle-*.jpeg", "excluir": set()},
    "estante": {"padrao": "estante-*-foto-*.jpeg", "excluir": {"07", "08"}},
}


def _id_imagem(caminho: Path) -> str:
    return re.search(r"-(\d{2})-", caminho.name).group(1)


def _gasto_total() -> float:
    return json.loads(GASTOS.read_text())["total"] if GASTOS.exists() else 0.0


def _registrar_gasto(valor: float) -> float:
    total = _gasto_total() + valor
    GASTOS.parent.mkdir(parents=True, exist_ok=True)
    GASTOS.write_text(json.dumps({"total": total}))
    return total


def rodar_amostra(nome: str, modelo: str, versao: str, filtro: set[str], chave: str, ol: OpenLibrary) -> dict:
    config = AMOSTRA[nome]
    pasta = AMOSTRAS / nome
    imagens = [
        img
        for img in sorted(pasta.glob(config["padrao"]))
        if _id_imagem(img) not in config["excluir"] and (not filtro or _id_imagem(img) in filtro)
    ]
    ids = {_id_imagem(img) for img in imagens}
    gabarito = [
        g for g in json.loads((pasta / "gabarito.json").read_text(encoding="utf-8")) if set(g["imagens"]) & ids
    ]

    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    saida = RESULTADOS / modelo.replace("/", "_") / f"{carimbo}-{nome}-{versao}"
    (saida / "bruto").mkdir(parents=True, exist_ok=True)

    todos, por_imagem = [], []
    for img in imagens:
        if _gasto_total() >= TETO_USD:
            raise SystemExit(f"Teto de US$ {TETO_USD} atingido; parando.")
        id_img = _id_imagem(img)
        resultado = extrair(img, modelo, PROMPTS[versao], chave)
        total = _registrar_gasto(resultado["custo"])
        (saida / "bruto" / f"{id_img}.json").write_text(
            json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        inicio_ol = time.monotonic()
        for item in resultado["itens"]:
            achado = ol.buscar(item["titulo"], item.get("autores") or [])
            todos.append(
                {
                    "titulo": item["titulo"],
                    "autores": item.get("autores") or [],
                    "status": item.get("status"),
                    "confianca_modelo": item.get("confianca"),
                    "imagem": id_img,
                    "obra": achado["obra"] if achado else None,
                    "capa": bool(achado and achado["capa"]),
                    "titulo_ol": achado["titulo_ol"] if achado else None,
                }
            )
        ol.salvar()
        segundos_ol = time.monotonic() - inicio_ol
        por_imagem.append(
            {
                "imagem": id_img,
                "itens": len(resultado["itens"]),
                "custo": resultado["custo"],
                "segundos_modelo": round(resultado["segundos"], 1),
                "segundos_openlibrary": round(segundos_ol, 1),
                "tokens_entrada": resultado["tokens_entrada"],
                "tokens_saida": resultado["tokens_saida"],
                "provedor": resultado["provedor"],
                "fim": resultado["fim"],
                "erro": resultado["erro"],
            }
        )
        print(
            f"  {nome} {id_img}: {len(resultado['itens'])} itens · US$ {resultado['custo']:.4f} · "
            f"{resultado['segundos']:.0f}s modelo + {segundos_ol:.0f}s OL · gasto total US$ {total:.3f}"
        )

    unicos, removidos = deduplicar(todos)
    m = calcular(unicos, gabarito)
    resumo = {
        "modelo": modelo,
        "amostra": nome,
        "prompt": versao,
        "carimbo": carimbo,
        "imagens": len(imagens),
        "itens_brutos": len(todos),
        "duplicados_removidos": removidos,
        **{k: v for k, v in m.items() if k not in ("faltantes", "extras")},
        "custo_total": sum(p["custo"] for p in por_imagem),
        "custo_por_imagem": sum(p["custo"] for p in por_imagem) / len(imagens),
        "segundos_por_imagem": sum(p["segundos_modelo"] + p["segundos_openlibrary"] for p in por_imagem)
        / len(imagens),
        "segundos_modelo_por_imagem": sum(p["segundos_modelo"] for p in por_imagem) / len(imagens),
        "por_imagem": por_imagem,
    }
    (saida / "itens.json").write_text(json.dumps(unicos, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "comparacao.json").write_text(
        json.dumps({"faltantes": m["faltantes"], "extras": m["extras"]}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    (saida / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(
        f"  → {nome}: cobertura {m['cobertura']:.0%} ({m['encontrados_firmes']}/{m['gabarito_firmes']}) · "
        f"fora do gabarito {m['fora_do_gabarito']}/{m['devolvidos']} · obra {m['com_obra']} · "
        f"capa {m['com_capa']} · duplicados {removidos} · {saida.relative_to(RAIZ)}"
    )
    return resumo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modelo", required=True)
    parser.add_argument("--amostra", choices=["kindle", "estante", "todas"], default="todas")
    parser.add_argument("--imagens", nargs="*", default=[])
    parser.add_argument("--prompt", default="v1", choices=sorted(PROMPTS))
    args = parser.parse_args()

    chave = carregar_chave()
    ol = OpenLibrary(RESULTADOS / "cache-openlibrary.json")
    nomes = ["kindle", "estante"] if args.amostra == "todas" else [args.amostra]
    print(f"{args.modelo} · prompt {args.prompt} · gasto acumulado US$ {_gasto_total():.3f}")
    for nome in nomes:
        rodar_amostra(nome, args.modelo, args.prompt, set(args.imagens), chave, ol)


if __name__ == "__main__":
    main()
