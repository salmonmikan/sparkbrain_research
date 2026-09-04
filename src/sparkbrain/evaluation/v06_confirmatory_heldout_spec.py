from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from typing import Any

WORLD_GENERATION_ID = "v06-confirmatory-candidate-002"
QUARANTINED_HELDOUT_SEEDS = tuple(range(100, 110))
HELDOUT_FAMILIES = (
    "heldout-sparse-permutation",
    "heldout-lag-dispersion",
    "heldout-threshold-band",
    "heldout-branch-competition",
    "heldout-contingency-cycles",
)
HELDOUT_SEEDS = tuple(range(1000, 1010))


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class HeldoutWorldParameters:
    """Pure shared data contract for one candidate confirmatory world.

    The contract contains execution-level structure only. It imports no
    capability adapter and contains no correct condition, reward, semantic role,
    evaluator-selected winner, or observed capability result.
    """

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
        if self.family_id not in HELDOUT_FAMILIES:
            raise ValueError("unknown held-out world family")
        if self.seed not in HELDOUT_SEEDS:
            raise ValueError("unsupported held-out seed")
        if self.seed in QUARANTINED_HELDOUT_SEEDS:
            raise ValueError("quarantined held-out seed cannot enter candidate grid")
        if not self.structural_token.startswith(f"{WORLD_GENERATION_ID}:"):
            raise ValueError("structural token must identify the fresh world generation")
        if self.unit_count < 16:
            raise ValueError("held-out worlds require at least 16 units")
        if len(set(self.active_unit_ids)) != len(self.active_unit_ids):
            raise ValueError("active unit IDs must be unique")
        if len(set(self.distractor_unit_ids)) != len(self.distractor_unit_ids):
            raise ValueError("distractor unit IDs must be unique")
        if set(self.active_unit_ids).intersection(self.distractor_unit_ids):
            raise ValueError("active and distractor units must be disjoint")
        all_ids = set(self.active_unit_ids).union(self.distractor_unit_ids)
        if not all(0 <= unit_id < self.unit_count for unit_id in all_ids):
            raise ValueError("unit IDs must fit the declared unit_count")

        paths = (
            self.main_path,
            self.alternate_path,
            self.control_path,
            *self.competition_paths,
        )
        if any(len(path) != 4 for path in paths):
            raise ValueError("every held-out path must contain four units")
        if any(len(set(path)) != len(path) for path in paths):
            raise ValueError("a path cannot repeat a unit")
        if any(not set(path).issubset(self.active_unit_ids) for path in paths):
            raise ValueError("all path units must be active")
        if self.main_path[0] != self.alternate_path[0]:
            raise ValueError("main and alternate paths must share the current cue")
        if set(self.control_path).intersection(
            set(self.main_path).union(self.alternate_path)
        ):
            raise ValueError("control path must be disjoint from main/alternate paths")
        if len(set(self.competition_paths)) != len(self.competition_paths):
            raise ValueError("competition paths must be unique")
        if any(path[0] != self.main_path[0] for path in self.competition_paths):
            raise ValueError("competition paths must share the main cue")

        targets = {self.old_target, self.new_target, self.third_target}
        if len(targets) != 3:
            raise ValueError("external relation targets must be distinct")
        if not targets.issubset(self.active_unit_ids):
            raise ValueError("external relation targets must be active units")
        if targets.intersection(
            set(self.main_path).union(self.alternate_path).union(self.control_path)
        ):
            raise ValueError("external targets must be separate from chain paths")
        if not self.main_port or not self.control_port:
            raise ValueError("boundary ports must be non-empty")
        if self.main_port == self.control_port:
            raise ValueError("main and control ports must be distinct")

        if len(self.training_lag_profiles_ms) < 3:
            raise ValueError("at least three training lag profiles are required")
        if any(len(profile) != 3 for profile in self.training_lag_profiles_ms):
            raise ValueError("each lag profile must contain three edge lags")
        lag_values = (
            *self.evaluation_lags_ms,
            *(
                lag
                for profile in self.training_lag_profiles_ms
                for lag in profile
            ),
            self.boundary_lag_ms,
        )
        if any(not math.isfinite(lag) or lag <= 0 for lag in lag_values):
            raise ValueError("all lags must be positive and finite")
        for name in ("threshold", "cue_magnitude", "relation_reentry_gain"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be positive and finite")
        if self.cue_magnitude <= self.threshold:
            raise ValueError("cue magnitude must cross the ordinary Field threshold")
        if len(self.episode_spacings_ms) < 9:
            raise ValueError("held-out worlds require at least nine episode spacings")
        if any(
            not math.isfinite(value) or value <= 0
            for value in self.episode_spacings_ms
        ):
            raise ValueError("episode spacings must be positive and finite")
        if len(self.branch_exposure_counts) != len(self.competition_paths):
            raise ValueError("each competition path requires one exposure count")
        if any(value < 1 for value in self.branch_exposure_counts):
            raise ValueError("branch exposure counts must be positive")
        if not self.contingency_cycle_targets:
            raise ValueError("at least one contingency target is required")
        if len(self.contingency_cycle_targets) != len(
            self.contingency_phase_lengths
        ):
            raise ValueError("contingency targets and phase lengths must align")
        if not set(self.contingency_cycle_targets).issubset(targets):
            raise ValueError("contingency cycles may use only declared targets")
        if any(value < 1 for value in self.contingency_phase_lengths):
            raise ValueError("contingency phase lengths must be positive")

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

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def specification_hash(self) -> str:
        return _digest(self.state_dict())


def _lag_profile(
    base: tuple[float, float, float],
    offsets: tuple[float, float, float],
) -> tuple[float, float, float]:
    return tuple(
        round(max(0.5, value + offset), 6)
        for value, offset in zip(base, offsets, strict=True)
    )


def _seed_index(seed: int) -> int:
    try:
        return HELDOUT_SEEDS.index(seed)
    except ValueError as exc:
        raise ValueError(f"unsupported held-out seed: {seed}") from exc


def heldout_world_parameters(
    family_id: str,
    seed: int,
) -> HeldoutWorldParameters:
    """Generate one deterministic, outcome-unopened world specification."""

    if family_id not in HELDOUT_FAMILIES:
        raise ValueError(f"unknown held-out world family: {family_id}")
    seed_index = _seed_index(seed)
    rng_seed = int(
        _digest(
            {
                "family_id": family_id,
                "generation": WORLD_GENERATION_ID,
                "seed": seed,
            }
        )[:16],
        16,
    )
    rng = random.Random(rng_seed)
    unit_count = 64
    roles = list(range(unit_count))
    rng.shuffle(roles)

    main_path = tuple(roles[0:4])
    alternate_path = (roles[0], roles[4], roles[5], roles[6])
    control_path = tuple(roles[7:11])
    branch_three = (roles[0], roles[14], roles[15], roles[16])
    old_target, new_target, third_target = roles[11:14]
    core_active = {
        *main_path,
        *alternate_path,
        *control_path,
        *branch_three,
        old_target,
        new_target,
        third_target,
    }

    base_lags = (
        round(3.60 + rng.random() * 2.8, 6),
        round(4.05 + rng.random() * 3.2, 6),
        round(3.35 + rng.random() * 3.8, 6),
    )
    profiles = tuple(
        _lag_profile(
            base_lags,
            (
                rng.uniform(-0.90, 0.90),
                rng.uniform(-1.15, 1.15),
                rng.uniform(-0.75, 0.75),
            ),
        )
        for _ in range(5)
    )
    evaluation_lags = tuple(
        round(sum(profile[index] for profile in profiles) / len(profiles), 6)
        for index in range(3)
    )
    threshold = round(0.395 + rng.random() * 0.25, 6)
    cue_magnitude = round(threshold + 0.31 + rng.random() * 0.19, 6)
    boundary_lag = round(7.25 + rng.random() * 8.5, 6)
    spacings = tuple(
        round(
            max(
                58.0,
                sum(evaluation_lags) + boundary_lag + 22.0,
            )
            + rng.uniform(0.0, 20.0),
            6,
        )
        for _ in range(12)
    )
    main_port = f"port:{700 + roles[17]}"
    control_port = f"port:{900 + roles[18]}"
    competition_paths = (main_path, alternate_path)
    branch_counts = (5, 4)
    contingency_targets = (
        old_target,
        new_target,
        old_target,
    )
    contingency_lengths = (3, 3, 3)

    if family_id == "heldout-sparse-permutation":
        active_extra = tuple(roles[19:25])
        active_ids = tuple(sorted(core_active.union(active_extra)))
        distractors = tuple(sorted(roles[25:33]))
    elif family_id == "heldout-lag-dispersion":
        active_ids = tuple(sorted(core_active.union(roles[19:31])))
        distractors = tuple(sorted(roles[31:41]))
        profiles = tuple(
            _lag_profile(
                base_lags,
                (
                    (-1.45, 0.65, 1.75)[index % 3]
                    + rng.uniform(-0.28, 0.28),
                    (1.35, -1.15, 0.85)[index % 3]
                    + rng.uniform(-0.28, 0.28),
                    (0.95, 1.65, -1.35)[index % 3]
                    + rng.uniform(-0.28, 0.28),
                ),
            )
            for index in range(6)
        )
        evaluation_lags = tuple(
            round(sum(profile[index] for profile in profiles) / len(profiles), 6)
            for index in range(3)
        )
        spacings = tuple(
            round(
                max(60.0, sum(profile) + boundary_lag + 22.0)
                + rng.uniform(0.0, 32.0),
                6,
            )
            for profile in (profiles * 2)[:12]
        )
    elif family_id == "heldout-threshold-band":
        active_ids = tuple(sorted(core_active.union(roles[19:31])))
        distractors = tuple(sorted(roles[31:41]))
        threshold = round(0.34 + seed_index * 0.038, 6)
        cue_magnitude = round(
            threshold + 0.28 + (seed_index % 3) * 0.035,
            6,
        )
    elif family_id == "heldout-branch-competition":
        active_ids = tuple(sorted(core_active.union(roles[19:35])))
        distractors = tuple(sorted(roles[35:47]))
        competition_paths = (main_path, alternate_path, branch_three)
        strongest = 6 + (seed_index % 2)
        branch_counts = (strongest, strongest - 1, strongest - 2)
    else:
        active_ids = tuple(sorted(core_active.union(roles[19:31])))
        distractors = tuple(sorted(roles[31:41]))
        contingency_targets = (
            old_target,
            new_target,
            old_target,
            third_target,
            new_target,
            old_target,
        )
        contingency_lengths = tuple(
            2 + ((seed_index + index) % 3) for index in range(6)
        )

    parameters = HeldoutWorldParameters(
        family_id=family_id,
        seed=seed,
        structural_token=f"{WORLD_GENERATION_ID}:{seed}",
        unit_count=unit_count,
        active_unit_ids=active_ids,
        distractor_unit_ids=distractors,
        main_path=main_path,
        alternate_path=alternate_path,
        control_path=control_path,
        competition_paths=competition_paths,
        old_target=old_target,
        new_target=new_target,
        third_target=third_target,
        main_port=main_port,
        control_port=control_port,
        training_lag_profiles_ms=profiles,
        evaluation_lags_ms=evaluation_lags,
        boundary_lag_ms=boundary_lag,
        threshold=threshold,
        cue_magnitude=cue_magnitude,
        relation_reentry_gain=threshold / 0.60,
        episode_spacings_ms=spacings,
        branch_exposure_counts=branch_counts,
        contingency_cycle_targets=contingency_targets,
        contingency_phase_lengths=contingency_lengths,
    )
    parameters.validate()
    return parameters


def build_heldout_world_grid() -> tuple[HeldoutWorldParameters, ...]:
    return tuple(
        heldout_world_parameters(family_id, seed)
        for family_id in HELDOUT_FAMILIES
        for seed in HELDOUT_SEEDS
    )


def heldout_world_grid_hash() -> str:
    return _digest(
        {
            "generation": WORLD_GENERATION_ID,
            "worlds": [row.state_dict() for row in build_heldout_world_grid()],
        }
    )
