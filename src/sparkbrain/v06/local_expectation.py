from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from .foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)


@dataclass(frozen=True, slots=True)
class LocalExpectationConfig:
    max_lag_ms: float = 80.0
    minimum_observations: int = 2
    minimum_confidence: float = 0.15
    maximum_candidates: int = 4
    proposal_ttl_ms: float = 25.0
    variance_scale_ms2: float = 16.0
    energy_scale: float = 0.05

    def validate(self) -> None:
        if self.max_lag_ms <= 0:
            raise ValueError("max_lag_ms must be positive")
        if self.minimum_observations < 1:
            raise ValueError("minimum_observations must be positive")
        if not 0 <= self.minimum_confidence <= 1:
            raise ValueError("minimum_confidence must be in [0, 1]")
        if self.maximum_candidates < 1:
            raise ValueError("maximum_candidates must be positive")
        if self.proposal_ttl_ms <= 0:
            raise ValueError("proposal_ttl_ms must be positive")
        if self.variance_scale_ms2 <= 0:
            raise ValueError("variance_scale_ms2 must be positive")
        if self.energy_scale < 0:
            raise ValueError("energy_scale must be non-negative")


@dataclass(slots=True)
class LocalTransitionStats:
    count: int = 0
    mean_lag_ms: float = 0.0
    lag_m2: float = 0.0
    mean_magnitude: float = 0.0
    positive_count: int = 0
    negative_count: int = 0

    def update(self, *, lag_ms: float, magnitude: float, polarity: int) -> None:
        if lag_ms <= 0 or not math.isfinite(lag_ms):
            raise ValueError("lag_ms must be finite and positive")
        if magnitude < 0 or not math.isfinite(magnitude):
            raise ValueError("magnitude must be finite and non-negative")
        if polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")
        self.count += 1
        lag_delta = lag_ms - self.mean_lag_ms
        self.mean_lag_ms += lag_delta / self.count
        self.lag_m2 += lag_delta * (lag_ms - self.mean_lag_ms)
        magnitude_delta = magnitude - self.mean_magnitude
        self.mean_magnitude += magnitude_delta / self.count
        if polarity > 0:
            self.positive_count += 1
        else:
            self.negative_count += 1

    @property
    def lag_variance(self) -> float:
        return self.lag_m2 / max(1, self.count - 1)

    @property
    def majority_polarity(self) -> int:
        return 1 if self.positive_count >= self.negative_count else -1

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> LocalTransitionStats:
        row = cls(
            count=int(value["count"]),
            mean_lag_ms=float(value["mean_lag_ms"]),
            lag_m2=float(value["lag_m2"]),
            mean_magnitude=float(value["mean_magnitude"]),
            positive_count=int(value["positive_count"]),
            negative_count=int(value["negative_count"]),
        )
        if row.count < 0 or row.positive_count < 0 or row.negative_count < 0:
            raise ValueError("transition counts must be non-negative")
        if row.positive_count + row.negative_count != row.count:
            raise ValueError("polarity counts must equal transition count")
        return row


class LocalTemporalExpectation:
    """G1 local lag memory with no Assembly or global sequence state.

    Learning accepts only observed external-to-external transitions. Proposal
    generation is read-only, so endogenous activity alone cannot increase a
    transition count or confidence.
    """

    def __init__(self, config: LocalExpectationConfig | None = None) -> None:
        self.config = config or LocalExpectationConfig()
        self.config.validate()
        self._transitions: dict[str, dict[str, LocalTransitionStats]] = {}
        self.external_transition_count = 0
        self.proposal_count = 0

    def observe_external_transition(
        self,
        source: RuntimePulse,
        target: RuntimePulse,
    ) -> None:
        if source.origin is not EventOrigin.EXTERNAL:
            raise ValueError("transition source must be an external observation")
        if target.origin is not EventOrigin.EXTERNAL:
            raise ValueError("transition target must be an external observation")
        lag_ms = target.time_ms - source.time_ms
        if lag_ms <= 0:
            raise ValueError("target must occur after source")
        if lag_ms > self.config.max_lag_ms:
            return
        table = self._transitions.setdefault(source.target, {})
        stats = table.setdefault(target.target, LocalTransitionStats())
        stats.update(
            lag_ms=lag_ms,
            magnitude=target.magnitude,
            polarity=target.polarity,
        )
        self.external_transition_count += 1

    def proposals_for(
        self,
        source: RuntimePulse,
        *,
        origin_state_hash: str,
    ) -> tuple[EndogenousPulseProposal, ...]:
        table = self._transitions.get(source.target, {})
        eligible = [
            (target, stats)
            for target, stats in table.items()
            if stats.count >= self.config.minimum_observations
        ]
        if not eligible:
            return ()
        total = sum(stats.count for _, stats in eligible)
        candidates: list[tuple[float, str, LocalTransitionStats]] = []
        for target, stats in eligible:
            frequency = stats.count / total
            stability = 1.0 / (
                1.0 + stats.lag_variance / self.config.variance_scale_ms2
            )
            confidence = frequency * stability
            if confidence >= self.config.minimum_confidence:
                candidates.append((confidence, target, stats))
        candidates.sort(key=lambda row: (-row[0], row[1]))
        parent = ()
        if source.origin.is_endogenous and source.event_id.startswith("endo:"):
            parent = (source.event_id.removeprefix("endo:"),)
        proposals: list[EndogenousPulseProposal] = []
        for confidence, target, stats in candidates[: self.config.maximum_candidates]:
            arrival = source.time_ms + stats.mean_lag_ms
            identity = {
                "arrival": round(arrival, 9),
                "count": stats.count,
                "source_event": source.event_id,
                "source_target": source.target,
                "target": target,
            }
            proposals.append(
                EndogenousPulseProposal(
                    proposal_id=f"g1-{digest(identity)[:24]}",
                    created_at_ms=source.time_ms,
                    target=target,
                    predicted_arrival_ms=arrival,
                    magnitude=stats.mean_magnitude,
                    polarity=stats.majority_polarity,
                    confidence=confidence,
                    origin_state_hash=origin_state_hash,
                    parent_proposal_ids=parent,
                    local_path_ids=(f"local:{source.target}->{target}",),
                    generation_depth=source.generation_depth + 1,
                    valid_until_ms=arrival + self.config.proposal_ttl_ms,
                    energy_cost=self.config.energy_scale * stats.mean_magnitude,
                )
            )
        self.proposal_count += len(proposals)
        return tuple(proposals)

    def state_dict(self) -> dict[str, Any]:
        value = {
            "config": asdict(self.config),
            "external_transition_count": self.external_transition_count,
            "proposal_count": self.proposal_count,
            "transitions": {
                source: {
                    target: stats.state_dict()
                    for target, stats in sorted(table.items())
                }
                for source, table in sorted(self._transitions.items())
            },
        }
        validate_runtime_mapping(value, path="g1.local_expectation")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> LocalTemporalExpectation:
        validate_runtime_mapping(value, path="g1.local_expectation")
        model = cls(LocalExpectationConfig(**value["config"]))
        model.external_transition_count = int(value["external_transition_count"])
        model.proposal_count = int(value["proposal_count"])
        model._transitions = {
            str(source): {
                str(target): LocalTransitionStats.from_state_dict(stats)
                for target, stats in table.items()
            }
            for source, table in value["transitions"].items()
        }
        return model
