from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, List, Tuple


@dataclass
class Spark:
    name: str
    activation: float = 0.0
    threshold: float = 1.0
    residual_decay: float = 0.82
    supports: deque = field(default_factory=lambda: deque(maxlen=6))
    last_fired: int = -1

    def decay(self):
        self.activation *= self.residual_decay


@dataclass
class Ignition:
    t: int
    winner: str
    score: float
    margin: float
    supports: Tuple[str, ...]


class SparkField:
    """
    Minimal runnable prototype of the Spark Field idea.

    This is intentionally NOT a biological brain simulator.
    It demonstrates:
      - event-driven evidence injection
      - leaky activation
      - lateral inhibition
      - coalition support diversity
      - ignition threshold + winner margin
      - residual losing hypotheses that can later recover
    """

    def __init__(
        self,
        ignition_threshold: float = 1.25,
        margin_threshold: float = 0.22,
        inhibition: float = 0.18,
        diversity_bonus: float = 0.12,
    ):
        self.t = 0
        self.ignition_threshold = ignition_threshold
        self.margin_threshold = margin_threshold
        self.inhibition = inhibition
        self.diversity_bonus = diversity_bonus

        self.sparks: Dict[str, Spark] = {
            "cat": Spark("cat"),
            "dog": Spark("dog"),
            "toy": Spark("toy"),
        }

        # Event -> hypothesis stimulation.
        # Positive = excitation, negative = contradiction/inhibition.
        self.evidence_map: Dict[str, Dict[str, float]] = {
            "fur":          {"cat": 0.48, "dog": 0.38, "toy": 0.06},
            "meow":         {"cat": 0.82, "dog": -0.18, "toy": -0.05},
            "purr":         {"cat": 0.78, "dog": -0.12, "toy": -0.05},
            "bark":         {"dog": 0.85, "cat": -0.18, "toy": -0.05},
            "tail_wag":     {"dog": 0.55, "cat": 0.10, "toy": 0.00},
            "motionless":   {"toy": 0.66, "cat": -0.22, "dog": -0.22},
            "plastic_seam": {"toy": 0.92, "cat": -0.15, "dog": -0.15},
            "warm_body":    {"cat": 0.25, "dog": 0.25, "toy": -0.45},
        }

        self.last_ignition: Ignition | None = None

    def _decay_all(self):
        # Toy implementation.
        # A production event-driven engine would schedule decay lazily
        # only for nodes touched by events.
        for s in self.sparks.values():
            s.decay()

    def _apply_lateral_inhibition(self):
        """
        Soft winner-take-most:
        stronger active hypotheses suppress weaker competitors,
        but losers retain residual activation.
        """
        ranked = sorted(self.sparks.values(), key=lambda x: x.activation, reverse=True)
        winner = ranked[0]
        if winner.activation <= 0:
            return

        for loser in ranked[1:]:
            gap = max(0.0, winner.activation - loser.activation)
            loser.activation -= self.inhibition * min(gap, 1.0)
            loser.activation = max(-0.5, loser.activation)

    def _coalition_score(self, spark: Spark) -> float:
        unique_supports = len(set(spark.supports))
        # independent evidence sources increase coalition strength
        bonus = max(0, unique_supports - 1) * self.diversity_bonus
        return spark.activation + bonus

    def inject(self, evidence: str) -> Ignition | None:
        if evidence not in self.evidence_map:
            raise KeyError(f"Unknown evidence: {evidence}")

        self.t += 1
        self._decay_all()

        for hypothesis, delta in self.evidence_map[evidence].items():
            s = self.sparks[hypothesis]
            s.activation += delta
            if delta > 0.08:
                s.supports.append(evidence)

        self._apply_lateral_inhibition()

        scored = sorted(
            (
                (name, self._coalition_score(s), s)
                for name, s in self.sparks.items()
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        top_name, top_score, top_spark = scored[0]
        second_score = scored[1][1]
        margin = top_score - second_score
        support_diversity = len(set(top_spark.supports))

        # Require a coalition: not merely one strong event.
        if (
            top_score >= self.ignition_threshold
            and margin >= self.margin_threshold
            and support_diversity >= 2
        ):
            ignition = Ignition(
                t=self.t,
                winner=top_name,
                score=round(top_score, 3),
                margin=round(margin, 3),
                supports=tuple(dict.fromkeys(top_spark.supports)),
            )
            self.last_ignition = ignition
            top_spark.last_fired = self.t
            return ignition

        return None

    def snapshot(self) -> Dict[str, float]:
        return {
            name: round(self._coalition_score(s), 3)
            for name, s in self.sparks.items()
        }


def demo():
    sf = SparkField()

    sequence = [
        "fur",           # ambiguous: cat/dog
        "meow",          # coalition should make cat ignite
        "motionless",    # contradictory evidence weakens cat, toy grows
        "plastic_seam",  # toy should take over / ignite
        "warm_body",     # toy weakened; biological hypotheses can recover
        "purr",          # cat should recover strongly
    ]

    print("Spark Field Architecture v0.1 demo")
    print("-" * 68)

    for ev in sequence:
        ignition = sf.inject(ev)
        snap = sf.snapshot()
        print(f"t={sf.t:02d} evidence={ev:12s} scores={snap}")
        if ignition:
            print(
                "   >>> IGNITION:",
                ignition.winner.upper(),
                f"score={ignition.score}",
                f"margin={ignition.margin}",
                f"supports={ignition.supports}",
            )


if __name__ == "__main__":
    demo()
