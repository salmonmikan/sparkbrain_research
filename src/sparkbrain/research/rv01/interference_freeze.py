from __future__ import annotations

import hashlib
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

from .direct_field_plasticity import DirectFieldPlasticityConfig
from .interference_contract import (
    DEVELOPMENT_SEEDS,
    HELD_OUT_SEEDS,
    development_worlds,
    held_out_worlds,
    world_grid_hash,
)
from .resource_matched_reservoir import ResourceMatchedReservoirConfig

R01_12D_EXECUTION_SOURCE_SHA = "b163117512daca23b613c8a109a544833af7d360"
R01_12D_DEVELOPMENT_GRID_HASH = (
    "1d9aed2d3be9cd04460943023321fe519160afb1e3f2ef5622d74949b49e5c48"
)
R01_12D_SUITE_HASH = (
    "16e29a77ffa714adbe8bb93cda1bc0cbf67a4022da135069fe731ca65709e7c6"
)
R01_12D_RESULT_PAYLOAD_HASH = (
    "4f07d2f645fc9319647b49775a6186eba95af4cf567f99b6b5f8f64fbe0ff79e"
)

CRITICAL_FREEZE_PATHS = (
    "src/sparkbrain/research/rv01/direct_field_plasticity.py",
    "src/sparkbrain/research/rv01/interference_contract.py",
    "src/sparkbrain/research/rv01/interference_controls.py",
    "src/sparkbrain/research/rv01/interference_freeze.py",
    "src/sparkbrain/research/rv01/interference_runner.py",
    "src/sparkbrain/research/rv01/physical_learner_bridge.py",
    "src/sparkbrain/research/rv01/physical_safety.py",
    "src/sparkbrain/research/rv01/resource_matched_reservoir.py",
    "docs/research/RV01_CONTINUAL_INTERFERENCE_PROTOCOL.md",
    "docs/research/RV01_R01_11_SAFETY_DIAGNOSTIC_ADDENDUM.md",
    "docs/research/RV01_R01_12D_COMPARATOR_CONTRACT.md",
    "docs/research/RV01_R01_12D_DEVELOPMENT_RESULT.md",
    "docs/research/RV01_R01_12E_HELDOUT_FREEZE_REVIEW.md",
    "artifacts/research/rv01/r01_12d/development_result_manifest.json",
)


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _file_sha256(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.is_file():
        raise RuntimeError(f"freeze-critical path is missing: {relative_path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _expected_counts() -> dict[str, int]:
    specs = held_out_worlds()
    route_count = sum(world.route_count for world in specs)
    probe_matrix_count = sum(world.route_count * world.route_count for world in specs)
    return {
        "world_count": len(specs),
        "training_phase_count": route_count,
        "field_probe_matrix_record_count": probe_matrix_count,
        "reservoir_final_probe_record_count": route_count,
    }


def build_r01_12e_preflight(
    *,
    source_git_sha: str,
    repository_root: Path | None = None,
) -> dict[str, Any]:
    """Build a capability-free held-out freeze candidate.

    This function may instantiate deterministic held-out world specifications and
    hash them. It does not train a Field, execute a route probe, fit a reservoir,
    or inspect any held-out capability outcome.
    """

    if len(source_git_sha) != 40:
        raise ValueError("source_git_sha must be a full 40-character Git SHA")
    development = development_worlds()
    observed_development_hash = world_grid_hash(development)
    if observed_development_hash != R01_12D_DEVELOPMENT_GRID_HASH:
        raise RuntimeError(
            "development world grid drifted after the fixed R01-12D result"
        )

    held_out = held_out_worlds()
    if len(development) != 15 or len(held_out) != 50:
        raise RuntimeError("interference world counts drifted from the protocol")
    if set(DEVELOPMENT_SEEDS).intersection(HELD_OUT_SEEDS):
        raise RuntimeError("development and held-out seed sets overlap")
    for world in held_out:
        world.validate()

    root = repository_root or _repository_root()
    source_hashes = {
        path: _file_sha256(root, path) for path in CRITICAL_FREEZE_PATHS
    }
    expected = _expected_counts()
    if expected != {
        "world_count": 50,
        "training_phase_count": 200,
        "field_probe_matrix_record_count": 1000,
        "reservoir_final_probe_record_count": 200,
    }:
        raise RuntimeError("held-out evidence cardinality drifted from the protocol")

    payload: dict[str, Any] = {
        "schema": "rv01-r01-12e-heldout-freeze-preflight-v1",
        "candidate_id": "rv01-r01-12-interference-heldout-v1",
        "status": "review-ready-not-sealed",
        "source_git_sha": source_git_sha,
        "held_out_capability_executed": False,
        "execution_policy": "one-way-no-rerun-after-seal",
        "development_result": {
            "execution_source_sha": R01_12D_EXECUTION_SOURCE_SHA,
            "world_grid_hash": R01_12D_DEVELOPMENT_GRID_HASH,
            "suite_hash": R01_12D_SUITE_HASH,
            "result_payload_hash": R01_12D_RESULT_PAYLOAD_HASH,
        },
        "development_seeds": list(DEVELOPMENT_SEEDS),
        "held_out_seeds": list(HELD_OUT_SEEDS),
        "held_out_world_grid_hash": world_grid_hash(held_out),
        "held_out_worlds": [
            {
                "world_id": world.world_id,
                "specification_hash": world.specification_hash(),
                "family": world.family.value,
                "seed": world.seed,
                "route_count": world.route_count,
                "maximum_active_outgoing_edges": (
                    world.maximum_active_outgoing_edges
                ),
                "maximum_total_active_edges": world.maximum_total_active_edges,
            }
            for world in held_out
        ],
        "expected_held_out_records": expected,
        "plasticity_config": asdict(DirectFieldPlasticityConfig()),
        "reservoir_config": asdict(ResourceMatchedReservoirConfig()),
        "evaluator_contract": {
            "initial_connection_weight": 0.05,
            "maximum_probe_spikes": 512,
            "field_probe_scope": "every route after every training phase",
            "reservoir_probe_scope": "final route probes only",
            "exact_route_rule": "ordered_retention==1 and contamination==0",
        },
        "critical_source_sha256": source_hashes,
        "blocked_before_seal": [
            "run_interference_world(held-out)",
            "run_resource_matched_reservoir_world(held-out)",
        ],
    }
    payload["preflight_payload_hash"] = digest(payload)
    return payload
