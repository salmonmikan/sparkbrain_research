"""Deterministic construction-only world grid for prospective RV01 R01-16.

The identities, fresh seed inventory, world salt, and five family names are bound
by ``rv01_r01_16_identity``.  This module supplies the previously missing exact
96-unit geometry/schedule construction needed to capture pre/post training state.
It exposes no capability runner and executes no probe.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

from .rv01.interference_contract import InterferenceFamily, RouteExposure
from .rv01_r01_16_identity import (
    R01_16_DEVELOPMENT_SEEDS,
    R01_16_PROTOCOL_ID,
    R01_16_UNIT_COUNT,
    R01_16_WORLD_SALT,
    R0116DevelopmentIdentity,
    development_identity_grid,
)


def _digest(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _route(route_id: str, units: tuple[int, ...], exposure_count: int) -> RouteExposure:
    return RouteExposure(route_id=route_id, units=units, exposure_count=exposure_count)


@dataclass(frozen=True, slots=True)
class R0116DevelopmentWorldSpec:
    """One fixed R01-16 development world before capability is opened."""

    identity: R0116DevelopmentIdentity
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

    @property
    def world_id(self) -> str:
        return self.identity.world_id

    @property
    def route_count(self) -> int:
        return len(self.routes)

    def validate(self) -> None:
        self.identity.validate()
        if self.seed != self.identity.seed:
            raise ValueError("R01-16 world seed diverged from its bound identity")
        if self.family.value != self.identity.family:
            raise ValueError("R01-16 world family diverged from its bound identity")
        if self.seed not in R01_16_DEVELOPMENT_SEEDS:
            raise ValueError("R01-16 world seed is outside the fixed development grid")
        if self.unit_count != R01_16_UNIT_COUNT:
            raise ValueError("R01-16 world must retain the bound 96-unit scale")
        if len(self.routes) < 2:
            raise ValueError("R01-16 world requires multiple routes")
        for route in self.routes:
            route.validate(unit_count=self.unit_count)
        route_ids = tuple(route.route_id for route in self.routes)
        if len(set(route_ids)) != len(route_ids):
            raise ValueError("R01-16 route IDs must be unique")
        if len(self.training_order) != len(route_ids) or set(self.training_order) != set(
            route_ids
        ):
            raise ValueError("R01-16 training_order must contain every route once")
        if len(self.probe_order) != len(route_ids) or set(self.probe_order) != set(route_ids):
            raise ValueError("R01-16 probe_order must contain every route once")
        if not set(self.reversal_route_ids).issubset(route_ids):
            raise ValueError("R01-16 reversal routes must be declared routes")
        if self.lag_ms <= 0.0 or self.threshold <= 0.0:
            raise ValueError("R01-16 timing and threshold must be positive")
        if self.cue_magnitude <= self.threshold:
            raise ValueError("R01-16 cue magnitude must cross the ordinary Field threshold")
        if self.maximum_active_outgoing_edges < 1:
            raise ValueError("R01-16 outgoing edge budget must be positive")
        if self.maximum_total_active_edges < self.maximum_active_outgoing_edges:
            raise ValueError("R01-16 total edge budget cannot be below outgoing budget")
        self._validate_family_shape()

    def _validate_family_shape(self) -> None:
        values = tuple(route.units for route in self.routes)
        if self.family is InterferenceFamily.DISJOINT_ROUTES:
            if any(
                set(left).intersection(right)
                for index, left in enumerate(values)
                for right in values[index + 1 :]
            ):
                raise ValueError("R01-16 disjoint family contains overlapping routes")
        elif self.family is InterferenceFamily.SHARED_CUE_BRANCHES:
            if len({route[0] for route in values}) != 1:
                raise ValueError("R01-16 shared-cue family must share one cue")
            if any(
                set(left[1:]).intersection(right[1:])
                for index, left in enumerate(values)
                for right in values[index + 1 :]
            ):
                raise ValueError("R01-16 shared-cue branches must diverge after the cue")
        elif self.family is InterferenceFamily.SHARED_PREFIX_BRANCHES:
            if len({route[:2] for route in values}) != 1:
                raise ValueError("R01-16 shared-prefix family must share two leading units")
            if any(
                set(left[2:]).intersection(right[2:])
                for index, left in enumerate(values)
                for right in values[index + 1 :]
            ):
                raise ValueError("R01-16 shared-prefix branches must diverge after prefix")
        elif self.family is InterferenceFamily.EDGE_REVERSAL:
            if not self.reversal_route_ids:
                raise ValueError("R01-16 edge-reversal family requires reversal routes")
            edges = {
                (route[index], route[index + 1])
                for route in values
                for index in range(len(route) - 1)
            }
            if not any((target, source) in edges for source, target in edges):
                raise ValueError("R01-16 edge-reversal family lacks opposing edge")
        elif self.family is InterferenceFamily.DENSE_ROUTE_LOAD:
            if len(values) < 6:
                raise ValueError("R01-16 dense-route family requires at least six routes")
            exposed_edges = sum(len(route) - 1 for route in values)
            if self.maximum_total_active_edges >= exposed_edges:
                raise ValueError("R01-16 dense-route family must exceed active-edge budget")

    def probe_horizon_ms(self, route: RouteExposure) -> float:
        if route.route_id not in {row.route_id for row in self.routes}:
            raise ValueError("probe route is not registered in this R01-16 world")
        return self.lag_ms * (len(route.units) + 3)

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "cue_magnitude": self.cue_magnitude,
            "family": self.family.value,
            "identity_sha256": self.identity.identity_sha256,
            "lag_ms": self.lag_ms,
            "maximum_active_outgoing_edges": self.maximum_active_outgoing_edges,
            "maximum_total_active_edges": self.maximum_total_active_edges,
            "phase": "development",
            "probe_order": list(self.probe_order),
            "protocol_id": R01_16_PROTOCOL_ID,
            "reversal_route_ids": list(self.reversal_route_ids),
            "routes": [route.state_dict() for route in self.routes],
            "seed": self.seed,
            "threshold": self.threshold,
            "training_order": list(self.training_order),
            "unit_count": self.unit_count,
            "world_id": self.world_id,
            "world_salt": R01_16_WORLD_SALT,
        }

    def specification_hash(self) -> str:
        return _digest(self.state_dict())


def build_development_world(identity: R0116DevelopmentIdentity) -> R0116DevelopmentWorldSpec:
    """Build one exact fresh world using the inherited 96-unit RV01 geometry."""

    identity.validate()
    family = InterferenceFamily(identity.family)
    rng_seed = int(
        _digest(
            {
                "family": family.value,
                "phase": "development",
                "protocol_id": R01_16_PROTOCOL_ID,
                "salt": R01_16_WORLD_SALT,
                "seed": identity.seed,
            }
        )[:16],
        16,
    )
    rng = random.Random(rng_seed)
    ids = list(range(R01_16_UNIT_COUNT))
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
            _route("route:forward", (ids[0], ids[1], ids[2], ids[3]), exposure_base + 1),
            _route("route:reverse", (ids[4], ids[2], ids[1], ids[5]), exposure_base),
            _route("route:control", (ids[6], ids[7], ids[8], ids[9]), exposure_base),
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
    world = R0116DevelopmentWorldSpec(
        identity=identity,
        family=family,
        seed=identity.seed,
        unit_count=R01_16_UNIT_COUNT,
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


def development_world_grid() -> tuple[R0116DevelopmentWorldSpec, ...]:
    worlds = tuple(build_development_world(identity) for identity in development_identity_grid())
    if len(worlds) != 25:
        raise RuntimeError("R01-16 development world grid must contain exactly 25 worlds")
    if len({world.world_id for world in worlds}) != len(worlds):
        raise RuntimeError("R01-16 development world grid contains duplicate identities")
    return worlds


def development_world_grid_hash() -> str:
    return _digest([world.state_dict() for world in development_world_grid()])


__all__ = [
    "R0116DevelopmentWorldSpec",
    "build_development_world",
    "development_world_grid",
    "development_world_grid_hash",
]
