#!/usr/bin/env python3
"""DEV-only Architecture Study for CAND-STRUCTURAL-ORDER-PATH-01.

This harness is intentionally NON_EVIDENTIARY. It implements only the cycle-1
contract prospectively fixed by Evidence Analyst commit
9c6302d83f71ab22d45c5f6290951a48902d9c1e. It never opens TEST.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

import torch

from sparkbrain.learned.checkpoint import save_checkpoint
from sparkbrain.learned.config import LearnedConfig
from sparkbrain.learned.training import calibrate_ignition, episode_examples, train_model
from sparkbrain.model import EventKind
from sparkbrain.structural.backend import StructuralBrainBackend
from sparkbrain.structural.config import StructuralConfig
from sparkbrain.tasks import Episode, generate_episode

SCIENTIFIC_SOURCE = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
ANALYST_COMMIT = "9c6302d83f71ab22d45c5f6290951a48902d9c1e"
MODEL_SEED = 43
STRUCTURAL_SEED = 83
PERMUTATION_SEED = 20260919
TRAIN_COUNT = 48
ADAPT_COUNT = 12
PROBE_COUNT = 12
STEPS = 24
TRAIN_WORLDS = ("switchworld", "contradiction_world")
DEV_WORLDS = ("goal_conflict_world", "multi_object_world")
DEV_MANIFEST = Path("configs/experiments/phase1/manifests/dev-v1.json")
PHASE2_CONFIG = Path("configs/experiments/phase2/main.json")
CONDITIONS = {
    "full_budget16": StructuralConfig(max_events_total=16),
    "full_budget64": StructuralConfig(max_events_total=64),
    "edge_only_budget64": StructuralConfig(
        max_events_total=64,
        enabled_events=("edge_grow", "edge_prune"),
    ),
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_contract() -> None:
    raw = _read_json(PHASE2_CONFIG)
    learned = raw["learned"]
    expected = {
        "seed": 41,
        "module_count": 12,
        "active_k": 4,
        "train_episodes": 48,
        "calibration_episodes": 12,
        "steps": 24,
    }
    for key, value in expected.items():
        if learned[key] != value:
            raise RuntimeError(f"phase2 contract drift: {key}={learned[key]!r}, expected {value!r}")
    if tuple(raw["train_worlds"]) != TRAIN_WORLDS:
        raise RuntimeError("phase2 train worlds drifted")
    if tuple(raw["calibration_worlds"]) != DEV_WORLDS:
        raise RuntimeError("phase2 calibration worlds drifted")
    if Path(raw["dev_manifest"]) != DEV_MANIFEST:
        raise RuntimeError("phase2 DEV manifest drifted")
    base = StructuralConfig()
    base.validate()
    required = {
        "seed": STRUCTURAL_SEED,
        "source_modules": 12,
        "max_modules": 18,
        "active_k": 4,
        "max_events_per_boundary": 2,
    }
    for key, value in required.items():
        if getattr(base, key) != value:
            raise RuntimeError(f"structural default drift: {key}")
    for config in CONDITIONS.values():
        config.validate()


def _episodes(
    manifest: dict[str, Any],
    *,
    count: int,
    offset: int,
    worlds: tuple[str, ...],
    steps: int,
) -> list[Episode]:
    if offset + count > int(manifest["episode_count"]):
        raise RuntimeError("DEV episode request exceeds immutable manifest")
    start = int(manifest["seed_start"]) + offset
    return [
        generate_episode(
            worlds[index % len(worlds)],
            seed=start + index,
            split=str(manifest["split"]),
            steps=steps,
        )
        for index in range(count)
    ]


def _source_checkpoint(output: Path, manifest: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    raw = _read_json(PHASE2_CONFIG)
    learned = LearnedConfig.from_dict({**raw["learned"], "seed": MODEL_SEED})
    training = _episodes(
        manifest,
        count=TRAIN_COUNT,
        offset=0,
        worlds=TRAIN_WORLDS,
        steps=STEPS,
    )
    calibration = _episodes(
        manifest,
        count=ADAPT_COUNT,
        offset=TRAIN_COUNT,
        worlds=DEV_WORLDS,
        steps=STEPS + 6,
    )
    model, history = train_model(learned, training)
    calibrated = calibrate_ignition(learned, model, calibration)
    checkpoint = output / "source-seed43.pt"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    save_checkpoint(
        checkpoint,
        config=calibrated,
        model=model,
        metadata={
            "scientific_source": SCIENTIFIC_SOURCE,
            "analyst_commit": ANALYST_COMMIT,
            "dev_manifest_sha256": _sha256(DEV_MANIFEST),
            "training_seed": MODEL_SEED,
            "test_manifest_opened": False,
        },
    )
    return checkpoint, {
        "training_seed": MODEL_SEED,
        "train_count": TRAIN_COUNT,
        "calibration_count": ADAPT_COUNT,
        "train_worlds": list(TRAIN_WORLDS),
        "calibration_worlds": list(DEV_WORLDS),
        "training_history": history,
        "confidence_threshold": calibrated.confidence_threshold,
        "margin_threshold": calibrated.margin_threshold,
    }


def _run_episode(backend: StructuralBrainBackend, episode: Episode) -> None:
    backend.reset(seed=episode.seed)
    for example in episode_examples(episode):
        backend.schedule(
            time=float(example.step_index + 1),
            kind=EventKind.STIMULUS,
            source=example.source_id,
            target=None,
            strength=example.strength,
            evidence_id=f"{episode.episode_id}:{example.step_index}",
            evidence_label=example.evidence_label,
            metadata={"channel": example.channel, "delivery_delay": example.delivery_delay},
        )
        backend.run()


def _adapt(
    checkpoint: Path,
    config: StructuralConfig,
    episodes: list[Episode],
    order: list[int],
) -> StructuralBrainBackend:
    backend = StructuralBrainBackend.from_c04_checkpoint(checkpoint, config)
    for boundary, index in enumerate(order, 1):
        _run_episode(backend, episodes[index])
        backend.discover_and_queue(next_boundary=boundary)
        backend.apply_boundary(boundary)
    return backend


def _clone(
    checkpoint: Path,
    config: StructuralConfig,
    state: dict[str, Any],
) -> StructuralBrainBackend:
    backend = StructuralBrainBackend.from_c04_checkpoint(checkpoint, config)
    backend.load_state_dict(state)
    return backend


def _probe(
    checkpoint: Path,
    config: StructuralConfig,
    state: dict[str, Any],
    episode: Episode,
) -> dict[str, Any]:
    backend = _clone(checkpoint, config, state)
    backend.reset(seed=episode.seed)
    rows: list[dict[str, Any]] = []
    correct = 0
    for example in episode_examples(episode):
        backend.schedule(
            time=float(example.step_index + 1),
            kind=EventKind.STIMULUS,
            source=example.source_id,
            target=None,
            strength=example.strength,
            evidence_id=f"{episode.episode_id}:{example.step_index}",
            evidence_label=example.evidence_label,
            metadata={"channel": example.channel, "delivery_delay": example.delivery_delay},
        )
        backend.run()
        record = backend.prediction_record()
        correct += int(record.belief == example.belief_truth)
        rows.append(
            {
                "step": example.step_index,
                "belief": record.belief,
                "truth": example.belief_truth,
                "probabilities": record.probabilities,
            }
        )
    return {
        "episode_id": episode.episode_id,
        "correct": correct,
        "steps": len(rows),
        "rows": rows,
    }


def _mask_snapshot(backend: StructuralBrainBackend) -> dict[str, Any]:
    modules = torch.where(backend.structural_model.active_module_mask)[0].tolist()
    edge_rows = torch.nonzero(backend.structural_model.active_edge_mask, as_tuple=False).tolist()
    identities = {
        str(slot): identity.to_dict()
        for slot, identity in sorted(backend.controller.identities.items())
    }
    kinds = Counter(event.kind for event in backend.controller.history if event.status == "applied")
    rejection = Counter(
        event.rejection or "unknown"
        for event in backend.controller.history
        if event.status == "rejected"
    )
    return {
        "active_modules": modules,
        "active_edges": edge_rows,
        "identities": identities,
        "tombstones": [item.to_dict() for item in backend.controller.tombstones],
        "event_kind_counts": dict(sorted(kinds.items())),
        "rejection_counts": dict(sorted(rejection.items())),
        "events_applied": backend.controller.events_applied,
        "events_rejected": backend.controller.events_rejected,
        "remaining_budget": backend.controller.remaining_budget,
        "homeostatic_updates": backend.controller.homeostatic_updates,
    }


def _jaccard(left: set[Any], right: set[Any]) -> float:
    union = left | right
    return 0.0 if not union else 1.0 - len(left & right) / len(union)


def _paired_probe_metrics(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
) -> dict[str, Any]:
    l1_values: list[float] = []
    disagreements = 0
    steps = 0
    left_correct = 0
    right_correct = 0
    labels: set[str] = set()
    for left_episode, right_episode in zip(left, right, strict=True):
        if left_episode["episode_id"] != right_episode["episode_id"]:
            raise RuntimeError("probe episode binding mismatch")
        left_correct += int(left_episode["correct"])
        right_correct += int(right_episode["correct"])
        for a, b in zip(left_episode["rows"], right_episode["rows"], strict=True):
            if a["step"] != b["step"] or a["truth"] != b["truth"]:
                raise RuntimeError("matched probe step binding mismatch")
            labels.update(a["probabilities"])
            labels.update(b["probabilities"])
            l1_values.append(
                sum(
                    abs(
                        float(a["probabilities"].get(label, 0.0))
                        - float(b["probabilities"].get(label, 0.0))
                    )
                    for label in labels
                )
            )
            disagreements += int(a["belief"] != b["belief"])
            steps += 1
    return {
        "mean_probability_l1": sum(l1_values) / len(l1_values),
        "prediction_disagreement_rate": disagreements / steps,
        "accuracy_difference": abs(left_correct / steps - right_correct / steps),
        "probe_steps": steps,
    }


def _order_pairs() -> list[tuple[list[int], list[int]]]:
    rng = random.Random(PERMUTATION_SEED)
    result = []
    for _ in range(12):
        order = list(range(ADAPT_COUNT))
        rng.shuffle(order)
        result.append((order, list(reversed(order))))
    return result


def _run_raw(output: Path) -> dict[str, Any]:
    _validate_contract()
    dev_before = _sha256(DEV_MANIFEST)
    phase2_before = _sha256(PHASE2_CONFIG)
    manifest = _read_json(DEV_MANIFEST)
    checkpoint, source = _source_checkpoint(output, manifest)
    adaptation = _episodes(
        manifest,
        count=ADAPT_COUNT,
        offset=TRAIN_COUNT,
        worlds=DEV_WORLDS,
        steps=STEPS,
    )
    probes = _episodes(
        manifest,
        count=PROBE_COUNT,
        offset=TRAIN_COUNT + ADAPT_COUNT,
        worlds=DEV_WORLDS,
        steps=STEPS,
    )
    pairs = _order_pairs()
    conditions: dict[str, list[dict[str, Any]]] = {}
    for condition_name, config in CONDITIONS.items():
        rows = []
        for pair_index, (order, reverse) in enumerate(pairs):
            left = _adapt(checkpoint, config, adaptation, order)
            right = _adapt(checkpoint, config, adaptation, reverse)
            left_state = left.state_dict(include_trace=False)
            right_state = right.state_dict(include_trace=False)
            left_mask = _mask_snapshot(left)
            right_mask = _mask_snapshot(right)
            left_modules = set(left_mask["active_modules"])
            right_modules = set(right_mask["active_modules"])
            left_edges = {tuple(row) for row in left_mask["active_edges"]}
            right_edges = {tuple(row) for row in right_mask["active_edges"]}
            module_distance = _jaccard(left_modules, right_modules)
            edge_distance = _jaccard(left_edges, right_edges)
            left_probe = [_probe(checkpoint, config, left_state, episode) for episode in probes]
            right_probe = [_probe(checkpoint, config, right_state, episode) for episode in probes]
            rows.append(
                {
                    "pair_index": pair_index,
                    "order": order,
                    "reverse": reverse,
                    "module_jaccard_distance": module_distance,
                    "edge_jaccard_distance": edge_distance,
                    "topology_diverged": module_distance > 0.0 or edge_distance > 0.0,
                    "probe": _paired_probe_metrics(left_probe, right_probe),
                    "left": left_mask,
                    "right": right_mask,
                }
            )
        conditions[condition_name] = rows
    if _sha256(DEV_MANIFEST) != dev_before or _sha256(PHASE2_CONFIG) != phase2_before:
        raise RuntimeError("bound DEV/config inputs changed during run")
    raw = {
        "schema_version": "0.1",
        "candidate": "CAND-STRUCTURAL-ORDER-PATH-01",
        "layer": "ARCHITECTURE_STUDY",
        "evidentiary_status": "NON_EVIDENTIARY",
        "scientific_source": SCIENTIFIC_SOURCE,
        "analyst_commit": ANALYST_COMMIT,
        "test_manifest_opened": False,
        "bindings": {
            "phase2_config": str(PHASE2_CONFIG),
            "phase2_config_sha256": phase2_before,
            "dev_manifest": str(DEV_MANIFEST),
            "dev_manifest_sha256": dev_before,
            "model_seed": MODEL_SEED,
            "structural_seed": STRUCTURAL_SEED,
            "permutation_seed": PERMUTATION_SEED,
            "train_episode_offset_count": [0, TRAIN_COUNT],
            "adapt_episode_offset_count": [TRAIN_COUNT, ADAPT_COUNT],
            "probe_episode_offset_count": [TRAIN_COUNT + ADAPT_COUNT, PROBE_COUNT],
            "steps": STEPS,
            "conditions": {name: config.to_dict() for name, config in CONDITIONS.items()},
        },
        "source_training": source,
        "conditions": conditions,
    }
    _write_json(output / "raw.json", raw)
    return raw


def _map(raw: dict[str, Any]) -> dict[str, Any]:
    if raw.get("test_manifest_opened") is not False:
        raise RuntimeError("invalid DEV-only binding")
    if (
        raw.get("scientific_source") != SCIENTIFIC_SOURCE
        or raw.get("analyst_commit") != ANALYST_COMMIT
    ):
        raise RuntimeError("authority/source binding mismatch")
    summary: dict[str, Any] = {}
    for condition, rows in raw["conditions"].items():
        topology = sum(bool(row["topology_diverged"]) for row in rows)
        functional = sum(float(row["probe"]["mean_probability_l1"]) >= 0.01 for row in rows)
        mean_l1 = sum(float(row["probe"]["mean_probability_l1"]) for row in rows) / len(rows)
        summary[condition] = {
            "topology_divergent_pairs": topology,
            "functional_l1_ge_0_01_pairs": functional,
            "mean_probability_l1": mean_l1,
        }
    b16 = summary["full_budget16"]
    b64 = summary["full_budget64"]
    edge = summary["edge_only_budget64"]
    if b16["topology_divergent_pairs"] >= 9 and b64["topology_divergent_pairs"] <= 3:
        label = "BUDGET_DOMINATED_PATH_DEPENDENCE"
    elif edge["topology_divergent_pairs"] >= 9 and edge["mean_probability_l1"] >= 0.01:
        label = "EDGE_OR_HOMEOSTASIS_CONTROL_REPRODUCES"
    elif b64["topology_divergent_pairs"] >= 9 and b64["functional_l1_ge_0_01_pairs"] >= 9:
        label = "REAL_DEV_FUNCTIONAL_PATH_DEPENDENCE"
    elif b64["topology_divergent_pairs"] >= 9 and b64["functional_l1_ge_0_01_pairs"] <= 3:
        label = "LOW_FUNCTIONAL_OR_TOPOLOGY_ONLY_PATH_DEPENDENCE"
    elif b64["topology_divergent_pairs"] <= 3 and b64["functional_l1_ge_0_01_pairs"] <= 3:
        label = "NO_OR_LOW_SUPPORT_REAL_DEV_PATH_DEPENDENCE"
    else:
        label = "MIXED_ARCHITECTURE_RESULT"
    return {
        "candidate": raw["candidate"],
        "layer": raw["layer"],
        "evidentiary_status": raw["evidentiary_status"],
        "scientific_source": raw["scientific_source"],
        "analyst_commit": raw["analyst_commit"],
        "local_architecture_label": label,
        "condition_summary": summary,
        "interpretation_boundary": (
            "DEV-only Architecture Study triage. This label is not FORMAL evidence, "
            "a novelty gate, or authority for PRE_FORMAL/FORMAL continuation. "
            "STOP for fresh Analyst review."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("validate", "raw", "map"), required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/architecture_studies/structural-order-path-cycle1"),
    )
    args = parser.parse_args()
    if args.phase == "validate":
        _validate_contract()
        return
    if args.phase == "raw":
        _run_raw(args.output)
        return
    raw_path = args.output / "raw.json"
    if not raw_path.is_file():
        raise RuntimeError("raw.json must exist before terminal mapping")
    _write_json(args.output / "summary.json", _map(_read_json(raw_path)))


if __name__ == "__main__":
    main()
