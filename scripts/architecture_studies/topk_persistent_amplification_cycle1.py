from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any

import torch

from sparkbrain.learned.config import LearnedConfig
from sparkbrain.learned.experiment import _episodes
from sparkbrain.learned.training import episode_examples, train_model

EXPECTED_MAIN_SHA = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
ANALYST_COMMIT = "3e83f1eb683ce80e326b756fa304e96688fdd3fe"
DIRECTION_SEED = 20260919
MAGNITUDES = (0.01, 0.05, 0.10)
PROBE_POSITIONS = (6, 12, 18, 24)
DIRECTIONS_PER_PROBE = 8
HORIZON = 6
TURNOVER_MINIMUM = 20
STATE_RATIO_SIGNAL = 2.0
OUTPUT_RATIO_SIGNAL = 1.5
STATE_RATIO_ORDINARY = 1.25
RATIO_FLOOR = 1e-12


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot(model: torch.nn.Module) -> tuple[torch.Tensor, torch.Tensor]:
    return model.module_state.detach().clone(), model.previous_probabilities.detach().clone()


def _restore(model: torch.nn.Module, snapshot: tuple[torch.Tensor, torch.Tensor]) -> None:
    model.module_state = snapshot[0].detach().clone()
    model.previous_probabilities = snapshot[1].detach().clone()


def _step(
    model: torch.nn.Module,
    example: Any,
    *,
    condition: str,
    perturbation: torch.Tensor | None = None,
) -> dict[str, Any]:
    pre_state = model.module_state.detach().clone()
    captured: list[torch.Tensor] = []

    def capture_update(
        _module: torch.nn.Module,
        _inputs: tuple[torch.Tensor, ...],
        output: torch.Tensor,
    ) -> None:
        captured.append(output.detach().clone())

    hook = model.update.register_forward_hook(capture_update)
    original_forward = model.encoder.forward
    if perturbation is not None:

        def perturbed_forward(*args: Any, **kwargs: Any) -> torch.Tensor:
            return original_forward(*args, **kwargs) + perturbation

        model.encoder.forward = perturbed_forward

    try:
        output = model.forward_step(
            evidence=example.evidence_label,
            source=example.source_id,
            channel=example.channel,
            strength=example.strength,
            delay=example.delivery_delay,
            condition=condition,
        )
    finally:
        model.encoder.forward = original_forward
        hook.remove()

    if len(captured) != 1:
        raise RuntimeError(f"Expected one GRU update capture, got {len(captured)}")

    previous = pre_state.index_select(0, output.selected)
    selected_state = captured[0]
    if condition != "no_persistent_state":
        selected_state = (
            model.config.persistence * selected_state
            + (1.0 - model.config.persistence) * previous
        )
    effective_state = pre_state.clone().index_copy(0, output.selected, selected_state)
    return {
        "selected": [int(value) for value in output.selected.detach().cpu().tolist()],
        "effective_state": effective_state.detach().cpu(),
        "probabilities": output.probabilities.detach().cpu(),
        "action_logits": output.action_logits.detach().cpu(),
    }


def _sequence(
    model: torch.nn.Module,
    examples: list[Any],
    *,
    start_index: int,
    condition: str,
    perturbation: torch.Tensor | None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset in range(HORIZON + 1):
        rows.append(
            _step(
                model,
                examples[start_index + offset],
                condition=condition,
                perturbation=perturbation if offset == 0 else None,
            )
        )
    return rows


def _auc(values: list[float]) -> float:
    return sum(
        (left + right) * 0.5
        for left, right in zip(values, values[1:], strict=False)
    )


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / max(denominator, RATIO_FLOOR)


def _metrics(
    baseline: list[dict[str, Any]], changed: list[dict[str, Any]]
) -> dict[str, Any]:
    state: list[float] = []
    probabilities: list[float] = []
    action_logits: list[float] = []
    for base, perturbed in zip(baseline, changed, strict=True):
        base_state = base["effective_state"]
        changed_state = perturbed["effective_state"]
        state.append(
            float(torch.linalg.vector_norm(changed_state - base_state))
            / max(float(torch.linalg.vector_norm(base_state)), RATIO_FLOOR)
        )
        probabilities.append(
            float(torch.sum(torch.abs(perturbed["probabilities"] - base["probabilities"])))
        )
        action_logits.append(
            float(torch.linalg.vector_norm(perturbed["action_logits"] - base["action_logits"]))
        )
    return {
        "state_divergence": state,
        "probability_l1_divergence": probabilities,
        "action_logit_l2_divergence": action_logits,
        "state_auc": _auc(state),
        "probability_auc": _auc(probabilities),
        "action_logit_auc": _auc(action_logits),
    }


def _unit_directions(event_dim: int, generator: torch.Generator) -> list[torch.Tensor]:
    rows = torch.randn(
        DIRECTIONS_PER_PROBE,
        event_dim,
        generator=generator,
        dtype=torch.float32,
    )
    return [row / torch.linalg.vector_norm(row) for row in rows]


def _probe_condition(
    model: torch.nn.Module,
    examples: list[Any],
    *,
    probe_index: int,
    condition: str,
    directions: list[torch.Tensor],
    encoded: torch.Tensor,
    margin: float,
    episode_id: str,
    episode_seed: int,
    probe_position: int,
) -> list[dict[str, Any]]:
    model.reset_runtime()
    with torch.no_grad():
        for example in examples[:probe_index]:
            model.forward_step(
                evidence=example.evidence_label,
                source=example.source_id,
                channel=example.channel,
                strength=example.strength,
                delay=example.delivery_delay,
                condition=condition,
            )
    prefix = _snapshot(model)
    encoded_norm = float(torch.linalg.vector_norm(encoded))
    rows: list[dict[str, Any]] = []

    for direction_index, direction in enumerate(directions):
        for magnitude in MAGNITUDES:
            perturbation = direction * (magnitude * encoded_norm)
            _restore(model, prefix)
            with torch.no_grad():
                baseline = _sequence(
                    model,
                    examples,
                    start_index=probe_index,
                    condition=condition,
                    perturbation=None,
                )
            _restore(model, prefix)
            with torch.no_grad():
                changed = _sequence(
                    model,
                    examples,
                    start_index=probe_index,
                    condition=condition,
                    perturbation=perturbation,
                )

            base_selected = set(baseline[0]["selected"])
            changed_selected = set(changed[0]["selected"])
            rows.append(
                {
                    "case_id": (
                        f"{episode_id}:p{probe_position}:d{direction_index}:m{magnitude:.2f}"
                    ),
                    "episode_id": episode_id,
                    "episode_seed": episode_seed,
                    "probe_position_1based": probe_position,
                    "probe_step_index": int(examples[probe_index].step_index),
                    "direction_index": direction_index,
                    "magnitude": magnitude,
                    "condition": condition,
                    "router_logit_margin_k_kplus1": margin,
                    "encoded_l2_norm": encoded_norm,
                    "selected_baseline": sorted(base_selected),
                    "selected_perturbed": sorted(changed_selected),
                    "selected_set_turnover": base_selected != changed_selected,
                    "turnover_count": len(base_selected.symmetric_difference(changed_selected)) // 2,
                    **_metrics(baseline, changed),
                }
            )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_case: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        by_case.setdefault(row["case_id"], {})[row["condition"]] = row

    paired: list[dict[str, Any]] = []
    for case_id, conditions in by_case.items():
        if set(conditions) != {"full", "no_persistent_state"}:
            raise RuntimeError(f"Missing paired condition for {case_id}")
        full = conditions["full"]
        control = conditions["no_persistent_state"]
        if full["selected_set_turnover"] != control["selected_set_turnover"]:
            raise RuntimeError(f"Router turnover mismatch across conditions for {case_id}")
        paired.append(
            {
                "case_id": case_id,
                "magnitude": full["magnitude"],
                "turnover": full["selected_set_turnover"],
                "state_auc_ratio": _ratio(full["state_auc"], control["state_auc"]),
                "probability_auc_ratio": _ratio(
                    full["probability_auc"], control["probability_auc"]
                ),
                "action_logit_auc_ratio": _ratio(
                    full["action_logit_auc"], control["action_logit_auc"]
                ),
            }
        )

    turnover = [row for row in paired if row["turnover"]]
    by_magnitude: list[dict[str, Any]] = []
    for magnitude in MAGNITUDES:
        selected = [row for row in turnover if math.isclose(row["magnitude"], magnitude)]
        by_magnitude.append(
            {
                "magnitude": magnitude,
                "turnover_cases": len(selected),
                "median_state_auc_ratio": (
                    statistics.median(row["state_auc_ratio"] for row in selected)
                    if selected
                    else None
                ),
                "median_probability_auc_ratio": (
                    statistics.median(row["probability_auc_ratio"] for row in selected)
                    if selected
                    else None
                ),
                "median_action_logit_auc_ratio": (
                    statistics.median(row["action_logit_auc_ratio"] for row in selected)
                    if selected
                    else None
                ),
            }
        )

    if len(turnover) < TURNOVER_MINIMUM:
        classification = "ARCHITECTURE_INCONCLUSIVE_LOW_TURNOVER"
    else:
        signal_count = sum(
            bool(
                row["median_state_auc_ratio"] is not None
                and row["median_state_auc_ratio"] >= STATE_RATIO_SIGNAL
                and row["median_probability_auc_ratio"] is not None
                and row["median_probability_auc_ratio"] >= OUTPUT_RATIO_SIGNAL
            )
            for row in by_magnitude
        )
        ordinary_state = all(
            row["median_state_auc_ratio"] is not None
            and row["median_state_auc_ratio"] < STATE_RATIO_ORDINARY
            for row in by_magnitude
        )
        ordinary_output = all(
            row["median_probability_auc_ratio"] is not None
            and row["median_probability_auc_ratio"] < OUTPUT_RATIO_SIGNAL
            for row in by_magnitude
        )
        if signal_count >= 2:
            classification = "PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL"
        elif ordinary_state and ordinary_output:
            classification = "ORDINARY_ROUTER_BOUNDARY_EFFECT_ONLY"
        else:
            classification = "MIXED_ARCHITECTURE_RESULT"

    return {
        "classification": classification,
        "evidentiary_status": "NON_EVIDENTIARY_ARCHITECTURE_STUDY",
        "total_paired_cases": len(paired),
        "total_turnover_cases": len(turnover),
        "magnitude_summary": by_magnitude,
        "interpretation_contract": {
            "turnover_minimum": TURNOVER_MINIMUM,
            "state_ratio_signal": STATE_RATIO_SIGNAL,
            "probability_ratio_signal": OUTPUT_RATIO_SIGNAL,
            "state_ratio_ordinary": STATE_RATIO_ORDINARY,
            "ordinary_output_materiality": "probability AUC ratio < 1.5 at all magnitudes",
            "ratio_denominator_floor": RATIO_FLOOR,
        },
    }


def run(output_dir: Path) -> dict[str, Any]:
    config_path = Path("configs/experiments/phase2/main.json")
    raw = _read_json(config_path)
    config = LearnedConfig.from_dict(raw["learned"])
    dev_path = Path(raw["dev_manifest"])
    dev_manifest = _read_json(dev_path)
    training = _episodes(
        dev_manifest,
        count=config.train_episodes,
        worlds=tuple(raw["train_worlds"]),
        steps=config.steps,
    )
    calibration = _episodes(
        dev_manifest,
        count=config.calibration_episodes,
        worlds=tuple(raw["calibration_worlds"]),
        steps=config.steps + 6,
        offset=config.train_episodes,
    )
    model, training_history = train_model(config, training)
    model.eval()
    generator = torch.Generator().manual_seed(DIRECTION_SEED)
    raw_rows: list[dict[str, Any]] = []

    for episode in calibration:
        examples = episode_examples(episode)
        for probe_position in PROBE_POSITIONS:
            probe_index = probe_position - 1
            if probe_index + HORIZON >= len(examples):
                continue
            example = examples[probe_index]
            with torch.no_grad():
                encoded = model.encoder(
                    example.evidence_label,
                    example.source_id,
                    example.channel,
                    example.strength,
                    example.delivery_delay,
                ).detach()
                logits = torch.sort(model.router(encoded).detach(), descending=True).values
                margin = float(logits[config.active_k - 1] - logits[config.active_k])
            directions = _unit_directions(config.event_dim, generator)
            for condition in ("full", "no_persistent_state"):
                raw_rows.extend(
                    _probe_condition(
                        model,
                        examples,
                        probe_index=probe_index,
                        condition=condition,
                        directions=directions,
                        encoded=encoded,
                        margin=margin,
                        episode_id=episode.episode_id,
                        episode_seed=episode.seed,
                        probe_position=probe_position,
                    )
                )

    metadata = {
        "schema_version": "1",
        "study": "CAND-TOPK-PA-01",
        "research_layer": "ARCHITECTURE_STUDY",
        "evidentiary_status": "NON_EVIDENTIARY",
        "analyst_commit": ANALYST_COMMIT,
        "source_main_sha": EXPECTED_MAIN_SHA,
        "dev_manifest_path": str(dev_path),
        "dev_manifest_sha256": _sha256(dev_path),
        "test_manifest_opened": False,
        "config_path": str(config_path),
        "config": config.to_dict(),
        "training_episode_count": len(training),
        "calibration_episode_count": len(calibration),
        "probe_positions_1based": list(PROBE_POSITIONS),
        "probe_horizon": HORIZON,
        "direction_seed": DIRECTION_SEED,
        "directions_per_probe": DIRECTIONS_PER_PROBE,
        "magnitudes": list(MAGNITUDES),
        "conditions": ["full", "no_persistent_state"],
        "state_measurement": (
            "normalized L2 divergence of effective post-step per-module hidden state; "
            "the no-persistent control records its transient post-update state before the "
            "existing ablation clears the persistent runtime buffer"
        ),
        "auc_method": "trapezoidal over horizons 0..6",
        "direction_reuse": "same 8 unit directions reused across magnitudes within each probe",
        "probe_step_semantics": "1-based positions in 30-step DEV calibration episodes",
        "training_history": training_history,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "metadata.json", metadata)
    _write_json(output_dir / "raw_rows.json", raw_rows)
    result = _summary(raw_rows)
    _write_json(output_dir / "summary.json", result)
    print("ARCHITECTURE_STUDY_RESULT=" + json.dumps(result, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/architecture_studies/topk-persistent-amplification-cycle1"),
    )
    args = parser.parse_args()
    run(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
