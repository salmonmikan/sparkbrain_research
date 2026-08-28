from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v03_seed import EvidenceContribution

from .runtime import (
    ACTION_TYPES,
    IntegratedV03Brain,
    SensorySample,
    V03BrainConfig,
    V03StepResult,
)

ENGINEERING_METRICS = (
    "coverage",
    "false_ignition_rate",
    "no_ignition_f1",
    "revision",
    "recovery",
    "calibration_error",
    "invariance",
    "attribution_fidelity",
    "entity_cross_talk",
    "active_spark_ratio",
    "dense_input_inspection_count",
    "downstream_active_work",
    "action_regret",
    "checkpoint_continuation_equality",
    "world_count",
)

ENGINEERING_WORLDS = (
    "repetition_omission",
    "multi_entity_cross_talk",
    "duplicate_correlated_evidence",
    "contradiction_reversal",
    "recovery",
    "goal_biased_search",
    "continuous_novelty",
    "action_feedback",
)

ENGINEERING_VARIANTS = (
    "full",
    "legacy",
    "baseline",
    "no_residual",
    "no_maintain_objective",
    "no_revision_objective",
    "no_recovery_objective",
    "one_weighted_ce",
    "no_attribution",
    "no_coalition",
)


@dataclass(frozen=True, slots=True)
class _WorldOutcome:
    action_type: str
    active_sparks: int
    attribution_total: int
    attribution_valid: int
    dense_input_inspection_count: int
    distractor_invariant: bool | None
    downstream_active_work: int
    duplicate_invariant: bool | None
    entity_cross_talk_events: int
    entity_cross_talk_opportunities: int
    expected_ignition: bool
    expected_transition: str | None
    feedback_evidence_returned: bool | None
    goal_bias_effect: bool | None
    input_sequence_hash: str
    predicted_ignition: bool
    predicted_transition: str
    probability: float
    recovery_latency: int | None
    recovery_opportunity: bool
    recovery_success: bool


_ROW_FIELDS = frozenset(
    {"config", "variant_id", "world_id", *_WorldOutcome.__dataclass_fields__}
)


def _sample(
    world: str,
    index: int,
    *,
    source: str,
    values: Mapping[str, float] | None = None,
    text: str | None = None,
    entity: str | None = None,
    correlation_group: str | None = None,
    omitted_channels: tuple[str, ...] = (),
) -> SensorySample:
    return SensorySample(
        sample_id=f"engineering:{world}:{index}:{source}",
        time=float(index),
        source_id=f"engineering:{world}:{source}",
        modality="engineering",
        values=dict(values if values is not None else {f"signal-{index}": 1.0}),
        omitted_channels=omitted_channels,
        correlation_group=correlation_group,
        entity_hint=entity,
        metadata={"text": text or f"stable {world} target"},
    )


def _variant_config(variant: str, world: str) -> V03BrainConfig:
    if variant not in ENGINEERING_VARIANTS:
        raise ValueError(f"unknown engineering variant: {variant}")
    entity_track = "E1_oracle_entity" if world == "multi_entity_cross_talk" else "E0_global"
    common = {
        "allow_oracle_diagnostics": entity_track == "E1_oracle_entity",
        "entity_track": entity_track,
    }
    if variant == "legacy":
        return V03BrainConfig(input_track="I0_whole_hash", **common)
    if variant == "baseline":
        return V03BrainConfig(ignition_threshold=1_000_000.0, **common)
    ablations = () if variant == "full" else (variant,)
    return V03BrainConfig(ablations=ablations, **common)


def _ratio(numerator: int | float, denominator: int | float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def _f1(tp: int, fp: int, fn: int) -> float:
    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    return _ratio(2.0 * precision * recall, precision + recall)


def _digest(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _probability(result: V03StepResult, config: V03BrainConfig) -> float:
    decisions = result.decisions
    if not decisions:
        return 0.0
    denominator = max(1.0, float(config.ignition_threshold) * 2.0)
    return min(1.0, max(0.0, float(decisions[0].score) / denominator))


def _run_world(variant: str, world: str) -> _WorldOutcome:
    config = _variant_config(variant, world)
    brain = IntegratedV03Brain(config)
    attribution_total = attribution_valid = 0
    interventions: list[dict[str, str]] = []

    def run(
        sample: SensorySample,
        *,
        goal_bias: Mapping[str, float] | None = None,
        feedback: Mapping[str, Any] | None = None,
    ) -> V03StepResult:
        nonlocal attribution_total, attribution_valid
        result = brain.step(sample, goal_bias=goal_bias, world_feedback=feedback)
        active_ids = {row.evidence_id for row in brain.ledger.rows()}
        cited_ids = {
            row["evidence_id"]
            for attribution in result.attributions
            for row in attribution["rows"]
        }
        attribution_total += len(cited_ids)
        attribution_valid += len(cited_ids & active_ids)
        return result

    expected_ignition = True
    expected_transition: str | None = None
    duplicate_invariant: bool | None = None
    distractor_invariant: bool | None = None
    cross_talk_events = cross_talk_opportunities = 0
    recovery_opportunity = recovery_success = False
    recovery_latency: int | None = None
    feedback_evidence_returned: bool | None = None
    goal_bias_effect: bool | None = None

    if world == "repetition_omission":
        run(_sample(world, 0, source="steady", values={"tone": 1.0}))
        run(_sample(world, 1, source="steady", values={"tone": 1.0}))
        result = run(
            _sample(
                world,
                2,
                source="steady",
                values={},
                omitted_channels=("tone",),
            )
        )
        expected_ignition = False
    elif world == "multi_entity_cross_talk":
        run(_sample(world, 0, source="a-1", text="alpha target", entity="entity-a"))
        run(_sample(world, 1, source="a-2", text="alpha target", entity="entity-a"))
        before = brain.inspect()["beliefs"].get("entity-a", {}).get("winner")
        run(_sample(world, 2, source="b-1", text="beta target", entity="entity-b"))
        result = run(
            _sample(world, 3, source="b-2", text="beta target", entity="entity-b")
        )
        after = brain.inspect()["beliefs"].get("entity-a", {}).get("winner")
        cross_talk_opportunities = 1
        cross_talk_events = int(before != after)
    elif world == "duplicate_correlated_evidence":
        group = "engineering:duplicate:one-causal-event"
        run(_sample(world, 0, source="copy-a", correlation_group=group))
        result = run(_sample(world, 1, source="copy-b", correlation_group=group))
        expected_ignition = False
        duplicate_invariant = not bool(result.action)
    elif world == "contradiction_reversal":
        run(_sample(world, 0, source="old-a", text="alpha zeta"))
        established = run(_sample(world, 1, source="old-b", text="alpha zeta"))
        old_belief = established.beliefs.get("__global__")
        interventions.append(
            {"evidence_id": "engineering:reversal-counter", "operation": "add"}
        )
        if old_belief is not None:
            brain.ledger.add(
                EvidenceContribution(
                    evidence_id="engineering:reversal-counter",
                    source_id="engineering:reversal:counter",
                    belief_key=old_belief,
                    time=2.0,
                    support=0.0,
                    contradiction=10.0,
                )
            )
        run(_sample(world, 20, source="new-a", text="beta omega"))
        result = run(_sample(world, 21, source="new-b", text="beta omega"))
        expected_transition = "revise"
    elif world == "recovery":
        run(_sample(world, 0, source="source-a"))
        established = run(_sample(world, 1, source="source-b"))
        belief = established.beliefs.get("__global__")
        counter_id = "engineering:recovery-counter"
        interventions.append({"evidence_id": counter_id, "operation": "add"})
        if belief is not None:
            brain.ledger.add(
                EvidenceContribution(
                    evidence_id=counter_id,
                    source_id="engineering:recovery:counter",
                    belief_key=belief,
                    time=2.0,
                    support=0.0,
                    contradiction=10.0,
                )
            )
        blocked = run(_sample(world, 2, source="source-c"))
        interventions.append({"evidence_id": counter_id, "operation": "remove"})
        if belief is not None:
            brain.ledger.remove(counter_id)
        result = run(_sample(world, 3, source="source-d"))
        expected_transition = "recover"
        recovery_opportunity = True
        recovery_success = (
            result.revision_transitions[0]["accepted"] is True
            and result.revision_transitions[0]["transition"] == "recover"
        )
        if recovery_success:
            recovery_latency = result.step_index - blocked.step_index
    elif world == "goal_biased_search":
        first = _sample(world, 0, source="same", values={"quiet": 1.0})
        second = _sample(world, 1, source="same", values={"quiet": 1.0})
        third = _sample(world, 2, source="independent", values={"quiet": 0.4})
        run(first)
        run(second)
        result = run(
            third,
            goal_bias={"engineering:quiet": 2.0},
        )
        control = IntegratedV03Brain(config)
        control.step(first)
        control.step(second)
        control_result = control.step(third)
        goal_bias_effect = len(result.sparks) > len(control_result.sparks)
    elif world == "continuous_novelty":
        first = _sample(world, 0, source="source-a", values={"novel-a": 1.0})
        second = _sample(world, 1, source="source-b", values={"novel-b": 1.0})
        run(first)
        run(second)
        values = {"novel-c": 1.0}
        values.update({f"distractor-{index}": 0.01 for index in range(12)})
        result = run(_sample(world, 2, source="source-c", values=values))
        control = IntegratedV03Brain(config)
        control.step(first)
        control.step(second)
        control_result = control.step(
            _sample(world, 2, source="source-c", values={"novel-c": 1.0})
        )
        distractor_invariant = bool(result.action) == bool(control_result.action)
    elif world == "action_feedback":
        run(_sample(world, 0, source="source-a"))
        result = run(
            _sample(world, 1, source="source-b"),
            feedback={
                "status": "observed",
                "text": "environment changed",
                "values": {"reward_signal": 0.25},
            },
        )
        feedback_evidence_returned = any(
            spark.feature_id == "world_feedback:reward_signal"
            for spark in result.sparks
        ) and any(row.source_id.startswith("world:") for row in brain.ledger.rows())
    else:  # pragma: no cover - protected by the frozen world inventory
        raise ValueError(f"unknown engineering world: {world}")

    inventory = brain.component_inventory()
    counters = inventory["sensory"]["counters"]
    transition = (
        result.revision_transitions[0]["transition"]
        if result.revision_transitions
        else "insufficient_information"
    )
    return _WorldOutcome(
        action_type=result.action_type,
        active_sparks=int(counters["sparks_emitted"]),
        attribution_total=attribution_total,
        attribution_valid=attribution_valid,
        dense_input_inspection_count=int(counters["channels_inspected"]),
        distractor_invariant=distractor_invariant,
        downstream_active_work=int(counters["downstream_active_work"]),
        duplicate_invariant=duplicate_invariant,
        entity_cross_talk_events=cross_talk_events,
        entity_cross_talk_opportunities=cross_talk_opportunities,
        expected_ignition=expected_ignition,
        expected_transition=expected_transition,
        feedback_evidence_returned=feedback_evidence_returned,
        goal_bias_effect=goal_bias_effect,
        input_sequence_hash=_digest(
            {"history": list(brain.history), "interventions": interventions}
        ),
        predicted_ignition=bool(result.action),
        predicted_transition=transition,
        probability=_probability(result, config),
        recovery_latency=recovery_latency,
        recovery_opportunity=recovery_opportunity,
        recovery_success=recovery_success,
    )


def _checkpoint_probe(config: V03BrainConfig) -> bool:
    if config.entity_track != "E0_global":
        config = replace(
            config,
            allow_oracle_diagnostics=False,
            entity_track="E0_global",
        )
    brain = IntegratedV03Brain(config)
    brain.step(_sample("checkpoint", 0, source="source-a"))
    restored = IntegratedV03Brain.restore(brain.checkpoint("engineering-evaluation"))
    next_sample = _sample("checkpoint", 1, source="source-b")
    return brain.step(next_sample).as_dict() == restored.step(next_sample).as_dict()


def _metrics(rows: list[dict[str, Any]], *, checkpoint_equal: bool) -> dict[str, Any]:
    positives = [row for row in rows if row["expected_ignition"]]
    negatives = [row for row in rows if not row["expected_ignition"]]
    false_positive = sum(row["predicted_ignition"] for row in negatives)
    no_ignition_tp = sum(not row["predicted_ignition"] for row in negatives)
    no_ignition_fp = sum(not row["predicted_ignition"] for row in positives)
    no_ignition_fn = false_positive
    revision_opportunities = [
        row for row in rows if row["expected_transition"] == "revise"
    ]
    predicted_revisions = [row for row in rows if row["predicted_transition"] == "revise"]
    correct_revisions = [row for row in predicted_revisions if row in revision_opportunities]
    recovery_rows = [row for row in rows if row["recovery_opportunity"]]
    recovered = [row for row in recovery_rows if row["recovery_success"]]
    recovery_latencies = [row["recovery_latency"] for row in recovered]
    cited = sum(row["attribution_total"] for row in rows)
    valid_citations = sum(row["attribution_valid"] for row in rows)
    cross_talk_events = sum(row["entity_cross_talk_events"] for row in rows)
    cross_talk_opportunities = sum(
        row["entity_cross_talk_opportunities"] for row in rows
    )
    dense = sum(row["dense_input_inspection_count"] for row in rows)
    active = sum(row["active_sparks"] for row in rows)
    metrics = {
        "coverage": _ratio(
            sum(row["predicted_ignition"] for row in positives), len(positives)
        ),
        "false_ignition_rate": _ratio(false_positive, len(negatives)),
        "no_ignition_f1": _f1(no_ignition_tp, no_ignition_fp, no_ignition_fn),
        "revision": {
            "precision": _ratio(len(correct_revisions), len(predicted_revisions)),
            "recall": _ratio(len(correct_revisions), len(revision_opportunities)),
        },
        "recovery": {
            "latency": (
                _ratio(sum(recovery_latencies), len(recovery_latencies))
                if recovery_latencies
                else None
            ),
            "rate": _ratio(len(recovered), len(recovery_rows)),
        },
        "calibration_error": _ratio(
            sum(
                abs(row["probability"] - float(row["expected_ignition"]))
                for row in rows
            ),
            len(rows),
        ),
        "invariance": {
            "distractor": _ratio(
                sum(row["distractor_invariant"] is True for row in rows),
                sum(row["distractor_invariant"] is not None for row in rows),
            ),
            "duplicate": _ratio(
                sum(row["duplicate_invariant"] is True for row in rows),
                sum(row["duplicate_invariant"] is not None for row in rows),
            ),
        },
        "attribution_fidelity": _ratio(valid_citations, cited) if cited else 1.0,
        "entity_cross_talk": _ratio(cross_talk_events, cross_talk_opportunities),
        "active_spark_ratio": _ratio(active, dense),
        "dense_input_inspection_count": dense,
        "downstream_active_work": sum(row["downstream_active_work"] for row in rows),
        "action_regret": _ratio(
            sum(row["predicted_ignition"] != row["expected_ignition"] for row in rows),
            len(rows),
        ),
        "checkpoint_continuation_equality": checkpoint_equal,
        "world_count": len(rows),
    }
    if tuple(metrics) != ENGINEERING_METRICS:
        raise RuntimeError("engineering metric inventory drifted")
    return metrics


def evaluate_engineering_runtime() -> dict[str, Any]:
    """Evaluate all frozen engineering variants without scientific claims.

    ``full`` is the dependency-light I1 integrated runtime. ``legacy`` uses the
    existing I0 whole-hash frontend, while ``baseline`` is an explicit
    no-ignition high-threshold control. The seven remaining variants use the
    exact registered ablations. I3/C15 controller integration is tested by the
    runtime suite but is not silently substituted into this CPU-only matrix.
    """

    rows: list[dict[str, Any]] = []
    metrics: dict[str, dict[str, Any]] = {}
    variants: list[dict[str, Any]] = []
    for variant in ENGINEERING_VARIANTS:
        variant_rows: list[dict[str, Any]] = []
        for world in ENGINEERING_WORLDS:
            outcome = _run_world(variant, world)
            row = {
                "config": _variant_config(variant, world).as_dict(),
                "variant_id": variant,
                "world_id": world,
                **asdict(outcome),
            }
            rows.append(row)
            variant_rows.append(row)
        config = _variant_config(variant, ENGINEERING_WORLDS[0])
        metrics[variant] = _metrics(
            variant_rows,
            checkpoint_equal=_checkpoint_probe(config),
        )
        variants.append(
            {
                "config": config.as_dict(),
                "role": {
                    "baseline": "high_threshold_no_ignition_control",
                    "full": "integrated_i1_reference",
                    "legacy": "i0_whole_hash_frontend",
                }.get(variant, "registered_ablation"),
                "variant_id": variant,
            }
        )
    document = {
        "metrics": metrics,
        "rows": rows,
        "status": "engineering_only_not_scientific",
        "variants": variants,
        "world_ids": list(ENGINEERING_WORLDS),
    }
    validate_engineering_evaluation(document)
    return document


def _finite_number(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite number")
    return result


def _rate(value: object, *, name: str) -> float:
    result = _finite_number(value, name=name)
    if not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return result


def _validate_metric_row(metrics: object) -> None:
    if (
        not isinstance(metrics, dict)
        or len(metrics) != len(ENGINEERING_METRICS)
        or set(metrics) != set(ENGINEERING_METRICS)
    ):
        raise ValueError("engineering metric inventory drifted")
    for name in (
        "coverage",
        "false_ignition_rate",
        "no_ignition_f1",
        "calibration_error",
        "attribution_fidelity",
        "entity_cross_talk",
        "active_spark_ratio",
        "action_regret",
    ):
        _rate(metrics[name], name=name)
    for name, expected in (
        ("revision", {"precision", "recall"}),
        ("recovery", {"latency", "rate"}),
        ("invariance", {"distractor", "duplicate"}),
    ):
        value = metrics[name]
        if not isinstance(value, Mapping) or set(value) != expected:
            raise ValueError(f"engineering metric {name} has unexpected fields")
    _rate(metrics["revision"]["precision"], name="revision.precision")
    _rate(metrics["revision"]["recall"], name="revision.recall")
    _rate(metrics["recovery"]["rate"], name="recovery.rate")
    latency = metrics["recovery"]["latency"]
    if latency is not None and _finite_number(latency, name="recovery.latency") < 0.0:
        raise ValueError("recovery.latency must be non-negative or null")
    _rate(metrics["invariance"]["distractor"], name="invariance.distractor")
    _rate(metrics["invariance"]["duplicate"], name="invariance.duplicate")
    for name in ("dense_input_inspection_count", "downstream_active_work"):
        value = metrics[name]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if metrics["world_count"] != len(ENGINEERING_WORLDS):
        raise ValueError("world_count must equal the exact world inventory")
    if metrics["checkpoint_continuation_equality"] is not True:
        raise ValueError("checkpoint continuation equality must pass")


def validate_engineering_evaluation(document: object) -> None:
    """Fail closed on drift in the engineering-only matrix contract."""

    if not isinstance(document, dict) or set(document) != {
        "metrics",
        "rows",
        "status",
        "variants",
        "world_ids",
    }:
        raise ValueError("engineering evaluation has unexpected top-level fields")
    if document["status"] != "engineering_only_not_scientific":
        raise ValueError("engineering evaluation status must remain non-scientific")
    if document["world_ids"] != list(ENGINEERING_WORLDS):
        raise ValueError("engineering evaluation world inventory drifted")
    variants = document["variants"]
    if not isinstance(variants, list) or [row.get("variant_id") for row in variants] != list(
        ENGINEERING_VARIANTS
    ):
        raise ValueError("engineering evaluation variant inventory drifted")
    for row in variants:
        if not isinstance(row, dict) or set(row) != {"config", "role", "variant_id"}:
            raise ValueError("engineering evaluation variant has unexpected fields")
        V03BrainConfig.from_dict(row["config"])
    metrics = document["metrics"]
    if not isinstance(metrics, dict) or set(metrics) != set(ENGINEERING_VARIANTS):
        raise ValueError("engineering evaluation metric variants drifted")
    for variant in ENGINEERING_VARIANTS:
        _validate_metric_row(metrics[variant])
    rows = document["rows"]
    expected_pairs = [
        (variant, world)
        for variant in ENGINEERING_VARIANTS
        for world in ENGINEERING_WORLDS
    ]
    if not isinstance(rows, list) or len(rows) != len(expected_pairs):
        raise ValueError("engineering evaluation row cardinality drifted")
    for row, pair in zip(rows, expected_pairs, strict=True):
        if not isinstance(row, dict) or set(row) != _ROW_FIELDS:
            raise ValueError("engineering evaluation row has unexpected fields")
        if (row["variant_id"], row["world_id"]) != pair:
            raise ValueError("engineering evaluation row order drifted")
        if V03BrainConfig.from_dict(row["config"]) != _variant_config(*pair):
            raise ValueError("engineering evaluation row config drifted")
        if row["action_type"] not in ACTION_TYPES:
            raise ValueError("engineering evaluation action type is invalid")
        for name in (
            "expected_ignition",
            "predicted_ignition",
            "recovery_opportunity",
            "recovery_success",
        ):
            if not isinstance(row[name], bool):
                raise ValueError(f"engineering evaluation {name} must be boolean")
        _rate(row["probability"], name="engineering evaluation probability")
        for name in (
            "active_sparks",
            "attribution_total",
            "attribution_valid",
            "dense_input_inspection_count",
            "downstream_active_work",
            "entity_cross_talk_events",
            "entity_cross_talk_opportunities",
        ):
            value = row[name]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"engineering evaluation {name} must be non-negative")
        if row["attribution_valid"] > row["attribution_total"]:
            raise ValueError("valid attribution count cannot exceed total attribution")
        for name in (
            "distractor_invariant",
            "duplicate_invariant",
            "feedback_evidence_returned",
            "goal_bias_effect",
        ):
            if row[name] is not None and not isinstance(row[name], bool):
                raise ValueError(f"engineering evaluation {name} must be boolean or null")
        latency = row["recovery_latency"]
        if latency is not None and (
            isinstance(latency, bool) or not isinstance(latency, int) or latency < 0
        ):
            raise ValueError("engineering recovery latency must be non-negative or null")
        expected_transition = row["expected_transition"]
        if expected_transition not in {None, "revise", "recover"}:
            raise ValueError("engineering expected transition is invalid")
        if row["predicted_transition"] not in {
            "insufficient_information",
            "maintain",
            "recover",
            "revise",
        }:
            raise ValueError("engineering predicted transition is invalid")
        sequence_hash = row["input_sequence_hash"]
        if (
            not isinstance(sequence_hash, str)
            or len(sequence_hash) != 64
            or any(character not in "0123456789abcdef" for character in sequence_hash)
        ):
            raise ValueError("engineering input sequence hash is invalid")
    for world in ENGINEERING_WORLDS:
        hashes = {
            row["input_sequence_hash"] for row in rows if row["world_id"] == world
        }
        if len(hashes) != 1:
            raise ValueError("engineering variants must share an exact input sequence")
