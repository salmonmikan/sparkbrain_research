from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sparkbrain.research.rv01.resource_matched_reservoir import (
    ResourceMatchedReservoirConfig,
    run_development_resource_matched_reservoir_suite,
)
from sparkbrain.v06.foundation import digest

SCHEMA = "rv01-r01-12d-development-result-v1"


def _aggregate(worlds: tuple[Any, ...]) -> dict[str, Any]:
    world_count = len(worlds)
    route_count = sum(len(world.probes) for world in worlds)
    field_weighted_retention = sum(
        world.assessment.field_mean_ordered_retention * len(world.probes)
        for world in worlds
    )
    reservoir_weighted_retention = sum(
        world.assessment.reservoir_mean_ordered_retention * len(world.probes)
        for world in worlds
    )
    return {
        "world_count": world_count,
        "route_count": route_count,
        "resource_match_world_count": sum(
            world.resources.resource_match_passed for world in worlds
        ),
        "deterministic_replay_world_count": sum(
            world.assessment.deterministic_replay_state_hash
            and world.assessment.deterministic_replay_probe_hash
            for world in worlds
        ),
        "reservoir_matches_or_exceeds_world_count": sum(
            world.assessment.reservoir_matches_or_exceeds_mean_retention
            for world in worlds
        ),
        "field_mean_ordered_retention_route_weighted": (
            field_weighted_retention / route_count
        ),
        "reservoir_mean_ordered_retention_route_weighted": (
            reservoir_weighted_retention / route_count
        ),
        "field_minus_reservoir_retention_route_weighted": (
            (field_weighted_retention - reservoir_weighted_retention) / route_count
        ),
        "field_exact_route_count": sum(
            world.assessment.field_exact_route_count for world in worlds
        ),
        "reservoir_exact_route_count": sum(
            world.assessment.reservoir_exact_route_count for world in worlds
        ),
        "field_contamination_count": sum(
            world.assessment.field_contamination_count for world in worlds
        ),
        "reservoir_contamination_count": sum(
            world.assessment.reservoir_contamination_count for world in worlds
        ),
    }


def build_result(*, execution_source_sha: str) -> dict[str, Any]:
    config = ResourceMatchedReservoirConfig()
    suite = run_development_resource_matched_reservoir_suite(config=config)
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "experiment_id": "R01-12D",
        "phase": "development",
        "execution_source_sha": execution_source_sha,
        "held_out_capability_executed": False,
        "comparator_config": asdict(config),
        "world_grid_hash": suite.world_grid_hash,
        "suite_hash": suite.suite_hash,
        "aggregate": _aggregate(suite.worlds),
        "worlds": [world.state_dict() for world in suite.worlds],
    }
    payload["result_payload_hash"] = digest(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute and serialize the preregistered RV01 R01-12D development comparison."
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the canonical JSON result.",
    )
    parser.add_argument(
        "--execution-source-sha",
        default=os.environ.get("GITHUB_SHA", "local-unbound"),
        help="Source SHA bound to this execution.",
    )
    args = parser.parse_args()

    result = build_result(execution_source_sha=args.execution_source_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "aggregate": result["aggregate"],
                "execution_source_sha": result["execution_source_sha"],
                "held_out_capability_executed": result[
                    "held_out_capability_executed"
                ],
                "result_payload_hash": result["result_payload_hash"],
                "suite_hash": result["suite_hash"],
                "world_grid_hash": result["world_grid_hash"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
