from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class CX01Family(StrEnum):
    HIGH_ORDER = "cx01-high-order-aliasing"
    TIMING = "cx01-timing-aliasing"
    CYCLE = "cx01-contingency-cycle"
    BRANCH = "cx01-ambiguous-branch"
    SELECTIVITY = "cx01-selective-interference"
    LOOP = "cx01-reality-provenance-loop"


DEVELOPMENT_GENERATION_ID = "cx01-development-001"
DEVELOPMENT_SEEDS = tuple(range(3000, 3005))
HISTORICALLY_EXPOSED_SEEDS = frozenset(
    (*range(100, 110), *range(1000, 1010), *range(2000, 2010))
)


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class SequenceExposure:
    tokens: tuple[str, ...]
    lags_ms: tuple[float, ...]
    exposures: int

    def validate(self) -> None:
        if len(self.tokens) < 2:
            raise ValueError("training sequence requires at least two tokens")
        if len(self.lags_ms) != len(self.tokens) - 1:
            raise ValueError("one lag is required between adjacent tokens")
        if any(not token for token in self.tokens):
            raise ValueError("sequence tokens must be non-empty")
        if any(not math.isfinite(lag) or lag <= 0 for lag in self.lags_ms):
            raise ValueError("sequence lags must be positive and finite")
        if self.exposures < 1:
            raise ValueError("sequence exposure count must be positive")


@dataclass(frozen=True, slots=True)
class ProbeCase:
    probe_id: str
    prefix: tuple[str, ...]
    lags_ms: tuple[float, ...]
    expected_distribution: tuple[tuple[str, float], ...]

    def validate(self) -> None:
        if not self.probe_id or not self.prefix:
            raise ValueError("probe identity and prefix are required")
        if len(self.lags_ms) != max(0, len(self.prefix) - 1):
            raise ValueError("probe lags must align with the prefix")
        if any(not math.isfinite(lag) or lag <= 0 for lag in self.lags_ms):
            raise ValueError("probe lags must be positive and finite")
        if not self.expected_distribution:
            raise ValueError("probe requires an expected distribution")
        total = 0.0
        seen: set[str] = set()
        for token, probability in self.expected_distribution:
            if not token or token in seen:
                raise ValueError("probe target tokens must be unique and non-empty")
            if not math.isfinite(probability) or probability <= 0:
                raise ValueError("probe probabilities must be positive and finite")
            seen.add(token)
            total += probability
        if not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("probe target probabilities must sum to one")


@dataclass(frozen=True, slots=True)
class CyclePhase:
    target: str
    exposures: int

    def validate(self) -> None:
        if not self.target or self.exposures < 1:
            raise ValueError("cycle phase target and exposure count are required")


@dataclass(frozen=True, slots=True)
class LoopSpec:
    cue_prefix: tuple[str, ...]
    expected_generated: str
    external_consequence: str

    def validate(self) -> None:
        if len(self.cue_prefix) < 1:
            raise ValueError("loop cue prefix is required")
        if not self.expected_generated or not self.external_consequence:
            raise ValueError("loop generated and external tokens are required")
        if self.expected_generated == self.external_consequence:
            raise ValueError("generated and external consequence tokens must differ")


@dataclass(frozen=True, slots=True)
class CX01World:
    generation_id: str
    family: CX01Family
    seed: int
    training: tuple[SequenceExposure, ...]
    probes: tuple[ProbeCase, ...]
    cycle_cue: str | None = None
    cycle_phases: tuple[CyclePhase, ...] = ()
    intervention_main: tuple[str, ...] = ()
    intervention_control: tuple[str, ...] = ()
    loop: LoopSpec | None = None

    def validate(self) -> None:
        if not self.generation_id:
            raise ValueError("world generation id is required")
        if self.seed < 0 or self.seed in HISTORICALLY_EXPOSED_SEEDS:
            raise ValueError("world seed is invalid or historically exposed")
        if not self.training:
            raise ValueError("world requires training data")
        for row in self.training:
            row.validate()
        for probe in self.probes:
            probe.validate()
        for phase in self.cycle_phases:
            phase.validate()
        if self.cycle_phases and not self.cycle_cue:
            raise ValueError("cycle phases require an anonymous cycle cue")
        if bool(self.intervention_main) != bool(self.intervention_control):
            raise ValueError("selectivity paths must be present together")
        if self.intervention_main and set(self.intervention_main).intersection(
            self.intervention_control
        ):
            raise ValueError("selectivity main/control paths must be disjoint")
        if self.loop is not None:
            self.loop.validate()

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["family"] = self.family.value
        return value

    def specification_hash(self) -> str:
        return _digest(self.state_dict())


def _roles(generation_id: str, family: CX01Family, seed: int) -> tuple[str, ...]:
    rng_seed = int(
        _digest({"generation": generation_id, "family": family.value, "seed": seed})[:16],
        16,
    )
    rng = random.Random(rng_seed)
    values = list(range(64))
    rng.shuffle(values)
    return tuple(f"u{value:02d}" for value in values)


def _sequence(tokens: tuple[str, ...], lags: tuple[float, ...], exposures: int) -> SequenceExposure:
    row = SequenceExposure(tokens, lags, exposures)
    row.validate()
    return row


def build_world(generation_id: str, family: CX01Family, seed: int) -> CX01World:
    if seed in HISTORICALLY_EXPOSED_SEEDS:
        raise ValueError("historic/exposed seed cannot enter CX01")
    roles = _roles(generation_id, family, seed)
    a, b, c, d, x, y, z, p, q, r, s, t = roles[:12]

    if family is CX01Family.HIGH_ORDER:
        training = (
            _sequence((a, b, c, x), (5.0, 7.0, 6.0), 5),
            _sequence((d, b, c, y), (5.0, 7.0, 6.0), 5),
        )
        probes = (
            ProbeCase("history-a", (a, b, c), (5.0, 7.0), ((x, 1.0),)),
            ProbeCase("history-d", (d, b, c), (5.0, 7.0), ((y, 1.0),)),
        )
        world = CX01World(generation_id, family, seed, training, probes)
    elif family is CX01Family.TIMING:
        # Token prefix is intentionally identical. Only temporal structure identifies the target.
        training = (
            _sequence((a, b, c, x), (4.0, 18.0, 6.0), 5),
            _sequence((a, b, c, y), (18.0, 4.0, 6.0), 5),
        )
        probes = (
            ProbeCase("fast-slow", (a, b, c), (4.0, 18.0), ((x, 1.0),)),
            ProbeCase("slow-fast", (a, b, c), (18.0, 4.0), ((y, 1.0),)),
        )
        world = CX01World(generation_id, family, seed, training, probes)
    elif family is CX01Family.CYCLE:
        training = (_sequence((a, x), (6.0,), 2),)
        phases = tuple(
            CyclePhase(target, 2 + ((seed + index) % 2))
            for index, target in enumerate((x, y, x, z, y, x))
        )
        world = CX01World(
            generation_id,
            family,
            seed,
            training,
            (),
            cycle_cue=a,
            cycle_phases=phases,
        )
    elif family is CX01Family.BRANCH:
        counts = (6, 5, 4)
        training = (
            _sequence((a, b, c, x), (5.0, 5.0, 5.0), counts[0]),
            _sequence((a, b, c, y), (5.0, 5.0, 5.0), counts[1]),
            _sequence((a, b, c, z), (5.0, 5.0, 5.0), counts[2]),
        )
        total = float(sum(counts))
        probes = (
            ProbeCase(
                "branch-distribution",
                (a, b, c),
                (5.0, 5.0),
                ((x, counts[0] / total), (y, counts[1] / total), (z, counts[2] / total)),
            ),
        )
        world = CX01World(generation_id, family, seed, training, probes)
    elif family is CX01Family.SELECTIVITY:
        main = (a, b, c, x)
        control = (p, q, r, s)
        training = (
            _sequence(main, (5.0, 7.0, 5.0), 5),
            _sequence(control, (5.0, 7.0, 5.0), 5),
        )
        probes = (
            ProbeCase("main", main[:-1], (5.0, 7.0), ((x, 1.0),)),
            ProbeCase("control", control[:-1], (5.0, 7.0), ((s, 1.0),)),
        )
        world = CX01World(
            generation_id,
            family,
            seed,
            training,
            probes,
            intervention_main=main,
            intervention_control=control,
        )
    else:
        training = (_sequence((a, b, c, t), (5.0, 5.0, 8.0), 5),)
        probes = (ProbeCase("loop-cue", (a, b), (5.0,), ((c, 1.0),)),)
        world = CX01World(
            generation_id,
            family,
            seed,
            training,
            probes,
            loop=LoopSpec((a, b), c, t),
        )

    world.validate()
    return world


def build_development_grid() -> tuple[CX01World, ...]:
    return tuple(
        build_world(DEVELOPMENT_GENERATION_ID, family, seed)
        for family in CX01Family
        for seed in DEVELOPMENT_SEEDS
    )


def development_grid_hash() -> str:
    return _digest(
        {
            "generation": DEVELOPMENT_GENERATION_ID,
            "worlds": [world.state_dict() for world in build_development_grid()],
        }
    )
