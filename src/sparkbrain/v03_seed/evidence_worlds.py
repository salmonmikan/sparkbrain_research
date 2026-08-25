from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


def canonical_fixture_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def fixture_sha256(value: object) -> str:
    return hashlib.sha256(canonical_fixture_json(value).encode()).hexdigest()


def build_evidence_fixture(seed: int) -> dict[str, object]:
    episodes: list[dict[str, object]] = []
    for episode_index in range(24):
        base_time = episode_index * 10
        support_group = f"cg:{seed}:{episode_index:02d}:support"
        events: list[dict[str, object]] = [
            {
                "correlation_group": support_group,
                "event_time": base_time,
                "kind": "add_primary",
                "observed_time": base_time,
                "polarity": "support",
                "source_id": "source-primary",
                "strength": 1.0,
            },
            {
                "correlation_group": support_group,
                "event_time": base_time + 1,
                "kind": "add_correlated_variant",
                "observed_time": base_time + 1,
                "polarity": "support",
                "source_id": "source-correlated",
                "strength": 1.0,
            },
            {
                "event_time": base_time + 2,
                "kind": "late_exact_redelivery",
                "redelivers": "add_primary",
            },
            {
                "correlation_group": f"cg:{seed}:{episode_index:02d}:contradiction",
                "event_time": base_time + 3,
                "kind": "add_contradiction",
                "observed_time": base_time + 3,
                "polarity": "contradict",
                "source_id": "source-contradiction",
                "strength": 0.4,
            },
            {
                "event_time": base_time + 4,
                "kind": "deactivate_primary",
                "target": "add_primary",
            },
            {
                "event_time": base_time + 5,
                "kind": "restore_primary",
                "target": "add_primary",
            },
        ]
        episodes.append(
            {
                "episode_id": f"seed-{seed}-episode-{episode_index:02d}",
                "episode_index": episode_index,
                "events": events,
                "target_entity": "object-a"
                if (episode_index + seed) % 2 == 0
                else "object-b",
                "target_hypothesis": "state-left"
                if (episode_index // 2 + seed) % 2 == 0
                else "state-right",
            }
        )
    return {"episodes": episodes, "schema_version": "0.3", "seed": seed}


@dataclass(frozen=True, slots=True)
class G0Decision:
    winner: str | None
    positive_probability: float | None
    confidence: float | None
    probability_margin: float | None
    citations: tuple[str, ...]
    abstained: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "abstained": self.abstained,
            "citations": list(self.citations),
            "confidence": self.confidence,
            "positive_probability": self.positive_probability,
            "probability_margin": self.probability_margin,
            "winner": self.winner,
        }
