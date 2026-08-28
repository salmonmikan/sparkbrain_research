from __future__ import annotations

import json
import tomllib
from pathlib import Path

import pytest

import sparkbrain
from sparkbrain.release import required_preparation_files, validate_source_revision

ROOT = Path(__file__).resolve().parents[1]


def test_v03_package_keeps_the_v02_persisted_schema_boundary() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == "0.3.2.dev0"
    assert sparkbrain.__version__ == "0.3.2.dev0"
    assert sparkbrain.SCHEMA_VERSION == "0.2"


def test_v032_development_package_keeps_v031_release_evidence_boundary() -> None:
    required = required_preparation_files(ROOT)
    assert "artifacts/release/v0.3.1/evidence_map.json" in required
    assert "artifacts/release/v0.3.2/evidence_map.json" not in required


def test_v032_missing_v031_evidence_does_not_fall_back_to_v030(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'sparkbrain-research'\nversion = '0.3.2.dev0'\n",
        encoding="utf-8",
    )
    required = required_preparation_files(tmp_path)
    assert "artifacts/release/v0.3.1/evidence_map.json" in required
    assert "artifacts/release/v0.3/evidence_map.json" not in required


@pytest.mark.slow
@pytest.mark.reproduction
def test_pre_lfs_evidence_revision_resolves_through_the_audited_map() -> None:
    assert validate_source_revision(
        ROOT,
        {"source_revision": "b991d78dd81bd98cfe65e10dfb46db2c96b798be"},
        label="v0.3.1 evidence",
        independent_lineage=True,
    ) == []


def test_v03_trace_and_checkpoint_schemas_are_explicit_and_additive() -> None:
    trace = json.loads((ROOT / "schemas" / "trace-v0.3.schema.json").read_text(encoding="utf-8"))
    checkpoint = json.loads(
        (ROOT / "schemas" / "checkpoint-v0.3.schema.json").read_text(encoding="utf-8")
    )
    legacy_trace = json.loads(
        (ROOT / "schemas" / "trace-v0.2.schema.json").read_text(encoding="utf-8")
    )
    assert trace["properties"]["schema_version"]["const"] == "0.3"
    assert checkpoint["properties"]["schema_version"]["const"] == "0.3"
    assert legacy_trace["properties"]["schema_version"]["const"] == "0.2"


def test_v03_migration_and_claim_boundaries_are_release_documents() -> None:
    migration = (ROOT / "docs" / "V03_MIGRATION_AND_COMPATIBILITY.md").read_text(encoding="utf-8")
    claims = (ROOT / "docs" / "V03_CLAIM_BOUNDARIES_AND_RISKS.md").read_text(encoding="utf-8")
    assert "never automatically interpreted as schema 0.3" in migration
    assert "C06, C08, C17, or unintegrated C19" in migration
    assert "Mark C19 as blocked" in claims
    assert "never converted into a novelty or performance claim" in claims
