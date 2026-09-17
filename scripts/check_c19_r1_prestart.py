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

    print(
        json.dumps(
            {
                "contract": contract,
                "synthetic_records": len(raw.records),
                "synthetic_raw_sha256": raw.sha256,
                "official_data_accessed": False,
                "official_execution_allowed": False,
                "status": "R1_PRE_START_READY_FOR_ANALYST_REVIEW",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
