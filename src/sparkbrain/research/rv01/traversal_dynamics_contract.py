from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from typing import Any

from .interference_contract import InterferenceFamily, InterferencePhase, RouteExposure

R01_14_PROTOCOL_ID = "rv01-r01-14-traversal-dynamics-v1"
R01_14_DEVELOPMENT_SEEDS = (400, 401, 402, 403, 404)
R01_14_HELD_OUT_SEEDS = tuple(range(500, 510))
_R01_14_WORLD_SALT = "rv01-r01-14-fresh-world-grid-v1"


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
class TraversalDynamicsWorldSpec:
    phase: InterferencePhase
    family: InterferenceFamily
    seed: int
    unit_count: int
    routes: tuple[RouteExposure, ...]
    training_order: tuple[str, ...]
    probe_order: tuple[str, ...]
    lag_ms: float
    threshold: float
    cue_magnitude: float
    maximum_active_outgoing_edges: int
    maximum_total_active_edges: int
    reversal_route_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        allowed = (
            R01_14_DEVELOPMENT_SEEDS
            if self.phase is InterferencePhase.DEVELOPMENT
            else R01_14_HELD_OUT_SEEDS
        )
        if self.seed not in allowed:
            raise ValueError("seed does not belong to the R01-14 phase")
        if self.unit_count != 96:
            raise ValueError("R01-14 fixes the world scale at 96 anonymous units")
        if len(self.routes) < 2:
            raise ValueError("R01-14 requires multiple routes")
        for route in self.routes:
            route.validate(unit_count=self.unit_count)
        route_ids = tuple(route.route_id for route in self.routes)
        if len(set(route_ids)) != len(route_ids):
            raise ValueError("route IDs must be unique")
        if (
            len(self.training_order) != len(route_ids)
            or set(self.training_order) != set(route_ids)
        ):
            raise ValueError("training_order must contain every route exactly once")
        if (
            len(self.probe_order) != len(route_ids)
            or set(self.probe_order) != set(route_ids)
        ):
            raise ValueError("probe_order must contain every route exactly once")
        if not set(self.reversal_route_ids).issubset(route_ids):
            raise ValueError("reversal route IDs must be declared routes")
        if self.lag_ms <= 0.0 or self.threshold <= 0.0:
            raise ValueError("timing and threshold must be positive")
        if self.cue_magnitude <= self.threshold:
            raise ValueError("cue magnitude must cross the ordinary Field threshold")
        if self.maximum_active_outgoing_edges < 1:
            raise ValueError("active outgoing budget must be positive")
        if self.maximum_total_active_edges < self.maximum_active_outgoing_edges:
            raise ValueError("total edge budget cannot be below outgoing budget")
        self._validate_family_shape()

    def _validate_family_shape(self) -> None:
        values = tuple(route.units for route in self.routes)
        if self.family is InterferenceFamily.DISJOINT_ROUTES:
            if any(
                set(left).intersection(right)
                for index, left in enumerate(values)
                for right in values[index + 1 :]
            ):
                raise ValueError("disjoint family contains overlapping routes")
        elif self.family is InterferenceFamily.SHARED_CUE_BRANCHES:
            if len({route[0] for route in values}) != 1:
                raise ValueError("shared-cue family must share one cue")
            if any(
                set(left[1:]).intersection(right[1:])
                for index, left in enumerate(values)
                for right in values[index + 1 :]
            ):
                raise ValueError("shared-cue branches must diverge after the cue")
        elif self.family is InterferenceFamily.SHARED_PREFIX_BRANCHES:
            if len({route[:2] for route in values}) != 1:
                raise ValueError("shared-prefix family must share two leading units")
            if any(
                set(left[2:]).intersection(right[2:])
                for index, left in enumerate(values)
                for right in values[index + 1 :]
            ):
                raise ValueError("shared-prefix branches must diverge after the prefix")
        elif self.family is InterferenceFamily.EDGE_REVERSAL:
            if not self.reversal_route_ids:
                raise ValueError("edge-reversal family requires reversal routes")
            pairs = {
                (route[index], route[index + 1])
                for route in values
                for index in range(len(route) - 1)
            }
            if not any((target, source) in pairs for source, target in pairs):
                raise ValueError("edge-reversal family lacks an opposing directed edge")
        elif self.family is InterferenceFamily.DENSE_ROUTE_LOAD:
            if len(values) < 6:
                raise ValueError("dense-route family requires at least six routes")
            exposed_edges = sum(len(route) - 1 for route in values)
            if self.maximum_total_active_edges >= exposed_edges:
                raise ValueError(
                    "dense-route family must exceed the active-edge budget"
                )

    @property
    def world_id(self) -> str:
        return f"r01-14:{self.phase.value}:{self.family.value}:{self.seed}"

    @property
    def route_count(self) -> int:
        return len(self.routes)

    @property
    def directed_exposure_edge_count(self) -> int:
        return sum(
            (len(route.units) - 1) * route.exposure_count for route in self.routes
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "protocol_id": R01_14_PROTOCOL_ID,
            "cue_magnitude": self.cue_magnitude,
            "family": self.family.value,
            "lag_ms": self.lag_ms,
            "maximum_active_outgoing_edges": self.maximum_active_outgoing_edges,
            "maximum_total_active_edges": self.maximum_total_active_edges,
            "phase": self.phase.value,
            "probe_order": list(self.probe_order),
            "reversal_route_ids": list(self.reversal_route_ids),
            "routes": [asdict(route) for route in self.routes],
            "seed": self.seed,
            "threshold": self.threshold,
            "training_order": list(self.training_order),
            "unit_count": self.unit_count,
        }

    def specification_hash(self) -> str:
        return _digest(self.state_dict())


def _route(route_id: str, units: tuple[int, ...], exposure_count: int) -> RouteExposure:
    return RouteExposure(route_id=route_id, units=units, exposure_count=exposure_count)


def traversal_dynamics_world(
    phase: InterferencePhase,
    family: InterferenceFamily,
    seed: int,
) -> TraversalDynamicsWorldSpec:
    allowed = (
        R01_14_DEVELOPMENT_SEEDS
        if phase is InterferencePhase.DEVELOPMENT
        else R01_14_HELD_OUT_SEEDS
    )
    if seed not in allowed:
        raise ValueError("unsupported R01-14 seed for phase")

    rng_seed = int(
        _digest(
            {
                "family": family.value,
                "phase": phase.value,
                "protocol_id": R01_14_PROTOCOL_ID,
                "salt": _R01_14_WORLD_SALT,
                "seed": seed,
            }
        )[:16],
        16,
    )
    rng = random.Random(rng_seed)
    unit_count = 96
    ids = list(range(unit_count))
    rng.shuffle(ids)
    exposure_base = 5

    if family is InterferenceFamily.DISJOINT_ROUTES:
        routes = tuple(
            _route(
                f"route:{index}",
                tuple(ids[index * 4 : index * 4 + 4]),
                exposure_base + index % 2,
            )
            for index in range(3)
        )
        outgoing_budget = 2
        total_budget = 16
        reversal_ids: tuple[str, ...] = ()
    elif family is InterferenceFamily.SHARED_CUE_BRANCHES:
        cue = ids[0]
        routes = tuple(
            _route(
                f"route:{index}",
                (cue, *ids[1 + index * 3 : 4 + index * 3]),
                exposure_base + (2 - index),
            )
            for index in range(3)
        )
        outgoing_budget = 3
        total_budget = 16
        reversal_ids = ()
    elif family is InterferenceFamily.SHARED_PREFIX_BRANCHES:
        prefix = (ids[0], ids[1])
        routes = tuple(
            _route(
                f"route:{index}",
                (*prefix, ids[2 + index * 2], ids[3 + index * 2]),
                exposure_base + (2 - index),
            )
            for index in range(3)
        )
        outgoing_budget = 3
        total_budget = 16
        reversal_ids = ()
    elif family is InterferenceFamily.EDGE_REVERSAL:
        routes = (
            _route(
                "route:forward",
                (ids[0], ids[1], ids[2], ids[3]),
                exposure_base + 1,
            ),
            _route(
                "route:reverse",
                (ids[4], ids[2], ids[1], ids[5]),
                exposure_base,
            ),
            _route(
                "route:control",
                (ids[6], ids[7], ids[8], ids[9]),
                exposure_base,
            ),
        )
        outgoing_budget = 3
        total_budget = 16
        reversal_ids = ("route:forward", "route:reverse")
    else:
        common = ids[0]
        routes = tuple(
            _route(
                f"route:{index}",
                (
                    common if index < 4 else ids[index],
                    ids[10 + index * 3],
                    ids[11 + index * 3],
                    ids[12 + index * 3],
                ),
                exposure_base + index % 3,
            )
            for index in range(8)
        )
        outgoing_budget = 3
        total_budget = 12
        reversal_ids = ()

    route_ids = [route.route_id for route in routes]
    training_order = route_ids.copy()
    probe_order = route_ids.copy()
    rng.shuffle(training_order)
    rng.shuffle(probe_order)
    threshold = round(0.44 + rng.random() * 0.12, 6)
    world = TraversalDynamicsWorldSpec(
        phase=phase,
        family=family,
        seed=seed,
        unit_count=unit_count,
        routes=routes,
        training_order=tuple(training_order),
        probe_order=tuple(probe_order),
        lag_ms=round(4.0 + rng.random() * 2.0, 6),
        threshold=threshold,
        cue_magnitude=round(threshold + 0.45, 6),
        maximum_active_outgoing_edges=outgoing_budget,
        maximum_total_active_edges=total_budget,
        reversal_route_ids=reversal_ids,
    )
    world.validate()
    return world


def development_traversal_dynamics_worlds() -> tuple[TraversalDynamicsWorldSpec, ...]:
    return tuple(
        traversal_dynamics_world(InterferencePhase.DEVELOPMENT, family, seed)
        for family in InterferenceFamily
        for seed in R01_14_DEVELOPMENT_SEEDS
    )


def held_out_traversal_dynamics_worlds() -> tuple[TraversalDynamicsWorldSpec, ...]:
    return tuple(
        traversal_dynamics_world(InterferencePhase.HELD_OUT, family, seed)
        for family in InterferenceFamily
        for seed in R01_14_HELD_OUT_SEEDS
    )


def traversal_dynamics_world_grid_hash(
    worlds: tuple[TraversalDynamicsWorldSpec, ...],
) -> str:
    return _digest([world.state_dict() for world in worlds])
