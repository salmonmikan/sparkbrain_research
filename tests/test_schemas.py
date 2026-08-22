from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def _load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def test_generated_json_artifacts_match_versioned_schemas() -> None:
    artifacts = {
        "trace-v0.2.schema.json": "artifacts/demo/trace.json",
        "state-v0.2.schema.json": "artifacts/demo/checkpoint.json",
        "config-document-v0.2.schema.json": "artifacts/demo/config.json",
        "summary-v0.2.schema.json": "artifacts/demo/summary.json",
        "benchmark-v0.2.schema.json": "artifacts/benchmarks/benchmark_results.json",
    }
    for schema_name, artifact_path in artifacts.items():
        Draft202012Validator(_schema(schema_name)).validate(_load(artifact_path))

    config_schema = Draft202012Validator(_schema("config-v0.2.schema.json"))
    config_schema.validate(_load("artifacts/demo/config.json")["config"])
    config_schema.validate(_load("artifacts/demo/checkpoint.json")["config"])


def test_state_schema_requires_broadcast_listeners() -> None:
    schema = _schema("state-v0.2.schema.json")
    assert "broadcast_listeners" in schema["required"]

    checkpoint = _load("artifacts/demo/checkpoint.json")
    checkpoint.pop("broadcast_listeners")
    errors = list(Draft202012Validator(schema).iter_errors(checkpoint))
    assert any(error.validator == "required" for error in errors)
