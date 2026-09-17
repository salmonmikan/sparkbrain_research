"""EXPLORATORY / NON_EVIDENTIARY H3 noisy-group privilege-removal probe.

Synthetic-only follow-up authorized by the Evidence Analyst. The probe replaces
perfect latent correlation-group IDs with a fixed noisy observed grouping proxy
and supplies that same proxy symmetrically to scalar and coalition-style readers.
It does not open, score, or reinterpret any formal SparkBrain experiment.
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Callable
from dataclasses import dataclass

CORRUPTION_RATES = (0.0, 0.10, 0.25, 0.50, 1.0)


@dataclass(frozen=True)
class EvidenceMessage:
    true_group_id: int
    source_id: int
    sign: int
    observed_group_id: int


def _binary_sign(score: float) -> int:
    return 1 if score >= 0.0 else -1


def _unique_source_votes(
    messages: list[EvidenceMessage],
) -> dict[tuple[int, int], tuple[int, int]]:
    votes: dict[tuple[int, int], tuple[int, int]] = {}
    for message in messages:
        key = (message.true_group_id, message.source_id)
        value = (message.sign, message.observed_group_id)
        previous = votes.get(key)
        if previous is not None and previous != value:
            raise ValueError("Synthetic exact duplicates disagree.")
        votes[key] = value
    return votes


def predict_naive(messages: list[EvidenceMessage]) -> int:
    return _binary_sign(sum(message.sign for message in messages))


def predict_source_dedup(messages: list[EvidenceMessage]) -> int:
    return _binary_sign(sum(sign for sign, _proxy in _unique_source_votes(messages).values()))


def _proxy_groups(messages: list[EvidenceMessage]) -> dict[int, list[int]]:
    groups: dict[int, list[int]] = {}
    for sign, observed_group_id in _unique_source_votes(messages).values():
        groups.setdefault(observed_group_id, []).append(sign)
    return groups


def predict_proxy_normalized(messages: list[EvidenceMessage]) -> int:
    """Ordinary scalar reduction using only the supplied observed grouping proxy."""
    groups = _proxy_groups(messages)
    score = sum(sum(votes) / len(votes) for votes in groups.values())
    return _binary_sign(score)


def predict_proxy_majority(messages: list[EvidenceMessage]) -> int:
    """Coalition-style proxy using the identical observed grouping proxy."""
    groups = _proxy_groups(messages)
    decisions = [_binary_sign(sum(votes)) for votes in groups.values()]
    return _binary_sign(sum(decisions))


Predictor = Callable[[list[EvidenceMessage]], int]


def _synthetic_examples(
    *,
    samples: int,
    seed: int,
    proxy_seed: int,
    corruption_rate: float,
) -> list[tuple[int, list[EvidenceMessage]]]:
    world_rng = random.Random(seed)
    proxy_rng = random.Random(proxy_seed)
    member_patterns = (
        (1, 1, 1, 1, 1),
        (1, 1, 2, 4, 8),
        (8, 4, 2, 1, 1),
        (1, 2, 4, 8, 16),
    )
    duplicate_pattern = (1, 1, 2, 4)
    group_count = 5
    examples: list[tuple[int, list[EvidenceMessage]]] = []

    for example_index in range(samples):
        truth = world_rng.choice((-1, 1))
        members_per_group = member_patterns[example_index % len(member_patterns)]
        messages: list[EvidenceMessage] = []

        for true_group_id, member_count in enumerate(members_per_group):
            latent_sign = truth if world_rng.random() < 0.70 else -truth
            for source_id in range(member_count):
                source_sign = latent_sign if world_rng.random() < 0.90 else -latent_sign

                if proxy_rng.random() < corruption_rate:
                    alternatives = [
                        group_id
                        for group_id in range(group_count)
                        if group_id != true_group_id
                    ]
                    observed_group_id = alternatives[proxy_rng.randrange(len(alternatives))]
                else:
                    observed_group_id = true_group_id

                duplicates = duplicate_pattern[
                    (example_index + 3 * true_group_id + source_id)
                    % len(duplicate_pattern)
                ]
                messages.extend(
                    EvidenceMessage(
                        true_group_id=true_group_id,
                        source_id=source_id,
                        sign=source_sign,
                        observed_group_id=observed_group_id,
                    )
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


def run_probe(
    *,
    samples: int = 4096,
    seed: int = 1337,
    proxy_seed: int = 20260918,
) -> dict[str, object]:
    predictors: dict[str, Predictor] = {
        "naive": predict_naive,
        "source_dedup": predict_source_dedup,
        "proxy_group_normalized": predict_proxy_normalized,
        "proxy_group_majority": predict_proxy_majority,
    }

    rows: list[dict[str, object]] = []
    for corruption_rate in CORRUPTION_RATES:
        examples = _synthetic_examples(
            samples=samples,
            seed=seed,
            proxy_seed=proxy_seed,
            corruption_rate=corruption_rate,
        )
        accuracy = {
            name: _accuracy(examples, predictor)
            for name, predictor in predictors.items()
        }
        agreement = sum(
            predict_proxy_normalized(messages) == predict_proxy_majority(messages)
            for _truth, messages in examples
        ) / len(examples)
        rows.append(
            {
                "corruption_rate": corruption_rate,
                "accuracy": accuracy,
                "proxy_scalar_vs_proxy_coalition_agreement": agreement,
            }
        )

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "question": (
            "When perfect latent correlation-group IDs are replaced by a fixed noisy "
            "observed grouping proxy supplied symmetrically to scalar and coalition "
            "readers, does the apparent coalition advantage survive?"
        ),
        "synthetic_contract": {
            "samples": samples,
            "world_seed": seed,
            "proxy_seed": proxy_seed,
            "corruption_rates": list(CORRUPTION_RATES),
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
            "proxy_corruption_rule": (
                "Per unique source, independently replace the true group label with "
                "a uniformly selected different group at the fixed corruption rate; "
                "exact duplicate deliveries retain the same observed proxy label."
            ),
            "information_symmetry": (
                "proxy_group_normalized and proxy_group_majority receive the identical "
                "observed_group_id and neither predictor reads true_group_id."
            ),
        },
        "rows": rows,
        "interpretation_boundary": (
            "Observed proxy labels are synthetic metadata, not learned structure. "
            "The probe is a reduction/sensitivity check only and cannot support an H3 claim."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--proxy-seed", type=int, default=20260918)
    args = parser.parse_args()
    print(
        json.dumps(
            run_probe(
                samples=args.samples,
                seed=args.seed,
                proxy_seed=args.proxy_seed,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
