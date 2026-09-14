from __future__ import annotations

import json
from pathlib import Path

import pytest

import sparkbrain.research.rv02_rd005_bound_construction as bound

_CANONICAL_DIGEST = "a" * 64


class _FakePlan:
    def __init__(self, *, source_manifest: object, collision_registry: object) -> None:
        self.source_manifest = source_manifest
        self.collision_registry = collision_registry

    def validate(self) -> None:
        return None

    @property
    def package_plan_sha256(self) -> str:
        return _CANONICAL_DIGEST


def _patch_plan_inputs(
    monkeypatch: pytest.MonkeyPatch,
    *,
    supplied_digest: str,
) -> None:
    monkeypatch.setattr(bound, "RD005DevelopmentPackagePlan", _FakePlan)
    monkeypatch.setattr(
        bound,
        "_load_input",
        lambda raw: (
            {"package_plan_sha256": supplied_digest},
            object(),
            object(),
        ),
    )


def test_package_plan_preflight_accepts_exact_canonical_digest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_plan_inputs(monkeypatch, supplied_digest=_CANONICAL_DIGEST)

    assert bound.verify_package_plan_binding({"fixture": True}) == _CANONICAL_DIGEST


def test_package_plan_preflight_rejects_unrelated_valid_hex_digest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_plan_inputs(monkeypatch, supplied_digest="d" * 64)

    with pytest.raises(ValueError, match="does not match the canonical"):
        bound.verify_package_plan_binding({"fixture": True})


def test_bound_runner_refuses_mismatch_before_delegating(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps({"fixture": True}), encoding="utf-8")
    _patch_plan_inputs(monkeypatch, supplied_digest="d" * 64)
    delegated = False

    def _unexpected_delegate(*, input_path: Path, repo_root: Path) -> Path:
        nonlocal delegated
        delegated = True
        return input_path

    monkeypatch.setattr(bound, "run_construction", _unexpected_delegate)

    with pytest.raises(ValueError, match="does not match the canonical"):
        bound.run_bound_construction(input_path=input_path, repo_root=tmp_path)
    assert delegated is False


def test_bound_runner_delegates_only_after_exact_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps({"fixture": True}), encoding="utf-8")
    _patch_plan_inputs(monkeypatch, supplied_digest=_CANONICAL_DIGEST)
    expected_output = tmp_path / "output"
    observed: list[tuple[Path, Path]] = []

    def _delegate(*, input_path: Path, repo_root: Path) -> Path:
        observed.append((input_path, repo_root))
        return expected_output

    monkeypatch.setattr(bound, "run_construction", _delegate)

    result = bound.run_bound_construction(input_path=input_path, repo_root=tmp_path)
    assert result == expected_output
    assert observed == [(input_path, tmp_path)]
