from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("c18_runner", ROOT / "scripts/run_c18_brain_lab.py")
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def test_disabled_and_tampered_source_fail_closed(tmp_path: Path) -> None:
    protocol = {
        "execution_base_commit": "4447c27eb7ac5f9a54f16a1e29552d3ae8c300d2",
        "protocol_id": "c18-trace-checkpoint-brain-lab-v6",
        "runner_execution_allowed": True,
        "source_commit": None,
        "source_control": {"expected_runtime_runner_and_test_paths": []},
    }
    protocol["runner_execution_allowed"] = False
    path = tmp_path / "disabled.json"
    path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(RuntimeError):
        runner.load_protocol(path, require_enabled=True)
    protocol["source_commit"] = "0" * 40
    with pytest.raises(RuntimeError):
        runner.preflight(protocol)


def test_v6_runner_defaults_to_the_preregistered_official_seed() -> None:
    parser = runner.argparse.ArgumentParser()
    parser.add_argument("--seed", default=1802, type=int)
    assert parser.parse_args([]).seed == 1802
    assert runner.PROTOCOL_RELATIVE.endswith("c18_brain_lab_v6/preregistration.json")


def test_write_artifacts_rejects_non_clean_room_before_protocol_read(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="clean room|source lineage"):
        runner.write_artifacts(tmp_path / "official", seed=1802)


def test_integration_allows_only_semantic_pin_amendment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    original = {"base_commit": "S", "runner_execution_allowed": False, "source_commit": None}
    original_raw = runner._canonical(original).encode("utf-8") + b"\n"
    original_hash = runner.hashlib.sha256(original_raw).hexdigest()
    original_sidecar = {"canonical_sha256": original_hash}
    original_sidecar_raw = runner._canonical(original_sidecar).encode() + b"\n"
    current = {**original, "runner_execution_allowed": True, "source_commit": "a" * 40}
    raw = runner._canonical(current).encode("utf-8") + b"\n"
    sidecar = {
        "canonical_raw_match": True,
        "canonical_sha256": runner.hashlib.sha256(raw).hexdigest(),
        "p_original_canonical_sha256": original_hash,
        "p_original_commit": runner.P_PREREGISTRATION_COMMIT,
        "p_original_raw_sha256": original_hash,
        "protocol": "preregistration.json",
        "raw_sha256": runner.hashlib.sha256(raw).hexdigest(),
    }
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    sidecar_path = tmp_path / runner.P_PREREGISTRATION_SIDECAR
    sidecar_path.parent.mkdir(parents=True)
    sidecar_path.write_text(runner._canonical(sidecar) + "\n", encoding="utf-8")
    monkeypatch.setattr(runner, "_git", lambda *_args: "blob")
    responses = iter((original_raw, original_sidecar_raw, raw, sidecar_path.read_bytes()))
    monkeypatch.setattr(runner, "_git_bytes", lambda *_args: next(responses))
    runner._require_integration_preregistration_amendment(current, raw)
    forged = {**current, "base_commit": "forged"}
    responses = iter((original_raw, original_sidecar_raw, raw, sidecar_path.read_bytes()))
    monkeypatch.setattr(runner, "_git_bytes", lambda *_args: next(responses))
    with pytest.raises(RuntimeError, match="unauthorized"):
        runner._require_integration_preregistration_amendment(forged, raw)
    sidecar["raw_sha256"] = "0" * 64
    sidecar_path.write_text(runner._canonical(sidecar) + "\n", encoding="utf-8")
    responses = iter((original_raw, original_sidecar_raw, raw, sidecar_path.read_bytes()))
    monkeypatch.setattr(runner, "_git_bytes", lambda *_args: next(responses))
    with pytest.raises(RuntimeError, match="stale or forged"):
        runner._require_integration_preregistration_amendment(current, raw)


def test_source_tree_hashes_are_exact_and_match_blobs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = ["one.py", "two.py"]
    contents = {"one.py": b"one", "two.py": b"two"}
    blobs = {"one.py": "a" * 40, "two.py": "b" * 40}
    for path, content in contents.items():
        (tmp_path / path).write_bytes(content)
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "_git", lambda _cmd, revision: blobs[revision.split(":", 1)[1]])
    monkeypatch.setattr(
        runner, "_git_bytes", lambda _cmd, revision: contents[revision.split(":", 1)[1]]
    )
    protocol = {"source_commit": "source", "source_tree_hashes": dict(blobs)}
    assert set(runner._require_source_tree_hashes(protocol, paths)) == set(paths)
    for bad in (
        {"one.py": blobs["one.py"]},
        {**blobs, "extra.py": "c" * 40},
        {"one.py": True, "two.py": blobs["two.py"]},
        {"one.py": "0" * 40, "two.py": blobs["two.py"]},
    ):
        with pytest.raises(RuntimeError):
            runner._require_source_tree_hashes(
                {"source_commit": "source", "source_tree_hashes": bad}, paths
            )
