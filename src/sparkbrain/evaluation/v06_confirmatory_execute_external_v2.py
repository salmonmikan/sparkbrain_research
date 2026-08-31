from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_external_launch_gate_v2 import (
    claim_external_one_way_execution_v2,
    require_external_launch_gate_v2,
)
from .v06_confirmatory_external_raw_store import (
    ExternalAtomicRawRunWriter,
    RawExecutionMetadata,
)
from .v06_confirmatory_external_verification_v2 import (
    load_external_freeze_bundle_v2,
)
from .v06_confirmatory_normalized_resource_v2 import (
    deterministic_execution_id_v2,
    measure_condition_execution_v2,
)


def _write_control_marker(path: Path, value: object) -> None:
    payload = (
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(path, 0o444)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute one externally sealed candidate-003 raw run.",
    )
    parser.add_argument("--freeze-bundle", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    bundle = load_external_freeze_bundle_v2(args.freeze_bundle)
    bundle.validate_for_execution()
    expected_raw_root = Path(bundle.artifact_layout["raw_root"])
    observed_raw_root = args.raw_root.expanduser().resolve(strict=False)
    if observed_raw_root != expected_raw_root:
        raise RuntimeError("CLI raw root differs from frozen artifact layout")

    # This gate runs before importing the candidate world generator or any real
    # capability adapter. A failed gate therefore cannot consume candidate-003.
    gate = require_external_launch_gate_v2(bundle)
    claim_external_one_way_execution_v2(bundle, gate)

    # Capability imports are intentionally below the irreversible STARTED
    # marker. From this line onward, any failure is a failed one-way run rather
    # than an opportunity to modify and retry the same candidate set.
    from .v06_confirmatory_adapter_registry_v2 import run_registered_adapter_v2
    from .v06_confirmatory_external_freeze import ExternalArtifactLayout
    from .v06_confirmatory_heldout_common import result_record_state
    from .v06_confirmatory_heldout_spec import build_heldout_world_grid

    layout = ExternalArtifactLayout(**bundle.artifact_layout)
    run_id = f"candidate-003-{bundle.bundle_hash()[:20]}"
    writer = ExternalAtomicRawRunWriter(
        layout,
        run_id=run_id,
        envelope_hash=bundle.bundle_hash(),
        source_git_sha=bundle.source_git_sha,
        expected_execution_count=50 * len(ConfirmatoryCondition),
        expected_evidence_record_count=50 * len(ConfirmatoryCondition) * 9,
    )
    control_root = Path(bundle.artifact_layout["control_root"])
    writer.begin()
    completed = 0
    try:
        for world in build_heldout_world_grid():
            for condition in ConfirmatoryCondition:
                execution_id = deterministic_execution_id_v2(
                    envelope_hash=bundle.bundle_hash(),
                    source_git_sha=bundle.source_git_sha,
                    manifest_hash=bundle.manifest_hash,
                    world_generation_id=bundle.world_generation_id,
                    family_id=world.family_id,
                    seed=world.seed,
                    condition=condition,
                    world_specification_hash=world.specification_hash(),
                )
                execution, normalized = measure_condition_execution_v2(
                    lambda world=world, condition=condition: (
                        run_registered_adapter_v2(world, condition)
                    ),
                    execution_id=execution_id,
                )
                metadata = RawExecutionMetadata(
                    execution_id=execution_id,
                    envelope_hash=bundle.bundle_hash(),
                    source_git_sha=bundle.source_git_sha,
                    manifest_hash=bundle.manifest_hash,
                    world_generation_id=bundle.world_generation_id,
                    world_grid_hash=bundle.world_grid_hash,
                    family_id=world.family_id,
                    seed=world.seed,
                    condition=condition.value,
                    world_specification_hash=world.specification_hash(),
                    record_count=len(execution.records),
                    resource_record_count=1,
                )
                writer.write_execution(
                    metadata,
                    result_rows=tuple(
                        result_record_state(row) for row in execution.records
                    ),
                    resource_row={
                        "normalized": normalized.state_dict(),
                        "raw_adapter": execution.resource.state_dict(),
                    },
                )
                completed += 1
        commit = writer.finalize()
    except BaseException as error:
        failed_root = writer.abort(preserve_partial=True)
        _write_control_marker(
            control_root / "RUN_FAILED.json",
            {
                "bundle_hash": bundle.bundle_hash(),
                "completed_execution_count": completed,
                "error_type": type(error).__name__,
                "failed_raw_root": str(failed_root) if failed_root is not None else None,
                "run_id": run_id,
                "state": "FAILED",
            },
        )
        raise

    _write_control_marker(
        control_root / "RAW_COMMITTED.json",
        {
            "bundle_hash": bundle.bundle_hash(),
            "commit_hash": commit.commit_hash(),
            "evidence_record_count": commit.evidence_record_count,
            "execution_count": commit.execution_count,
            "raw_root": str(writer.final_root),
            "resource_record_count": commit.resource_record_count,
            "run_id": run_id,
            "state": "RAW_COMMITTED",
        },
    )
    print(
        json.dumps(
            {
                "commit_hash": commit.commit_hash(),
                "raw_root": str(writer.final_root),
                "state": "RAW_COMMITTED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
