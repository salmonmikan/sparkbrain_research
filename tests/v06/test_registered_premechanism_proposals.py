from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import StateLocus
from sparkbrain.evaluation.v061_premechanism_admission import (
    MechanismFamily,
    PreMechanismProposal,
    assess_premechanism_admission,
)

A01_V1_HASH = "2794d1596227eab17c68c46d6874662c3669656edb49e28425f1ef613b66c5dc"
A01_V2_HASH = "c31e7c4148a2940e09c65960b8f208242e9e1d4c19f01929fcdc81b7b7379147"
A01_PROTOCOL_SOURCE_SHA = "92c2ead081844861847d679315639da6de401e1b"


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _record(filename: str) -> dict[str, object]:
    path = _repository_root() / "docs" / "diagnostics" / "v061" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _proposal_from_record(record: dict[str, object]) -> PreMechanismProposal:
    raw = dict(record["proposal"])  # type: ignore[arg-type]
    raw["mechanism_family"] = MechanismFamily(str(raw["mechanism_family"]))
    raw["expected_p3_carrier_loci"] = tuple(
        StateLocus(str(value)) for value in raw["expected_p3_carrier_loci"]
    )
    return PreMechanismProposal(**raw)  # type: ignore[arg-type]


def test_a01_v1_is_preserved_as_superseded_before_implementation() -> None:
    record = _record("V061_A01_TRANSIENT_RETURN_ADDRESS_PROPOSAL.json")
    proposal = dict(record["proposal"])  # type: ignore[arg-type]
    assert record["status"] == "SUPERSEDED_BEFORE_IMPLEMENTATION"
    assert record["superseded_by"] == (
        "V061_A01_TRANSIENT_RETURN_ADDRESS_PROPOSAL_V2.json"
    )
    assert proposal["bound_specification_hash"] == A01_V1_HASH
    assert record["candidate_003_reexecuted"] is False
    assert record["primary_runtime_modified"] is False


def test_a01_v2_preregistration_is_source_bound_and_admitted() -> None:
    record = _record("V061_A01_TRANSIENT_RETURN_ADDRESS_PROPOSAL_V2.json")
    proposal = _proposal_from_record(record)
    assessment = assess_premechanism_admission(proposal)
    assert record["status"] == "PREREGISTERED_NOT_IMPLEMENTED"
    assert record["candidate_003_reexecuted"] is False
    assert record["primary_runtime_modified"] is False
    assert proposal.bound_specification_hash == A01_V2_HASH
    assert proposal.protocol_bundle_source_sha == A01_PROTOCOL_SOURCE_SHA
    assert assessment.specification_hash == A01_V2_HASH
    assert assessment.specification_binding_valid is True
    assert assessment.protocol_source_binding_valid is True
    assert assessment.admitted_for_implementation is True
    assert assessment.missing_requirements == ()


def test_a01_v2_binds_exact_mechanism_and_null_documents() -> None:
    proposal = _proposal_from_record(
        _record("V061_A01_TRANSIENT_RETURN_ADDRESS_PROPOSAL_V2.json")
    )
    assert proposal.mechanism_rule_spec_path == (
        "docs/V061_A01_TRANSIENT_RETURN_ADDRESS_PROTOCOL.md"
    )
    assert proposal.null_ladder_spec_path == "docs/V061_A01_NULL_LADDER.md"
    assert proposal.mechanism_family is MechanismFamily.TRANSIENT_RETURN_ADDRESS
    assert proposal.expected_p3_carrier_loci == (
        StateLocus.LOCAL_TRANSITION,
        StateLocus.TRANSIENT_RETURN_ADDRESS,
    )
