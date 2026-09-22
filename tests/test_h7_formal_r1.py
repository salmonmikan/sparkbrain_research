from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.learned.h7_formal_r1 import (
    COMPARATORS,
    EXPECTED_CONTRACT_BLOB,
    EXPECTED_EVALUATOR_SHA256,
    EXPECTED_INPUT_SURFACE_SHA256,
    INTERVENTION_ID,
    FormalIntegrityError,
    FutureIdentityBinding,
    TargetBlindRawCollector,
    assert_contract_design,
    preflight_sentinel,
    preserve_raw_create_only,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "artifacts" / "formal_h7_r1" / "contract_design.json"


def _binding() -> FutureIdentityBinding:
    return FutureIdentityBinding(
        identity_id="SENTINEL-NOT-A-FORMAL-IDENTITY",
        final_source_sha="a" * 40,
        contract_blob=EXPECTED_CONTRACT_BLOB,
        runner_blob="b" * 40,
        scorer_blob="c" * 40,
        preserver_blob="d" * 40,
        package_manifest_sha256="e" * 64,
        runtime_manifest_sha256="f" * 64,
        input_surface_sha256=EXPECTED_INPUT_SURFACE_SHA256,
        evaluator_spec_sha256=EXPECTED_EVALUATOR_SHA256,
        intervention_id=INTERVENTION_ID,
        comparators=COMPARATORS,
    )


def test_contract_design_is_exactly_supported() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert_contract_design(contract)


def test_same_final_sha_gate_fails_closed() -> None:
    binding = _binding()
    binding.assert_frozen_semantics()
    binding.assert_same_final_sha("a" * 40)
    with pytest.raises(FormalIntegrityError, match="same-final-SHA"):
        binding.assert_same_final_sha("9" * 40)


def test_target_blind_collector_and_preserver_are_create_only(tmp_path: Path) -> None:
    binding = _binding()
    raw = tmp_path / "raw.jsonl"
    collector = TargetBlindRawCollector(raw, binding, "a" * 40)
    collector.append(
        {
            "endpoint": "SENTINEL_NOT_SCIENTIFIC",
            "world": "SENTINEL",
            "episode_seed": -1,
            "step_index": -1,
            "baseline_correct": 0,
            "cut_correct": 0,
            "total_variation": 0.0,
        }
    )
    receipt = collector.close()
    assert receipt["target_blind"] is True
    assert receipt["decision_present"] is False

    preserve = preserve_raw_create_only(
        raw_path=raw,
        preserve_dir=tmp_path / "preserved",
        binding=binding,
        actual_sha="a" * 40,
    )
    assert preserve.raw_sha256 == receipt["raw_sha256"]

    with pytest.raises(FormalIntegrityError, match="no-clobber"):
        TargetBlindRawCollector(raw, binding, "a" * 40)
    with pytest.raises(FormalIntegrityError, match="no-clobber"):
        preserve_raw_create_only(
            raw_path=raw,
            preserve_dir=tmp_path / "preserved",
            binding=binding,
            actual_sha="a" * 40,
        )


def test_target_blind_collector_rejects_decision_fields(tmp_path: Path) -> None:
    collector = TargetBlindRawCollector(tmp_path / "raw.jsonl", _binding(), "a" * 40)
    with pytest.raises(FormalIntegrityError, match="scorer field"):
        collector.append({"decision": "PASS"})
    collector.close()


def test_preflight_is_explicitly_non_scientific() -> None:
    value = preflight_sentinel()
    assert value["target_blind_guard"] == "PASS"
    assert value["no_identity_created"] is True
    assert value["no_started_created"] is True
    assert value["no_protected_evaluation_access"] is True
    assert value["no_official_raw_created"] is True
    assert value["no_scoring_performed"] is True
    assert "decision" not in value
