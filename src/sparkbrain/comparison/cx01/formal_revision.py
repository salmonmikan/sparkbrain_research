from __future__ import annotations

import hashlib
import json
from collections import Counter

from .formal_worlds import build_formal_world
from .worlds import (
    CX01Family,
    CX01World,
    CyclePhase,
    LoopSpec,
    ProbeCase,
    SequenceExposure,
)

FORMAL_GENERATOR_REVISION = "cx01-formal-structural-revision-v4"


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _fresh_token(world: CX01World, role: str) -> str:
    existing = {
        token
        for row in world.training
        for token in row.tokens
    }
    existing.update(
        token
        for probe in world.probes
        for token in (
            *probe.prefix,
            *(target for target, _ in probe.expected_distribution),
        )
    )
    existing.update(phase.target for phase in world.cycle_phases)
    material = {
        "family": world.family.value,
        "generation_id": world.generation_id,
        "revision": FORMAL_GENERATOR_REVISION,
        "role": role,
        "seed": world.seed,
    }
    candidate = f"u{64 + int(_digest(material)[:8], 16) % 10000:05d}"
    suffix = 0
    while candidate in existing:
        suffix += 1
        candidate = f"u{64 + int(_digest((material, suffix))[:8], 16) % 10000:05d}"
    return candidate


def _extra_lag(world: CX01World, role: str) -> float:
    values = (3.0, 4.0, 6.0, 8.0, 9.0, 11.0)
    material = {
        "family": world.family.value,
        "revision": FORMAL_GENERATOR_REVISION,
        "role": role,
        "seed": world.seed,
    }
    return values[int(_digest(material)[:8], 16) % len(values)]


def _prepend_sequence(
    row: SequenceExposure,
    token: str,
    lag_ms: float,
) -> SequenceExposure:
    value = SequenceExposure(
        tokens=(token, *row.tokens),
        lags_ms=(lag_ms, *row.lags_ms),
        exposures=row.exposures,
    )
    value.validate()
    return value


def _prepend_probe(
    probe: ProbeCase,
    token: str,
    lag_ms: float,
) -> ProbeCase:
    value = ProbeCase(
        probe_id=probe.probe_id,
        prefix=(token, *probe.prefix),
        lags_ms=(lag_ms, *probe.lags_ms),
        expected_distribution=probe.expected_distribution,
    )
    value.validate()
    return value


def _revise_high_order(world: CX01World) -> CX01World:
    left_token = _fresh_token(world, "high-order-left-context")
    right_token = _fresh_token(world, "high-order-right-context")
    left_lag = _extra_lag(world, "high-order-left-context")
    right_lag = _extra_lag(world, "high-order-right-context")
    return CX01World(
        generation_id=world.generation_id,
        family=world.family,
        seed=world.seed,
        training=(
            _prepend_sequence(world.training[0], left_token, left_lag),
            _prepend_sequence(world.training[1], right_token, right_lag),
        ),
        probes=(
            _prepend_probe(world.probes[0], left_token, left_lag),
            _prepend_probe(world.probes[1], right_token, right_lag),
        ),
    )


def _revise_shared_context(world: CX01World, role: str) -> CX01World:
    token = _fresh_token(world, f"{role}-shared-context")
    lag = _extra_lag(world, f"{role}-shared-context")
    return CX01World(
        generation_id=world.generation_id,
        family=world.family,
        seed=world.seed,
        training=tuple(_prepend_sequence(row, token, lag) for row in world.training),
        probes=tuple(_prepend_probe(probe, token, lag) for probe in world.probes),
    )


def _cycle_has_global_majority_conflict(world: CX01World) -> bool:
    """Mirror the family-identifiability condition without consulting outcomes."""

    if world.family is not CX01Family.CYCLE or world.cycle_cue is None:
        raise RuntimeError("cycle conflict check requires a cycle world")

    historical = Counter[str]()
    for row in world.training:
        if row.tokens and row.tokens[0] == world.cycle_cue:
            historical[row.tokens[-1]] += row.exposures

    for phase in world.cycle_phases:
        historical[phase.target] += phase.exposures
        maximum = max(historical.values(), default=0)
        if historical[phase.target] < maximum:
            return True
    return False


def _revise_cycle(world: CX01World) -> CX01World:
    fourth_target = _fresh_token(world, "cycle-fourth-target")
    phases = (
        world.cycle_phases[0],
        CyclePhase(target=fourth_target, exposures=1),
        *world.cycle_phases[1:],
    )
    return CX01World(
        generation_id=world.generation_id,
        family=world.family,
        seed=world.seed,
        training=world.training,
        probes=world.probes,
        cycle_cue=world.cycle_cue,
        cycle_phases=phases,
    )


def _revise_selectivity(world: CX01World) -> CX01World:
    main_token = _fresh_token(world, "selectivity-main-context")
    control_token = _fresh_token(world, "selectivity-control-context")
    lag = _extra_lag(world, "selectivity-matched-context")
    main = (main_token, *world.intervention_main)
    control = (control_token, *world.intervention_control)
    return CX01World(
        generation_id=world.generation_id,
        family=world.family,
        seed=world.seed,
        training=(
            _prepend_sequence(world.training[0], main_token, lag),
            _prepend_sequence(world.training[1], control_token, lag),
        ),
        probes=(
            _prepend_probe(world.probes[0], main_token, lag),
            _prepend_probe(world.probes[1], control_token, lag),
        ),
        intervention_main=main,
        intervention_control=control,
    )


def _revise_loop(world: CX01World) -> CX01World:
    if world.loop is None:
        raise RuntimeError("loop revision requires a loop specification")
    token = _fresh_token(world, "loop-context")
    lag = _extra_lag(world, "loop-context")
    return CX01World(
        generation_id=world.generation_id,
        family=world.family,
        seed=world.seed,
        training=(_prepend_sequence(world.training[0], token, lag),),
        probes=(_prepend_probe(world.probes[0], token, lag),),
        loop=LoopSpec(
            cue_prefix=(token, *world.loop.cue_prefix),
            expected_generated=world.loop.expected_generated,
            external_consequence=world.loop.external_consequence,
        ),
    )


def build_revised_formal_world(
    generation_id: str,
    family: CX01Family,
    seed: int,
) -> CX01World:
    """Build the pre-formal revision with seed-conditioned topology variation.

    Odd seeds deterministically change one family-valid topological degree of
    freedom. A cycle world that would otherwise lack the preregistered
    historical-majority conflict receives the same outcome-blind fourth-target
    construction even on an even seed. This is a generator-domain correction:
    it depends only on the generated world structure and never on comparator
    results, scores, thresholds, or rapid-cycle performance.
    """

    world = build_formal_world(generation_id, family, seed)

    if family is CX01Family.CYCLE:
        needs_topology_revision = seed % 2 != 0
        needs_identifiability_revision = not _cycle_has_global_majority_conflict(world)
        if needs_topology_revision or needs_identifiability_revision:
            revised = _revise_cycle(world)
            revised.validate()
            if not _cycle_has_global_majority_conflict(revised):
                raise RuntimeError(
                    "cycle revision failed to establish family identifiability"
                )
            return revised
        return world

    if seed % 2 == 0:
        return world

    revisers = {
        CX01Family.HIGH_ORDER: _revise_high_order,
        CX01Family.TIMING: lambda value: _revise_shared_context(value, "timing"),
        CX01Family.BRANCH: lambda value: _revise_shared_context(value, "branch"),
        CX01Family.SELECTIVITY: _revise_selectivity,
        CX01Family.LOOP: _revise_loop,
    }
    revised = revisers[family](world)
    revised.validate()
    return revised
