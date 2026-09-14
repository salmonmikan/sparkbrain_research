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
        "verify_rd005_d1_runtime",
        lambda: {"python_implementation": "CPython", "python_version": "3.11.15"},
    )

    def _load(raw: bytes) -> tuple[dict[str, str], object, object]:
        assert isinstance(raw, bytes)
        json.loads(raw)
        return (
            {"package_plan_sha256": supplied_digest},
            object(),
            object(),
        )

    monkeypatch.setattr(bound, "_load_input", _load)


def test_package_plan_preflight_accepts_exact_canonical_digest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_plan_inputs(monkeypatch, supplied_digest=_CANONICAL_DIGEST)

    assert bound.verify_package_plan_binding(b'{"fixture": true}') == _CANONICAL_DIGEST


def test_package_plan_preflight_rejects_unrelated_valid_hex_digest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_plan_inputs(monkeypatch, supplied_digest="d" * 64)

    with pytest.raises(ValueError, match="does not match the canonical"):
        bound.verify_package_plan_binding(b'{"fixture": true}')


def test_bound_runner_refuses_wrong_runtime_before_reading_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing_input = tmp_path / "not-created.json"

    def _reject_runtime() -> dict[str, str]:
        raise RuntimeError("RD005 D1 Python version mismatch")

    monkeypatch.setattr(bound, "verify_rd005_d1_runtime", _reject_runtime)

    with pytest.raises(RuntimeError, match="Python version mismatch"):
        bound.run_bound_construction(input_path=missing_input, repo_root=tmp_path)


def test_bound_runner_refuses_mismatch_before_delegating(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps({"fixture": True}), encoding="utf-8")
    _patch_plan_inputs(monkeypatch, supplied_digest="d" * 64)
    delegated = False

    def _unexpected_delegate(*, raw: bytes, repo_root: Path) -> Path:
        nonlocal delegated
        delegated = True
        return repo_root

    monkeypatch.setattr(bound, "run_construction_from_bytes", _unexpected_delegate)

    with pytest.raises(ValueError, match="does not match the canonical"):
        bound.run_bound_construction(input_path=input_path, repo_root=tmp_path)
    assert delegated is False


def test_bound_runner_delegates_exact_verified_bytes_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    original_raw = json.dumps({"fixture": True}).encode("utf-8")
    replacement_raw = json.dumps({"fixture": "replaced"}).encode("utf-8")
    input_path.write_bytes(original_raw)
    _patch_plan_inputs(monkeypatch, supplied_digest=_CANONICAL_DIGEST)
    expected_output = tmp_path / "output"
    observed: list[tuple[bytes, Path]] = []

    original_verify = bound.verify_package_plan_binding

    def _verify_then_replace(raw: bytes) -> str:
        result = original_verify(raw)
        input_path.write_bytes(replacement_raw)
        return result

    def _delegate(*, raw: bytes, repo_root: Path) -> Path:
        observed.append((raw, repo_root))
        return expected_output

    monkeypatch.setattr(bound, "verify_package_plan_binding", _verify_then_replace)
    monkeypatch.setattr(bound, "run_construction_from_bytes", _delegate)

    result = bound.run_bound_construction(input_path=input_path, repo_root=tmp_path)
    assert result == expected_output
    assert input_path.read_bytes() == replacement_raw
    assert observed == [(original_raw, tmp_path)]
