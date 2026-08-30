from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from test_capability_staging_development_fixture import (
    DevelopmentCapabilityWorld,
    _run as run_baseline,
)
from test_capability_staging_development_variants import (
    DevelopmentVariantWorld,
    _run as run_variant,
    development_variants,
)


def _run_world(
    world: DevelopmentCapabilityWorld | DevelopmentVariantWorld,
) -> dict[str, Any]:
    runner = run_baseline if isinstance(world, DevelopmentCapabilityWorld) else run_variant
    first = {
        condition: runner(world, condition)  # type: ignore[arg-type]
        for condition in ConfirmatoryCondition
    }
    second = {
        condition: runner(world, condition)  # type: ignore[arg-type]
        for condition in ConfirmatoryCondition
    }
    condition_rows: dict[str, Any] = {}
    for condition in ConfirmatoryCondition:
        execution = first[condition]
        replay = second[condition]
        execution.validate()
        replay.validate()
        metrics = dict(execution.records[0].metrics)
        resource = execution.resource
        passed_domains = [
            row.evidence_domain.value for row in execution.records if row.passed
        ]
        condition_rows[condition.value] = {
            "control_contract_passed": metrics.get("control_contract_passed"),
            "generated_internal_events": resource.generated_internal_events,
            "intervention_count": resource.intervention_count,
            "normal_field_threshold_crossings": (
                resource.normal_field_threshold_crossings
            ),
            "normal_field_threshold_present": (
                resource.normal_field_threshold_present
            ),
            "observed_training_events": resource.observed_training_events,
            "parameter_count": resource.parameter_count,
            "passed_domain_count": len(passed_domains),
            "passed_domains": passed_domains,
            "persistent_state_entries": resource.persistent_state_entries,
            "privileged_information": [
                row.value for row in resource.privileged_information
            ],
            "scalar_reward_observations": (
                resource.scalar_reward_observations
            ),
            "semantic_replay_match": (
                execution.semantic_hash == replay.semantic_hash
                and execution.records == replay.records
            ),
            "taxonomy_hash_match": metrics.get("taxonomy_hash_match"),
            "threshold_bypassed": resource.threshold_bypassed,
            "typed_head_count": resource.typed_head_count,
            "explicit_assembly_entries": resource.explicit_assembly_entries,
        }
    return {
        "branch_count": world.branch_count,
        "conditions": condition_rows,
        "contingency_change_count": world.contingency_change_count,
        "family_id": world.family_id,
        "seed": world.seed,
        "structural_token": world.structural_token,
        "threshold": world.threshold,
        "world_specification_hash": world.specification_hash(),
    }


def build_report() -> dict[str, Any]:
    worlds: tuple[DevelopmentCapabilityWorld | DevelopmentVariantWorld, ...] = (
        DevelopmentCapabilityWorld(),
        *development_variants(),
    )
    world_rows = tuple(_run_world(world) for world in worlds)
    aggregate: dict[str, Any] = {}
    for condition in ConfirmatoryCondition:
        rows = tuple(
            world["conditions"][condition.value] for world in world_rows
        )
        aggregate[condition.value] = {
            "all_semantic_replays_match": all(
                row["semantic_replay_match"] for row in rows
            ),
            "control_contract_fraction": (
                sum(row["control_contract_passed"] or 0.0 for row in rows)
                / len(rows)
                if any(row["control_contract_passed"] is not None for row in rows)
                else None
            ),
            "domain_positive_fraction": (
                sum(row["passed_domain_count"] for row in rows)
                / (len(rows) * len(EvidenceDomain))
            ),
            "execution_count": len(rows),
            "maximum_parameter_count": max(row["parameter_count"] for row in rows),
            "maximum_persistent_state_entries": max(
                row["persistent_state_entries"] for row in rows
            ),
            "total_generated_internal_events": sum(
                row["generated_internal_events"] for row in rows
            ),
            "total_observed_training_events": sum(
                row["observed_training_events"] for row in rows
            ),
        }
    return {
        "candidate_002_capability_executions": 0,
        "condition_count": len(ConfirmatoryCondition),
        "development_execution_count": len(world_rows) * len(ConfirmatoryCondition),
        "development_record_count": (
            len(world_rows) * len(ConfirmatoryCondition) * len(EvidenceDomain)
        ),
        "development_world_count": len(world_rows),
        "interpretation": (
            "Development-only execution and resource evidence. Not held-out or "
            "confirmatory evidence."
        ),
        "per_condition": aggregate,
        "worlds": list(world_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report()
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
