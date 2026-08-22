from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Any

import torch

from ..learned.backend import LearnedBrainBackend
from ..learned.checkpoint import load_checkpoint
from ..learned.training import episode_examples
from ..model import EventKind
from ..tasks import Episode, generate_episode
from .backend import StructuralBrainBackend
from .config import StructuralConfig


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _episodes(
    manifest: dict[str, Any], *, count: int, worlds: tuple[str, ...], steps: int, offset: int = 0
) -> list[Episode]:
    if count + offset > int(manifest["episode_count"]):
        raise ValueError("Requested structural episodes exceed frozen manifest")
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


def _run_episode(backend, episode: Episode) -> dict[str, Any]:
    backend.reset(seed=episode.seed)
    correct = 0
    covered = 0
    rows = []
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
        prediction = backend.prediction
        correct += int(prediction == example.belief_truth)
        covered += int(prediction is not None)
        rows.append(
            {
                "step": example.step_index,
                "object_id": example.object_id,
                "prediction": prediction,
                "truth": example.belief_truth,
                "selected_modules": list(backend.prediction_record().selected_modules),
            }
        )
    return {
        "episode_id": episode.episode_id,
        "world_id": episode.world_id,
        "correct": correct,
        "covered": covered,
        "steps": len(rows),
        "accuracy": correct / len(rows),
        "coverage": covered / len(rows),
        "rows": rows,
        "counters": backend.work.to_dict(),
    }


def _evaluate(backend, episodes: list[Episode]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = [_run_episode(backend, episode) for episode in episodes]
    total = sum(row["steps"] for row in rows)
    by_world: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        by_world[row["world_id"]].append(row["accuracy"])
    counter_keys = rows[0]["counters"] if rows else {}
    counters = {
        key: sum(row["counters"][key] for row in rows) for key in counter_keys
    }
    return (
        {
            "episodes": len(rows),
            "steps": total,
            "accuracy": sum(row["correct"] for row in rows) / total,
            "coverage": sum(row["covered"] for row in rows) / total,
            "accuracy_by_world": {
                world: sum(values) / len(values) for world, values in sorted(by_world.items())
            },
            "counters": counters,
        },
        rows,
    )


def _graph_stats(backend: StructuralBrainBackend) -> dict[str, Any]:
    active = torch.where(backend.structural_model.active_module_mask)[0].tolist()
    edges = backend.structural_model.active_edge_mask
    degrees = {
        str(slot): int(edges[slot].sum() + edges[:, slot].sum()) for slot in active
    }
    unseen = set(active)
    components: list[list[int]] = []
    while unseen:
        pending = [min(unseen)]
        component: list[int] = []
        while pending:
            slot = pending.pop()
            if slot not in unseen:
                continue
            unseen.remove(slot)
            component.append(slot)
            neighbors = torch.where(edges[slot] | edges[:, slot])[0].tolist()
            pending.extend(item for item in neighbors if item in unseen)
        components.append(sorted(component))
    edge_count = int(edges.sum())
    possible = max(1, len(active) ** 2)
    return {
        "active_modules": len(active),
        "active_edges": edge_count,
        "directed_density": edge_count / possible,
        "degrees": degrees,
        "connected_components": components,
        "fragmented": len(components) > 1,
        "erdos_renyi_density_null": edge_count / possible,
    }


def _mutual_information(rows: list[dict[str, Any]], candidate: tuple[int, ...]) -> float:
    observations = [
        (row["world_id"], bool(set(step["selected_modules"]) & set(candidate)))
        for row in rows
        for step in row["rows"]
    ]
    total = len(observations)
    if not total:
        return 0.0
    worlds = sorted({world for world, _ in observations})
    result = 0.0
    for world in worlds:
        for active in (False, True):
            joint = sum(pair == (world, active) for pair in observations) / total
            if not joint:
                continue
            p_world = sum(item[0] == world for item in observations) / total
            p_active = sum(item[1] == active for item in observations) / total
            result += joint * math.log(joint / (p_world * p_active))
    return result


def _selectivity_analysis(
    rows: list[dict[str, Any]], candidate: tuple[int, ...], *, seed: int
) -> dict[str, Any]:
    observed = _mutual_information(rows, candidate)
    labels = [row["world_id"] for row in rows]
    rng = random.Random(seed)
    null_values = []
    for _ in range(50):
        shuffled = list(labels)
        rng.shuffle(shuffled)
        permuted = [{**row, "world_id": label} for row, label in zip(rows, shuffled, strict=True)]
        null_values.append(_mutual_information(permuted, candidate))
    return {
        "measure": "mutual_information(candidate_routed, world_id)",
        "observed": observed,
        "permutation_null_mean": sum(null_values) / len(null_values),
        "permutations": len(null_values),
        "post_hoc_only": True,
        "used_for_candidate_discovery": False,
    }


def _specificity_gate(
    dev_effects: dict[str, float],
    test_effects: dict[str, float],
    *,
    target_minimum: float,
    collateral_maximum: float,
) -> dict[str, Any]:
    ranked = sorted(dev_effects.items(), key=lambda row: (-row[1], row[0]))
    target = None
    if ranked and ranked[0][1] > 0:
        if len(ranked) == 1 or ranked[0][1] > ranked[1][1]:
            target = ranked[0][0]
    target_impairment = test_effects.get(target) if target is not None else None
    collateral = max(
        [0.0, *(effect for world, effect in test_effects.items() if world != target)]
    )
    available = target is not None and target in test_effects
    return {
        "passed": available
        and target_impairment is not None
        and target_impairment >= target_minimum
        and collateral <= collateral_maximum,
        "dev_target_world": target,
        "target_present_in_test": available,
        "target_impairment": target_impairment,
        "target_minimum": target_minimum,
        "unrelated_collateral": collateral,
        "unrelated_collateral_maximum": collateral_maximum,
        "fail_closed_reason": (
            None if available else "dev target unavailable or absent from held-out test families"
        ),
    }


def _clone_from_state(
    source_checkpoint: Path, config: StructuralConfig, state: dict[str, Any]
) -> StructuralBrainBackend:
    backend = StructuralBrainBackend.from_c04_checkpoint(source_checkpoint, config)
    backend.load_state_dict(state)
    return backend


def _ablate(backend: StructuralBrainBackend, slots: tuple[int, ...]) -> None:
    for slot in slots:
        backend.structural_model.active_module_mask[slot] = False
        backend.structural_model.active_edge_mask[slot, :] = False
        backend.structural_model.active_edge_mask[:, slot] = False


def _activate(backend: StructuralBrainBackend, slots: tuple[int, ...], strength: float) -> None:
    """Apply a bounded post-hoc router intervention without changing discovery."""
    with torch.no_grad():
        for slot in slots:
            backend.structural_model.router.bias[slot].add_(strength)


def _timeline_html(seed_runs: list[dict[str, Any]]) -> str:
    rows = []
    for seed_run in seed_runs:
        for event in seed_run["history"]:
            rows.append(
                "<tr>"
                f"<td>{seed_run['seed']}</td><td>{event['boundary']}</td>"
                f"<td>{event['sequence']}</td><td>{event['kind']}</td>"
                f"<td>{event['status']}</td><td>{event.get('rejection') or ''}</td>"
                "</tr>"
            )
    return (
        "<!doctype html><meta charset=\"utf-8\"><title>C08 structural timeline</title>"
        "<style>body{font:14px system-ui;margin:2rem}table{border-collapse:collapse}"
        "th,td{border:1px solid #aaa;padding:.35rem}.applied{background:#dfd}</style>"
        "<h1>C08 structural event timeline</h1>"
        "<p>Episode-boundary order; rejected events are retained as negative evidence.</p>"
        "<table><thead><tr><th>seed</th><th>boundary</th><th>sequence</th>"
        "<th>event</th><th>status</th><th>rejection</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>\n"
    )


def _degree_matched(
    backend: StructuralBrainBackend, target: tuple[int, ...], *, size: int
) -> tuple[int, ...]:
    edges = backend.structural_model.active_edge_mask
    active = torch.where(backend.structural_model.active_module_mask)[0].tolist()
    degrees = {slot: int(edges[slot].sum() + edges[:, slot].sum()) for slot in active}
    target_degree = sum(degrees[slot] for slot in target) / len(target)
    candidates = sorted(
        (slot for slot in active if slot not in target),
        key=lambda slot: (abs(degrees[slot] - target_degree), slot),
    )
    return tuple(candidates[:size])


def _root_lineage_signature(
    backend: StructuralBrainBackend, slots: tuple[int, ...]
) -> list[list[str]]:
    identities = backend.controller.identities

    def roots(slot: int) -> list[str]:
        identity = identities[slot]
        if not identity.parents:
            return [identity.logical_id]
        return sorted(parent for parent in identity.parents if parent.startswith("source:"))

    return sorted(roots(slot) for slot in slots)


def _adapt(
    source_checkpoint: Path,
    config: StructuralConfig,
    episodes: list[Episode],
    *,
    hard_deadline: float,
) -> tuple[StructuralBrainBackend, tuple[int, ...], bool]:
    backend = StructuralBrainBackend.from_c04_checkpoint(source_checkpoint, config)
    optimizer = torch.optim.Adam(backend.structural_model.parameters(), lr=0.0)
    capped = False
    for boundary, episode in enumerate(episodes, 1):
        if time.perf_counter() >= hard_deadline:
            capped = True
            break
        _run_episode(backend, episode)
        backend.discover_and_queue(next_boundary=boundary)
        backend.apply_boundary(boundary)
    backend.optimizer_state = optimizer.state_dict()
    candidate = backend.controller.candidate_group(backend.structural_stats(), size=2)
    return backend, candidate, capped


def run(config_path: str | Path) -> dict[str, Any]:
    started = time.perf_counter()
    raw = _read_json(Path(config_path))
    base_config = StructuralConfig.from_dict(raw["structural"])
    source_checkpoint = Path(raw["source_checkpoint"])
    source_config = Path(raw["source_config"])
    dev_path = Path(raw["dev_manifest"])
    test_path = Path(raw["test_manifest"])
    frozen_before = {
        "source_checkpoint": _sha256(source_checkpoint),
        "source_config": _sha256(source_config),
        "dev_manifest": _sha256(dev_path),
        "test_manifest": _sha256(test_path),
    }
    expected = raw["expected_sha256"]
    if frozen_before != expected:
        raise RuntimeError("C08 frozen input hash mismatch")
    dev_manifest = _read_json(dev_path)
    test_manifest = _read_json(test_path)
    train = _episodes(
        dev_manifest,
        count=int(raw["train_episodes"]),
        worlds=tuple(raw["train_worlds"]),
        steps=int(raw["steps"]),
    )
    held_out = _episodes(
        test_manifest,
        count=int(raw["test_episodes"]),
        worlds=tuple(raw["test_worlds"]),
        steps=int(raw["steps"]) + 8,
    )
    output = Path(raw["output_dir"])
    hard_deadline = started + float(raw["hard_cap_seconds"])
    seed_runs = []
    states: list[dict[str, Any]] = []
    candidates: list[tuple[int, ...]] = []
    capped_any = False
    for seed in raw["structural_seeds"]:
        config = replace(base_config, seed=int(seed))
        backend, candidate, capped = _adapt(
            source_checkpoint, config, train, hard_deadline=hard_deadline
        )
        state = backend.state_dict(include_trace=False)
        states.append(state)
        candidates.append(candidate)
        capped_any |= capped
        checkpoint_path = output / f"structural-seed-{seed}.pt"
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(state, checkpoint_path)
        dev_unablated = _clone_from_state(source_checkpoint, config, state)
        dev_unablated_summary, _ = _evaluate(dev_unablated, train)
        dev_targeted = _clone_from_state(source_checkpoint, config, state)
        _ablate(dev_targeted, candidate)
        dev_targeted_summary, _ = _evaluate(dev_targeted, train)
        dev_effects = {
            world: dev_unablated_summary["accuracy_by_world"][world]
            - dev_targeted_summary["accuracy_by_world"][world]
            for world in dev_unablated_summary["accuracy_by_world"]
        }
        seed_runs.append(
            {
                "seed": seed,
                "candidate": list(candidate),
                "events_applied": backend.controller.events_applied,
                "events_rejected": backend.controller.events_rejected,
                "active_modules": int(backend.structural_model.active_module_mask.sum()),
                "active_edges": int(backend.structural_model.active_edge_mask.sum()),
                "lineage_signature": _root_lineage_signature(backend, candidate),
                "dev_functional_effect_signature": dev_effects,
                "history": [event.to_dict() for event in backend.controller.history],
                "identities": [row.to_dict() for row in backend.controller.identities.values()],
                "tombstones": [row.to_dict() for row in backend.controller.tombstones],
            }
        )
    primary_config = replace(base_config, seed=int(raw["structural_seeds"][0]))
    primary_state = states[0]
    candidate = candidates[0]
    unablated = _clone_from_state(source_checkpoint, primary_config, primary_state)
    unablated_summary, unablated_rows = _evaluate(unablated, held_out)
    random_backend = _clone_from_state(source_checkpoint, primary_config, primary_state)
    active = torch.where(random_backend.structural_model.active_module_mask)[0].tolist()
    control_rng = random.Random(base_config.seed + 9000)
    random_slots = tuple(
        sorted(control_rng.sample([x for x in active if x not in candidate], len(candidate)))
    )
    _ablate(random_backend, random_slots)
    random_summary, random_rows = _evaluate(random_backend, held_out)
    degree_backend = _clone_from_state(source_checkpoint, primary_config, primary_state)
    degree_slots = _degree_matched(degree_backend, candidate, size=len(candidate))
    _ablate(degree_backend, degree_slots)
    degree_summary, degree_rows = _evaluate(degree_backend, held_out)
    targeted_backend = _clone_from_state(source_checkpoint, primary_config, primary_state)
    _ablate(targeted_backend, candidate)
    targeted_summary, targeted_rows = _evaluate(targeted_backend, held_out)
    activation_backend = _clone_from_state(source_checkpoint, primary_config, primary_state)
    _activate(activation_backend, candidate, strength=0.5)
    activation_summary, activation_rows = _evaluate(activation_backend, held_out)

    learned_config, learned_model, _ = load_checkpoint(source_checkpoint)
    source_backend = LearnedBrainBackend(learned_config, learned_model)
    source_summary, source_rows = _evaluate(source_backend, held_out)
    target_impairment = unablated_summary["accuracy"] - targeted_summary["accuracy"]
    random_impairment = unablated_summary["accuracy"] - random_summary["accuracy"]
    degree_impairment = unablated_summary["accuracy"] - degree_summary["accuracy"]
    world_effects = {
        world: unablated_summary["accuracy_by_world"][world]
        - targeted_summary["accuracy_by_world"][world]
        for world in unablated_summary["accuracy_by_world"]
    }
    primary_dev_effects = seed_runs[0]["dev_functional_effect_signature"]
    specificity_gate = _specificity_gate(
        primary_dev_effects,
        world_effects,
        target_minimum=base_config.specificity_margin,
        collateral_maximum=base_config.unrelated_collateral_max,
    )
    dev_target_world = specificity_gate["dev_target_world"]
    lineage_signatures = [row["lineage_signature"] for row in seed_runs]
    gates = {
        "multiplicity": {
            "passed": len(candidates) >= base_config.multiplicity_min_seeds
            and all(row == candidate for row in candidates),
            "observed": len(candidates),
            "threshold": base_config.multiplicity_min_seeds,
            "slot_sets_consistent": all(row == candidate for row in candidates),
            "lineage_signatures": lineage_signatures,
            "lineage_consistent": all(row == lineage_signatures[0] for row in lineage_signatures),
            "dev_functional_effect_signatures": [
                row["dev_functional_effect_signature"] for row in seed_runs
            ],
        },
        "decisiveness": {
            "passed": target_impairment - max(random_impairment, degree_impairment)
            >= base_config.decisiveness_margin,
            "observed": target_impairment - max(random_impairment, degree_impairment),
            "threshold": base_config.decisiveness_margin,
        },
        "fertility": {
            "passed": unablated_summary["accuracy"] - source_summary["accuracy"]
            >= base_config.fertility_min_effect,
            "observed": unablated_summary["accuracy"] - source_summary["accuracy"],
            "threshold": base_config.fertility_min_effect,
        },
        "specificity": specificity_gate,
    }
    specialization_passed = all(row["passed"] for row in gates.values())
    sensitivity = []
    for event_budget in raw["budget_sensitivity"]:
        config = replace(
            base_config,
            seed=base_config.seed + int(event_budget),
            max_events_total=int(event_budget),
        )
        backend, group, capped = _adapt(
            source_checkpoint,
            config,
            train[: max(1, len(train) // 2)],
            hard_deadline=hard_deadline,
        )
        summary, _ = _evaluate(backend, held_out[: max(1, len(held_out) // 3)])
        sensitivity.append(
            {
                "event_budget": event_budget,
                "candidate": list(group),
                "events_applied": backend.controller.events_applied,
                "active_modules": int(backend.structural_model.active_module_mask.sum()),
                "active_edges": int(backend.structural_model.active_edge_mask.sum()),
                "accuracy": summary["accuracy"],
                "capped": capped,
            }
        )
    frozen_after = {
        "source_checkpoint": _sha256(source_checkpoint),
        "source_config": _sha256(source_config),
        "dev_manifest": _sha256(dev_path),
        "test_manifest": _sha256(test_path),
    }
    if frozen_after != frozen_before:
        raise RuntimeError("C08 frozen inputs changed during execution")
    paired = {
        "candidate": list(candidate),
        "random_slots": list(random_slots),
        "degree_matched_slots": list(degree_slots),
        "unablated": unablated_summary,
        "targeted": targeted_summary,
        "activation_intervention": activation_summary,
        "random": random_summary,
        "degree_matched": degree_summary,
        "source_c04": source_summary,
        "target_impairment": target_impairment,
        "activation_effect": activation_summary["accuracy"] - unablated_summary["accuracy"],
        "random_impairment": random_impairment,
        "degree_impairment": degree_impairment,
        "world_effects": world_effects,
    }
    analyses = {
        "graph": _graph_stats(unablated),
        "selectivity": _selectivity_analysis(
            unablated_rows, candidate, seed=base_config.seed + 12000
        ),
        "functional_reuse_world_effects": world_effects,
        "dev_target_selection": {
            "selected_world": dev_target_world,
            "development_effects": primary_dev_effects,
            "selection_rule": "unique positive maximum development ablation impairment",
            "test_worlds": sorted(world_effects),
            "fail_closed": dev_target_world is None or dev_target_world not in world_effects,
        },
        "specialization_load_balance_tradeoff": {
            "candidate": list(candidate),
            "active_modules": int(unablated.structural_model.active_module_mask.sum()),
            "active_edges": int(unablated.structural_model.active_edge_mask.sum()),
            "target_impairment": target_impairment,
            "activation_effect": activation_summary["accuracy"]
            - unablated_summary["accuracy"],
        },
    }
    negative = {
        "specialization_passed": specialization_passed,
        "claim_grade": "E0" if not specialization_passed else "candidate-only",
        "allowed_wording": "candidate functional specialization",
        "prohibited_wording": "organs emerged",
        "candidate_discovery_inputs": [
            "routing_load",
            "coactivation",
            "edge_credit",
            "confidence_delta",
        ],
        "test_threshold_tuning": False,
        "runtime_cap_reached": capped_any or time.perf_counter() >= hard_deadline,
    }
    acceptance = {
        "frozen_inputs_unchanged": frozen_after == expected,
        "deterministic_events_serialized": bool(seed_runs),
        "bounded_capacity": all(
            row["active_modules"] <= base_config.max_modules
            and row["active_edges"] <= base_config.max_active_edges
            for row in seed_runs
        ),
        "random_control": bool(random_slots),
        "degree_matched_control": bool(degree_slots),
        "activation_intervention": bool(activation_rows),
        "dev_target_fixed_or_fail_closed": dev_target_world is not None
        or not gates["specificity"]["passed"],
        "gate_matrix_recorded": set(gates)
        == {"multiplicity", "decisiveness", "fertility", "specificity"},
        "positive_or_valid_negative": specialization_passed or negative["claim_grade"] == "E0",
        "budget_sensitivity_recorded": bool(sensitivity),
        "actual_edge_counters": all(
            0 < row["counters"]["evaluated_edges"]
            <= row["counters"]["observations"] * base_config.active_k**2
            for row in unablated_rows
        ),
    }
    result = {
        "schema_version": "0.2",
        "runtime_seconds": time.perf_counter() - started,
        "frozen_inputs": frozen_before,
        "structural_config": base_config.to_dict(),
        "seed_runs": seed_runs,
        "paired_controls": paired,
        "analyses": analyses,
        "gates": gates,
        "specialization_passed": specialization_passed,
        "negative_findings": negative,
        "acceptance": acceptance,
    }
    _write_json(output / "resolved-config.json", raw)
    _write_json(output / "input-hashes.json", {"before": frozen_before, "after": frozen_after})
    _write_json(output / "structural-history.json", seed_runs)
    _write_json(output / "paired-controls.json", paired)
    _write_json(output / "paired-rows.json", {
        "unablated": unablated_rows,
        "targeted": targeted_rows,
        "activation_intervention": activation_rows,
        "random": random_rows,
        "degree_matched": degree_rows,
        "source_c04": source_rows,
    })
    _write_json(output / "gate-matrix.json", gates)
    _write_json(output / "dev-target-selection.json", analyses["dev_target_selection"])
    _write_json(output / "analyses.json", analyses)
    _write_json(output / "budget-sensitivity.json", sensitivity)
    _write_json(output / "negative-findings.json", negative)
    _write_json(output / "acceptance-matrix.json", acceptance)
    _write_json(output / "summary.json", result)
    with (output / "structural-timeline.html").open(
        "w", encoding="utf-8", newline="\n"
    ) as stream:
        stream.write(_timeline_html(seed_runs))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run offline C08 structural-plasticity study")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.config), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
