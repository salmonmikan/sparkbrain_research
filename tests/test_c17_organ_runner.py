from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("c17_runner", ROOT / "scripts/run_c17_organs.py")
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def protocol():
    return json.loads((ROOT / runner.PROTOCOL_RELATIVE).read_text(encoding="utf-8"))


def test_disabled_preregistration_rejects_before_execution(tmp_path):
    with pytest.raises(RuntimeError, match="remains disabled"):
        runner._preflight(
            root=ROOT,
            protocol_path=ROOT / runner.PROTOCOL_RELATIVE,
            output=tmp_path / "out",
            source_commit="a" * 40,
        )
    assert not (tmp_path / "out").exists()


def test_frozen_fixture_hash_validator_and_tamper():
    value = protocol()
    runner._validate_fixture_hashes(value)
    value["fixtures"]["fixture_sha256_by_run_seed"]["4701"] = "0" * 64
    with pytest.raises(RuntimeError, match="fixture hash"):
        runner._validate_fixture_hashes(value)


def test_protected_hash_manifest_and_tamper(tmp_path):
    target = tmp_path / "protected.txt"
    target.write_bytes(b"protected")
    manifest = {target.name: hashlib.sha256(target.read_bytes()).hexdigest()}
    runner._validate_hash_manifest(tmp_path, manifest)
    target.write_bytes(b"tampered")
    with pytest.raises(RuntimeError, match="protected hash"):
        runner._validate_hash_manifest(tmp_path, manifest)


def test_source_scope_requires_exact_allowlist_and_clean_pin(tmp_path, monkeypatch):
    value = protocol()
    value["base_commit"] = "b" * 40
    expected = value["source_control"]["expected_source_and_test_paths"]
    for relative in expected:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"pinned")

    def git(root, *args):
        if args[:2] == ("diff", "--name-only") and args[2:] == ("b" * 40, "a" * 40):
            return "\n".join(expected)
        if args[:2] == ("diff", "--name-only"):
            return runner.PROTOCOL_RELATIVE
        if args[0] == "status":
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(runner, "_git", git)
    monkeypatch.setattr(runner, "_git_bytes", lambda *args: b"pinned")
    runner._validate_source_scope(tmp_path, value, "a" * 40)
    monkeypatch.setattr(runner, "_git", lambda *args: "src/unregistered.py")
    with pytest.raises(RuntimeError, match="allowlisted"):
        runner._validate_source_scope(tmp_path, value, "a" * 40)


def test_exact_nine_canonical_writer_and_zero_byte_jsonl(tmp_path):
    value = protocol()
    bundle = {
        name: (
            []
            if name.endswith(".jsonl")
            else "report\n"
            if name.endswith(".md")
            else {"z": 1, "a": 2}
        )
        for name in runner.EXPECTED_FILES
    }
    output = tmp_path / "bundle"
    runner._write_bundle(output, bundle)
    assert {path.name for path in output.iterdir()} == runner.EXPECTED_FILES
    assert (output / "candidate_discovery.jsonl").read_bytes() == b""
    for path in output.glob("*.json"):
        assert path.read_bytes() == (
            runner._canonical(json.loads(path.read_bytes())) + "\n"
        ).encode("utf-8")
    assert set(value["artifacts"]["exact_files"]) == runner.EXPECTED_FILES


def test_nonempty_output_fails_before_disabled_gate(tmp_path):
    output = tmp_path / "out"
    output.mkdir()
    marker = output / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    with pytest.raises(RuntimeError, match="new or empty"):
        runner._preflight(
            root=ROOT,
            protocol_path=ROOT / runner.PROTOCOL_RELATIVE,
            output=output,
            source_commit="a" * 40,
        )
    assert marker.read_text(encoding="utf-8") == "keep"


def test_failure_bundle_is_exact_nine_with_zero_success(monkeypatch):
    from sparkbrain.v03_organs import evaluation

    value = protocol()
    value["fixtures"]["run_seeds"] = [9901701]
    value["statistics"]["bootstrap_resamples"] = 5
    monkeypatch.setattr(
        evaluation,
        "_run_seed",
        lambda *args: (_ for _ in ()).throw(RuntimeError("reserved failure")),
    )
    bundle = evaluation.generate_bundle(value, "a" * 40)
    evaluation.validate_bundle(bundle, value, "a" * 40)
    acceptance = bundle["acceptance_matrix.json"]
    assert acceptance["engineering_status"] == "implementation_failure"
    assert acceptance["scientific_status"] == "not_evaluated_implementation_failure"
    assert acceptance["successful_seeds"] == []
    assert bundle["candidate_discovery.jsonl"] == []
    assert set(bundle) == runner.EXPECTED_FILES
