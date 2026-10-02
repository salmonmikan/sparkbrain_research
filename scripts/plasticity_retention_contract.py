"""Pure retention accounting/scoring helpers; no SparkBrain imports or model execution."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


class OutputWriter:
    """All limits are within the protocol total, including bounded terminal metadata."""

    def __init__(self, root: Path, *, terminal_limit: int, live: Callable[[], None] = lambda: None):
        self.root = root.resolve()
        self.terminal_limit = terminal_limit
        self.terminal_written = 0
        self.live = live
        self.measurement_failed = False

    def total(self) -> int:
        return sum(path.stat().st_size for path in self.root.rglob("*") if path.is_file())

    def raw(self, path: Path, data: bytes, *, append: bool = False, terminal: bool = False) -> None:
        if not terminal:
            self.live()
            require(not self.measurement_failed, "measurement failure latched")
        target = path.resolve()
        require(target.is_relative_to(self.root) and not path.is_symlink(), "output escaped root")
        cap = (256 if terminal else 252) * 1024**2
        if terminal:
            require(self.terminal_written + len(data) <= self.terminal_limit, "terminal allowance")
        require(self.total() + len(data) <= cap, "output admission ceiling exceeded")
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("ab" if append else "xb") as stream:
                stream.write(data)
                stream.flush()
                import os

                os.fsync(stream.fileno())
        except BaseException:
            self.measurement_failed = True
            raise
        if terminal:
            self.terminal_written += len(data)

    def json(self, path: Path, value: Any, *, append: bool = False, terminal: bool = False) -> None:
        try:
            self.raw(path, canonical(value), append=append, terminal=terminal)
        except BaseException:
            if not terminal:
                self.measurement_failed = True
            raise


class CallLedger:
    """Intent and observed completion are separate; failed observation blocks the next call."""

    def __init__(self, emit: Callable[[dict[str, Any]], None], limits: dict[str, int]):
        self.emit = emit
        self.limits = limits
        self.intents: Counter[str] = Counter()
        self.returns: Counter[str] = Counter()
        self.errors: Counter[str] = Counter()
        self.observation_failed = False
        self.events: list[dict[str, Any]] = []
        self.depth = 0

    def event(self, value: dict[str, Any], *, after: bool = False) -> None:
        self.events.append(value)
        try:
            self.emit(value)
        except (TimeoutError, MemoryError):
            raise
        except BaseException:
            self.observation_failed = True
            if not after:
                raise

    def call(self, kind: str, function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        # An observation failure cannot replace an admitted outer method's result.
        # Its nested operations finish; the next top-level method is prohibited.
        require(
            self.depth > 0 or not self.observation_failed,
            "no next method after observation failure",
        )
        require(kind in self.limits and self.intents[kind] < self.limits[kind], "method limit")
        number = self.intents[kind] + 1
        self.event({"kind": kind, "phase": "intent", "number": number}, after=self.depth > 0)
        self.intents[kind] += 1
        self.depth += 1
        try:
            try:
                value = function(*args, **kwargs)
            except BaseException as exc:
                self.errors[kind] += 1
                self.event(
                    {
                        "kind": kind,
                        "phase": "error",
                        "number": number,
                        "error_type": type(exc).__name__,
                        "error": str(exc)[:4096],
                    },
                    after=True,
                )
                raise
            self.returns[kind] += 1
            self.event({"kind": kind, "phase": "return", "number": number}, after=True)
            return value
        finally:
            self.depth -= 1

    def require_observed(self) -> None:
        require(not self.observation_failed, "method completed but observation failed")

    def summary(self) -> dict[str, Any]:
        return {
            "intents": dict(self.intents),
            "returns": dict(self.returns),
            "errors": dict(self.errors),
            "observation_failed": self.observation_failed,
            "intent_boundary": "an interrupted intent is not proof of method entry/completion",
        }


def audit_apply_before(field: Any, spikes: Any, controller: Any) -> dict[str, Any]:
    """Read-only arithmetic observer; it does not call apply or mutate any model object."""
    cfg = controller.config
    by_unit: dict[int, list[float]] = {}
    for row in sorted(spikes, key=lambda x: (x.time_ms, x.unit_id)):
        by_unit.setdefault(row.unit_id, []).append(row.time_ms)
    before_e = dict(controller.eligibility)
    expected_e = {
        key: value * cfg.eligibility_decay
        for key, value in before_e.items()
        if abs(value * cfg.eligibility_decay) >= 1e-8
    }
    updates = []
    before_weights = {f"{s}:{t}": edge.weight for (s, t), edge in field.connections.items()}
    before_delays = {f"{s}:{t}": edge.delay_ms for (s, t), edge in field.connections.items()}
    pair_work = 0
    for edge_key in sorted(field.connections):
        if len(updates) >= cfg.max_updates_per_step:
            break
        edge = field.connections[edge_key]
        if not edge.plastic:
            continue
        pre, post = by_unit.get(edge.source_id, ()), by_unit.get(edge.target_id, ())
        if not pre or not post:
            continue
        delta = 0.0
        for t0 in pre:
            for t1 in post:
                pair_work += 1
                lag = t1 - t0
                if lag > 0:
                    delta += math.exp(-lag / cfg.tau_plus_ms)
                elif lag < 0:
                    delta -= cfg.depression_ratio * math.exp(lag / cfg.tau_minus_ms)
        if delta == 0.0:
            continue
        key = f"{edge.source_id}:{edge.target_id}"
        carry = expected_e.get(key, 0.0)
        eligibility = carry + delta
        expected_e[key] = eligibility
        proposal = edge.weight + cfg.learning_rate * controller.reward_trace * eligibility
        expected_weight = max(cfg.min_weight, min(cfg.max_weight, proposal))
        if not cfg.enable_weight_learning:
            expected_weight = edge.weight
        updates.append(
            {
                "edge": key,
                "pre_eligibility": before_e.get(key, 0.0),
                "decayed_carry": carry,
                "current_delta": delta,
                "eligibility_after": eligibility,
                "weight_before": edge.weight,
                "unclipped_proposal": proposal,
                "weight_expected": expected_weight,
                "weight_write_enabled": cfg.enable_weight_learning,
                "clipped": bool(cfg.enable_weight_learning and expected_weight != proposal),
            }
        )
    return {
        "pre_eligibility": before_e,
        "expected_eligibility": expected_e,
        "weights_before": before_weights,
        "delays_before": before_delays,
        "update_count_before": controller.update_count,
        "updates": updates,
        "observer_pair_evaluations": pair_work,
    }


def audit_apply_after(
    audit: dict[str, Any], field: Any, controller: Any, returned: int
) -> dict[str, Any]:
    require(
        controller.eligibility == audit["expected_eligibility"], "eligibility observer mismatch"
    )
    require(
        returned == len(audit["updates"])
        and controller.update_count == audit["update_count_before"] + returned,
        "apply/work count mismatch",
    )
    actual_weights = {f"{s}:{t}": edge.weight for (s, t), edge in field.connections.items()}
    actual_delays = {f"{s}:{t}": edge.delay_ms for (s, t), edge in field.connections.items()}
    expected = dict(audit["weights_before"])
    for row in audit["updates"]:
        expected[row["edge"]] = row["weight_expected"]
        row["actual_delta_weight"] = actual_weights[row["edge"]] - row["weight_before"]
    require(actual_weights == expected, "actual weight writes differ from observed rule")
    require(actual_delays == audit["delays_before"], "delay write in fixed-delay study")
    return {
        "pre_eligibility": audit["pre_eligibility"],
        "post_eligibility": dict(controller.eligibility),
        "updates": audit["updates"],
        "actual_weight_abs_change": math.fsum(
            abs(row["actual_delta_weight"]) for row in audit["updates"]
        ),
        "actual_weight_signed_change": math.fsum(
            row["actual_delta_weight"] for row in audit["updates"]
        ),
        "changed_weights": sum(row["actual_delta_weight"] != 0 for row in audit["updates"]),
        "clipped_weights": sum(row["clipped"] for row in audit["updates"]),
        "delays_unchanged": True,
        "delay_map_sha256": digest(actual_delays),
        "observer_pair_evaluations": audit["observer_pair_evaluations"],
        "eligible_edge_work": returned,
        "extra_apply_calls": 0,
    }


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(bool(rows), "empty scored rows")
    for row in rows:
        require(type(row["outcome"]) is int and row["outcome"] in (0, 1), "outcome type")
        require(
            type(row["p1"]) in (int, float) and math.isfinite(row["p1"]) and 0 <= row["p1"] <= 1,
            "probability invalid",
        )
        require(
            row["native"] is None or (type(row["native"]) is int and row["native"] in (0, 1)),
            "native decision type",
        )
    n = len(rows)
    correct = sum(row["native"] == row["outcome"] for row in rows)
    selected = sum(row["native"] is not None for row in rows)
    calibration = []
    for lower, upper in zip((0.0, 0.25, 0.5, 0.75), (0.25, 0.5, 0.75, 1.0), strict=True):
        group = [r for r in rows if lower <= r["p1"] < upper or (upper == 1 and r["p1"] == 1)]
        calibration.append(
            {
                "lower": lower,
                "upper": upper,
                "count": len(group),
                "mean_probability": math.fsum(r["p1"] for r in group) / len(group)
                if group
                else None,
                "outcome_fraction": sum(r["outcome"] for r in group) / len(group)
                if group
                else None,
            }
        )
    return {
        "n": n,
        "brier": math.fsum((r["p1"] - r["outcome"]) ** 2 for r in rows) / n,
        "correct": correct,
        "wrong": selected - correct,
        "abstain": n - selected,
        "coverage": selected / n,
        "correct_per_total": correct / n,
        "correct_per_nonabstaining": correct / selected if selected else None,
        "calibration": calibration,
        "first": {k: rows[0][k] for k in ("p1", "native", "outcome")},
    }


def evaluate_fixture(
    rows: dict[str, dict[str, list[dict[str, Any]]]], protocol: dict[str, Any]
) -> dict:
    values = {
        condition: {arm: metrics(records) for arm, records in arms.items()}
        for condition, arms in rows.items()
    }
    c, local, gain = (values["return"][arm] for arm in ("C", "L", "G"))
    primary = (
        c["brier"] - local["brier"] >= 0.02
        and local["correct"] >= c["correct"]
        and local["coverage"] >= c["coverage"]
    )
    secondary = gain["brier"] - local["brier"] >= 0.02
    c, local = (values["stationary"][arm] for arm in ("C", "L"))
    stationary = (
        local["brier"] - c["brier"] <= 0.02
        and local["correct"] >= c["correct"] - 1
        and local["coverage"] >= c["coverage"]
    )
    novel = rows["novel"]["L"]
    require(len(novel) == 32, "novel row count")
    early, late, control = (
        metrics(novel[:16]),
        metrics(novel[16:]),
        metrics(rows["novel"]["C"][16:]),
    )
    require(
        Counter(r["outcome"] for r in novel[:16]) == Counter({0: 8, 1: 8})
        and Counter(r["outcome"] for r in novel[16:]) == Counter({0: 8, 1: 8}),
        "novel balance",
    )
    ceiling = early["correct"] >= 15 or early["brier"] < 0.02
    acquisition = (
        early["brier"] - late["brier"] >= 0.02
        and late["correct"] - early["correct"] >= 2
        and late["coverage"] >= early["coverage"]
        and late["correct"] >= 12
        and all(
            sum(r["native"] == label for r in novel[16:] if r["outcome"] == label) >= 6
            for label in (0, 1)
        )
        and math.fsum(r.get("actual_weight_abs_change", 0) for r in novel) > 0
    )
    preservation = (
        late["brier"] - control["brier"] <= 0.02
        and late["correct"] >= control["correct"] - 1
        and late["coverage"] >= control["coverage"]
    )
    return {
        "metrics": values,
        "novel_early": early,
        "novel_late": late,
        "primary_C_L": primary,
        "secondary_G_L": secondary,
        "stationary_preserved": stationary,
        "novel_ceiling_inconclusive": ceiling,
        "novel_acquisition": acquisition,
        "novel_preserved": preservation,
        "bounded_gate": bool(
            primary and secondary and stationary and acquisition and preservation and not ceiling
        ),
        "scientific_credit": protocol["scientific_credit"],
        "claim_limit": (
            "conditional exposed-fixture comparison; no general or unique-mediation claim"
        ),
    }
