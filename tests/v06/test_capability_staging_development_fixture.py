from __future__ import annotations

import ast
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

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
from sparkbrain.evaluation.v06_confirmatory_resources import (
    PrivilegedInformation,
)

_DEVELOPMENT_FAMILY = "development-capability-staging"
_DEVELOPMENT_SEED = 900_000
_PRIMARY_AND_CONTROLS = {
    ConfirmatoryCondition.PRIMARY,
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
    ConfirmatoryCondition.SHUFFLED_RELATION,
}
_CONTROLS = _PRIMARY_AND_CONTROLS - {ConfirmatoryCondition.PRIMARY}
_COMPARATORS = {
    ConfirmatoryCondition.G3_RECURRENT,
    ConfirmatoryCondition.G4_ASSEMBLY,
    ConfirmatoryCondition.G5_TYPED,
}


@dataclass(frozen=True, slots=True)
class DevelopmentCapabilityWorld:
    """Duck-typed execution fixture that cannot address candidate confirmatory seeds."""

    family_id: str = _DEVELOPMENT_FAMILY
    seed: int = _DEVELOPMENT_SEED
    structural_token: str = "development-only:capability-staging-900000"
    unit_count: int = 24
    active_unit_ids: tuple[int, ...] = tuple(range(17))
    distractor_unit_ids: tuple[int, ...] = tuple(range(17, 24))
    main_path: tuple[int, int, int, int] = (0, 1, 2, 3)
    alternate_path: tuple[int, int, int, int] = (0, 4, 5, 6)
    control_path: tuple[int, int, int, int] = (7, 8, 9, 10)
    competition_paths: tuple[tuple[int, int, int, int], ...] = (
        (0, 1, 2, 3),
        (0, 4, 5, 6),
        (0, 11, 12, 13),
    )
    old_target: int = 14
    new_target: int = 15
    third_target: int = 16
    main_port: str = "port:development-main"
    control_port: str = "port:development-control"
    training_lag_profiles_ms: tuple[tuple[float, float, float], ...] = (
        (5.0, 5.0, 5.0),
        (4.8, 5.2, 5.0),
        (5.2, 4.8, 5.0),
        (5.1, 5.0, 4.9),
    )
    evaluation_lags_ms: tuple[float, float, float] = (5.0, 5.0, 5.0)
    boundary_lag_ms: float = 10.0
    threshold: float = 0.5
    cue_magnitude: float = 1.0
    relation_reentry_gain: float = 0.5 / 0.60
    episode_spacings_ms: tuple[float, ...] = (
        80.0,
        82.0,
        79.0,
        84.0,
        81.0,
        83.0,
        80.0,
        85.0,
        78.0,
        82.0,
        81.0,
        84.0,
    )
    branch_exposure_counts: tuple[int, ...] = (6, 5, 4)
    contingency_cycle_targets: tuple[int, ...] = (14, 15, 14)
    contingency_phase_lengths: tuple[int, ...] = (3, 3, 3)

    def validate(self) -> None:
        if self.family_id != _DEVELOPMENT_FAMILY:
            raise ValueError("development capability fixture has the wrong family")
        if self.seed != _DEVELOPMENT_SEED:
            raise ValueError("development capability fixture has the wrong seed")
        if not self.structural_token.startswith("development-only:"):
            raise ValueError("development fixture cannot use a confirmatory token")
        if 100 <= self.seed <= 109 or 1000 <= self.seed <= 1009:
            raise ValueError("development fixture cannot address held-out seed ranges")
        if self.unit_count != 24:
            raise ValueError("development fixture unit count changed unexpectedly")
        if set(self.active_unit_ids).intersection(self.distractor_unit_ids):
            raise ValueError("active and distractor units must be disjoint")
        if len(set(self.competition_paths)) != 3:
            raise ValueError("development branch fixture must preserve three paths")
        if {path[0] for path in self.competition_paths} != {self.main_path[0]}:
            raise ValueError("development branches must share one root")
        if self.branch_exposure_counts != (6, 5, 4):
            raise ValueError("development branch exposures changed unexpectedly")
        if self.cue_magnitude <= self.threshold:
            raise ValueError("development cue must cross the ordinary Field threshold")
        if len(self.training_lag_profiles_ms) < 3:
            raise ValueError("development timing fixture requires multiple profiles")
        if len(self.episode_spacings_ms) < 9:
            raise ValueError("development fixture requires sufficient episode spacings")
        if len(self.contingency_cycle_targets) != len(self.contingency_phase_lengths):
            raise ValueError("development contingency phases are misaligned")

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


def _run(
    world: DevelopmentCapabilityWorld,
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


@pytest.fixture(scope="module")
def world() -> DevelopmentCapabilityWorld:
    value = DevelopmentCapabilityWorld()
    value.validate()
    return value


@pytest.fixture(scope="module")
def executions(
    world: DevelopmentCapabilityWorld,
) -> dict[ConfirmatoryCondition, HeldoutConditionExecution]:
    return {condition: _run(world, condition) for condition in ConfirmatoryCondition}


def test_fixture_is_explicitly_development_only(world: DevelopmentCapabilityWorld) -> None:
    assert world.family_id == _DEVELOPMENT_FAMILY
    assert world.seed == 900_000
    assert world.structural_token.startswith("development-only:")
    assert not 100 <= world.seed <= 109
    assert not 1000 <= world.seed <= 1009
    assert world.branch_count == 3
    assert world.contingency_change_count == 2


def test_all_eight_real_adapters_emit_complete_payloads(
    world: DevelopmentCapabilityWorld,
    executions: dict[ConfirmatoryCondition, HeldoutConditionExecution],
) -> None:
    assert set(executions) == set(ConfirmatoryCondition)
    for condition, execution in executions.items():
        execution.validate()
        assert execution.condition is condition
        assert execution.family_id == world.family_id
        assert execution.seed == world.seed
        assert execution.world_specification_hash == world.specification_hash()
        assert len(execution.records) == len(EvidenceDomain)
        assert {row.evidence_domain for row in execution.records} == set(EvidenceDomain)
        assert all(row.family_id == world.family_id for row in execution.records)
        assert all(row.seed == world.seed for row in execution.records)
        assert all(row.condition is condition for row in execution.records)
        assert all(
            math.isfinite(value)
            for row in execution.records
            for _, value in row.metrics
        )
        assert len(execution.semantic_hash) == 64


def test_resource_emitters_match_each_architectural_contract(
    executions: dict[ConfirmatoryCondition, HeldoutConditionExecution],
) -> None:
    for condition in _PRIMARY_AND_CONTROLS:
        resource = executions[condition].resource
        assert resource.normal_field_threshold_present is True
        assert resource.threshold_bypassed is False
        assert resource.explicit_assembly_entries == 0
        assert resource.typed_head_count == 0
        assert resource.scalar_reward_observations == 0
        assert resource.privileged_information == ()

    g3 = executions[ConfirmatoryCondition.G3_RECURRENT].resource
    assert g3.normal_field_threshold_present is False
    assert g3.threshold_bypassed is True
    assert g3.privileged_information == ()

    g4 = executions[ConfirmatoryCondition.G4_ASSEMBLY].resource
    assert g4.normal_field_threshold_present is False
    assert g4.threshold_bypassed is True
    assert g4.explicit_assembly_entries >= 1
    assert g4.privileged_information == (
        PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
    )

    g5 = executions[ConfirmatoryCondition.G5_TYPED].resource
    assert g5.normal_field_threshold_present is False
    assert g5.threshold_bypassed is True
    assert g5.typed_head_count >= 3
    assert g5.scalar_reward_observations >= 1
    assert set(g5.privileged_information) == {
        PrivilegedInformation.TYPED_PREDICTION_HEAD,
        PrivilegedInformation.TYPED_BOUNDARY_HEAD,
        PrivilegedInformation.TYPED_MEMORY_HEAD,
        PrivilegedInformation.SCALAR_REWARD,
    }


def test_semantic_replay_is_deterministic_for_all_eight_adapters(
    world: DevelopmentCapabilityWorld,
    executions: dict[ConfirmatoryCondition, HeldoutConditionExecution],
) -> None:
    replay = {condition: _run(world, condition) for condition in ConfirmatoryCondition}
    for condition in ConfirmatoryCondition:
        first = executions[condition]
        second = replay[condition]
        assert first.records == second.records
        assert first.semantic_hash == second.semantic_hash
        assert first.world_specification_hash == second.world_specification_hash
        assert first.resource.wall_clock_ms >= 0.0
        assert second.resource.wall_clock_ms >= 0.0


def test_development_fixture_test_imports_no_candidate_world_builder() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_modules = {
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert not any(
        module.endswith("v06_confirmatory_heldout_spec")
        for module in imported_modules
    )
    assert {
        "HELDOUT_SEEDS",
        "WORLD_GENERATION_ID",
        "build_heldout_world_grid",
        "heldout_world_parameters",
    }.isdisjoint(imported_names)
