from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from .formal_revision import FORMAL_GENERATOR_REVISION
from .worlds import CX01Family, CX01World, build_development_grid

COMPONENT_AUDIT_POLICY_VERSION = "cx01-component-structural-audit-v1"
STRUCTURAL_AXES = (
    "topology",
    "timing",
    "exposure_schedule",
    "contingency",
)
ALL_AXES = (*STRUCTURAL_AXES, "token_assignment", "full")

_REQUIRED_SEED_DIVERSITY: dict[CX01Family, tuple[str, ...]] = {
    CX01Family.HIGH_ORDER: (
        "topology",
        "timing",
        "exposure_schedule",
        "token_assignment",
    ),
    CX01Family.TIMING: (
        "topology",
        "timing",
        "exposure_schedule",
        "token_assignment",
    ),
    CX01Family.CYCLE: (
        "topology",
        "timing",
        "exposure_schedule",
        "contingency",
        "token_assignment",
    ),
    CX01Family.BRANCH: (
        "topology",
        "timing",
        "exposure_schedule",
        "contingency",
        "token_assignment",
    ),
    CX01Family.SELECTIVITY: (
        "topology",
        "timing",
        "exposure_schedule",
        "token_assignment",
    ),
    CX01Family.LOOP: (
        "topology",
        "timing",
        "exposure_schedule",
        "contingency",
        "token_assignment",
    ),
}


class _CanonicalTokens:
    def __init__(self) -> None:
        self._mapping: dict[str, str] = {}

    def token(self, value: str | None) -> str | None:
        if value is None:
            return None
        if value not in self._mapping:
            self._mapping[value] = f"t{len(self._mapping)}"
        return self._mapping[value]


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _topology_state(world: CX01World) -> dict[str, Any]:
    canonical = _CanonicalTokens()
    training = [
        [canonical.token(token) for token in row.tokens]
        for row in world.training
    ]
    probes = [
        {
            "prefix": [canonical.token(token) for token in probe.prefix],
            "targets": sorted(
                canonical.token(target)
                for target, _ in probe.expected_distribution
            ),
        }
        for probe in world.probes
    ]
    cycle_cue = canonical.token(world.cycle_cue)
    cycle_targets = sorted(
        {
            canonical.token(phase.target)
            for phase in world.cycle_phases
        }
    )
    intervention_main = [
        canonical.token(token)
        for token in world.intervention_main
    ]
    intervention_control = [
        canonical.token(token)
        for token in world.intervention_control
    ]
    loop = None
    if world.loop is not None:
        loop = {
            "cue_prefix": [
                canonical.token(token)
                for token in world.loop.cue_prefix
            ],
            "expected_generated": canonical.token(
                world.loop.expected_generated
            ),
            "external_consequence": canonical.token(
                world.loop.external_consequence
            ),
        }
    return {
        "cycle_cue": cycle_cue,
        "cycle_target_set": cycle_targets,
        "family": world.family.value,
        "intervention_control": intervention_control,
        "intervention_main": intervention_main,
        "loop": loop,
        "probes": probes,
        "training": training,
    }


def _timing_state(world: CX01World) -> dict[str, Any]:
    return {
        "family": world.family.value,
        "probe_lags_ms": [list(probe.lags_ms) for probe in world.probes],
        "training_lags_ms": [list(row.lags_ms) for row in world.training],
    }


def _exposure_schedule_state(world: CX01World) -> dict[str, Any]:
    return {
        "cycle_phase_exposures": [
            phase.exposures
            for phase in world.cycle_phases
        ],
        "family": world.family.value,
        "training_exposures": [row.exposures for row in world.training],
    }


def _integer_ratio(values: tuple[int, ...]) -> tuple[int, ...]:
    divisor = 0
    for value in values:
        divisor = math.gcd(divisor, value)
    if divisor == 0:
        return values
    return tuple(value // divisor for value in values)


def _contingency_state(world: CX01World) -> dict[str, Any]:
    if world.family is CX01Family.CYCLE:
        canonical = _CanonicalTokens()
        canonical.token(world.cycle_cue)
        schedule = [
            canonical.token(phase.target)
            for phase in world.cycle_phases
        ]
        return {
            "applicable": True,
            "family": world.family.value,
            "phase_target_schedule": schedule,
        }

    if world.family is CX01Family.BRANCH:
        ratio = _integer_ratio(
            tuple(row.exposures for row in world.training)
        )
        return {
            "applicable": True,
            "branch_ratio": sorted(ratio, reverse=True),
            "family": world.family.value,
        }

    if world.family is CX01Family.LOOP:
        if world.loop is None:
            raise RuntimeError("loop family requires a loop specification")
        sequence_lengths = [len(row.tokens) for row in world.training]
        return {
            "applicable": True,
            "cue_length": len(world.loop.cue_prefix),
            "family": world.family.value,
            "sequence_lengths": sequence_lengths,
        }

    return {
        "applicable": False,
        "family": world.family.value,
    }


def _raw_token_assignment_state(world: CX01World) -> dict[str, Any]:
    values: list[str | None] = []
    for row in world.training:
        values.extend(row.tokens)
    for probe in world.probes:
        values.extend(probe.prefix)
        values.extend(target for target, _ in probe.expected_distribution)
    values.append(world.cycle_cue)
    values.extend(phase.target for phase in world.cycle_phases)
    values.extend(world.intervention_main)
    values.extend(world.intervention_control)
    if world.loop is not None:
        values.extend(world.loop.cue_prefix)
        values.append(world.loop.expected_generated)
        values.append(world.loop.external_consequence)
    return {
        "family": world.family.value,
        "tokens": values,
    }


def structural_component_states(world: CX01World) -> dict[str, Any]:
    world.validate()
    topology = _topology_state(world)
    timing = _timing_state(world)
    exposure_schedule = _exposure_schedule_state(world)
    contingency = _contingency_state(world)
    token_assignment = _raw_token_assignment_state(world)
    return {
        "contingency": contingency,
        "exposure_schedule": exposure_schedule,
        "full": {
            "contingency": contingency,
            "exposure_schedule": exposure_schedule,
            "family": world.family.value,
            "timing": timing,
            "topology": topology,
        },
        "timing": timing,
        "token_assignment": token_assignment,
        "topology": topology,
    }


def structural_component_signatures(world: CX01World) -> dict[str, str]:
    states = structural_component_states(world)
    return {
        axis: _digest(states[axis])
        for axis in ALL_AXES
    }


def development_component_signatures() -> dict[
    CX01Family,
    dict[str, frozenset[str]],
]:
    grouped: dict[CX01Family, dict[str, set[str]]] = {
        family: {axis: set() for axis in ALL_AXES}
        for family in CX01Family
    }
    for world in build_development_grid():
        signatures = structural_component_signatures(world)
        for axis, signature in signatures.items():
            grouped[world.family][axis].add(signature)
    return {
        family: {
            axis: frozenset(signatures)
            for axis, signatures in axes.items()
        }
        for family, axes in grouped.items()
    }


def component_structural_report(
    worlds: Iterable[CX01World],
) -> dict[str, Any]:
    selected = tuple(worlds)
    if not selected:
        raise ValueError("component structural audit requires worlds")

    grouped: dict[CX01Family, list[CX01World]] = defaultdict(list)
    for world in selected:
        world.validate()
        grouped[world.family].append(world)

    development = development_component_signatures()
    family_rows: dict[str, Any] = {}
    world_rows: list[dict[str, Any]] = []
    violations: list[str] = []

    for family in CX01Family:
        family_worlds = grouped.get(family, [])
        if not family_worlds:
            violations.append(f"missing-family:{family.value}")
            continue

        family_signatures = [
            structural_component_signatures(world)
            for world in family_worlds
        ]
        axis_rows: dict[str, Any] = {}
        for axis in ALL_AXES:
            values = [row[axis] for row in family_signatures]
            unique_values = set(values)
            overlap = unique_values.intersection(development[family][axis])
            novel = unique_values.difference(development[family][axis])
            required_seed_diversity = axis in _REQUIRED_SEED_DIVERSITY[family]
            minimum_unique = 2 if required_seed_diversity else 1
            if axis == "full":
                minimum_unique = min(5, len(family_worlds))
            axis_passed = (
                len(novel) >= 1
                and len(unique_values) >= minimum_unique
            )
            if axis == "full":
                axis_passed = axis_passed and not overlap
            if not axis_passed:
                violations.append(
                    f"axis:{family.value}:{axis}:"
                    f"unique={len(unique_values)}:"
                    f"novel={len(novel)}:"
                    f"overlap={len(overlap)}"
                )
            axis_rows[axis] = {
                "development_overlap_count": len(overlap),
                "formal_novel_count": len(novel),
                "formal_unique_count": len(unique_values),
                "minimum_unique_required": minimum_unique,
                "passed": axis_passed,
                "required_seed_diversity": required_seed_diversity,
            }

        for world, signatures in zip(
            family_worlds,
            family_signatures,
            strict=True,
        ):
            novelty = {
                axis: signatures[axis] not in development[family][axis]
                for axis in STRUCTURAL_AXES
            }
            novelty_count = sum(novelty.values())
            row_passed = (
                signatures["full"] not in development[family]["full"]
                and novelty_count >= 2
            )
            if not row_passed:
                violations.append(
                    f"world:{family.value}:{world.seed}:"
                    f"non-token-novel-axes={novelty_count}"
                )
            world_rows.append(
                {
                    "family": family.value,
                    "full_structure_novel": (
                        signatures["full"]
                        not in development[family]["full"]
                    ),
                    "non_token_novel_axis_count": novelty_count,
                    "novel_vs_development": novelty,
                    "passed": row_passed,
                    "seed": world.seed,
                }
            )

        family_rows[family.value] = {
            "axes": axis_rows,
            "passed": all(row["passed"] for row in axis_rows.values())
            and all(
                row["passed"]
                for row in world_rows
                if row["family"] == family.value
            ),
            "world_count": len(family_worlds),
        }

    return {
        "family_rows": family_rows,
        "formal_generator_revision": FORMAL_GENERATOR_REVISION,
        "passed": not violations,
        "policy_version": COMPONENT_AUDIT_POLICY_VERSION,
        "violations": violations,
        "world_count": len(selected),
        "world_rows": world_rows,
    }


def audit_formal_grid_components(
    worlds: Iterable[CX01World],
) -> dict[str, Any]:
    report = component_structural_report(worlds)
    if not report["passed"]:
        joined = "; ".join(report["violations"][:12])
        raise RuntimeError(
            "formal component structural held-out audit failed: "
            f"{joined}"
        )
    return report
