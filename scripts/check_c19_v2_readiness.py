from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.v03_external_validation.truth_free_adapter import (
    BeliefRTruthFreeSymbolicAdapter,
    TruthFreeBeliefRInput,
    static_representation_audit,
)

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "artifacts/v03/c19_external_validation/v2/preregistration.json"


def main() -> None:
    protocol = json.loads(PREREG.read_text(encoding="utf-8"))
    if protocol["official_evaluation_allowed"] is not False:
        raise RuntimeError("C19-v2 readiness must not enable official evaluation")
    pin = protocol["belief_r_metadata_pin"]
    if any(
        pin[key] is not False
        for key in (
            "cache_content_access_allowed",
            "cache_verification_allowed",
            "examples_read_allowed",
        )
    ):
        raise RuntimeError("C19-v2 readiness must keep official data inaccessible")

    probe = TruthFreeBeliefRInput(
        record_id="synthetic-readiness-probe",
        source_index=0,
        step_index=0,
        question=(
            "Premise one. New premise. What necessarily had to follow assuming that "
            "the above premises were true?"
        ),
        choices=("alpha", "beta", "uncertain"),
    )
    encoded = BeliefRTruthFreeSymbolicAdapter().encode(probe)
    audit = static_representation_audit(probe)
    if encoded.oracle:
        raise RuntimeError("truth-free adapter unexpectedly became Oracle-privileged")
    if not audit["same_visible_input_bytes"]:
        raise RuntimeError("autonomous conditions do not share the same visible byte boundary")
    if audit["exact_feature_equivalent_to_i0"] or audit["exact_feature_equivalent_to_i1"]:
        raise RuntimeError("truth-free adapter is exactly feature-equivalent to an existing input")

    print(
        json.dumps(
            {
                "adapter_contract_id": protocol["adapter_contract_id"],
                "official_data_access": False,
                "protocol_id": protocol["protocol_id"],
                "readiness": "static_checks_pass",
                "representation_audit": audit,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
