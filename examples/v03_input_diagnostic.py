from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v03_seed import (
    compositional_text_features,
    sparse_cosine_similarity,
    whole_string_hash_features,
)

PAIRS = (
    ("paraphrase", "The cat is on the table", "A cat is on that table", "similar"),
    (
        "restatement",
        "What necessarily follows from the premises?",
        "Given only the premises, which conclusion necessarily follows?",
        "similar",
    ),
    ("unrelated", "The cat is on the table", "Rain changes the river", "different"),
    ("negation-trap", "Ada is a bird", "Ada is not a bird", "opposite-high-overlap"),
)


def score(kind: str, left: str, right: str) -> float:
    encoder = (
        whole_string_hash_features
        if kind == "legacy-whole-string-hash"
        else compositional_text_features
    )
    return sparse_cosine_similarity(encoder(left), encoder(right))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/v03_input_diagnostic")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for pair_id, left, right, relation in PAIRS:
        rows.append(
            {
                "pair_id": pair_id,
                "expected_relation": relation,
                "legacy_similarity": score("legacy-whole-string-hash", left, right),
                "local_feature_similarity": score("local-compositional", left, right),
            }
        )
    payload = {
        "status": "diagnostic_only",
        "claim_boundary": "surface overlap is not semantic understanding",
        "rows": rows,
    }
    (output / "input-diagnostic.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# v0.3 input seed diagnostic",
        "",
        "| pair | expected | whole-string hash | local features |",
        "|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['pair_id']} | {row['expected_relation']} | "
            f"{row['legacy_similarity']:.4f} | {row['local_feature_similarity']:.4f} |"
        )
    lines.extend(
        [
            "",
            "The negation trap is intentionally included: local overlap may stay high "
            "even when meaning reverses.",
            "This report is not evidence of semantic or language understanding.",
        ]
    )
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
