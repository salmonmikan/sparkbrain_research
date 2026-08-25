from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import asdict, dataclass, fields, is_dataclass, replace

from .contracts import (
    EvidenceAuditRow,
    EvidenceContribution,
    EvidenceRecord,
    EvidenceSummary,
)

EVIDENCE_LEDGER_SCHEMA_VERSION = "0.3"
_ZERO_HASH = "0" * 64


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _qualified_type(value: object) -> str:
    value_type = type(value)
    return f"{value_type.__module__}.{value_type.__qualname__}"


def rejection_envelope_hash(value: object, *, stable_reason_code: str) -> str:
    """Hash only deterministic type metadata for an invalid attempted payload."""

    if isinstance(value, Mapping):
        top_level = {key: item for key, item in value.items() if isinstance(key, str)}
    elif is_dataclass(value) and not isinstance(value, type):
        top_level = {field.name: getattr(value, field.name) for field in fields(value)}
    else:
        top_level = {}
    evidence_id = top_level.get("evidence_id")
    envelope = {
        "evidence_id_if_string_else_empty": evidence_id
        if isinstance(evidence_id, str)
        else "",
        "fully_qualified_value_type": _qualified_type(value),
        "sorted_string_top_level_keys": sorted(top_level),
        "sorted_top_level_field_type_names": sorted(
            f"{key}:{_qualified_type(item)}" for key, item in top_level.items()
        ),
        "stable_reason_code": stable_reason_code,
    }
    return _sha256(_canonical_json(envelope))


class EvidenceRejection(ValueError):
    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def derive_evidence_id(
    *, spark_evidence_id: str, hypothesis_id: str, polarity: str
) -> str:
    if not spark_evidence_id or not hypothesis_id:
        raise ValueError("spark evidence and hypothesis IDs must not be empty")
    if polarity not in {"support", "contradict", "neutral"}:
        raise ValueError("invalid evidence polarity")
    payload = _canonical_json(
        [EVIDENCE_LEDGER_SCHEMA_VERSION, spark_evidence_id, hypothesis_id, polarity]
    )
    return f"ev-{_sha256(payload)}"


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
    """Immutable records, transitive active state, and an append-only audit chain."""

    def __init__(self, config: EvidenceLedgerConfig | None = None) -> None:
        self.config = config or EvidenceLedgerConfig()
        self.config.validate()
        self._records: dict[str, EvidenceRecord] = {}
        self._active: dict[str, bool] = {}
        self._audit: list[EvidenceAuditRow] = []
        self._sample_ids: set[str] = set()
        self._spark_to_samples: dict[str, tuple[str, ...]] = {}
        self.duplicate_deliveries: dict[str, int] = {}

    def reset(self) -> None:
        self._records.clear()
        self._active.clear()
        self._audit.clear()
        self._sample_ids.clear()
        self._spark_to_samples.clear()
        self.duplicate_deliveries.clear()

    def register_sample(self, sample_id: str) -> None:
        if not sample_id:
            raise ValueError("sample_id must not be empty")
        self._sample_ids.add(sample_id)

    def register_spark(self, spark_id: str, parent_sample_ids: tuple[str, ...]) -> None:
        if not spark_id:
            raise ValueError("spark_id must not be empty")
        if (
            not parent_sample_ids
            or tuple(sorted(parent_sample_ids)) != parent_sample_ids
            or len(set(parent_sample_ids)) != len(parent_sample_ids)
        ):
            raise ValueError("parent_sample_ids must be non-empty, sorted, and unique")
        unknown = set(parent_sample_ids) - self._sample_ids
        if unknown:
            raise ValueError(f"Spark lineage has unknown samples: {sorted(unknown)}")
        previous = self._spark_to_samples.get(spark_id)
        if previous is not None and previous != parent_sample_ids:
            raise ValueError("one spark_id cannot change parent samples")
        self._spark_to_samples[spark_id] = parent_sample_ids

    def add(
        self,
        row: object,
        *,
        delivered_at: float | None = None,
    ) -> None:
        state_before = self.active_state_hash()
        event_time = self._safe_event_time(row, delivered_at)
        try:
            if isinstance(row, EvidenceContribution):
                record = self._legacy_record(row)
            elif isinstance(row, EvidenceRecord):
                record = row
            else:
                raise EvidenceRejection(
                    "invalid_record_type", "evidence payload must be an EvidenceRecord"
                )
            record.validate()
            delivery_time = record.time if delivered_at is None else float(delivered_at)
            if not math.isfinite(delivery_time) or delivery_time < record.time:
                raise EvidenceRejection(
                    "invalid_delivery_time",
                    "delivery time must be finite and not precede evidence time",
                )
        except (TypeError, ValueError) as exc:
            reason_code = getattr(exc, "reason_code", "invalid_record")
            self._audit_rejection(
                attempted=row,
                evidence_id=self._attempted_evidence_id(row),
                event_time=event_time,
                reason_code=reason_code,
                reason=str(exc) or reason_code,
                before_active=None,
                state_hash=state_before,
            )
            raise ValueError(str(exc) or reason_code) from exc

        if isinstance(row, EvidenceContribution):
            sample_id = f"legacy-sample:{record.evidence_id}"
            spark_id = record.parent_spark_ids[0]
            self.register_sample(sample_id)
            self.register_spark(spark_id, (sample_id,))
        previous = self._records.get(record.evidence_id)
        payload_hash = _sha256(record.to_canonical_json())
        if previous is not None:
            if previous != record:
                active = self._active[record.evidence_id]
                self._audit_rejection(
                    attempted=row,
                    evidence_id=record.evidence_id,
                    event_time=delivery_time,
                    reason_code="immutable_payload_mismatch",
                    reason="immutable evidence payload mismatch",
                    before_active=active,
                    state_hash=self.active_state_hash(),
                )
                raise ValueError("one evidence_id cannot change its immutable payload")
            active = self._active[record.evidence_id]
            self.duplicate_deliveries[record.evidence_id] = (
                self.duplicate_deliveries.get(record.evidence_id, 0) + 1
            )
            self._audit_event(
                action="redelivery_noop",
                evidence_id=record.evidence_id,
                event_time=delivery_time,
                reason="exact immutable payload redelivered",
                before_active=active,
                after_active=active,
                payload_hash=payload_hash,
            )
            return

        try:
            self._validate_lineage(record)
        except EvidenceRejection as exc:
            self._audit_rejection(
                attempted=row,
                evidence_id=record.evidence_id,
                event_time=delivery_time,
                reason_code=exc.reason_code,
                reason=str(exc),
                before_active=None,
                state_hash=self.active_state_hash(),
            )
            raise
        before = self.active_state_hash()
        self._records[record.evidence_id] = record
        self._active[record.evidence_id] = True
        after = self.active_state_hash()
        self._audit_event(
            action="add",
            evidence_id=record.evidence_id,
            event_time=delivery_time,
            reason="new immutable evidence",
            before_active=None,
            after_active=True,
            payload_hash=payload_hash,
            state_hash_before=before,
            state_hash_after=after,
        )

    def deactivate(
        self,
        evidence_id: str,
        *,
        at_time: float,
        reason: str = "causal intervention",
    ) -> None:
        record = self.resolve(evidence_id)
        if not self._active[evidence_id]:
            raise ValueError("evidence is already inactive")
        self._validate_intervention_time(at_time, record)
        before = self.active_state_hash()
        self._active[evidence_id] = False
        after = self.active_state_hash()
        self._audit_event(
            action="deactivate",
            evidence_id=record.evidence_id,
            event_time=at_time,
            reason=reason,
            before_active=True,
            after_active=False,
            payload_hash=_sha256(record.to_canonical_json()),
            state_hash_before=before,
            state_hash_after=after,
        )

    def restore(
        self,
        evidence_id: str,
        *,
        at_time: float,
        reason: str = "restore causal intervention",
    ) -> None:
        record = self.resolve(evidence_id)
        if self._active[evidence_id]:
            raise ValueError("evidence is already active")
        self._validate_intervention_time(at_time, record)
        before = self.active_state_hash()
        self._active[evidence_id] = True
        after = self.active_state_hash()
        self._audit_event(
            action="restore",
            evidence_id=record.evidence_id,
            event_time=at_time,
            reason=reason,
            before_active=False,
            after_active=True,
            payload_hash=_sha256(record.to_canonical_json()),
            state_hash_before=before,
            state_hash_after=after,
        )

    def remove(self, evidence_id: str) -> None:
        record = self.resolve(evidence_id)
        self.deactivate(evidence_id, at_time=record.time, reason="legacy remove alias")

    def resolve(self, evidence_id: str) -> EvidenceRecord:
        try:
            return self._records[evidence_id]
        except KeyError as exc:
            raise KeyError(f"unknown evidence ID: {evidence_id}") from exc

    def is_active(self, evidence_id: str, *, effective: bool = False) -> bool:
        self.resolve(evidence_id)
        return (
            self._effective_active(evidence_id, set())
            if effective
            else self._active[evidence_id]
        )

    def rows(self, *, active_only: bool = True) -> tuple[EvidenceRecord, ...]:
        return tuple(
            self._records[key]
            for key in sorted(self._records)
            if not active_only or self._effective_active(key, set())
        )

    def audit_rows(self) -> tuple[EvidenceAuditRow, ...]:
        return tuple(self._audit)

    def active_state_hash(self) -> str:
        return _sha256(
            _canonical_json(
                {
                    "active": {key: self._active[key] for key in sorted(self._active)},
                    "config": asdict(self.config),
                    "records": {
                        key: json.loads(self._records[key].to_canonical_json())
                        for key in sorted(self._records)
                    },
                    "schema_version": EVIDENCE_LEDGER_SCHEMA_VERSION,
                }
            )
        )

    def state_hash(self) -> str:
        return self.active_state_hash()

    def audit_chain_hash(self) -> str:
        return self._audit[-1].audit_hash if self._audit else _ZERO_HASH

    def lineage_resolution_rate(self) -> float:
        citations = 0
        resolved = 0
        for record in self._records.values():
            for parent in record.parent_evidence_ids:
                citations += 1
                resolved += int(parent in self._records)
            for spark_id in record.parent_spark_ids:
                citations += 1
                sample_ids = self._spark_to_samples.get(spark_id, ())
                resolved += int(
                    bool(sample_ids)
                    and all(item in self._sample_ids for item in sample_ids)
                )
        return 1.0 if citations == 0 else resolved / citations

    def active_projection(self, entity_key: str) -> str:
        return _canonical_json(
            {
                "entity_key": entity_key,
                "records": [
                    json.loads(record.to_canonical_json())
                    for record in self.rows()
                    if record.entity_key == entity_key
                ],
            }
        )

    def serialize_state(self) -> str:
        return _canonical_json(
            {
                "active": {key: self._active[key] for key in sorted(self._active)},
                "audit": [json.loads(row.to_canonical_json()) for row in self._audit],
                "config": asdict(self.config),
                "duplicate_deliveries": dict(sorted(self.duplicate_deliveries.items())),
                "records": {
                    key: json.loads(self._records[key].to_canonical_json())
                    for key in sorted(self._records)
                },
                "sample_ids": sorted(self._sample_ids),
                "schema_version": EVIDENCE_LEDGER_SCHEMA_VERSION,
                "spark_to_samples": {
                    key: list(self._spark_to_samples[key]) for key in sorted(self._spark_to_samples)
                },
            }
        )

    @classmethod
    def from_serialized_state(cls, payload: str) -> EvidenceLedger:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("EvidenceLedger state must be valid JSON") from exc
        expected = {
            "active",
            "audit",
            "config",
            "duplicate_deliveries",
            "records",
            "sample_ids",
            "schema_version",
            "spark_to_samples",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("EvidenceLedger state has unexpected fields")
        if value["schema_version"] != EVIDENCE_LEDGER_SCHEMA_VERSION:
            raise ValueError("unsupported EvidenceLedger schema version")
        try:
            ledger = cls(EvidenceLedgerConfig(**value["config"]))
            ledger._sample_ids = set(value["sample_ids"])
            ledger._spark_to_samples = {
                key: tuple(parents) for key, parents in value["spark_to_samples"].items()
            }
            ledger._records = {
                key: EvidenceRecord.from_canonical_json(_canonical_json(record))
                for key, record in value["records"].items()
            }
            ledger._active = dict(value["active"])
            ledger._audit = [
                EvidenceAuditRow.from_canonical_json(_canonical_json(row))
                for row in value["audit"]
            ]
            ledger.duplicate_deliveries = dict(value["duplicate_deliveries"])
            ledger._validate_loaded_state()
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("invalid EvidenceLedger state") from exc
        if ledger.serialize_state() != payload:
            raise ValueError("EvidenceLedger state is not strict canonical JSON")
        return ledger

    def summary(self, belief_key: str, *, object_key: str | None, now: float) -> EvidenceSummary:
        if not math.isfinite(now) or now < 0:
            raise ValueError("summary time must be finite and non-negative")
        entity_key = "__global__" if object_key is None else object_key
        rows = [
            record
            for record in self.rows()
            if record.hypothesis_id == belief_key and record.entity_key == entity_key
        ]
        weighted = [
            (
                record,
                record.strength
                * math.exp(-max(0.0, now - record.time) / self.config.recency_tau),
            )
            for record in rows
        ]
        groups: dict[str, list[tuple[EvidenceRecord, float]]] = {}
        for item in weighted:
            record = item[0]
            group = record.correlation_group or f"evidence:{record.evidence_id}"
            groups.setdefault(group, []).append(item)

        support = 0.0
        contradiction = 0.0
        redundancy = 0.0
        for items in groups.values():
            for polarity in ("support", "contradict"):
                values = sorted(
                    (value for record, value in items if record.polarity == polarity),
                    reverse=True,
                )
                if not values:
                    continue
                effective = values[0] + self.config.correlation_discount * sum(values[1:])
                if polarity == "support":
                    support += effective
                else:
                    contradiction += effective
                redundancy += (1.0 - self.config.correlation_discount) * sum(values[1:])

        support_rows = [record for record in rows if record.polarity == "support"]
        contradiction_rows = [record for record in rows if record.polarity == "contradict"]
        support_groups = {
            record.correlation_group or f"evidence:{record.evidence_id}"
            for record in support_rows
        }
        return EvidenceSummary(
            belief_key=belief_key,
            object_key=object_key,
            effective_support=support,
            effective_contradiction=contradiction,
            redundancy=redundancy,
            unique_evidence_count=len(support_rows),
            source_count=len({record.source_id for record in support_rows}),
            independent_group_count=len(support_groups),
            support_ids=tuple(sorted(record.evidence_id for record in support_rows)),
            contradiction_ids=tuple(
                sorted(record.evidence_id for record in contradiction_rows)
            ),
        )

    def _audit_event(
        self,
        *,
        action: str,
        evidence_id: str,
        event_time: float,
        reason: str,
        before_active: bool | None,
        after_active: bool | None,
        payload_hash: str,
        state_hash_before: str | None = None,
        state_hash_after: str | None = None,
    ) -> None:
        previous = self.audit_chain_hash()
        sequence = len(self._audit)
        row = EvidenceAuditRow(
            schema_version=EVIDENCE_LEDGER_SCHEMA_VERSION,
            audit_id=f"audit:{sequence:08d}",
            sequence=sequence,
            branch_id="main",
            action=action,
            evidence_id=evidence_id,
            event_time=event_time,
            reason=reason,
            before_active=before_active,
            after_active=after_active,
            payload_hash=payload_hash,
            active_state_hash_before=state_hash_before or self.active_state_hash(),
            active_state_hash_after=state_hash_after or self.active_state_hash(),
            previous_audit_hash=previous,
            audit_hash=_ZERO_HASH,
        )
        payload = json.loads(row.to_canonical_json())
        payload.pop("audit_hash")
        final = replace(row, audit_hash=_sha256(_canonical_json(payload)))
        final.validate()
        self._audit.append(final)

    def _audit_rejection(
        self,
        *,
        attempted: object,
        evidence_id: str,
        event_time: float,
        reason_code: str,
        reason: str,
        before_active: bool | None,
        state_hash: str,
    ) -> None:
        self._audit_event(
            action="rejection",
            evidence_id=evidence_id or "__invalid__",
            event_time=event_time,
            reason=reason,
            before_active=before_active,
            after_active=before_active,
            payload_hash=rejection_envelope_hash(
                attempted, stable_reason_code=reason_code
            ),
            state_hash_before=state_hash,
            state_hash_after=state_hash,
        )

    def _validate_lineage(self, record: EvidenceRecord) -> None:
        if record.evidence_id in record.parent_evidence_ids:
            raise EvidenceRejection(
                "self_parent", "evidence cannot cite itself as a parent"
            )
        unknown_evidence = set(record.parent_evidence_ids) - self._records.keys()
        if unknown_evidence:
            raise EvidenceRejection(
                "unknown_parent_evidence", "unknown parent evidence IDs"
            )
        unknown_sparks = set(record.parent_spark_ids) - self._spark_to_samples.keys()
        if unknown_sparks:
            raise EvidenceRejection("unknown_parent_spark", "unknown parent Spark IDs")
        self._assert_acyclic(extra=record)

    def _assert_acyclic(self, *, extra: EvidenceRecord | None = None) -> None:
        parents = {
            key: record.parent_evidence_ids for key, record in self._records.items()
        }
        if extra is not None:
            parents[extra.evidence_id] = extra.parent_evidence_ids
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(evidence_id: str) -> None:
            if evidence_id in visiting:
                raise EvidenceRejection("lineage_cycle", "evidence lineage cycle detected")
            if evidence_id in visited:
                return
            visiting.add(evidence_id)
            for parent in parents.get(evidence_id, ()):
                visit(parent)
            visiting.remove(evidence_id)
            visited.add(evidence_id)

        for evidence_id in sorted(parents):
            visit(evidence_id)

    def _effective_active(self, evidence_id: str, visiting: set[str]) -> bool:
        if evidence_id in visiting:
            raise ValueError("evidence lineage cycle detected")
        if not self._active[evidence_id]:
            return False
        visiting.add(evidence_id)
        result = all(
            self._effective_active(parent, visiting)
            for parent in self._records[evidence_id].parent_evidence_ids
        )
        visiting.remove(evidence_id)
        return result

    def _validate_loaded_state(self) -> None:
        if set(self._active) != set(self._records):
            raise ValueError("active evidence keys must match records")
        if any(not isinstance(value, bool) for value in self._active.values()):
            raise ValueError("active flags must be booleans")
        if any(
            key not in self._records or not isinstance(count, int) or count < 0
            for key, count in self.duplicate_deliveries.items()
        ):
            raise ValueError("invalid duplicate delivery counters")
        for spark_id, sample_ids in self._spark_to_samples.items():
            if (
                not spark_id
                or not sample_ids
                or any(item not in self._sample_ids for item in sample_ids)
            ):
                raise ValueError("invalid Spark-to-sample lineage")
        self._assert_acyclic()
        for record in self._records.values():
            self._validate_lineage(record)
        previous = _ZERO_HASH
        for sequence, row in enumerate(self._audit):
            if row.sequence != sequence or row.previous_audit_hash != previous:
                raise ValueError("invalid evidence audit chain ordering")
            payload = json.loads(row.to_canonical_json())
            audit_hash = payload.pop("audit_hash")
            if audit_hash != _sha256(_canonical_json(payload)):
                raise ValueError("invalid evidence audit hash")
            previous = row.audit_hash

    @staticmethod
    def _validate_intervention_time(at_time: float, record: EvidenceRecord) -> None:
        if not math.isfinite(at_time) or at_time < record.time:
            raise ValueError("intervention time must be finite and not precede evidence time")

    @staticmethod
    def _attempted_evidence_id(value: object) -> str:
        if isinstance(value, Mapping):
            evidence_id = value.get("evidence_id")
        else:
            evidence_id = getattr(value, "evidence_id", "")
        return evidence_id if isinstance(evidence_id, str) else ""

    @staticmethod
    def _safe_event_time(value: object, delivered_at: float | None) -> float:
        candidate = delivered_at
        if candidate is None:
            candidate = getattr(value, "time", 0.0)
        try:
            event_time = float(candidate)
        except (TypeError, ValueError):
            return 0.0
        return event_time if math.isfinite(event_time) and event_time >= 0 else 0.0

    @staticmethod
    def _legacy_record(row: EvidenceContribution) -> EvidenceRecord:
        row.validate()
        if row.support > 0:
            polarity = "support"
            strength = row.support
        elif row.contradiction > 0:
            polarity = "contradict"
            strength = row.contradiction
        else:
            polarity = "neutral"
            strength = 0.0
        return EvidenceRecord(
            evidence_id=row.evidence_id,
            source_id=row.source_id,
            entity_key=row.object_key or "__global__",
            hypothesis_id=row.belief_key,
            time=row.time,
            polarity=polarity,
            strength=strength,
            correlation_group=row.correlation_group,
            parent_evidence_ids=tuple(sorted(row.parent_ids)),
            parent_spark_ids=(f"legacy-spark:{row.evidence_id}",),
        )
