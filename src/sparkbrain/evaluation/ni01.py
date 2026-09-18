from __future__ import annotations

import math
import random
from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScoredStep:
    world: str
    episode_id: str
    candidate_loss: float
    comparator_loss: float


@dataclass(frozen=True, slots=True)
class EffectSummary:
    candidate_loss: float
    comparator_loss: float
    effect: float
    ci95_lower: float
    ci95_upper: float
    world_effects: dict[str, float]


def coverage_matched_threshold(
    native_decided: Sequence[bool], confidences: Sequence[float]
) -> float:
    """Select a target-free threshold that most closely matches native coverage.

    Ties are resolved toward the larger (more conservative) threshold.
    """
    if len(native_decided) != len(confidences):
        raise ValueError("native_decided and confidences must have equal length")
    if not confidences:
        raise ValueError("at least one DEV confidence is required")
    if any(not math.isfinite(value) for value in confidences):
        raise ValueError("DEV confidences must be finite")

    target_coverage = sum(native_decided) / len(native_decided)
    thresholds = sorted({*confidences, math.inf, -math.inf}, reverse=True)

    def key(threshold: float) -> tuple[float, float]:
        coverage = sum(value >= threshold for value in confidences) / len(confidences)
        return (abs(coverage - target_coverage), -threshold)

    return min(thresholds, key=key)


def comparator_decision(
    probabilities: Sequence[float], labels: Sequence[str], threshold: float
) -> str | None:
    """Return canonical-order argmax iff max probability reaches threshold."""
    if not probabilities or len(probabilities) != len(labels):
        raise ValueError("probabilities and labels must be non-empty and equally sized")
    if any(not math.isfinite(value) for value in probabilities):
        raise ValueError("probabilities must be finite")
    best_index = max(range(len(probabilities)), key=lambda index: probabilities[index])
    if probabilities[best_index] < threshold:
        return None
    return labels[best_index]


def selective_decision_loss(
    prediction: str | None, *, truth: str, decision_justified: bool
) -> float:
    """Prospectively fixed NI01 per-step selective decision loss."""
    if not decision_justified:
        return 0.0 if prediction is None else 1.0
    if prediction is None:
        return 0.5
    return 0.0 if prediction == truth else 1.0


def type7_quantile(values: Sequence[float], probability: float) -> float:
    """R/NumPy-style Type-7 sample quantile for deterministic bootstrap CIs."""
    if not values:
        raise ValueError("values must be non-empty")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0, 1]")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def _mean(values: Iterable[float]) -> float:
    data = tuple(values)
    if not data:
        raise ValueError("cannot take mean of an empty sequence")
    return sum(data) / len(data)


def summarize_effect(
    rows: Sequence[ScoredStep],
    *,
    worlds: Sequence[str],
    episodes_per_world: int,
    steps_per_episode: int,
    resamples: int = 10_000,
    seed: int = 74_017,
) -> EffectSummary:
    """Equal-world point effect and episode-cluster bootstrap interval."""
    if len(set(worlds)) != len(worlds) or not worlds:
        raise ValueError("worlds must be unique and non-empty")
    if episodes_per_world <= 0 or steps_per_episode <= 0 or resamples <= 0:
        raise ValueError("positive cardinalities are required")

    by_world_episode: dict[str, dict[str, list[ScoredStep]]] = {world: {} for world in worlds}
    for row in rows:
        if row.world not in by_world_episode:
            raise ValueError(f"unexpected world: {row.world}")
        by_world_episode[row.world].setdefault(row.episode_id, []).append(row)

    world_episode_effects: dict[str, list[float]] = {}
    world_candidate_losses: dict[str, float] = {}
    world_comparator_losses: dict[str, float] = {}
    for world in worlds:
        episodes = by_world_episode[world]
        if len(episodes) != episodes_per_world:
            raise ValueError(
                f"{world}: expected {episodes_per_world} episodes, got {len(episodes)}"
            )
        episode_effects: list[float] = []
        candidate_episode_losses: list[float] = []
        comparator_episode_losses: list[float] = []
        for episode_id in sorted(episodes):
            episode_rows = episodes[episode_id]
            if len(episode_rows) != steps_per_episode:
                raise ValueError(
                    f"{world}/{episode_id}: expected {steps_per_episode} steps, "
                    f"got {len(episode_rows)}"
                )
            candidate_loss = _mean(row.candidate_loss for row in episode_rows)
            comparator_loss = _mean(row.comparator_loss for row in episode_rows)
            candidate_episode_losses.append(candidate_loss)
            comparator_episode_losses.append(comparator_loss)
            episode_effects.append(comparator_loss - candidate_loss)
        world_episode_effects[world] = episode_effects
        world_candidate_losses[world] = _mean(candidate_episode_losses)
        world_comparator_losses[world] = _mean(comparator_episode_losses)

    world_effects = {
        world: world_comparator_losses[world] - world_candidate_losses[world] for world in worlds
    }
    candidate_loss = _mean(world_candidate_losses.values())
    comparator_loss = _mean(world_comparator_losses.values())
    effect = _mean(world_effects.values())

    rng = random.Random(seed)
    bootstrap_effects: list[float] = []
    for _ in range(resamples):
        resampled_world_effects: list[float] = []
        for world in worlds:
            episode_effects = world_episode_effects[world]
            draw = (
                episode_effects[rng.randrange(episodes_per_world)]
                for _ in range(episodes_per_world)
            )
            resampled_world_effects.append(_mean(draw))
        bootstrap_effects.append(_mean(resampled_world_effects))

    return EffectSummary(
        candidate_loss=candidate_loss,
        comparator_loss=comparator_loss,
        effect=effect,
        ci95_lower=type7_quantile(bootstrap_effects, 0.025),
        ci95_upper=type7_quantile(bootstrap_effects, 0.975),
        world_effects=world_effects,
    )
