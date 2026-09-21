from __future__ import annotations

import copy
import hashlib
import itertools
from importlib.metadata import version
import json
import platform
import random
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from sparkbrain.v05.evaluation import train_brain
from sparkbrain.v05.worlds import held_out_episodes

CANDIDATE_ID = "CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01"
SOURCE_SHA = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
CONTRACT_SHA = "52e14294d8e413a95c1dad387104bdeaa4468d39"
ANALYST_GENERATION = "EVA-20260921T105950+0900-R33-5A8C31E7"
ANALYST_COMMIT = "f22b345bceab464ac0fd593c11a7b6b99742af4f"
SURFACE_SEEDS = (1701, 1702, 1703, 1704)
TRAIN_COUNT = 24
HELD_OUT_GENERATOR_COUNT = 15
EPISODES_PER_ARM = 8
UNIFORM_CONTROL_COUNT = 64
BALANCED_RESERVOIR_COUNT = 256
BALANCED_CONTROL_COUNT = 64
MIN_ELIGIBLE_SET_COUNT = 320
EXPECTED_PROJECT_VERSION = "0.3.2.dev0"


def _median(values: list[float | int]) -> float:
    return float(statistics.median(values))


def _rng_seed(surface_seed: int, suffix: str) -> int:
    payload = f"{CANDIDATE_ID}|{surface_seed}|{suffix}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big", signed=False)


def _mature_label_counts(train_rows: list[Any], trained: Any) -> dict[str, dict[str, int]]:
    mature_ids = {
        assembly_id
        for assembly_id, candidate in trained.assemblies.candidates.items()
        if candidate.episode_count >= trained.assemblies.config.mature_episodes
    }
    counts: dict[str, dict[str, int]] = {}
    for row in train_rows:
        if row.assembly_id is None or row.motif_name is None or row.assembly_id not in mature_ids:
            continue
        table = counts.setdefault(row.assembly_id, {})
        table[row.motif_name] = table.get(row.motif_name, 0) + 1
    return counts


def _select_target(
    train_rows: list[Any],
    trained: Any,
) -> tuple[str, tuple[int, ...], dict[str, int]]:
    counts = _mature_label_counts(train_rows, trained)
    ranked: list[tuple[int, int, str]] = []
    for assembly_id, table in counts.items():
        x_count = int(table.get("motif_x", 0))
        y_count = int(table.get("motif_y", 0))
        ranked.append((x_count - y_count, x_count, assembly_id))
    ranked.sort(key=lambda row: (-row[0], -row[1], row[2]))
    if not ranked or ranked[0][0] <= 0:
        raise ValueError("INVALID_SURFACE:NO_POSITIVE_MOTIF_X_TARGET")
    _, _, assembly_id = ranked[0]
    candidate = trained.assemblies.candidates[assembly_id]
    target = tuple(sorted(int(unit_id) for unit_id in candidate.prototype.unit_ids))
    if not 2 <= len(target) <= 4:
        raise ValueError("INVALID_SURFACE:TARGET_CARDINALITY_OUTSIDE_2_4")
    return assembly_id, target, dict(counts[assembly_id])


def _strongest_mature(result: Any) -> Any | None:
    rows = [row for row in result.assembly_activations if row.mature and not row.suppressed]
    return max(
        rows,
        key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
        default=None,
    )


def _baseline_probe(trained: Any, surface_seed: int, target_assembly_id: str) -> tuple[Any, Any]:
    episode = held_out_episodes(
        seed=surface_seed,
        condition="jitter",
        count=1,
        start_ms=trained.current_time_ms + 100.0,
    )[0]
    if episode.motif_name != "motif_x":
        raise ValueError("INVALID_SURFACE:BASELINE_PROBE_NOT_MOTIF_X")
    brain = copy.deepcopy(trained)
    result = brain.process_episode(
        episode.pulses,
        learn_assembly=False,
        learn_field=False,
        metadata={"condition": episode.condition, "phase": "preformal-baseline"},
        episode_id=f"preformal-baseline-{surface_seed}",
        explore_action=False,
    )
    strongest = _strongest_mature(result)
    if strongest is None or strongest.assembly_id != target_assembly_id:
        raise ValueError("INVALID_SURFACE:BASELINE_STRONGEST_TARGET_MISMATCH")
    if result.prediction.value != episode.future_event:
        raise ValueError("INVALID_SURFACE:BASELINE_PREDICTION_MISMATCH")
    return episode, result


def _depth_two_reach(field: Any, unit_id: int, *, incoming: bool, internal_ids: set[int]) -> int:
    adjacency = field.incoming if incoming else field.outgoing
    reached: set[int] = set()
    frontier = {unit_id}
    for _depth in (1, 2):
        next_frontier: set[int] = set()
        for current in frontier:
            for edge in adjacency[current]:
                neighbor = edge.source_id if incoming else edge.target_id
                if neighbor in internal_ids:
                    reached.add(neighbor)
                next_frontier.add(neighbor)
        frontier = next_frontier
    return len(reached & internal_ids)


def _unit_features(
    trained: Any,
    baseline_result: Any,
) -> dict[int, tuple[int, int, int, int, int, int, int]]:
    field = trained.base.field
    receptor_ids = set(field.receptor_ids)
    internal_ids = set(field.units) - receptor_ids
    baseline_spike_counts = Counter(
        int(spike.unit_id)
        for spike in baseline_result.v04_result.spikes
        if int(spike.unit_id) in internal_ids
    )
    features: dict[int, tuple[int, int, int, int, int, int, int]] = {}
    for unit_id in sorted(internal_ids):
        unit = field.units[unit_id]
        incoming = field.incoming[unit_id]
        outgoing = field.outgoing[unit_id]
        features[unit_id] = (
            int(baseline_spike_counts.get(unit_id, 0)),
            int(bool(unit.excitatory)),
            len(incoming),
            len(outgoing),
            sum(edge.source_id in receptor_ids for edge in incoming),
            _depth_two_reach(field, unit_id, incoming=False, internal_ids=internal_ids),
            _depth_two_reach(field, unit_id, incoming=True, internal_ids=internal_ids),
        )
    return features


def _set_vector(
    unit_set: tuple[int, ...],
    unit_features: dict[int, tuple[int, int, int, int, int, int, int]],
) -> tuple[int, int, int, int, int, int, int]:
    return tuple(
        sum(unit_features[unit_id][j] for unit_id in unit_set)
        for j in range(7)
    )  # type: ignore[return-value]


def _build_controls(
    trained: Any,
    baseline_result: Any,
    target: tuple[int, ...],
    surface_seed: int,
) -> dict[str, Any]:
    field = trained.base.field
    internal_ids = sorted(set(field.units) - set(field.receptor_ids))
    target_set = set(target)
    pool = tuple(unit_id for unit_id in internal_ids if unit_id not in target_set)
    population = list(itertools.combinations(pool, len(target)))
    if len(population) < MIN_ELIGIBLE_SET_COUNT:
        raise ValueError("INVALID_SURFACE:COMPARATOR_POPULATION_LT_320")

    unit_features = _unit_features(trained, baseline_result)
    target_vector = _set_vector(target, unit_features)
    vectors = [_set_vector(combo, unit_features) for combo in population]

    uniform_rng = random.Random(_rng_seed(surface_seed, "uniform-v1"))
    uniform = sorted(
        population[index]
        for index in uniform_rng.sample(range(len(population)), UNIFORM_CONTROL_COUNT)
    )

    medians = [_median([vector[j] for vector in vectors]) for j in range(7)]
    mads = [
        _median([abs(float(vector[j]) - medians[j]) for vector in vectors])
        for j in range(7)
    ]
    scales = [max(mad, 1.0) for mad in mads]

    def distance(index: int) -> float:
        vector = vectors[index]
        return sum(
            abs(float(vector[j]) - float(target_vector[j])) / scales[j]
            for j in range(7)
        )

    ranked_indices = sorted(
        range(len(population)),
        key=lambda index: (distance(index), population[index]),
    )
    reservoir_indices = ranked_indices[:BALANCED_RESERVOIR_COUNT]
    if len(reservoir_indices) < BALANCED_RESERVOIR_COUNT:
        raise ValueError("INVALID_SURFACE:BALANCE_RESERVOIR_LT_256")

    balanced_rng = random.Random(_rng_seed(surface_seed, "balanced-v1"))
    balanced = sorted(
        population[index]
        for index in balanced_rng.sample(reservoir_indices, BALANCED_CONTROL_COUNT)
    )
    return {
        "eligible_pool_size": len(pool),
        "eligible_set_count": len(population),
        "target_vector": list(target_vector),
        "population_medians": medians,
        "population_mads": mads,
        "population_scales": scales,
        "uniform": [list(row) for row in uniform],
        "balanced": [list(row) for row in balanced],
        "overlap_count": len(set(uniform) & set(balanced)),
    }


def _future_episodes(trained: Any, surface_seed: int) -> list[Any]:
    rows = held_out_episodes(
        seed=surface_seed,
        condition="jitter",
        count=HELD_OUT_GENERATOR_COUNT,
        start_ms=trained.current_time_ms + 100.0,
    )
    selected = [row for row in rows if row.motif_name == "motif_x"][:EPISODES_PER_ARM]
    if len(selected) != EPISODES_PER_ARM:
        raise ValueError("INVALID_SURFACE:EIGHT_MOTIF_X_EPISODES_UNAVAILABLE")
    return selected


def _spike_counts(result: Any) -> Counter[int]:
    return Counter(int(spike.unit_id) for spike in result.v04_result.spikes)


def _evaluate_single_episode(trained: Any, episode: Any, suppressed: tuple[int, ...]) -> Any:
    brain = copy.deepcopy(trained)
    if suppressed:
        brain.suppress_units(suppressed)
    return brain.process_episode(
        episode.pulses,
        learn_assembly=False,
        learn_field=False,
        metadata={"condition": episode.condition, "phase": "preformal"},
        episode_id=(
            f"preformal-{episode.episode_id}-lesion-"
            f"{','.join(map(str, suppressed)) or 'sham'}"
        ),
        explore_action=False,
    )


def _evaluate_arm(
    trained: Any,
    episodes: list[Any],
    suppressed: tuple[int, ...],
    sham_spikes: list[Counter[int]] | None,
) -> dict[str, Any]:
    results = [_evaluate_single_episode(trained, episode, suppressed) for episode in episodes]
    successes = [
        int(result.prediction.value == episode.future_event)
        for result, episode in zip(results, episodes, strict=True)
    ]
    accuracy = sum(successes) / len(successes)
    footprint: list[tuple[int, int]] = []
    if sham_spikes is not None:
        for result, paired_sham in zip(results, sham_spikes, strict=True):
            counts = _spike_counts(result)
            all_units = set(counts) | set(paired_sham)
            footprint_count_delta = abs(sum(counts.values()) - sum(paired_sham.values()))
            footprint_unit_l1 = sum(abs(counts[u] - paired_sham[u]) for u in all_units)
            footprint.append((footprint_count_delta, footprint_unit_l1))
    return {
        "accuracy": accuracy,
        "successes": successes,
        "spike_counts": [dict(sorted(_spike_counts(result).items())) for result in results],
        "footprint": [
            sum(row[j] for row in footprint) / len(footprint)
            for j in range(2)
        ] if footprint else None,
    }


def _run_surface(surface_seed: int) -> dict[str, Any]:
    trained, train_rows = train_brain(surface_seed, count=TRAIN_COUNT)
    target_assembly_id, target, label_counts = _select_target(train_rows, trained)
    baseline_episode, baseline_result = _baseline_probe(trained, surface_seed, target_assembly_id)
    controls = _build_controls(trained, baseline_result, target, surface_seed)
    episodes = _future_episodes(trained, surface_seed)

    sham = _evaluate_arm(trained, episodes, (), None)
    sham_spikes = [
        Counter({int(k): int(v) for k, v in row.items()})
        for row in sham["spike_counts"]
    ]
    target_arm = _evaluate_arm(trained, episodes, target, sham_spikes)

    uniform_rows: list[dict[str, Any]] = []
    for units in controls["uniform"]:
        unit_tuple = tuple(int(value) for value in units)
        uniform_rows.append(
            {"units": units, **_evaluate_arm(trained, episodes, unit_tuple, sham_spikes)}
        )

    balanced_rows: list[dict[str, Any]] = []
    for units in controls["balanced"]:
        unit_tuple = tuple(int(value) for value in units)
        balanced_rows.append(
            {"units": units, **_evaluate_arm(trained, episodes, unit_tuple, sham_spikes)}
        )

    sham_accuracy = float(sham["accuracy"])
    target_impairment = sham_accuracy - float(target_arm["accuracy"])
    uniform_impairments = [sham_accuracy - float(row["accuracy"]) for row in uniform_rows]
    balanced_impairments = [sham_accuracy - float(row["accuracy"]) for row in balanced_rows]
    d_uniform = target_impairment - _median(uniform_impairments)
    d_balanced = target_impairment - _median(balanced_impairments)

    target_fp = tuple(float(value) for value in target_arm["footprint"])
    control_fps = [
        tuple(float(value) for value in row["footprint"])
        for row in [*uniform_rows, *balanced_rows]
    ]
    fp_min = tuple(min(row[j] for row in control_fps) for j in range(2))
    fp_max = tuple(max(row[j] for row in control_fps) for j in range(2))
    footprint_in_support = all(fp_min[j] <= target_fp[j] <= fp_max[j] for j in range(2))

    return {
        "surface_seed": surface_seed,
        "trained_current_time_ms": trained.current_time_ms,
        "target_assembly_id": target_assembly_id,
        "target_units": list(target),
        "target_label_counts": label_counts,
        "baseline_episode_id": baseline_episode.episode_id,
        "baseline_prediction": baseline_result.prediction.value,
        "baseline_expected_prediction": baseline_episode.future_event,
        "controls": controls,
        "future_episode_ids": [episode.episode_id for episode in episodes],
        "sham": {"accuracy": sham_accuracy, "successes": sham["successes"]},
        "target": {
            "accuracy": target_arm["accuracy"],
            "successes": target_arm["successes"],
            "impairment": target_impairment,
            "footprint": list(target_fp),
        },
        "uniform": {
            "impairment_median": _median(uniform_impairments),
            "impairments": uniform_impairments,
            "arms": [
                {
                    "units": row["units"],
                    "accuracy": row["accuracy"],
                    "successes": row["successes"],
                    "footprint": row["footprint"],
                }
                for row in uniform_rows
            ],
        },
        "balanced": {
            "impairment_median": _median(balanced_impairments),
            "impairments": balanced_impairments,
            "arms": [
                {
                    "units": row["units"],
                    "accuracy": row["accuracy"],
                    "successes": row["successes"],
                    "footprint": row["footprint"],
                }
                for row in balanced_rows
            ],
        },
        "D_uniform": d_uniform,
        "D_balanced": d_balanced,
        "footprint_support": {
            "target": list(target_fp),
            "ordinary_min": list(fp_min),
            "ordinary_max": list(fp_max),
            "in_support": footprint_in_support,
        },
    }


def _runtime_binding() -> dict[str, Any]:
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "project_version_expected": EXPECTED_PROJECT_VERSION,
    }


def _classify_surface(surface: dict[str, Any]) -> str:
    if float(surface["D_uniform"]) <= 0.0 or float(surface["D_balanced"]) <= 0.0:
        return "REJECT_CURRENT_OBJECT_TERMINAL"
    if not bool(surface["footprint_support"]["in_support"]):
        return "HOLD_MECHANISM_UNRESOLVED_TERMINAL"
    return "CONTINUE_FIXED_NEXT_SURFACE"


def main() -> int:
    if version("sparkbrain-research") != EXPECTED_PROJECT_VERSION:
        raise RuntimeError(
            "RUNTIME_SOURCE_RESOURCE_PRIVILEGE_MISMATCH:"
            f"project_version={version('sparkbrain-research')}"
        )
    if sys.version_info[:3] != (3, 11, 13):
        raise RuntimeError(
            "RUNTIME_SOURCE_RESOURCE_PRIVILEGE_MISMATCH:"
            f"python={platform.python_version()}"
        )

    output: dict[str, Any] = {
        "schema_version": 2,
        "candidate_id": CANDIDATE_ID,
        "claim_ceiling": "MECHANISM",
        "layer": "PRE_FORMAL",
        "preformal_eligible": True,
        "preformal_readiness": "READY",
        "analyst_generation": ANALYST_GENERATION,
        "analyst_commit": ANALYST_COMMIT,
        "source_sha": SOURCE_SHA,
        "contract_sha": CONTRACT_SHA,
        "scientific_identity_consumed": False,
        "formal": False,
        "official_scoring": False,
        "runtime_binding": _runtime_binding(),
        "fixed_inputs": {
            "surface_seeds": list(SURFACE_SEEDS),
            "train_count": TRAIN_COUNT,
            "held_out_generator_count": HELD_OUT_GENERATOR_COUNT,
            "episodes_per_arm": EPISODES_PER_ARM,
            "uniform_controls_per_surface": UNIFORM_CONTROL_COUNT,
            "balanced_reservoir_count": BALANCED_RESERVOIR_COUNT,
            "balanced_controls_per_surface": BALANCED_CONTROL_COUNT,
            "min_eligible_set_count": MIN_ELIGIBLE_SET_COUNT,
        },
        "surfaces": [],
        "terminal": None,
        "terminal_detail": None,
    }

    try:
        for surface_seed in SURFACE_SEEDS:
            surface = _run_surface(surface_seed)
            output["surfaces"].append(surface)
            disposition = _classify_surface(surface)
            if disposition == "REJECT_CURRENT_OBJECT_TERMINAL":
                output["terminal"] = disposition
                output["terminal_detail"] = {
                    "surface_seed": surface_seed,
                    "D_uniform": surface["D_uniform"],
                    "D_balanced": surface["D_balanced"],
                }
                break
            if disposition == "HOLD_MECHANISM_UNRESOLVED_TERMINAL":
                output["terminal"] = disposition
                output["terminal_detail"] = {
                    "surface_seed": surface_seed,
                    "footprint_support": surface["footprint_support"],
                }
                break
        else:
            output["terminal"] = "ALL_FIXED_SURFACES_POSITIVE_IN_SUPPORT_STOP_FRESH_ANALYST"
    except ValueError as exc:
        message = str(exc)
        if message.startswith("INVALID_SURFACE:"):
            output["terminal"] = "HOLD_METHOD_LIMITED_TERMINAL"
            output["terminal_detail"] = {"reason": message}
        else:
            raise

    result_path = Path("preformal-result.json")
    result_path.write_text(json.dumps(output, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
