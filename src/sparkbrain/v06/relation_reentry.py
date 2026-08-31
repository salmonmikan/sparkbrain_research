from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField

from .boundary import BoundaryEvent
from .consistency import UntypedBoundaryConsistency
from .foundation import (
    EndogenousPulseProposal,
    ProvenanceLedger,
    digest,
    validate_runtime_mapping,
)
from .reinjection import FieldReinjectionGate, ReinjectionDecision


@dataclass(frozen=True, slots=True)
class RelationReentryConfig:
    """Category-free projection from existing consistency state to the Field."""

    delay_ms: float = 1.0
    magnitude_gain: float = 0.9
    maximum_magnitude: float = 2.0
    minimum_consistent_count: int = 1
    minimum_reliability: float = 0.0
    proposal_ttl_ms: float = 10.0
    maximum_links_per_boundary: int = 16

    def validate(self) -> None:
        for name in (
            "delay_ms",
            "magnitude_gain",
            "maximum_magnitude",
            "minimum_reliability",
            "proposal_ttl_ms",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.delay_ms < 0:
            raise ValueError("delay_ms must be non-negative")
        if self.magnitude_gain <= 0 or self.maximum_magnitude <= 0:
            raise ValueError("magnitude limits must be positive")
        if not 0 <= self.minimum_reliability <= 1:
            raise ValueError("minimum_reliability must be in [0, 1]")
        if self.minimum_consistent_count < 1:
            raise ValueError("minimum_consistent_count must be positive")
        if self.proposal_ttl_ms <= 0:
            raise ValueError("proposal_ttl_ms must be positive")
        if self.maximum_links_per_boundary < 1:
            raise ValueError("maximum_links_per_boundary must be positive")


@dataclass(frozen=True, slots=True)
class RelationReentryRecord:
    boundary_event_id: str
    link_id: str
    port_id: str
    target: str
    reliability: float
    consistent_count: int
    inconsistent_count: int
    magnitude_ratio: float
    proposal_id: str
    predicted_arrival_ms: float
    proposal_magnitude: float
    reinjection: ReinjectionDecision

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["reinjection"] = self.reinjection.state_dict()
        validate_runtime_mapping(value, path="v06.relation_reentry.record")
        return value


class AnonymousRelationReentry:
    """Project existing anonymous relation reliability into normal Field rules.

    This component learns no new relation state. It reads the already externally
    gated `UntypedBoundaryConsistency` state, creates an endogenous proposal for
    every eligible link on the emitted port, and delegates current scheduling to
    the existing `FieldReinjectionGate`.

    It does not select a correct target or winner. All eligible links use the
    same structural rule; ordinary confidence scaling and Field thresholds
    determine which later Sparks occur.
    """

    def __init__(
        self,
        consistency: UntypedBoundaryConsistency,
        ledger: ProvenanceLedger,
        reinjection: FieldReinjectionGate,
        config: RelationReentryConfig | None = None,
    ) -> None:
        if consistency.ledger is not ledger:
            raise ValueError("re-entry and consistency must share one ledger")
        if reinjection.ledger is not ledger:
            raise ValueError("re-entry and reinjection must share one ledger")
        self.consistency = consistency
        self.ledger = ledger
        self.reinjection = reinjection
        self.config = config or RelationReentryConfig()
        self.config.validate()
        self.records: list[RelationReentryRecord] = []
        self._processed_boundary_event_ids: set[str] = set()

    def schedule(
        self,
        boundary: BoundaryEvent,
        field: TemporalExcitableField,
    ) -> tuple[RelationReentryRecord, ...]:
        if boundary.event_id in self._processed_boundary_event_ids:
            raise ValueError("boundary event was already processed for relation re-entry")
        if boundary.time_ms < field.current_time_ms:
            raise ValueError("relation re-entry cannot schedule into the Field past")

        links = self._eligible_links(boundary.port_id)
        if len(links) > self.config.maximum_links_per_boundary:
            raise RuntimeError("relation re-entry link budget exceeded")
        for _, link in links:
            target_unit_id = self._target_unit_id(str(link["target"]))
            if target_unit_id not in field.units:
                raise KeyError(f"unknown relation re-entry target unit: {target_unit_id}")

        self._processed_boundary_event_ids.add(boundary.event_id)
        created: list[RelationReentryRecord] = []
        consistency_hash = self.consistency.state_hash()
        origin_state_hash = digest(
            {
                "boundary_source_state_hash": boundary.source_state_hash,
                "consistency_state_hash": consistency_hash,
                "field_state_hash": field.state_hash(),
            }
        )
        arrival_ms = boundary.time_ms + self.config.delay_ms

        for link_id, link in links:
            ratio = max(0.0, float(link["mean_magnitude_ratio"]))
            magnitude = min(
                self.config.maximum_magnitude,
                boundary.magnitude * self.config.magnitude_gain * ratio,
            )
            identity = {
                "boundary_event_id": boundary.event_id,
                "consistency_state_hash": consistency_hash,
                "link_id": link_id,
                "target": link["target"],
            }
            proposal_id = f"reentry-{digest(identity)[:24]}"
            proposal = EndogenousPulseProposal(
                proposal_id=proposal_id,
                created_at_ms=boundary.time_ms,
                target=str(link["target"]),
                predicted_arrival_ms=arrival_ms,
                magnitude=magnitude,
                polarity=int(link["polarity"]),
                confidence=float(link["reliability"]),
                origin_state_hash=origin_state_hash,
                parent_proposal_ids=boundary.source_proposal_ids,
                local_path_ids=(f"anonymous-link:{link_id}",),
                generation_depth=boundary.generation_depth + 1,
                valid_until_ms=arrival_ms + self.config.proposal_ttl_ms,
                energy_cost=0.0,
            )
            self.ledger.register_proposal(proposal)
            decision = self.reinjection.schedule(proposal, field)
            record = RelationReentryRecord(
                boundary_event_id=boundary.event_id,
                link_id=link_id,
                port_id=boundary.port_id,
                target=proposal.target,
                reliability=proposal.confidence,
                consistent_count=int(link["consistent_count"]),
                inconsistent_count=int(link["inconsistent_count"]),
                magnitude_ratio=ratio,
                proposal_id=proposal_id,
                predicted_arrival_ms=arrival_ms,
                proposal_magnitude=magnitude,
                reinjection=decision,
            )
            self.records.append(record)
            created.append(record)
        return tuple(created)

    def _eligible_links(self, port_id: str) -> tuple[tuple[str, dict[str, Any]], ...]:
        links = self.consistency.state_dict()["links"]
        rows: list[tuple[str, dict[str, Any]]] = []
        for link_id, value in links.items():
            link = dict(value)
            if link["port_id"] != port_id:
                continue
            if int(link["consistent_count"]) < self.config.minimum_consistent_count:
                continue
            if float(link["reliability"]) < self.config.minimum_reliability:
                continue
            rows.append((str(link_id), link))
        return tuple(
            sorted(
                rows,
                key=lambda row: (
                    str(row[1]["target"]),
                    int(row[1]["polarity"]),
                    row[0],
                ),
            )
        )

    @staticmethod
    def _target_unit_id(target: str) -> int:
        prefix = "unit:"
        if not target.startswith(prefix) or not target[len(prefix) :].isdigit():
            raise ValueError("relation re-entry target must use unit:<non-negative-int>")
        return int(target[len(prefix) :])

    def state_dict(self) -> dict[str, Any]:
        value = {
            "config": asdict(self.config),
            "processed_boundary_event_ids": sorted(self._processed_boundary_event_ids),
            "records": [row.state_dict() for row in self.records],
        }
        validate_runtime_mapping(value, path="v06.relation_reentry")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())
