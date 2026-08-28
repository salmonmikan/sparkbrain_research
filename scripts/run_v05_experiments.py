from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v05 import render_v05_report, run_v05_reference_experiments, write_v05_html


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/v05/reference_results.json"))
    parser.add_argument("--html", type=Path, default=Path("artifacts/v05/assembly_visualizer.html"))
    parser.add_argument("--seeds", default="")
    parser.add_argument("--report", type=Path, default=Path("artifacts/v05/reference_report.md"))
    args = parser.parse_args()
    seeds = tuple(int(item) for item in args.seeds.split(",") if item.strip())
    payload = run_v05_reference_experiments(seeds=seeds or None)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical_json(payload) + "\n", encoding="utf-8")
    write_v05_html(args.html, payload)
    args.report.write_text(render_v05_report(payload) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "completion": payload["completion"],
                "gates": payload["gates"],
                "output": str(args.output),
                "report": str(args.report),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
