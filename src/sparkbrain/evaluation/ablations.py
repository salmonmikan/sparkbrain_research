from __future__ import annotations

from dataclasses import dataclass, replace

from ..engine import SparkBrain
from ..model import BrainConfig, SparkKind


@dataclass(frozen=True, slots=True)
class Ablation:
    name: str

    def configure(self, base: BrainConfig) -> BrainConfig:
        overrides: dict[str, float | int] = {}
        if self.name == "no_source_diversity":
            overrides["diversity_bonus"] = 0.0
        elif self.name == "no_contradiction_penalty":
            overrides["contradiction_penalty"] = 0.0
        elif self.name == "no_temporal_stability":
            overrides.update(temporal_coherence_bonus=0.0, stability_evaluations=1)
        elif self.name == "no_margin_gate":
            overrides["ignition_margin"] = 0.0
        elif self.name == "single_spark_ignition":
            overrides.update(diversity_bonus=0.0, min_support_sources=1)
        elif self.name == "no_homeostasis":
            overrides["homeostatic_increment"] = 0.0
        elif self.name == "no_refractory":
            overrides["refractory_period"] = 0.0
        return replace(base, **overrides)

    def transform(self, brain: SparkBrain) -> None:
        if self.name == "no_residual":
            for spark in brain.sparks.values():
                if spark.kind in {SparkKind.HYPOTHESIS, SparkKind.MEMORY, SparkKind.GOAL}:
                    spark.metadata["post_fire_residual"] = 0.0
        elif self.name == "no_lateral_inhibition":
            retained = [edge for edge in brain.connections if edge.label != "lateral_inhibition"]
            brain.connections = retained
            brain.edges_out.clear()
            for edge in retained:
                brain.edges_out[edge.source].append(edge)
        elif self.name == "no_workspace_broadcast":
            brain.broadcast_listeners.clear()

    @property
    def forced_prediction(self) -> bool:
        return self.name == "forced_prediction"

    @property
    def hard_wta(self) -> bool:
        return self.name == "hard_wta"


ABLATION_NAMES = (
    "full",
    "no_residual",
    "hard_wta",
    "no_lateral_inhibition",
    "no_source_diversity",
    "no_contradiction_penalty",
    "no_temporal_stability",
    "no_margin_gate",
    "single_spark_ignition",
    "forced_prediction",
    "dense_update_accounting",
    "no_workspace_broadcast",
    "no_homeostasis",
    "no_refractory",
)


def get_ablation(name: str) -> Ablation:
    if name not in ABLATION_NAMES:
        raise ValueError(f"Unknown ablation: {name!r}")
    return Ablation(name)
