from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

from .foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    digest,
    validate_runtime_mapping,
)


@dataclass(frozen=True, slots=True)
class ReinjectionConfig:
    """Safety and uncertainty gates for endogenous Field reinjection."""

    minimum_confidence: float = 0.5
    confidence_power: float = 1.0
    current_gain: float = 1.0
    maximum_effective_current: float = 1.0
    maximum_generation_depth: int = 4
    maximum_energy_per_window: float = 8.0
    maximum_proposals_per_window: int = 32
    maximum_branches_per_origin_state: int = 4
    window_ms: float = 50.0

    def validate(self) -> None:
        for name in (
            "minimum_confidence",
            "confidence_power",
            "current_gain",
            "maximum_effective_current",
            "maximum_energy_per_window",
            "window_ms",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if not 0 <= self.minimum_confidence <= 1:
            raise ValueError("minimum_confidence must be in [0, 1]")
        if self.confidence_power <= 0 or self.current_gain <= 0:
            raise ValueError("confidence_power and current_gain must be positive")
        if self.maximum_effective_current <= 0:
            raise ValueError("maximum_effective_current must be positive")
        if self.maximum_generation_depth < 0:
            raise ValueError("maximum_generation_depth must be non-negative")
        if self.maximum_energy_per_window <= 0 or self.window_ms <= 0:
            raise ValueError("energy and time-window limits must be positive")
        if self.maximum_proposals_per_window < 1:
            raise ValueError("maximum_proposals_per_window must be positive")
        if self.maximum_branches_per_origin_state < 1:
            raise ValueError("maximum_branches_per_origin_state must be positive")


@dataclass(frozen=True, slots=True)
class ReinjectionDecision:
    proposal_id: str
    accepted: bool
    reason: str
    target_unit_id: int | None
    scheduled_time_ms: float | None
    effective_current: float
    energy_cost: float
    field_state_hash_before: str
    field_state_hash_after: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class FieldReinjectionGate:
    """Reinject endogenous proposals as ordinary synaptic arrivals.

    The gate never emits a Spike directly. Accepted proposals enter the same
    queue and are processed by the retained v0.4 membrane, inhibition,
    threshold, refractory, adaptation, and recurrent-propagation rules.
    Reinjection cannot commit positive learning or convert an endogenous event
    into an observation.
    """

    def __init__(
        self,
        ledger: ProvenanceLedger,
        config: ReinjectionConfig | None = None,
    ) -> None:
        self.ledger = ledger
        self.config = config or ReinjectionConfig()
        self.config.validate()
        self._scheduled_proposal_ids: set[str] = set()
        self._window_counts: dict[int, int] = {}
        self._window_energy: dict[int, float] = {}
        self._origin_branches: dict[str, int] = {}
        self.accepted_count = 0
        self.rejected_count = 0

    def schedule(
        self,
        proposal: EndogenousPulseProposal,
        field: TemporalExcitableField,
    ) -> ReinjectionDecision:
        before = field.state_hash()
        rejection = self._rejection_reason(proposal, field)
        if rejection is not None:
            self.rejected_count += 1
            return ReinjectionDecision(
                proposal_id=proposal.proposal_id,
                accepted=False,
                reason=rejection,
                target_unit_id=None,
                scheduled_time_ms=None,
                effective_current=0.0,
                energy_cost=0.0,
                field_state_hash_before=before,
                field_state_hash_after=field.state_hash(),
            )

        target_unit_id = self._target_unit_id(proposal.target)
        if target_unit_id not in field.units:
            raise KeyError(f"unknown reinjection target unit: {target_unit_id}")
        confidence_weight = proposal.confidence**self.config.confidence_power
        signed_current = proposal.polarity * min(
            self.config.maximum_effective_current,
            proposal.magnitude * confidence_weight * self.config.current_gain,
        )
        energy_cost = proposal.energy_cost + abs(signed_current)
        window = self._window_index(proposal.predicted_arrival_ms)
        if self._window_energy.get(window, 0.0) + energy_cost > (
            self.config.maximum_energy_per_window + 1e-12
        ):
            self.rejected_count += 1
            return ReinjectionDecision(
                proposal_id=proposal.proposal_id,
                accepted=False,
                reason="energy_budget",
                target_unit_id=None,
                scheduled_time_ms=None,
                effective_current=0.0,
                energy_cost=energy_cost,
                field_state_hash_before=before,
                field_state_hash_after=field.state_hash(),
            )

        event_id = f"endo:{proposal.proposal_id}"
        field.schedule_arrival(
            SynapticArrival(
                time_ms=proposal.predicted_arrival_ms,
                target_id=target_unit_id,
                current=signed_current,
                source_id=None,
                pulse_id=event_id,
                novelty=0.0,
                prediction_error=0.0,
            )
        )
        self._scheduled_proposal_ids.add(proposal.proposal_id)
        self._window_counts[window] = self._window_counts.get(window, 0) + 1
        self._window_energy[window] = self._window_energy.get(window, 0.0) + energy_cost
        self._origin_branches[proposal.origin_state_hash] = (
            self._origin_branches.get(proposal.origin_state_hash, 0) + 1
        )
        self.accepted_count += 1
        return ReinjectionDecision(
            proposal_id=proposal.proposal_id,
            accepted=True,
            reason="scheduled_normal_rule_arrival",
            target_unit_id=target_unit_id,
            scheduled_time_ms=proposal.predicted_arrival_ms,
            effective_current=signed_current,
            energy_cost=energy_cost,
            field_state_hash_before=before,
            field_state_hash_after=field.state_hash(),
        )

    def _rejection_reason(
        self,
        proposal: EndogenousPulseProposal,
        field: TemporalExcitableField,
    ) -> str | None:
        registered = self.ledger.proposals.get(proposal.proposal_id)
        if registered is None:
            return "unregistered_proposal"
        if registered != proposal:
            return "proposal_content_mismatch"
        event = self.ledger.events.get(f"endo:{proposal.proposal_id}")
        if event is None or event.origin is not EventOrigin.ENDOGENOUS_UNCONFIRMED:
            return "proposal_not_pending"
        if proposal.proposal_id in self._scheduled_proposal_ids:
            return "already_scheduled"
        if proposal.predicted_arrival_ms < field.current_time_ms:
            return "arrival_in_past"
        if proposal.predicted_arrival_ms > proposal.valid_until_ms:
            return "expired_before_arrival"
        if field.current_time_ms > proposal.valid_until_ms:
            return "expired"
        if proposal.confidence < self.config.minimum_confidence:
            return "low_confidence"
        if proposal.generation_depth > self.config.maximum_generation_depth:
            return "generation_depth"
        window = self._window_index(proposal.predicted_arrival_ms)
        if self._window_counts.get(window, 0) >= self.config.maximum_proposals_per_window:
            return "proposal_budget"
        if self._origin_branches.get(proposal.origin_state_hash, 0) >= (
            self.config.maximum_branches_per_origin_state
        ):
            return "branch_budget"
        try:
            self._target_unit_id(proposal.target)
        except ValueError:
            return "invalid_target"
        return None

    @staticmethod
    def _target_unit_id(target: str) -> int:
        prefix = "unit:"
        if not target.startswith(prefix):
            raise ValueError("reinjection target must use unit:<non-negative-int>")
        raw = target[len(prefix) :]
        if not raw or not raw.isdigit():
            raise ValueError("reinjection target must use unit:<non-negative-int>")
        return int(raw)

    def _window_index(self, time_ms: float) -> int:
        return int(math.floor(time_ms / self.config.window_ms))

    def state_dict(self) -> dict[str, Any]:
        value = {
            "accepted_count": self.accepted_count,
            "config": asdict(self.config),
            "origin_branches": dict(sorted(self._origin_branches.items())),
            "rejected_count": self.rejected_count,
            "scheduled_proposal_ids": sorted(self._scheduled_proposal_ids),
            "window_counts": {
                str(key): value for key, value in sorted(self._window_counts.items())
            },
            "window_energy": {
                str(key): value for key, value in sorted(self._window_energy.items())
            },
        }
        validate_runtime_mapping(value, path="v06.reinjection")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())
