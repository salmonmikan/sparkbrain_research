"""Synthetic causal-opportunity diagnostic for noncanonical Forge work.

This tool is deliberately NON_EVIDENTIARY and NONCANONICAL. It does not read
Candidate 35 artifacts, protected evaluators, held-out payloads, formal results,
or historical R100 outcomes. It only checks a prospectively supplied toy graph
for two ordinary failure modes relevant to rough Forge screening:

1. no treated-node -> declared-observable causal path within a fixed horizon;
2. a reachable observable whose fixed linear readout is null/cancelling for the
   treated-state perturbation.

A passing diagnostic is not scientific evidence and is not a promotion signal.
It only says that these two simple screening failures were not reproduced by the
supplied synthetic graph.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    gain: float


@dataclass(frozen=True)
class Diagnostic:
    has_causal_path: bool
    max_abs_readout_effect: float
    sensitivity_pass: bool
    disposition: str
    evidentiary_status: str = "NON_EVIDENTIARY_NONCANONICAL"
    promotion_support_signal: bool = False


def diagnose_causal_opportunity(
    *,
    edges: Sequence[Edge],
    treated_node: str,
    readout_weights: Mapping[str, float],
    horizon: int = 6,
    treated_shift: float = 1.0,
    sensitivity_floor: float = 1e-9,
) -> Diagnostic:
    """Check fixed-path reachability and fixed-readout sensitivity.

    The propagation is intentionally minimal: each step sends the current delta
    through fixed weighted edges. There is no fitting, threshold search, timing
    search, cue search, or result-responsive retuning.
    """
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    if sensitivity_floor < 0:
        raise ValueError("sensitivity_floor must be >= 0")

    adjacency: dict[str, list[Edge]] = {}
    for edge in edges:
        if edge.gain != 0.0:
            adjacency.setdefault(edge.source, []).append(edge)

    declared_readout_nodes = {
        node for node, weight in readout_weights.items() if weight != 0.0
    }

    frontier = {treated_node}
    seen = {treated_node}
    has_causal_path = treated_node in declared_readout_nodes
    for _ in range(horizon):
        next_frontier: set[str] = set()
        for node in frontier:
            for edge in adjacency.get(node, ()):
                if edge.target in declared_readout_nodes:
                    has_causal_path = True
                if edge.target not in seen:
                    seen.add(edge.target)
                    next_frontier.add(edge.target)
        frontier = next_frontier
        if not frontier:
            break

    state: dict[str, float] = {treated_node: treated_shift}
    readout_effects: list[float] = []
    for _ in range(horizon + 1):
        readout_effects.append(
            sum(state.get(node, 0.0) * weight for node, weight in readout_weights.items())
        )
        next_state: dict[str, float] = {}
        for source, value in state.items():
            for edge in adjacency.get(source, ()):
                next_state[edge.target] = next_state.get(edge.target, 0.0) + value * edge.gain
        state = next_state

    max_abs_readout_effect = max(abs(value) for value in readout_effects)
    sensitivity_pass = has_causal_path and max_abs_readout_effect >= sensitivity_floor

    if not has_causal_path:
        disposition = "NO_PROSPECTIVE_TREATED_TO_OBSERVABLE_CAUSAL_PATH"
    elif not sensitivity_pass:
        disposition = "OUTPUT_NULL_OR_CANCELLING_READOUT_PROJECTION"
    else:
        disposition = "CAUSAL_OPPORTUNITY_AND_FIXED_SENSITIVITY_PRESENT"

    return Diagnostic(
        has_causal_path=has_causal_path,
        max_abs_readout_effect=max_abs_readout_effect,
        sensitivity_pass=sensitivity_pass,
        disposition=disposition,
    )


def _load_case(path: Path) -> tuple[list[Edge], str, dict[str, float], int, float, float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    edges = [Edge(str(item["source"]), str(item["target"]), float(item["gain"])) for item in payload["edges"]]
    return (
        edges,
        str(payload["treated_node"]),
        {str(node): float(weight) for node, weight in payload["readout_weights"].items()},
        int(payload.get("horizon", 6)),
        float(payload.get("treated_shift", 1.0)),
        float(payload.get("sensitivity_floor", 1e-9)),
    )


def _self_test() -> None:
    sensitive = diagnose_causal_opportunity(
        edges=[Edge("treated", "downstream", 0.5)],
        treated_node="treated",
        readout_weights={"downstream": 1.0},
        horizon=3,
        sensitivity_floor=0.1,
    )
    assert sensitive.has_causal_path
    assert sensitive.sensitivity_pass
    assert sensitive.disposition == "CAUSAL_OPPORTUNITY_AND_FIXED_SENSITIVITY_PRESENT"

    unreachable = diagnose_causal_opportunity(
        edges=[Edge("treated", "downstream", 0.5)],
        treated_node="treated",
        readout_weights={"unrelated": 1.0},
        horizon=3,
        sensitivity_floor=0.1,
    )
    assert not unreachable.has_causal_path
    assert unreachable.disposition == "NO_PROSPECTIVE_TREATED_TO_OBSERVABLE_CAUSAL_PATH"

    cancelled = diagnose_causal_opportunity(
        edges=[Edge("treated", "left", 1.0), Edge("treated", "right", 1.0)],
        treated_node="treated",
        readout_weights={"left": 1.0, "right": -1.0},
        horizon=2,
        sensitivity_floor=0.1,
    )
    assert cancelled.has_causal_path
    assert not cancelled.sensitivity_pass
    assert cancelled.disposition == "OUTPUT_NULL_OR_CANCELLING_READOUT_PROJECTION"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", type=Path, help="JSON synthetic case")
    parser.add_argument("--self-test", action="store_true", help="run deterministic toy checks")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        print(json.dumps({"self_test": "PASS", "evidentiary_status": "NON_EVIDENTIARY"}))
        return
    if args.case is None:
        parser.error("provide a JSON case or --self-test")

    edges, treated_node, readout_weights, horizon, treated_shift, sensitivity_floor = _load_case(
        args.case
    )
    diagnostic = diagnose_causal_opportunity(
        edges=edges,
        treated_node=treated_node,
        readout_weights=readout_weights,
        horizon=horizon,
        treated_shift=treated_shift,
        sensitivity_floor=sensitivity_floor,
    )
    print(json.dumps(asdict(diagnostic), sort_keys=True))


if __name__ == "__main__":
    main()
