"""EXPLORATORY / NON_EVIDENTIARY H3 correlation-aware reduction probe.

This module uses synthetic data only. It does not open, score, or reinterpret any
formal SparkBrain experiment. The goal is to test whether robustness that could
look "coalition-like" can be reproduced by ordinary provenance-aware scalar
aggregation when the comparator receives the same correlation-group information.
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceMessage:
    group_id: int
    source_id: int
    sign: int


def _binary_sign(score: float) -> int:
    return 1 if score >= 0.0 else -1


def predict_naive(messages: list[EvidenceMessage]) -> int:
    """Count every delivered message independently."""
    return _binary_sign(sum(message.sign for message in messages))


def _unique_source_votes(messages: list[EvidenceMessage]) -> dict[tuple[int, int], int]:
    votes: dict[tuple[int, int], int] = {}
    for message in messages:
        key = (message.group_id, message.source_id)
        previous = votes.get(key)
        if previous is not None and previous != message.sign:
            raise ValueError("A synthetic source emitted inconsistent exact duplicates.")
        votes[key] = message.sign
    return votes


def predict_source_dedup(messages: list[EvidenceMessage]) -> int:
    """Collapse exact duplicate deliveries but still count correlated sources separately."""
    return _binary_sign(sum(_unique_source_votes(messages).values()))


def _group_votes(messages: list[EvidenceMessage]) -> dict[int, list[int]]:
    groups: dict[int, list[int]] = {}
    for (group_id, _source_id), sign in _unique_source_votes(messages).items():
        groups.setdefault(group_id, []).append(sign)
    return groups


def predict_group_normalized(messages: list[EvidenceMessage]) -> int:
    """Ordinary scalar reduction: each known correlation group contributes unit mass."""
    groups = _group_votes(messages)
    score = sum(sum(votes) / len(votes) for votes in groups.values())
    return _binary_sign(score)


def predict_group_majority(messages: list[EvidenceMessage]) -> int:
    """Coalition-style proxy: one majority vote per known correlation group."""
    groups = _group_votes(messages)
    group_decisions = [_binary_sign(sum(votes)) for votes in groups.values()]
    return _binary_sign(sum(group_decisions))


Predictor = Callable[[list[EvidenceMessage]], int]


def _synthetic_examples(samples: int, seed: int) -> list[tuple[int, list[EvidenceMessage]]]:
    rng = random.Random(seed)
    member_patterns = (
        (1, 1, 1, 1, 1),
        (1, 1, 2, 4, 8),
        (8, 4, 2, 1, 1),
        (1, 2, 4, 8, 16),
    )
    duplicate_pattern = (1, 1, 2, 4)
    examples: list[tuple[int, list[EvidenceMessage]]] = []

    for example_index in range(samples):
        truth = rng.choice((-1, 1))
        members_per_group = member_patterns[example_index % len(member_patterns)]
        messages: list[EvidenceMessage] = []

        for group_id, member_count in enumerate(members_per_group):
            latent_sign = truth if rng.random() < 0.70 else -truth
            for source_id in range(member_count):
                source_sign = latent_sign if rng.random() < 0.90 else -latent_sign
                duplicates = duplicate_pattern[
                    (example_index + 3 * group_id + source_id) % len(duplicate_pattern)
                ]
                messages.extend(
                    EvidenceMessage(group_id, source_id, source_sign)
                    for _ in range(duplicates)
                )

        examples.append((truth, messages))

    return examples


def _accuracy(
    examples: list[tuple[int, list[EvidenceMessage]]],
    predictor: Predictor,
) -> float:
    correct = sum(predictor(messages) == truth for truth, messages in examples)
    return correct / len(examples)


def _adversarial_correlated_sweep() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    predictors: dict[str, Predictor] = {
        "naive": predict_naive,
        "source_dedup": predict_source_dedup,
        "group_normalized": predict_group_normalized,
        "group_majority": predict_group_majority,
    }

    for correlated_members in (1, 2, 4, 8, 16):
        messages = [
            EvidenceMessage(group_id=0, source_id=source_id, sign=-1)
            for source_id in range(correlated_members)
        ]
        messages.extend(
            (
                EvidenceMessage(group_id=1, source_id=0, sign=1),
                EvidenceMessage(group_id=2, source_id=0, sign=1),
            )
        )
        row = {"correlated_wrong_sources": correlated_members}
        row.update({name: predictor(messages) for name, predictor in predictors.items()})
        rows.append(row)

    return rows


def run_probe(samples: int = 4096, seed: int = 1337) -> dict[str, object]:
    examples = _synthetic_examples(samples=samples, seed=seed)
    predictors: dict[str, Predictor] = {
        "naive": predict_naive,
        "source_dedup": predict_source_dedup,
        "group_normalized": predict_group_normalized,
        "group_majority": predict_group_majority,
    }
    accuracy = {
        name: _accuracy(examples, predictor)
        for name, predictor in predictors.items()
    }
    group_agreement = sum(
        predict_group_normalized(messages) == predict_group_majority(messages)
        for _truth, messages in examples
    ) / len(examples)

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "question": (
            "Can duplicate/correlation robustness that looks coalition-like be reproduced "
            "by an ordinary provenance-aware scalar reduction when the comparator receives "
            "the same correlation-group information?"
        ),
        "synthetic_contract": {
            "samples": samples,
            "seed": seed,
            "latent_group_truth_probability": 0.70,
            "within_group_source_agreement_probability": 0.90,
            "groups_per_example": 5,
            "member_patterns": [
                [1, 1, 1, 1, 1],
                [1, 1, 2, 4, 8],
                [8, 4, 2, 1, 1],
                [1, 2, 4, 8, 16],
            ],
            "exact_duplicate_pattern": [1, 1, 2, 4],
        },
        "accuracy": accuracy,
        "group_normalized_vs_group_majority_agreement": group_agreement,
        "adversarial_correlated_sweep": _adversarial_correlated_sweep(),
        "interpretation_boundary": (
            "Known correlation-group IDs are privileged synthetic information. "
            "The probe tests a reduction possibility, not H3 itself."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=1337)
    args = parser.parse_args()
    print(json.dumps(run_probe(samples=args.samples, seed=args.seed), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
