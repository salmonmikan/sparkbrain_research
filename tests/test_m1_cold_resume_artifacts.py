"""Data-only archive checks; never run the M1 diagnostic from CI."""
from __future__ import annotations

import base64
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "scripts/verify_m1_cold_resume_artifacts.py"
SPEC = importlib.util.spec_from_file_location("verify_m1_cold_resume_artifacts", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def test_retained_results_recalculate_without_runtime_execution() -> None:
    result = TOOL.verify(TOOL.DEFAULT)
    assert result["total_primary_commits"] == 198
    assert result["resumed_transitions"] == 96
    assert result["scientific_credit"] == 0


def test_transport_tampering_is_rejected(tmp_path: Path) -> None:
    source = TOOL.DEFAULT / "corrected.parts"
    dest = tmp_path / "parts"
    shutil.copytree(source, dest)
    part = dest / "part-000.b64"
    part.write_bytes(part.read_bytes() + b"A")
    with pytest.raises(ValueError, match="digest mismatch"):
        TOOL.read_bundle(dest, "corrected")


def retained_files(identity: str = "corrected") -> dict[str, bytes]:
    files, _ = TOOL.read_bundle(TOOL.DEFAULT / f"{identity}.parts", identity)
    return files


@pytest.mark.parametrize("removed", ["baseline/config.json", "observed.stdout",
                                     "restore-37-7/COMPLETED.json"])
def test_rewritten_archive_and_self_descriptions_cannot_remove_raw_files(
    tmp_path: Path, removed: str,
) -> None:
    files = retained_files()
    del files[removed]
    files["inventory.json"] = TOOL.canonical(
        {name: TOOL.sha(raw) for name, raw in files.items() if name != "inventory.json"})
    with pytest.raises(ValueError, match="frozen raw inventory"):
        TOOL.verify_inventory(files, TOOL.load_anchors()["attempts"]["corrected"])
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w:xz") as stream:
        for name, raw in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(raw)
            stream.addfile(info, io.BytesIO(raw))
    payload = archive.getvalue()
    part = base64.b64encode(payload)
    (tmp_path / "part-000.b64").write_bytes(part)
    (tmp_path / "manifest.json").write_bytes(TOOL.canonical({
        "archive_bytes": len(payload), "archive_sha256": TOOL.sha(payload),
        "parts": [{"path": "part-000.b64", "sha256": TOOL.sha(part)}],
    }))
    with pytest.raises(ValueError, match="frozen archive"):
        TOOL.read_bundle(tmp_path, "corrected")


def test_external_anchor_replacement_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    replacement = tmp_path / "anchors.json"
    replacement.write_bytes(TOOL.ANCHORS.read_bytes() + b" ")
    monkeypatch.setattr(TOOL, "ANCHORS", replacement)
    with pytest.raises(ValueError, match="anchors digest"):
        TOOL.load_anchors()


@pytest.mark.parametrize("identity", ["original", "corrected"])
@pytest.mark.parametrize("key", ["source_commit", "runner_sha256", "protocol_sha256",
                                 "python", "executable", "platform", "dependency_versions",
                                 "scientific_credit", "protocol",
                                 "runtime_source_files_sha256", "schema_assets_sha256"])
def test_every_top_level_source_binding_is_checked(identity: str, key: str) -> None:
    files = retained_files(identity)
    started = json.loads(files["STARTED.json"])
    started[key] = "tampered"
    files["STARTED.json"] = TOOL.canonical(started)
    with pytest.raises(ValueError, match="top-level execution provenance"):
        TOOL.verify_provenance(files, identity)


@pytest.mark.parametrize("name", ["baseline", "observed", "secondary"] + [
    f"restore-{seed}-{cut}" for seed in (1, 37) for cut in (2, 7, 15)])
@pytest.mark.parametrize("identity", ["original", "corrected"])
def test_all_nine_worker_protocol_bindings_are_checked(identity: str, name: str) -> None:
    files = retained_files(identity)
    path = f"{name}/STARTED.json"
    started = json.loads(files[path])
    started["protocol_sha256"] = "0" * 64
    files[path] = TOOL.canonical(started)
    with pytest.raises(ValueError, match="worker execution provenance"):
        TOOL.verify_provenance(files, identity)


@pytest.mark.parametrize("key,value", [
    ("runner_sha256", "0" * 64), ("python", "another interpreter"),
    ("executable", "/other/python"), ("platform", "another platform"),
    ("mode", "baseline"), ("cut", 8), ("hashseed", "38"),
    ("reference_timeline", None), ("pid", True), ("parent_pid", 99999),
])
def test_worker_interpreter_and_mode_parameters_are_checked(key: str, value: object) -> None:
    files = retained_files()
    path = "restore-37-7/STARTED.json"
    started = json.loads(files[path])
    started[key] = value
    files[path] = TOOL.canonical(started)
    with pytest.raises(ValueError, match="provenance|identity"):
        TOOL.verify_provenance(files, "corrected")


def test_worker_configuration_is_bound_without_model_imports() -> None:
    files = retained_files()
    files["secondary/config.json"] += b" "
    with pytest.raises(ValueError, match="worker configuration"):
        TOOL.verify_provenance(files, "corrected")


def test_optimized_python_cannot_silently_disable_verification() -> None:
    result = subprocess.run([sys.executable, "-O", str(SOURCE)],
                            capture_output=True, text=True, check=False)
    assert result.returncode != 0
    assert "requires Python without -O" in result.stderr
