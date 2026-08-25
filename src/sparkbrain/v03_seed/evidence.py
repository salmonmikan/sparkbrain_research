from __future__ import annotations

import math
from dataclasses import dataclass

from .contracts import EvidenceContribution, EvidenceSummary


@dataclass(frozen=True, slots=True)
class EvidenceLedgerConfig:
    correlation_discount: float = 0.20
    recency_tau: float = 30.0

    def validate(self) -> None:
        if not 0 <= self.correlation_discount <= 1:
            raise ValueError("correlation_discount must be in [0, 1]")
        if self.recency_tau <= 0 or not math.isfinite(self.recency_tau):
            raise ValueError("recency_tau must be finite and positive")


class EvidenceLedger:
    """Deduplicated, correlation-aware evidence storage."""

    def __init__(self, config: EvidenceLedgerConfig | None = None) -> None:
        self.config = config or EvidenceLedgerConfig()
        self.config.validate()
        self._rows: dict[str, EvidenceContribution] = {}
        self.duplicate_deliveries: dict[str, int] = {}

    def reset(self) -> None:
        self._rows.clear()
        self.duplicate_deliveries.clear()

    def add(self, row: EvidenceContribution) -> None:
        row.validate()
        previous = self._rows.get(row.evidence_id)
        if previous is None:
            self._rows[row.evidence_id] = row
            return
        if (previous.belief_key, previous.object_key) != (row.belief_key, row.object_key):
            raise ValueError("one evidence_id cannot be reassigned to another belief/object")
        if previous.source_id != row.source_id:
            raise ValueError("one evidence_id cannot be reassigned to another source")
        if (
            previous.correlation_group is not None
            and row.correlation_group is not None
            and previous.correlation_group != row.correlation_group
        ):
            raise ValueError("one evidence_id cannot change correlation group")
        self.duplicate_deliveries[row.evidence_id] = (
            self.duplicate_deliveries.get(row.evidence_id, 0) + 1
        )
        # Re-delivery is not another vote.  Keep the strongest attributable form
        # and the latest time for decay, while preserving the original identity.
        self._rows[row.evidence_id] = EvidenceContribution(
            evidence_id=row.evidence_id,
            source_id=previous.source_id,
            belief_key=row.belief_key,
            time=max(previous.time, row.time),
            support=max(previous.support, row.support),
            contradiction=max(previous.contradiction, row.contradiction),
            correlation_group=previous.correlation_group or row.correlation_group,
            object_key=row.object_key,
            parent_ids=tuple(sorted(set(previous.parent_ids + row.parent_ids))),
        )

    def remove(self, evidence_id: str) -> None:
        self._rows.pop(evidence_id, None)
        self.duplicate_deliveries.pop(evidence_id, None)

    def rows(self) -> tuple[EvidenceContribution, ...]:
        return tuple(self._rows[key] for key in sorted(self._rows))

    def summary(self, belief_key: str, *, object_key: str | None, now: float) -> EvidenceSummary:
        rows = [
            row
            for row in self._rows.values()
            if row.belief_key == belief_key and row.object_key == object_key
        ]
        weighted: list[tuple[EvidenceContribution, float, float, float]] = []
        for row in rows:
            age = max(0.0, now - row.time)
            recency = math.exp(-age / self.config.recency_tau)
            weighted.append(
                (row, row.support * recency, row.contradiction * recency, recency)
            )

        groups: dict[str, list[tuple[EvidenceContribution, float, float, float]]] = {}
        for item in weighted:
            row = item[0]
            group = row.correlation_group or f"evidence:{row.evidence_id}"
            groups.setdefault(group, []).append(item)

        support = 0.0
        contradiction = 0.0
        redundancy = 0.0
        for items in groups.values():
            support_values = sorted((item[1] for item in items), reverse=True)
            contradiction_values = sorted((item[2] for item in items), reverse=True)
            if support_values:
                support += support_values[0] + self.config.correlation_discount * sum(
                    support_values[1:]
                )
                redundancy += (1.0 - self.config.correlation_discount) * sum(support_values[1:])
            if contradiction_values:
                contradiction += contradiction_values[0] + self.config.correlation_discount * sum(
                    contradiction_values[1:]
                )
                redundancy += (1.0 - self.config.correlation_discount) * sum(
                    contradiction_values[1:]
                )

        support_rows = [row for row in rows if row.support > 0]
        support_ids = tuple(sorted(row.evidence_id for row in support_rows))
        contradiction_ids = tuple(
            sorted(row.evidence_id for row in rows if row.contradiction > 0)
        )
        support_groups = {
            row.correlation_group or f"evidence:{row.evidence_id}" for row in support_rows
        }
        return EvidenceSummary(
            belief_key=belief_key,
            object_key=object_key,
            effective_support=support,
            effective_contradiction=contradiction,
            redundancy=redundancy,
            unique_evidence_count=len(support_rows),
            source_count=len({row.source_id for row in support_rows}),
            independent_group_count=len(support_groups),
            support_ids=support_ids,
            contradiction_ids=contradiction_ids,
        )
