from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class DiagnosticWorld:
    """Development-only world contract for mechanistic diagnosis.

    The shape intentionally matches the Primary adapter's read-only world
    interface, but the family, seed, and structural token cannot address a
    confirmatory candidate. These worlds are interventions on input structure,
    not replacements for a held-out capability programme.
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
    factor_name: str
    factor_value: str

    def validate(self) -> None:
        if not self.family_id.startswith("diagnostic-"):
            raise ValueError("diagnostic family must use diagnostic-* namespace")
        if not self.structural_token.startswith("development-only:diagnostic:"):
            raise ValueError("diagnostic world must remain development-only")
        if self.seed < 900_000:
            raise ValueError("diagnostic seeds must remain outside held-out ranges")
        if self.unit_count < 20:
            raise ValueError("diagnostic world requires at least 20 units")
        if not self.factor_name or not self.factor_value:
            raise ValueError("diagnostic factor identity must be explicit")
        active = set(self.active_unit_ids)
        distractors = set(self.distractor_unit_ids)
        if active.intersection(distractors):
            raise ValueError("active and distractor units must be disjoint")
        if not active.union(distractors).issubset(range(self.unit_count)):
            raise ValueError("diagnostic unit IDs must fit unit_count")
        paths = (
            self.main_path,
            self.alternate_path,
            self.control_path,
            *self.competition_paths,
        )
        if any(len(path) != 4 or len(set(path)) != 4 for path in paths):
            raise ValueError("diagnostic paths must contain four unique units")
        if any(not set(path).issubset(active) for path in paths):
            raise ValueError("diagnostic path units must be active")
        if set(self.control_path).intersection(
            set(self.main_path).union(self.alternate_path)
        ):
            raise ValueError("diagnostic control path must be disjoint")
        targets = {self.old_target, self.new_target, self.third_target}
        if len(targets) != 3 or not targets.issubset(active):
            raise ValueError("diagnostic relation targets must be distinct active units")
        if targets.intersection(
            set(self.main_path).union(self.alternate_path).union(self.control_path)
        ):
            raise ValueError("diagnostic relation targets must be outside core paths")
        if len(self.branch_exposure_counts) != len(self.competition_paths):
            raise ValueError("one exposure count is required per competition path")
        if any(count < 1 for count in self.branch_exposure_counts):
            raise ValueError("diagnostic exposure counts must be positive")
        if len(self.training_lag_profiles_ms) < 2:
            raise ValueError("diagnostic world requires multiple lag profiles")
        if any(len(profile) != 3 for profile in self.training_lag_profiles_ms):
            raise ValueError("each lag profile must contain three edge lags")
        values = (
            *self.evaluation_lags_ms,
            *(lag for profile in self.training_lag_profiles_ms for lag in profile),
            self.boundary_lag_ms,
            self.threshold,
            self.cue_magnitude,
            self.relation_reentry_gain,
            *self.episode_spacings_ms,
        )
        if any(not math.isfinite(float(value)) or value <= 0 for value in values):
            raise ValueError("diagnostic timing and magnitude values must be positive")
        if self.cue_magnitude <= self.threshold:
            raise ValueError("diagnostic cue must cross ordinary Field threshold")
        if len(self.episode_spacings_ms) < 18:
            raise ValueError("diagnostic relation cycles need at least 18 spacings")
        if len(self.contingency_cycle_targets) != len(
            self.contingency_phase_lengths
        ):
            raise ValueError("diagnostic contingency phases must align")
        if any(length < 1 for length in self.contingency_phase_lengths):
            raise ValueError("diagnostic phase lengths must be positive")
        if not set(self.contingency_cycle_targets).issubset(targets):
            raise ValueError("diagnostic contingency targets must be declared targets")

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
        encoded = json.dumps(
            self.state_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def _evaluation_lags(
    profiles: tuple[tuple[float, float, float], ...],
) -> tuple[float, float, float]:
    return tuple(
        sum(profile[index] for profile in profiles) / len(profiles)
        for index in range(3)
    )


def _base_world(
    *,
    family_id: str,
    seed: int,
    factor_name: str,
    factor_value: str,
    profiles: tuple[tuple[float, float, float], ...],
    exposure_counts: tuple[int, int] = (5, 4),
    alternate_root_shared: bool = True,
    contingency_targets: tuple[int, ...] = (14, 15, 14),
    contingency_lengths: tuple[int, ...] = (3, 3, 3),
) -> DiagnosticWorld:
    main_path = (0, 1, 2, 3)
    alternate_path = (
        (0, 4, 5, 6) if alternate_root_shared else (11, 4, 5, 6)
    )
    control_path = (7, 8, 9, 10)
    active = tuple(range(17))
    world = DiagnosticWorld(
        family_id=family_id,
        seed=seed,
        structural_token=f"development-only:diagnostic:{family_id}:{seed}",
        unit_count=32,
        active_unit_ids=active,
        distractor_unit_ids=tuple(range(17, 32)),
        main_path=main_path,
        alternate_path=alternate_path,
        control_path=control_path,
        competition_paths=(main_path, alternate_path),
        old_target=14,
        new_target=15,
        third_target=16,
        main_port=f"port:{family_id}:main",
        control_port=f"port:{family_id}:control",
        training_lag_profiles_ms=profiles,
        evaluation_lags_ms=_evaluation_lags(profiles),
        boundary_lag_ms=10.0,
        threshold=0.5,
        cue_magnitude=1.0,
        relation_reentry_gain=0.5 / 0.60,
        episode_spacings_ms=tuple(90.0 + (index % 5) for index in range(24)),
        branch_exposure_counts=exposure_counts,
        contingency_cycle_targets=contingency_targets,
        contingency_phase_lengths=contingency_lengths,
        factor_name=factor_name,
        factor_value=factor_value,
    )
    world.validate()
    return world


def _profiles_from_first_edges(
    first_edges: tuple[float, float, float, float, float, float],
) -> tuple[tuple[float, float, float], ...]:
    return tuple((value, 5.0, 5.0) for value in first_edges)


def lag_factor_worlds() -> tuple[DiagnosticWorld, ...]:
    """One-factor development worlds for D2/D3 trajectory diagnosis."""

    worlds: list[DiagnosticWorld] = []
    narrow = _profiles_from_first_edges((4.9, 5.0, 5.1, 4.95, 5.05, 5.0))
    worlds.append(
        _base_world(
            family_id="diagnostic-lag-narrow-shared",
            seed=930_000,
            factor_name="lag-variance",
            factor_value="narrow-symmetric",
            profiles=narrow,
        )
    )

    resonant = _profiles_from_first_edges((3.0, 5.0, 5.0, 5.0, 5.05, 7.0))
    worlds.append(
        _base_world(
            family_id="diagnostic-lag-resonant-shared",
            seed=930_001,
            factor_name="profile-path-assignment",
            factor_value="main-bimodal-alternate-narrow",
            profiles=resonant,
        )
    )
    worlds.append(
        _base_world(
            family_id="diagnostic-lag-resonant-separated",
            seed=930_002,
            factor_name="shared-root-competition",
            factor_value="disabled",
            profiles=resonant,
            alternate_root_shared=False,
        )
    )

    swapped = _profiles_from_first_edges((5.0, 3.0, 5.0, 5.0, 7.0, 5.05))
    worlds.append(
        _base_world(
            family_id="diagnostic-lag-assignment-swapped",
            seed=930_003,
            factor_name="profile-path-assignment",
            factor_value="main-narrow-alternate-bimodal",
            profiles=swapped,
        )
    )

    for index, delta in enumerate((0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)):
        profiles = _profiles_from_first_edges(
            (5.0 - delta, 5.0, 5.0, 5.0, 5.02, 5.0 + delta)
        )
        worlds.append(
            _base_world(
                family_id=f"diagnostic-lag-main-variance-{index}",
                seed=930_100 + index,
                factor_name="main-first-edge-mode-separation",
                factor_value=f"{2.0 * delta:.3f}ms",
                profiles=profiles,
            )
        )

    for index, counts in enumerate(((4, 4), (5, 4), (6, 4), (4, 5))):
        worlds.append(
            _base_world(
                family_id=f"diagnostic-lag-exposure-{counts[0]}-{counts[1]}",
                seed=930_200 + index,
                factor_name="branch-exposure-counts",
                factor_value=f"main={counts[0]},alternate={counts[1]}",
                profiles=resonant,
                exposure_counts=counts,
            )
        )

    for rotation in range(6):
        profiles = resonant[rotation:] + resonant[:rotation]
        worlds.append(
            _base_world(
                family_id=f"diagnostic-lag-profile-rotation-{rotation}",
                seed=930_300 + rotation,
                factor_name="lag-profile-phase-rotation",
                factor_value=str(rotation),
                profiles=profiles,
            )
        )

    return tuple(worlds)


def relation_factor_worlds() -> tuple[DiagnosticWorld, ...]:
    """Development-only worlds isolating storage and expression regimes."""

    profiles = _profiles_from_first_edges((5.0, 5.05, 4.95, 5.0, 5.02, 4.98))
    targets = (14, 15, 14, 16, 15, 14)
    patterns = (
        ("expression-abstention", (2, 3, 4, 2, 3, 4)),
        ("hysteresis-short-return", (3, 4, 2, 3, 4, 2)),
        ("parallel-link-superposition", (4, 2, 3, 4, 2, 3)),
    )
    return tuple(
        _base_world(
            family_id=f"diagnostic-relation-{name}",
            seed=931_000 + index,
            factor_name="contingency-phase-length-pattern",
            factor_value=name,
            profiles=profiles,
            contingency_targets=targets,
            contingency_lengths=lengths,
        )
        for index, (name, lengths) in enumerate(patterns)
    )


def with_profiles(
    world: DiagnosticWorld,
    profiles: tuple[tuple[float, float, float], ...],
    *,
    family_suffix: str,
    seed: int,
    factor_name: str,
    factor_value: str,
) -> DiagnosticWorld:
    result = replace(
        world,
        family_id=f"diagnostic-{family_suffix}",
        seed=seed,
        structural_token=f"development-only:diagnostic:{family_suffix}:{seed}",
        main_port=f"port:diagnostic-{family_suffix}:main",
        control_port=f"port:diagnostic-{family_suffix}:control",
        training_lag_profiles_ms=profiles,
        evaluation_lags_ms=_evaluation_lags(profiles),
        factor_name=factor_name,
        factor_value=factor_value,
    )
    result.validate()
    return result
