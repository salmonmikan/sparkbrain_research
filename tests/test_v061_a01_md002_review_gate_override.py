from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.v061_a01.md002_review_gate_override import (
    USER_REVIEW_OVERRIDE_SHA256,
    validate_user_review_override,
)

_OVERRIDE = Path("docs/research/v061_a01/md002_user_review_gate_override_20260911.json")


def test_md002_user_review_override_is_exact_review_only_governance_record() -> None:
    raw = _OVERRIDE.read_bytes()
    assert validate_user_review_override(raw) == USER_REVIEW_OVERRIDE_SHA256


def test_md002_user_review_override_fails_closed_on_tamper() -> None:
    raw = _OVERRIDE.read_bytes()
    tampered = raw.replace(b'"formal_execution_authority":false', b'"formal_execution_authority":true')
    with pytest.raises(PermissionError, match="hash mismatch"):
        validate_user_review_override(tampered)
