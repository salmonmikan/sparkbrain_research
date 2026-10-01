"""Data-only evidence checks; never rerun the allocated compatibility diagnostic."""
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

SOURCE = (Path(__file__).resolve().parents[1] /
          "scripts/verify_m1_checkpoint_compatibility_artifacts.py")
SPEC = importlib.util.spec_from_file_location("verify_m1_compatibility", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def test_retained_matrix_recalculates_without_a_runtime() -> None:
    result = TOOL.verify()
    assert result["primary_load_calls"] == 10
    assert result["direct_validation_calls"] == 13
    assert result["direct_validation_rejections"] == 1
    assert result["outer_boolean_schema_accepted"] is True
    assert result["scientific_credit"] == result["dynamics_transitions"] == 0


def test_transport_corruption_fails(tmp_path: Path) -> None:
    shutil.copytree(TOOL.DEFAULT, tmp_path / "copy")
    part = tmp_path / "copy/run.parts/part-000.b64"
    part.write_bytes(part.read_bytes() + b"A")
    with pytest.raises(ValueError, match="part digest"):
        TOOL.read_bundle(tmp_path / "copy")


def test_rewritten_archive_and_manifest_cannot_remove_worker_provenance(tmp_path: Path) -> None:
    files = TOOL.read_bundle(TOOL.DEFAULT)
    del files["cases/C09/STARTED.json"]
    files["inventory.json"] = TOOL.canonical({n: TOOL.sha(raw) for n, raw in files.items()
                                            if n != "inventory.json"})
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w:xz") as stream:
        for name, raw in files.items():
            entry = tarfile.TarInfo(name)
            entry.size = len(raw)
            stream.addfile(entry, io.BytesIO(raw))
    payload = archive.getvalue()
    parts = tmp_path / "run.parts"
    parts.mkdir()
    raw = base64.b64encode(payload)
    (parts / "part-000.b64").write_bytes(raw)
    (parts / "manifest.json").write_bytes(TOOL.canonical({
        "archive_bytes": len(payload), "archive_sha256": TOOL.sha(payload),
        "parts": [{"path": "part-000.b64", "sha256": TOOL.sha(raw)}],
    }))
    with pytest.raises(ValueError, match="frozen archive"):
        TOOL.read_bundle(tmp_path)


@pytest.mark.parametrize("path,key", [
    ("STARTED.json", "source_commit"),
    ("cases/C05/STARTED.json", "runner_sha256"),
    ("cases/C02/STARTED.json", "case_id"),
    ("cases/C04/primary-result.json", "returned"),
    ("cases/C10/result.json", "input_unchanged"),
    ("summary.json", "direct_reconstructions_completed_observed"),
])
def test_semantic_checks_independently_reject_inconsistent_records(
    monkeypatch: pytest.MonkeyPatch, path: str, key: str,
) -> None:
    files = TOOL.read_bundle(TOOL.DEFAULT)
    data = json.loads(files[path])
    data[key] = "tampered"
    files[path] = TOOL.canonical(data)
    # Exercise semantic checks independently of the preceding transport trust boundary.
    monkeypatch.setattr(TOOL, "read_bundle", lambda root: files)
    with pytest.raises(AssertionError):
        TOOL.verify()


def test_anchor_replacement_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "anchors.json"
    path.write_bytes(TOOL.ANCHORS.read_bytes() + b" ")
    monkeypatch.setattr(TOOL, "ANCHORS", path)
    with pytest.raises(ValueError, match="external anchor"):
        TOOL.anchors()


def test_optimized_python_does_not_disable_verification() -> None:
    result = subprocess.run([sys.executable, "-O", str(SOURCE)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "requires Python without -O" in result.stderr


def test_verifier_import_and_execution_do_not_import_sparkbrain() -> None:
    code = (
        "import builtins,runpy; original=builtins.__import__; "
        "exec(\"def guard(name,*a,**k):\\n"
        " if name.startswith('sparkbrain'): raise AssertionError(name)\\n"
        " return original(name,*a,**k)\"); "
        "builtins.__import__=guard; scope=runpy.run_path(" + repr(str(SOURCE)) +
        ");scope['verify']()"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def with_standalone_copies(tmp_path: Path) -> Path:
    root = tmp_path / "package"
    shutil.copytree(TOOL.DEFAULT, root)
    manifest = json.loads((root / "run.parts/manifest.json").read_bytes())
    payload = b"".join(base64.b64decode((root / "run.parts" / row["path"]).read_bytes())
                       for row in manifest["parts"])
    (root / "run.tar.xz").write_bytes(payload)
    (root / "anchors.json").write_bytes(TOOL.ANCHORS.read_bytes())
    return root


def test_all_emitted_package_representations_verify(tmp_path: Path) -> None:
    result = TOOL.verify(with_standalone_copies(tmp_path))
    assert result["status"] == "verified_without_runtime_execution"


@pytest.mark.parametrize("name", ["run.tar.xz", "anchors.json"])
@pytest.mark.parametrize("damage", ["truncated", "appended", "directory", "symlink"])
def test_optional_package_copies_cannot_hide_corruption(
    tmp_path: Path, name: str, damage: str,
) -> None:
    root = with_standalone_copies(tmp_path)
    path = root / name
    original = path.read_bytes()
    if damage == "truncated":
        path.write_bytes(original[:len(original) // 2])
    elif damage == "appended":
        path.write_bytes(original + b" ")
    else:
        path.unlink()
        if damage == "directory":
            path.mkdir()
        else:
            target = tmp_path / "copy"
            target.write_bytes(original)
            path.symlink_to(target)
    with pytest.raises(ValueError, match="standalone package copy"):
        TOOL.verify(root)
