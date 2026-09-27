from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

BUILD_ID = "BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT"
SCHEMA_VERSION = 2
CLAIM_BOUNDARY = (
    "NON_EVIDENTIARY_BUILD: ordinary bounded online two-centroid routing plus "
    "route-local evidence revision. This build carries zero scientific credit and does "
    "not establish general scope learning, comparative support, composition contribution, "
    "capability improvement, or scientific novelty."
)
COMPONENT_PROVENANCE = {
    "causal_online_router": {
        "source": "forge_prototypes/causal_online_scope_router.py",
        "prototype_head": "f980c13d984460f158a95e8181239db8d19c8468",
        "handoff_head": "164ce39b99fbfa7146e439215c804c638305dea3",
        "reuse": "selective reimplementation as bounded noncanonical engineering input",
        "scientific_credit": 0,
    },
    "route_local_revision": {
        "source": (
            "Forge hypothesis_revision_overlay.py, stable_scope_hypothesis_revision.py, "
            "and managed_scope_hypothesis_revision.py"
        ),
        "reuse": "selective reimplementation of ordinary scoped evidence accumulation",
        "scientific_credit": 0,
    },
    "integration_design": {
        "source": "ID-SB-LATENT-SCOPE-PLURAL-REVISION-001 / Theory R11",
        "reuse": "non-evidentiary design input only",
        "scientific_credit": 0,
    },
}


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _finite(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    resolved = float(value)
    if not math.isfinite(resolved):
        raise ValueError(f"{name} must be a finite number")
    return resolved


def _strict_dict(value: object, expected: set[str], *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{name} has unexpected fields")
    return value


@dataclass(frozen=True, slots=True)
class ScopeRevisionConfig:
    birth_distance: float = 0.25
    maximum_assignment_distance: float = 0.25
    minimum_distance_margin: float = 0.05
    max_components: int = 2
    candidates: tuple[str, ...] = ("alpha", "beta")
    evidence_gain: float = 1.0
    minimum_confidence: float = 0.60
    minimum_hypothesis_margin: float = 0.20
    maximum_absolute_support: float = 4.0
    maximum_dimensions: int = 8

    def validate(self) -> None:
        if _finite(self.birth_distance, name="birth_distance") <= 0:
            raise ValueError("birth_distance must be positive")
        if (
            _finite(
                self.maximum_assignment_distance,
                name="maximum_assignment_distance",
            )
            <= 0
        ):
            raise ValueError("maximum_assignment_distance must be positive")
        if (
            _finite(
                self.minimum_distance_margin,
                name="minimum_distance_margin",
            )
            < 0
        ):
            raise ValueError("minimum_distance_margin must be non-negative")
        if self.max_components != 2:
            raise ValueError("BUILD-SB-002 requires exactly two components")
        if (
            not isinstance(self.candidates, tuple)
            or len(self.candidates) < 2
            or len(self.candidates) != len(set(self.candidates))
            or any(not isinstance(row, str) or not row.strip() for row in self.candidates)
        ):
            raise ValueError("candidates must contain at least two unique non-empty strings")
        if _finite(self.evidence_gain, name="evidence_gain") <= 0:
            raise ValueError("evidence_gain must be positive")
        for name in ("minimum_confidence", "minimum_hypothesis_margin"):
            value = _finite(getattr(self, name), name=name)
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be in [0, 1]")
        if (
            _finite(
                self.maximum_absolute_support,
                name="maximum_absolute_support",
            )
            <= 0
        ):
            raise ValueError("maximum_absolute_support must be positive")
        if (
            isinstance(self.maximum_dimensions, bool)
            or not isinstance(self.maximum_dimensions, int)
            or not 1 <= self.maximum_dimensions <= 8
        ):
            raise ValueError("maximum_dimensions must be an integer in [1, 8]")

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        result = asdict(self)
        result["candidates"] = list(self.candidates)
        return result

    @classmethod
    def from_dict(cls, value: object) -> ScopeRevisionConfig:
        expected = set(cls.__dataclass_fields__)
        row = _strict_dict(value, expected, name="scope revision config")
        candidates = row["candidates"]
        if not isinstance(candidates, list):
            raise ValueError("config candidates must be a list")
        result = cls(**{**row, "candidates": tuple(candidates)})
        result.validate()
        return result


@dataclass(frozen=True, slots=True)
class CandidateEvidence:
    candidate: str
    evidence_id: str
    strength: float = 1.0


@dataclass(frozen=True, slots=True)
class OnlineScope:
    token: str
    centroid: tuple[float, ...]
    count: int

    def as_dict(self) -> dict[str, Any]:
        return {"centroid": list(self.centroid), "count": self.count, "token": self.token}


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    token: str | None
    action: str
    abstained: bool
    reason: str
    nearest_distance: float | None
    distance_margin: float | None


class CausalScopeRouter:
    """Current-observation-only bounded two-centroid router.

    Tokens are opaque. Their literal names are stable for exact checkpoint replay,
    but callers must not compare token names across different arrival orders.
    """

    def __init__(self, config: ScopeRevisionConfig | None = None) -> None:
        self.config = config or ScopeRevisionConfig()
        self.config.validate()
        self._components: list[OnlineScope] = []

    @staticmethod
    def _vector(observation: Sequence[float], *, maximum_dimensions: int) -> tuple[float, ...]:
        if isinstance(observation, (str, bytes)):
            raise TypeError("observation must be a non-empty numeric vector")
        vector = tuple(_finite(value, name="observation scalar") for value in observation)
        if not vector:
            raise ValueError("observation must be non-empty")
        if len(vector) > maximum_dimensions:
            raise ValueError("observation exceeds maximum_dimensions")
        return vector

    @staticmethod
    def _distance(left: Sequence[float], right: Sequence[float]) -> float:
        if len(left) != len(right):
            raise ValueError("observation dimension changed")
        return math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(left, right, strict=True)))

    def _resolve_vector(self, observation: Sequence[float]) -> tuple[float, ...]:
        vector = self._vector(observation, maximum_dimensions=self.config.maximum_dimensions)
        if self._components and len(vector) != len(self._components[0].centroid):
            raise ValueError("observation dimension changed")
        return vector

    def _create(self, vector: tuple[float, ...], *, action: str) -> RoutingDecision:
        component = OnlineScope(
            token=f"scope-{len(self._components) + 1:08d}",
            centroid=vector,
            count=1,
        )
        self._components.append(component)
        return RoutingDecision(component.token, action, False, action, 0.0, None)

    def _rank(
        self,
        vector: Sequence[float],
    ) -> tuple[tuple[int, float], tuple[int, float] | None]:
        ranked = sorted(
            (
                (index, self._distance(vector, component.centroid))
                for index, component in enumerate(self._components)
            ),
            key=lambda row: (row[1], row[0]),
        )
        return ranked[0], None if len(ranked) == 1 else ranked[1]

    def observe(self, observation: Sequence[float]) -> RoutingDecision:
        vector = self._resolve_vector(observation)
        if not self._components:
            return self._create(vector, action="created_initial_component")

        best, second = self._rank(vector)
        best_index, best_distance = best
        if len(self._components) < self.config.max_components:
            if best_distance >= self.config.birth_distance:
                return self._create(vector, action="created_second_component")
        else:
            if best_distance > self.config.maximum_assignment_distance:
                return RoutingDecision(
                    None,
                    "abstained",
                    True,
                    "component_capacity_exhausted_out_of_support",
                    best_distance,
                    None if second is None else second[1] - best_distance,
                )
            if second is not None:
                margin = second[1] - best_distance
                if margin < self.config.minimum_distance_margin:
                    return RoutingDecision(
                        None,
                        "abstained",
                        True,
                        "ambiguous_nearest_components",
                        best_distance,
                        margin,
                    )

        component = self._components[best_index]
        count = component.count + 1
        centroid = tuple(
            old + (new - old) / count for old, new in zip(component.centroid, vector, strict=True)
        )
        self._components[best_index] = OnlineScope(component.token, centroid, count)
        return RoutingDecision(
            component.token,
            "updated_existing_component",
            False,
            "selected_nearest_component",
            best_distance,
            None if second is None else second[1] - best_distance,
        )

    def route(self, observation: Sequence[float]) -> RoutingDecision:
        vector = self._resolve_vector(observation)
        if not self._components:
            return RoutingDecision(None, "abstained", True, "no_components", None, None)
        best, second = self._rank(vector)
        best_index, best_distance = best
        if best_distance > self.config.maximum_assignment_distance:
            return RoutingDecision(
                None,
                "abstained",
                True,
                "observation_outside_component_support",
                best_distance,
                None if second is None else second[1] - best_distance,
            )
        margin = None if second is None else second[1] - best_distance
        if margin is not None and margin < self.config.minimum_distance_margin:
            return RoutingDecision(
                None,
                "abstained",
                True,
                "ambiguous_nearest_components",
                best_distance,
                margin,
            )
        return RoutingDecision(
            self._components[best_index].token,
            "selected_existing",
            False,
            "selected_nearest_component",
            best_distance,
            margin,
        )

    @property
    def components(self) -> tuple[OnlineScope, ...]:
        return tuple(self._components)

    def state_dict(self) -> dict[str, Any]:
        return {
            "components": [row.as_dict() for row in self._components],
            "config": self.config.as_dict(),
        }

    @classmethod
    def from_state_dict(cls, value: object) -> CausalScopeRouter:
        state = _strict_dict(value, {"components", "config"}, name="router state")
        router = cls(ScopeRevisionConfig.from_dict(state["config"]))
        rows = state["components"]
        if not isinstance(rows, list) or len(rows) > router.config.max_components:
            raise ValueError("invalid persisted component collection")
        for index, raw in enumerate(rows, start=1):
            row = _strict_dict(raw, {"centroid", "count", "token"}, name="component")
            centroid = router._vector(
                row["centroid"],
                maximum_dimensions=router.config.maximum_dimensions,
            )
            count = row["count"]
            token = row["token"]
            if (
                isinstance(count, bool)
                or not isinstance(count, int)
                or count < 1
                or token != f"scope-{index:08d}"
            ):
                raise ValueError("invalid persisted component identity or count")
            if router._components and len(centroid) != len(router._components[0].centroid):
                raise ValueError("persisted component dimension changed")
            router._components.append(OnlineScope(token, centroid, count))
        return router


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    sequence: int
    evidence_id: str
    observation_digest: str
    candidate: str
    strength: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EvidenceIdentityRecord:
    route_token: str
    observation_digest: str
    candidate: str
    strength: float
    sequence: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HypothesisView:
    candidate: str
    cumulative_support: float
    probability: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RevisionView:
    hypotheses: tuple[HypothesisView, ...]
    selected_candidate: str | None
    confidence: float
    margin: float
    abstained: bool
    reason: str
    evidence_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "abstained": self.abstained,
            "confidence": self.confidence,
            "evidence_count": self.evidence_count,
            "hypotheses": [row.as_dict() for row in self.hypotheses],
            "margin": self.margin,
            "reason": self.reason,
            "selected_candidate": self.selected_candidate,
        }


class _RevisionRejected(ValueError):
    pass


@dataclass(slots=True)
class RouteLocalState:
    supports: dict[str, float]
    evidence: list[EvidenceRecord]

    @classmethod
    def empty(cls, candidates: tuple[str, ...]) -> RouteLocalState:
        return cls({candidate: 0.0 for candidate in candidates}, [])

    def as_dict(self) -> dict[str, Any]:
        return {
            "evidence": [row.as_dict() for row in self.evidence],
            "supports": dict(sorted(self.supports.items())),
        }


@dataclass(frozen=True, slots=True)
class ScopeRevisionStep:
    committed: bool
    abstained: bool
    reason: str
    token: str | None
    routing: RoutingDecision
    revision: RevisionView | None
    sequence: int


@dataclass(frozen=True, slots=True)
class ScopeRevisionQuery:
    routing: RoutingDecision
    revision: RevisionView | None


class CausalScopeRevisionPilot:
    """Transactional current-observation routing and route-local revision loop."""

    def __init__(self, config: ScopeRevisionConfig | None = None) -> None:
        self.config = config or ScopeRevisionConfig()
        self.config.validate()
        self._router = CausalScopeRouter(self.config)
        self._routes: dict[str, RouteLocalState] = {}
        self._observation_bindings: dict[str, str] = {}
        self._evidence_bindings: dict[str, EvidenceIdentityRecord] = {}
        self._sequence = 0

    @staticmethod
    def _evidence_id(value: object) -> str:
        if not isinstance(value, str) or re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", value) is None:
            raise _RevisionRejected(
                "evidence_id must contain 1..128 ASCII letters, digits, dot, "
                "underscore, colon or hyphen"
            )
        return value

    def _resolved_evidence(self, evidence: CandidateEvidence) -> tuple[str, str, float]:
        evidence_id = self._evidence_id(evidence.evidence_id)
        if evidence.candidate not in self.config.candidates:
            raise _RevisionRejected("candidate is absent from the exposed hypothesis set")
        try:
            strength = _finite(evidence.strength, name="evidence strength")
        except ValueError as exc:
            raise _RevisionRejected(str(exc)) from exc
        if not -1 <= strength <= 1:
            raise _RevisionRejected("evidence strength must be in [-1, 1]")
        return evidence_id, evidence.candidate, strength

    def _revision_view(self, state: RouteLocalState) -> RevisionView:
        logits = [
            self.config.evidence_gain
            * max(
                -self.config.maximum_absolute_support,
                min(self.config.maximum_absolute_support, state.supports[candidate]),
            )
            for candidate in self.config.candidates
        ]
        maximum = max(logits)
        weights = [math.exp(value - maximum) for value in logits]
        normalizer = math.fsum(weights)
        hypotheses = tuple(
            sorted(
                (
                    HypothesisView(candidate, state.supports[candidate], weight / normalizer)
                    for candidate, weight in zip(
                        self.config.candidates,
                        weights,
                        strict=True,
                    )
                ),
                key=lambda row: (-row.probability, row.candidate),
            )
        )
        confidence = hypotheses[0].probability
        second = hypotheses[1].probability if len(hypotheses) > 1 else 0.0
        margin = confidence - second
        ambiguous = confidence < self.config.minimum_confidence or (
            len(hypotheses) > 1 and margin < self.config.minimum_hypothesis_margin
        )
        return RevisionView(
            hypotheses,
            None if ambiguous else hypotheses[0].candidate,
            confidence,
            margin,
            ambiguous,
            "ambiguous_after_revision" if ambiguous else "selected_after_revision",
            len(state.evidence),
        )

    def _apply_revision(
        self,
        *,
        token: str,
        evidence: CandidateEvidence,
        observation_digest: str,
        sequence: int,
    ) -> RevisionView:
        evidence_id, candidate, strength = self._resolved_evidence(evidence)
        state = self._routes.setdefault(token, RouteLocalState.empty(self.config.candidates))
        state.supports[candidate] += strength
        state.evidence.append(
            EvidenceRecord(sequence, evidence_id, observation_digest, candidate, strength)
        )
        return self._revision_view(state)

    @staticmethod
    def _observation_digest(vector: tuple[float, ...]) -> str:
        return _digest({"features": list(vector)})

    def step(
        self,
        observation: Sequence[float],
        evidence: CandidateEvidence,
    ) -> ScopeRevisionStep:
        """Atomically route and revise from one current observation.

        Any downstream revision rejection restores router, hypothesis, evidence,
        binding, and checkpoint-visible sequence state to the exact pre-step value.
        """

        before = self._checkpoint_payload()
        vector = CausalScopeRouter._vector(
            observation,
            maximum_dimensions=self.config.maximum_dimensions,
        )
        observation_digest = self._observation_digest(vector)
        try:
            evidence_id, candidate, strength = self._resolved_evidence(evidence)
        except _RevisionRejected:
            return ScopeRevisionStep(
                False,
                True,
                "invalid_downstream_revision",
                None,
                self._router.route(vector),
                None,
                self._sequence,
            )

        prior_evidence = self._evidence_bindings.get(evidence_id)
        if prior_evidence is not None:
            routing = self._router.route(vector)
            identical = (
                prior_evidence.observation_digest == observation_digest
                and prior_evidence.candidate == candidate
                and prior_evidence.strength == strength
                and routing.token == prior_evidence.route_token
            )
            if identical:
                revision = self._revision_view(self._routes[prior_evidence.route_token])
                return ScopeRevisionStep(
                    False,
                    False,
                    "duplicate_evidence_id",
                    prior_evidence.route_token,
                    routing,
                    revision,
                    self._sequence,
                )
            return ScopeRevisionStep(
                False,
                True,
                "evidence_identity_conflict",
                None,
                routing,
                None,
                self._sequence,
            )

        prior_candidate = self._observation_bindings.get(observation_digest)
        if prior_candidate is not None and prior_candidate != candidate:
            routing = self._router.route(vector)
            return ScopeRevisionStep(
                False,
                True,
                "identical_observation_conflict",
                None,
                routing,
                None,
                self._sequence,
            )

        routing = self._router.observe(vector)
        if routing.abstained or routing.token is None:
            if self._checkpoint_payload() != before:
                self._restore_payload(before)
                raise RuntimeError("router abstention violated the no-write invariant")
            return ScopeRevisionStep(
                False,
                True,
                routing.reason,
                None,
                routing,
                None,
                self._sequence,
            )

        next_sequence = self._sequence + 1
        try:
            revision = self._apply_revision(
                token=routing.token,
                evidence=evidence,
                observation_digest=observation_digest,
                sequence=next_sequence,
            )
        except _RevisionRejected:
            self._restore_payload(before)
            return ScopeRevisionStep(
                False,
                True,
                "invalid_downstream_revision",
                None,
                RoutingDecision(
                    None,
                    "abstained",
                    True,
                    "invalid_downstream_revision",
                    routing.nearest_distance,
                    routing.distance_margin,
                ),
                None,
                self._sequence,
            )

        self._observation_bindings.setdefault(observation_digest, candidate)
        self._evidence_bindings[evidence_id] = EvidenceIdentityRecord(
            routing.token,
            observation_digest,
            candidate,
            strength,
            next_sequence,
        )
        self._sequence = next_sequence
        return ScopeRevisionStep(
            True,
            False,
            "committed_route_local_revision",
            routing.token,
            routing,
            revision,
            self._sequence,
        )

    def query(self, observation: Sequence[float]) -> ScopeRevisionQuery:
        """Return a pure route and route-local hypothesis view."""

        before = self.state_hash()
        routing = self._router.route(observation)
        revision = (
            None if routing.token is None else self._revision_view(self._routes[routing.token])
        )
        if self.state_hash() != before:
            raise RuntimeError("query mutated BUILD-SB-002 state")
        return ScopeRevisionQuery(routing, revision)

    def inspect(self) -> dict[str, Any]:
        return json.loads(
            _canonical(
                {
                    "build_id": BUILD_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "component_provenance": COMPONENT_PROVENANCE,
                    "config": self.config.as_dict(),
                    "evidentiary_status": "NON_EVIDENTIARY_BUILD",
                    "evidence_bindings": {
                        evidence_id: binding.as_dict()
                        for evidence_id, binding in sorted(self._evidence_bindings.items())
                    },
                    "observation_bindings": dict(sorted(self._observation_bindings.items())),
                    "router": self._router.state_dict(),
                    "routes": {
                        token: state.as_dict() for token, state in sorted(self._routes.items())
                    },
                    "scientific_credit": 0,
                    "sequence": self._sequence,
                }
            )
        )

    def state_hash(self) -> str:
        return _digest(self.inspect())

    def _checkpoint_payload(self) -> dict[str, Any]:
        return {
            "build_id": BUILD_ID,
            "config": self.config.as_dict(),
            "evidence_bindings": {
                evidence_id: binding.as_dict()
                for evidence_id, binding in sorted(self._evidence_bindings.items())
            },
            "observation_bindings": dict(sorted(self._observation_bindings.items())),
            "router": self._router.state_dict(),
            "routes": {token: state.as_dict() for token, state in sorted(self._routes.items())},
            "schema_version": SCHEMA_VERSION,
            "sequence": self._sequence,
        }

    def _restore_payload(self, value: object) -> None:
        restored = self._from_checkpoint_payload(value)
        self.config = restored.config
        self._router = restored._router
        self._routes = restored._routes
        self._observation_bindings = restored._observation_bindings
        self._evidence_bindings = restored._evidence_bindings
        self._sequence = restored._sequence

    @classmethod
    def _from_checkpoint_payload(cls, value: object) -> CausalScopeRevisionPilot:
        expected = {
            "build_id",
            "config",
            "evidence_bindings",
            "observation_bindings",
            "router",
            "routes",
            "schema_version",
            "sequence",
        }
        payload = _strict_dict(value, expected, name="BUILD-SB-002 checkpoint")
        if payload["build_id"] != BUILD_ID or payload["schema_version"] != SCHEMA_VERSION:
            raise ValueError("unsupported BUILD-SB-002 checkpoint identity")
        config = ScopeRevisionConfig.from_dict(payload["config"])
        pilot = cls(config)
        router = CausalScopeRouter.from_state_dict(payload["router"])
        if router.config != config:
            raise ValueError("router config does not match checkpoint config")
        pilot._router = router
        sequence = payload["sequence"]
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
            raise ValueError("checkpoint sequence must be a non-negative integer")
        pilot._sequence = sequence

        routes = payload["routes"]
        if not isinstance(routes, dict):
            raise ValueError("checkpoint routes must be an object")
        component_tokens = {row.token for row in router.components}
        if set(routes) != component_tokens:
            raise ValueError("checkpoint route state must exactly match router components")
        total_evidence = 0
        observed_sequences: list[int] = []
        expected_evidence_bindings: dict[str, EvidenceIdentityRecord] = {}
        for token, raw in routes.items():
            row = _strict_dict(raw, {"evidence", "supports"}, name="route-local state")
            supports = row["supports"]
            if not isinstance(supports, dict) or set(supports) != set(config.candidates):
                raise ValueError("route-local support candidates do not match config")
            resolved_supports = {
                candidate: _finite(supports[candidate], name="cumulative support")
                for candidate in config.candidates
            }
            evidence_rows = row["evidence"]
            if not isinstance(evidence_rows, list):
                raise ValueError("route-local evidence must be a list")
            records: list[EvidenceRecord] = []
            calculated = {candidate: 0.0 for candidate in config.candidates}
            for raw_record in evidence_rows:
                record = _strict_dict(
                    raw_record,
                    {"candidate", "evidence_id", "observation_digest", "sequence", "strength"},
                    name="evidence record",
                )
                candidate = record["candidate"]
                evidence_id = record["evidence_id"]
                strength = _finite(record["strength"], name="evidence strength")
                record_sequence = record["sequence"]
                digest = record["observation_digest"]
                if (
                    candidate not in config.candidates
                    or not -1 <= strength <= 1
                    or isinstance(record_sequence, bool)
                    or not isinstance(record_sequence, int)
                    or not 1 <= record_sequence <= sequence
                    or not isinstance(digest, str)
                    or len(digest) != 64
                ):
                    raise ValueError("invalid evidence record")
                try:
                    pilot._evidence_id(evidence_id)
                except _RevisionRejected as exc:
                    raise ValueError("invalid evidence record") from exc
                if evidence_id in expected_evidence_bindings:
                    raise ValueError("checkpoint evidence ids must be unique")
                records.append(
                    EvidenceRecord(record_sequence, evidence_id, digest, candidate, strength)
                )
                expected_evidence_bindings[evidence_id] = EvidenceIdentityRecord(
                    token,
                    digest,
                    candidate,
                    strength,
                    record_sequence,
                )
                observed_sequences.append(record_sequence)
                calculated[candidate] += strength
            if calculated != resolved_supports:
                raise ValueError("route-local support does not match evidence ledger")
            pilot._routes[token] = RouteLocalState(resolved_supports, records)
            total_evidence += len(records)
        if total_evidence != sequence:
            raise ValueError("checkpoint sequence does not match committed evidence count")
        if sorted(observed_sequences) != list(range(1, sequence + 1)):
            raise ValueError(
                "checkpoint evidence sequence must be the unique permutation 1..sequence"
            )

        evidence_bindings = payload["evidence_bindings"]
        if not isinstance(evidence_bindings, dict):
            raise ValueError("evidence_bindings must be an object")
        resolved_evidence_bindings: dict[str, EvidenceIdentityRecord] = {}
        for evidence_id, raw_binding in evidence_bindings.items():
            try:
                pilot._evidence_id(evidence_id)
            except _RevisionRejected as exc:
                raise ValueError("invalid evidence binding identity") from exc
            binding = _strict_dict(
                raw_binding,
                {"candidate", "observation_digest", "route_token", "sequence", "strength"},
                name="evidence binding",
            )
            route_token = binding["route_token"]
            observation_digest = binding["observation_digest"]
            candidate = binding["candidate"]
            strength = _finite(binding["strength"], name="evidence binding strength")
            binding_sequence = binding["sequence"]
            if (
                not isinstance(route_token, str)
                or route_token not in component_tokens
                or not isinstance(observation_digest, str)
                or len(observation_digest) != 64
                or not isinstance(candidate, str)
                or candidate not in config.candidates
                or not -1 <= strength <= 1
                or isinstance(binding_sequence, bool)
                or not isinstance(binding_sequence, int)
                or not 1 <= binding_sequence <= sequence
            ):
                raise ValueError("invalid evidence binding")
            resolved_evidence_bindings[evidence_id] = EvidenceIdentityRecord(
                route_token,
                observation_digest,
                candidate,
                strength,
                binding_sequence,
            )
        if resolved_evidence_bindings != expected_evidence_bindings:
            raise ValueError("evidence bindings do not match committed evidence ledger")
        pilot._evidence_bindings = resolved_evidence_bindings

        bindings = payload["observation_bindings"]
        if not isinstance(bindings, dict):
            raise ValueError("observation_bindings must be an object")
        for digest, candidate in bindings.items():
            if (
                not isinstance(digest, str)
                or len(digest) != 64
                or candidate not in config.candidates
            ):
                raise ValueError("invalid observation binding")
        evidence_bindings = {
            record.observation_digest: record.candidate
            for state in pilot._routes.values()
            for record in state.evidence
        }
        if bindings != evidence_bindings:
            raise ValueError("observation bindings do not match committed evidence")
        pilot._observation_bindings = dict(bindings)
        return pilot


class ScopeRevisionCheckpointManager:
    FILE_NAME = "sb002-state.json"

    @staticmethod
    def save(pilot: CausalScopeRevisionPilot, directory: str | Path) -> str:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        path = root / ScopeRevisionCheckpointManager.FILE_NAME
        payload = pilot._checkpoint_payload()
        envelope = {
            "payload": payload,
            "payload_sha256": _digest(payload),
            "state_hash": pilot.state_hash(),
        }
        raw = (_canonical(envelope) + "\n").encode("utf-8")
        with path.open("xb") as handle:
            handle.write(raw)
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def load(directory: str | Path) -> CausalScopeRevisionPilot:
        path = Path(directory) / ScopeRevisionCheckpointManager.FILE_NAME
        envelope = _strict_dict(
            json.loads(path.read_text(encoding="utf-8")),
            {"payload", "payload_sha256", "state_hash"},
            name="checkpoint envelope",
        )
        if envelope["payload_sha256"] != _digest(envelope["payload"]):
            raise ValueError("checkpoint payload digest mismatch")
        pilot = CausalScopeRevisionPilot._from_checkpoint_payload(envelope["payload"])
        if pilot.state_hash() != envelope["state_hash"]:
            raise ValueError("restored BUILD-SB-002 state hash mismatch")
        return pilot


__all__ = [
    "BUILD_ID",
    "CLAIM_BOUNDARY",
    "COMPONENT_PROVENANCE",
    "CandidateEvidence",
    "CausalScopeRevisionPilot",
    "CausalScopeRouter",
    "EvidenceRecord",
    "EvidenceIdentityRecord",
    "HypothesisView",
    "OnlineScope",
    "RevisionView",
    "RoutingDecision",
    "ScopeRevisionCheckpointManager",
    "ScopeRevisionConfig",
    "ScopeRevisionQuery",
    "ScopeRevisionStep",
]
