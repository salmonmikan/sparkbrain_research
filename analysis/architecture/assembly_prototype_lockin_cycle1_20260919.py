from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
from pathlib import Path
from typing import Any

from sparkbrain.v05.action import AssemblyActionPolicy
from sparkbrain.v05.assemblies import AssemblyConfig, TemporalAssemblyMemory, pattern_similarity
from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig
from sparkbrain.v05.prediction import AssemblyPredictor
from sparkbrain.v05.worlds import held_out_episodes, training_episodes

CONTRACT_PATH = Path(
    "analysis/architecture/assembly_prototype_lockin_cycle1_contract_20260919.json"
)


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _git_blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True).strip()


def _verify_contract(contract: dict[str, Any]) -> None:
    if contract["candidate_id"] != "CAND-ASSEMBLY-PROTOTYPE-LOCKIN-01":
        raise RuntimeError("candidate binding mismatch")
    if contract["research_layer"] != "ARCHITECTURE_STUDY":
        raise RuntimeError("research layer mismatch")
    if contract["evidentiary_status"] != "NON_EVIDENTIARY":
        raise RuntimeError("evidentiary status mismatch")
    if contract["data_authority"]["development_seeds"] != [501, 502]:
        raise RuntimeError("development-seed binding mismatch")
    if not contract["data_authority"]["official_test_forbidden"]:
        raise RuntimeError("official TEST must remain forbidden")
    if contract["order_family"]["pairs_per_seed"] != 12:
        raise RuntimeError("order-pair count mismatch")
    if contract["corpus"]["probe_episode_count_per_seed"] != 16:
        raise RuntimeError("probe-count binding mismatch")
    if contract["native_path"]["similarity_threshold"] != 0.66:
        raise RuntimeError("similarity-threshold binding mismatch")
    for path, expected in contract["source_binding"].items():
        if path == "main_sha":
            continue
        observed = _git_blob(path)
        if observed != expected:
            raise RuntimeError(f"source blob mismatch for {path}: {observed} != {expected}")
    reference = json.loads(Path("configs/v05_reference.json").read_text(encoding="utf-8"))
    if reference["development_seeds"] != [501, 502]:
        raise RuntimeError("reference DEV seeds changed")
    if float(reference["assembly_similarity_threshold"]) != 0.66:
        raise RuntimeError("reference assembly threshold changed")


def _episode_row(episode: Any, patterns: tuple[Any, ...]) -> dict[str, Any]:
    return {
        "episode_id": episode.episode_id,
        "future_event": episode.future_event,
        "rewarded_action": episode.rewarded_action,
        "patterns": [pattern.as_dict() for pattern in patterns],
    }


def _generate_corpus(seed: int, contract: dict[str, Any]) -> dict[str, Any]:
    brain = IntegratedV05Brain(
        V05BrainConfig(
            topology_seed=41,
            enable_assembly=False,
            enable_prediction=False,
            enable_action=False,
        )
    )
    adaptation_count = int(contract["corpus"]["adaptation_episode_count_per_seed"])
    probe_count = int(contract["corpus"]["probe_episode_count_per_seed"])
    probe_condition = str(contract["corpus"]["probe_condition"])

    adaptation: list[dict[str, Any]] = []
    adaptation_objects: list[tuple[Any, tuple[Any, ...]]] = []
    for episode in training_episodes(seed=seed, count=adaptation_count):
        result = brain.process_episode(
            episode.pulses,
            learn_assembly=False,
            learn_field=True,
            episode_id=episode.episode_id,
            explore_action=False,
        )
        patterns = tuple(result.patterns)
        adaptation.append(_episode_row(episode, patterns))
        adaptation_objects.append((episode, patterns))

    probe_start = brain.current_time_ms + 100.0
    probes: list[dict[str, Any]] = []
    probe_objects: list[tuple[Any, tuple[Any, ...]]] = []
    for episode in held_out_episodes(
        seed=seed,
        count=probe_count,
        condition=probe_condition,
        start_ms=probe_start,
    ):
        result = brain.process_episode(
            episode.pulses,
            learn_assembly=False,
            learn_field=False,
            episode_id=episode.episode_id,
            explore_action=False,
        )
        patterns = tuple(result.patterns)
        probes.append(_episode_row(episode, patterns))
        probe_objects.append((episode, patterns))

    manifest = {
        "seed": seed,
        "adaptation": adaptation,
        "probes": probes,
        "adaptation_count": len(adaptation),
        "probe_count": len(probes),
        "adaptation_pattern_count": sum(len(row["patterns"]) for row in adaptation),
        "probe_pattern_count": sum(len(row["patterns"]) for row in probes),
    }
    manifest["sha256"] = _sha256(manifest)
    return {
        "manifest": manifest,
        "adaptation_objects": adaptation_objects,
        "probe_objects": probe_objects,
    }


def _write_json_fsync(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def _write_jsonl_fsync(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(_canonical(row) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _strongest(activations: list[Any]) -> Any | None:
    usable = [row for row in activations if row.mature and not row.suppressed]
    return max(
        usable,
        key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
        default=None,
    )


def _reward(action: str | None, expected: str | None) -> float:
    if expected is None:
        return 0.0
    return 1.0 if action == expected else -0.35


def _derive_order(
    candidate_id: str,
    source_main_sha: str,
    development_seed: int,
    pair_index: int,
    count: int,
) -> tuple[list[int], int]:
    material = f"{candidate_id}|{source_main_sha}|{development_seed}|{pair_index}"
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    order_seed = int.from_bytes(digest[:8], "big")
    order = list(range(count))
    random.Random(order_seed).shuffle(order)
    return order, order_seed


def _final_assignments(
    memory: TemporalAssemblyMemory,
    adaptation: list[tuple[Any, tuple[Any, ...]]],
    threshold: float,
) -> dict[str, str | None]:
    assignments: dict[str, str | None] = {}
    for episode_index, (_, patterns) in enumerate(adaptation):
        for pattern_index, pattern in enumerate(patterns):
            key = f"e{episode_index:03d}-p{pattern_index:03d}"
            candidate, similarity = memory.best_match(pattern)
            if (
                candidate is not None
                and similarity >= threshold
                and candidate.episode_count >= memory.config.mature_episodes
            ):
                assignments[key] = candidate.assembly_id
            else:
                assignments[key] = None
    return assignments


def _run_arm(
    adaptation: list[tuple[Any, tuple[Any, ...]]],
    probes: list[tuple[Any, tuple[Any, ...]]],
    order: list[int],
    threshold: float,
) -> dict[str, Any]:
    memory = TemporalAssemblyMemory(
        AssemblyConfig(similarity_threshold=threshold, mature_episodes=3)
    )
    predictor = AssemblyPredictor()
    action_policy = AssemblyActionPolicy()
    replay_tick = 1

    for episode_index in order:
        episode, patterns = adaptation[episode_index]
        activations: list[Any] = []
        for pattern_index, pattern in enumerate(patterns):
            activation = memory.observe(
                pattern,
                time_ms=float(replay_tick) + pattern_index / 1000.0,
                episode_id=episode.episode_id,
                learn=True,
            )
            replay_tick += 1
            if activation is not None:
                activations.append(activation)
        strongest = _strongest(activations)
        predictor.predict(strongest)
        action = action_policy.choose(strongest, explore=True)
        predictor.observe(strongest, episode.future_event)
        action_policy.reward(_reward(action.action, episode.rewarded_action))

    assignments = _final_assignments(memory, adaptation, threshold)
    mature_count = sum(
        candidate.episode_count >= memory.config.mature_episodes
        for candidate in memory.candidates.values()
    )

    probe_rows: list[dict[str, Any]] = []
    correct = 0
    covered = 0
    for probe_index, (episode, patterns) in enumerate(probes):
        activations = []
        for pattern_index, pattern in enumerate(patterns):
            activation = memory.observe(
                pattern,
                time_ms=float(replay_tick) + pattern_index / 1000.0,
                episode_id=episode.episode_id,
                learn=False,
            )
            replay_tick += 1
            if activation is not None:
                activations.append(activation)
        strongest = _strongest(activations)
        prediction = predictor.predict(strongest)
        action = action_policy.choose(strongest, explore=False)
        covered += prediction.value is not None
        correct += prediction.value == episode.future_event
        probe_rows.append(
            {
                "probe_index": probe_index,
                "episode_id": episode.episode_id,
                "expected_prediction": episode.future_event,
                "prediction": prediction.value,
                "action": action.action,
                "assembly_id": strongest.assembly_id if strongest is not None else None,
            }
        )

    probe_count = len(probe_rows)
    return {
        "assignments": assignments,
        "mature_assembly_count": mature_count,
        "probe_rows": probe_rows,
        "prediction_coverage": covered / probe_count if probe_count else 0.0,
        "prediction_accuracy": correct / probe_count if probe_count else 0.0,
    }


def _coclustering_disagreement(
    left: dict[str, str | None], right: dict[str, str | None]
) -> float:
    keys = sorted(left)
    if keys != sorted(right):
        raise RuntimeError("assignment key mismatch")
    disagreements = 0
    comparisons = 0
    for index, first in enumerate(keys):
        for second in keys[index + 1 :]:
            left_same = left[first] is not None and left[first] == left[second]
            right_same = right[first] is not None and right[first] == right[second]
            disagreements += left_same != right_same
            comparisons += 1
    return disagreements / comparisons if comparisons else 0.0


def _build_comparator(
    adaptation: list[tuple[Any, tuple[Any, ...]]],
    probes: list[tuple[Any, tuple[Any, ...]]],
    threshold: float,
) -> dict[str, Any]:
    flat: list[tuple[int, int, Any]] = []
    for episode_index, (_, patterns) in enumerate(adaptation):
        for pattern_index, pattern in enumerate(patterns):
            flat.append((episode_index, pattern_index, pattern))
    parent = list(range(len(flat)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        a = find(left)
        b = find(right)
        if a != b:
            parent[max(a, b)] = min(a, b)

    for left in range(len(flat)):
        for right in range(left + 1, len(flat)):
            if pattern_similarity(flat[left][2], flat[right][2]) >= threshold:
                union(left, right)

    groups: dict[int, list[int]] = {}
    for index in range(len(flat)):
        groups.setdefault(find(index), []).append(index)

    components: list[dict[str, Any]] = []
    for members in groups.values():
        member_keys = [f"e{flat[i][0]:03d}-p{flat[i][1]:03d}" for i in members]
        component_id = "cc-" + _sha256(sorted(member_keys))[:12]
        episode_ids = {adaptation[flat[i][0]][0].episode_id for i in members}
        components.append(
            {
                "component_id": component_id,
                "members": members,
                "member_keys": sorted(member_keys),
                "mature": len(episode_ids) >= 3,
                "episode_count": len(episode_ids),
            }
        )
    components.sort(key=lambda row: row["component_id"])
    mature = [row for row in components if row["mature"]]

    def component_for_patterns(patterns: tuple[Any, ...]) -> str | None:
        best_id: str | None = None
        best_score = -1.0
        for component in mature:
            score = max(
                (
                    pattern_similarity(pattern, flat[index][2])
                    for pattern in patterns
                    for index in component["members"]
                ),
                default=0.0,
            )
            component_id = str(component["component_id"])
            if score > best_score or (score == best_score and best_id is not None and component_id < best_id):
                best_id = component_id
                best_score = score
        return best_id if best_id is not None and best_score >= threshold else None

    counts: dict[str, dict[str, int]] = {}
    for episode, patterns in adaptation:
        component_id = component_for_patterns(patterns)
        if component_id is None or episode.future_event is None:
            continue
        table = counts.setdefault(component_id, {})
        table[episode.future_event] = table.get(episode.future_event, 0) + 1

    def predict(component_id: str | None) -> str | None:
        if component_id is None:
            return None
        table = counts.get(component_id, {})
        if not table:
            return None
        return max(sorted(table), key=lambda value: table[value])

    probe_rows: list[dict[str, Any]] = []
    covered = 0
    correct = 0
    for probe_index, (episode, patterns) in enumerate(probes):
        component_id = component_for_patterns(patterns)
        prediction = predict(component_id)
        covered += prediction is not None
        correct += prediction == episode.future_event
        probe_rows.append(
            {
                "probe_index": probe_index,
                "episode_id": episode.episode_id,
                "component_id": component_id,
                "prediction": prediction,
                "expected_prediction": episode.future_event,
            }
        )
    probe_count = len(probe_rows)
    return {
        "component_count": len(components),
        "mature_component_count": len(mature),
        "prediction_coverage": covered / probe_count if probe_count else 0.0,
        "prediction_accuracy": correct / probe_count if probe_count else 0.0,
        "probe_rows": probe_rows,
    }


def _summarize(raw_rows: list[dict[str, Any]], seeds: list[int]) -> dict[str, Any]:
    by_seed: dict[int, dict[str, int]] = {}
    for seed in seeds:
        pair_rows = [
            row for row in raw_rows if row["row_type"] == "pair" and row["seed"] == seed
        ]
        by_seed[seed] = {
            "representation_divergent_pairs": sum(
                bool(row["representation_divergent"]) for row in pair_rows
            ),
            "prediction_support_pairs": sum(
                int(row["prediction_disagreement_count"]) >= 2 for row in pair_rows
            ),
            "joint_representation_and_prediction_support_pairs": sum(
                bool(row["representation_divergent"])
                and int(row["prediction_disagreement_count"]) >= 2
                for row in pair_rows
            ),
        }

    rep_counts = [by_seed[seed]["representation_divergent_pairs"] for seed in seeds]
    pred_counts = [by_seed[seed]["prediction_support_pairs"] for seed in seeds]
    if any(value < 4 for value in rep_counts):
        label = "NO_OR_LOW_SUPPORT"
    elif all(value >= 8 for value in rep_counts) and all(value >= 8 for value in pred_counts):
        label = "FUNCTIONAL_ORDER_LOCKIN_SIGNAL"
    elif all(value >= 8 for value in rep_counts):
        label = "REPRESENTATION_ONLY"
    else:
        label = "MIXED"
    return {
        "mapped_result": label,
        "per_seed": {str(key): value for key, value in sorted(by_seed.items())},
        "evidentiary_status": "NON_EVIDENTIARY_ARCHITECTURE_STUDY",
        "formal_scientific_evidence": false,
    }


def _execute(output_dir: Path, contract: dict[str, Any]) -> None:
    seeds = [int(value) for value in contract["data_authority"]["development_seeds"]]
    threshold = float(contract["native_path"]["similarity_threshold"])
    corpora = {seed: _generate_corpus(seed, contract) for seed in seeds}

    corpus_manifest = {
        "candidate_id": contract["candidate_id"],
        "source_main_sha": contract["source_binding"]["main_sha"],
        "evidentiary_status": "NON_EVIDENTIARY",
        "official_test_opened": False,
        "seeds": {str(seed): corpora[seed]["manifest"] for seed in seeds},
    }
    _write_json_fsync(output_dir / "corpus_manifest.json", corpus_manifest)

    raw_rows: list[dict[str, Any]] = []
    comparators: dict[str, Any] = {}
    for seed in seeds:
        adaptation = corpora[seed]["adaptation_objects"]
        probes = corpora[seed]["probe_objects"]
        comparator = _build_comparator(adaptation, probes, threshold)
        comparators[str(seed)] = comparator
        raw_rows.append(
            {
                "row_type": "comparator",
                "seed": seed,
                "component_count": comparator["component_count"],
                "mature_component_count": comparator["mature_component_count"],
                "prediction_coverage": comparator["prediction_coverage"],
                "prediction_accuracy": comparator["prediction_accuracy"],
            }
        )
        for pair_index in range(int(contract["order_family"]["pairs_per_seed"])):
            order_a, order_seed = _derive_order(
                contract["candidate_id"],
                contract["source_binding"]["main_sha"],
                seed,
                pair_index,
                len(adaptation),
            )
            order_b = list(reversed(order_a))
            arm_a = _run_arm(adaptation, probes, order_a, threshold)
            arm_b = _run_arm(adaptation, probes, order_b, threshold)
            disagreement = _coclustering_disagreement(
                arm_a["assignments"], arm_b["assignments"]
            )
            rep_divergent = (
                arm_a["mature_assembly_count"] != arm_b["mature_assembly_count"]
                or disagreement > 0.0
            )
            prediction_disagreement = sum(
                left["prediction"] != right["prediction"]
                for left, right in zip(
                    arm_a["probe_rows"], arm_b["probe_rows"], strict=True
                )
            )
            action_disagreement = sum(
                left["action"] != right["action"]
                for left, right in zip(
                    arm_a["probe_rows"], arm_b["probe_rows"], strict=True
                )
            )
            raw_rows.append(
                {
                    "row_type": "pair",
                    "seed": seed,
                    "pair_index": pair_index,
                    "order_seed": order_seed,
                    "order_a": order_a,
                    "order_b": order_b,
                    "mature_assembly_count_a": arm_a["mature_assembly_count"],
                    "mature_assembly_count_b": arm_b["mature_assembly_count"],
                    "pairwise_co_clustering_disagreement": disagreement,
                    "representation_divergent": rep_divergent,
                    "prediction_disagreement_count": prediction_disagreement,
                    "prediction_coverage_delta": (
                        arm_a["prediction_coverage"] - arm_b["prediction_coverage"]
                    ),
                    "prediction_accuracy_delta": (
                        arm_a["prediction_accuracy"] - arm_b["prediction_accuracy"]
                    ),
                    "descriptive_action_disagreement_count": action_disagreement,
                }
            )
            for left, right in zip(arm_a["probe_rows"], arm_b["probe_rows"], strict=True):
                raw_rows.append(
                    {
                        "row_type": "probe",
                        "seed": seed,
                        "pair_index": pair_index,
                        "probe_index": left["probe_index"],
                        "episode_id": left["episode_id"],
                        "expected_prediction": left["expected_prediction"],
                        "prediction_a": left["prediction"],
                        "prediction_b": right["prediction"],
                        "action_a": left["action"],
                        "action_b": right["action"],
                        "prediction_disagree": left["prediction"] != right["prediction"],
                        "action_disagree": left["action"] != right["action"],
                    }
                )

    metadata = {
        "candidate_id": contract["candidate_id"],
        "analyst_authority": contract["analyst_authority"],
        "source_binding": contract["source_binding"],
        "contract_sha256": hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest(),
        "evidentiary_status": "NON_EVIDENTIARY_ARCHITECTURE_STUDY",
        "official_test_opened": False,
        "formal_identity": None,
        "started": False,
        "raw_before_interpretation": True,
        "corpus_manifest_sha256": hashlib.sha256(
            (output_dir / "corpus_manifest.json").read_bytes()
        ).hexdigest(),
        "comparator": comparators,
    }
    _write_json_fsync(output_dir / "metadata.json", metadata)
    _write_jsonl_fsync(output_dir / "raw.jsonl", raw_rows)

    reloaded_rows = [
        json.loads(line)
        for line in (output_dir / "raw.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    summary = _summarize(reloaded_rows, seeds)
    summary["candidate_id"] = contract["candidate_id"]
    summary["analyst_authority"] = contract["analyst_authority"]
    summary["source_main_sha"] = contract["source_binding"]["main_sha"]
    summary["exploration_cycle"] = {"discovery_completed": 1, "architecture_completed": 1}
    summary["stop_for_fresh_analyst"] = True
    summary["formal_authority_used"] = False
    _write_json_fsync(output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/architecture/assembly_prototype_lockin_cycle1"),
    )
    args = parser.parse_args()
    contract = _load_contract()
    _verify_contract(contract)
    if args.preflight_only:
        print("preflight-ok")
        return
    _execute(args.output_dir, contract)


if __name__ == "__main__":
    main()
