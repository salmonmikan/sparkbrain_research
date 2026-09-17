#!/usr/bin/env python3
"""
EXPLORATORY / NON_EVIDENTIARY.

Bounded synthetic feasibility probe for an explicit revision-authority
finite-state reducer. This is not a formal SparkBrain experiment, does not
consume an identity, and must not be treated as scientific evidence.

Question:
Can a history-sensitive revision policy be represented exactly by a tiny
explicit finite-state controller when the task semantics are source authority
plus assertion/retraction?

Synthetic setup:
- three fixed authority-ranked sources: low < mid < high
- each source can assert -1/+1, retract, or receive an irrelevant event
- the reference policy replays full history, keeps the latest active assertion
  per source, and emits the highest-authority active assertion
- the finite-state reducer stores only the active assertion per source
- a stateless baseline sees only the current event

The point is reduction feasibility, not realism: the synthetic reference policy
is deliberately chosen so an explicit-state reduction can be tested exactly.
"""

from __future__ import annotations

import json
import random
from itertools import product

SOURCES = ("low", "mid", "high")
RANK = {"low": 1, "mid": 2, "high": 3}
EVENTS = tuple(
    [("assert", source, sign) for source in SOURCES for sign in (-1, 1)]
    + [("retract", source, 0) for source in SOURCES]
    + [("irrelevant", "none", 0)]
)


def reference_full_history(history):
    active = {source: 0 for source in SOURCES}
    for kind, source, sign in history:
        if kind == "assert":
            active[source] = sign
        elif kind == "retract":
            active[source] = 0
    for source in sorted(SOURCES, key=RANK.__getitem__, reverse=True):
        if active[source] != 0:
            return active[source]
    return 0


def fsa_step(state, event):
    active = dict(zip(SOURCES, state, strict=True))
    kind, source, sign = event
    if kind == "assert":
        active[source] = sign
    elif kind == "retract":
        active[source] = 0
    return tuple(active[source] for source in SOURCES)


def fsa_output(state):
    active = dict(zip(SOURCES, state, strict=True))
    for source in sorted(SOURCES, key=RANK.__getitem__, reverse=True):
        if active[source] != 0:
            return active[source]
    return 0


def stateless_output(event):
    kind, _, sign = event
    return sign if kind == "assert" else 0


def run():
    max_exhaustive_horizon = 5
    histories_checked = 0
    fsa_matches = 0
    stateless_matches = 0
    reachable_states = set()
    first_stateless_counterexample = None

    for horizon in range(max_exhaustive_horizon + 1):
        for history in product(EVENTS, repeat=horizon):
            histories_checked += 1
            state = (0, 0, 0)
            for event in history:
                state = fsa_step(state, event)
            reachable_states.add(state)

            expected = reference_full_history(history)
            reduced = fsa_output(state)
            fsa_matches += expected == reduced

            baseline = 0 if not history else stateless_output(history[-1])
            stateless_matches += expected == baseline
            if first_stateless_counterexample is None and expected != baseline and history:
                first_stateless_counterexample = {
                    "history": [list(event) for event in history],
                    "reference_output": expected,
                    "stateless_output": baseline,
                    "fsa_state": list(state),
                }

    rng = random.Random(170917)
    long_horizon = {}
    for horizon in (10, 25, 50):
        samples = 20_000
        exact = 0
        baseline = 0
        states = set()
        for _ in range(samples):
            history = tuple(rng.choice(EVENTS) for _ in range(horizon))
            state = (0, 0, 0)
            for event in history:
                state = fsa_step(state, event)
            states.add(state)
            expected = reference_full_history(history)
            exact += expected == fsa_output(state)
            baseline += expected == stateless_output(history[-1])
        long_horizon[str(horizon)] = {
            "samples": samples,
            "fsa_exact_match_rate": exact / samples,
            "stateless_match_rate": baseline / samples,
            "reachable_fsa_states_seen": len(states),
        }

    result = {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "question": (
            "Can a source-authority assertion/retraction policy with history "
            "dependence be represented exactly by a bounded explicit FSA?"
        ),
        "synthetic_contract": {
            "sources": list(SOURCES),
            "authority_order": list(SOURCES),
            "event_alphabet_size": len(EVENTS),
            "fsa_state_definition": "one ternary active-claim slot {-1,0,+1} per source",
            "maximum_fsa_states": 3 ** len(SOURCES),
        },
        "exhaustive": {
            "max_horizon": max_exhaustive_horizon,
            "histories_checked": histories_checked,
            "fsa_exact_matches": fsa_matches,
            "fsa_exact_match_rate": fsa_matches / histories_checked,
            "stateless_matches": stateless_matches,
            "stateless_match_rate": stateless_matches / histories_checked,
            "reachable_fsa_states": len(reachable_states),
            "first_stateless_counterexample": first_stateless_counterexample,
        },
        "long_horizon_random_checks": long_horizon,
        "interpretation": (
            "Within this deliberately simplified synthetic revision-authority "
            "world, full-history behavior compresses exactly into 27 explicit "
            "states independent of horizon, while a current-event-only baseline "
            "fails frequently. This supports testing explicit-state/FSA "
            "reductions prospectively before attributing history-sensitive gains "
            "to richer persistent dynamics. It is not evidence about C19, "
            "Belief-R, or SparkBrain."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
