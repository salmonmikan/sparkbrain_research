from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from .worlds import (
    HISTORICALLY_EXPOSED_SEEDS,
    CX01Family,
    CX01World,
    CyclePhase,
    LoopSpec,
    ProbeCase,
    SequenceExposure,
    build_development_grid,
)

FORMAL_STRUCTURE_POLICY_VERSION = "cx01-formal-structure-v2"


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _rng(generation_id: str, family: CX01Family, seed: int) -> random.Random:
    material = {
        "family": family.value,
        "generation_id": generation_id,
        "policy": FORMAL_STRUCTURE_POLICY_VERSION,
        "seed": seed,
    }
    return random.Random(int(_digest(material)[:16], 16))


def _roles(generation_id: str, family: CX01Family, seed: int) -> tuple[str, ...]:
    rng = _rng(generation_id + ":roles", family, seed)
    values = list(range(64))
    rng.shuffle(values)
    return tuple(f"u{value:02d}" for value in values)


def _sequence(
    tokens: tuple[str, ...],
    lags_ms: tuple[float, ...],
    exposures: int,
) -> SequenceExposure:
    row = SequenceExposure(tokens=tokens, lags_ms=lags_ms, exposures=exposures)
    row.validate()
    return row


def _canonical_token_state(world: CX01World) -> dict[str, Any]:
    """Return a token-renaming-invariant description of one CX01 world."""

    token_ids: dict[str, str] = {}

    def token(value: str | None) -> str | None:
        if value is None:
            return None
        if value not in token_ids:
            token_ids[value] = f"t{len(token_ids)}"
        return token_ids[value]

    training = [
        {
            "exposures": row.exposures,
            "lags_ms": list(row.lags_ms),
            "tokens": [token(value) for value in row.tokens],
        }
        for row in world.training
    ]
    probes = [
        {
            "expected_distribution": [
                [token(target), probability]
                for target, probability in probe.expected_distribution
            ],
            "lags_ms": list(probe.lags_ms),
            "prefix": [token(value) for value in probe.prefix],
        }
        for probe in world.probes
    ]
    cycle_phases = [
        {"exposures": phase.exposures, "target": token(phase.target)}
        for phase in world.cycle_phases
    ]
    loop = None
    if world.loop is not None:
        loop = {
            "cue_prefix": [token(value) for value in world.loop.cue_prefix],
            "expected_generated": token(world.loop.expected_generated),
            "external_consequence": token(world.loop.external_consequence),
        }
    return {
        "cycle_cue": token(world.cycle_cue),
        "cycle_phases": cycle_phases,
        "family": world.family.value,
        "intervention_control": [token(value) for value in world.intervention_control],
        "intervention_main": [token(value) for value in world.intervention_main],
        "loop": loop,
        "probes": probes,
        "training": training,
    }


def world_structure_signature(world: CX01World) -> str:
    world.validate()
    return _digest(_canonical_token_state(world))


def development_structure_signatures() -> dict[CX01Family, frozenset[str]]:
    grouped: dict[CX01Family, set[str]] = defaultdict(set)
    for world in build_development_grid():
        grouped[world.family].add(world_structure_signature(world))
    return {family: frozenset(grouped[family]) for family in CX01Family}


def _build_high_order(
    generation_id: str,
    seed: int,
    roles: tuple[str, ...],
    rng: random.Random,
) -> CX01World:
    unique_depth = rng.choice((2, 3))
    left_unique = roles[:unique_depth]
    right_unique = roles[8 : 8 + unique_depth]
    shared = roles[16:18]
    x, y = roles[18:20]
    prefix_len = unique_depth + len(shared)
    lags = tuple(float(rng.choice((3, 4, 6, 8, 9))) for _ in range(prefix_len))
    exposures = rng.choice((4, 6, 7))
    left = tuple(left_unique) + tuple(shared) + (x,)
    right = tuple(right_unique) + tuple(shared) + (y,)
    return CX01World(
        generation_id=generation_id,
        family=CX01Family.HIGH_ORDER,
        seed=seed,
        training=(
            _sequence(left, lags, exposures),
            _sequence(right, lags, exposures),
        ),
        probes=(
            ProbeCase("history-left", left[:-1], lags[:-1], ((x, 1.0),)),
            ProbeCase("history-right", right[:-1], lags[:-1], ((y, 1.0),)),
        ),
    )


def _build_timing(
    generation_id: str,
    seed: int,
    roles: tuple[str, ...],
    rng: random.Random,
) -> CX01World:
    a, b, c, d, x, y = roles[:6]
    short = float(rng.randint(3, 7))
    long = float(rng.randint(14, 23))
    anchor = float(rng.randint(6, 11))
    target_lag = float(rng.randint(5, 10))
    exposures = rng.choice((4, 6, 7))
    left_lags = (short, long, anchor, target_lag)
    right_lags = (long, short, anchor, target_lag)
    prefix = (a, b, c, d)
    return CX01World(
        generation_id=generation_id,
        family=CX01Family.TIMING,
        seed=seed,
        training=(
            _sequence(prefix + (x,), left_lags, exposures),
            _sequence(prefix + (y,), right_lags, exposures),
        ),
        probes=(
            ProbeCase("timing-left", prefix, left_lags[:-1], ((x, 1.0),)),
            ProbeCase("timing-right", prefix, right_lags[:-1], ((y, 1.0),)),
        ),
    )


def _build_cycle(
    generation_id: str,
    seed: int,
    roles: tuple[str, ...],
    rng: random.Random,
) -> CX01World:
    cue, x, y, z = roles[:4]
    targets = (x, y, z)
    patterns = (
        (0, 1, 2, 0, 2, 1, 0),
        (0, 2, 1, 0, 1, 2, 0),
        (0, 1, 0, 2, 1, 2, 0),
        (0, 2, 0, 1, 2, 1, 0),
    )
    pattern = rng.choice(patterns)
    phase_exposures = tuple(2 + rng.randrange(3) for _ in pattern)
    training_exposures = rng.choice((1, 3, 4))
    training_lag = float(rng.choice((4, 5, 7, 8)))
    return CX01World(
        generation_id=generation_id,
        family=CX01Family.CYCLE,
        seed=seed,
        training=(_sequence((cue, x), (training_lag,), training_exposures),),
        probes=(),
        cycle_cue=cue,
        cycle_phases=tuple(
            CyclePhase(target=targets[index], exposures=exposures)
            for index, exposures in zip(pattern, phase_exposures, strict=True)
        ),
    )


def _build_branch(
    generation_id: str,
    seed: int,
    roles: tuple[str, ...],
    rng: random.Random,
) -> CX01World:
    a, b, c, d, x, y, z = roles[:7]
    counts = rng.choice(((8, 5, 3), (7, 5, 3), (9, 6, 3), (8, 6, 4), (9, 5, 4)))
    prefix = (a, b, c, d)
    prefix_lags = tuple(float(rng.choice((4, 6, 7, 9))) for _ in range(3))
    target_lag = float(rng.choice((4, 5, 7, 8)))
    lags = prefix_lags + (target_lag,)
    total = float(sum(counts))
    return CX01World(
        generation_id=generation_id,
        family=CX01Family.BRANCH,
        seed=seed,
        training=(
            _sequence(prefix + (x,), lags, counts[0]),
            _sequence(prefix + (y,), lags, counts[1]),
            _sequence(prefix + (z,), lags, counts[2]),
        ),
        probes=(
            ProbeCase(
                "branch-distribution",
                prefix,
                prefix_lags,
                (
                    (x, counts[0] / total),
                    (y, counts[1] / total),
                    (z, counts[2] / total),
                ),
            ),
        ),
    )


def _build_selectivity(
    generation_id: str,
    seed: int,
    roles: tuple[str, ...],
    rng: random.Random,
) -> CX01World:
    path_length = rng.choice((5, 6))
    main = tuple(roles[:path_length])
    control = tuple(roles[16 : 16 + path_length])
    exposures = rng.choice((4, 6, 7))
    lags = tuple(float(rng.choice((4, 6, 8, 9))) for _ in range(path_length - 1))
    return CX01World(
        generation_id=generation_id,
        family=CX01Family.SELECTIVITY,
        seed=seed,
        training=(
            _sequence(main, lags, exposures),
            _sequence(control, lags, exposures),
        ),
        probes=(
            ProbeCase("main", main[:-1], lags[:-1], ((main[-1], 1.0),)),
            ProbeCase("control", control[:-1], lags[:-1], ((control[-1], 1.0),)),
        ),
        intervention_main=main,
        intervention_control=control,
    )


def _build_loop(
    generation_id: str,
    seed: int,
    roles: tuple[str, ...],
    rng: random.Random,
) -> CX01World:
    sequence_length = rng.choice((5, 6))
    sequence = tuple(roles[:sequence_length])
    cue_length = sequence_length - 2
    cue = sequence[:cue_length]
    expected_generated = sequence[cue_length]
    external_consequence = sequence[-1]
    lags = tuple(float(rng.choice((4, 6, 7, 9))) for _ in range(sequence_length - 1))
    exposures = rng.choice((4, 6, 7))
    return CX01World(
        generation_id=generation_id,
        family=CX01Family.LOOP,
        seed=seed,
        training=(_sequence(sequence, lags, exposures),),
        probes=(
            ProbeCase(
                "loop-cue",
                cue,
                lags[: cue_length - 1],
                ((expected_generated, 1.0),),
            ),
        ),
        loop=LoopSpec(cue, expected_generated, external_consequence),
    )


def build_formal_world(
    generation_id: str,
    family: CX01Family,
    seed: int,
) -> CX01World:
    """Build a formal-candidate world with structural variation beyond token relabeling.

    The development generator remains unchanged. This generator varies topology,
    timing values, exposure ratios, or contingency schedules according to family,
    and then refuses any token-renaming-equivalent development structure.
    """

    if seed < 0 or seed in HISTORICALLY_EXPOSED_SEEDS:
        raise ValueError("formal world seed is invalid or historically exposed")
    if not generation_id:
        raise ValueError("formal world requires a generation id")

    rng = _rng(generation_id, family, seed)
    roles = _roles(generation_id, family, seed)
    builders = {
        CX01Family.HIGH_ORDER: _build_high_order,
        CX01Family.TIMING: _build_timing,
        CX01Family.CYCLE: _build_cycle,
        CX01Family.BRANCH: _build_branch,
        CX01Family.SELECTIVITY: _build_selectivity,
        CX01Family.LOOP: _build_loop,
    }
    world = builders[family](generation_id, seed, roles, rng)
    world.validate()
    if world_structure_signature(world) in development_structure_signatures()[family]:
        raise RuntimeError(
            f"formal world is token-renaming-equivalent to development structure: {family.value}"
        )
    return world


def audit_formal_grid_structure(worlds: Iterable[CX01World]) -> dict[str, Any]:
    grouped: dict[CX01Family, list[CX01World]] = defaultdict(list)
    for world in worlds:
        world.validate()
        grouped[world.family].append(world)

    development = development_structure_signatures()
    family_rows: dict[str, Any] = {}
    for family in CX01Family:
        selected = grouped.get(family, [])
        if not selected:
            raise ValueError(f"formal grid is missing family {family.value}")
        signatures = [world_structure_signature(world) for world in selected]
        overlaps = sorted(set(signatures).intersection(development[family]))
        minimum_unique = min(5, len(selected))
        unique_count = len(set(signatures))
        if overlaps:
            raise RuntimeError(f"formal grid overlaps development structure: {family.value}")
        if unique_count < minimum_unique:
            raise RuntimeError(
                f"formal grid lacks structural diversity for {family.value}: "
                f"unique={unique_count} required={minimum_unique}"
            )
        family_rows[family.value] = {
            "development_overlap_count": len(overlaps),
            "unique_structure_count": unique_count,
            "world_count": len(selected),
        }

    return {
        "family_rows": family_rows,
        "policy_version": FORMAL_STRUCTURE_POLICY_VERSION,
        "world_count": sum(len(values) for values in grouped.values()),
    }
