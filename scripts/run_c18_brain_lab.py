"""C18 runner. The preregistration starts disabled and fails closed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v03_integration import V03TraceSession, replay_checkpoint


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c18_brain_lab/preregistration.json"


def load_protocol(path: Path, *, require_enabled: bool) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("protocol_id") != "c18-trace-checkpoint-brain-lab-v1":
        raise RuntimeError("unexpected C18 protocol")
    if require_enabled and not value.get("runner_execution_allowed"):
        raise RuntimeError("C18 runner remains disabled")
    return value


def build_cases(seed: int) -> tuple[dict, dict, dict]:
    """Build a deterministic C18 inspection case without calling the v0.2 engine."""
    session = V03TraceSession(config={"seed": seed, "mode": "v03_reference"})
    evidence = {
        "ev:vision": {"source_id": "vision", "entity": "object:a", "polarity": "support"},
        "ev:audio": {"source_id": "audio", "entity": "object:a", "polarity": "support"},
    }
    session.record(
        "sensory_accepted",
        {"sample_id": "sample:vision", "salience_terms": {"novelty": 0.8, "goal": 0.0, "habituation": 0.1}},
        {"evidence": {"ev:vision": evidence["ev:vision"]}},
    )
    session.record(
        "sensory_suppressed",
        {"sample_id": "sample:repeat", "salience_terms": {"novelty": 0.0, "goal": 0.0, "habituation": 0.8}},
        {},
    )
    session.record(
        "evidence_added",
        {"evidence_id": "ev:audio", "cited_evidence_ids": ["ev:vision"]},
        {"evidence": evidence},
    )
    session.record(
        "coalition_evaluated",
        {"cited_evidence_ids": ["ev:vision", "ev:audio"], "score_components": {"support": 1.0, "contradiction": 0.0, "stability": 1.0}},
        {"beliefs": {"object:a": {"winner": "cat", "residual_losers": ["toy"]}}},
    )
    session.record(
        "workspace_broadcast",
        {"cited_evidence_ids": ["ev:vision", "ev:audio"], "entity": "object:a", "hypothesis": "cat"},
        {},
    )
    checkpoint = session.checkpoint("checkpoint:primary")
    if replay_checkpoint(checkpoint) != checkpoint.state_hash:
        raise RuntimeError("C18 replay hash mismatch")
    child = session.fork(checkpoint, branch_id="fork:remove-audio", intervention={"kind": "remove_evidence", "evidence_id": "ev:audio"})
    child_evidence = child.inspect()["evidence"]
    child_evidence.pop("ev:audio")
    child.record("evidence_removed", {"evidence_id": "ev:audio", "cited_evidence_ids": []}, {"evidence": child_evidence})
    child.record("no_ignition", {"reason": "insufficient_sources", "cited_evidence_ids": ["ev:vision"]}, {"beliefs": {"object:a": {"winner": None, "residual_losers": ["cat", "toy"]}}})
    return (
        {"seed": seed, "checkpoint": checkpoint.as_dict(), "replay_state_hash": replay_checkpoint(checkpoint)},
        {"parent_checkpoint": checkpoint.checkpoint_id, "branch_id": child.branch_id, "trace": [event.as_dict() for event in child.events], "state_hash": child.state_hash()},
        {"checkpoint": checkpoint.as_dict(), "fork": [event.as_dict() for event in child.events]},
    )


def _canonical(value: object) -> str:
    return json.dumps(value, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_artifacts(output: Path, *, seed: int) -> dict:
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("C18 output must be new or empty")
    replay, intervention, export = build_cases(seed)
    output.mkdir(parents=True, exist_ok=True)
    static = output / "screenshots_or_static_exports"
    static.mkdir(exist_ok=False)
    protocol = load_protocol(ROOT / PROTOCOL_RELATIVE, require_enabled=True)
    values = {
        "preregistration.json": protocol,
        "replay_cases.json": replay,
        "intervention_cases.json": intervention,
        "checkpoint_manifest.json": {"checkpoint_hash": replay["checkpoint"]["state_hash"], "schema_version": "0.3"},
    }
    for name, value in values.items():
        (output / name).write_text(_canonical(value) + "\n", encoding="utf-8", newline="\n")
    (output / "report.md").write_text(
        "# C18 trace/checkpoint/Brain Lab artifact\n\n"
        "Engineering result: accepted deterministic contract smoke artifact.\n\n"
        "Scientific result: not_supported; this artifact establishes observability and replay only.\n",
        encoding="utf-8",
        newline="\n",
    )
    static_html = """<!doctype html><meta charset=\"utf-8\"><title>SparkBrain C18 Brain Lab</title>
<h1>SparkBrain C18 Brain Lab static export</h1><p>Local static export; no external assets or inferred state.</p>
<pre id=\"trace\"></pre><script>document.getElementById('trace').textContent=%s;</script>""" % json.dumps(
        _canonical(export), ensure_ascii=False
    )
    (static / "brain_lab.html").write_text(static_html, encoding="utf-8", newline="\n")
    return {"engineering_status": "accepted", "scientific_status": "not_supported", "state_hash": replay["checkpoint"]["state_hash"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", default=1801, type=int)
    args = parser.parse_args()
    print(_canonical(write_artifacts(args.output, seed=args.seed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
