from __future__ import annotations

import argparse
import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_artifacts import (
    ARTIFACT_CONTRACT_VERSION,
    AtomicRawRunWriter,
    ExecutionIdentity,
    RawRunReceipt,
    deterministic_execution_id,
)
from .v06_confirmatory_candidate_manifest import build_candidate_manifest
from .v06_confirmatory_environment import environment_lock_from_state
from .v06_confirmatory_execution_seal import (
    ConfirmatoryFreezeRecord,
    freeze_record_from_state,
)
from .v06_confirmatory_launch_gate import (
    LaunchGateReport,
    claim_one_way_execution,
    require_launch_gate,
)
from .v06_confirmatory_resource_accounting import measure_condition_execution

EXPECTED_EXECUTION_COUNT = 50 * len(ConfirmatoryCondition)
EXPECTED_RESULT_RECORD_COUNT = EXPECTED_EXECUTION_COUNT * len(EvidenceDomain)


@dataclass(frozen=True, slots=True)
class CandidateExecutionState:
    run_id: str
    seal_hash: str
    source_code_sha: str
    status: str
    expected_execution_count: int
    candidate_execution_count: int
    expected_result_record_count: int
    committed_result_record_count: int
    current_family_id: str | None
    current_seed: int | None
    current_condition: str | None
    raw_receipt: dict[str, Any] | None
    failure_type: str | None
    failure_message: str | None

    def validate(self) -> None:
        if not self.run_id or len(self.seal_hash) != 64:
            raise ValueError("candidate execution identity is invalid")
        if len(self.source_code_sha) != 40:
            raise ValueError("candidate source SHA is invalid")
        if self.status not in {"RUNNING", "RAW_COMMITTED", "FAILED"}:
            raise ValueError("candidate execution status is invalid")
        if self.expected_execution_count != EXPECTED_EXECUTION_COUNT:
            raise ValueError("candidate execution count contract changed")
        if self.expected_result_record_count != EXPECTED_RESULT_RECORD_COUNT:
            raise ValueError("candidate result count contract changed")
        if not 0 <= self.candidate_execution_count <= self.expected_execution_count:
            raise ValueError("candidate execution counter is invalid")
        if self.committed_result_record_count != (
            self.candidate_execution_count * len(EvidenceDomain)
        ):
            raise ValueError("committed result count does not match executions")
        if self.status == "RAW_COMMITTED":
            if self.candidate_execution_count != self.expected_execution_count:
                raise ValueError("committed raw run is incomplete")
            if self.raw_receipt is None:
                raise ValueError("committed raw run requires a receipt")
        if self.status == "FAILED" and not self.failure_type:
            raise ValueError("failed candidate run requires failure metadata")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text("utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"required control file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"control file is not valid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"control file must contain one JSON object: {path}")
    return value


def _atomic_json_replace(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _atomic_json_exclusive(path: Path, value: object) -> None:
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o444,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(
                value,
                stream,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def _run_id(freeze_record: ConfirmatoryFreezeRecord) -> str:
    return f"confirmatory-{freeze_record.seal_hash()[:32]}"


def _validate_control_layout(
    *,
    output_root: Path,
    freeze_record_path: Path,
    environment_lock_path: Path,
) -> None:
    expected_control = (output_root / "control").resolve()
    if freeze_record_path.resolve() != expected_control / "freeze_record.json":
        raise RuntimeError("freeze record must be output-root/control/freeze_record.json")
    if environment_lock_path.resolve() != expected_control / "environment_lock.json":
        raise RuntimeError(
            "environment lock must be output-root/control/environment_lock.json"
        )
    verification_path = expected_control / "freeze_verification.json"
    if not verification_path.is_file():
        raise RuntimeError("independent freeze verification is missing")


def _validate_independent_verification(
    freeze_record: ConfirmatoryFreezeRecord,
    verification_state: dict[str, Any],
) -> None:
    if verification_state.get("ready_for_approval") is not True:
        raise RuntimeError("freeze verification is not approval-ready")
    candidate_hash = str(verification_state.get("candidate_hash", ""))
    reviewer_id = str(verification_state.get("reviewer_id", ""))
    if len(candidate_hash) != 64 or not reviewer_id:
        raise RuntimeError("freeze verification identity is incomplete")
    approval_parts = freeze_record.approval_id.split(":")
    if approval_parts != ["APPROVED", reviewer_id, candidate_hash[:16]]:
        raise RuntimeError("freeze approval does not match independent verification")


def _initial_state(freeze_record: ConfirmatoryFreezeRecord) -> CandidateExecutionState:
    return CandidateExecutionState(
        run_id=_run_id(freeze_record),
        seal_hash=freeze_record.seal_hash(),
        source_code_sha=freeze_record.source_code_sha,
        status="RUNNING",
        expected_execution_count=EXPECTED_EXECUTION_COUNT,
        candidate_execution_count=0,
        expected_result_record_count=EXPECTED_RESULT_RECORD_COUNT,
        committed_result_record_count=0,
        current_family_id=None,
        current_seed=None,
        current_condition=None,
        raw_receipt=None,
        failure_type=None,
        failure_message=None,
    )


def execute_confirmatory(
    *,
    repository_root: Path,
    freeze_record_path: Path,
    environment_lock_path: Path,
    output_root: Path,
) -> RawRunReceipt:
    """Execute one sealed candidate run and commit raw evidence only."""

    repository_root = repository_root.resolve()
    output_root = output_root.resolve()
    _validate_control_layout(
        output_root=output_root,
        freeze_record_path=freeze_record_path,
        environment_lock_path=environment_lock_path,
    )
    freeze_record = freeze_record_from_state(_read_json(freeze_record_path))
    environment_lock = environment_lock_from_state(_read_json(environment_lock_path))
    verification_path = output_root / "control" / "freeze_verification.json"
    _validate_independent_verification(
        freeze_record,
        _read_json(verification_path),
    )
    manifest = build_candidate_manifest(
        source_code_sha=freeze_record.source_code_sha
    )
    execution_state_path = output_root / "control" / "execution_state.json"
    start_marker_path = output_root / "control" / "STARTED.json"
    launch_report_path = output_root / "control" / "launch_report.json"
    launch_report: LaunchGateReport = require_launch_gate(
        manifest,
        freeze_record,
        environment_lock,
        repository_root=repository_root,
        output_root=output_root,
        execution_counter_path=execution_state_path,
        start_marker_path=start_marker_path,
    )
    claim_one_way_execution(
        start_marker_path,
        freeze_record=freeze_record,
        launch_report=launch_report,
    )
    _atomic_json_exclusive(launch_report_path, launch_report.state_dict())

    state = _initial_state(freeze_record)
    state.validate()
    _atomic_json_replace(execution_state_path, state.state_dict())

    writer = AtomicRawRunWriter(
        output_root,
        run_id=state.run_id,
        expected_execution_count=EXPECTED_EXECUTION_COUNT,
        expected_result_record_count=EXPECTED_RESULT_RECORD_COUNT,
    )
    try:
        from .v06_confirmatory_adapter_registry import run_registered_condition
        from .v06_confirmatory_heldout_spec import build_heldout_world_grid

        worlds = build_heldout_world_grid()
        if len(worlds) != 50:
            raise RuntimeError("candidate world grid must contain exactly 50 worlds")
        for world in worlds:
            for condition in ConfirmatoryCondition:
                state = CandidateExecutionState(
                    **{
                        **state.state_dict(),
                        "current_family_id": world.family_id,
                        "current_seed": world.seed,
                        "current_condition": condition.value,
                    }
                )
                state.validate()
                _atomic_json_replace(execution_state_path, state.state_dict())
                measured = measure_condition_execution(
                    lambda world=world, condition=condition: run_registered_condition(
                        world,
                        condition,
                    )
                )
                identity = ExecutionIdentity(
                    artifact_contract_version=ARTIFACT_CONTRACT_VERSION,
                    world_generation_id=freeze_record.world_generation_id,
                    family_id=world.family_id,
                    seed=world.seed,
                    condition=condition,
                    source_code_sha=freeze_record.source_code_sha,
                    manifest_hash=freeze_record.manifest_hash,
                    execution_id=deterministic_execution_id(
                        world_generation_id=freeze_record.world_generation_id,
                        family_id=world.family_id,
                        seed=world.seed,
                        condition=condition,
                        source_code_sha=freeze_record.source_code_sha,
                        manifest_hash=freeze_record.manifest_hash,
                    ),
                )
                writer.add(identity, measured)
                state = CandidateExecutionState(
                    **{
                        **state.state_dict(),
                        "candidate_execution_count": (
                            state.candidate_execution_count + 1
                        ),
                        "committed_result_record_count": (
                            state.committed_result_record_count
                            + len(EvidenceDomain)
                        ),
                    }
                )
                state.validate()
                _atomic_json_replace(execution_state_path, state.state_dict())
        receipt = writer.finalize()
        state = CandidateExecutionState(
            **{
                **state.state_dict(),
                "status": "RAW_COMMITTED",
                "current_family_id": None,
                "current_seed": None,
                "current_condition": None,
                "raw_receipt": receipt.state_dict(),
            }
        )
        state.validate()
        _atomic_json_replace(execution_state_path, state.state_dict())
        return receipt
    except BaseException as exc:
        failed_state = CandidateExecutionState(
            **{
                **state.state_dict(),
                "status": "FAILED",
                "raw_receipt": None,
                "failure_type": type(exc).__name__,
                "failure_message": str(exc),
            }
        )
        failed_state.validate()
        _atomic_json_replace(execution_state_path, failed_state.state_dict())
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute one sealed SparkBrain v0.6 confirmatory raw run."
    )
    parser.add_argument("--freeze-record", type=Path, required=True)
    parser.add_argument("--environment-lock", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    receipt = execute_confirmatory(
        repository_root=arguments.repository_root,
        freeze_record_path=arguments.freeze_record,
        environment_lock_path=arguments.environment_lock,
        output_root=arguments.output_root,
    )
    print(json.dumps(receipt.state_dict(), sort_keys=True))


if __name__ == "__main__":
    main()
