#!/usr/bin/env python3
"""
Compara métricas locais (JSON do treino) com ordens de grandeza citadas para Delfos.

Referência principal: Lim & Jung, Chem. Sci. 2019 (DOI 10.1039/C9SC02452B).
No artigo, o modelo atinge erros no conjunto de teste MNSOL da ordem de ~1 kcal/mol
(MAE) ou melhor, dependendo do split; use este script como lembrete qualitativo, não
como replicação exata do split do artigo.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Faixas de referência qualitativas (kcal/mol) — conferir Tabela 2 / texto no PMC.
DELFOS_PMC = "https://pmc.ncbi.nlm.nih.gov/articles/PMC7017869/"
REF = {
    "paper": "Lim & Jung, Chem. Sci. 2019",
    "doi": "10.1039/C9SC02452B",
    "pmc": DELFOS_PMC,
    "typical_test_mae_kcal_mol": (0.4, 1.1),
    "typical_test_rmse_kcal_mol": (0.5, 1.2),
}


def main() -> None:
    p = argparse.ArgumentParser(description="Compare training metrics to Delfos-scale literature.")
    p.add_argument(
        "metrics_json",
        type=Path,
        nargs="?",
        default=ROOT / "models" / "metrics.json",
        help="Path to metrics JSON from run_train.py",
    )
    args = p.parse_args()

    if not args.metrics_json.is_file():
        print(f"Arquivo não encontrado: {args.metrics_json}", file=sys.stderr)
        print("Treine antes: python scripts/run_train.py ... --metrics models/metrics.json", file=sys.stderr)
        sys.exit(1)

    m = json.loads(args.metrics_json.read_text(encoding="utf-8"))
    mae = m.get("mae_kcal_mol")
    rmse = m.get("rmse_kcal_mol")

    lo_mae, hi_mae = REF["typical_test_mae_kcal_mol"]
    lo_rmse, hi_rmse = REF["typical_test_rmse_kcal_mol"]

    def _in_range(x, lo, hi) -> str:
        if x is None:
            return "n/d"
        return "dentro" if lo <= x <= hi else "fora (datasets pequenos ou splits diferentes do artigo)"

    print("=== SolvScreen vs referência Delfos (ordem de grandeza) ===\n")
    print(f"Referência: {REF['paper']}")
    print(f"DOI: {REF['doi']}")
    print(f"PMC: {REF['pmc']}\n")
    print(f"  MAE  (seu modelo):  {mae} kcal/mol")
    print(f"  Faixa tipica Delfos MAE: ~{lo_mae}-{hi_mae} kcal/mol -> {_in_range(mae, lo_mae, hi_mae)}")
    print(f"  RMSE (seu modelo):  {rmse} kcal/mol")
    print(f"  Faixa tipica Delfos RMSE: ~{lo_rmse}-{hi_rmse} kcal/mol -> {_in_range(rmse, lo_rmse, hi_rmse)}")
    print(
        "\nNota: o baseline deste repositório (MLP+Morgan) não é o Delfos; "
        "valores no fixture de 5 linhas não são comparáveis estatisticamente. "
        "Use MNSOL completo e splits por cluster para comparação séria."
    )


if __name__ == "__main__":
    main()
