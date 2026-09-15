from __future__ import annotations

from scripts.run_v061_a01_md002_p2_candidate_002 import (
    CANDIDATE_ID,
    build_candidate_002_fixture_and_schedule,
    candidate_manifest,
)
from scripts.run_v061_a01_md002_p2_shared_probe import (
    build_registered_fixture_and_schedule,
)
from sparkbrain.v061_a01.md002_protocol import canonical_sha256


def _contract_state(fixture: object) -> dict[str, object]:
    contract = fixture.prospective_contract()
    contract.validate()
    return {
        "control": contract.control.state_dict(),
        "intervention": contract.intervention.state_dict(),
        "control_world_relation_sha256": contract.control_world_relation_sha256,
        "intervention_world_relation_sha256": contract.intervention_world_relation_sha256,
        "admissible_external_evidence_sha256": contract.admissible_external_evidence_sha256,
    }


def test_candidate_002_is_structurally_distinct_without_execution() -> None:
    candidate_fixture, candidate_schedule = build_candidate_002_fixture_and_schedule()
    legacy_fixture, legacy_schedule = build_registered_fixture_and_schedule()

    candidate_contract = _contract_state(candidate_fixture)
    legacy_contract = _contract_state(legacy_fixture)
    assert canonical_sha256(candidate_contract) != canonical_sha256(legacy_contract)
    assert canonical_sha256(candidate_schedule.state_dict()) != canonical_sha256(
        legacy_schedule.state_dict()
    )


def test_candidate_manifest_binds_exact_source_and_input_without_scoring() -> None:
    source_sha = "1" * 40
    manifest = candidate_manifest(source_sha)
    assert manifest["candidate_id"] == CANDIDATE_ID
    assert manifest["source_sha"] == source_sha
    assert manifest["development_only"] is True
    assert manifest["held_out_execution_allowed"] is False
    assert manifest["formal_execution_allowed"] is False
    assert str(manifest["execution_identity"]).startswith(
        "a01-md002-p2-candidate-002-"
    )
    assert "result" not in manifest
    assert "verdict" not in manifest
