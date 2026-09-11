"""Transparent user-authorized waiver of the MD-002 independent-human review gate.

This module validates one exact governance record. It does not impersonate an
independent reviewer, does not grant execution authority, does not alter the
MD002ExecutionGate pins, and cannot open capability by itself.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .md002_protocol import MD002_ID

USER_REVIEW_OVERRIDE_SHA256 = "a08752e1642799d58f56e6d1c466258ba758bbb42a3f992df4b1e4ca1d050c96"
USER_REVIEW_OVERRIDE_SOURCE_GIT_SHA = "98280ad3b34f934ad77a33d881e6d94e61af67ca"
USER_REVIEW_OVERRIDE_PROTOCOL_SHA256 = (
    "242a62999e4eb76259440312230b8760e24ee37168284e6c8d03b099ed344be8"
)
USER_REVIEW_OVERRIDE_AUTHORITY = "explicit-user-authorization-2026-09-11"
USER_REVIEW_OVERRIDE_KIND = "user-authorized-review-gate-override"


def _require_false(record: dict[str, Any], name: str) -> None:
    if record.get(name) is not False:
        raise PermissionError(f"MD-002 review override requires {name}=false")


def validate_user_review_override(raw: bytes) -> str:
    """Validate the exact review-only waiver and return its SHA-256 digest."""

    digest = hashlib.sha256(raw).hexdigest()
    if digest != USER_REVIEW_OVERRIDE_SHA256:
        raise PermissionError("MD-002 user review override hash mismatch")
    try:
        record = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise PermissionError("MD-002 user review override is not valid JSON") from exc
    if record.get("md002_id") != MD002_ID:
        raise PermissionError("MD-002 user review override targets a different diagnostic")
    if record.get("kind") != USER_REVIEW_OVERRIDE_KIND:
        raise PermissionError("MD-002 user review override has the wrong kind")
    if record.get("approved") is not True:
        raise PermissionError("MD-002 user review override is not approved")
    if record.get("scope") != "human-review-only":
        raise PermissionError("MD-002 user review override exceeds human-review-only scope")
    if record.get("authority") != USER_REVIEW_OVERRIDE_AUTHORITY:
        raise PermissionError("MD-002 user review override authority drifted")
    source_git_sha = record.get("source_git_sha")
    if source_git_sha != USER_REVIEW_OVERRIDE_SOURCE_GIT_SHA:
        raise PermissionError("MD-002 user review override source binding drifted")
    if record.get("protocol_binding") != "sha256(md002_id+'@'+source_git_sha)":
        raise PermissionError("MD-002 user review override protocol-binding rule drifted")
    expected_protocol_sha256 = hashlib.sha256(
        f"{MD002_ID}@{source_git_sha}".encode()
    ).hexdigest()
    if expected_protocol_sha256 != USER_REVIEW_OVERRIDE_PROTOCOL_SHA256:
        raise AssertionError("MD-002 review override protocol constant drifted")
    if record.get("protocol_sha256") != expected_protocol_sha256:
        raise PermissionError("MD-002 user review override protocol binding drifted")
    _require_false(record, "independent_human_review_performed")
    _require_false(record, "formal_execution_authority")
    return digest


__all__ = [
    "USER_REVIEW_OVERRIDE_SHA256",
    "validate_user_review_override",
]
