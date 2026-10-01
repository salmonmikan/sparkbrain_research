"""Deterministic data-only packaging checks; no diagnostic execution."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/package_m1_checkpoint_compatibility_artifacts.py"
SPEC = importlib.util.spec_from_file_location("package_m1_compatibility", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)
PUBLISHED = ROOT / "artifacts/m1_checkpoint_compatibility_20261001"


@pytest.fixture(scope="module")
def retained() -> dict[str, bytes]:
    return TOOL.read_published(PUBLISHED)


def test_exact_published_transport_and_anchors_are_reproducible(retained) -> None:
    package = TOOL.build_package(retained, ROOT)
    assert len(package["run.tar.xz"]) == 34500
    assert TOOL.sha(package["run.tar.xz"]) == (
        "ae440c596046867aacc4ef5b72a3b1b1e3bd3bdeef10e6fced37e57030a192d8")
    assert package["anchors.json"] == (
        ROOT / "protocols/m1_checkpoint_compatibility_artifact_anchors_v1.json").read_bytes()
    for path in (PUBLISHED / "run.parts").iterdir():
        assert package["run.parts/" + path.name] == path.read_bytes()
    assert TOOL.build_package(dict(reversed(list(retained.items()))), ROOT) == package


def test_raw_and_published_routes_use_identical_bytes(retained, tmp_path: Path) -> None:
    for name, raw in retained.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    assert TOOL.read_raw(tmp_path) == retained


def test_existing_output_is_never_modified(retained, tmp_path: Path) -> None:
    sentinel = tmp_path / "sentinel"
    sentinel.write_bytes(b"unchanged")
    with pytest.raises(FileExistsError, match="no clobber"):
        TOOL.write_package(retained, tmp_path, ROOT)
    assert list(tmp_path.iterdir()) == [sentinel]
    assert sentinel.read_bytes() == b"unchanged"


def test_output_symlink_is_rejected(retained, tmp_path: Path) -> None:
    output = tmp_path / "link"
    output.symlink_to(tmp_path / "absent")
    with pytest.raises(FileExistsError, match="no clobber"):
        TOOL.write_package(retained, output, ROOT)
    assert not (tmp_path / "absent").exists()


def test_raw_symlink_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "link").symlink_to(SOURCE)
    with pytest.raises(ValueError, match="non-regular"):
        TOOL.read_raw(tmp_path)


@pytest.mark.parametrize("key", ["source_tree", "runtime_source_files_sha256", "runner_sha256"])
def test_coherently_changed_inventory_cannot_replace_git_provenance(retained, key: str) -> None:
    changed = dict(retained)
    started = json.loads(changed["STARTED.json"])
    started[key] = {} if key == "runtime_source_files_sha256" else "0" * 64
    changed["STARTED.json"] = TOOL.formatted(started)
    changed["inventory.json"] = TOOL.formatted({
        name: TOOL.sha(raw) for name, raw in changed.items() if name != "inventory.json"})
    with pytest.raises(ValueError, match="source tree|source manifest|execution input/source"):
        TOOL.build_package(changed, ROOT)


def test_corrupt_raw_inventory_is_rejected(retained) -> None:
    changed = dict(retained)
    changed["summary.json"] += b" "
    with pytest.raises(ValueError, match="inventory"):
        TOOL.build_package(changed, ROOT)


def test_packager_cli_and_repacked_verifier_import_no_runtime(tmp_path: Path) -> None:
    output = tmp_path / "package"
    code = (
        "import builtins,runpy,sys; original=builtins.__import__; "
        "exec(\"def guard(name,*a,**k):\\n"
        " if name.startswith('sparkbrain'): raise AssertionError(name)\\n"
        " return original(name,*a,**k)\"); "
        "builtins.__import__=guard; sys.argv=" + repr([
            str(SOURCE), "--published", str(PUBLISHED), "--output", str(output)]) + ";"
        "runpy.run_path(" + repr(str(SOURCE)) + ",run_name='__main__');"
        "scope=runpy.run_path(" + repr(str(
            ROOT / "scripts/verify_m1_checkpoint_compatibility_artifacts.py")) + ");"
        "scope['verify'](" + repr(str(output)) + ")"
    )
    # verify accepts a Path, so construct it in the isolated interpreter.
    code = code.replace("scope['verify'](" + repr(str(output)) + ")",
                        "scope['verify'](__import__('pathlib').Path(" + repr(str(output)) + "))")
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["model_executed"] is False
