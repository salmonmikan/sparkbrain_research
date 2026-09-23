from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v04.contracts import canonical_json

from . import candidate35_architecture
from .brain import IntegratedV05Brain
from .candidate35_architecture import (
    CANDIDATE_ID,
    DEVELOPMENT_REVISION,
    Candidate35Arm,
    Candidate35ResponseNotAuthorized,
    Candidate35ResponseRecord,
    candidate35_frozen_contract,
    candidate35_nonresult_preflight,
)

ANALYST_GENERATION = "EVA-20260923T210010+0900-R99-6F2B8C14"
ANALYST_COMMIT = "59dbcdc2e3541e78a64f64e16fa0be5ef38efc26"
DEVELOPMENT_PHASE = "OPEN_DEVELOPMENT"
CLAIM_CEILING = "SYSTEM"
PREFORMAL_ELIGIBLE = False
PREFORMAL_READINESS = "NOT_APPLICABLE"
TERMINAL_STATE = "NONTERMINAL"
QUEUE_STATE = "QUEUED_FOR_MAIN_ARCHITECTURE_R3_OR_R4_NONRESULT_PRESERVATION_BOUNDARY"
SYSTEM_PRIORITY_EXCEPTION = "NO_EXECUTABLE_MECHANISM_WHILE_H7_FORMAL_INTEGRITY_CAPABILITY_BLOCKED"
SOURCE_BRANCH = "research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3"
SOURCE_HEAD = "8ea6581544c642ad74f1a95955ab2c5f795afccc"
SOURCE_BLOB_SHA1 = "4055f42483d5bba73eef51b1753a2c19f18d5ab5"
RESPONSE_PRODUCER = "sparkbrain.v05.candidate35_architecture.execute_candidate35_response"
RAW_SERIALIZER = "sparkbrain.v04.contracts.canonical_json"
RAW_SCHEMA = "cand35-architecture-raw-response-v1"
PRESERVE_MODE = "EXCLUSIVE_CREATE_BEFORE_RETURN"


@dataclass(frozen=True, slots=True)
class Candidate35PreservationPreflight:
    provenance_json: str
    provenance_sha256: str
    contract_sha256: str
    binding_sha256: str
    source_blob_sha1: str
    response_producer: str
    candidate_response_executed: bool = False
    raw_artifact_created: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Candidate35PreservedResponse:
    response: Candidate35ResponseRecord
    raw_path: str
    raw_sha256: str
    raw_size_bytes: int
    provenance_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324


def _response_producer_name() -> str:
    producer = candidate35_architecture.execute_candidate35_response
    return f"{producer.__module__}.{producer.__name__}"


def candidate35_preservation_contract() -> dict[str, Any]:
    return {
        "candidate_id": CANDIDATE_ID,
        "claim_ceiling": CLAIM_CEILING,
        "development_phase": DEVELOPMENT_PHASE,
        "development_revision": DEVELOPMENT_REVISION,
        "preformal_eligible": PREFORMAL_ELIGIBLE,
        "preformal_readiness": PREFORMAL_READINESS,
        "terminal_state": TERMINAL_STATE,
        "queue_state": QUEUE_STATE,
        "system_priority_exception": SYSTEM_PRIORITY_EXCEPTION,
        "analyst_generation": ANALYST_GENERATION,
        "analyst_commit": ANALYST_COMMIT,
        "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE_HEAD,
        "source_blob_sha1": SOURCE_BLOB_SHA1,
        "response_producer": RESPONSE_PRODUCER,
        "raw_serializer": RAW_SERIALIZER,
        "raw_schema": RAW_SCHEMA,
        "preserve_mode": PRESERVE_MODE,
        "raw_before_read": True,
        "no_clobber": True,
        "candidate_response_execution_allowed": False,
        "preformal_execution_allowed": False,
        "formal_action_allowed": False,
    }


def candidate35_preservation_nonresult_preflight() -> Candidate35PreservationPreflight:
    base = candidate35_nonresult_preflight()
    frozen = candidate35_frozen_contract()
    if frozen["candidate_response_execution_allowed"] is not False:
        raise AssertionError("candidate #35 response authority drifted")
    if frozen["preformal_execution_allowed"] is not False:
        raise AssertionError("candidate #35 PRE_FORMAL authority drifted")
    if frozen["formal_action_allowed"] is not False:
        raise AssertionError("candidate #35 FORMAL authority drifted")

    source_path = Path(candidate35_architecture.__file__).resolve()
    source_blob_sha1 = _git_blob_sha1(source_path)
    if source_blob_sha1 != SOURCE_BLOB_SHA1:
        raise AssertionError("candidate #35 response source bytes drifted")

    response_producer = _response_producer_name()
    if response_producer != RESPONSE_PRODUCER:
        raise AssertionError("candidate #35 response producer binding drifted")

    provenance = candidate35_preservation_contract()
    provenance["contract_sha256"] = base.contract_sha256
    provenance["binding_sha256"] = base.binding_sha256
    provenance_json = canonical_json(provenance)
    return Candidate35PreservationPreflight(
        provenance_json=provenance_json,
        provenance_sha256=_sha256_text(provenance_json),
        contract_sha256=base.contract_sha256,
        binding_sha256=base.binding_sha256,
        source_blob_sha1=source_blob_sha1,
        response_producer=response_producer,
    )


def execute_candidate35_response_preserve_before_read(
    anchor_brain: IntegratedV05Brain,
    *,
    anchor_time_ms: float,
    arm: Candidate35Arm,
    output_path: Path,
    response_execution_allowed: bool = False,
) -> Candidate35PreservedResponse:
    """Execute only after future authority, preserving canonical raw bytes before return."""
    if response_execution_allowed is not True:
        raise Candidate35ResponseNotAuthorized(
            "candidate #35 response remains STOP pending fresh Analyst review"
        )

    preflight = candidate35_preservation_nonresult_preflight()
    response = candidate35_architecture.execute_candidate35_response(
        anchor_brain,
        anchor_time_ms=anchor_time_ms,
        arm=arm,
        response_execution_allowed=True,
    )
    raw_payload = {
        "schema": RAW_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "development_phase": DEVELOPMENT_PHASE,
        "development_revision": DEVELOPMENT_REVISION,
        "provenance_sha256": preflight.provenance_sha256,
        "source_head": SOURCE_HEAD,
        "source_blob_sha1": SOURCE_BLOB_SHA1,
        "response": response.as_dict(),
        "evidentiary_status": "DEVELOPMENT_ONLY_UNSCORED_RAW_RESPONSE",
        "official_scoring_performed": False,
        "formal_action_performed": False,
    }
    raw_bytes = (canonical_json(raw_payload) + "\n").encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("xb") as handle:
        handle.write(raw_bytes)

    return Candidate35PreservedResponse(
        response=response,
        raw_path=str(output_path),
        raw_sha256=hashlib.sha256(raw_bytes).hexdigest(),
        raw_size_bytes=len(raw_bytes),
        provenance_sha256=preflight.provenance_sha256,
    )
