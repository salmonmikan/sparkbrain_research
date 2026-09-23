from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v05.candidate35_architecture import ARMS, build_candidate35_anchor
from sparkbrain.v05.candidate35_preservation import (
    ANALYST_COMMIT,
    ANALYST_GENERATION,
    DEVELOPMENT_PHASE,
    QUEUE_STATE,
    RESPONSE_AUTHORITY_DECISION,
    RESPONSE_AUTHORITY_EXHAUSTION,
    SOURCE_BLOB_SHA1,
    SOURCE_HEAD,
    candidate35_preservation_nonresult_preflight,
    execute_candidate35_response_preserve_before_read,
)

EXPECTED_ANALYST_GENERATION = "EVA-20260923T225720+0900-R100-C6A2F18D"
EXPECTED_ANALYST_COMMIT = "a32494246245a559ad4e1f8543a1f252b03ef2e7"
EXPECTED_SOURCE_HEAD = "8ea6581544c642ad74f1a95955ab2c5f795afccc"
EXPECTED_SOURCE_BLOB_SHA1 = "4055f42483d5bba73eef51b1753a2c19f18d5ab5"
EXPECTED_DEVELOPMENT_PHASE = "OPEN_DEVELOPMENT"
EXPECTED_QUEUE_STATE = "QUEUED_FOR_MAIN_ARCHITECTURE_ONE_BOUNDED_RESPONSE"
EXPECTED_ARMS = (
    "SHAM_STATE",
    "POTENTIAL_NULL",
    "ADAPTATION_NULL",
    "JOINT_SUBTHRESHOLD_NULL",
    "DELAYED_SHAM_32MS",
)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _git_head(repo_root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _write_exclusive_json(path: Path, payload: dict[str, object]) -> tuple[str, int]:
    raw = (canonical_json(payload) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)
    return _sha256_bytes(raw), len(raw)


def _require_exact_authority() -> None:
    checks = {
        "analyst_generation": (ANALYST_GENERATION, EXPECTED_ANALYST_GENERATION),
        "analyst_commit": (ANALYST_COMMIT, EXPECTED_ANALYST_COMMIT),
        "source_head": (SOURCE_HEAD, EXPECTED_SOURCE_HEAD),
        "source_blob_sha1": (SOURCE_BLOB_SHA1, EXPECTED_SOURCE_BLOB_SHA1),
        "development_phase": (DEVELOPMENT_PHASE, EXPECTED_DEVELOPMENT_PHASE),
        "queue_state": (QUEUE_STATE, EXPECTED_QUEUE_STATE),
        "arms": (tuple(ARMS), EXPECTED_ARMS),
    }
    drift = {name: values for name, values in checks.items() if values[0] != values[1]}
    if drift:
        raise RuntimeError(f"candidate #35 R100 binding drift: {drift}")


def run(*, output_dir: Path, expected_implementation_head: str) -> dict[str, object]:
    repo_root = Path(__file__).resolve().parents[1]
    _require_exact_authority()

    actual_head = _git_head(repo_root)
    if actual_head != expected_implementation_head:
        raise RuntimeError(
            "candidate #35 implementation head drifted: "
            f"expected {expected_implementation_head}, got {actual_head}"
        )

    preflight = candidate35_preservation_nonresult_preflight()
    package_bindings = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "pyproject_sha256": _sha256_file(repo_root / "pyproject.toml"),
        "requirements_release_sha256": _sha256_file(repo_root / "requirements-release.lock"),
        "candidate_source_blob_sha1": SOURCE_BLOB_SHA1,
        "preservation_wrapper_sha256": _sha256_file(
            repo_root / "src/sparkbrain/v05/candidate35_preservation.py"
        ),
        "response_runner_sha256": _sha256_file(Path(__file__).resolve()),
    }
    preflight_payload: dict[str, object] = {
        "schema": "cand35-r100-response-preflight-v1",
        "analyst_generation": ANALYST_GENERATION,
        "analyst_commit": ANALYST_COMMIT,
        "response_authority_decision": RESPONSE_AUTHORITY_DECISION,
        "response_authority_exhaustion": RESPONSE_AUTHORITY_EXHAUSTION,
        "development_phase": DEVELOPMENT_PHASE,
        "queue_state": QUEUE_STATE,
        "implementation_head": actual_head,
        "scientific_source_head": SOURCE_HEAD,
        "scientific_source_blob_sha1": SOURCE_BLOB_SHA1,
        "fixed_arm_order": list(ARMS),
        "contract_sha256": preflight.contract_sha256,
        "component_binding_sha256": preflight.binding_sha256,
        "provenance_sha256": preflight.provenance_sha256,
        "response_producer": preflight.response_producer,
        "raw_serializer": "sparkbrain.v04.contracts.canonical_json",
        "preservation_target": str(output_dir.resolve()),
        "preserve_mode": "EXCLUSIVE_CREATE_BEFORE_RETURN",
        "package_runtime_binding": package_bindings,
        "candidate_response_executed": False,
        "scientific_result": None,
        "official_scoring_performed": False,
        "preformal_execution_performed": False,
        "formal_action_performed": False,
    }
    preflight_sha256, preflight_size = _write_exclusive_json(
        output_dir / "00-preflight.json", preflight_payload
    )

    anchor_brain, anchor_time_ms = build_candidate35_anchor()
    preserved: list[dict[str, object]] = []
    for index, arm in enumerate(ARMS, start=1):
        raw_path = output_dir / f"{index:02d}-{arm}.json"
        record = execute_candidate35_response_preserve_before_read(
            anchor_brain,
            anchor_time_ms=anchor_time_ms,
            arm=arm,
            output_path=raw_path,
            response_execution_allowed=True,
        )
        preserved.append(
            {
                "arm": arm,
                "raw_path": record.raw_path,
                "raw_sha256": record.raw_sha256,
                "raw_size_bytes": record.raw_size_bytes,
                "provenance_sha256": record.provenance_sha256,
            }
        )

    completion_payload: dict[str, object] = {
        "schema": "cand35-r100-response-batch-complete-v1",
        "analyst_generation": ANALYST_GENERATION,
        "analyst_commit": ANALYST_COMMIT,
        "implementation_head": actual_head,
        "scientific_source_head": SOURCE_HEAD,
        "scientific_source_blob_sha1": SOURCE_BLOB_SHA1,
        "development_phase_at_execution": DEVELOPMENT_PHASE,
        "fixed_arm_order": list(ARMS),
        "preflight_sha256": preflight_sha256,
        "preflight_size_bytes": preflight_size,
        "raw_artifacts": preserved,
        "complete_batch": True,
        "evidentiary_status": "DEVELOPMENT_ONLY_UNSCORED_ARCHITECTURE_RESPONSE",
        "confirmatory_credit": 0,
        "official_scoring_performed": False,
        "preformal_execution_performed": False,
        "formal_action_performed": False,
        "response_authority_exhausted": True,
    }
    completion_sha256, completion_size = _write_exclusive_json(
        output_dir / "99-batch-complete.json", completion_payload
    )
    return {
        "complete_batch": True,
        "output_dir": str(output_dir.resolve()),
        "arm_count": len(preserved),
        "completion_sha256": completion_sha256,
        "completion_size_bytes": completion_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-implementation-head", required=True)
    args = parser.parse_args()
    result = run(
        output_dir=args.output_dir,
        expected_implementation_head=args.expected_implementation_head,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
