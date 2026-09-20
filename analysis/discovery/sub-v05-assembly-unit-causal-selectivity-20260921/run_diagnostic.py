from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from sparkbrain.v05.evaluation import train_brain
from sparkbrain.v05.worlds import MOTIF_X, make_episode

SEED = 501
TRAIN_COUNT = 24
EXPECTED = "outcome-0"
MAX_TARGET_UNITS = 4


def _strongest(result: Any) -> Any | None:
    rows = [row for row in result.assembly_activations if row.mature and not row.suppressed]
    return max(
        rows,
        key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
        default=None,
    )


def _run_probe(brain: Any, probe: Any) -> Any:
    return brain.process_episode(
        probe.pulses,
        learn_assembly=False,
        learn_field=False,
        metadata={"condition": "motif", "phase": "sub_dev_causal_selectivity"},
        episode_id=probe.episode_id,
        explore_action=False,
    )


def _invalid(reason: str, **details: Any) -> dict[str, Any]:
    return {
        "terminal": "INVALID_DIAGNOSTIC",
        "invalid_reason": reason,
        "details": details,
    }


def run() -> dict[str, Any]:
    trained, train_rows = train_brain(SEED, count=TRAIN_COUNT)

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
        return _invalid("NO_POSITIVE_MOTIF_X_MATURE_ASSEMBLY")

    ranked.sort(key=lambda row: (-row[0], row[1]))
    selectivity_delta, selected_id = ranked[0]
    selected = trained.assemblies.candidates.get(selected_id)
    if selected is None:
        return _invalid("SELECTED_ASSEMBLY_MISSING", selected_id=selected_id)

    probe = make_episode(
        seed=SEED,
        index=TRAIN_COUNT,
        motif=MOTIF_X,
        condition="motif",
        start_ms=trained.current_time_ms + 100.0,
    )

    baseline_result = _run_probe(copy.deepcopy(trained), probe)
    baseline_activation = _strongest(baseline_result)
    baseline_prediction = baseline_result.prediction.value
    if baseline_activation is None:
        return _invalid(
            "NO_BASELINE_MATURE_ACTIVATION",
            selected_id=selected_id,
            baseline_prediction=baseline_prediction,
        )
    if baseline_activation.assembly_id != selected_id or baseline_prediction != EXPECTED:
        return _invalid(
            "BASELINE_CONTRACT_FAILED",
            selected_id=selected_id,
            baseline_assembly_id=baseline_activation.assembly_id,
            baseline_prediction=baseline_prediction,
            expected_prediction=EXPECTED,
        )

    prototype_units = tuple(sorted(selected.prototype.unit_ids))
    k = min(MAX_TARGET_UNITS, len(prototype_units))
    if k < 1:
        return _invalid("EMPTY_SELECTED_ASSEMBLY_PROTOTYPE", selected_id=selected_id)

    baseline_spike_counts = Counter(spike.unit_id for spike in baseline_result.v04_result.spikes)
    target_units = sorted(
        prototype_units,
        key=lambda unit_id: (-baseline_spike_counts[unit_id], unit_id),
    )[:k]

    internal_units = (
        set(trained.base.field.units)
        - set(trained.base.field.receptor_ids)
        - set(prototype_units)
    )
    if len(internal_units) < k:
        return _invalid(
            "INSUFFICIENT_NONMEMBER_COMPARATOR_POOL",
            comparator_pool_size=len(internal_units),
            required=k,
        )

    available = set(internal_units)
    comparator_units: list[int] = []
    match_rows: list[dict[str, int]] = []
    for target_unit in target_units:
        comparator = min(
            available,
            key=lambda unit_id: (
                abs(baseline_spike_counts[unit_id] - baseline_spike_counts[target_unit]),
                unit_id,
            ),
        )
        available.remove(comparator)
        comparator_units.append(comparator)
        match_rows.append(
            {
                "target_unit": target_unit,
                "target_baseline_spikes": baseline_spike_counts[target_unit],
                "comparator_unit": comparator,
                "comparator_baseline_spikes": baseline_spike_counts[comparator],
            }
        )

    targeted_brain = copy.deepcopy(trained)
    targeted_brain.suppress_units(target_units)
    targeted_result = _run_probe(targeted_brain, probe)

    comparator_brain = copy.deepcopy(trained)
    comparator_brain.suppress_units(comparator_units)
    comparator_result = _run_probe(comparator_brain, probe)

    targeted_prediction = targeted_result.prediction.value
    comparator_prediction = comparator_result.prediction.value
    if targeted_prediction != EXPECTED and comparator_prediction == EXPECTED:
        terminal = "SELECTIVE_TARGETED_FUNCTION_LOSS"
    elif targeted_prediction != EXPECTED and comparator_prediction != EXPECTED:
        terminal = "GENERIC_ACTIVITY_LESION_REDUCTION"
    else:
        terminal = "NO_TARGETED_FUNCTION_LOSS"

    targeted_activation = _strongest(targeted_result)
    comparator_activation = _strongest(comparator_result)
    return {
        "candidate_id": "CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01",
        "cycle": 1,
        "discovery_mode": "THEORY_BACKWARD_MECHANISM_DISCOVERY",
        "evidentiary_status": "NON_EVIDENTIARY",
        "seed": SEED,
        "train_count": TRAIN_COUNT,
        "probe_episode_id": probe.episode_id,
        "selected_assembly_id": selected_id,
        "selected_assembly_motif_x_count": label_counts[selected_id]["motif_x"],
        "selected_assembly_motif_y_count": label_counts[selected_id]["motif_y"],
        "selected_assembly_delta": selectivity_delta,
        "prototype_unit_count": len(prototype_units),
        "k": k,
        "target_units": target_units,
        "comparator_units": comparator_units,
        "activity_matches": match_rows,
        "baseline": {
            "prediction": baseline_prediction,
            "strongest_assembly_id": baseline_activation.assembly_id,
            "strongest_similarity": baseline_activation.similarity,
            "spike_count": len(baseline_result.v04_result.spikes),
        },
        "targeted": {
            "prediction": targeted_prediction,
            "strongest_assembly_id": (
                targeted_activation.assembly_id if targeted_activation is not None else None
            ),
            "strongest_similarity": (
                targeted_activation.similarity if targeted_activation is not None else 0.0
            ),
            "spike_count": len(targeted_result.v04_result.spikes),
        },
        "activity_matched_nonmember": {
            "prediction": comparator_prediction,
            "strongest_assembly_id": (
                comparator_activation.assembly_id if comparator_activation is not None else None
            ),
            "strongest_similarity": (
                comparator_activation.similarity if comparator_activation is not None else 0.0
            ),
            "spike_count": len(comparator_result.v04_result.spikes),
        },
        "terminal": terminal,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
