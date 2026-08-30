from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_comparators import (
    run_condition as run_comparator,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_controls import (
    run_condition as run_control,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_primary import (
    run_condition as run_primary,
)

_CONTROLS = {
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
    ConfirmatoryCondition.SHUFFLED_RELATION,
}
_COMPARATORS = {
    ConfirmatoryCondition.G3_RECURRENT,
    ConfirmatoryCondition.G4_ASSEMBLY,
    ConfirmatoryCondition.G5_TYPED,
}


@dataclass(frozen=True, slots=True)
class DevelopmentVariantWorld:
    family_id: str
    seed: int
    structural_token: str
    unit_count: int
    active_unit_ids: tuple[int, ...]
    distractor_unit_ids: tuple[int, ...]
    main_path: tuple[int, int, int, int]
    alternate_path: tuple[int, int, int, int]
    control_path: tuple[int, int, int, int]
    competition_paths: tuple[tuple[int, int, int, int], ...]
    old_target: int
    new_target: int
    third_target: int
    main_port: str
    control_port: str
    training_lag_profiles_ms: tuple[tuple[float, float, float], ...]
    evaluation_lags_ms: tuple[float, float, float]
    boundary_lag_ms: float
    threshold: float
    cue_magnitude: float
    relation_reentry_gain: float
    episode_spacings_ms: tuple[float, ...]
    branch_exposure_counts: tuple[int, ...]
    contingency_cycle_targets: tuple[int, ...]
    contingency_phase_lengths: tuple[int, ...]

    def validate(self) -> None:
        if not self.family_id.startswith("development-"):
            raise ValueError("staging variants must remain development-only")
        if not self.structural_token.startswith("development-only:"):
            raise ValueError("staging variants cannot use a confirmatory token")
        if 100 <= self.seed <= 109 or 1000 <= self.seed <= 1009:
            raise ValueError("staging variants cannot address held-out seed ranges")
        if self.unit_count < 20:
            raise ValueError("development variant requires at least 20 units")
        if set(self.active_unit_ids).intersection(self.distractor_unit_ids):
            raise ValueError("active and distractor units must be disjoint")
        all_ids = set(self.active_unit_ids).union(self.distractor_unit_ids)
        if not all(0 <= unit_id < self.unit_count for unit_id in all_ids):
            raise ValueError("unit IDs must fit the development topology")
        paths = (
            self.main_path,
            self.alternate_path,
            self.control_path,
            *self.competition_paths,
        )
        if any(len(path) != 4 or len(set(path)) != 4 for path in paths):
            raise ValueError("each development path must have four unique units")
        if any(not set(path).issubset(self.active_unit_ids) for path in paths):
            raise ValueError("every path unit must be active")
        if self.main_path[0] != self.alternate_path[0]:
            raise ValueError("main and alternate paths must share a root")
        if any(path[0] != self.main_path[0] for path in self.competition_paths):
            raise ValueError("all competing paths must share the main root")
        if set(self.control_path).intersection(
            set(self.main_path).union(self.alternate_path)
        ):
            raise ValueError("control path must remain disjoint")
        targets = {self.old_target, self.new_target, self.third_target}
        if len(targets) != 3 or not targets.issubset(self.active_unit_ids):
            raise ValueError("relation targets must be distinct active units")
        if targets.intersection(
            set(self.main_path).union(self.alternate_path).union(self.control_path)
        ):
            raise ValueError("relation targets must remain outside core paths")
        if len(self.branch_exposure_counts) != len(self.competition_paths):
            raise ValueError("branch exposures must align with paths")
        if not all(
            left > right
            for left, right in zip(
                self.branch_exposure_counts,
                self.branch_exposure_counts[1:],
                strict=False,
            )
        ):
            raise ValueError("branch exposures must be strictly ordered")
        if self.cue_magnitude <= self.threshold:
            raise ValueError("cue must cross the ordinary Field threshold")
        if len(self.training_lag_profiles_ms) < 3:
            raise ValueError("multiple lag profiles are required")
        if any(len(profile) != 3 for profile in self.training_lag_profiles_ms):
            raise ValueError("each lag profile must describe three edges")
        if len(self.episode_spacings_ms) < 12:
            raise ValueError("development variants require sufficient episode spacing")
        if len(self.contingency_cycle_targets) != len(
            self.contingency_phase_lengths
        ):
            raise ValueError("contingency phases must align")

    @property
    def active_fraction(self) -> float:
        return len(self.active_unit_ids) / self.unit_count

    @property
    def branch_count(self) -> int:
        return len(self.competition_paths)

    @property
    def contingency_change_count(self) -> int:
        return sum(
            left != right
            for left, right in zip(
                self.contingency_cycle_targets,
                self.contingency_cycle_targets[1:],
                strict=False,
            )
        )

    def state_dict(self) -> dict[str, object]:
        return asdict(self)

    def specification_hash(self) -> str:
        encoded = json.dumps(
            self.state_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def _base(
    *,
    family_id: str,
    seed: int,
    threshold: float = 0.5,
    cue_magnitude: float = 1.0,
    training_lags: tuple[tuple[float, float, float], ...] = (
        (5.0, 5.0, 5.0),
        (4.8, 5.2, 5.0),
        (5.2, 4.8, 5.0),
        (5.1, 5.0, 4.9),
    ),
    evaluation_lags: tuple[float, float, float] = (5.0, 5.0, 5.0),
    paths: tuple[
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
    ] = (
        (0, 1, 2, 3),
        (0, 4, 5, 6),
        (7, 8, 9, 10),
        (0, 11, 12, 13),
    ),
    targets: tuple[int, int, int] = (14, 15, 16),
    contingency_targets: tuple[int, ...] = (14, 15, 14),
    contingency_lengths: tuple[int, ...] = (3, 3, 3),
) -> DevelopmentVariantWorld:
    main, alternate, control, third = paths
    value = DevelopmentVariantWorld(
        family_id=family_id,
        seed=seed,
        structural_token=f"development-only:{family_id}:{seed}",
        unit_count=32,
        active_unit_ids=tuple(range(21)),
        distractor_unit_ids=tuple(range(21, 32)),
        main_path=main,
        alternate_path=alternate,
        control_path=control,
        competition_paths=(main, alternate, third),
        old_target=targets[0],
        new_target=targets[1],
        third_target=targets[2],
        main_port=f"port:{family_id}:main",
        control_port=f"port:{family_id}:control",
        training_lag_profiles_ms=training_lags,
        evaluation_lags_ms=evaluation_lags,
        boundary_lag_ms=11.0,
        threshold=threshold,
        cue_magnitude=cue_magnitude,
        relation_reentry_gain=threshold / 0.60,
        episode_spacings_ms=(
            92.0,
            87.0,
            95.0,
            89.0,
            94.0,
            91.0,
            96.0,
            88.0,
            93.0,
            90.0,
            97.0,
            86.0,
        ),
        branch_exposure_counts=(6, 5, 4),
        contingency_cycle_targets=contingency_targets,
        contingency_phase_lengths=contingency_lengths,
    )
    value.validate()
    return value


def development_variants() -> tuple[DevelopmentVariantWorld, ...]:
    return (
        _base(
            family_id="development-threshold-high",
            seed=910_001,
            threshold=0.68,
            cue_magnitude=1.18,
        ),
        _base(
            family_id="development-lag-dispersed",
            seed=910_002,
            training_lags=(
                (3.6, 6.4, 4.2),
                (6.1, 3.9, 5.5),
                (4.2, 5.8, 6.0),
                (5.7, 4.5, 3.8),
            ),
            evaluation_lags=(4.9, 5.15, 4.875),
        ),
        _base(
            family_id="development-topology-cycles",
            seed=910_003,
            paths=(
                (5, 1, 17, 3),
                (5, 7, 19, 9),
                (11, 13, 15, 0),
                (5, 2, 4, 6),
            ),
            targets=(8, 10, 12),
            contingency_targets=(8, 10, 8, 12, 10, 8),
            contingency_lengths=(2, 3, 2, 4, 3, 2),
        ),
    )


def _run(
    world: DevelopmentVariantWorld,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    world.validate()
    if condition is ConfirmatoryCondition.PRIMARY:
        return run_primary(world)  # type: ignore[arg-type]
    if condition in _CONTROLS:
        return run_control(world, condition)  # type: ignore[arg-type]
    if condition in _COMPARATORS:
        return run_comparator(world, condition)  # type: ignore[arg-type]
    raise AssertionError(condition)


@pytest.mark.parametrize("world", development_variants(), ids=lambda row: row.family_id)
def test_all_eight_adapters_execute_each_development_perturbation(
    world: DevelopmentVariantWorld,
) -> None:
    executions = {
        condition: _run(world, condition) for condition in ConfirmatoryCondition
    }
    assert set(executions) == set(ConfirmatoryCondition)
    for condition, execution in executions.items():
        execution.validate()
        assert execution.condition is condition
        assert execution.world_specification_hash == world.specification_hash()
        assert len(execution.records) == len(EvidenceDomain)
        assert {row.evidence_domain for row in execution.records} == set(
            EvidenceDomain
        )
        assert all(
            math.isfinite(value)
            for row in execution.records
            for _, value in row.metrics
        )
        assert execution.resource.observed_training_events >= 0
        assert execution.resource.generated_internal_events >= 0
        assert execution.resource.wall_clock_ms >= 0.0


@pytest.mark.parametrize("world", development_variants(), ids=lambda row: row.family_id)
def test_development_perturbation_semantic_replay_is_deterministic(
    world: DevelopmentVariantWorld,
) -> None:
    first = {
        condition: _run(world, condition) for condition in ConfirmatoryCondition
    }
    second = {
        condition: _run(world, condition) for condition in ConfirmatoryCondition
    }
    for condition in ConfirmatoryCondition:
        assert first[condition].records == second[condition].records
        assert first[condition].semantic_hash == second[condition].semantic_hash
        assert (
            first[condition].world_specification_hash
            == second[condition].world_specification_hash
        )


def test_variants_are_disjoint_from_all_heldout_seed_ranges() -> None:
    worlds = development_variants()
    assert len({row.specification_hash() for row in worlds}) == len(worlds)
    for world in worlds:
        assert world.structural_token.startswith("development-only:")
        assert not 100 <= world.seed <= 109
        assert not 1000 <= world.seed <= 1009
