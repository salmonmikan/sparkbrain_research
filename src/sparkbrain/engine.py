from __future__ import annotations

import heapq
import math
import random
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, replace

from .model import (
    BrainConfig,
    Coalition,
    Connection,
    EngineStats,
    Event,
    EventKind,
    EvidenceRecord,
    Ignition,
    Spark,
    SparkKind,
    TraceFrame,
    WorkspaceItem,
)
from .validation import (
    SCHEMA_VERSION,
    validate_config,
    validate_graph,
    validate_spark,
    validate_state_payload,
)


def _jsonable_tuple(value):
    if isinstance(value, tuple):
        return [_jsonable_tuple(item) for item in value]
    if isinstance(value, list):
        return [_jsonable_tuple(item) for item in value]
    return value


def _restore_tuple(value):
    if isinstance(value, list):
        return tuple(_restore_tuple(item) for item in value)
    return value


class SparkBrain:
    """Event-driven reference implementation of Spark-based cognitive dynamics.

    This engine is intentionally inspectable.  It favours explicit state and
    deterministic traces over raw speed.  Neural/spiking backends are separate
    research milestones so that failures can be attributed to the theory rather
    than to difficult training or hardware details.
    """

    def __init__(self, config: BrainConfig | None = None) -> None:
        self.config = config or BrainConfig()
        validate_config(self.config)
        self.random = random.Random(self.config.random_seed)

        self.time: float = 0.0
        self.sparks: dict[str, Spark] = {}
        self.edges_out: dict[str, list[Connection]] = defaultdict(list)
        self.connections: list[Connection] = []
        self.broadcast_listeners: set[str] = set()

        self._queue: list[Event] = []
        self._sequence: int = 0
        self._active_hypotheses: set[str] = set()
        self._stability: dict[str, int] = defaultdict(int)
        self._last_top_hypothesis: str | None = None
        self._last_ignition_time: float = -math.inf
        self._last_ignition_hypothesis: str | None = None

        self.workspace: list[WorkspaceItem] = []
        self.ignitions: list[Ignition] = []
        self.last_coalitions: list[Coalition] = []
        self.belief_label: str | None = None

        self.stats = EngineStats()
        self.trace: list[TraceFrame] = []
        self._fired_since_frame: list[str] = []
        self._active_edges_since_frame: list[tuple[str, str, float]] = []
        self._updated_since_frame: set[str] = set()

    def reset(
        self,
        *,
        seed: int | None = None,
        config: BrainConfig | None = None,
    ) -> None:
        """Reset runtime state while preserving the constructed graph.

        Connection weights remain in place so a learned backend can reset an
        episode without discarding learned parameters.  Episode-local
        eligibility, evidence, activity, queue state, and traces are cleared.
        """

        if config is not None:
            self.config = config
        if seed is not None:
            self.config = replace(self.config, random_seed=seed)
        validate_config(self.config)
        self.random = random.Random(self.config.random_seed)
        self.time = 0.0
        self._queue = []
        self._sequence = 0
        self._active_hypotheses = set()
        self._stability = defaultdict(int)
        self._last_top_hypothesis = None
        self._last_ignition_time = -math.inf
        self._last_ignition_hypothesis = None
        self.workspace = []
        self.ignitions = []
        self.last_coalitions = []
        self.belief_label = None
        self.stats = EngineStats()
        self.trace = []
        self._fired_since_frame = []
        self._active_edges_since_frame = []
        self._updated_since_frame = set()

        for spark in self.sparks.values():
            spark.activation = 0.0
            spark.threshold = spark.base_threshold
            spark.last_update = 0.0
            spark.refractory_until = 0.0
            spark.last_fire = None
            spark.fired_count = 0
            spark.supports.clear()
            spark.contradictions.clear()
        for edge in self.connections:
            edge.eligibility = 0.0

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------
    def add_spark(self, spark: Spark) -> None:
        validate_spark(spark)
        if spark.id in self.sparks:
            raise ValueError(f"Duplicate Spark id: {spark.id}")
        if spark.base_threshold <= 0:
            spark.base_threshold = spark.threshold
        self.sparks[spark.id] = spark

    def connect(
        self,
        source: str,
        target: str,
        weight: float,
        *,
        delay: float | None = None,
        plastic: bool = False,
        label: str = "",
    ) -> Connection:
        if source not in self.sparks or target not in self.sparks:
            raise KeyError(f"Unknown Spark in connection: {source!r} -> {target!r}")
        resolved_delay = self.config.propagation_delay if delay is None else delay
        if not math.isfinite(weight):
            raise ValueError("Connection weight must be finite")
        if not math.isfinite(resolved_delay) or resolved_delay < 0:
            raise ValueError("Connection delay must be finite and >= 0")
        edge = Connection(
            source=source,
            target=target,
            weight=weight,
            delay=resolved_delay,
            plastic=plastic,
            label=label,
        )
        self.edges_out[source].append(edge)
        self.connections.append(edge)
        return edge

    def add_soft_competition(self, spark_ids: Iterable[str], weight: float = -0.18) -> None:
        ids = list(spark_ids)
        for source in ids:
            for target in ids:
                if source != target:
                    self.connect(source, target, weight, label="lateral_inhibition")

    def register_broadcast_listener(self, spark_id: str) -> None:
        if spark_id not in self.sparks:
            raise KeyError(f"Unknown broadcast listener: {spark_id}")
        self.broadcast_listeners.add(spark_id)

    # ------------------------------------------------------------------
    # Event scheduling and execution
    # ------------------------------------------------------------------
    def schedule(
        self,
        *,
        time: float,
        kind: EventKind,
        source: str,
        target: str | None,
        strength: float = 0.0,
        priority: int = 10,
        evidence_id: str | None = None,
        evidence_label: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        if time < self.time - 1e-9:
            raise ValueError(f"Cannot schedule an event in the past: {time} < {self.time}")
        if not math.isfinite(time) or not math.isfinite(strength):
            raise ValueError("Event time and strength must be finite")
        if isinstance(priority, bool) or not isinstance(priority, int):
            raise ValueError(f"Event priority must be an integer, got {priority!r}")
        sequence = self._sequence
        self._sequence += 1
        event = Event(
            time=time,
            priority=priority,
            sequence=sequence,
            kind=kind,
            source=source,
            target=target,
            strength=strength,
            evidence_id=evidence_id,
            evidence_label=evidence_label,
            metadata=dict(metadata or {}),
        )
        heapq.heappush(self._queue, event)

    def inject_stimulus(
        self,
        *,
        target: str,
        label: str,
        time: float,
        strength: float = 1.0,
        source: str = "world",
        evidence_id: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        evidence_id = evidence_id or f"{source}:{label}:{time:.6f}"
        merged = {"origin_kind": "external", **(metadata or {})}
        self.schedule(
            time=time,
            kind=EventKind.STIMULUS,
            source=source,
            target=target,
            strength=strength,
            priority=0,
            evidence_id=evidence_id,
            evidence_label=label,
            metadata=merged,
        )

    def inject_reward(self, *, reward: float, time: float, source: str = "world") -> None:
        self.schedule(
            time=time,
            kind=EventKind.REWARD,
            source=source,
            target=None,
            strength=reward,
            priority=50,
        )

    def run(self, *, max_events: int = 100_000) -> None:
        processed = 0
        while self._queue:
            if processed >= max_events:
                preview = [
                    {
                        "time": event.time,
                        "kind": event.kind.value,
                        "source": event.source,
                        "target": event.target,
                    }
                    for event in sorted(self._queue)[:5]
                ]
                raise RuntimeError(
                    "Event limit exceeded; possible recurrent event loop; "
                    f"remaining={len(self._queue)} next={preview}"
                )
            event = heapq.heappop(self._queue)
            self.time = event.time
            self._decay_eligibilities()
            self._process_event(event)
            processed += 1

    def _process_event(self, event: Event) -> None:
        self.stats.events_processed += 1
        if event.kind is EventKind.REWARD:
            self._apply_reward(event.strength)
            return
        if event.target is None:
            return
        if event.target not in self.sparks:
            raise KeyError(f"Unknown event target: {event.target}")

        spark = self.sparks[event.target]
        self._touch(spark, event.time)
        spark.activation += event.strength

        if spark.kind is SparkKind.HYPOTHESIS:
            self._active_hypotheses.add(spark.id)
            self._record_evidence(spark, event)

        fired = False
        if spark.activation >= spark.threshold and event.time >= spark.refractory_until:
            fired = self._fire(spark, event)

        # Coalition state is recomputed after every hypothesis-affecting event.
        # This allows weak, asynchronous events to accumulate and compete.
        if spark.kind is SparkKind.HYPOTHESIS or fired:
            self._evaluate_coalitions(event.time)

    def _touch(self, spark: Spark, now: float) -> None:
        dt = max(0.0, now - spark.last_update)
        if dt > 0:
            if spark.decay_tau > 0:
                spark.activation *= math.exp(-dt / spark.decay_tau)
            if self.config.threshold_relaxation_tau > 0:
                relax = math.exp(-dt / self.config.threshold_relaxation_tau)
                spark.threshold = spark.base_threshold + (
                    spark.threshold - spark.base_threshold
                ) * relax
        spark.last_update = now
        self.stats.spark_updates += 1
        self._updated_since_frame.add(spark.id)

    def _record_evidence(self, spark: Spark, event: Event) -> None:
        if not event.evidence_id or event.metadata.get("origin_kind") != "external":
            return
        record = EvidenceRecord(
            evidence_id=event.evidence_id,
            source=str(event.metadata.get("sensor", event.evidence_label or event.source)),
            label=event.evidence_label or event.evidence_id,
            time=event.time,
            strength=event.strength,
        )
        if event.strength >= 0:
            spark.supports[event.evidence_id] = record
            spark.contradictions.pop(event.evidence_id, None)
        else:
            spark.contradictions[event.evidence_id] = record
            spark.supports.pop(event.evidence_id, None)

    def _fire(self, spark: Spark, event: Event) -> bool:
        pre_activation = spark.activation
        spark.last_fire = event.time
        spark.fired_count += 1
        spark.refractory_until = event.time + self.config.refractory_period
        spark.threshold += self.config.homeostatic_increment
        self.stats.fires += 1
        self._fired_since_frame.append(spark.id)

        residual = float(spark.metadata.get("post_fire_residual", self.config.post_fire_residual))
        if spark.kind in {SparkKind.HYPOTHESIS, SparkKind.MEMORY, SparkKind.GOAL}:
            residual = float(spark.metadata.get("post_fire_residual", max(residual, 0.82)))
        spark.activation = pre_activation * residual

        for edge in self.edges_out.get(spark.id, []):
            self.stats.edge_evaluations += 1
            edge.eligibility += max(0.0, min(1.0, pre_activation / max(spark.threshold, 1e-6)))
            kind = EventKind.PROPAGATION if edge.weight >= 0 else EventKind.INHIBITION
            metadata = dict(event.metadata)
            # External evidence identity survives only sensory -> downstream
            # propagation.  Competition between hypotheses is an internal
            # dynamic and must not be mistaken for new external evidence.
            propagated_evidence_id = event.evidence_id
            propagated_evidence_label = event.evidence_label
            if spark.kind is not SparkKind.SENSORY:
                metadata["origin_kind"] = "internal"
                propagated_evidence_id = None
                propagated_evidence_label = None
            self.schedule(
                time=event.time + edge.delay,
                kind=kind,
                source=spark.id,
                target=edge.target,
                strength=edge.weight,
                priority=20 if edge.weight >= 0 else 15,
                evidence_id=propagated_evidence_id,
                evidence_label=propagated_evidence_label,
                metadata=metadata,
            )
            self._active_edges_since_frame.append((edge.source, edge.target, edge.weight))
        return True

    # ------------------------------------------------------------------
    # Coalition and workspace dynamics
    # ------------------------------------------------------------------
    def _evaluate_coalitions(self, now: float) -> None:
        coalitions: list[Coalition] = []
        expired: list[str] = []

        for spark_id in sorted(self._active_hypotheses):
            spark = self.sparks[spark_id]
            self._touch(spark, now)
            if abs(spark.activation) < self.config.active_epsilon and not spark.supports:
                expired.append(spark_id)
                continue

            positive_records = self._live_records(spark.supports.values(), now)
            negative_records = self._live_records(spark.contradictions.values(), now)
            source_names = {record.source for record, _ in positive_records}
            evidence_strength = sum(
                max(0.0, record.strength) * recency
                for record, recency in positive_records
            )
            contradiction = sum(
                abs(record.strength) * recency
                for record, recency in negative_records
            )

            base_score = (
                max(0.0, spark.activation)
                + 0.08 * evidence_strength
                + self.config.diversity_bonus * max(0, len(source_names) - 1)
                - self.config.contradiction_penalty * contradiction
            )

            coalition = Coalition(
                id=f"coalition:{spark.id}",
                hypothesis_id=spark.id,
                label=spark.label,
                members=tuple(sorted({record.label for record, _ in positive_records})),
                score=base_score,
                activation=spark.activation,
                evidence_strength=evidence_strength,
                diversity=len(source_names),
                stability=0,
                contradiction=contradiction,
            )
            coalitions.append(coalition)

        for spark_id in expired:
            self._active_hypotheses.discard(spark_id)

        if not coalitions:
            self.last_coalitions = []
            return

        coalitions.sort(key=lambda coalition: coalition.score, reverse=True)
        top_id = coalitions[0].hypothesis_id
        if top_id == self._last_top_hypothesis:
            self._stability[top_id] += 1
        else:
            for hypothesis_id in list(self._stability):
                self._stability[hypothesis_id] = max(0, self._stability[hypothesis_id] - 1)
            self._stability[top_id] = 1
            self._last_top_hypothesis = top_id

        enriched: list[Coalition] = []
        for coalition in coalitions:
            stability = self._stability[coalition.hypothesis_id]
            score = coalition.score + self.config.temporal_coherence_bonus * min(stability, 4)
            enriched.append(
                Coalition(
                    id=coalition.id,
                    hypothesis_id=coalition.hypothesis_id,
                    label=coalition.label,
                    members=coalition.members,
                    score=score,
                    activation=coalition.activation,
                    evidence_strength=coalition.evidence_strength,
                    diversity=coalition.diversity,
                    stability=stability,
                    contradiction=coalition.contradiction,
                )
            )
        enriched.sort(key=lambda coalition: coalition.score, reverse=True)
        self.last_coalitions = enriched
        self._maybe_ignite(now, enriched)

    def _live_records(
        self, records: Iterable[EvidenceRecord], now: float
    ) -> list[tuple[EvidenceRecord, float]]:
        live: list[tuple[EvidenceRecord, float]] = []
        for record in records:
            age = max(0.0, now - record.time)
            recency = math.exp(-age / self.config.support_tau)
            if recency >= 0.02:
                live.append((record, recency))
        return live

    def _maybe_ignite(self, now: float, coalitions: list[Coalition]) -> None:
        top = coalitions[0]
        second_score = coalitions[1].score if len(coalitions) > 1 else 0.0
        margin = top.score - second_score
        cooldown_elapsed = now - self._last_ignition_time >= self.config.ignition_cooldown
        changed = top.hypothesis_id != self._last_ignition_hypothesis

        if not (
            top.score >= self.config.ignition_threshold
            and margin >= self.config.ignition_margin
            and top.diversity >= self.config.min_support_sources
            and top.stability >= self.config.stability_evaluations
            and (changed or cooldown_elapsed)
        ):
            return

        ignition = Ignition(
            time=now,
            label=top.label,
            hypothesis_id=top.hypothesis_id,
            coalition_id=top.id,
            score=top.score,
            margin=margin,
            supports=top.members,
        )
        self.ignitions.append(ignition)
        self.stats.ignitions += 1
        self._last_ignition_time = now
        self._last_ignition_hypothesis = top.hypothesis_id
        self.belief_label = top.label

        self.workspace = [
            item for item in self.workspace if item.hypothesis_id != top.hypothesis_id
        ]
        self.workspace.insert(
            0,
            WorkspaceItem(
                coalition_id=top.id,
                hypothesis_id=top.hypothesis_id,
                label=top.label,
                score=top.score,
                ignition_time=now,
                supports=top.members,
            ),
        )
        self.workspace = self.workspace[: self.config.workspace_slots]

        for listener_id in sorted(self.broadcast_listeners):
            self.stats.broadcasts += 1
            self.schedule(
                time=now + self.config.propagation_delay,
                kind=EventKind.BROADCAST,
                source="global_workspace",
                target=listener_id,
                strength=min(1.0, top.score),
                priority=30,
                metadata={
                    "origin_kind": "workspace",
                    "coalition_id": top.id,
                    "belief": top.label,
                },
            )

    # ------------------------------------------------------------------
    # Learning and inspection
    # ------------------------------------------------------------------
    def _decay_eligibilities(self) -> None:
        for edge in self.connections:
            edge.eligibility *= self.config.eligibility_decay

    def _apply_reward(self, reward: float) -> None:
        for edge in self.connections:
            if not edge.plastic or edge.eligibility == 0:
                continue
            edge.weight += self.config.learning_rate * reward * edge.eligibility
            edge.weight = max(
                -self.config.max_abs_weight,
                min(self.config.max_abs_weight, edge.weight),
            )

    @property
    def prediction(self) -> str | None:
        return self.belief_label

    def snapshot(self, *, external_event: str, truth: str | None = None) -> TraceFrame:
        spark_rows: list[dict] = []
        for spark in self.sparks.values():
            # Inspection must not turn dormant Sparks into computational work.
            # Values are projected lazily without mutating engine state or stats.
            dt = max(0.0, self.time - spark.last_update)
            activation = spark.activation
            threshold = spark.threshold
            if dt > 0:
                if spark.decay_tau > 0:
                    activation *= math.exp(-dt / spark.decay_tau)
                if self.config.threshold_relaxation_tau > 0:
                    relax = math.exp(-dt / self.config.threshold_relaxation_tau)
                    threshold = spark.base_threshold + (threshold - spark.base_threshold) * relax
            spark_rows.append(
                {
                    "id": spark.id,
                    "label": spark.label,
                    "kind": spark.kind.value,
                    "organ": spark.organ,
                    "activation": round(activation, 6),
                    "threshold": round(threshold, 6),
                    "fired_count": spark.fired_count,
                    "last_fire": spark.last_fire,
                }
            )

        frame = TraceFrame(
            time=self.time,
            external_event=external_event,
            truth=truth,
            prediction=self.prediction,
            sparks=spark_rows,
            coalitions=[
                {
                    "id": c.id,
                    "hypothesis_id": c.hypothesis_id,
                    "label": c.label,
                    "members": list(c.members),
                    "score": round(c.score, 6),
                    "activation": round(c.activation, 6),
                    "evidence_strength": round(c.evidence_strength, 6),
                    "diversity": c.diversity,
                    "stability": c.stability,
                    "contradiction": round(c.contradiction, 6),
                }
                for c in self.last_coalitions
            ],
            workspace=[asdict(item) for item in self.workspace],
            fired=list(dict.fromkeys(self._fired_since_frame)),
            active_edges=list(self._active_edges_since_frame),
            stats={
                **asdict(self.stats),
                "active_sparks_since_frame": len(self._updated_since_frame),
                "active_spark_fraction": len(self._updated_since_frame) / max(1, len(self.sparks)),
            },
        )
        self.trace.append(frame)
        self._fired_since_frame.clear()
        self._active_edges_since_frame.clear()
        self._updated_since_frame.clear()
        return frame

    def export_graph(self) -> dict:
        return {
            "nodes": [
                {
                    "id": spark.id,
                    "label": spark.label,
                    "kind": spark.kind.value,
                    "organ": spark.organ,
                }
                for spark in self.sparks.values()
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "weight": edge.weight,
                    "plastic": edge.plastic,
                    "label": edge.label,
                }
                for edge in self.connections
            ],
        }

    def state_dict(self, *, include_trace: bool = True) -> dict:
        """Return a JSON-compatible deterministic checkpoint.

        The checkpoint includes the event queue and internal control state, so a
        restored engine can continue the same event stream.  It is a versioned
        research format, not yet a long-term public storage guarantee.
        """

        validate_config(self.config)
        validate_graph(self.sparks.values(), self.connections, self.broadcast_listeners)

        spark_rows: list[dict] = []
        for spark in self.sparks.values():
            row = asdict(spark)
            row["kind"] = spark.kind.value
            spark_rows.append(row)

        event_rows = [
            {
                "time": event.time,
                "priority": event.priority,
                "sequence": event.sequence,
                "kind": event.kind.value,
                "source": event.source,
                "target": event.target,
                "strength": event.strength,
                "evidence_id": event.evidence_id,
                "evidence_label": event.evidence_label,
                "metadata": event.metadata,
            }
            for event in sorted(self._queue)
        ]

        return {
            "schema_version": SCHEMA_VERSION,
            "config": asdict(self.config),
            "time": self.time,
            "sparks": spark_rows,
            "connections": [asdict(edge) for edge in self.connections],
            "broadcast_listeners": sorted(self.broadcast_listeners),
            "queue": event_rows,
            "next_sequence": self._sequence,
            "active_hypotheses": sorted(self._active_hypotheses),
            "stability": dict(self._stability),
            "last_top_hypothesis": self._last_top_hypothesis,
            "last_ignition_time": (
                None if self._last_ignition_time == -math.inf else self._last_ignition_time
            ),
            "last_ignition_hypothesis": self._last_ignition_hypothesis,
            "workspace": [asdict(item) for item in self.workspace],
            "ignitions": [asdict(item) for item in self.ignitions],
            "last_coalitions": [asdict(item) for item in self.last_coalitions],
            "belief_label": self.belief_label,
            "stats": asdict(self.stats),
            "trace": [asdict(frame) for frame in self.trace] if include_trace else [],
            "fired_since_frame": list(self._fired_since_frame),
            "active_edges_since_frame": [list(edge) for edge in self._active_edges_since_frame],
            "updated_since_frame": sorted(self._updated_since_frame),
            "random_state": _jsonable_tuple(self.random.getstate()),
        }

    @classmethod
    def from_state_dict(cls, state: dict) -> SparkBrain:
        validate_state_payload(state)
        config_payload = dict(state["config"])
        brain = cls(BrainConfig(**config_payload))

        spark_payload = state["sparks"]
        for raw in spark_payload:
            row = dict(raw)
            kind = SparkKind(row.pop("kind"))
            row["supports"] = {
                key: EvidenceRecord(**value)
                for key, value in dict(row.get("supports", {})).items()
            }
            row["contradictions"] = {
                key: EvidenceRecord(**value)
                for key, value in dict(row.get("contradictions", {})).items()
            }
            brain.add_spark(Spark(kind=kind, **row))

        connection_payload = state["connections"]
        for raw in connection_payload:
            row = dict(raw)
            eligibility = float(row.pop("eligibility", 0.0))
            edge = brain.connect(**row)
            edge.eligibility = eligibility

        for listener in state["broadcast_listeners"]:
            brain.register_broadcast_listener(str(listener))

        queue_payload = state["queue"]
        brain._queue = []
        for raw in queue_payload:
            row = dict(raw)
            row["kind"] = EventKind(row["kind"])
            heapq.heappush(brain._queue, Event(**row))

        brain._sequence = int(state["next_sequence"])
        if brain._queue:
            brain._sequence = max(
                brain._sequence,
                max(event.sequence for event in brain._queue) + 1,
            )
        brain.time = float(state["time"])
        brain._active_hypotheses = set(state["active_hypotheses"])
        brain._stability = defaultdict(
            int,
            {str(key): int(value) for key, value in dict(state["stability"]).items()},
        )
        brain._last_top_hypothesis = state["last_top_hypothesis"]
        last_ignition_time = state["last_ignition_time"]
        brain._last_ignition_time = (
            -math.inf if last_ignition_time is None else float(last_ignition_time)
        )
        brain._last_ignition_hypothesis = state["last_ignition_hypothesis"]
        brain.workspace = [WorkspaceItem(**row) for row in state["workspace"]]
        brain.ignitions = [Ignition(**row) for row in state["ignitions"]]
        brain.last_coalitions = [Coalition(**row) for row in state["last_coalitions"]]
        brain.belief_label = state["belief_label"]
        brain.stats = EngineStats(**dict(state["stats"]))
        brain.trace = [TraceFrame(**row) for row in state["trace"]]
        brain._fired_since_frame = list(state["fired_since_frame"])
        brain._active_edges_since_frame = [
            (str(row[0]), str(row[1]), float(row[2]))
            for row in state["active_edges_since_frame"]
        ]
        brain._updated_since_frame = set(state["updated_since_frame"])
        brain.random.setstate(_restore_tuple(state["random_state"]))

        validate_graph(brain.sparks.values(), brain.connections, brain.broadcast_listeners)
        unknown_active = brain._active_hypotheses - set(brain.sparks)
        if unknown_active:
            raise ValueError(f"Unknown active hypotheses: {sorted(unknown_active)}")
        for event in brain._queue:
            if event.target is not None and event.target not in brain.sparks:
                raise ValueError(f"Queued event targets unknown Spark: {event.target}")
        return brain

    def load_state_dict(self, state: dict) -> None:
        """Replace this instance with a fully validated checkpoint state."""

        restored = type(self).from_state_dict(state)
        self.__dict__.clear()
        self.__dict__.update(restored.__dict__)
