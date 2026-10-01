"""Frozen, non-evidentiary evaluation-clock diagnostic of the legacy engine."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, EventKind, Spark, SparkKind

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/experiments/exploratory/event_clock/protocol.json"
PROTOCOL_SHA256 = "778a37f8507879f6a84f68ce0d00980542cb59932aa9b321e98f15392f088ebc"


def canonical(value: Any) -> bytes:
    """Serialize without platform-dependent whitespace or nonfinite numbers."""
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return (text + "\n").encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_protocol(path: Path = PROTOCOL) -> dict[str, Any]:
    raw = path.read_bytes()
    if sha256(raw) != PROTOCOL_SHA256:
        raise ValueError("Frozen protocol bytes differ; use a new protocol")
    return json.loads(raw)


def verify_runtime(protocol: dict[str, Any]) -> dict[str, str]:
    result = {}
    for name, expected in protocol["runtime_git_blobs"].items():
        raw = (ROOT / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != expected:
            raise ValueError(f"Pinned runtime differs: {name}")
        result[name] = sha256(raw)
    return result


def cells(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    axes = ("evidence_strengths", "source_counts", "stability_evaluations",
            "temporal_coherence_bonuses", "padding_gaps")
    names = ("strength", "sources", "stability", "bonus", "gap")
    rows = []
    for values in itertools.product(*(protocol[axis] for axis in axes)):
        base = dict(zip(names, values, strict=True))
        rows.append({**base, "padding_count": 0, "padding_kind": "none"})
        for count in protocol["padding_counts"]:
            if count:
                rows.extend({**base, "padding_count": count, "padding_kind": kind}
                            for kind in protocol["padding_kinds"])
    return rows


def input_stream(cell: dict[str, Any], protocol: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for index, time in enumerate(protocol["evidence_times"]):
        rows.append({
            "phase": "evidence", "time": time, "kind": "stimulus", "source": "external",
            "target": "target", "strength": cell["strength"], "priority": 0,
            "evidence_id": f"genuine:{index}", "evidence_label": f"observation:{index}",
            "metadata": {"origin_kind": "external", "sensor": f"sensor:{index % cell['sources']}"},
        })
    for index in range(1, cell["padding_count"] + 1):
        kind = cell["padding_kind"]
        rows.append({
            "phase": "padding", "time": protocol["evidence_times"][-1] + cell["gap"] * index,
            "kind": "reward" if kind == "reward" else "propagation", "source": "padding",
            "target": None if kind == "reward" else f"padding:{kind}", "strength": 0.0,
            "priority": 10, "evidence_id": None, "evidence_label": None,
            "metadata": {"origin_kind": "internal"},
        })
    rows.append({
        "phase": "terminal_marker",
        "time": protocol["evidence_times"][-1] + max(protocol["padding_counts"]) * cell["gap"],
        "kind": "reward", "source": "terminal_marker", "target": None,
        "strength": 0.0, "priority": 10, "evidence_id": None, "evidence_label": None,
        "metadata": {"origin_kind": "internal"},
    })
    return [{"index": index, **row} for index, row in enumerate(rows)]


def make_brain(cell: dict[str, Any], protocol: dict[str, Any]) -> SparkBrain:
    config = BrainConfig(random_seed=protocol["random_seed"],
                         stability_evaluations=cell["stability"],
                         temporal_coherence_bonus=cell["bonus"])
    brain = SparkBrain(config)
    for spark_id, kind in (("target", SparkKind.HYPOTHESIS),
                           ("padding:hypothesis", SparkKind.HYPOTHESIS),
                           ("padding:sensory", SparkKind.SENSORY)):
        brain.add_spark(Spark(
            id=spark_id, label=spark_id, kind=kind, organ=f"organ:{spark_id}",
            competition_group=f"independent:{spark_id}",
            threshold=protocol["spark_threshold"], base_threshold=protocol["spark_threshold"],
            decay_tau=protocol["spark_decay_tau"],
        ))
    return brain


def observe(brain: SparkBrain, last_evaluation_time: float | None) -> dict[str, Any]:
    """Read state; never call a runtime evaluation or state-touching operation."""
    target = brain.sparks["target"]
    activation = target.activation * math.exp(-(brain.time - target.last_update) / target.decay_tau)
    records = [
        (record, math.exp(-(brain.time - record.time) / brain.config.support_tau))
        for record in target.supports.values()
    ]
    live = [(record, recency) for record, recency in records if recency >= 0.02]
    strength = sum(max(0.0, record.strength) * recency for record, recency in live)
    source_count = len({record.source for record, _ in live})
    stability = brain._stability.get("target", 0)
    return {
        "time": brain.time, "last_coalition_evaluation_time": last_evaluation_time,
        "stored_target_activation": target.activation, "target_last_update": target.last_update,
        "stored_coalitions": [asdict(item) for item in brain.last_coalitions],
        "target_stability": stability,
        "target_supports": {key: asdict(value) for key, value in target.supports.items()},
        "target_contradictions": {
            key: asdict(value) for key, value in target.contradictions.items()
        },
        "active_hypotheses": sorted(brain._active_hypotheses),
        "observer_only_projection": {
            "target_activation": activation, "target_support_strength": strength,
            "target_live_source_count": source_count,
            "target_score_without_reevaluation": max(0.0, activation) + 0.08 * strength
            + brain.config.diversity_bonus * max(0, source_count - 1)
            + brain.config.temporal_coherence_bonus * min(stability, 4),
        },
        "counters": asdict(brain.stats),
    }


def run_episode(cell: dict[str, Any], protocol: dict[str, Any]) -> dict[str, Any]:
    brain = make_brain(cell, protocol)
    graph = [asdict(spark) for spark in brain.sparks.values()]
    stream = input_stream(cell, protocol)
    observations, ignitions = [], []
    last_evaluation_time = None
    after_evidence = None
    for row in stream:
        event = {key: value for key, value in row.items() if key not in {"phase", "index"}}
        event["kind"] = EventKind(event["kind"])
        brain.schedule(**event)
        previous = len(brain.ignitions)
        brain.run()
        if row["kind"] != "reward" and row["target"] in {"target", "padding:hypothesis"}:
            last_evaluation_time = row["time"]
        before = canonical(brain.state_dict(include_trace=False))
        observation = observe(brain, last_evaluation_time)
        if canonical(brain.state_dict(include_trace=False)) != before:
            raise AssertionError("Observer changed runtime state")
        new = [{**asdict(item), "input_index": row["index"], "phase": row["phase"]}
               for item in brain.ignitions[previous:]]
        ignitions.extend(new)
        observations.append({"input_index": row["index"], **observation, "new_ignitions": new})
        if row["index"] == 1:
            after_evidence = observation
    assert after_evidence is not None
    final = observations[-1]
    first = ignitions[0] if ignitions else None
    pad_ignitions = [item for item in ignitions if item["phase"] == "padding"]
    pad_first = bool(first and first["phase"] == "padding")
    metrics = {
        "pre_padding_ignition_count": sum(item["phase"] == "evidence" for item in ignitions),
        "post_padding_first_ignition": pad_first,
        "first_ignition_time": first["time"] if first else None,
        "first_ignition_input_index": first["input_index"] if first else None,
        "first_ignition_phase": first["phase"] if first else None,
        "target_stability_after_evidence": after_evidence["target_stability"],
        "target_stability_at_end": final["target_stability"],
        "target_support_count": len(final["target_supports"]),
        "target_source_count": len({r["source"] for r in final["target_supports"].values()}),
        "ignition_count": len(ignitions),
        "post_padding_repeat_ignition_count": len(pad_ignitions) - int(pad_first),
        "target_activation_projected_at_horizon":
            final["observer_only_projection"]["target_activation"],
        "target_support_strength_projected_at_horizon":
            final["observer_only_projection"]["target_support_strength"],
        **{name: final["counters"][name]
           for name in ("events_processed", "spark_updates", "fires", "edge_evaluations")},
    }
    if not set(protocol["primary_metrics"] + protocol["secondary_metrics"]) <= metrics.keys():
        raise AssertionError("Registered metric missing")
    for observation in observations[2:]:
        if observation["target_supports"] != after_evidence["target_supports"]:
            raise AssertionError("Padding changed genuine evidence")
        if "padding:hypothesis" in observation["active_hypotheses"]:
            raise AssertionError("Empty padding hypothesis survived expiry")
    return {
        "cell": cell, "config": asdict(brain.config), "initial_sparks": graph,
        "connections": [], "broadcast_listeners": [], "inputs": stream,
        "genuine_input_sha256": sha256(canonical(stream[:2])),
        "observations": observations, "ignitions": ignitions, "metrics": metrics,
        "final_workspace": [asdict(item) for item in brain.workspace],
        "final_coalitions": [asdict(item) for item in brain.last_coalitions],
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        condition = {key: value for key, value in row["cell"].items()
                     if key not in {"padding_count", "padding_kind"}}
        groups.setdefault(canonical(condition).decode().strip(), []).append(row)
    contrasts = []
    for condition, group in sorted(groups.items()):
        arms = {(r["cell"]["padding_kind"], r["cell"]["padding_count"]): r for r in group}
        for count in (1, 2, 4):
            treatment = arms[("hypothesis", count)]
            for kind in ("sensory", "reward"):
                control = arms[(kind, count)]
                contrasts.append({
                    "condition": json.loads(condition), "padding_count": count,
                    "control": kind,
                    "genuine_inputs_identical": treatment["inputs"][:2] == control["inputs"][:2],
                    "final_time_identical": treatment["observations"][-1]["time"]
                    == control["observations"][-1]["time"],
                    "event_counts_identical": treatment["metrics"]["events_processed"]
                    == control["metrics"]["events_processed"],
                    "hypothesis_padding_first_ignition":
                        treatment["metrics"]["post_padding_first_ignition"],
                    "control_padding_first_ignition":
                        control["metrics"]["post_padding_first_ignition"],
                })
    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY", "episode_count": len(rows),
        "all_cell_metrics": [{"cell": row["cell"], "metrics": row["metrics"]} for row in rows],
        "matched_contrasts": contrasts,
        "sampling_note": "Deterministic constructed cells; no statistical replication claim",
    }


def produce(output: Path, source_commit: str, protocol_path: Path = PROTOCOL) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must be the readback-verified source checkpoint")
    protocol = load_protocol(protocol_path)
    runtime_hashes = verify_runtime(protocol)
    provenance = {
        "base_commit": protocol["base_commit"],
        "declared_source_checkpoint": source_commit,
        "checkpoint_note": "GitHub source readback is verified outside this offline runner",
        "runner_sha256": sha256(Path(__file__).read_bytes()),
        "protocol_sha256": PROTOCOL_SHA256,
        "runtime_sha256": runtime_hashes,
        "runtime_git_blobs": protocol["runtime_git_blobs"],
    }
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    active_cell = None
    stage = "open_raw"
    try:
        with (output / "raw_episodes.jsonl").open("wb") as raw:
            for cell in cells(protocol):
                active_cell = cell
                stage = "run_cell"
                row = run_episode(cell, protocol)
                stage = "write_raw"
                raw.write(canonical(row))
                raw.flush()
                rows.append(row)
        active_cell = None
        stage = "write_summary"
        (output / "summary.json").write_bytes(canonical(summarize(rows)))
        manifest = {
            "status": protocol["status"], **provenance, "episodes": len(rows),
            "files": {name: sha256((output / name).read_bytes())
                      for name in ("raw_episodes.jsonl", "summary.json")},
        }
        stage = "write_manifest"
        (output / "manifest.json").write_bytes(canonical(manifest))
    except Exception as exc:
        (output / "failure.json").write_bytes(canonical({
            **provenance,
            "status": "IMPLEMENTATION_FAILURE", "completed_rows": len(rows),
            "error_type": type(exc).__name__, "error": str(exc),
            "failure_stage": stage, "failing_cell": active_cell,
            "retained_files": {
                name: {"sha256": sha256((output / name).read_bytes()),
                       "bytes": (output / name).stat().st_size}
                for name in ("raw_episodes.jsonl", "summary.json", "manifest.json")
                if (output / name).is_file()
            },
        }))
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    produce(args.output, args.source_commit)


if __name__ == "__main__":
    main()
