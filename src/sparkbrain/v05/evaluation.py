from __future__ import annotations

import copy
import random
import statistics
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

from .assemblies import AssemblyActivation
from .brain import IntegratedV05Brain, V05BrainConfig
from .worlds import MotifEpisode, held_out_episodes, training_episodes


@dataclass(frozen=True, slots=True)
class V05ProtocolConfig:
    """Frozen reference protocol for the v0.5 development milestone.

    Seed 501 was used for engineering-scale alignment of receptor output and
    field thresholds.  Primary gates are therefore computed only from the
    confirmatory seeds.  Plasticity ablations use a smaller, explicitly
    secondary budget and cannot by themselves upgrade a primary claim.
    """

    # 501 and 502 were inspected during engineering alignment.  Confirmatory
    # seeds were replaced before the retained v0.5 scientific run.
    development_seeds: tuple[int, ...] = (501, 502)
    confirmatory_seeds: tuple[int, ...] = (601, 602, 603, 604)
    train_count: int = 48
    held_out_count: int = 16
    ablation_seeds: tuple[int, ...] = (601, 602, 603)
    ablation_train_count: int = 24
    ablation_held_out_count: int = 8


@dataclass(frozen=True, slots=True)
class EpisodeEvaluation:
    seed: int
    phase: str
    condition: str
    episode_id: str
    motif_name: str | None
    assembly_id: str | None
    prediction: str | None
    expected_prediction: str | None
    action: str | None
    expected_action: str | None
    assembly_similarity: float
    mature: bool
    assembly_episode_count: int
    internal_pattern_count: int
    spike_count: int
    runaway: bool
    dead: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _strongest(result: Any) -> AssemblyActivation | None:
    rows = [row for row in result.assembly_activations if row.mature and not row.suppressed]
    return max(
        rows,
        key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
        default=None,
    )


def _reward(action: str | None, expected: str | None) -> float:
    if expected is None:
        return 0.0
    return 1.0 if action == expected else -0.35


def _run_episode(
    brain: IntegratedV05Brain,
    episode: MotifEpisode,
    *,
    seed: int,
    phase: str,
    learn: bool,
) -> EpisodeEvaluation:
    result = brain.process_episode(
        episode.pulses,
        learn_assembly=learn,
        learn_field=learn,
        metadata={"condition": episode.condition, "phase": phase},
        episode_id=episode.episode_id,
        explore_action=learn,
    )
    activation = _strongest(result)
    row = EpisodeEvaluation(
        seed=seed,
        phase=phase,
        condition=episode.condition,
        episode_id=episode.episode_id,
        motif_name=episode.motif_name,
        assembly_id=activation.assembly_id if activation is not None else None,
        prediction=result.prediction.value,
        expected_prediction=episode.future_event,
        action=result.action.action,
        expected_action=episode.rewarded_action,
        assembly_similarity=activation.similarity if activation is not None else 0.0,
        mature=activation is not None,
        assembly_episode_count=(activation.episode_count if activation is not None else 0),
        internal_pattern_count=len(result.patterns),
        spike_count=len(result.v04_result.spikes),
        runaway=result.stability.runaway,
        dead=result.stability.dead,
    )
    if learn:
        brain.learn_outcome(
            next_event=episode.future_event,
            reward=_reward(result.action.action, episode.rewarded_action),
        )
    return row


def _accuracy(rows: Iterable[EpisodeEvaluation], predicted: str, expected: str) -> float:
    values = list(rows)
    if not values:
        return 0.0
    return sum(getattr(row, predicted) == getattr(row, expected) for row in values) / len(values)


def _candidate_purity(rows: Iterable[EpisodeEvaluation]) -> float:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        if row.assembly_id is None or row.motif_name is None:
            continue
        table = counts.setdefault(row.assembly_id, {})
        table[row.motif_name] = table.get(row.motif_name, 0) + 1
    total = sum(sum(table.values()) for table in counts.values())
    if total == 0:
        return 0.0
    return sum(max(table.values()) for table in counts.values()) / total


def summarize_rows(rows: Iterable[EpisodeEvaluation]) -> dict[str, float]:
    values = list(rows)
    if not values:
        return {
            "action_accuracy": 0.0,
            "assembly_activation_rate": 0.0,
            "assembly_purity": 0.0,
            "mean_similarity": 0.0,
            "prediction_accuracy": 0.0,
            "prediction_coverage": 0.0,
            "abstention_accuracy": 0.0,
            "runaway_rate": 0.0,
            "dead_rate": 0.0,
        }
    expected_prediction_rows = [row for row in values if row.expected_prediction is not None]
    expected_abstention_rows = [row for row in values if row.expected_prediction is None]
    return {
        "action_accuracy": _accuracy(values, "action", "expected_action"),
        "assembly_activation_rate": sum(row.mature for row in values) / len(values),
        "assembly_purity": _candidate_purity(values),
        "mean_similarity": statistics.fmean(row.assembly_similarity for row in values),
        "prediction_accuracy": _accuracy(
            expected_prediction_rows,
            "prediction",
            "expected_prediction",
        ),
        "prediction_coverage": sum(row.prediction is not None for row in values) / len(values),
        "abstention_accuracy": (
            sum(row.prediction is None for row in expected_abstention_rows)
            / len(expected_abstention_rows)
            if expected_abstention_rows
            else 0.0
        ),
        "runaway_rate": sum(row.runaway for row in values) / len(values),
        "dead_rate": sum(row.dead for row in values) / len(values),
    }


def _brain_config_for_mode(mode: str, *, topology_seed: int = 41) -> V05BrainConfig:
    if mode not in {"full", "frozen", "weight_only", "delay_only", "no_assembly"}:
        raise ValueError(f"unknown ablation mode: {mode}")
    return V05BrainConfig(
        topology_seed=topology_seed,
        enable_weight_learning=mode in {"full", "weight_only", "no_assembly"},
        enable_delay_learning=mode in {"full", "delay_only", "no_assembly"},
        enable_assembly=mode != "no_assembly",
    )


def train_brain(
    seed: int,
    *,
    config: V05BrainConfig | None = None,
    count: int = 48,
) -> tuple[IntegratedV05Brain, list[EpisodeEvaluation]]:
    brain = IntegratedV05Brain(config or V05BrainConfig(topology_seed=41))
    rows = [
        _run_episode(brain, episode, seed=seed, phase="train", learn=True)
        for episode in training_episodes(seed=seed, count=count)
    ]
    return brain, rows


def evaluate_condition(
    brain: IntegratedV05Brain,
    *,
    seed: int,
    condition: str,
    count: int = 16,
) -> list[EpisodeEvaluation]:
    episodes = held_out_episodes(
        seed=seed,
        condition=condition,
        count=count,
        start_ms=brain.current_time_ms + 100.0,
    )
    return [
        _run_episode(brain, episode, seed=seed, phase="held_out", learn=False)
        for episode in episodes
    ]


def _assembly_label_counts(
    rows: Iterable[EpisodeEvaluation],
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        if row.assembly_id is None or row.motif_name is None:
            continue
        table = counts.setdefault(row.assembly_id, {})
        table[row.motif_name] = table.get(row.motif_name, 0) + 1
    return counts


def causal_ablation(
    trained: IntegratedV05Brain,
    *,
    seed: int,
    train_rows: list[EpisodeEvaluation],
    count: int = 16,
) -> dict[str, Any]:
    label_counts = _assembly_label_counts(train_rows)
    target_ids = sorted(
        assembly_id
        for assembly_id, table in label_counts.items()
        if table.get("motif_x", 0) > table.get("motif_y", 0)
    )
    if not target_ids:
        return {"status": "no_target_assembly"}
    non_target_ids = sorted(
        assembly_id
        for assembly_id in trained.assemblies.candidates
        if assembly_id not in target_ids
    )
    rng = random.Random(seed + 991)
    random_ids = list(non_target_ids)
    rng.shuffle(random_ids)
    random_ids = sorted(random_ids[: len(target_ids)])

    target_units = sorted(
        {
            unit_id
            for assembly_id in target_ids
            for unit_id in trained.assemblies.candidates[assembly_id].prototype.unit_ids
        }
    )
    random_pool = sorted(
        set(trained.base.field.units) - set(trained.base.field.receptor_ids) - set(target_units)
    )
    rng.shuffle(random_pool)
    random_units = sorted(random_pool[: len(target_units)])

    baseline = copy.deepcopy(trained)
    assembly_targeted = copy.deepcopy(trained)
    for assembly_id in target_ids:
        assembly_targeted.suppress_assembly(assembly_id)
    assembly_random = copy.deepcopy(trained)
    for assembly_id in random_ids:
        assembly_random.suppress_assembly(assembly_id)
    collateral_assembly_targeted = copy.deepcopy(trained)
    for assembly_id in target_ids:
        collateral_assembly_targeted.suppress_assembly(assembly_id)
    unit_targeted = copy.deepcopy(trained)
    unit_targeted.suppress_units(target_units)
    collateral_unit_targeted = copy.deepcopy(trained)
    collateral_unit_targeted.suppress_units(target_units)
    unit_random = copy.deepcopy(trained)
    unit_random.suppress_units(random_units)

    start_ms = baseline.current_time_ms + 100.0
    all_episodes = held_out_episodes(
        seed=seed,
        condition="jitter",
        count=count,
        start_ms=start_ms,
    )
    target_episodes = [row for row in all_episodes if row.motif_name == "motif_x"]
    collateral_episodes = [row for row in all_episodes if row.motif_name == "motif_y"]

    def score(brain: IntegratedV05Brain, episodes: list[MotifEpisode]) -> dict[str, float]:
        rows = [
            _run_episode(brain, episode, seed=seed, phase="ablation", learn=False)
            for episode in episodes
        ]
        return summarize_rows(rows)

    baseline_score = score(copy.deepcopy(baseline), target_episodes)
    assembly_targeted_score = score(assembly_targeted, target_episodes)
    assembly_random_score = score(assembly_random, target_episodes)
    assembly_collateral_score = score(collateral_assembly_targeted, collateral_episodes)
    unit_targeted_score = score(unit_targeted, target_episodes)
    unit_random_score = score(unit_random, target_episodes)
    collateral_baseline = score(copy.deepcopy(baseline), collateral_episodes)
    collateral_targeted = score(collateral_unit_targeted, collateral_episodes)

    return {
        "status": "ok",
        "target_assembly_ids": target_ids,
        "random_assembly_ids": random_ids,
        "target_unit_ids": target_units,
        "random_unit_ids": random_units,
        "baseline": baseline_score,
        "assembly_targeted": assembly_targeted_score,
        "assembly_random": assembly_random_score,
        "assembly_collateral": assembly_collateral_score,
        "unit_targeted": unit_targeted_score,
        "unit_random": unit_random_score,
        "collateral_baseline": collateral_baseline,
        "collateral_targeted": collateral_targeted,
        "assembly_targeted_impairment": (
            baseline_score["prediction_accuracy"] - assembly_targeted_score["prediction_accuracy"]
        ),
        "assembly_random_impairment": (
            baseline_score["prediction_accuracy"] - assembly_random_score["prediction_accuracy"]
        ),
        "assembly_collateral_damage": (
            collateral_baseline["prediction_accuracy"]
            - assembly_collateral_score["prediction_accuracy"]
        ),
        "unit_targeted_impairment": (
            baseline_score["prediction_accuracy"] - unit_targeted_score["prediction_accuracy"]
        ),
        "unit_random_impairment": (
            baseline_score["prediction_accuracy"] - unit_random_score["prediction_accuracy"]
        ),
        "unit_collateral_damage": (
            collateral_baseline["prediction_accuracy"] - collateral_targeted["prediction_accuracy"]
        ),
    }


def train_null_noise_control(
    seed: int,
    *,
    count: int,
) -> tuple[IntegratedV05Brain, list[EpisodeEvaluation]]:
    brain = IntegratedV05Brain(V05BrainConfig(topology_seed=41))
    episodes = held_out_episodes(
        seed=seed + 30_000,
        condition="pure_noise",
        count=count,
        start_ms=0.0,
    )
    rows = [
        _run_episode(brain, episode, seed=seed, phase="null_train", learn=True)
        for episode in episodes
    ]
    return brain, rows


def run_seed(
    seed: int,
    *,
    train_count: int = 48,
    held_out_count: int = 16,
) -> dict[str, Any]:
    brain, train_rows = train_brain(seed, count=train_count)
    null_brain, null_rows = train_null_noise_control(seed, count=train_count)
    null_mature_candidates = sum(
        candidate.episode_count >= null_brain.assemblies.config.mature_episodes
        for candidate in null_brain.assemblies.candidates.values()
    )
    conditions = {
        condition: evaluate_condition(
            copy.deepcopy(brain),
            seed=seed,
            condition=condition,
            count=held_out_count,
        )
        for condition in (
            "jitter",
            "distractor",
            "one_event_omission",
            "order_shuffle",
            "timing_shuffle",
            "pure_noise",
        )
    }
    return {
        "ablation": causal_ablation(
            brain,
            seed=seed,
            train_rows=train_rows,
            count=held_out_count,
        ),
        "assembly_count": len(brain.assemblies.candidates),
        "conditions": {
            key: {
                "rows": [row.as_dict() for row in value],
                "summary": summarize_rows(value),
            }
            for key, value in conditions.items()
        },
        "null_noise_training": {
            "candidate_count": len(null_brain.assemblies.candidates),
            "mature_candidate_count": null_mature_candidates,
            "rows": [row.as_dict() for row in null_rows],
            "summary": summarize_rows(null_rows),
        },
        "seed": seed,
        "train": {
            "rows": [row.as_dict() for row in train_rows],
            "summary": summarize_rows(train_rows),
        },
    }


def run_plasticity_ablation(
    seed: int,
    *,
    train_count: int,
    held_out_count: int,
) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for mode in ("full", "frozen", "weight_only", "delay_only", "no_assembly"):
        brain, train_rows = train_brain(
            seed,
            config=_brain_config_for_mode(mode),
            count=train_count,
        )
        heldout = evaluate_condition(
            copy.deepcopy(brain),
            seed=seed,
            condition="jitter",
            count=held_out_count,
        )
        rows[mode] = {
            "assembly_count": len(brain.assemblies.candidates),
            "train": summarize_rows(train_rows),
            "jitter": summarize_rows(heldout),
            "plasticity_updates": brain.plasticity.update_count,
        }
    return {"seed": seed, "modes": rows}


def _compact_seed_result(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "ablation": value["ablation"],
        "assembly_count": value["assembly_count"],
        "conditions": {
            key: {"summary": row["summary"]} for key, row in value["conditions"].items()
        },
        "null_noise_training": {
            "candidate_count": value["null_noise_training"]["candidate_count"],
            "mature_candidate_count": value["null_noise_training"]["mature_candidate_count"],
            "summary": value["null_noise_training"]["summary"],
        },
        "seed": value["seed"],
        "train": {"summary": value["train"]["summary"]},
    }


def _mean_seed_metric(seed_results: list[dict[str, Any]], condition: str, metric: str) -> float:
    return statistics.fmean(row["conditions"][condition]["summary"][metric] for row in seed_results)


def _aggregate(seed_results: list[dict[str, Any]]) -> dict[str, Any]:
    conditions = (
        "jitter",
        "distractor",
        "one_event_omission",
        "order_shuffle",
        "timing_shuffle",
        "pure_noise",
    )
    metrics = (
        "action_accuracy",
        "assembly_activation_rate",
        "assembly_purity",
        "mean_similarity",
        "prediction_accuracy",
        "prediction_coverage",
        "abstention_accuracy",
        "runaway_rate",
        "dead_rate",
    )
    return {
        condition: {
            metric: _mean_seed_metric(seed_results, condition, metric) for metric in metrics
        }
        for condition in conditions
    }


def _ablation_aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    modes = rows[0]["modes"]
    return {
        mode: {
            metric: statistics.fmean(row["modes"][mode]["jitter"][metric] for row in rows)
            for metric in (
                "prediction_accuracy",
                "action_accuracy",
                "assembly_activation_rate",
                "assembly_purity",
            )
        }
        for mode in modes
    }


def aggregate_v05_results(
    *,
    protocol: V05ProtocolConfig,
    development_results: list[dict[str, Any]],
    confirmatory_results: list[dict[str, Any]],
    ablation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate independently retained seed shards without rerunning dynamics."""
    if not confirmatory_results:
        raise ValueError("at least one confirmatory seed result is required")
    aggregate = _aggregate(confirmatory_results)
    null_noise_mature_candidates = statistics.fmean(
        row["null_noise_training"]["mature_candidate_count"] for row in confirmatory_results
    )
    ablation_aggregate = _ablation_aggregate(ablation_rows)

    def causal_values(name: str) -> list[float]:
        return [
            row["ablation"].get(name, 0.0)
            for row in confirmatory_results
            if row["ablation"].get("status") == "ok"
        ]

    assembly_targeted = causal_values("assembly_targeted_impairment")
    assembly_random = causal_values("assembly_random_impairment")
    assembly_collateral = causal_values("assembly_collateral_damage")
    unit_targeted = causal_values("unit_targeted_impairment")
    unit_random = causal_values("unit_random_impairment")
    unit_collateral = causal_values("unit_collateral_damage")

    gate_a = all(aggregate[condition]["runaway_rate"] == 0.0 for condition in aggregate) and all(
        aggregate[condition]["dead_rate"] <= 0.10 for condition in aggregate
    )
    gate_b = (
        aggregate["jitter"]["assembly_purity"] >= 0.70
        and aggregate["jitter"]["assembly_activation_rate"]
        > aggregate["pure_noise"]["assembly_activation_rate"] + 0.15
        and aggregate["jitter"]["assembly_activation_rate"]
        > aggregate["order_shuffle"]["assembly_activation_rate"] + 0.10
        and aggregate["jitter"]["assembly_activation_rate"]
        > aggregate["timing_shuffle"]["assembly_activation_rate"] + 0.10
        and null_noise_mature_candidates <= 1.0
    )
    gate_c = (
        aggregate["jitter"]["prediction_accuracy"] >= 0.70
        and aggregate["distractor"]["prediction_accuracy"] >= 0.65
        and aggregate["one_event_omission"]["prediction_accuracy"] >= 0.25
    )
    no_assembly_accuracy = ablation_aggregate.get("no_assembly", {}).get("prediction_accuracy", 0.0)
    gate_d = (
        aggregate["jitter"]["prediction_accuracy"] >= 0.70
        and aggregate["jitter"]["prediction_accuracy"] > no_assembly_accuracy + 0.20
    )
    gate_e = (
        bool(assembly_targeted)
        and statistics.fmean(assembly_targeted) > statistics.fmean(assembly_random) + 0.10
        and statistics.fmean(assembly_collateral) <= 0.25
    )
    plasticity_dependency = bool(ablation_aggregate) and (
        ablation_aggregate["full"]["prediction_accuracy"]
        > ablation_aggregate["frozen"]["prediction_accuracy"] + 0.05
    )
    gates = {
        "A_engineering_stability": gate_a,
        "B_selective_assembly": gate_b,
        "C_held_out_reuse": gate_c,
        "D_functional_utility": gate_d,
        "E_causal_contribution": gate_e,
        "P_plasticity_dependency_diagnostic": plasticity_dependency,
    }

    def mean_or_zero(values: list[float]) -> float:
        return statistics.fmean(values) if values else 0.0

    return {
        "schema": "sparkbrain-v05-reference-experiments-3",
        "protocol": asdict(protocol),
        "claim_boundary": (
            "pre-semantic controlled-world evidence only; no meaning, concept, organ, "
            "biological-equivalence, energy, consciousness, AGI, or external-model "
            "superiority claim"
        ),
        "development_results": development_results,
        "confirmatory_results": confirmatory_results,
        "aggregate": aggregate,
        "null_noise_mature_candidates_mean": null_noise_mature_candidates,
        "plasticity_ablations": ablation_rows,
        "plasticity_ablation_aggregate": ablation_aggregate,
        "causal_aggregate": {
            "assembly_targeted_impairment": mean_or_zero(assembly_targeted),
            "assembly_random_impairment": mean_or_zero(assembly_random),
            "assembly_collateral_damage": mean_or_zero(assembly_collateral),
            "unit_targeted_impairment": mean_or_zero(unit_targeted),
            "unit_random_impairment": mean_or_zero(unit_random),
            "unit_collateral_damage": mean_or_zero(unit_collateral),
        },
        "gates": gates,
        "completion": (
            "positive_completion"
            if all(
                gates[key]
                for key in (
                    "A_engineering_stability",
                    "B_selective_assembly",
                    "C_held_out_reuse",
                    "D_functional_utility",
                    "E_causal_contribution",
                )
            )
            else "negative_or_partial_completion"
        ),
    }


def run_v05_reference_experiments(
    *,
    seeds: tuple[int, ...] | None = None,
    protocol: V05ProtocolConfig | None = None,
    include_rows: bool = False,
) -> dict[str, Any]:
    cfg = protocol or V05ProtocolConfig()
    if seeds is not None:
        development_seeds: tuple[int, ...] = ()
        confirmatory_seeds = tuple(seeds)
    else:
        development_seeds = cfg.development_seeds
        confirmatory_seeds = cfg.confirmatory_seeds

    development_results: list[dict[str, Any]] = []
    for seed in development_seeds:
        row = run_seed(
            seed,
            train_count=cfg.train_count,
            held_out_count=cfg.held_out_count,
        )
        development_results.append(row if include_rows else _compact_seed_result(row))
    confirmatory_results: list[dict[str, Any]] = []
    for seed in confirmatory_seeds:
        row = run_seed(
            seed,
            train_count=cfg.train_count,
            held_out_count=cfg.held_out_count,
        )
        confirmatory_results.append(row if include_rows else _compact_seed_result(row))
    ablation_rows = [
        run_plasticity_ablation(
            seed,
            train_count=cfg.ablation_train_count,
            held_out_count=cfg.ablation_held_out_count,
        )
        for seed in cfg.ablation_seeds
        if seed in confirmatory_seeds
    ]
    return aggregate_v05_results(
        protocol=cfg,
        development_results=development_results,
        confirmatory_results=confirmatory_results,
        ablation_rows=ablation_rows,
    )


def render_v05_report(payload: dict[str, Any]) -> str:
    """Render a compact, claim-bounded Markdown report from retained results."""
    lines = [
        "# SparkBrain v0.5 reference results",
        "",
        f"Completion: **{payload['completion']}**",
        "",
        "> Controlled, pre-semantic local experiment. This does not establish meaning, concepts, organs, biological equivalence, consciousness, AGI, energy efficiency, or general model superiority.",
        "",
        "## Primary gates",
        "",
        "| Gate | Result |",
        "|---|---:|",
    ]
    for name, value in payload["gates"].items():
        lines.append(f"| `{name}` | {'PASS' if value else 'FAIL'} |")
    lines.extend(
        [
            "",
            "## Confirmatory aggregate",
            "",
            "| Condition | Prediction | Action | Assembly activation | Purity |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for condition, row in payload["aggregate"].items():
        lines.append(
            f"| {condition} | {row['prediction_accuracy']:.3f} | "
            f"{row['action_accuracy']:.3f} | {row['assembly_activation_rate']:.3f} | "
            f"{row['assembly_purity']:.3f} |"
        )
    causal = payload["causal_aggregate"]
    lines.extend(
        [
            "",
            "## Causal intervention aggregate",
            "",
            f"- Targeted Assembly impairment: `{causal['assembly_targeted_impairment']:.3f}`",
            f"- Matched random Assembly impairment: `{causal['assembly_random_impairment']:.3f}`",
            f"- Assembly collateral damage: `{causal['assembly_collateral_damage']:.3f}`",
            f"- Targeted physical-unit impairment (diagnostic): `{causal['unit_targeted_impairment']:.3f}`",
            f"- Physical-unit collateral damage (diagnostic): `{causal['unit_collateral_damage']:.3f}`",
            "",
            "## Interpretation",
            "",
        ]
    )
    if payload["completion"] == "positive_completion":
        lines.append(
            "All preregistered engineering/scientific gates passed in this bounded synthetic protocol; the strongest permitted phrase is **causal functional temporal Assembly support under the retained controlled conditions**."
        )
    else:
        failed = [
            name
            for name, value in payload["gates"].items()
            if not value and not name.startswith("P_")
        ]
        lines.append(
            "The implementation completed the protocol, but the full functional-Assembly hypothesis was not supported. Failed primary gates: "
            + ", ".join(f"`{name}`" for name in failed)
            + "."
        )
    lines.extend(
        [
            "",
            "The plasticity-dependency gate is diagnostic and does not upgrade a claim by itself.",
            "",
        ]
    )
    return "\n".join(lines)
