from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import StrEnum
from typing import Any

from sparkbrain.v06.boundary import BoundaryEvent
from sparkbrain.v06.consistency import (
    AnonymousConsistencyResolution,
    UntypedBoundaryConsistency,
)
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)
from sparkbrain.v06.local_expectation import (
    LocalExpectationConfig,
    LocalTemporalExpectation,
    LocalTransitionStats,
)


@dataclass(slots=True)
class A01CausalSupportState:
    external_consistent_count: int = 0
    external_contradicted_count: int = 0

    def reliability(self) -> float:
        return (1.0 + self.external_consistent_count) / (
            2.0
            + self.external_consistent_count
            + self.external_contradicted_count
        )

    def gain(self) -> float:
        return self.reliability() / 0.5

    def observe(self, *, matched: bool) -> None:
        if matched:
            self.external_consistent_count += 1
        else:
            self.external_contradicted_count += 1

    def state_dict(self) -> dict[str, int]:
        return asdict(self)

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> A01CausalSupportState:
        row = cls(
            external_consistent_count=int(value["external_consistent_count"]),
            external_contradicted_count=int(value["external_contradicted_count"]),
        )
        if row.external_consistent_count < 0 or row.external_contradicted_count < 0:
            raise ValueError("A01 causal-support counts must be non-negative")
        return row


class A01LocalTemporalExpectation(LocalTemporalExpectation):
    """G1 plus explicit anonymous external causal support for existing local paths."""

    def __init__(self, config: LocalExpectationConfig | None = None) -> None:
        super().__init__(config)
        self._causal_support: dict[str, A01CausalSupportState] = {}

    def observe_causal_evidence(
        self,
        path_ids: tuple[str, ...],
        *,
        matched: bool,
    ) -> None:
        if not path_ids:
            raise ValueError("A01 causal evidence requires at least one local path")
        unique = tuple(dict.fromkeys(path_ids))
        if len(unique) != len(path_ids):
            raise ValueError("A01 causal path IDs must be unique")
        known = {
            f"local:{source}->{target}"
            for source, table in self._transitions.items()
            for target in table
        }
        unknown = set(unique) - known
        if unknown:
            raise ValueError(f"A01 causal evidence references unknown paths: {sorted(unknown)}")
        for path_id in unique:
            self._causal_support.setdefault(path_id, A01CausalSupportState()).observe(
                matched=matched
            )

    def causal_support(self, path_id: str) -> A01CausalSupportState:
        return self._causal_support.get(path_id, A01CausalSupportState())

    def causal_reliability(self, path_id: str) -> float:
        return self.causal_support(path_id).reliability()

    def causal_gain(self, path_id: str) -> float:
        return self.causal_support(path_id).gain()

    def proposals_for(
        self,
        source: RuntimePulse,
        *,
        origin_state_hash: str,
    ) -> tuple[EndogenousPulseProposal, ...]:
        base_rows = super().proposals_for(
            source,
            origin_state_hash=origin_state_hash,
        )
        adjusted: list[EndogenousPulseProposal] = []
        for row in base_rows:
            if len(row.local_path_ids) != 1:
                raise ValueError("A01 requires exactly one local path per G1 proposal")
            path_id = row.local_path_ids[0]
            confidence = min(1.0, row.confidence * self.causal_gain(path_id))
            adjusted.append(replace(row, confidence=confidence))
        return tuple(adjusted)

    def learned_state_dict(self) -> dict[str, Any]:
        value = super().learned_state_dict()
        value["a01_causal_support"] = {
            path_id: row.state_dict()
            for path_id, row in sorted(self._causal_support.items())
        }
        validate_runtime_mapping(value, path="v061_a01.local_expectation.learned")
        return value

    def state_dict(self) -> dict[str, Any]:
        value = super().state_dict()
        value["a01_causal_support"] = {
            path_id: row.state_dict()
            for path_id, row in sorted(self._causal_support.items())
        }
        validate_runtime_mapping(value, path="v061_a01.local_expectation")
        return value

    def learned_state_hash(self) -> str:
        return digest(self.learned_state_dict())

    def state_hash(self) -> str:
        return digest(self.state_dict())

    @classmethod
    def from_learned_state_dict(
        cls,
        value: dict[str, Any],
    ) -> A01LocalTemporalExpectation:
        validate_runtime_mapping(value, path="v061_a01.local_expectation.learned")
        model = cls(LocalExpectationConfig(**value["config"]))
        model.external_transition_count = int(value["external_transition_count"])
        model.proposal_count = 0
        model._transitions = {
            str(source): {
                str(target): LocalTransitionStats.from_state_dict(dict(stats))
                for target, stats in table.items()
            }
            for source, table in value["transitions"].items()
        }
        model._causal_support = {
            str(path_id): A01CausalSupportState.from_state_dict(dict(row))
            for path_id, row in value.get("a01_causal_support", {}).items()
        }
        model._validate_transition_count()
        model._validate_causal_support_paths()
        return model

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> A01LocalTemporalExpectation:
        validate_runtime_mapping(value, path="v061_a01.local_expectation")
        model = cls(LocalExpectationConfig(**value["config"]))
        model.external_transition_count = int(value["external_transition_count"])
        model.proposal_count = int(value["proposal_count"])
        model._transitions = {
            str(source): {
                str(target): LocalTransitionStats.from_state_dict(dict(stats))
                for target, stats in table.items()
            }
            for source, table in value["transitions"].items()
        }
        model._causal_support = {
            str(path_id): A01CausalSupportState.from_state_dict(dict(row))
            for path_id, row in value.get("a01_causal_support", {}).items()
        }
        model._validate_transition_count()
        model._validate_causal_support_paths()
        return model

    def _validate_transition_count(self) -> None:
        observed = sum(
            stats.count
            for table in self._transitions.values()
            for stats in table.values()
        )
        if observed != self.external_transition_count:
            raise ValueError("A01 transition count does not match transition content")

    def _validate_causal_support_paths(self) -> None:
        known = {
            f"local:{source}->{target}"
            for source, table in self._transitions.items()
            for target in table
        }
        unknown = set(self._causal_support) - known
        if unknown:
            raise ValueError(f"A01 restored causal support has unknown paths: {sorted(unknown)}")


@dataclass(frozen=True, slots=True)
class A01PriorRelation:
    target: str
    polarity: int
    reliability: float


class A01CausalCreditStatus(StrEnum):
    EXACT_MATCH = "exact-match"
    EXACT_CONTRADICTION = "exact-contradiction"
    ABSTAINED_NO_PRIOR = "abstained-no-prior"
    ABSTAINED_NO_PATH = "abstained-no-path"
    FALLBACK_PAIRED_NO_CREDIT = "fallback-paired-no-credit"
    UNPAIRED_NO_CREDIT = "unpaired-no-credit"
    EXACT_PARENT_NOT_PAIRED = "exact-parent-not-paired"


@dataclass(frozen=True, slots=True)
class A01CausalCreditResolution:
    status: A01CausalCreditStatus
    boundary_event_id: str
    external_event_id: str
    prior_relation: A01PriorRelation | None
    path_ids: tuple[str, ...]
    path_reliability_before: tuple[tuple[str, float], ...]
    path_reliability_after: tuple[tuple[str, float], ...]
    consistency_resolution: AnonymousConsistencyResolution

    @property
    def positive_credit_applied(self) -> bool:
        return self.status is A01CausalCreditStatus.EXACT_MATCH

    @property
    def contradiction_credit_applied(self) -> bool:
        return self.status is A01CausalCreditStatus.EXACT_CONTRADICTION

    def state_dict(self) -> dict[str, Any]:
        return {
            "boundary_event_id": self.boundary_event_id,
            "consistency_resolution": self.consistency_resolution.state_dict(),
            "external_event_id": self.external_event_id,
            "path_ids": self.path_ids,
            "path_reliability_after": self.path_reliability_after,
            "path_reliability_before": self.path_reliability_before,
            "prior_relation": (
                asdict(self.prior_relation) if self.prior_relation is not None else None
            ),
            "status": self.status.value,
        }


class A01TransientCreditBridge:
    """Use only exact-parent external evidence to update actual historical G1 paths."""

    def __init__(
        self,
        expectation: A01LocalTemporalExpectation,
        consistency: UntypedBoundaryConsistency,
        ledger: ProvenanceLedger,
    ) -> None:
        if consistency.ledger is not ledger:
            raise ValueError("A01 bridge components must share one provenance ledger")
        self.expectation = expectation
        self.consistency = consistency
        self.ledger = ledger
        self.resolutions: list[A01CausalCreditResolution] = []

    def observe_external(
        self,
        boundary: BoundaryEvent,
        external: RuntimePulse,
    ) -> A01CausalCreditResolution:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("A01 bridge accepts only external events")
        registered = self.ledger.events.get(external.event_id)
        if registered is None or registered != external:
            raise ValueError("A01 external event must be registered in the shared ledger")

        prior = self._dominant_prior_relation(boundary.port_id)
        exact_parent = boundary.event_id in external.parent_event_ids
        consistency_resolution = self.consistency.observe_external(external)

        if not exact_parent:
            status = (
                A01CausalCreditStatus.FALLBACK_PAIRED_NO_CREDIT
                if consistency_resolution.boundary_event_id is not None
                else A01CausalCreditStatus.UNPAIRED_NO_CREDIT
            )
            return self._record(
                status=status,
                boundary=boundary,
                external=external,
                prior=prior,
                path_ids=(),
                before=(),
                after=(),
                consistency_resolution=consistency_resolution,
            )

        if consistency_resolution.boundary_event_id != boundary.event_id:
            return self._record(
                status=A01CausalCreditStatus.EXACT_PARENT_NOT_PAIRED,
                boundary=boundary,
                external=external,
                prior=prior,
                path_ids=(),
                before=(),
                after=(),
                consistency_resolution=consistency_resolution,
            )

        if prior is None:
            return self._record(
                status=A01CausalCreditStatus.ABSTAINED_NO_PRIOR,
                boundary=boundary,
                external=external,
                prior=None,
                path_ids=(),
                before=(),
                after=(),
                consistency_resolution=consistency_resolution,
            )

        path_ids = self._causal_path_ids(boundary.source_proposal_ids)
        if not path_ids:
            return self._record(
                status=A01CausalCreditStatus.ABSTAINED_NO_PATH,
                boundary=boundary,
                external=external,
                prior=prior,
                path_ids=(),
                before=(),
                after=(),
                consistency_resolution=consistency_resolution,
            )

        before = self._path_reliabilities(path_ids)
        matched = prior.target == external.target and prior.polarity == external.polarity
        self.expectation.observe_causal_evidence(path_ids, matched=matched)
        after = self._path_reliabilities(path_ids)
        status = (
            A01CausalCreditStatus.EXACT_MATCH
            if matched
            else A01CausalCreditStatus.EXACT_CONTRADICTION
        )
        return self._record(
            status=status,
            boundary=boundary,
            external=external,
            prior=prior,
            path_ids=path_ids,
            before=before,
            after=after,
            consistency_resolution=consistency_resolution,
        )

    def _dominant_prior_relation(self, port_id: str) -> A01PriorRelation | None:
        learned = self.consistency.learned_state_dict()
        rows: list[A01PriorRelation] = []
        for value in learned["links"].values():
            row = dict(value)
            if str(row["port_id"]) != port_id or int(row["consistent_count"]) < 1:
                continue
            consistent = int(row["consistent_count"])
            inconsistent = int(row["inconsistent_count"])
            reliability = (
                self.consistency.config.prior_consistent + consistent
            ) / (
                self.consistency.config.prior_consistent
                + self.consistency.config.prior_inconsistent
                + consistent
                + inconsistent
            )
            rows.append(
                A01PriorRelation(
                    target=str(row["target"]),
                    polarity=int(row["polarity"]),
                    reliability=reliability,
                )
            )
        if not rows:
            return None
        maximum = max(row.reliability for row in rows)
        winners = [row for row in rows if row.reliability == maximum]
        return winners[0] if len(winners) == 1 else None

    def _causal_path_ids(self, proposal_ids: tuple[str, ...]) -> tuple[str, ...]:
        pending = list(proposal_ids)
        visited: set[str] = set()
        paths: set[str] = set()
        while pending:
            proposal_id = pending.pop()
            if proposal_id in visited:
                continue
            visited.add(proposal_id)
            proposal = self.ledger.proposals.get(proposal_id)
            if proposal is None:
                raise ValueError(
                    f"A01 boundary references unknown proposal: {proposal_id}"
                )
            paths.update(proposal.local_path_ids)
            pending.extend(proposal.parent_proposal_ids)
        return tuple(sorted(paths))

    def _path_reliabilities(
        self,
        path_ids: tuple[str, ...],
    ) -> tuple[tuple[str, float], ...]:
        return tuple(
            (path_id, self.expectation.causal_reliability(path_id))
            for path_id in path_ids
        )

    def _record(
        self,
        *,
        status: A01CausalCreditStatus,
        boundary: BoundaryEvent,
        external: RuntimePulse,
        prior: A01PriorRelation | None,
        path_ids: tuple[str, ...],
        before: tuple[tuple[str, float], ...],
        after: tuple[tuple[str, float], ...],
        consistency_resolution: AnonymousConsistencyResolution,
    ) -> A01CausalCreditResolution:
        row = A01CausalCreditResolution(
            status=status,
            boundary_event_id=boundary.event_id,
            external_event_id=external.event_id,
            prior_relation=prior,
            path_ids=path_ids,
            path_reliability_before=before,
            path_reliability_after=after,
            consistency_resolution=consistency_resolution,
        )
        self.resolutions.append(row)
        return row

    def state_dict(self) -> dict[str, Any]:
        value = {
            "resolutions": [row.state_dict() for row in self.resolutions],
        }
        validate_runtime_mapping(value, path="v061_a01.credit_bridge")
        return value
