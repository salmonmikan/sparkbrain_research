from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace
from typing import Any

from .foundation import (
    EndogenousChainRecord,
    EndogenousPulseProposal,
    EventOrigin,
    LearningEligibility,
    ProvenanceLedger,
    RealityMatchRecord,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)
from .local_expectation import LocalTemporalExpectation


@dataclass(frozen=True, slots=True)
class SparseTransitionConfig:
    """G2 confirmation-gated adaptation for sparse local transition paths."""

    learning_rate: float = 0.2
    prior_success: float = 1.0
    prior_failure: float = 1.0
    minimum_confidence_scale: float = 0.25
    maximum_confidence_scale: float = 1.5
    maximum_timing_error_ms: float = 8.0
    maximum_magnitude_error: float = 0.75
    maximum_pending: int = 128

    def validate(self) -> None:
        for name in (
            "learning_rate",
            "prior_success",
            "prior_failure",
            "minimum_confidence_scale",
            "maximum_confidence_scale",
            "maximum_timing_error_ms",
            "maximum_magnitude_error",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if not 0 < self.learning_rate <= 1:
            raise ValueError("learning_rate must be in (0, 1]")
        if self.prior_success <= 0 or self.prior_failure <= 0:
            raise ValueError("reliability priors must be positive")
        if self.minimum_confidence_scale <= 0:
            raise ValueError("minimum_confidence_scale must be positive")
        if self.maximum_confidence_scale < self.minimum_confidence_scale:
            raise ValueError("maximum_confidence_scale must be at least the minimum")
        if self.maximum_timing_error_ms < 0 or self.maximum_magnitude_error < 0:
            raise ValueError("match tolerances must be non-negative")
        if self.maximum_pending < 1:
            raise ValueError("maximum_pending must be positive")


@dataclass(slots=True)
class LocalPathAdaptation:
    confirmed_count: int = 0
    contradicted_count: int = 0
    mean_timing_correction_ms: float = 0.0
    mean_magnitude_correction: float = 0.0

    def reliability(self, config: SparseTransitionConfig) -> float:
        return (config.prior_success + self.confirmed_count) / (
            config.prior_success
            + config.prior_failure
            + self.confirmed_count
            + self.contradicted_count
        )

    def confidence_scale(self, config: SparseTransitionConfig) -> float:
        prior = config.prior_success / (config.prior_success + config.prior_failure)
        scale = self.reliability(config) / prior
        return min(
            config.maximum_confidence_scale,
            max(config.minimum_confidence_scale, scale),
        )

    def observe_match(
        self,
        *,
        timing_correction_ms: float,
        magnitude_correction: float,
        learning_rate: float,
    ) -> None:
        self.confirmed_count += 1
        self.mean_timing_correction_ms += learning_rate * (
            timing_correction_ms - self.mean_timing_correction_ms
        )
        self.mean_magnitude_correction += learning_rate * (
            magnitude_correction - self.mean_magnitude_correction
        )

    def observe_contradiction(self) -> None:
        self.contradicted_count += 1

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> LocalPathAdaptation:
        row = cls(
            confirmed_count=int(value["confirmed_count"]),
            contradicted_count=int(value["contradicted_count"]),
            mean_timing_correction_ms=float(value["mean_timing_correction_ms"]),
            mean_magnitude_correction=float(value["mean_magnitude_correction"]),
        )
        if row.confirmed_count < 0 or row.contradicted_count < 0:
            raise ValueError("adaptation counts must be non-negative")
        if not math.isfinite(row.mean_timing_correction_ms):
            raise ValueError("timing correction must be finite")
        if not math.isfinite(row.mean_magnitude_correction):
            raise ValueError("magnitude correction must be finite")
        return row


@dataclass(frozen=True, slots=True)
class PendingLocalTransition:
    proposal_id: str
    chain_id: str
    eligibility_id: str
    path_id: str
    created_at_ms: float
    valid_until_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PreparedLocalTransition:
    proposal: EndogenousPulseProposal
    pulse: RuntimePulse
    chain_id: str
    eligibility_id: str
    path_id: str


@dataclass(frozen=True, slots=True)
class LocalTransitionResolution:
    proposal_id: str
    path_id: str
    matched: bool
    timing_error_ms: float
    magnitude_error: float
    polarity_match: bool
    confidence_before: float
    confidence_after: float


class SparseLocalTransitionAdaptation:
    """G2 sparse adaptation with external-confirmation-only positive commits.

    G1 supplies local timing proposals. G2 creates a provenance chain and an
    uncommitted eligibility record for each proposal. Merely producing or
    reinjecting an endogenous event cannot change a path adaptation. A matched
    external event commits the eligibility and updates only that local path.
    """

    def __init__(
        self,
        expectation: LocalTemporalExpectation,
        ledger: ProvenanceLedger,
        config: SparseTransitionConfig | None = None,
    ) -> None:
        self.expectation = expectation
        self.ledger = ledger
        self.config = config or SparseTransitionConfig()
        self.config.validate()
        self._paths: dict[str, LocalPathAdaptation] = {}
        self._pending: dict[str, PendingLocalTransition] = {}
        self.prepared_count = 0
        self.confirmed_count = 0
        self.contradicted_count = 0

    def prepare(
        self,
        source: RuntimePulse,
        *,
        origin_state_hash: str,
    ) -> tuple[PreparedLocalTransition, ...]:
        proposal_count_before = self.expectation.proposal_count
        base_rows = self.expectation.proposals_for(
            source,
            origin_state_hash=origin_state_hash,
        )
        if len(self._pending) + len(base_rows) > self.config.maximum_pending:
            self.expectation.proposal_count = proposal_count_before
            raise RuntimeError("G2 pending transition budget exceeded")

        prepared: list[PreparedLocalTransition] = []
        for base in base_rows:
            if len(base.local_path_ids) != 1:
                raise ValueError("G2 requires exactly one local path per proposal")
            path_id = base.local_path_ids[0]
            path_state = self._paths.get(path_id)
            confidence_scale = (
                path_state.confidence_scale(self.config) if path_state is not None else 1.0
            )
            timing_correction = (
                path_state.mean_timing_correction_ms if path_state is not None else 0.0
            )
            magnitude_correction = (
                path_state.mean_magnitude_correction if path_state is not None else 0.0
            )
            arrival = max(base.created_at_ms, base.predicted_arrival_ms + timing_correction)
            magnitude = max(0.0, base.magnitude + magnitude_correction)
            confidence = min(1.0, max(0.0, base.confidence * confidence_scale))
            identity = {
                "base_proposal_id": base.proposal_id,
                "origin_state_hash": origin_state_hash,
                "path_id": path_id,
                "source_event_id": source.event_id,
            }
            proposal_id = f"g2-{digest(identity)[:24]}"
            proposal = replace(
                base,
                proposal_id=proposal_id,
                predicted_arrival_ms=arrival,
                magnitude=magnitude,
                confidence=confidence,
                valid_until_ms=max(base.valid_until_ms, arrival),
            )
            pulse = self.ledger.register_proposal(proposal)
            chain_id = f"g2-chain-{digest({'proposal_id': proposal_id})[:24]}"
            eligibility_id = f"g2-elig-{digest({'chain_id': chain_id})[:24]}"
            self.ledger.register_chain(
                EndogenousChainRecord(
                    chain_id=chain_id,
                    root_state_hash=origin_state_hash,
                    proposal_ids=(proposal_id,),
                    generated_event_ids=(pulse.event_id,),
                    predicted_external_targets=(proposal.target,),
                    eligibility=max(0.0, 1.0 - proposal.confidence),
                )
            )
            self.ledger.register_eligibility(
                LearningEligibility(
                    eligibility_id=eligibility_id,
                    chain_id=chain_id,
                    path_ids=(path_id,),
                    candidate_delta=self.config.learning_rate,
                    created_at_ms=proposal.created_at_ms,
                    valid_until_ms=proposal.valid_until_ms,
                )
            )
            pending = PendingLocalTransition(
                proposal_id=proposal_id,
                chain_id=chain_id,
                eligibility_id=eligibility_id,
                path_id=path_id,
                created_at_ms=proposal.created_at_ms,
                valid_until_ms=proposal.valid_until_ms,
            )
            self._pending[proposal_id] = pending
            prepared.append(
                PreparedLocalTransition(
                    proposal=proposal,
                    pulse=pulse,
                    chain_id=chain_id,
                    eligibility_id=eligibility_id,
                    path_id=path_id,
                )
            )
        self.prepared_count += len(prepared)
        return tuple(prepared)

    def resolve_external(
        self,
        proposal_id: str,
        external: RuntimePulse,
    ) -> LocalTransitionResolution:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G2 resolution requires an external observation")
        pending = self._pending[proposal_id]
        if external.time_ms > pending.valid_until_ms:
            self.expire_pending(external.time_ms)
            raise ValueError("G2 external observation arrived after eligibility expiry")
        proposal = self.ledger.proposals[proposal_id]
        self._ensure_external_registered(external)

        signed_timing_error = external.time_ms - proposal.predicted_arrival_ms
        signed_magnitude_error = external.magnitude - proposal.magnitude
        timing_error = abs(signed_timing_error)
        magnitude_error = abs(signed_magnitude_error)
        polarity_match = external.polarity == proposal.polarity
        target_match = external.target == proposal.target
        matched = (
            target_match
            and polarity_match
            and timing_error <= self.config.maximum_timing_error_ms
            and magnitude_error <= self.config.maximum_magnitude_error
        )
        before = self.path_confidence_scale(pending.path_id)

        if matched:
            self.ledger.record_match(
                RealityMatchRecord(
                    proposal_id=proposal_id,
                    external_event_id=external.event_id,
                    status="matched",
                    target_error=0.0,
                    timing_error_ms=timing_error,
                    magnitude_error=magnitude_error,
                    polarity_match=True,
                    confirmed_at_ms=external.time_ms,
                )
            )
            self.ledger.commit_eligibility(
                pending.eligibility_id,
                external_event_id=external.event_id,
                now_ms=external.time_ms,
            )
            path_state = self._paths.setdefault(pending.path_id, LocalPathAdaptation())
            path_state.observe_match(
                timing_correction_ms=signed_timing_error,
                magnitude_correction=signed_magnitude_error,
                learning_rate=self.config.learning_rate,
            )
            self.confirmed_count += 1
        else:
            self.ledger.record_match(
                RealityMatchRecord(
                    proposal_id=proposal_id,
                    external_event_id=external.event_id,
                    status="contradicted",
                    target_error=0.0 if target_match else 1.0,
                    timing_error_ms=timing_error,
                    magnitude_error=magnitude_error,
                    polarity_match=polarity_match,
                )
            )
            path_state = self._paths.setdefault(pending.path_id, LocalPathAdaptation())
            path_state.observe_contradiction()
            self.contradicted_count += 1

        del self._pending[proposal_id]
        after = self.path_confidence_scale(pending.path_id)
        return LocalTransitionResolution(
            proposal_id=proposal_id,
            path_id=pending.path_id,
            matched=matched,
            timing_error_ms=timing_error,
            magnitude_error=magnitude_error,
            polarity_match=polarity_match,
            confidence_before=before,
            confidence_after=after,
        )

    def path_confidence_scale(self, path_id: str) -> float:
        state = self._paths.get(path_id)
        return state.confidence_scale(self.config) if state is not None else 1.0

    def pending(self, proposal_id: str) -> PendingLocalTransition:
        return self._pending[proposal_id]

    def expire_pending(self, now_ms: float) -> tuple[str, ...]:
        expired = tuple(
            proposal_id
            for proposal_id, pending in sorted(self._pending.items())
            if now_ms > pending.valid_until_ms
        )
        self.ledger.expire(now_ms)
        for proposal_id in expired:
            self._pending.pop(proposal_id, None)
        return expired

    def state_dict(self) -> dict[str, Any]:
        value = {
            "config": asdict(self.config),
            "confirmed_count": self.confirmed_count,
            "contradicted_count": self.contradicted_count,
            "expectation": self.expectation.state_dict(),
            "paths": {
                path_id: state.state_dict()
                for path_id, state in sorted(self._paths.items())
            },
            "pending": {
                proposal_id: pending.state_dict()
                for proposal_id, pending in sorted(self._pending.items())
            },
            "prepared_count": self.prepared_count,
        }
        validate_runtime_mapping(value, path="g2.local_transition")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())

    @classmethod
    def from_state_dict(
        cls,
        value: dict[str, Any],
        *,
        ledger: ProvenanceLedger,
    ) -> SparseLocalTransitionAdaptation:
        validate_runtime_mapping(value, path="g2.local_transition")
        model = cls(
            LocalTemporalExpectation.from_state_dict(value["expectation"]),
            ledger,
            SparseTransitionConfig(**value["config"]),
        )
        model._paths = {
            str(path_id): LocalPathAdaptation.from_state_dict(state)
            for path_id, state in value["paths"].items()
        }
        pending_rows = {
            str(proposal_id): PendingLocalTransition(**pending)
            for proposal_id, pending in value["pending"].items()
        }
        for proposal_id, pending in pending_rows.items():
            if proposal_id not in ledger.proposals:
                raise ValueError(
                    "restoring pending G2 state requires a matching provenance ledger"
                )
            if pending.chain_id not in ledger.chains:
                raise ValueError(
                    "restoring pending G2 state requires a matching provenance ledger"
                )
            if pending.eligibility_id not in ledger.eligibilities:
                raise ValueError(
                    "restoring pending G2 state requires a matching provenance ledger"
                )
        model._pending = pending_rows
        model.prepared_count = int(value["prepared_count"])
        model.confirmed_count = int(value["confirmed_count"])
        model.contradicted_count = int(value["contradicted_count"])
        return model

    def _ensure_external_registered(self, external: RuntimePulse) -> None:
        existing = self.ledger.events.get(external.event_id)
        if existing is None:
            self.ledger.register_external(external)
            return
        if existing != external or existing.origin is not EventOrigin.EXTERNAL:
            raise ValueError("external event ID is already registered with different content")
