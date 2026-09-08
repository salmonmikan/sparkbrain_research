from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable
from typing import Any

from .worlds import CX01Family, CX01World


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _audit_high_order(world: CX01World) -> dict[str, bool]:
    _require(len(world.training) == 2, "high-order world requires two balanced histories")
    left, right = world.training
    _require(left.exposures == right.exposures, "high-order histories must be exposure balanced")
    _require(left.tokens[-1] != right.tokens[-1], "high-order targets must differ")
    _require(left.tokens[-2] == right.tokens[-2], "high-order current token must be aliased")
    _require(left.tokens[:-1] != right.tokens[:-1], "high-order histories must differ")
    _require(len(world.probes) == 2, "high-order world requires two probes")
    return {
        "balanced_histories": True,
        "first_order_alias": True,
        "distinct_targets": True,
    }


def _audit_timing(world: CX01World) -> dict[str, bool]:
    _require(len(world.training) == 2, "timing world requires two alternatives")
    left, right = world.training
    _require(left.tokens[:-1] == right.tokens[:-1], "timing alternatives must share token prefix")
    _require(left.tokens[-1] != right.tokens[-1], "timing targets must differ")
    _require(left.exposures == right.exposures, "timing alternatives must be exposure balanced")
    _require(len(world.probes) == 2, "timing world requires two probes")
    left_probe, right_probe = world.probes
    _require(left_probe.prefix == right_probe.prefix, "timing probes must share token prefix")
    _require(left_probe.lags_ms != right_probe.lags_ms, "timing probes must differ in timing")
    _require(
        math.isclose(sum(left_probe.lags_ms), sum(right_probe.lags_ms), rel_tol=0, abs_tol=1e-9),
        "timing probes must have matched total prefix duration",
    )
    return {
        "matched_total_duration": True,
        "timestamp_only_alias": True,
        "distinct_targets": True,
    }


def _audit_cycle(world: CX01World) -> dict[str, bool]:
    _require(world.cycle_cue is not None, "cycle world requires a cue")
    _require(len(world.cycle_phases) >= 7, "formal cycle requires a new multi-phase schedule")
    targets = tuple(phase.target for phase in world.cycle_phases)
    _require(len(set(targets)) >= 3, "cycle world requires at least three contingencies")
    _require(
        all(left != right for left, right in zip(targets, targets[1:], strict=False)),
        "cycle phases must represent actual contingency changes",
    )
    _require(len(set(targets)) < len(targets), "cycle world requires recurrence/re-entry")

    historical = Counter[str]()
    for row in world.training:
        if row.tokens and row.tokens[0] == world.cycle_cue:
            historical[row.tokens[-1]] += row.exposures

    # The relevant leakage question is whether the *new contingency at phase
    # entry* can be predicted from cumulative pre-phase majority alone. Count
    # current-phase exposures only after making that check; otherwise the audit
    # grants the baseline the evidence whose reacquisition is under test.
    global_majority_conflict = False
    for phase in world.cycle_phases:
        maximum = max(historical.values(), default=0)
        if maximum > 0 and historical[phase.target] < maximum:
            global_majority_conflict = True
        historical[phase.target] += phase.exposures

    _require(
        global_majority_conflict,
        "cycle world can be followed by pre-phase global historical majority at every phase",
    )
    return {
        "global_majority_conflict": True,
        "recurrent_contingency": True,
        "three_target_schedule": True,
    }


def _audit_branch(world: CX01World) -> dict[str, bool]:
    _require(len(world.training) == 3, "branch world requires three futures")
    prefixes = {row.tokens[:-1] for row in world.training}
    targets = {row.tokens[-1] for row in world.training}
    _require(len(prefixes) == 1, "branch futures must share one cue prefix")
    _require(len(targets) == 3, "branch world requires three distinct targets")
    _require(len(world.probes) == 1, "branch world requires one distribution probe")
    counts = {row.tokens[-1]: row.exposures for row in world.training}
    total = float(sum(counts.values()))
    expected = dict(world.probes[0].expected_distribution)
    _require(set(expected) == targets, "branch expected support must match trained targets")
    for target, count in counts.items():
        _require(
            math.isclose(expected[target], count / total, rel_tol=0, abs_tol=1e-12),
            "branch expected distribution must match exposure ratios",
        )
    return {
        "multi_future_support": True,
        "shared_prefix": True,
        "exposure_distribution_bound": True,
    }


def _audit_selectivity(world: CX01World) -> dict[str, bool]:
    main = world.intervention_main
    control = world.intervention_control
    _require(main and control, "selectivity world requires main and control paths")
    _require(set(main).isdisjoint(control), "selectivity paths must be disjoint")
    _require(len(main) == len(control), "selectivity paths must have matched lengths")
    _require(len(world.training) == 2, "selectivity world requires two training paths")
    left, right = world.training
    _require(left.tokens == main and right.tokens == control, "selectivity training paths mismatch")
    _require(left.exposures == right.exposures, "selectivity exposure budgets must match")
    _require(left.lags_ms == right.lags_ms, "selectivity path timing must match")
    return {
        "disjoint_paths": True,
        "matched_exposure": True,
        "matched_timing": True,
    }


def _audit_loop(world: CX01World) -> dict[str, bool]:
    _require(world.loop is not None, "loop world requires provenance specification")
    _require(len(world.training) == 1, "loop world requires one external training sequence")
    sequence = world.training[0].tokens
    cue = world.loop.cue_prefix
    index = len(cue)
    _require(sequence[:index] == cue, "loop cue must be a strict training prefix")
    _require(index + 1 < len(sequence), "loop requires generated event then later external event")
    _require(
        sequence[index] == world.loop.expected_generated,
        "loop expected generated event must immediately follow cue in external history",
    )
    _require(
        sequence[index + 1] == world.loop.external_consequence,
        "loop external consequence must follow the generated proposal position",
    )
    _require(
        world.loop.expected_generated != world.loop.external_consequence,
        "loop generated proposal and external consequence must remain distinct",
    )
    return {
        "generated_external_distinct": True,
        "ordered_provenance_loop": True,
        "strict_cue_prefix": True,
    }


def audit_formal_world_identifiability(world: CX01World) -> dict[str, Any]:
    world.validate()
    auditors = {
        CX01Family.HIGH_ORDER: _audit_high_order,
        CX01Family.TIMING: _audit_timing,
        CX01Family.CYCLE: _audit_cycle,
        CX01Family.BRANCH: _audit_branch,
        CX01Family.SELECTIVITY: _audit_selectivity,
        CX01Family.LOOP: _audit_loop,
    }
    gates = auditors[world.family](world)
    return {
        "family": world.family.value,
        "gates": gates,
        "passed": all(gates.values()),
        "seed": world.seed,
    }


def audit_formal_grid_identifiability(worlds: Iterable[CX01World]) -> dict[str, Any]:
    rows = tuple(audit_formal_world_identifiability(world) for world in worlds)
    if not rows:
        raise ValueError("formal identifiability audit requires worlds")
    by_family = {
        family.value: sum(row["passed"] for row in rows if row["family"] == family.value)
        for family in CX01Family
    }
    counts = {
        family.value: sum(row["family"] == family.value for row in rows) for family in CX01Family
    }
    if any(by_family[family.value] != counts[family.value] for family in CX01Family):
        raise RuntimeError("formal grid contains an identifiability failure")
    return {
        "family_pass_counts": by_family,
        "family_world_counts": counts,
        "world_count": len(rows),
    }
