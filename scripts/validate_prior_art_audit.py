from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/research/literature_matrix.csv"
REPORT = ROOT / "docs/research/claim_challenge_report.md"
START = "<!-- GENERATED:PRIOR_ART_CLAIMS:START -->"
END = "<!-- GENERATED:PRIOR_ART_CLAIMS:END -->"
TARGETS = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "CL-008", "CL-009", "CL-010", "CL-011"]
TESTS = {
    "G1": (
        "formal state semantics and held-out revision against HMM, active-inference, "
        "and blackboard baselines"
    ),
    "G2": (
        "compare provenance, duplicate evidence, support, and attack semantics against "
        "LIDA and bipolar argumentation"
    ),
    "G3": "preregistered loser-retention ablation with uncertainty across reversals",
    "G4": (
        "calibrated abstention and reset/search comparison with an explicit no-ignition "
        "trace contract"
    ),
    "G5": "no-touch counters, identical-output dense equivalence, and scale measurements",
    "G6": (
        "causal intervention and trace utility beyond existing inspectable cognitive "
        "architectures"
    ),
    "G7": "predeclared rate/spike behavioral equivalence and documented failures",
    "CL-008": "causal specialization, held-out reuse, and destruction controls",
    "CL-009": "C07 invariant suite against established spiking cognitive and neuromorphic systems",
    "CL-010": "matched physical energy measurement with accuracy and latency controls",
    "CL-011": "clean-room local reproduction on supported platforms",
}
RANK = {
    "strong_near_duplicate": 0,
    "strong_execution_precedent": 0,
    "strong_formal_precedent": 0,
    "strong_hardware_precedent": 0,
    "known_component": 1,
    "baseline_precedent": 1,
    "evaluation_precedent": 1,
    "partial_overlap": 2,
}
REQUIRED_CODE_ROWS = {"PA-006", "PA-008", "PA-009", "PA-014", "PA-015"}


def load_rows() -> list[dict[str, str]]:
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def claims(row: dict[str, str]) -> set[str]:
    return {item.strip() for item in row["sparkbrain_claims_challenged"].split(";") if item.strip()}


def strongest(rows: list[dict[str, str]], target: str) -> list[dict[str, str]]:
    candidates = [row for row in rows if target in claims(row)]
    best = min(RANK.get(row["novelty_verdict"], 9) for row in candidates)
    return [row for row in candidates if RANK.get(row["novelty_verdict"], 9) == best]


def render(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Target | Strongest matrix counterexample(s) | Matrix verdict(s) | "
        "Evidence required to survive the challenge |",
        "|---|---|---|---|",
    ]
    for target in TARGETS:
        selected = strongest(rows, target)
        ids = ", ".join(row["id"] for row in selected)
        verdicts = ", ".join(sorted({row["novelty_verdict"] for row in selected}))
        lines.append(f"| {target} | {ids} | {verdicts} | {TESTS[target]} |")
    return "\n".join(lines)


def validate() -> list[str]:
    errors: list[str] = []
    rows = load_rows()
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("matrix IDs are not unique")
    for row in rows:
        if not re.fullmatch(r"PA-\d{3}", row["id"]):
            errors.append(f"invalid ID: {row['id']}")
        required_fields = (
            "family",
            "title",
            "publication_status",
            "primary_url",
            "novelty_verdict",
            "review_status",
            "access_status",
            "reviewed_date",
        )
        for field in required_fields:
            if not row[field].strip():
                errors.append(f"{row['id']} missing {field}")
    covered = set().union(*(claims(row) for row in rows))
    missing = set(TARGETS) - covered
    if missing:
        errors.append(f"targets missing from matrix: {sorted(missing)}")
    by_id = {row["id"]: row for row in rows}
    for item in REQUIRED_CODE_ROWS:
        if not by_id[item]["code_license"].strip() or by_id[item]["code_license"] == "not checked":
            errors.append(f"{item} lacks explicit code/license state")
    if REPORT.is_file():
        text = REPORT.read_text(encoding="utf-8")
        expected = f"{START}\n{render(rows)}\n{END}"
        if expected not in text:
            errors.append("generated claim table is stale relative to matrix")
    else:
        errors.append("claim challenge report is missing")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("PRIOR ART VALIDATION FAILED:\n- " + "\n- ".join(errors))
    print(f"Prior-art audit valid: {len(load_rows())} sources, {len(TARGETS)} targets")


if __name__ == "__main__":
    main()
