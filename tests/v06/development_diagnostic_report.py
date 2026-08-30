from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from test_capability_staging_development_fixture import DevelopmentCapabilityWorld
from test_capability_staging_development_variants import development_variants

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_heldout_comparators import (
    _FACADE_FACTORIES,
    _context,
    _train_paths,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_controls import (
    _rotate_relation_state,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_primary import (
    _dominant_target,
    _relation_cycles,
    _run_reentry,
)


def _chain_diagnostic(world: Any, condition: ConfirmatoryCondition) -> dict[str, Any]:
    factory = _FACADE_FACTORIES[condition]
    paths = (*world.competition_paths, world.control_path)
    main_context = _context("sequence", world.main_path)
    control_context = _context("sequence", world.control_path)

    sham = factory.create()
    _train_paths(sham, world, paths)
    sham_main = sham.rollout(main_context, world.main_path[0])
    sham_control = sham.rollout(control_context, world.control_path[0])

    targeted = factory.create()
    _train_paths(targeted, world, paths)
    targeted_main = targeted.rollout(
        main_context,
        world.main_path[0],
        suppressed_sources=(world.main_path[1],),
    )

    matched = factory.create()
    _train_paths(matched, world, paths)
    matched_control = matched.rollout(
        control_context,
        world.control_path[0],
        suppressed_sources=(world.control_path[1],),
    )
    matched_main = matched.rollout(main_context, world.main_path[0])
    return {
        "expected_control": list(world.control_path[1:]),
        "expected_main": list(world.main_path[1:]),
        "matched_control": list(matched_control),
        "matched_main": list(matched_main),
        "sham_control": list(sham_control),
        "sham_main": list(sham_main),
        "targeted_expected": [world.main_path[1]],
        "targeted_main": list(targeted_main),
        "training_path_order": [list(path) for path in dict.fromkeys(paths)],
        "training_path_exposures": [
            world.branch_exposure_counts[
                world.competition_paths.index(path)
            ]
            if path in world.competition_paths
            else max(3, len(world.training_lag_profiles_ms))
            for path in dict.fromkeys(paths)
        ],
    }


def _link_rows(snapshot: dict[str, Any], port_id: str) -> list[dict[str, Any]]:
    rows = [
        {
            "consistent_count": int(row["consistent_count"]),
            "inconsistent_count": int(row["inconsistent_count"]),
            "reliability": float(row["reliability"]),
            "target": str(row["target"]),
        }
        for row in snapshot["links"].values()
        if row["port_id"] == port_id
    ]
    return sorted(rows, key=lambda row: (-row["reliability"], row["target"]))


def _relation_diagnostic(world: Any) -> dict[str, Any]:
    relation = _relation_cycles(world)
    shuffled_states = tuple(
        _rotate_relation_state(world, snapshot) for snapshot in relation.snapshots
    )
    shuffled_responses = tuple(
        _run_reentry(
            world,
            snapshot,
            event_id=f"development-diagnostic:shuffled:{index}",
        )
        for index, snapshot in enumerate(shuffled_states)
    )
    original_reentry = tuple(
        _run_reentry(
            world,
            snapshot,
            event_id=f"development-diagnostic:original:{index}",
        )
        for index, snapshot in enumerate(relation.snapshots)
    )
    return {
        "expected_targets": list(world.contingency_cycle_targets),
        "phase_dominant_targets": list(relation.phase_dominant_targets),
        "phase_links": [
            _link_rows(snapshot, world.main_port)
            for snapshot in relation.snapshots
        ],
        "phase_lengths": list(world.contingency_phase_lengths),
        "primary_reentry_responses": [list(row) for row in original_reentry],
        "shuffled_correct_fraction": (
            sum(
                response == (target,)
                for response, target in zip(
                    shuffled_responses,
                    world.contingency_cycle_targets,
                    strict=True,
                )
            )
            / len(shuffled_responses)
        ),
        "shuffled_reentry_responses": [list(row) for row in shuffled_responses],
    }


def build_report() -> dict[str, Any]:
    worlds = (DevelopmentCapabilityWorld(), *development_variants())
    return {
        "candidate_002_capability_executions": 0,
        "interpretation": "Development-only diagnostic; no held-out candidate imported.",
        "worlds": [
            {
                "chain": {
                    condition.value: _chain_diagnostic(world, condition)
                    for condition in (
                        ConfirmatoryCondition.G3_RECURRENT,
                        ConfirmatoryCondition.G4_ASSEMBLY,
                        ConfirmatoryCondition.G5_TYPED,
                    )
                },
                "family_id": world.family_id,
                "relation": _relation_diagnostic(world),
                "seed": world.seed,
                "world_specification_hash": world.specification_hash(),
            }
            for world in worlds
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(build_report(), indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
