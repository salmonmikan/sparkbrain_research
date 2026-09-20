from __future__ import annotations

import argparse
import copy
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from sparkbrain.v05.evaluation import train_brain
from sparkbrain.v05.worlds import MOTIF_X, make_episode

CANDIDATE_ID = "CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01"
DEV_SEEDS = (501, 502)
TRAIN_COUNT = 24
EXPECTED = "outcome-0"
MAX_TARGET_UNITS = 4
RANDOM_CONTROL_OFFSET = 7919


def _strongest(result: Any) -> Any | None:
    rows = [row for row in result.assembly_activations if row.mature and not row.suppressed]
    return max(
        rows,
        key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
        default=None,
    )


def _run_baseline_probe(brain: Any, probe: Any) -> Any:
    return brain.process_episode(
        probe.pulses,
        learn_assembly=False,
        learn_field=False,
        metadata={"condition": "motif", "phase": "main_arch_comparator_feasibility"},
        episode_id=probe.episode_id,
        explore_action=False,
    )


def _two_hop_out(field: Any, unit_id: int, internal_ids: set[int]) -> int:
    reached: set[int] = set()
    first = {
        edge.target_id
        for edge in field.outgoing[unit_id]
        if edge.target_id in internal_ids
    }
    reached.update(first)
    for neighbor in first:
        reached.update(
            edge.target_id
            for edge in field.outgoing[neighbor]
            if edge.target_id in internal_ids
        )
    reached.discard(unit_id)
    return len(reached)


def _two_hop_in(field: Any, unit_id: int, internal_ids: set[int]) -> int:
    reached: set[int] = set()
    first = {
        edge.source_id
        for edge in field.incoming[unit_id]
        if edge.source_id in internal_ids
    }
    reached.update(first)
    for neighbor in first:
        reached.update(
            edge.source_id
            for edge in field.incoming[neighbor]
            if edge.source_id in internal_ids
        )
    reached.discard(unit_id)
    return len(reached)


def _signature(
    field: Any,
    unit_ids: tuple[int, ...],
    baseline_spikes: Counter[int],
    internal_ids: set[int],
    receptor_ids: set[int],
) -> tuple[int, int, int, int, int, int, int]:
    return (
        sum(baseline_spikes[unit_id] for unit_id in unit_ids),
        sum(bool(field.units[unit_id].excitatory) for unit_id in unit_ids),
        sum(len(field.incoming[unit_id]) for unit_id in unit_ids),
        sum(len(field.outgoing[unit_id]) for unit_id in unit_ids),
        sum(
            sum(edge.source_id in receptor_ids for edge in field.incoming[unit_id])
            for unit_id in unit_ids
        ),
        sum(_two_hop_out(field, unit_id, internal_ids) for unit_id in unit_ids),
        sum(_two_hop_in(field, unit_id, internal_ids) for unit_id in unit_ids),
    )


def _signature_dict(signature: tuple[int, ...]) -> dict[str, int]:
    names = (
        "baseline_probe_spikes",
        "excitatory_units",
        "incoming_edges",
        "outgoing_edges",
        "receptor_incoming_edges",
        "two_hop_out_reach_sum",
        "two_hop_in_reach_sum",
    )
    return dict(zip(names, signature, strict=True))


def _random_control(
    eligible: tuple[int, ...],
    k: int,
    seed: int,
    primary: tuple[int, ...],
) -> tuple[int, ...] | None:
    values = list(eligible)
    rng = random.Random(RANDOM_CONTROL_OFFSET + seed)
    rng.shuffle(values)
    if len(values) < k:
        return None
    for offset in range(len(values)):
        rotated = values[offset:] + values[:offset]
        candidate = tuple(sorted(rotated[:k]))
        if candidate != primary:
            return candidate
    return None


def _invalid(seed: int, reason: str, **details: Any) -> dict[str, Any]:
    return {"seed": seed, "status": "INVALID", "reason": reason, **details}


def _inspect_seed(seed: int) -> dict[str, Any]:
    trained, train_rows = train_brain(seed, count=TRAIN_COUNT)
    label_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in train_rows:
        if row.assembly_id is None or row.motif_name is None or not row.mature:
            continue
        label_counts[row.assembly_id][row.motif_name] += 1

    ranked: list[tuple[int, str]] = []
    for assembly_id, counts in label_counts.items():
        delta = counts["motif_x"] - counts["motif_y"]
        if delta > 0:
            ranked.append((delta, assembly_id))
    if not ranked:
        return _invalid(seed, "NO_POSITIVE_MOTIF_X_MATURE_ASSEMBLY")

    ranked.sort(key=lambda row: (-row[0], row[1]))
    selectivity_delta, selected_id = ranked[0]
    selected = trained.assemblies.candidates.get(selected_id)
    if selected is None:
        return _invalid(seed, "SELECTED_ASSEMBLY_MISSING")

    target_units = tuple(sorted(selected.prototype.unit_ids))
    if not 1 <= len(target_units) <= MAX_TARGET_UNITS:
        return _invalid(
            seed,
            "TARGET_PROTOTYPE_CARDINALITY_OUT_OF_BOUNDS",
            target_unit_count=len(target_units),
        )

    probe = make_episode(
        seed=seed,
        index=TRAIN_COUNT,
        motif=MOTIF_X,
        condition="motif",
        start_ms=trained.current_time_ms + 100.0,
    )
    baseline_brain = copy.deepcopy(trained)
    baseline_result = _run_baseline_probe(baseline_brain, probe)
    baseline_activation = _strongest(baseline_result)
    baseline_prediction = baseline_result.prediction.value
    if baseline_activation is None:
        return _invalid(
            seed,
            "NO_BASELINE_MATURE_ACTIVATION",
            baseline_prediction=baseline_prediction,
        )
    if baseline_activation.assembly_id != selected_id or baseline_prediction != EXPECTED:
        return _invalid(
            seed,
            "BASELINE_CONTRACT_FAILED",
            selected_assembly_id=selected_id,
            baseline_assembly_id=baseline_activation.assembly_id,
            baseline_prediction=baseline_prediction,
        )

    field = baseline_brain.base.field
    receptor_ids = set(field.receptor_ids)
    internal_ids = set(field.units) - receptor_ids
    eligible = tuple(sorted(internal_ids - set(target_units)))
    if len(eligible) < len(target_units):
        return _invalid(seed, "INSUFFICIENT_NONMEMBER_COMPARATOR_POOL")

    baseline_spikes = Counter(spike.unit_id for spike in baseline_result.v04_result.spikes)
    target_signature = _signature(
        field,
        target_units,
        baseline_spikes,
        internal_ids,
        receptor_ids,
    )

    primary: tuple[int, ...] | None = None
    checked = 0
    for candidate in itertools.combinations(eligible, len(target_units)):
        checked += 1
        candidate_signature = _signature(
            field,
            candidate,
            baseline_spikes,
            internal_ids,
            receptor_ids,
        )
        if candidate_signature == target_signature:
            primary = candidate
            break

    row: dict[str, Any] = {
        "seed": seed,
        "status": "VALID",
        "selected_assembly_id": selected_id,
        "selectivity_delta": selectivity_delta,
        "target_units": list(target_units),
        "target_signature": _signature_dict(target_signature),
        "baseline_prediction": baseline_prediction,
        "baseline_strongest_assembly_id": baseline_activation.assembly_id,
        "baseline_similarity": baseline_activation.similarity,
        "baseline_total_spikes": len(baseline_result.v04_result.spikes),
        "eligible_pool_size": len(eligible),
        "combinations_checked_until_first_match_or_exhaustion": checked,
        "exact_comparator_found": primary is not None,
    }
    if primary is not None:
        random_control = _random_control(eligible, len(target_units), seed, primary)
        if random_control is None:
            return {**row, "status": "INVALID", "reason": "DISTINCT_RANDOM_CONTROL_UNAVAILABLE"}
        primary_signature = _signature(
            field,
            primary,
            baseline_spikes,
            internal_ids,
            receptor_ids,
        )
        random_signature = _signature(
            field,
            random_control,
            baseline_spikes,
            internal_ids,
            receptor_ids,
        )
        row.update(
            {
                "primary_exact_comparator": list(primary),
                "primary_exact_comparator_signature": _signature_dict(primary_signature),
                "generic_random_control": list(random_control),
                "generic_random_control_signature": _signature_dict(random_signature),
                "sham_suppressed_units": [],
            }
        )
    return row


def run() -> dict[str, Any]:
    rows = [_inspect_seed(seed) for seed in DEV_SEEDS]
    feasible = [
        row
        for row in rows
        if row.get("status") == "VALID" and row.get("exact_comparator_found")
    ]
    invalid = [row for row in rows if row.get("status") == "INVALID"]
    if feasible:
        selected = feasible[0]
        terminal = "MATCHED_LOAD_COMPARATOR_CONTRACT_FEASIBLE"
    elif invalid:
        selected = None
        terminal = "SUPPORTED_REACHABILITY_OR_API_CONTRACT_INVALID"
    else:
        selected = None
        terminal = "EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE"
    return {
        "candidate_id": CANDIDATE_ID,
        "cycle": 1,
        "research_layer": "ARCHITECTURE_STUDY",
        "claim_ceiling": "MECHANISM",
        "evidentiary_status": "NON_EVIDENTIARY",
        "intervention_outcomes_executed": 0,
        "fixed_development_seeds": list(DEV_SEEDS),
        "seed_rows": rows,
        "selected_future_surface": selected,
        "terminal": terminal,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
