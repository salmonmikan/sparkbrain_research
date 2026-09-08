from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SuppressionIntervention:
    token: str

    def validate(self) -> None:
        if not self.token:
            raise ValueError("suppression intervention requires a token")
