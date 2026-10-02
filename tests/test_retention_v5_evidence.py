"""Model-free preservation checks; no runtime or study baseline evaluation."""
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "retention_v5_preservation", ROOT / "scripts/verify_retention_v5_evidence.py"
)
assert SPEC and SPEC.loader
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def test_all_preserved_bytes_and_frozen_sources_verify():
    result = V.verify()
    assert result["archive_files"] == 521
    assert result["run_files"] == 315
    assert result["runtime_model_method_calls"] == 0


def test_modified_transport_archive_pin_is_rejected(tmp_path):
    transport = json.loads((V.PACKAGE / "transport_manifest.json").read_text())
    transport["archive_sha256"] = "0" * 64
    (tmp_path / "transport_manifest.json").write_text(json.dumps(transport))
    with pytest.raises(ValueError, match="independent transport binding: archive_sha256"):
        V.verify(tmp_path)


def test_corrupted_part_is_rejected(tmp_path):
    shutil.copyfile(V.PACKAGE / "transport_manifest.json", tmp_path / "transport_manifest.json")
    (tmp_path / "evidence-000.b64").write_text("corrupted\n")
    with pytest.raises(ValueError, match="transport part hash"):
        V.verify(tmp_path)


def test_extraction_refuses_existing_destination(tmp_path):
    with pytest.raises(ValueError, match="extraction no clobber"):
        V.verify(extract=tmp_path)


@pytest.mark.parametrize("key,value", [
    ("source_commit", "0" * 40),
    ("terminal_sha256", "0" * 64),
    ("execution_manifest_sha256", "0" * 64),
    ("raw_run_files", 0),
    ("scientific_credit", False),
])
def test_transport_provenance_and_types_are_independently_bound(tmp_path, key, value):
    transport = json.loads((V.PACKAGE / "transport_manifest.json").read_text())
    transport[key] = value
    (tmp_path / "transport_manifest.json").write_text(json.dumps(transport))
    with pytest.raises(ValueError, match="independent transport binding"):
        V.verify(tmp_path)


def test_fresh_extraction_preserves_all_pinned_bytes(tmp_path):
    destination = tmp_path / "fresh"
    result = V.verify(extract=destination)
    inventory = json.loads((destination / "preservation-manifest.json").read_text())
    assert len(inventory) + 1 == result["archive_files"]
    assert all(V.sha((destination / name).read_bytes()) == pin for name, pin in inventory.items())


@pytest.mark.parametrize("target_exists", [False, True])
def test_extraction_refuses_live_and_dangling_symlink(tmp_path, target_exists):
    target = tmp_path / "target"
    if target_exists:
        target.mkdir()
        (target / "marker").write_text("unchanged")
    destination = tmp_path / "link"
    destination.symlink_to(target, target_is_directory=True)
    with pytest.raises(ValueError, match="extraction no clobber"):
        V.verify(extract=destination)
    if target_exists:
        assert list(target.iterdir()) == [target / "marker"]
        assert (target / "marker").read_text() == "unchanged"
    else:
        assert not target.exists()


def test_archive_preservation_is_independent_of_later_checkout_changes(monkeypatch, tmp_path):
    monkeypatch.setattr(V, "ROOT", tmp_path)
    assert V.verify()["current_source_files_verified"] == 0
    with pytest.raises(ValueError, match="current audit source mismatch"):
        V.verify(check_current_sources=True)


def test_explicit_source_preflight_accepts_extracted_frozen_snapshot(monkeypatch, tmp_path):
    destination = tmp_path / "archive"
    V.verify(extract=destination)
    monkeypatch.setattr(V, "ROOT", destination / "frozen-sources")
    assert V.verify(check_current_sources=True)["current_source_files_verified"] == 198
