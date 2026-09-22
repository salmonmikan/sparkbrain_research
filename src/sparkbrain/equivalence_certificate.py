"""Candidate-independent, non-evidentiary equivalence-certificate verification.

This module validates tooling contracts only. It does not create scientific authority,
interpret outcomes, or establish candidate/Funnel status.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

_CERTIFICATE_TYPE = "equivalence-certificate-v0.1"
_BINDING_KEYS = {"source", "protocol", "package", "input", "evaluator"}
_TOP_LEVEL_KEYS = {
    "schema_version",
    "certificate_type",
    "bindings",
    "privilege_envelope",
    "resource_envelope",
    "members",
}
_IDENTITY_KEYS = {"id", "sha256"}
_MEMBER_KEYS = {
    "producer_id",
    "process_id",
    "challenge_nonce",
    "os_pid",
    "bindings_sha256",
    "privilege_envelope_sha256",
    "resource_envelope_sha256",
    "ordered_trajectory_sha256",
    "checkpoint_sequence_sha256",
}
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_NONCE_RE = re.compile(r"[0-9a-f]{32}")


class Verdict(StrEnum):
    """The only verdict classes emitted by the verifier."""

    VALID_EQUIVALENT = "VALID_EQUIVALENT"
    VALID_NOT_EQUIVALENT = "VALID_NOT_EQUIVALENT"
    INVALID_CONTRACT = "INVALID_CONTRACT"


@dataclass(frozen=True)
class VerificationResult:
    verdict: Verdict
    reason: str


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("value is not canonical-JSON serializable") from exc


def canonical_sha256(value: Any) -> str:
    """Return the SHA-256 of canonical JSON for a pure-data contract fragment."""

    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _invalid(reason: str) -> VerificationResult:
    return VerificationResult(Verdict.INVALID_CONTRACT, reason)


def verify_equivalence_certificate(certificate: Mapping[str, Any]) -> VerificationResult:
    """Fail closed while validating a two-producer equivalence certificate.

    A valid certificate binds both producers to the same source/protocol/package/input/
    evaluator identities and the same privilege/resource envelopes. Producer attestations
    must be independent by producer ID, process ID, challenge nonce, and observed PID.
    Equivalence is then a byte-digest statement about the ordered trajectory and checkpoint
    sequence only; no scientific interpretation is performed.
    """

    if not isinstance(certificate, Mapping):
        return _invalid("CERTIFICATE_NOT_MAPPING")
    if set(certificate) != _TOP_LEVEL_KEYS:
        return _invalid("TOP_LEVEL_SCHEMA_MISMATCH")
    if certificate.get("schema_version") != 1:
        return _invalid("SCHEMA_VERSION_MISMATCH")
    if certificate.get("certificate_type") != _CERTIFICATE_TYPE:
        return _invalid("CERTIFICATE_TYPE_MISMATCH")

    bindings = certificate.get("bindings")
    if not isinstance(bindings, Mapping) or set(bindings) != _BINDING_KEYS:
        return _invalid("BINDINGS_SCHEMA_MISMATCH")
    for key in sorted(_BINDING_KEYS):
        identity = bindings[key]
        if not isinstance(identity, Mapping) or set(identity) != _IDENTITY_KEYS:
            return _invalid(f"IDENTITY_SCHEMA_MISMATCH:{key}")
        if not isinstance(identity["id"], str) or not identity["id"]:
            return _invalid(f"IDENTITY_ID_INVALID:{key}")
        if not _is_sha256(identity["sha256"]):
            return _invalid(f"IDENTITY_SHA256_INVALID:{key}")

    privilege = certificate.get("privilege_envelope")
    resources = certificate.get("resource_envelope")
    if not isinstance(privilege, Mapping):
        return _invalid("PRIVILEGE_ENVELOPE_NOT_MAPPING")
    if not isinstance(resources, Mapping):
        return _invalid("RESOURCE_ENVELOPE_NOT_MAPPING")

    try:
        bindings_sha = canonical_sha256(bindings)
        privilege_sha = canonical_sha256(privilege)
        resources_sha = canonical_sha256(resources)
    except ValueError:
        return _invalid("NON_CANONICAL_CONTRACT_VALUE")

    members = certificate.get("members")
    if not isinstance(members, list) or len(members) != 2:
        return _invalid("EXACTLY_TWO_MEMBERS_REQUIRED")

    verified: list[Mapping[str, Any]] = []
    for index, member in enumerate(members):
        if not isinstance(member, Mapping) or set(member) != _MEMBER_KEYS:
            return _invalid(f"MEMBER_SCHEMA_MISMATCH:{index}")
        if not isinstance(member["producer_id"], str) or not member["producer_id"]:
            return _invalid(f"PRODUCER_ID_INVALID:{index}")
        if not isinstance(member["process_id"], str) or not member["process_id"]:
            return _invalid(f"PROCESS_ID_INVALID:{index}")
        if not isinstance(member["challenge_nonce"], str) or _NONCE_RE.fullmatch(
            member["challenge_nonce"]
        ) is None:
            return _invalid(f"CHALLENGE_NONCE_INVALID:{index}")
        if (
            not isinstance(member["os_pid"], int)
            or isinstance(member["os_pid"], bool)
            or member["os_pid"] <= 0
        ):
            return _invalid(f"OS_PID_INVALID:{index}")
        for field in (
            "bindings_sha256",
            "privilege_envelope_sha256",
            "resource_envelope_sha256",
            "ordered_trajectory_sha256",
            "checkpoint_sequence_sha256",
        ):
            if not _is_sha256(member[field]):
                return _invalid(f"MEMBER_SHA256_INVALID:{index}:{field}")
        if member["bindings_sha256"] != bindings_sha:
            return _invalid(f"BINDINGS_ATTESTATION_MISMATCH:{index}")
        if member["privilege_envelope_sha256"] != privilege_sha:
            return _invalid(f"PRIVILEGE_ATTESTATION_MISMATCH:{index}")
        if member["resource_envelope_sha256"] != resources_sha:
            return _invalid(f"RESOURCE_ATTESTATION_MISMATCH:{index}")
        verified.append(member)

    independence_fields = ("producer_id", "process_id", "challenge_nonce", "os_pid")
    for field in independence_fields:
        if len({member[field] for member in verified}) != 2:
            return _invalid(f"PRODUCERS_NOT_INDEPENDENT:{field}")

    left, right = verified
    if (
        left["ordered_trajectory_sha256"] == right["ordered_trajectory_sha256"]
        and left["checkpoint_sequence_sha256"] == right["checkpoint_sequence_sha256"]
    ):
        return VerificationResult(Verdict.VALID_EQUIVALENT, "EXACT_SEMANTIC_DIGEST_MATCH")
    return VerificationResult(
        Verdict.VALID_NOT_EQUIVALENT,
        "ORDERED_TRAJECTORY_OR_CHECKPOINT_SEQUENCE_MISMATCH",
    )
