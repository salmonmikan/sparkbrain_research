from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sparkbrain.research.rv01_r01_16_construction import run_construction
from sparkbrain.research.rv01_r01_16_development_package import (
    R01_16_REQUIRED_SOURCE_PATHS,
    R0116CollisionRegistry,
    R0116DevelopmentPackagePlan,
    R0116SourceManifest,
    R0116SourceManifestEntry,
)

SOURCE_SHA = "a" * 40
FILE_SHA = "b" * 64


def _connection(
    source_id: int,
    target_id: int,
    *,
    weight: float,
    delay_ms: float,
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "target_id": target_id,
        "weight": weight,
        "delay_ms": delay_ms,
        "plastic": True,
    }


def _manifest() -> R0116SourceManifest:
    return R0116SourceManifest(
        source_git_sha=SOURCE_SHA,
        entries=tuple(
            R0116SourceManifestEntry(path=path, sha256=FILE_SHA)
            for path in sorted(R01_16_REQUIRED_SOURCE_PATHS)
        ),
    )


def _registry() -> R0116CollisionRegistry:
    return R0116CollisionRegistry(
        registry_id="rv01-retained-identities-v1",
        source_paths=("docs/research/RV01_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(141500, 141600),
        consumed_or_reserved_world_ids=(
            "r01-15:development:route-a:141500",
            "r01-15:held-out:route-a:141600",
        ),
        authoritative_complete=True,
    )


def _payload(
    *,
    changed: bool = True,
    cue_source_ids: list[int] | None = None,
) -> tuple[dict[str, object], R0116DevelopmentPackagePlan]:
    pre = [
        _connection(1, 2, weight=0.25, delay_ms=2.0),
        _connection(2, 3, weight=0.50, delay_ms=3.0),
    ]
    post = [
        _connection(1, 2, weight=0.75 if changed else 0.25, delay_ms=2.0),
        _connection(2, 3, weight=0.50, delay_ms=4.0 if changed else 3.0),
    ]
    plan = R0116DevelopmentPackagePlan(
        source_manifest=_manifest(),
        collision_registry=_registry(),
    )
    return (
        {
            "source_manifest": plan.source_manifest.state_dict(),
            "collision_registry": plan.collision_registry.state_dict(),
            "package_plan_sha256": plan.package_plan_sha256,
            "registered_unit_ids": [1, 2, 3, 9],
            "cue_source_ids": cue_source_ids or [1],
            "probe_horizon_ms": 10.0,
            "pre_training": pre,
            "post_training": post,
            "queued_propagation": [],
        },
        plan,
    )


def _write_input(
    path: Path,
    *,
    changed: bool = True,
    cue_source_ids: list[int] | None = None,
) -> R0116DevelopmentPackagePlan:
    payload, plan = _payload(changed=changed, cue_source_ids=cue_source_ids)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return plan


def test_r01_16_construction_writes_package_bound_reachability_artifacts(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    plan = _write_input(input_path)
    expected_output = tmp_path / plan.output_relpath

    result = run_construction(input_path=input_path, repo_root=tmp_path)

    assert result == expected_output
    assert (result / "construction_input.json").read_bytes() == input_path.read_bytes()
    complete = json.loads((result / "COMPLETE.json").read_text(encoding="utf-8"))
    assert complete["status"] == (
        "CONSTRUCTION_COMPLETE_REACHABILITY_BOUND_CAPABILITY_UNOPENED"
    )
    assert complete["weight_eligible"] is True
    assert complete["delay_eligible"] is True
    assert complete["combined_eligible"] is True
    assert complete["capability_output_opened"] is False
    assert complete["learner_or_probe_executed"] is False
    assert complete["formal_execution_allowed"] is False
    assert (result / "reachability_certificate.json").is_file()
    assert not (result / "FAILED.json").exists()

    identity = json.loads((result / "input_identity.json").read_text(encoding="utf-8"))
    assert identity["package_plan_sha256"] == plan.package_plan_sha256
    assert identity["output_relpath"] == plan.output_relpath
    runtime = json.loads((result / "runtime.json").read_text(encoding="utf-8"))
    assert runtime["python_executable"] == sys.executable
    assert runtime["runner_module"] == "sparkbrain.research.rv01_r01_16_construction"

    for arm in ("F0", "FW", "FD", "FWD"):
        assert (result / "arms" / f"{arm}.json").is_file()


def test_r01_16_unreachable_contrast_is_retained_as_ineligible_not_negative(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    plan = _write_input(input_path, cue_source_ids=[9])

    result = run_construction(input_path=input_path, repo_root=tmp_path)

    assert result == tmp_path / plan.output_relpath
    complete = json.loads((result / "COMPLETE.json").read_text(encoding="utf-8"))
    assert complete["weight_eligible"] is False
    assert complete["delay_eligible"] is False
    assert complete["combined_eligible"] is False
    certificate = json.loads(
        (result / "reachability_certificate.json").read_text(encoding="utf-8")
    )
    assert certificate["reachable_weight_edges"] == []
    assert certificate["reachable_delay_edges"] == []


def test_r01_16_package_identity_never_allows_alternate_output_or_clobber(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    plan = _write_input(input_path)
    output_dir = tmp_path / plan.output_relpath
    run_construction(input_path=input_path, repo_root=tmp_path)
    complete_before = (output_dir / "COMPLETE.json").read_bytes()

    with pytest.raises(FileExistsError):
        run_construction(input_path=input_path, repo_root=tmp_path)

    assert (output_dir / "COMPLETE.json").read_bytes() == complete_before


def test_r01_16_zero_contrast_is_retained_as_terminal_construction_failure(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    plan = _write_input(input_path, changed=False)
    output_dir = tmp_path / plan.output_relpath

    with pytest.raises(RuntimeError, match="no learned weight or delay contrast"):
        run_construction(input_path=input_path, repo_root=tmp_path)

    failed = json.loads((output_dir / "FAILED.json").read_text(encoding="utf-8"))
    assert failed["status"] == "CONSTRUCTION_FAILED_TERMINAL_FOR_THIS_OUTPUT_IDENTITY"
    assert failed["retry_same_output_identity_allowed"] is False
    assert not (output_dir / "COMPLETE.json").exists()


def test_r01_16_invalid_input_does_not_consume_a_package_output_identity(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    payload, plan = _payload()
    payload["capability_allowed"] = True
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="keys must exactly match"):
        run_construction(input_path=input_path, repo_root=tmp_path)

    assert not (tmp_path / plan.output_relpath).exists()


def test_r01_16_package_digest_mismatch_fails_before_consuming_output(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    payload, plan = _payload()
    payload["package_plan_sha256"] = "f" * 64
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="package plan digest does not match"):
        run_construction(input_path=input_path, repo_root=tmp_path)

    assert not (tmp_path / plan.output_relpath).exists()


def test_r01_16_missing_input_does_not_leave_empty_output_directory(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        run_construction(input_path=missing, repo_root=tmp_path)

    assert not (tmp_path / "artifacts").exists()
