from __future__ import annotations

import argparse
import json
from pathlib import Path

from .development import development_summary, run_development_matrix


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def write_development_artifacts(output_dir: Path) -> tuple[Path, Path]:
    """Run and retain the complete development-only CX01 matrix."""

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = run_development_matrix()
    records_path = output_dir / "development_records.jsonl"
    summary_path = output_dir / "development_summary.json"
    with records_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(_canonical(row.state_dict()))
            handle.write("\n")
    summary_path.write_text(
        json.dumps(development_summary(rows), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return records_path, summary_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    write_development_artifacts(args.output_dir)


if __name__ == "__main__":
    main()
