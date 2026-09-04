from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.evaluation.v061_premechanism_admission import (
    MechanismFamily,
    PreMechanismProposal,
    assess_premechanism_admission,
)
from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import StateLocus


A01_HASH = "2794d1596227eab17c68c46d6874662c3669656edb49e28425f1ef613b66c5dc"


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _a01_record() -> dict[str, object]:
    path = (
        _repository_root()
        / "docs"
        / "diagnostics"
        / "v061"
        / "V061_A01_TRANSIENT_RETURN_ADDRESS_PROPOSAL.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _proposal_from_record(record: dict[str, object]) -> PreMechanismProposal:
    raw = dict(record["proposal"])  # type: ignore[arg-type]
    raw["mechanism_family"] = MechanismFamily(str(raw["mechanism_family"]))
    raw["expected_p3_carrier_loci"] = tuple(
        StateLocus(str(value)) for value in raw["expected_p3_carrier_loci"]
    )
    return PreMechanismProposal(**raw)  # type: ignore[arg-type]


def test_a01_preregistration_is_bound_and_admitted() -> None:
    record = _a01_record()
    proposal = _proposal_from_record(record)
    assessment = assess_premechanism_admission(proposal)
    assert record["status"] == "PREREGISTERED_NOT_IMPLEMENTED"
    assert record["candidate_003_reexecuted"] is False
    assert record["primary_runtime_modified"] is False
    assert proposal.bound_specification_hash == A01_HASH
    assert assessment.specification_hash == A01_HASH
    assert assessment.specification_binding_valid is True
    assert assessment.admitted_for_implementation is True
    assert assessment.missing_requirements == ()


def test_a01_is_registered_as_transient_return_address_family() -> None:
    proposal = _proposal_from_record(_a01_record())
    assert proposal.mechanism_family is MechanismFamily.TRANSIENT_RETURN_ADDRESS
    assert proposal.expected_p3_carrier_loci == (
        StateLocus.LOCAL_TRANSITION,
        StateLocus.TRANSIENT_RETURN_ADDRESS,
    )
