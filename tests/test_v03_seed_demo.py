from __future__ import annotations

import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v03_seed_demo_emits_strict_json_schema(capsys) -> None:
    runpy.run_path(str(ROOT / "examples/v03_seed_demo.py"), run_name="__main__")
    payload = json.loads(capsys.readouterr().out)

    assert set(payload) == {
        "sensory_trace",
        "concept_candidates",
        "coalition_first",
        "coalition_second",
    }
    assert len(payload["sensory_trace"]) == 5
    for row in payload["sensory_trace"]:
        assert set(row) == {"time", "value", "sparks", "state"}
        assert isinstance(row["time"], int)
        assert isinstance(row["value"], float)
        assert isinstance(row["sparks"], list)
        assert isinstance(row["state"], dict)
        assert set(row["state"]) == {
            "prediction",
            "variability",
            "habituation",
            "threshold",
            "initialized",
            "last_value",
            "last_time",
        }
        assert isinstance(row["state"]["initialized"], bool)
    assert payload["concept_candidates"]
    for row in payload["concept_candidates"]:
        assert set(row) == {"id", "members", "strength", "reuse_count"}
        assert isinstance(row["id"], str)
        assert isinstance(row["members"], list)
        assert isinstance(row["strength"], float)
        assert isinstance(row["reuse_count"], int)
    assert set(payload["coalition_first"]) == {"ignited", "reason"}
    assert isinstance(payload["coalition_first"]["ignited"], bool)
    assert isinstance(payload["coalition_first"]["reason"], str)
    assert set(payload["coalition_second"]) == {
        "ignited",
        "belief",
        "reason",
        "supports",
    }
    assert isinstance(payload["coalition_second"]["ignited"], bool)
    assert isinstance(payload["coalition_second"]["belief"], str)
    assert isinstance(payload["coalition_second"]["reason"], str)
    assert isinstance(payload["coalition_second"]["supports"], list)
