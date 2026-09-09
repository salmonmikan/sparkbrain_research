"""N3-DEV-001 signed recurrent learner; no world/evaluator dependency."""

from __future__ import annotations

import math
import random
from typing import Any

from .credit_bridge import A01LocalTemporalExpectation


class N3CausalTrace:
    """Two opaque slots; fixed sparse recurrence and learned signed readout."""

    def __init__(self, path_ids: tuple[str, str]) -> None:
        if len(path_ids) != 2 or len(set(path_ids)) != 2:
            raise ValueError("exactly two unique paths required")
        if any(type(path) is not str or not path for path in path_ids):
            raise ValueError("path identifiers must be nonempty strings")
        self.path_ids = tuple(path_ids)
        rng = random.Random(12001)
        raw = [rng.uniform(-1.0, 1.0) for _ in range(2)]
        scale = 0.75 / max(abs(value) for value in raw)
        self.fixed = tuple(value * scale for value in raw)
        self.hidden = (0.0, 0.0)
        self.weights = (0.0, 0.0)
        self.tick = 0
        self.counters = dict(
            hidden_writes=0,
            learned_writes=0,
            edge_evaluations=0,
            update_slot_index_comparisons=0,
            evidence_calls=0,
        )

    def _indices(self, paths: tuple[str, ...]) -> tuple[int, ...]:
        if len(set(paths)) != len(paths):
            raise ValueError("duplicate active paths")
        if any(path not in self.path_ids for path in paths):
            raise ValueError("unknown active path")
        return tuple(self.path_ids.index(path) for path in paths)

    def advance(self, active_path_ids: tuple[str, ...] = ()) -> None:
        indices = self._indices(active_path_ids)
        if self.tick >= 64:
            raise ValueError("adapter tick budget exceeded")
        old = self.hidden
        # Fixed edge order is 0->1, 1->0; both targets use the same old state.
        self.hidden = tuple(
            0.2 * old[i] + 0.8 * math.tanh(float(i in indices) + self.fixed[1 - i] * old[1 - i])
            for i in range(2)
        )
        self.tick += 1
        self.counters["hidden_writes"] += 2
        self.counters["edge_evaluations"] += 2
        self.counters["update_slot_index_comparisons"] += sum(index + 1 for index in indices)

    def observe_causal_evidence(self, path_ids: tuple[str, ...], *, matched: bool) -> None:
        indices = self._indices(path_ids)
        if not indices or type(matched) is not bool:
            raise ValueError("nonempty eligible paths and boolean anonymous match required")
        values = list(self.weights)
        for index in indices:
            h = self.hidden[index]
            w = values[index]
            error = (1.0 if matched else -1.0) - math.tanh(w * h)
            values[index] = min(2.0, max(-2.0, w + 0.25 * error * h / (1e-8 + h * h)))
            self.counters["learned_writes"] += 1
        self.weights = tuple(values)
        self.counters["update_slot_index_comparisons"] += sum(index + 1 for index in indices)
        self.counters["evidence_calls"] += 1

    def causal_reliability(self, path_id: str) -> float:
        index = self._indices((path_id,))[0]
        return (1.0 + math.tanh(self.weights[index] * self.hidden[index])) / 2.0

    def causal_gain(self, path_id: str) -> float:
        return self.causal_reliability(path_id) * 2.0

    def learned_state_dict(self) -> dict[str, Any]:
        return {"weights": list(self.weights)}

    def state_dict(self) -> dict[str, Any]:
        return {
            "schema": "n3-causal-trace-v1",
            "path_ids": list(self.path_ids),
            "config": {
                "seed": 12001,
                "leak": 0.8,
                "input_scale": 1.0,
                "recurrent_scale": 0.75,
                "learning_rate": 0.25,
                "weight_bound": 2.0,
                "epsilon": 1e-8,
                "maximum_ticks": 64,
            },
            "edges": [[0, 1], [1, 0]],
            "fixed": list(self.fixed),
            "hidden": list(self.hidden),
            "weights": list(self.weights),
            "tick": self.tick,
            "counters": dict(self.counters),
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> N3CausalTrace:
        model = cls(tuple(value["path_ids"]))
        original = model.state_dict()
        if set(value) != set(original):
            raise ValueError("invalid checkpoint keys")
        for name in ("schema", "config", "edges", "fixed"):
            if value[name] != original[name]:
                raise ValueError("fixed configuration mismatch")
        for name, limit in (("hidden", 1.0), ("weights", 2.0)):
            vector = value[name]
            if (
                not isinstance(vector, list)
                or len(vector) != 2
                or any(
                    type(x) not in (float, int) or not math.isfinite(x) or abs(x) > limit
                    for x in vector
                )
            ):
                raise ValueError("invalid numeric vector")
            setattr(model, name, tuple(float(x) for x in vector))
        tick = value["tick"]
        if type(tick) is not int or not 0 <= tick <= 64:
            raise ValueError("invalid clock")
        counters = value["counters"]
        if set(counters) != set(model.counters) or any(
            type(x) is not int or x < 0 for x in counters.values()
        ):
            raise ValueError("invalid counters")
        if counters["hidden_writes"] != 2 * tick or counters["edge_evaluations"] != 2 * tick:
            raise ValueError("inconsistent recurrence accounting")
        model.tick = tick
        model.counters = dict(counters)
        return model


class N3LocalTemporalExpectation(A01LocalTemporalExpectation):
    """Retain common temporal proposals; replace only A01 causal support."""

    def __init__(self, base: A01LocalTemporalExpectation, path_ids: tuple[str, str]) -> None:
        super().__init__(base.config)
        restored = A01LocalTemporalExpectation.from_state_dict(base.state_dict())
        if restored._causal_support:
            raise ValueError("N3 must start without candidate causal support")
        self._transitions = restored._transitions
        self.external_transition_count = restored.external_transition_count
        self.proposal_count = restored.proposal_count
        self.trace = N3CausalTrace(path_ids)

    def observe_causal_evidence(self, path_ids: tuple[str, ...], *, matched: bool) -> None:
        self.trace.observe_causal_evidence(path_ids, matched=matched)

    def causal_reliability(self, path_id: str) -> float:
        return self.trace.causal_reliability(path_id)

    def causal_gain(self, path_id: str) -> float:
        return self.trace.causal_gain(path_id)

    def learned_state_dict(self) -> dict[str, Any]:
        value = super().learned_state_dict()
        value.pop("a01_causal_support")
        value["n3_readout"] = self.trace.learned_state_dict()
        return value

    def state_dict(self) -> dict[str, Any]:
        value = super().state_dict()
        value.pop("a01_causal_support")
        value["n3_trace"] = self.trace.state_dict()
        return value

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> N3LocalTemporalExpectation:
        base = dict(value)
        trace = N3CausalTrace.from_state_dict(base.pop("n3_trace"))
        base["a01_causal_support"] = {}
        model = cls(A01LocalTemporalExpectation.from_state_dict(base), trace.path_ids)
        model.trace = trace
        return model

    @classmethod
    def from_learned_state_dict(cls, value: dict[str, Any]) -> N3LocalTemporalExpectation:
        raise ValueError("N3 requires a full checkpoint including live hidden state")
