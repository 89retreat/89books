"""Mostra a última rodada de cada modelo e amostra em tabela Markdown.

Uso: uv run python resumir.py [--prompt v1]
"""

import argparse
import json
from pathlib import Path

RESULTADOS = Path(__file__).parent / "resultados"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default=None)
    args = parser.parse_args()
    ultimos = {}
    for arquivo in sorted(RESULTADOS.glob("*/*/resumo.json")):
        r = json.loads(arquivo.read_text(encoding="utf-8"))
        if args.prompt and r["prompt"] != args.prompt:
            continue
        ultimos[(r["amostra"], r["modelo"])] = r
    print(
        "| Amostra | Modelo | Imagens | Cobertura | Incertos achados | Fora do gabarito | "
        "Com obra na OL | Com capa | Duplicados removidos | US$/imagem | s/imagem |"
    )
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for (amostra, modelo), r in sorted(ultimos.items()):
        dev = r["devolvidos"] or 1
        print(
            f"| {amostra} | {modelo.split('/')[-1]} | {r['imagens']} | "
            f"{r['cobertura']:.0%} ({r['encontrados_firmes']}/{r['gabarito_firmes']}) | "
            f"{r['encontrados_incertos']}/{r['gabarito_incertos']} | "
            f"{r['fora_do_gabarito']}/{r['devolvidos']} ({r['fora_do_gabarito'] / dev:.0%}) | "
            f"{r['com_obra'] / dev:.0%} | {r['com_capa'] / max(r['com_obra'], 1):.0%} | "
            f"{r['duplicados_removidos']} | {r['custo_por_imagem']:.4f} | {r['segundos_por_imagem']:.0f} |"
        )


if __name__ == "__main__":
    main()
