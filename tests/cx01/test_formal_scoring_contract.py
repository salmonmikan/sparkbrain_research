from __future__ import annotations

import hashlib

import pytest

from sparkbrain.comparison.cx01.candidate import (
    CX01_COMPARATOR_INVENTORY,
    CandidatePurpose,
    CandidateSpec,
)
from sparkbrain.comparison.cx01.formal_policy import FormalScoringPolicy
from sparkbrain.comparison.cx01.formal_scoring import _validate_rows
from sparkbrain.comparison.cx01.freeze import build_freeze_manifest
from sparkbrain.comparison.cx01.privilege import privilege_profile
from sparkbrain.comparison.cx01.worlds import CX01Family


def _candidate() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-fixture-scoring-001",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
    )


def _manifest(candidate: CandidateSpec):
    return build_freeze_manifest(
        source_git_sha="a" * 40,
        builder="builder-a",
        candidate=candidate,
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
    )


def _rows(candidate: CandidateSpec, manifest) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    index = 0
    for family in CX01Family:
        for seed in candidate.seeds:
            transcript_hash = hashlib.sha256(f"{family.value}:{seed}".encode()).hexdigest()
            for kind in CX01_COMPARATOR_INVENTORY:
                rows.append(
                    {
                        "candidate_spec_hash": candidate.specification_hash(),
                        "decision": {"family": family.value, "passed": True},
                        "execution_id": hashlib.sha256(f"execution:{index}".encode()).hexdigest(),
                        "family": family.value,
                        "formal_index": index,
                        "kind": kind.value,
                        "manifest_hash": manifest.manifest_hash(),
                        "resource": {
                            "privileges": [
                                value.value for value in privilege_profile(kind).privileges
                            ]
                        },
                        "seed": seed,
                        "training_transcript_hash": transcript_hash,
                    }
                )
                index += 1
    return tuple(rows)


def test_manifest_binds_exact_formal_scoring_policy() -> None:
    manifest = _manifest(_candidate())
    assert manifest.scoring_policy_hash == FormalScoringPolicy().policy_hash()


def test_formal_row_validator_requires_complete_equal_transcripts_and_privileges() -> None:
    candidate = _candidate()
    manifest = _manifest(candidate)
    rows = _rows(candidate, manifest)
    _validate_rows(
        rows,
        candidate=candidate,
        manifest=manifest,
        policy=FormalScoringPolicy(),
    )


def test_formal_row_validator_rejects_transcript_mismatch() -> None:
    candidate = _candidate()
    manifest = _manifest(candidate)
    rows = list(_rows(candidate, manifest))
    rows[1] = {**rows[1], "training_transcript_hash": "f" * 64}
    with pytest.raises(RuntimeError, match="identical training transcripts"):
        _validate_rows(
            tuple(rows),
            candidate=candidate,
            manifest=manifest,
            policy=FormalScoringPolicy(),
        )


def test_formal_row_validator_rejects_hidden_privilege_drift() -> None:
    candidate = _candidate()
    manifest = _manifest(candidate)
    rows = list(_rows(candidate, manifest))
    rows[0] = {**rows[0], "resource": {"privileges": []}}
    with pytest.raises(RuntimeError, match="privilege inventory mismatch"):
        _validate_rows(
            tuple(rows),
            candidate=candidate,
            manifest=manifest,
            policy=FormalScoringPolicy(),
        )
