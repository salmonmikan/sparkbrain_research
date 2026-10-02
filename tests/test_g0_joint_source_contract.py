"""Model-free tests for the prospective G0 static source registry."""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/verify_g0_joint_source_contract.py"
SPEC = importlib.util.spec_from_file_location("g0_source_contract", SOURCE)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


@pytest.fixture
def copied_sources(tmp_path):
    contract = json.loads((ROOT / AUDIT.CONTRACT).read_text())
    for path in [AUDIT.CONTRACT, *contract["runtime_sources_sha256"],
                 *contract["runtime_schema_sha256"], *contract["reuse_sources_sha256"]]:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    return tmp_path


def test_exact_static_source_inventory():
    result = AUDIT.verify()
    assert result["source_files"] == 28
    assert result["class_witnesses"] == 101
    assert result["runtime_python_files"] == 157
    assert result["runtime_schema_files"] > 0
    assert result["reuse_source_files"] == 1
    assert result["runtime_execution_authorized"] is False
    assert result["scientific_credit"] == 0


@pytest.mark.parametrize("change", ["remove_class", "remove_file", "authorize", "credit"])
def test_contract_cannot_be_reduced_or_promoted(copied_sources, change):
    path = copied_sources / AUDIT.CONTRACT
    contract = json.loads(path.read_text())
    if change == "remove_class":
        next(iter(contract["files"].values()))["classes"].popitem()
    elif change == "remove_file":
        contract["files"].popitem()
    elif change == "authorize":
        contract["runtime_execution_authorized"] = True
    else:
        contract["scientific_credit"] = 1
    path.write_text(json.dumps(contract))
    with pytest.raises(ValueError, match="contract digest"):
        AUDIT.verify(copied_sources)


def test_source_drift_rejected(copied_sources):
    path = copied_sources / "src/sparkbrain/v032/runtime.py"
    path.write_text(path.read_text() + "\n# altered\n")
    with pytest.raises(ValueError, match="runtime dependency inventory"):
        AUDIT.verify(copied_sources)


def test_source_symlink_escape_rejected(copied_sources, tmp_path_factory):
    path = copied_sources / "src/sparkbrain/v032/runtime.py"
    external = tmp_path_factory.mktemp("outside") / "runtime.py"
    shutil.copyfile(path, external)
    path.unlink()
    path.symlink_to(external)
    with pytest.raises(ValueError, match="runtime dependency symlink"):
        AUDIT.verify(copied_sources)


def test_runtime_directory_symlink_cannot_hide_uninventoried_python(
    copied_sources, tmp_path_factory
):
    external = tmp_path_factory.mktemp("hidden_module")
    (external / "__init__.py").write_text("# hidden Python source\n")
    (copied_sources / "src/sparkbrain/hidden").symlink_to(external, target_is_directory=True)
    with pytest.raises(ValueError, match="runtime dependency symlink"):
        AUDIT.verify(copied_sources)


@pytest.mark.parametrize("directory", ["src/sparkbrain", "src", "schemas"])
def test_inventory_roots_and_ancestors_cannot_be_aliased(copied_sources, directory):
    original = copied_sources / directory
    relocated = copied_sources / "relocated_source"
    original.rename(relocated)
    original.symlink_to(relocated, target_is_directory=True)
    with pytest.raises(ValueError, match="runtime dependency symlink"):
        AUDIT.verify(copied_sources)


@pytest.mark.parametrize("relative", [
    "scripts/v05_acquired_ownership_probe.py", "scripts",
    AUDIT.CONTRACT, "artifacts/research",
])
def test_reuse_and_contract_files_and_ancestors_reject_aliases(copied_sources, relative):
    original = copied_sources / relative
    relocated = copied_sources / "relocated_dependency"
    is_directory = original.is_dir()
    original.rename(relocated)
    original.symlink_to(relocated, target_is_directory=is_directory)
    with pytest.raises(ValueError, match="symlink is unsupported"):
        AUDIT.verify(copied_sources)


@pytest.mark.parametrize("ancestor", [False, True])
def test_source_root_and_absolute_ancestor_aliases_reject(
    copied_sources, tmp_path_factory, ancestor
):
    alias = tmp_path_factory.mktemp("root_alias") / "alias"
    target = copied_sources.parent if ancestor else copied_sources
    alias.symlink_to(target, target_is_directory=True)
    supplied = alias / copied_sources.name if ancestor else alias
    with pytest.raises(ValueError, match="source root symlink"):
        AUDIT.verify(supplied)
    from scripts.g0_joint_ownership import OwnershipError, SourceRegistry
    with pytest.raises(OwnershipError, match="source verification failed"):
        SourceRegistry.from_verified_source(supplied, ())


@pytest.mark.parametrize("relative", ["/absolute.py", "../parent.py"])
def test_public_confined_path_rejects_escape(copied_sources, relative):
    with pytest.raises(ValueError, match="escapes root"):
        AUDIT.confined_path(copied_sources, relative, "test")


@pytest.mark.parametrize("layout", ["missing", "regular_file", "fifo", "unknown"])
def test_source_path_error_categories_are_fail_closed(copied_sources, layout):
    if layout == "unknown":
        with pytest.raises(ValueError, match="unsupported path"):
            AUDIT.verify(None)
        with pytest.raises(ValueError, match="unsupported path"):
            AUDIT.confined_path(copied_sources, None, "test")
    elif layout == "missing":
        with pytest.raises(ValueError, match="unavailable"):
            AUDIT.verify(copied_sources / "missing")
    elif layout == "regular_file":
        with pytest.raises(ValueError, match="unsupported path kind"):
            AUDIT.verify(copied_sources / AUDIT.CONTRACT)
    else:
        if not hasattr(os, "mkfifo"):
            pytest.skip("platform lacks a native FIFO fixture")
        target = copied_sources / AUDIT.CONTRACT
        target.unlink()
        os.mkfifo(target)
        with pytest.raises(ValueError, match="unsupported path kind"):
            AUDIT.verify(copied_sources)


@pytest.mark.parametrize("metadata,platform,reason", [
    ({"st_mode": stat.S_IFDIR, "st_file_attributes": 0x400,
      "st_reparse_tag": 0xA0000003}, "nt", "reparse point"),
    ({"st_mode": stat.S_IFDIR, "st_file_attributes": 0x400,
      "st_reparse_tag": 0xDEADBEEF}, "nt", "reparse point"),
    ({"st_mode": stat.S_IFDIR}, "nt", "unsupported path metadata"),
    ({"st_mode": stat.S_IFDIR, "st_file_attributes": "unknown"},
     "nt", "unsupported path metadata"),
    ({"st_mode": stat.S_IFSOCK}, "posix", "unsupported path kind"),
])
def test_junction_unknown_reparse_and_metadata_categories(metadata, platform, reason):
    with pytest.raises(ValueError, match=reason):
        AUDIT.reject_alias_metadata(SimpleNamespace(**metadata), "test", platform)


def test_verified_binder_does_not_normalize_loaded_class_source_alias(
    copied_sources, monkeypatch
):
    from scripts.g0_joint_ownership import OwnershipError, SourceRegistry
    module_name = "sparkbrain.v032.runtime"
    impostor = type("IntegratedV032Brain", (), {"__module__": module_name})
    module = ModuleType(module_name)
    module.IntegratedV032Brain = impostor
    alias = copied_sources / "class_alias.py"
    alias.symlink_to(copied_sources / "src/sparkbrain/v032/runtime.py")
    module.__file__ = str(alias)
    monkeypatch.setitem(sys.modules, module_name, module)
    with pytest.raises(OwnershipError, match="source path is unavailable"):
        SourceRegistry.from_verified_source(copied_sources, (impostor,))


@pytest.mark.parametrize(
    "change", ["helper_drift", "schema_drift", "extra_source", "missing_source"]
)
def test_full_dependency_closure_not_only_selected_class_sources(copied_sources, change):
    if change == "helper_drift":
        path = copied_sources / "src/sparkbrain/v032/checkpoint.py"
        path.write_text(path.read_text() + "\n# altered non-class helper\n")
    elif change == "schema_drift":
        path = next((copied_sources / "schemas").glob("*.json"))
        path.write_text(path.read_text() + "\n")
    elif change == "extra_source":
        (copied_sources / "src/sparkbrain/unreviewed.py").write_text("# unexpected source\n")
    else:
        (copied_sources / "src/sparkbrain/v032/checkpoint.py").unlink()
    with pytest.raises(ValueError, match="runtime dependency inventory"):
        AUDIT.verify(copied_sources)


def test_ast_distinguishes_dict_and_slot_fields():
    classes = ast.parse("""
@dataclass(slots=True)
class Slot:
    one: int
class Dict:
    def __init__(self):
        self.one = 1
    def reset(self):
        self.two = 2
""").body
    assert AUDIT.class_spec(classes[0])["slot_fields"] == ["one"]
    assert AUDIT.class_spec(classes[0])["dict_fields"] == []
    assert AUDIT.class_spec(classes[1])["dict_fields"] == ["one", "two"]


def test_all_source_auditing_forbids_sparkbrain_import():
    program = """
import importlib.abc, runpy, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname == 'sparkbrain' or fullname.startswith('sparkbrain.'):
            raise AssertionError('model import forbidden: ' + fullname)
sys.meta_path.insert(0, Block())
runpy.run_path(sys.argv[1], run_name='__main__')
"""
    result = subprocess.run([sys.executable, "-B", "-c", program, str(SOURCE)],
                            capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["runtime_execution_authorized"] is False
