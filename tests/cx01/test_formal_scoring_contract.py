from __future__ import annotations

import hashlib

import pytest

from sparkbrain.comparison.cx01.candidate import (
    CX01_COMPARATOR_INVENTORY,
    CandidatePurpose,
    CandidateSpec,
)
from sparkbrain.comparison.cx01.formal import _semantic_execution_hash
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


def _add_semantic_hash(row: dict[str, object]) -> dict[str, object]:
    identity_payload = {
        "candidate_spec_hash": row["candidate_spec_hash"],
        "family": row["family"],
        "formal_index": row["formal_index"],
        "kind": row["kind"],
        "manifest_hash": row["manifest_hash"],
        "seed": row["seed"],
        "training_transcript_hash": row["training_transcript_hash"],
        "world_hash": row["world_hash"],
    }
    return {
        **row,
        "semantic_execution_hash": _semantic_execution_hash(
            identity_payload=identity_payload,
            row=row,
        ),
    }


def _rows(candidate: CandidateSpec, manifest) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    index = 0
    for family in CX01Family:
        for seed in candidate.seeds:
            transcript_hash = hashlib.sha256(f"{family.value}:{seed}".encode()).hexdigest()
            world_hash = hashlib.sha256(f"world:{family.value}:{seed}".encode()).hexdigest()
            for kind in CX01_COMPARATOR_INVENTORY:
                row: dict[str, object] = {
                    "candidate_spec_hash": candidate.specification_hash(),
                    "decision": {"family": family.value, "gates": [], "passed": True},
                    "evidence": {"family": family.value},
                    "execution_id": hashlib.sha256(f"execution:{index}".encode()).hexdigest(),
                    "family": family.value,
                    "formal_index": index,
                    "kind": kind.value,
                    "manifest_hash": manifest.manifest_hash(),
                    "resource": {
                        "decision_use": "descriptive-only",
                        "generated_internal_events": 0,
                        "observed_external_events": 0,
                        "parameter_count": 0,
                        "peak_traced_memory_bytes": 100,
                        "privileges": [
                            value.value for value in privilege_profile(kind).privileges
                        ],
                        "process_cpu_ns": 100,
                        "state_entry_count": 0,
                        "wall_clock_ns": 100,
                    },
                    "seed": seed,
                    "training_transcript_hash": transcript_hash,
                    "world_hash": world_hash,
                }
                rows.append(_add_semantic_hash(row))
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
    changed = {**rows[1], "training_transcript_hash": "f" * 64}
    rows[1] = _add_semantic_hash(changed)
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
    changed = {**rows[0], "resource": {**rows[0]["resource"], "privileges": []}}
    rows[0] = _add_semantic_hash(changed)
    with pytest.raises(RuntimeError, match="privilege inventory mismatch"):
        _validate_rows(
            tuple(rows),
            candidate=candidate,
            manifest=manifest,
            policy=FormalScoringPolicy(),
        )


def test_formal_row_validator_rejects_semantic_tamper_even_when_raw_checksum_is_valid() -> None:
    candidate = _candidate()
    manifest = _manifest(candidate)
    rows = list(_rows(candidate, manifest))
    rows[0] = {**rows[0], "decision": {"family": rows[0]["family"], "passed": False}}
    with pytest.raises(RuntimeError, match="semantic execution hash mismatch"):
        _validate_rows(
            tuple(rows),
            candidate=candidate,
            manifest=manifest,
            policy=FormalScoringPolicy(),
        )
