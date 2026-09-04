from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class FormalScoringPolicy:
    """Non-compensatory formal decision rule frozen before candidate execution."""

    policy_version: str = "cx01-formal-scoring-policy-1"
    minimum_family_pass_fraction: float = 0.80
    require_all_families: bool = True
    require_training_transcript_match: bool = True
    require_privilege_match: bool = True

    def validate(self) -> None:
        if self.policy_version != "cx01-formal-scoring-policy-1":
            raise ValueError("unexpected CX01 formal scoring policy version")
        if not 0.0 < self.minimum_family_pass_fraction <= 1.0:
            raise ValueError("minimum family pass fraction must be in (0, 1]")
        if not self.require_all_families:
            raise ValueError("CX01 formal scoring must remain non-compensatory across families")
        if not self.require_training_transcript_match:
            raise ValueError("CX01 formal scoring requires training transcript equality")
        if not self.require_privilege_match:
            raise ValueError("CX01 formal scoring requires exact privilege disclosure")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    def policy_hash(self) -> str:
        return _digest(self.state_dict())
