from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.endogenous_chain import EndogenousChainIntervention

from .v06_confirmatory_heldout_primary import (
    _chain_paths,
    _estimated_reinjection_gain,
    _pulse,
    _run_cue,
    _runtime,
    _train_expectation,
)
from .v06_confirmatory_training_schedule import (
    build_balanced_training_schedule,
)
from .v061_diagnostic_worlds import DiagnosticWorld, lag_factor_worlds


@dataclass(frozen=True, slots=True)
class RootCandidateTelemetry:
    branch: str
    source_unit_id: int
    target_unit_id: int
    observation_count: int
    frequency: float
    mean_lag_ms: float
    lag_variance_ms2: float
    temporal_stability: float
    confidence: float
    reinjection_gain: float
    effective_current: float
    threshold: float
    current_threshold_ratio: float
    predicted_arrival_ms: float
    profile_indices: tuple[int, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ChainRunTelemetry:
    condition: str
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    first_generation_units: tuple[int, ...]
    main_trajectory_present: bool
    alternate_trajectory_present: bool
    trajectory_class: str
    proposal_count: int
    accepted_proposal_count: int
    rejected_proposal_count: int
    maximum_same_time_proposals: int
    proposals: tuple[dict[str, Any], ...]
    sparks: tuple[dict[str, Any], ...]
    interventions: tuple[dict[str, Any], ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CausalBaselineTelemetry:
    baseline_status: str
    baseline_main_downstream_count: int
    targeted_main_downstream_count: int
    matched_main_downstream_count: int
    formal_targeted_impairment: float
    formal_matched_impairment: float
    formal_selective_effect: float
    selectivity_interpretable: bool
    diagnostic_targeted_impairment: float | None
    diagnostic_matched_impairment: float | None
    diagnostic_selective_effect: float | None
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LagWorldDiagnosis:
    family_id: str
    seed: int
    factor_name: str
    factor_value: str
    shared_root: bool
    exposure_counts: tuple[int, ...]
    profile_assignments: tuple[tuple[str, tuple[int, ...]], ...]
    root_candidates: tuple[RootCandidateTelemetry, ...]
    predicted_root_winner: str | None
    predicted_expressed_branches: tuple[str, ...]
    sham: ChainRunTelemetry
    targeted: ChainRunTelemetry
    matched: ChainRunTelemetry
    causal_baseline: CausalBaselineTelemetry

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "causal_baseline": self.causal_baseline.state_dict(),
            "matched": self.matched.state_dict(),
            "root_candidates": [row.state_dict() for row in self.root_candidates],
            "sham": self.sham.state_dict(),
            "targeted": self.targeted.state_dict(),
        }


def _is_subsequence(values: tuple[int, ...], expected: tuple[int, ...]) -> bool:
    if not expected:
        return True
    index = 0
    for value in values:
        if value == expected[index]:
            index += 1
            if index == len(expected):
                return True
    return False


def _branch_name(world: DiagnosticWorld, target_unit_id: int) -> str:
    if target_unit_id == world.main_path[1]:
        return "main"
    if target_unit_id == world.alternate_path[1]:
        return "alternate"
    if target_unit_id == world.control_path[1]:
        return "control"
    return f"unit:{target_unit_id}"


def _path_profile_assignments(
    world: DiagnosticWorld,
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    paths = _chain_paths(world)  # type: ignore[arg-type]
    competition = dict(
        zip(
            world.competition_paths,
            world.branch_exposure_counts,
            strict=True,
        )
    )
    counts = tuple(
        competition.get(path, max(3, len(world.training_lag_profiles_ms)))
        for path in paths
    )
    schedule = build_balanced_training_schedule(
        counts,
        lag_profile_count=len(world.training_lag_profiles_ms),
    )
    names = tuple(
        "main"
        if path == world.main_path
        else "alternate"
        if path == world.alternate_path
        else "control"
        if path == world.control_path
        else f"path:{index}"
        for index, path in enumerate(paths)
    )
    return tuple(
        (
            names[path_index],
            tuple(
                episode.lag_profile_index
                for episode in schedule.episodes
                if episode.path_index == path_index
            ),
        )
        for path_index in range(len(paths))
    )


def _root_candidates(
    world: DiagnosticWorld,
) -> tuple[RootCandidateTelemetry, ...]:
    paths = _chain_paths(world)  # type: ignore[arg-type]
    model = _train_expectation(world, paths)  # type: ignore[arg-type]
    gain = _estimated_reinjection_gain(world, model, paths)  # type: ignore[arg-type]
    source_target = f"unit:{world.main_path[0]}"
    transition_table = model.learned_state_dict()["transitions"].get(
        source_target,
        {},
    )
    eligible = {
        target: stats
        for target, stats in transition_table.items()
        if int(stats["count"]) >= model.config.minimum_observations
    }
    total = sum(int(stats["count"]) for stats in eligible.values())
    source = _pulse(
        world,  # type: ignore[arg-type]
        "diagnostic:root-proposal",
        0.0,
        world.main_path[0],
    )
    proposals = {
        proposal.target: proposal
        for proposal in model.proposals_for(
            source,
            origin_state_hash="0" * 64,
        )
    }
    assignments = dict(_path_profile_assignments(world))
    rows: list[RootCandidateTelemetry] = []
    for target, stats in sorted(eligible.items()):
        target_unit_id = int(str(target).removeprefix("unit:"))
        branch = _branch_name(world, target_unit_id)
        count = int(stats["count"])
        variance = float(stats["lag_m2"]) / max(1, count - 1)
        frequency = count / total
        stability = 1.0 / (1.0 + variance / model.config.variance_scale_ms2)
        confidence = frequency * stability
        proposal = proposals.get(target)
        effective_current = min(
            max(2.0, world.cue_magnitude * gain),
            float(stats["mean_magnitude"]) * confidence * gain,
        )
        rows.append(
            RootCandidateTelemetry(
                branch=branch,
                source_unit_id=world.main_path[0],
                target_unit_id=target_unit_id,
                observation_count=count,
                frequency=frequency,
                mean_lag_ms=float(stats["mean_lag_ms"]),
                lag_variance_ms2=variance,
                temporal_stability=stability,
                confidence=confidence,
                reinjection_gain=gain,
                effective_current=effective_current,
                threshold=world.threshold,
                current_threshold_ratio=effective_current / world.threshold,
                predicted_arrival_ms=(
                    float(proposal.predicted_arrival_ms)
                    if proposal is not None
                    else float(stats["mean_lag_ms"])
                ),
                profile_indices=assignments.get(branch, ()),
            )
        )
    return tuple(sorted(rows, key=lambda row: (-row.confidence, row.branch)))


def _run_chain(
    world: DiagnosticWorld,
    *,
    condition: str,
    intervention: EndogenousChainIntervention | None,
) -> ChainRunTelemetry:
    runtime = _runtime(
        world,  # type: ignore[arg-type]
        _chain_paths(world),  # type: ignore[arg-type]
        intervention=intervention,
    )
    _run_cue(
        runtime,
        world,  # type: ignore[arg-type]
        cue_unit_id=world.control_path[0],
        start_ms=100.0,
        event_id=f"diagnostic:{condition}:control",
    )
    main_start = 100.0 + world.episode_spacings_ms[0]
    proposal_before = len(runtime.proposal_records)
    spark_before = len(runtime.generated_sparks)
    intervention_before = len(runtime.intervention_records)
    result = _run_cue(
        runtime,
        world,  # type: ignore[arg-type]
        cue_unit_id=world.main_path[0],
        start_ms=main_start,
        event_id=f"diagnostic:{condition}:main",
    )
    proposals = tuple(runtime.proposal_records[proposal_before:])
    sparks = tuple(runtime.generated_sparks[spark_before:])
    interventions = tuple(runtime.intervention_records[intervention_before:])
    units = result.units
    main_present = _is_subsequence(units, world.main_path[1:])
    alternate_present = _is_subsequence(units, world.alternate_path[1:])
    if units == world.main_path[1:]:
        trajectory_class = "main-only-exact"
    elif main_present and alternate_present:
        trajectory_class = "dual-trajectory-superposition"
    elif alternate_present and not main_present:
        trajectory_class = "alternate-only-substitution"
    elif main_present:
        trajectory_class = "main-with-extra-activity"
    elif not units:
        trajectory_class = "no-endogenous-trajectory"
    else:
        trajectory_class = "incomplete-or-other-trajectory"
    time_counts = Counter(
        round(row.predicted_arrival_ms, 9)
        for row in proposals
        if row.reinjection is not None and row.reinjection.accepted
    )
    return ChainRunTelemetry(
        condition=condition,
        generated_units=units,
        generated_times_ms=result.times_ms,
        first_generation_units=tuple(
            row.unit_id for row in sparks if row.generation_depth == 1
        ),
        main_trajectory_present=main_present,
        alternate_trajectory_present=alternate_present,
        trajectory_class=trajectory_class,
        proposal_count=len(proposals),
        accepted_proposal_count=sum(
            row.reinjection is not None and row.reinjection.accepted
            for row in proposals
        ),
        rejected_proposal_count=sum(
            row.reinjection is not None and not row.reinjection.accepted
            for row in proposals
        ),
        maximum_same_time_proposals=max(time_counts.values(), default=0),
        proposals=tuple(row.state_dict() for row in proposals),
        sparks=tuple(row.state_dict() for row in sparks),
        interventions=tuple(row.state_dict() for row in interventions),
    )


def _main_downstream_count(
    world: DiagnosticWorld,
    run: ChainRunTelemetry,
) -> int:
    return sum(unit in world.main_path[2:] for unit in run.generated_units)


def _causal_baseline(
    world: DiagnosticWorld,
    sham: ChainRunTelemetry,
    targeted: ChainRunTelemetry,
    matched: ChainRunTelemetry,
) -> CausalBaselineTelemetry:
    sham_count = _main_downstream_count(world, sham)
    targeted_count = _main_downstream_count(world, targeted)
    matched_count = _main_downstream_count(world, matched)
    denominator = max(1, sham_count)
    formal_targeted = 1.0 - targeted_count / denominator
    formal_matched = 1.0 - matched_count / denominator
    formal_effect = formal_targeted - formal_matched
    if not sham.main_trajectory_present:
        baseline_status = "absent"
        interpretation = (
            "The tested main trajectory is absent before intervention; formal "
            "selectivity is diagnostically uninterpretable."
        )
        interpretable = False
        diagnostic_targeted = None
        diagnostic_matched = None
        diagnostic_effect = None
    else:
        baseline_status = (
            "present-exact"
            if sham.trajectory_class == "main-only-exact"
            else "present-superposed"
        )
        interpretable = sham_count > 0
        if interpretable:
            diagnostic_targeted = 1.0 - targeted_count / sham_count
            diagnostic_matched = 1.0 - matched_count / sham_count
            diagnostic_effect = diagnostic_targeted - diagnostic_matched
            interpretation = (
                "Selectivity is interpretable because the main trajectory exists "
                "in the sham baseline."
            )
        else:
            diagnostic_targeted = None
            diagnostic_matched = None
            diagnostic_effect = None
            interpretation = "Main root exists, but no downstream main baseline exists."
    return CausalBaselineTelemetry(
        baseline_status=baseline_status,
        baseline_main_downstream_count=sham_count,
        targeted_main_downstream_count=targeted_count,
        matched_main_downstream_count=matched_count,
        formal_targeted_impairment=formal_targeted,
        formal_matched_impairment=formal_matched,
        formal_selective_effect=formal_effect,
        selectivity_interpretable=interpretable,
        diagnostic_targeted_impairment=diagnostic_targeted,
        diagnostic_matched_impairment=diagnostic_matched,
        diagnostic_selective_effect=diagnostic_effect,
        interpretation=interpretation,
    )


def diagnose_lag_world(world: DiagnosticWorld) -> LagWorldDiagnosis:
    world.validate()
    root_candidates = _root_candidates(world)
    predicted_winner = root_candidates[0].branch if root_candidates else None
    expressed = tuple(
        sorted(
            row.branch
            for row in root_candidates
            if row.current_threshold_ratio + 1e-12 >= 1.0
        )
    )
    sham = _run_chain(world, condition="sham", intervention=None)
    targeted = _run_chain(
        world,
        condition="targeted",
        intervention=EndogenousChainIntervention(
            suppress_expansion_unit_ids=(world.main_path[1],)
        ),
    )
    matched = _run_chain(
        world,
        condition="matched",
        intervention=EndogenousChainIntervention(
            suppress_expansion_unit_ids=(world.control_path[1],)
        ),
    )
    return LagWorldDiagnosis(
        family_id=world.family_id,
        seed=world.seed,
        factor_name=world.factor_name,
        factor_value=world.factor_value,
        shared_root=world.main_path[0] == world.alternate_path[0],
        exposure_counts=world.branch_exposure_counts,
        profile_assignments=_path_profile_assignments(world),
        root_candidates=root_candidates,
        predicted_root_winner=predicted_winner,
        predicted_expressed_branches=expressed,
        sham=sham,
        targeted=targeted,
        matched=matched,
        causal_baseline=_causal_baseline(world, sham, targeted, matched),
    )


def run_lag_diagnostic_suite() -> dict[str, Any]:
    diagnoses = tuple(diagnose_lag_world(world) for world in lag_factor_worlds())
    prediction_matches = sum(
        set(row.predicted_expressed_branches)
        == {
            branch
            for branch, present in (
                ("main", row.sham.main_trajectory_present),
                ("alternate", row.sham.alternate_trajectory_present),
            )
            if present
        }
        for row in diagnoses
        if row.shared_root
    )
    shared_count = sum(row.shared_root for row in diagnoses)
    return {
        "scope": "development-only factor-controlled SparkBrain diagnosis",
        "candidate_003_executions": 0,
        "world_count": len(diagnoses),
        "shared_root_world_count": shared_count,
        "root_threshold_prediction_match_count": prediction_matches,
        "root_threshold_prediction_match_fraction": (
            prediction_matches / shared_count if shared_count else math.nan
        ),
        "baseline_absent_count": sum(
            row.causal_baseline.baseline_status == "absent" for row in diagnoses
        ),
        "baseline_superposed_count": sum(
            row.causal_baseline.baseline_status == "present-superposed"
            for row in diagnoses
        ),
        "selectivity_interpretable_count": sum(
            row.causal_baseline.selectivity_interpretable for row in diagnoses
        ),
        "worlds": [row.state_dict() for row in diagnoses],
    }
