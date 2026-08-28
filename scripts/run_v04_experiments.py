from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v04 import IntegratedV04Brain, run_reference_experiments, write_trace_html
from sparkbrain.v04.worlds import noisy_motif_stream


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/v04"))
    args = parser.parse_args()
    output: Path = args.output
    output.mkdir(parents=True, exist_ok=True)

    results = run_reference_experiments()
    (output / "reference_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    brain = IntegratedV04Brain()
    brain.ingest_pulses(noisy_motif_stream(repeats=5), settle_ms=50.0)
    (output / "demo_trace.json").write_text(
        json.dumps(brain.trace, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_trace_html(output / "demo_visualizer.html", brain.trace)

    report = [
        "# SparkBrain v0.4 reference experiment report",
        "",
        (
            "> Engineering signal-dynamics results only. These experiments do not establish "
            "semantic understanding, biological equivalence, energy efficiency, concepts, "
            "organs, consciousness, or general intelligence."
        ),
        "",
    ]
    for row in results["experiments"]:
        report.extend(
            [
                f"## {row['name']}",
                "",
                "```json",
                json.dumps(row["metrics"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
            ]
        )
    (output / "report.md").write_text("\n".join(report).rstrip() + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "status": "pass"}, sort_keys=True))


if __name__ == "__main__":
    main()
