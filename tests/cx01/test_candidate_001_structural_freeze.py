from __future__ import annotations

from sparkbrain.comparison.cx01.candidate import (
    CandidatePurpose,
    CandidateSpec,
    build_outcome_blind_declarations,
)
from sparkbrain.comparison.cx01.freeze import build_freeze_manifest

SOURCE_SHA = "f2c5ead5afda7d731033d585511ea68dc066a162"
CANDIDATE_SPEC_HASH = "aba791ade53feb89950ef0f0b673c68f9ef91b82b1ed9f0560ab9f2576e2fc30"
CANDIDATE_GRID_HASH = "6c81390a785deb0ea8fe30e35186361621dc31bb1e42fe09d7c63ab221575db7"
DECLARATION_BUNDLE_HASH = "c77ff6cb90207d9ce02be328fff245926d1f40e196bb86f9b5eeb5d533404613"
MANIFEST_HASH = "e440dbb6fb6ba06e0196380d04c3c177f647a071a0a7c564fa2e817d6eebc915"


def _candidate() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-candidate-001",
        seeds=tuple(range(269810, 269820)),
        purpose=CandidatePurpose.FORMAL,
    )


def test_candidate_001_is_outcome_blind_and_hash_bound() -> None:
    candidate = _candidate()
    candidate.require_formal()
    assert candidate.specification_hash() == CANDIDATE_SPEC_HASH

    declarations = build_outcome_blind_declarations(candidate)
    assert len(declarations) == 420
    assert all(row.status == "unscored" for row in declarations)
    assert all(not row.capability_result_present for row in declarations)
    assert all(not row.measurements_present for row in declarations)


def test_candidate_001_manifest_recomputes_from_frozen_source() -> None:
    manifest = build_freeze_manifest(
        source_git_sha=SOURCE_SHA,
        builder="openai-chatgpt-cx01-freeze-builder",
        candidate=_candidate(),
        execution_command="python -m sparkbrain.comparison.cx01.formal",
        artifact_root="/tmp/cx01-formal",
    )

    assert manifest.candidate_spec_hash == CANDIDATE_SPEC_HASH
    assert manifest.candidate_grid_hash == CANDIDATE_GRID_HASH
    assert manifest.declaration_bundle_hash == DECLARATION_BUNDLE_HASH
    assert manifest.development_grid_hash == (
        "d93b362ce672fffd233973b8f27521f9d6a5fbdf4f3d4cba9369495635a33c9f"
    )
    assert manifest.privilege_inventory_hash == (
        "2a59a2cf34782bcbcf8fd135f2e378fef8dfb391215b25ba5ef8dfc8cd8f513a"
    )
    assert manifest.schedule_policy_hash == (
        "b013e667a6f5fbc8910d11f13e19f7e200d790da17689caa672bd3e965452b6c"
    )
    assert manifest.scoring_policy_hash == (
        "5cc3fe30c978f95e2ddbd0834eafd8963c37e0ccccb1dcc32915556577fcc76a"
    )
    assert manifest.result_schema_hash == (
        "ecfa7bf1e1b9c9546879176bdb2891d6d4b0f984d146bba37566ab0b20c239dc"
    )
    assert manifest.resource_schema_hash == (
        "b452efd1abbd37b581fc064783dfd9da021a1a2a897223fda8b5976e63a248bb"
    )
    assert manifest.manifest_hash() == MANIFEST_HASH
