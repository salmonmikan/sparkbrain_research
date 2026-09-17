#!/usr/bin/env python3
"""EXPLORATORY / NON_EVIDENTIARY provenance-sensitive revision-state stress.

Synthetic-only diagnostic. It is not formal evidence and must not be used to
support SparkBrain/C19/Belief-R claims or satisfy any scientific gate.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from pathlib import Path

VALUES = (-1, 0, 1)


def aggregate(state: tuple[int, ...]) -> int:
    has_pos = 1 in state
    has_neg = -1 in state
    if has_pos == has_neg:
        return 0
    return 1 if has_pos else -1


def apply_exact(state: tuple[int, ...], event: tuple[int, int]) -> tuple[int, ...]:
    idx, value = event
    out = list(state)
    out[idx] = value
    return tuple(out)


def replay_exact(token_count: int, history: list[tuple[int, int]]) -> int:
    state = (0,) * token_count
    for event in history:
        state = apply_exact(state, event)
    return aggregate(state)


def apply_source_only(
    state: tuple[int, ...], event: tuple[int, int], per_source: int
) -> tuple[int, ...]:
    idx, value = event
    source = idx // per_source
    out = list(state)
    # Deliberately compact comparator: provenance-specific retraction clears
    # the source because provenance identity is not represented.
    out[source] = value
    return tuple(out)


def reachable_counts(token_count: int, max_horizon: int) -> list[dict[str, int]]:
    events = [(i, v) for i in range(token_count) for v in VALUES]
    current = {(0,) * token_count}
    result = []
    for horizon in range(max_horizon + 1):
        formula = sum(
            math.comb(token_count, j) * (2**j)
            for j in range(min(token_count, horizon) + 1)
        )
        result.append(
            {
                "horizon": horizon,
                "reachable": len(current),
                "closed_form": formula,
            }
        )
        nxt = set(current)
        for state in current:
            for event in events:
                nxt.add(apply_exact(state, event))
        current = nxt
    return result


def minimal_moore_states(token_count: int) -> int:
    states = list(itertools.product(VALUES, repeat=token_count))
    index = {state: i for i, state in enumerate(states)}
    events = [(i, v) for i in range(token_count) for v in VALUES]
    transitions = [
        [index[apply_exact(state, event)] for event in events]
        for state in states
    ]

    output_labels = [aggregate(state) for state in states]
    unique_outputs = {value: i for i, value in enumerate(sorted(set(output_labels)))}
    blocks = [unique_outputs[value] for value in output_labels]
    while True:
        sig_to_block: dict[tuple[int, tuple[int, ...]], int] = {}
        next_blocks: list[int] = []
        for state_i, state in enumerate(states):
            signature = (
                aggregate(state),
                tuple(blocks[next_i] for next_i in transitions[state_i]),
            )
            if signature not in sig_to_block:
                sig_to_block[signature] = len(sig_to_block)
            next_blocks.append(sig_to_block[signature])
        same_partition = all(
            (blocks[i] == blocks[j]) == (next_blocks[i] == next_blocks[j])
            for i in range(len(states))
            for j in range(i)
        )
        if same_partition:
            return len(set(next_blocks))
        blocks = next_blocks


def random_agreement(
    source_count: int, per_source: int, horizon: int, samples: int, seed: int
) -> dict[str, float | int]:
    rng = random.Random(seed)
    token_count = source_count * per_source
    exact_matches = 0
    source_matches = 0
    for _ in range(samples):
        history = [
            (rng.randrange(token_count), rng.choice(VALUES)) for _ in range(horizon)
        ]
        exact_state = (0,) * token_count
        source_state = (0,) * source_count
        for event in history:
            exact_state = apply_exact(exact_state, event)
            source_state = apply_source_only(source_state, event, per_source)
        reference = replay_exact(token_count, history)
        exact_matches += aggregate(exact_state) == reference
        source_matches += aggregate(source_state) == reference
    return {
        "sources": source_count,
        "provenances_per_source": per_source,
        "horizon": horizon,
        "samples": samples,
        "exact_incremental_match_rate": exact_matches / samples,
        "source_only_match_rate": source_matches / samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260917)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    reachable = {}
    moore = {}
    for tokens in range(1, 7):
        reachable[str(tokens)] = reachable_counts(tokens, max_horizon=tokens + 2)
        moore[str(tokens)] = {
            "nominal_token_states": 3**tokens,
            "minimal_output_equivalent_moore_states": minimal_moore_states(tokens),
        }

    random_checks = []
    for sources in (1, 2, 3):
        for per_source in (1, 2):
            for horizon in (10, 25, 50):
                random_checks.append(
                    random_agreement(
                        sources,
                        per_source,
                        horizon,
                        args.samples,
                        args.seed + sources * 1000 + per_source * 100 + horizon,
                    )
                )

    witness_history = [(0, 1), (1, 1), (0, 0)]
    witness_exact = replay_exact(2, witness_history)
    source_state = (0,)
    for event in witness_history:
        source_state = apply_source_only(source_state, event, per_source=2)

    result = {
        "label": "EXPLORATORY / NON_EVIDENTIARY",
        "question": (
            "How does exact explicit state grow when same-rank conflicts and "
            "provenance-sensitive retractions require provenance memory?"
        ),
        "semantics": {
            "token_state": [-1, 0, 1],
            "all_sources_same_authority_rank": True,
            "retraction_targets_specific_provenance": True,
            "aggregate": (
                "positive-only=>+1; negative-only=>-1; "
                "empty or mixed-sign conflict=>0"
            ),
            "source_only_comparator": (
                "one trit per source; a provenance-targeted retract clears the entire "
                "source because provenance is unrepresented"
            ),
        },
        "reachable_state_growth": reachable,
        "moore_minimization": moore,
        "random_agreement": random_checks,
        "deterministic_provenance_witness": {
            "sources": 1,
            "provenances_per_source": 2,
            "history": witness_history,
            "exact_output": witness_exact,
            "source_only_output": aggregate(source_state),
        },
        "evidentiary_status": "NON_EVIDENTIARY",
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
