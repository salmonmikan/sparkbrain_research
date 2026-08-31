from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .development import (
    COMPARATOR_KINDS,
    DevelopmentExecution,
    development_summary,
    run_development_matrix,
)


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _training_transcript_audit(
    rows: tuple[DevelopmentExecution, ...],
) -> dict[str, Any]:
    grouped: dict[tuple[str, int], list[DevelopmentExecution]] = {}
    for row in rows:
        grouped.setdefault((row.family.value, row.seed), []).append(row)

    mismatches: list[str] = []
    incomplete: list[str] = []
    for (family, seed), selected in sorted(grouped.items()):
        key = f"{family}|{seed}"
        if len(selected) != len(COMPARATOR_KINDS):
            incomplete.append(key)
            continue
        kinds = {row.kind for row in selected}
        hashes = {row.training_transcript_hash for row in selected}
        if kinds != set(COMPARATOR_KINDS):
            incomplete.append(key)
        if len(hashes) != 1:
            mismatches.append(key)

    audit = {
        "architecture_count": len(COMPARATOR_KINDS),
        "complete_world_count": len(grouped) - len(set(incomplete)),
        "incomplete_worlds": incomplete,
        "matching_transcript_world_count": len(grouped) - len(set(mismatches)),
        "transcript_mismatch_worlds": mismatches,
        "world_count": len(grouped),
    }
    if incomplete or mismatches:
        raise RuntimeError(f"CX01 development fairness audit failed: {audit}")
    return audit


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
    summary = development_summary(rows)
    summary["training_transcript_audit"] = _training_transcript_audit(rows)
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
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
