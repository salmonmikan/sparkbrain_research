from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v05 import render_v05_report, write_v05_html
from sparkbrain.v05.evaluation import (
    V05ProtocolConfig,
    _compact_seed_result,
    aggregate_v05_results,
)


def load_rows(directory: Path, seeds: tuple[int, ...]) -> list[dict]:
    rows = []
    for seed in seeds:
        path = directory / f"seed_{seed}.json"
        if not path.is_file():
            raise FileNotFoundError(path)
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("artifacts/v05"))
    args = parser.parse_args()
    cfg = V05ProtocolConfig()
    development = [
        _compact_seed_result(row)
        for row in load_rows(args.root / "development_seeds", cfg.development_seeds)
    ]
    confirmatory = [
        _compact_seed_result(row)
        for row in load_rows(args.root / "retained_seeds", cfg.confirmatory_seeds)
    ]
    ablations = load_rows(args.root / "plasticity_ablations", cfg.ablation_seeds)
    payload = aggregate_v05_results(
        protocol=cfg,
        development_results=development,
        confirmatory_results=confirmatory,
        ablation_rows=ablations,
    )
    output = args.root / "reference_results.json"
    report = args.root / "reference_report.md"
    html = args.root / "assembly_visualizer.html"
    output.write_text(canonical_json(payload) + "\n", encoding="utf-8")
    report.write_text(render_v05_report(payload) + "\n", encoding="utf-8")
    write_v05_html(html, payload)
    print(json.dumps({"completion": payload["completion"], "gates": payload["gates"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
