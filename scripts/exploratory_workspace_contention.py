"""Frozen, non-evidentiary diagnostic of the legacy global ignition gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, Spark, SparkKind

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/experiments/exploratory/workspace_contention/protocol.json"
PROTOCOL_SHA256 = "8f4be213aee46e83e9f992156d712301b9910de383290407186974cb3bce19b0"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_protocol(path: Path = PROTOCOL) -> dict[str, Any]:
    """Reject every mutation, including types, extra fields and raw formatting."""
    raw = path.read_bytes()
    if sha256(raw) != PROTOCOL_SHA256:
        raise ValueError("Frozen protocol bytes differ; create a new protocol instead")
    return json.loads(raw)


def verify_runtime(protocol: dict[str, Any]) -> dict[str, str]:
    actual = {}
    for name, expected in protocol["runtime_git_blobs"].items():
        raw = (ROOT / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != expected:
            raise ValueError(f"Pinned runtime differs: {name}")
        actual[name] = sha256(raw)
    return actual


def cells(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    names = ("seed", "task_count", "slots", "order", "strength_profile", "variant")
    axes = ("seeds", "task_counts", "workspace_slots", "orders", "strength_profiles", "variants")
    return [dict(zip(names, values, strict=True)) for values in itertools.product(
        *(protocol[axis] for axis in axes)
    )]


def input_stream(cell: dict[str, Any], protocol: dict[str, Any]) -> list[dict[str, Any]]:
    rng = random.Random(cell["seed"])
    ids = list(range(cell["task_count"]))
    rng.shuffle(ids)
    order = list(range(cell["task_count"]))
    rng.shuffle(order)
    rounds = range(protocol["rounds"])
    if cell["order"] == "interleaved":
        pairs = [(task, turn) for turn in rounds for task in order]
    else:
        pairs = [(task, turn) for task in order for turn in rounds]
    rows = []
    for task, turn in pairs:
        for source in range(protocol["sources_per_task"]):
            index = len(rows)
            dominant = cell["strength_profile"] == "dominant_first" and task == 0
            rows.append({
                "index": index,
                "time": (index + 1) * protocol["event_spacing"],
                "task": task,
                "hypothesis_id": f"h{ids[task]}",
                "source": f"task{task}:sensor{source}",
                "evidence_id": f"task{task}:round{turn}:sensor{source}",
                "strength": protocol["dominant_strength" if dominant else "base_strength"],
            })
    return rows


def run_episode(cell: dict[str, Any], protocol: dict[str, Any]) -> dict[str, Any]:
    stream = input_stream(cell, protocol)
    mapping = {row["task"]: row["hypothesis_id"] for row in stream}
    inverse = {value: key for key, value in mapping.items()}
    config = BrainConfig(random_seed=cell["seed"], workspace_slots=cell["slots"])
    if cell["variant"] == "shared_zero_margin":
        config.ignition_margin = 0.0
    isolated = cell["variant"] == "isolated_reference"
    brains = {task: SparkBrain(config) for task in range(cell["task_count"])} if isolated else {
        0: SparkBrain(config)
    }
    for task, spark_id in mapping.items():
        brain = brains[task if isolated else 0]
        brain.add_spark(Spark(
            id=spark_id, label=f"compatible_fact_{task}", kind=SparkKind.HYPOTHESIS,
            organ=f"task_{task}", competition_group=f"independent_group_{task}",
            threshold=protocol["spark_threshold"], base_threshold=protocol["spark_threshold"],
            decay_tau=protocol["spark_decay_tau"],
        ))
    ignitions = []
    for row in stream:
        brain = brains[row["task"] if isolated else 0]
        previous = len(brain.ignitions)
        brain.inject_stimulus(
            target=row["hypothesis_id"], label=row["source"], time=row["time"],
            strength=row["strength"], source=row["source"], evidence_id=row["evidence_id"],
        )
        brain.run()
        for ignition in brain.ignitions[previous:]:
            ignitions.append({
                **asdict(ignition), "input_index": row["index"],
                "task": inverse[ignition.hypothesis_id],
            })
    workspace = [
        {**asdict(item), "task": inverse[item.hypothesis_id]}
        for brain in brains.values() for item in brain.workspace
    ]
    coalitions = [
        {**asdict(item), "task": inverse[item.hypothesis_id]}
        for brain in brains.values() for item in brain.last_coalitions
    ]
    first = {
        str(task): next((row["input_index"] for row in ignitions if row["task"] == task), None)
        for task in range(cell["task_count"])
    }
    counters = {
        name: sum(asdict(brain.stats)[name] for brain in brains.values())
        for name in asdict(next(iter(brains.values())).stats)
    }
    return {
        "cell": cell, "config": asdict(config), "inputs": stream,
        "input_sha256": sha256(canonical(stream)), "ignitions": ignitions,
        "final_workspace": workspace, "final_coalitions": coalitions,
        "engine_count": len(brains), "counters": counters,
        "metrics": {
            "fraction_tasks_ever_ignited": sum(v is not None for v in first.values())
            / cell["task_count"],
            "fraction_tasks_in_final_workspace": len({row["task"] for row in workspace})
            / cell["task_count"],
            "per_task_first_ignition_input_index": first,
        },
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        cell = row["cell"]
        key = f"{cell['variant']}:tasks={cell['task_count']}:slots={cell['slots']}"
        groups.setdefault(key, []).append(row)
    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY", "episode_count": len(rows),
        "groups": {
            key: {
                "episodes": len(group),
                "mean_fraction_tasks_ever_ignited": sum(
                    row["metrics"]["fraction_tasks_ever_ignited"] for row in group
                ) / len(group),
                "mean_fraction_tasks_in_final_workspace": sum(
                    row["metrics"]["fraction_tasks_in_final_workspace"] for row in group
                ) / len(group),
                "minimum_fraction_tasks_ever_ignited": min(
                    row["metrics"]["fraction_tasks_ever_ignited"] for row in group
                ),
            } for key, group in sorted(groups.items())
        },
    }


def produce(output: Path, source_commit: str, protocol_path: Path = PROTOCOL) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must be the published 40-character source checkpoint")
    protocol = load_protocol(protocol_path)
    runtime_hashes = verify_runtime(protocol)
    if output.exists():
        raise FileExistsError("Choose a fresh output directory; never overwrite a result")
    rows = [run_episode(cell, protocol) for cell in cells(protocol)]
    raw = b"".join(canonical(row) for row in rows)
    summary = canonical(summarize(rows))
    manifest = {
        "status": protocol["status"], "base_commit": protocol["base_commit"],
        "declared_source_checkpoint": source_commit,
        "source_checkpoint_note": "GitHub readback is verified outside this offline runner",
        "runner_sha256": sha256(Path(__file__).read_bytes()),
        "protocol_sha256": PROTOCOL_SHA256, "runtime_sha256": runtime_hashes,
        "runtime_git_blobs": protocol["runtime_git_blobs"],
        "files": {"raw_episodes.jsonl": sha256(raw), "summary.json": sha256(summary)},
        "episodes": len(rows), "seed_role": "task order and hypothesis ID permutation only",
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, data in (("raw_episodes.jsonl", raw), ("summary.json", summary),
                       ("manifest.json", canonical(manifest))):
        (output / name).write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    produce(args.output, args.source_commit)


if __name__ == "__main__":
    main()
