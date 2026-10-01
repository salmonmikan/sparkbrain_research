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
    package = TOOL.build_package(retained)
    assert len(package["run.tar.xz"]) == 34500
    assert TOOL.sha(package["run.tar.xz"]) == (
        "ae440c596046867aacc4ef5b72a3b1b1e3bd3bdeef10e6fced37e57030a192d8")
    assert package["anchors.json"] == (
        ROOT / "protocols/m1_checkpoint_compatibility_artifact_anchors_v1.json").read_bytes()
    for path in (PUBLISHED / "run.parts").iterdir():
        assert package["run.parts/" + path.name] == path.read_bytes()
    assert TOOL.build_package(dict(reversed(list(retained.items())))) == package


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
def test_coherently_changed_inventory_cannot_replace_frozen_provenance(retained, key: str) -> None:
    changed = dict(retained)
    started = json.loads(changed["STARTED.json"])
    started[key] = {} if key == "runtime_source_files_sha256" else "0" * 64
    changed["STARTED.json"] = TOOL.formatted(started)
    changed["inventory.json"] = TOOL.formatted({
        name: TOOL.sha(raw) for name, raw in changed.items() if name != "inventory.json"})
    with pytest.raises(ValueError, match="external evidence anchor"):
        TOOL.build_package(changed)


def test_corrupt_raw_inventory_is_rejected(retained) -> None:
    changed = dict(retained)
    changed["summary.json"] += b" "
    with pytest.raises(ValueError, match="external evidence anchor"):
        TOOL.build_package(changed)


def test_packager_cli_and_repacked_verifier_import_no_runtime(tmp_path: Path) -> None:
    output = tmp_path / "package"
    code = (
        "import builtins,runpy,sys,subprocess; original=builtins.__import__; "
        "exec(\"def no_process(*a,**k):\\n raise AssertionError('subprocess forbidden')\"); "
        "subprocess.Popen=no_process; "
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


@pytest.mark.parametrize("path", ["summary.json", "cases/C01/result.json",
                                  "cases/C10/primary-result.json"])
def test_coherent_raw_edit_is_rejected_before_output_creation(
    retained, tmp_path: Path, path: str,
) -> None:
    changed = dict(retained)
    changed[path] += b" "
    changed["inventory.json"] = TOOL.formatted({
        name: TOOL.sha(raw) for name, raw in changed.items() if name != "inventory.json"})
    output = tmp_path / "must-not-exist"
    with pytest.raises(ValueError, match="external evidence anchor"):
        TOOL.write_package(changed, output)
    assert not output.exists()


def test_optional_git_audit_remains_fail_closed(retained, monkeypatch: pytest.MonkeyPatch) -> None:
    def unavailable(*args):
        raise RuntimeError("frozen Git objects unavailable")

    monkeypatch.setattr(TOOL, "git_bytes", unavailable)
    with pytest.raises(RuntimeError, match="Git objects unavailable"):
        TOOL.build_package(retained, ROOT)


def test_external_anchor_replacement_is_rejected(retained, monkeypatch: pytest.MonkeyPatch,
                                                tmp_path: Path) -> None:
    verifier = TOOL.verifier()
    replaced = tmp_path / "anchor.json"
    replaced.write_bytes(verifier.ANCHORS.read_bytes() + b" ")
    monkeypatch.setattr(verifier, "ANCHORS", replaced)
    monkeypatch.setattr(TOOL, "verifier", lambda: verifier)
    with pytest.raises(ValueError, match="external anchor"):
        TOOL.build_package(retained)


@pytest.mark.parametrize("kind", ["--raw", "--published"])
@pytest.mark.parametrize("route", ["child", "symlink", "normalized"])
def test_cli_rejects_input_output_overlap_without_touching_input(
    tmp_path: Path, kind: str, route: str,
) -> None:
    source = tmp_path / "retained"
    source.mkdir()
    sentinel = source / "untouched"
    sentinel.write_bytes(b"original")
    if route == "symlink":
        alias = tmp_path / "alias"
        alias.symlink_to(source, target_is_directory=True)
        output = alias / "package"
    elif route == "normalized":
        output = source / "unused" / ".." / "package"
    else:
        output = source / "package"
    result = subprocess.run([sys.executable, str(SOURCE), kind, str(source),
                             "--output", str(output)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "input and output must not overlap" in result.stderr
    assert list(source.iterdir()) == [sentinel]
    assert sentinel.read_bytes() == b"original"
    assert not output.exists()


def test_disjoint_path_check_rejects_equal_and_ancestor(tmp_path: Path) -> None:
    source = tmp_path / "raw"
    source.mkdir()
    for output in (source, tmp_path):
        with pytest.raises(ValueError, match="must not overlap"):
            TOOL.require_disjoint_paths(source, output)
    TOOL.require_disjoint_paths(source, tmp_path / "sibling")
    TOOL.require_disjoint_paths(source, source / ".." / "sibling")


def test_resolved_disjoint_output_does_not_create_intermediate_raw_directory(
    retained, tmp_path: Path,
) -> None:
    source = tmp_path / "retained"
    for name, raw in retained.items():
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    output = source / "must-not-be-created" / ".." / ".." / "repacked"
    result = subprocess.run([sys.executable, str(SOURCE), "--raw", str(source),
                             "--output", str(output)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert not (source / "must-not-be-created").exists()
    assert TOOL.read_raw(source) == retained
    assert (tmp_path / "repacked/run.tar.xz").is_file()
