from __future__ import annotations

import json
import tomllib
from pathlib import Path

import sparkbrain

ROOT = Path(__file__).resolve().parents[1]


def test_v03_package_keeps_the_v02_persisted_schema_boundary() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == "0.3.1"
    assert sparkbrain.__version__ == "0.3.1"
    assert sparkbrain.SCHEMA_VERSION == "0.2"


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
