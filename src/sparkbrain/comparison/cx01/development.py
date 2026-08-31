from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .contract import ComparatorKind, ComparatorProtocol
from .events import ComparatorEvent, EventOrigin
from .fairness import TrainingTranscript, build_training_transcript
from .g3_anchor import G3FirstOrderAnchor
from .g6_vomm import VariableOrderMarkovPredictor
from .g7_htm_tm import HTMTemporalMemoryComparator
from .g8_spiking_tm import SpikingTemporalMemoryComparator
from .historical_anchors import G4AssemblyAnchor, G5TypedAnchor
from .resources import ResourceRecord, measure_model_call
from .scoring import (
    FamilyDecision,
    FamilyEvidence,
    brier_score,
    cross_entropy,
    decide_family,
)
from .worlds import CX01Family, CX01World, build_development_grid

COMPARATOR_KINDS = (
    ComparatorKind.G3_FIRST_ORDER,
    ComparatorKind.G4_ASSEMBLY,
    ComparatorKind.G5_TYPED,
    ComparatorKind.G6_VARIABLE_ORDER,
    ComparatorKind.G7_HTM_TEMPORAL_MEMORY,
    ComparatorKind.G8_PREDICTION,
    ComparatorKind.G8_REPLAY,
)


@dataclass(frozen=True, slots=True)
class DevelopmentExecution:
    kind: ComparatorKind
    family: CX01Family
    seed: int
    world_hash: str
    training_transcript_hash: str
    evidence: FamilyEvidence
    decision: FamilyDecision
    resource: ResourceRecord

    def state_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.state_dict(),
            "evidence": self.evidence.state_dict(),
            "family": self.family.value,
            "kind": self.kind.value,
            "resource": self.resource.state_dict(),
            "seed": self.seed,
            "training_transcript_hash": self.training_transcript_hash,
            "world_hash": self.world_hash,
        }


def create_model(kind: ComparatorKind) -> ComparatorProtocol:
    if kind is ComparatorKind.G3_FIRST_ORDER:
        return G3FirstOrderAnchor()
    if kind is ComparatorKind.G4_ASSEMBLY:
        return G4AssemblyAnchor()
    if kind is ComparatorKind.G5_TYPED:
        return G5TypedAnchor()
    if kind is ComparatorKind.G6_VARIABLE_ORDER:
        return VariableOrderMarkovPredictor()
    if kind is ComparatorKind.G7_HTM_TEMPORAL_MEMORY:
        return HTMTemporalMemoryComparator()
    if kind is ComparatorKind.G8_PREDICTION:
        return SpikingTemporalMemoryComparator(replay_mode=False)
    if kind is ComparatorKind.G8_REPLAY:
        return SpikingTemporalMemoryComparator(replay_mode=True)
    raise ValueError(f"unsupported comparator kind: {kind}")


def _feed(
    model: ComparatorProtocol,
    tokens: tuple[str, ...],
    lags_ms: tuple[float, ...],
    start_ms: float,
) -> float:
    if len(lags_ms) != max(0, len(tokens) - 1):
        raise ValueError("feed lags must align with tokens")
    now = start_ms
    model.observe_external(ComparatorEvent(tokens[0], now, EventOrigin.EXTERNAL, True))
    for token, lag in zip(tokens[1:], lags_ms, strict=True):
        now += lag
        model.observe_external(ComparatorEvent(token, now, EventOrigin.EXTERNAL))
    return now + 25.0


def _train(model: ComparatorProtocol, transcript: TrainingTranscript) -> float:
    transcript.validate()
    for event in transcript.events:
        model.observe_external(event)
    model.advance(transcript.end_time_ms)
    return transcript.end_time_ms


def _top1(distribution: dict[str, float]) -> str | None:
    if not distribution:
        return None
    return min(distribution, key=lambda token: (-distribution[token], token))


def _evaluate_probes(
    model: ComparatorProtocol,
    world: CX01World,
    now: float,
) -> tuple[FamilyEvidence, float]:
    correct = 0
    total = 0
    brier_values: list[float] = []
    log_losses: list[float] = []
    for probe in world.probes:
        now = _feed(model, probe.prefix, probe.lags_ms, now)
        observed = model.distribution().as_dict()
        expected = dict(probe.expected_distribution)
        total += 1
        expected_top = _top1(expected)
        observed_top = _top1(observed)
        correct += int(observed_top == expected_top)
        brier_values.append(brier_score(expected, observed))
        log_losses.append(cross_entropy(expected, observed))
    evidence = FamilyEvidence(
        family=world.family,
        correct_probes=correct,
        total_probes=total,
        brier_score=(sum(brier_values) / len(brier_values) if brier_values else None),
        log_loss=(sum(log_losses) / len(log_losses) if log_losses else None),
    )
    return evidence, now


def _evaluate_cycle(
    model: ComparatorProtocol,
    world: CX01World,
    now: float,
) -> tuple[FamilyEvidence, float]:
    if world.cycle_cue is None:
        raise ValueError("cycle world is missing cue")
    correct_phases = 0
    reacquisition: list[int] = []
    for phase in world.cycle_phases:
        first_correct: int | None = None
        final_correct = False
        for exposure_index in range(1, phase.exposures + 1):
            now = _feed(model, (world.cycle_cue, phase.target), (6.0,), now)
            now = _feed(model, (world.cycle_cue,), (), now)
            predicted = _top1(model.distribution().as_dict())
            final_correct = predicted == phase.target
            if final_correct and first_correct is None:
                first_correct = exposure_index
        correct_phases += int(final_correct)
        reacquisition.append(first_correct if first_correct is not None else phase.exposures + 1)
    return (
        FamilyEvidence(
            family=world.family,
            cycle_correct_fraction=correct_phases / max(1, len(world.cycle_phases)),
            maximum_reacquisition_observations=max(reacquisition, default=0),
        ),
        now,
    )


def _rollout_from_cue(
    model: ComparatorProtocol,
    cue: str,
    now: float,
    *,
    max_steps: int,
    suppressed: str | None = None,
) -> tuple[tuple[str, ...], float]:
    model.clear_suppression()
    if suppressed is not None:
        model.suppress(suppressed)
    now = _feed(model, (cue,), (), now)
    generated = tuple(row.token for row in model.generate(max_steps=max_steps))
    model.clear_suppression()
    return generated, now


def _evaluate_selectivity(
    model: ComparatorProtocol,
    world: CX01World,
    now: float,
) -> tuple[FamilyEvidence, float]:
    main = world.intervention_main
    control = world.intervention_control
    if len(main) < 3 or len(control) < 3:
        raise ValueError("selectivity paths are incomplete")
    sham, now = _rollout_from_cue(model, main[0], now, max_steps=len(main) - 1)
    targeted, now = _rollout_from_cue(
        model,
        main[0],
        now,
        max_steps=len(main) - 1,
        suppressed=main[1],
    )
    matched, now = _rollout_from_cue(
        model,
        main[0],
        now,
        max_steps=len(main) - 1,
        suppressed=control[1],
    )
    sham_downstream = sum(token in main[2:] for token in sham)
    targeted_downstream = sum(token in main[2:] for token in targeted)
    matched_downstream = sum(token in main[2:] for token in matched)
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    return (
        FamilyEvidence(
            family=world.family,
            selective_effect=targeted_impairment - matched_impairment,
        ),
        now,
    )


def _evaluate_loop(
    model: ComparatorProtocol,
    world: CX01World,
    now: float,
) -> tuple[FamilyEvidence, float]:
    if world.loop is None:
        raise ValueError("loop world is missing loop specification")
    now = _feed(model, world.loop.cue_prefix, (5.0,) * (len(world.loop.cue_prefix) - 1), now)
    before_observed = model.observed_external_events
    generated = model.generate(max_steps=1)
    after_generated_observed = model.observed_external_events
    correct = int(bool(generated) and generated[0].token == world.loop.expected_generated)
    violations = int(after_generated_observed != before_observed)
    external_time = max(
        now,
        generated[0].timestamp_ms + 8.0 if generated else now + 8.0,
    )
    model.observe_external(
        ComparatorEvent(
            world.loop.external_consequence,
            external_time,
            EventOrigin.EXTERNAL,
            False,
        )
    )
    return (
        FamilyEvidence(
            family=world.family,
            correct_probes=correct,
            total_probes=1,
            self_confirmation_violations=violations,
        ),
        external_time + 25.0,
    )


def _evaluate(
    model: ComparatorProtocol,
    world: CX01World,
    transcript: TrainingTranscript,
) -> FamilyEvidence:
    now = _train(model, transcript)
    if world.family is CX01Family.CYCLE:
        evidence, _ = _evaluate_cycle(model, world, now)
    elif world.family is CX01Family.SELECTIVITY:
        evidence, _ = _evaluate_selectivity(model, world, now)
    elif world.family is CX01Family.LOOP:
        evidence, _ = _evaluate_loop(model, world, now)
    else:
        evidence, _ = _evaluate_probes(model, world, now)
    evidence.validate()
    return evidence


def run_development_execution(
    kind: ComparatorKind,
    world: CX01World,
) -> DevelopmentExecution:
    # Materialize and hash the complete architecture-neutral training stream
    # before any comparator instance exists.
    transcript = build_training_transcript(world)
    model = create_model(kind)
    evidence, resource = measure_model_call(
        model,
        lambda: _evaluate(model, world, transcript),
    )
    decision = decide_family(evidence)
    return DevelopmentExecution(
        kind=kind,
        family=world.family,
        seed=world.seed,
        world_hash=world.specification_hash(),
        training_transcript_hash=transcript.transcript_hash(),
        evidence=evidence,
        decision=decision,
        resource=resource,
    )


def run_development_matrix() -> tuple[DevelopmentExecution, ...]:
    return tuple(
        run_development_execution(kind, world)
        for world in build_development_grid()
        for kind in COMPARATOR_KINDS
    )


def development_summary(rows: tuple[DevelopmentExecution, ...]) -> dict[str, Any]:
    by_kind: dict[str, dict[str, Any]] = {}
    for kind in COMPARATOR_KINDS:
        selected = [row for row in rows if row.kind is kind]
        family_pass = {
            family.value: sum(row.decision.passed for row in selected if row.family is family)
            for family in CX01Family
        }
        by_kind[kind.value] = {
            "executions": len(selected),
            "passed": sum(row.decision.passed for row in selected),
            "family_pass_counts": family_pass,
        }
    return {
        "architecture_count": len(COMPARATOR_KINDS),
        "execution_count": len(rows),
        "results": by_kind,
    }


def main() -> None:
    rows = run_development_matrix()
    print(json.dumps(development_summary(rows), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
