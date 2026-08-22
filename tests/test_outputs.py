from __future__ import annotations

import json

from sparkbrain.visualizer import write_trace, write_visualizer
from sparkbrain.worlds import SwitchWorld, run_scenario


def test_visualizer_and_trace_are_self_contained(tmp_path) -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario())
    trace_path = write_trace(brain, tmp_path / "trace.json")
    html_path = write_visualizer(brain, tmp_path / "visualizer.html")

    payload = json.loads(trace_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")
    assert len(payload["frames"]) == 7
    assert "SparkBrain Visualizer" in html
    assert "__PAYLOAD__" not in html
    assert "plastic_seam" in html
