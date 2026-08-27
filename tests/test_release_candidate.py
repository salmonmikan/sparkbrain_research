from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

import pytest

import sparkbrain.release_candidate as release_candidate
from sparkbrain.release_candidate import (
    CANDIDATE_MANIFEST_SCHEMA,
    PRIVATE_REVIEW_NOTICE,
    PRIVATE_REVIEW_NOTICE_NAME,
    RELEASE_GROUP_MANIFEST_NAME,
    REVIEW_MANIFEST_NAME,
    build_candidate_and_review_archives,
    build_canonical_reproduction_manifest,
    validate_candidate_archive,
    validate_canonical_reproduction_manifest,
    validate_network_client_boundary,
    validate_release_group,
    validate_review_bundle,
)


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def fixture(root: Path) -> str:
    (root / "src" / "sparkbrain").mkdir(parents=True)
    (root / "src" / "sparkbrain" / "runtime.py").write_text("import json\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "result.md").write_text("evidence\n", encoding="utf-8")
    git(root, "init", "--quiet")
    git(root, "config", "user.name", "fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "add", "--all")
    git(root, "commit", "--quiet", "-m", "fixture")
    return git(root, "rev-parse", "HEAD")


def test_manifest_uses_real_commit_and_rejects_bool_and_payload_drift(tmp_path: Path) -> None:
    revision = fixture(tmp_path)
    manifest = build_canonical_reproduction_manifest(
        tmp_path, source_revision=revision, paths=["docs/result.md"]
    )
    assert manifest["schema_version"] == CANDIDATE_MANIFEST_SCHEMA
    assert validate_canonical_reproduction_manifest(tmp_path, manifest) == []
    boolean = json.loads(json.dumps(manifest))
    boolean["file_count"] = True
    boolean["total_bytes"] = False
    boolean["files"][0]["size"] = True
    problems = validate_canonical_reproduction_manifest(tmp_path, boolean)
    assert "candidate manifest file_count mismatch" in problems
    assert "candidate manifest total_bytes mismatch" in problems
    assert any("size must be" in problem for problem in problems)

    tampered = json.loads(json.dumps(manifest))
    tampered["files"][0]["size"] = 1
    tampered["files"][0]["sha256"] = "0" * 64
    tampered["total_bytes"] = 1
    problems = validate_canonical_reproduction_manifest(tmp_path, tampered)
    assert any("size does not match Git blob" in problem for problem in problems)
    assert any("sha256 does not match Git blob" in problem for problem in problems)

    (tmp_path / "docs" / "result.md").write_text("drift\n", encoding="utf-8")
    problems = validate_canonical_reproduction_manifest(tmp_path, manifest)
    assert any("payload content is not bound" in problem for problem in problems)


@pytest.mark.parametrize(
    "source",
    [
        "import httpx\n",
        "__import__('socket')\n",
        "__import__('torch')\n",
        "import importlib\nimportlib.import_module('socket')\n",
        "import importlib\nimportlib.import_module('arbitrary_plugin')\n",
        "from importlib import import_module\nimport_module('socket')\n",
        "from builtins import __import__ as load\nload('socket')\n",
        "import importlib\nname = 'torch'\nimportlib.import_module(name)\n",
        "import importlib\nload = importlib.import_module\nload('socket')\n",
        "import importlib\ngetattr(importlib, 'import_module')('socket')\n",
        "__builtins__['__import__']('socket')\n",
        "import importlib as il\nload = il.import_module\nload('socket')\n",
        "import builtins as bi\nload = bi.__import__\nload('socket')\n",
        "import importlib as il\nload = getattr(il, 'import_module')\nload('unknown')\n",
        "name = '__import__'\n__builtins__[name]('torch')\n",
        "load = __builtins__['__import__']\nload('socket')\n",
        "from importlib import import_module as load\nalias = load\nalias('socket')\n",
        "import importlib\n(load := importlib.import_module)('socket')\n",
        "import importlib\n(load,) = (importlib.import_module,)\nload('socket')\n",
        "import importlib\n[[load]] = [[importlib.import_module]]\nload('socket')\n",
        "import importlib\ndef f(load=importlib.import_module):\n    load('socket')\n",
        "import importlib\ndef f(*, load=importlib.import_module):\n    load('socket')\n",
        "import importlib\nf = lambda load=importlib.import_module: load('socket')\n",
        "import importlib\n(load,) = [safe, importlib.import_module]\nload('torch')\n",
        "import importlib\n"
        "def f(load=importlib.import_module if flag else safe):\n"
        "    load('torch')\n",
        "import importlib\nload = importlib.import_module\nload('torch')\n",
        "import importlib as il\nload = il.import_module\nload('torch')\n",
        "import builtins as bi\nload = bi.__import__\nload('torch')\n",
        "load = __builtins__['__import__']\nload('torch')\n",
        "from importlib import import_module as load\nalias = load\nalias('torch')\n",
        "import importlib\n(load := importlib.import_module)('torch')\n",
        "import importlib\n(load,) = (importlib.import_module,)\nload('torch')\n",
        "import importlib\n[[load]] = [[importlib.import_module]]\nload('torch')\n",
        "import importlib\ndef f(load=importlib.import_module):\n    load('torch')\n",
        "import importlib\ndef f(*, load=importlib.import_module):\n    load('torch')\n",
        "import importlib\nf = lambda load=importlib.import_module: load('torch')\n",
        "import importlib\ndef f():\n    return importlib.import_module\n",
        "import importlib\nloaders = [importlib.import_module]\n",
        "import importlib\nloaders = [importlib.import_module for _ in values]\n",
        "import importlib\nclass Loader:\n    dynamic = importlib.import_module\n",
        "import importlib\nwrapper(importlib.import_module)\n",
        "import importlib\ndef f(importlib):\n    importlib.import_module('torch')\n",
        "from importlib import import_module as load\ndef f(load):\n    load('torch')\n",
        "import importlib\nimport fake as importlib\nimportlib.import_module('torch')\n",
        "from importlib import import_module as load\nimport fake as load\nload('torch')\n",
        "eval('1 + 1')\n",
        "exec('value = 1')\n",
        "compile('1 + 1', '<fixture>', 'eval')\n",
        "globals()\n",
        "locals()\n",
        "vars()\n",
        "import importlib\nimportlib.__getattribute__('import_module')('torch')\n",
        "import importlib\nimportlib.__dict__['import_module']('torch')\n",
        "import builtins\nbuiltins.__dict__['__import__']('torch')\n",
        "__builtins__.__getitem__('__import__')('torch')\n",
        "import importlib\nname = 'safe'\ngetattr(importlib, name)\n",
        "locals()['__' + 'import__']('torch')\n",
        "mapping['import_' + 'module']\n",
        "getattr(loader, '__' + 'import__')('torch')\n",
        "import sys\nsys.modules['builtins'].__dict__['__import__']('torch')\n",
        "import sys as system\nsystem.modules['builtins']\n",
        "from sys import modules as loaded\nloaded['builtins']\n",
        "import pkgutil\npkgutil.resolve_name('socket.socket')\n",
        "import pydoc\npydoc.locate('socket.socket')\n",
        "import runpy\nrunpy.run_module('socket')\n",
        "from zipimport import zipimporter\nzipimporter('payload.zip')\n",
        "import pkg_resources\n",
    ],
)
def test_network_boundary_scans_package_and_fails_closed(tmp_path: Path, source: str) -> None:
    fixture(tmp_path)
    (tmp_path / "src" / "sparkbrain" / "runtime.py").write_text(source, encoding="utf-8")
    assert validate_network_client_boundary(tmp_path)


def test_network_boundary_allows_actual_repo_function_local_static_torch_import(
    tmp_path: Path,
) -> None:
    fixture(tmp_path)
    allowed = tmp_path / "src" / "sparkbrain" / "evaluation" / "run_baselines.py"
    allowed.parent.mkdir()
    allowed.write_text(
        "def run():\n    import torch\n    return torch.tensor([1])\n", encoding="utf-8"
    )
    assert validate_network_client_boundary(tmp_path) == []


@pytest.mark.parametrize(
    "source",
    [
        "__import__('torch.nn')\n",
        "__import__('torch', globals(), locals(), [], 0)\n",
        "name = 'torch'\n__import__(name)\n",
        "import importlib\nimportlib.import_module('torch')\n",
        "from importlib import import_module as load\nload('torch')\n",
        "import importlib\ngetattr(importlib, 'import_module')('torch')\n",
        "__builtins__['__import__']('torch')\n",
        "import builtins as bi\nbi.__dict__['__import__']('torch')\n",
        "import importlib\n(load := importlib.import_module)('torch')\n",
        "import importlib\n(load,) = (importlib.import_module,)\nload('torch')\n",
        "import importlib\ndef f(load=importlib.import_module):\n    load('torch')\n",
    ],
)
def test_network_boundary_rejects_dynamic_import_in_previous_torch_path(
    tmp_path: Path, source: str
) -> None:
    fixture(tmp_path)
    allowed = tmp_path / "src" / "sparkbrain" / "evaluation" / "run_baselines.py"
    allowed.parent.mkdir()
    allowed.write_text(source, encoding="utf-8")
    assert validate_network_client_boundary(tmp_path)


def test_network_boundary_allows_only_audited_static_stdlib_imports(tmp_path: Path) -> None:
    fixture(tmp_path)
    external = tmp_path / "src" / "sparkbrain" / "external_validation"
    external.mkdir()
    (external / "belief_r.py").write_text("import urllib.request\n", encoding="utf-8")
    (external / "evaluation.py").write_text("import socket\n", encoding="utf-8")
    assert validate_network_client_boundary(tmp_path) == []

    (external / "belief_r.py").write_text("import urllib.request\nimport httpx\n", encoding="utf-8")
    assert validate_network_client_boundary(tmp_path)


def test_manifest_uses_git_blob_bytes_with_crlf_checkout(tmp_path: Path) -> None:
    (tmp_path / ".gitattributes").write_text("*.md text eol=crlf\n", encoding="ascii")
    revision = fixture(tmp_path)
    blob = subprocess.run(
        ["git", "show", f"{revision}:docs/result.md"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    ).stdout
    (tmp_path / "docs" / "result.md").write_bytes(blob.replace(b"\n", b"\r\n"))

    manifest = build_canonical_reproduction_manifest(
        tmp_path, source_revision=revision, paths=["docs/result.md"]
    )

    assert validate_canonical_reproduction_manifest(tmp_path, manifest) == []
    assert manifest["files"][0]["size"] == len(blob)
    assert manifest["files"][0]["sha256"] == hashlib.sha256(blob).hexdigest()


def test_build_rejects_bool_epoch_and_existing_destination(tmp_path: Path) -> None:
    root = tmp_path / "source"
    revision = fixture(root)
    with pytest.raises(ValueError, match="source_date_epoch must be an integer"):
        build_candidate_and_review_archives(
            root,
            source_revision=revision,
            paths=["docs/result.md"],
            release_directory=tmp_path / "bool-epoch",
            source_date_epoch=True,
        )

    destination = tmp_path / "existing"
    destination.mkdir()
    marker = destination / "marker.txt"
    marker.write_text("preserve\n", encoding="utf-8")
    with pytest.raises(ValueError, match="already exists"):
        build_candidate_and_review_archives(
            root,
            source_revision=revision,
            paths=["docs/result.md"],
            release_directory=destination,
            source_date_epoch=1_700_000_000,
        )
    assert marker.read_text(encoding="utf-8") == "preserve\n"


def test_candidate_review_and_group_validators_cross_bind_every_payload(tmp_path: Path) -> None:
    root = tmp_path / "source"
    revision = fixture(root)
    destination = tmp_path / "release"
    build_candidate_and_review_archives(
        root,
        source_revision=revision,
        paths=["docs/result.md"],
        release_directory=destination,
        source_date_epoch=1_700_000_000,
    )

    candidate = destination / "candidate.zip"
    review = destination / "review.zip"
    assert validate_candidate_archive(root, candidate) == []
    assert validate_review_bundle(root, review) == []
    assert validate_release_group(root, destination) == []

    with zipfile.ZipFile(review) as archive:
        review_manifest = json.loads(archive.read(REVIEW_MANIFEST_NAME))
        assert archive.read(PRIVATE_REVIEW_NOTICE_NAME) == PRIVATE_REVIEW_NOTICE
    assert review_manifest["license_status"] == "owner-decision-pending"
    assert review_manifest["source_revision"] == revision
    assert (destination / RELEASE_GROUP_MANIFEST_NAME).is_file()


def _rewrite_zip_member(path: Path, member: str, replacement: bytes) -> None:
    rewritten = path.with_suffix(".rewritten.zip")
    with zipfile.ZipFile(path) as source, zipfile.ZipFile(rewritten, "w") as output:
        for info in source.infolist():
            output.writestr(info, replacement if info.filename == member else source.read(info))
    path.unlink()
    rewritten.replace(path)


def test_archive_validators_reject_candidate_review_and_group_tampering(tmp_path: Path) -> None:
    root = tmp_path / "source"
    revision = fixture(root)
    destination = tmp_path / "release"
    build_candidate_and_review_archives(
        root,
        source_revision=revision,
        paths=["docs/result.md"],
        release_directory=destination,
        source_date_epoch=1_700_000_000,
    )

    candidate = destination / "candidate.zip"
    _rewrite_zip_member(candidate, "docs/result.md", b"tampered\n")
    assert any("mismatch" in problem for problem in validate_candidate_archive(root, candidate))
    assert any("mismatch" in problem for problem in validate_release_group(root, destination))

    review = destination / "review.zip"
    with zipfile.ZipFile(review) as archive:
        review_manifest = json.loads(archive.read(REVIEW_MANIFEST_NAME))
    review_manifest["source_revision"] = "0" * 40
    replacement = (json.dumps(review_manifest, sort_keys=True, indent=2) + "\n").encode()
    _rewrite_zip_member(review, REVIEW_MANIFEST_NAME, replacement)
    assert any(
        "source revision mismatch" in problem
        for problem in validate_review_bundle(root, review)
    )

    _rewrite_zip_member(review, "candidate.zip.sha256", b"0" * 64 + b"  candidate.zip\n")
    assert any("mismatch" in problem for problem in validate_review_bundle(root, review))
    assert any("mismatch" in problem for problem in validate_release_group(root, destination))

    group_path = destination / RELEASE_GROUP_MANIFEST_NAME
    group = json.loads(group_path.read_text(encoding="utf-8"))
    group["unexpected"] = True
    group_path.write_text(
        json.dumps(group, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    assert any(
        "fields do not match" in problem
        for problem in validate_release_group(root, destination)
    )


def test_publish_revalidates_after_rename_and_retracts_raced_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "source"
    revision = fixture(root)
    destination = tmp_path / "release"
    original_rename = release_candidate.os.rename

    def tampering_rename(source: str | Path, target: str | Path) -> None:
        candidate = Path(source) / "candidate.zip"
        candidate.write_bytes(candidate.read_bytes() + b"tamper")
        original_rename(source, target)

    monkeypatch.setattr(release_candidate.os, "rename", tampering_rename)
    with pytest.raises(ValueError, match="published release group validation failed"):
        build_candidate_and_review_archives(
            root,
            source_revision=revision,
            paths=["docs/result.md"],
            release_directory=destination,
            source_date_epoch=1_700_000_000,
        )
    assert not destination.exists()
    assert not list(tmp_path.glob(".candidate-release-staging-*"))


def test_publish_race_never_replaces_a_competing_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "source"
    revision = fixture(root)
    destination = tmp_path / "release"
    original_rename = release_candidate.os.rename

    def racing_rename(source: str | Path, target: str | Path) -> None:
        target_path = Path(target)
        target_path.mkdir()
        (target_path / "competing.txt").write_text("preserve\n", encoding="utf-8")
        original_rename(source, target)

    monkeypatch.setattr(release_candidate.os, "rename", racing_rename)
    with pytest.raises(OSError):
        build_candidate_and_review_archives(
            root,
            source_revision=revision,
            paths=["docs/result.md"],
            release_directory=destination,
            source_date_epoch=1_700_000_000,
        )
    assert (destination / "competing.txt").read_text(encoding="utf-8") == "preserve\n"
    assert not list(tmp_path.glob(".candidate-release-staging-*"))
