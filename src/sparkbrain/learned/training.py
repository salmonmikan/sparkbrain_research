from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, replace

import torch
from torch import nn

from ..tasks.schema import Episode
from .backend import LearnedBrainBackend
from .config import LearnedConfig
from .contracts import EvaluationSummary, LearnedExample
from .model import SparseRoutingModel


def episode_examples(episode: Episode) -> list[LearnedExample]:
    rows: list[LearnedExample] = []
    for step in episode.steps:
        observation = step.observation
        object_id = observation.object_id or sorted(step.target.belief_truth_by_object)[0]
        rows.append(
            LearnedExample(
                episode.episode_id,
                episode.world_id,
                episode.split,
                observation.step_index,
                observation.evidence_label,
                observation.source_id,
                observation.channel,
                observation.strength,
                observation.delivery_time - observation.emitted_time,
                step.target.belief_truth_by_object[object_id],
                step.target.optimal_action,
                step.target.update_required,
                step.target.scenario_tags,
                object_id,
            )
        )
    return rows


def train_model(
    config: LearnedConfig, episodes: Iterable[Episode]
) -> tuple[SparseRoutingModel, list[dict]]:
    config.validate()
    torch.manual_seed(config.seed)
    random.seed(config.seed)
    model = SparseRoutingModel(config)
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    label_index = {label: index for index, label in enumerate(config.labels)}
    history: list[dict] = []
    episode_rows = list(episodes)
    for epoch in range(config.epochs):
        generator = torch.Generator().manual_seed(config.seed + epoch)
        order = torch.randperm(len(episode_rows), generator=generator).tolist()
        total_loss = 0.0
        correct = 0
        examples = 0
        load = torch.zeros(config.module_count)
        for episode_index in order:
            model.reset_runtime()
            optimizer.zero_grad()
            losses = []
            for example in episode_examples(episode_rows[episode_index]):
                output = model.forward_step(
                    evidence=example.evidence_label,
                    source=example.source_id,
                    channel=example.channel,
                    strength=example.strength,
                    delay=example.delivery_delay,
                    generator=generator,
                )
                target = torch.tensor(label_index[example.belief_truth], dtype=torch.long)
                belief = nn.functional.cross_entropy(
                    output.logits.unsqueeze(0), target.unsqueeze(0)
                )
                desired_load = torch.full_like(output.router_probabilities, 1 / config.module_count)
                balance = torch.mean((output.router_probabilities - desired_load) ** 2)
                entropy = -torch.sum(
                    output.router_probabilities * torch.log(output.router_probabilities + 1e-8)
                )
                target_one_hot = nn.functional.one_hot(
                    target, num_classes=len(config.labels)
                ).float()
                ignition_calibration = torch.mean(
                    (output.probabilities - target_one_hot) ** 2
                )
                selected_mass = output.router_probabilities.gather(0, output.selected).sum()
                provenance = 1.0 - selected_mass
                trace_consistency = (output.coalition_score - output.support) ** 2
                revision_weight = 1.0 + config.revision_loss * float(example.update_required)
                loss = (
                    config.belief_loss * revision_weight * belief
                    + config.recovery_loss * float(example.update_required) * belief
                    + config.ignition_loss * ignition_calibration
                    + config.load_balance_loss * balance
                    + config.sparsity_loss * entropy
                    + config.provenance_loss * provenance
                    + config.trace_consistency_loss * trace_consistency
                )
                losses.append(loss)
                load += output.router_probabilities.detach().cpu()
                correct += int(output.logits.argmax().item() == target.item())
                examples += 1
            episode_loss = torch.stack(losses).mean()
            episode_loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 2.0)
            optimizer.step()
            model.module_state = model.module_state.detach()
            model.previous_probabilities = model.previous_probabilities.detach()
            total_loss += float(episode_loss.detach())
        normalized_load = load / max(1.0, float(load.sum()))
        load_entropy = float(
            -(normalized_load * torch.log(normalized_load + 1e-8)).sum()
            / math.log(config.module_count)
        )
        history.append(
            {
                "epoch": epoch + 1,
                "mean_loss": total_loss / len(episode_rows),
                "training_accuracy": correct / examples,
                "soft_routing_entropy": load_entropy,
            }
        )
    model.eval()
    model.reset_runtime()
    return model, history


def calibrate_ignition(
    config: LearnedConfig, model: SparseRoutingModel, episodes: Iterable[Episode]
) -> LearnedConfig:
    backend = LearnedBrainBackend(config, model)
    confidences: list[float] = []
    margins: list[float] = []
    for episode in episodes:
        backend.reset(seed=episode.seed)
        for example in episode_examples(episode):
            backend.schedule(
                time=float(example.step_index + 1),
                kind="stimulus",  # EventKind is a StrEnum and validates at consumers.
                source=example.source_id,
                target=None,
                strength=example.strength,
                evidence_id=f"{example.episode_id}:{example.step_index}",
                evidence_label=example.evidence_label,
                metadata={"channel": example.channel, "delivery_delay": example.delivery_delay},
            )
            backend.run()
            values = sorted(backend.prediction_record().probabilities.values(), reverse=True)
            confidences.append(values[0])
            margins.append(values[0] - values[1])
    confidence_threshold = float(torch.tensor(confidences).quantile(0.25))
    margin_threshold = float(torch.tensor(margins).quantile(0.20))
    return replace(
        config,
        confidence_threshold=max(1 / len(config.labels), confidence_threshold),
        margin_threshold=max(0.0, margin_threshold),
    )


def evaluate_model(
    config: LearnedConfig,
    model: SparseRoutingModel,
    episodes: Iterable[Episode],
    *,
    condition: str = "full",
    majority_label: str | None = None,
    retain_trace: bool = False,
) -> tuple[EvaluationSummary, list[dict], list[dict]]:
    active_config = replace(config, condition=condition)
    backend = LearnedBrainBackend(active_config, model)
    rows: list[dict] = []
    recovery_rows: list[dict] = []
    truths: list[str] = []
    predictions: list[str | None] = []
    module_loads = [0] * config.module_count
    aggregate_counters: dict[str, int | float] = {}
    for episode in episodes:
        backend.reset(seed=episode.seed)
        examples = episode_examples(episode)
        pending_recovery: tuple[int, str] | None = None
        for example in examples:
            before = backend.prediction
            backend.schedule(
                time=float(example.step_index + 1),
                kind="stimulus",
                source=example.source_id,
                target=None,
                strength=example.strength,
                evidence_id=f"{example.episode_id}:{example.step_index}",
                evidence_label=example.evidence_label,
                metadata={"channel": example.channel, "delivery_delay": example.delivery_delay},
            )
            backend.run()
            record = backend.prediction_record()
            truths.append(example.belief_truth)
            predictions.append(record.belief)
            if example.update_required and before not in {None, example.belief_truth}:
                pending_recovery = (example.step_index, example.belief_truth)
            if pending_recovery and record.belief == pending_recovery[1]:
                recovery_rows.append(
                    {
                        "episode_id": episode.episode_id,
                        "switch_step": pending_recovery[0],
                        "recovered_step": example.step_index,
                        "label": pending_recovery[1],
                        "hand_authored_event_weights": False,
                    }
                )
                pending_recovery = None
            row = {
                "episode_id": episode.episode_id,
                "world_id": episode.world_id,
                "step_index": example.step_index,
                "object_id": example.object_id,
                "truth": example.belief_truth,
                "belief": record.belief,
                "action": record.action,
                "probabilities": record.probabilities,
                "selected_modules": list(record.selected_modules),
                "evidence_path": [list(pair) for pair in record.evidence_path],
                "coalition": record.coalition,
            }
            if retain_trace:
                row["trace"] = backend.snapshot(
                    external_event=example.evidence_label, truth=example.belief_truth
                )
                row["trace"] = asdict(row["trace"])
            rows.append(row)
        module_loads = [a + b for a, b in zip(module_loads, backend.module_loads, strict=True)]
        for key, value in backend.work.to_dict().items():
            aggregate_counters[key] = aggregate_counters.get(key, 0) + value

    covered = [index for index, value in enumerate(predictions) if value is not None]
    accuracy = sum(a == b for a, b in zip(predictions, truths, strict=True)) / len(truths)
    covered_accuracy = (
        sum(predictions[index] == truths[index] for index in covered) / len(covered)
        if covered
        else None
    )
    majority = majority_label or Counter(truths).most_common(1)[0][0]
    nonlearning = sum(truth == majority for truth in truths) / len(truths)
    total_load = sum(module_loads)
    probabilities = [value / total_load for value in module_loads if value and total_load]
    entropy = (
        -sum(value * math.log(value) for value in probabilities) / math.log(config.module_count)
        if probabilities
        else 0.0
    )
    summary = EvaluationSummary(
        condition=condition,
        split="test",
        examples=len(truths),
        accuracy=accuracy,
        covered_accuracy=covered_accuracy,
        coverage=len(covered) / len(truths),
        chance_accuracy=1 / len(config.labels),
        nonlearning_accuracy=nonlearning,
        recovery_count=len(recovery_rows),
        routing_entropy=entropy,
        module_loads=tuple(module_loads),
        counters=aggregate_counters,
        diagnostics={
            "dead_modules": sum(value == 0 for value in module_loads),
            "overloaded_modules": sum(
                value > 2 * total_load / config.module_count for value in module_loads
            ),
            "no_ignition_count": len(truths) - len(covered),
        },
    )
    return summary, rows, recovery_rows
