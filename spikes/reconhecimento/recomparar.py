"""Recalcula comparação e métricas de rodadas já feitas, sem chamar o modelo.

Útil quando o casamento com o gabarito ou o próprio gabarito mudam.
Uso: uv run python recomparar.py
"""

import json
from pathlib import Path

from metricas import calcular

RAIZ = Path(__file__).parent


def recomparar(pasta: Path) -> None:
    resumo = json.loads((pasta / "resumo.json").read_text(encoding="utf-8"))
    itens = json.loads((pasta / "itens.json").read_text(encoding="utf-8"))
    ids = {p["imagem"] for p in resumo["por_imagem"]}
    gabarito_path = RAIZ / "amostras" / resumo["amostra"] / "gabarito.json"
    gabarito = [g for g in json.loads(gabarito_path.read_text(encoding="utf-8")) if set(g["imagens"]) & ids]
    m = calcular(itens, gabarito)
    resumo.update({k: v for k, v in m.items() if k not in ("faltantes", "extras")})
    (pasta / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    (pasta / "comparacao.json").write_text(
        json.dumps({"faltantes": m["faltantes"], "extras": m["extras"]}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print(f"{pasta.relative_to(RAIZ)}: cobertura {m['cobertura']:.0%} · fora do gabarito {m['fora_do_gabarito']}")


if __name__ == "__main__":
    for arquivo in sorted((RAIZ / "resultados").glob("*/*/resumo.json")):
        recomparar(arquivo.parent)
