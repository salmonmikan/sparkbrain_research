from __future__ import annotations

import json

from sparkbrain.v03_external_validation.c19_r1_protocol import (
    EXPECTED_PAIRS,
    OFFICIAL_SEEDS,
    load_and_validate_contract,
)
from sparkbrain.v03_external_validation.c19_r1_revision_authority import (
    ExecutionAdmissionR1,
    R1AcquisitionHarness,
    RuntimeBoundary,
    select_revision_authority,
)
from sparkbrain.v03_external_validation.c19_r1_source_map import (
    atomic_idx_clusters,
    atomic_idx_source_map_sha256,
    validate_atomic_idx_source_map,
)


def _synthetic_examples() -> tuple[dict[str, object], ...]:
    examples = []
    for pair_index in range(EXPECTED_PAIRS):
        for step_index in (0, 1):
            examples.append(
                {
                    "record_id": f"synthetic-r1-{pair_index}-step-{step_index}",
                    "source_index": step_index,
                    "pair_index": pair_index,
                    "step_index": step_index,
                    "question": (
                        f"Entity {pair_index} has a visible revision at step {step_index}. "
                        "What necessarily had to follow?"
                    ),
                    "choices": (
                        f"option a {pair_index}",
                        f"option b {step_index}",
                        f"option c {pair_index + step_index}",
                    ),
                }
            )
    return tuple(examples)


def _synthetic_source_map() -> tuple[dict[str, object], ...]:
    return validate_atomic_idx_source_map(
        tuple(
            {"pair_index": pair_index, "atomic_idx": f"atomic-{pair_index // 2}"}
            for pair_index in range(EXPECTED_PAIRS)
        )
    )


def main() -> None:
    contract = load_and_validate_contract()
    tie = {"a": 0.6, "b": 0.3, "c": 0.1}
    selected, _, _, _ = select_revision_authority(tie, tie)
    if selected != 1:
        raise SystemExit("R1 exact certainty tie must prefer visible revision")
    selected, _, _, _ = select_revision_authority(
        {"a": 0.8, "b": 0.1, "c": 0.1},
        {"a": 0.4, "b": 0.35, "c": 0.25},
    )
    if selected != 0:
        raise SystemExit("R1 stronger earlier certainty must retain step 0")

    harness = R1AcquisitionHarness(boundary=RuntimeBoundary())
    raw = harness.acquire(
        admission=ExecutionAdmissionR1.synthetic_dev(),
        examples=_synthetic_examples(),
    )
    expected_records = len(OFFICIAL_SEEDS) * EXPECTED_PAIRS
    if len(raw.records) != expected_records:
        raise SystemExit("R1 synthetic raw inventory drift")
    if any(record["source_index"] != 1 or record["step_index"] != 1 for record in raw.records):
        raise SystemExit("R1 raw must preserve the final-step evaluator join identity")

    source_map = _synthetic_source_map()
    source_map_digest = atomic_idx_source_map_sha256(source_map)
    if source_map_digest != atomic_idx_source_map_sha256(tuple(dict(row) for row in source_map)):
        raise SystemExit("R1 atomic_idx source-map digest must be deterministic")
    if any(set(row) != {"pair_index", "atomic_idx"} for row in source_map):
        raise SystemExit("R1 atomic_idx source map must contain no target fields")
    clusters = atomic_idx_clusters(source_map)
    if sum(len(indices) for _, indices in clusters) != EXPECTED_PAIRS:
        raise SystemExit("R1 atomic_idx source map must assign every pair exactly once")

    print(
        json.dumps(
            {
                "contract": contract,
                "synthetic_records": len(raw.records),
                "synthetic_raw_sha256": raw.sha256,
                "synthetic_atomic_idx_source_map_sha256": source_map_digest,
                "synthetic_atomic_idx_clusters": len(clusters),
                "official_data_accessed": False,
                "official_execution_allowed": False,
                "status": "R1_PRE_START_READY_FOR_ANALYST_REVIEW",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
