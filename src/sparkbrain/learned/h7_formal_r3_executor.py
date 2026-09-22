from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

import torch
import torch.nn.functional as F
from torch import Tensor, nn

from ..tasks import generate_episode
from .h7_dev_r1 import (
    dense_recurrent_comparator_config,
    native_development_config,
    paired_top1_selected_local_node_cut,
)
from .h7_dev_r2 import (
    ENCODER_PROVENANCE,
    GRAD_CLIP_NORM,
    HEAD_EPOCHS,
    HEAD_LR,
    EligibilityRouteLedgerV2,
    FiniteStateRouteHistoryV2,
    InterventionConformanceSnapshot,
    LedgerFitStep,
    assert_intervention_well_posed,
)
from .h7_formal_r1 import INTERVENTION_ID, FormalIntegrityError
from .h7_formal_r2 import (
    CALIBRATION_SEEDS,
    CALIBRATION_SPLIT,
    DENSE_TRAINING_SEED,
    ELIGIBILITY_HEAD_SEED,
    FIT_SEEDS,
    FIT_SPLIT,
    NATIVE_TRAINING_SEED,
)
from .h7_formal_r3 import (
    EVALUATION_EPISODES,
    EVALUATION_EPISODES_PER_WORLD,
    EVALUATION_SPLIT,
    STEPS_PER_EPISODE,
    WORLDS,
)
from .h7_formal_r3_integrity import validate_prediction_raw_row
from .training import calibrate_ignition, episode_examples, train_model


@dataclass(frozen=True, slots=True)
class ProtectedEpisodeSpec:
    """Controller-supplied concealed evaluation episode binding.

    The executor consumes this structure only after the future one-way controller
    has authorized access. It never writes the world or seed into prediction raw.
    """

    world: str
    seed: int
    opaque_target_ids: tuple[str, ...]

    def assert_valid(self) -> None:
        if self.world not in WORLDS:
            raise FormalIntegrityError("R3 protected episode world drift")
        if not isinstance(self.seed, int):
            raise FormalIntegrityError("R3 protected episode seed must be an integer")
        if len(self.opaque_target_ids) != STEPS_PER_EPISODE:
            raise FormalIntegrityError("R3 protected episode target-id count drift")
        for token in self.opaque_target_ids:
            if len(token) != 64 or any(char not in "0123456789abcdef" for char in token):
                raise FormalIntegrityError(
                    "R3 protected opaque target id must be lowercase SHA-256"
                )


@dataclass(slots=True)
class FrozenExecutionState:
    native: nn.Module
    dense: nn.Module
    native_config: Any
    dense_config: Any
    fsa: FiniteStateRouteHistoryV2
    ledger: EligibilityRouteLedgerV2
    labels: tuple[str, ...]


def validate_protected_evaluation_plan(plan: Sequence[ProtectedEpisodeSpec]) -> None:
    if len(plan) != EVALUATION_EPISODES:
        raise FormalIntegrityError("R3 protected evaluation episode-count drift")
    counts = Counter(spec.world for spec in plan)
    expected_counts = Counter({world: EVALUATION_EPISODES_PER_WORLD for world in WORLDS})
    if counts != expected_counts:
        raise FormalIntegrityError("R3 protected evaluation per-world count drift")
    seeds = [spec.seed for spec in plan]
    if len(seeds) != len(set(seeds)):
        raise FormalIntegrityError("R3 protected evaluation contains duplicate seeds")
    opaque_ids: list[str] = []
    for index, spec in enumerate(plan):
        spec.assert_valid()
        if spec.world != WORLDS[index % len(WORLDS)]:
            raise FormalIntegrityError("R3 protected evaluation world-assignment drift")
        opaque_ids.extend(spec.opaque_target_ids)
    if len(opaque_ids) != len(set(opaque_ids)):
        raise FormalIntegrityError("R3 protected evaluation contains duplicate opaque ids")


def _parameter_digest(model: nn.Module) -> str:
    digest = hashlib.sha256()
    for name, parameter in sorted(model.named_parameters()):
        value = parameter.detach().cpu().contiguous()
        digest.update(name.encode())
        digest.update(str(tuple(value.shape)).encode())
        digest.update(str(value.dtype).encode())
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def _tensor_digest(tensor: Tensor) -> str:
    value = tensor.detach().cpu().contiguous()
    header = f"{tuple(value.shape)}|{value.dtype}|".encode()
    return hashlib.sha256(header + value.numpy().tobytes()).hexdigest()


def _rng_digest() -> str:
    return _tensor_digest(torch.get_rng_state())


def _event_payload(example: Any) -> dict[str, Any]:
    return {
        "evidence": example.evidence_label,
        "source": example.source_id,
        "channel": example.channel,
        "strength": example.strength,
        "delay": example.delivery_delay,
    }


def _canonical_digest(value: Any) -> str:
    import json

    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _paired_checked(model: nn.Module, example: Any, *, condition: str) -> Any:
    parameter_before = _parameter_digest(model)
    rng_before = _rng_digest()
    input_digest = _canonical_digest(
        {
            **_event_payload(example),
            "step_index": example.step_index,
            "object_id": example.object_id,
        }
    )
    with torch.no_grad():
        pair = paired_top1_selected_local_node_cut(
            model,
            evidence=example.evidence_label,
            source=example.source_id,
            channel=example.channel,
            strength=example.strength,
            delay=example.delivery_delay,
            condition=condition,
        )
    snapshot = InterventionConformanceSnapshot(
        baseline_selected=pair.selected,
        cut_selected=pair.selected,
        baseline_output=pair.baseline.logits,
        cut_output=pair.cut.logits,
        baseline_input_digest=input_digest,
        cut_input_digest=input_digest,
        baseline_parameter_digest=parameter_before,
        cut_parameter_digest=_parameter_digest(model),
        baseline_rng_digest=rng_before,
        cut_rng_digest=_rng_digest(),
        cut_state_carried_forward=not torch.equal(model.module_state, pair.baseline_post_state),
    )
    assert_intervention_well_posed(snapshot)
    return pair


def _materialize_development_episodes(role: str) -> list[Any]:
    if role == "fit":
        seeds, split = FIT_SEEDS, FIT_SPLIT
    elif role == "calibration":
        seeds, split = CALIBRATION_SEEDS, CALIBRATION_SPLIT
    else:
        raise FormalIntegrityError("R3 executor may materialize only public fit/calibration roles")
    return [
        generate_episode(
            WORLDS[index % len(WORLDS)],
            seed=seed,
            split=split,
            steps=STEPS_PER_EPISODE,
        )
        for index, seed in enumerate(seeds)
    ]


def _collect_development_route_rows(
    model: nn.Module, episodes: Sequence[Any]
) -> list[list[dict[str, Any]]]:
    rows: list[list[dict[str, Any]]] = []
    model.eval()
    for episode in episodes:
        model.reset_runtime()
        episode_rows: list[dict[str, Any]] = []
        for example in episode_examples(episode):
            pair = _paired_checked(model, example, condition="full")
            episode_rows.append(
                {
                    **_event_payload(example),
                    "truth": example.belief_truth,
                    "selected": list(pair.selected),
                    "route": pair.selected[0],
                }
            )
        rows.append(episode_rows)
    return rows


def _fit_fsa(
    route_rows: Sequence[Sequence[Mapping[str, Any]]], labels: tuple[str, ...]
) -> FiniteStateRouteHistoryV2:
    comparator = FiniteStateRouteHistoryV2(labels)
    for episode in route_rows:
        comparator.reset_episode()
        for row in episode:
            comparator.fit_step(
                unperturbed_rank1_route=int(row["route"]),
                label=str(row["truth"]),
            )
    return comparator


def _calibrate_fsa(
    comparator: FiniteStateRouteHistoryV2,
    route_rows: Sequence[Sequence[Mapping[str, Any]]],
) -> None:
    before = _canonical_digest(
        {
            "counts": [
                [repr(key), sorted(counts.items())]
                for key, counts in sorted(
                    comparator._counts.items(), key=lambda item: repr(item[0])
                )
            ],
            "global": sorted(comparator._global_counts.items()),
        }
    )
    for episode in route_rows:
        comparator.reset_episode()
        for row in episode:
            comparator.predict_pair(unperturbed_rank1_route=int(row["route"]))
    after = _canonical_digest(
        {
            "counts": [
                [repr(key), sorted(counts.items())]
                for key, counts in sorted(
                    comparator._counts.items(), key=lambda item: repr(item[0])
                )
            ],
            "global": sorted(comparator._global_counts.items()),
        }
    )
    if before != after:
        raise FormalIntegrityError("R3 FSA calibration mutated fit counts")


def _ledger_fit_rows(
    route_rows: Sequence[Sequence[Mapping[str, Any]]], labels: tuple[str, ...]
) -> list[list[LedgerFitStep]]:
    label_index = {label: index for index, label in enumerate(labels)}
    return [
        [
            LedgerFitStep(
                evidence=str(row["evidence"]),
                source=str(row["source"]),
                channel=str(row["channel"]),
                strength=float(row["strength"]),
                delay=float(row["delay"]),
                selected=tuple(int(value) for value in row["selected"]),
                label_index=label_index[str(row["truth"])],
            )
            for row in episode
        ]
        for episode in route_rows
    ]


def _configure_formal_eligibility_ledger(comparator: EligibilityRouteLedgerV2) -> None:
    output_features = comparator.head.out_features
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(ELIGIBILITY_HEAD_SEED)
        comparator.head = nn.Linear(
            comparator.module_count + comparator.event_dim,
            output_features,
        )


def _fit_formal_eligibility_ledger(
    comparator: EligibilityRouteLedgerV2,
    episodes: Sequence[Sequence[LedgerFitStep]],
) -> None:
    optimizer = torch.optim.Adam(comparator.head.parameters(), lr=HEAD_LR, weight_decay=0.0)
    for epoch in range(HEAD_EPOCHS):
        generator = torch.Generator(device="cpu")
        generator.manual_seed(ELIGIBILITY_HEAD_SEED + epoch)
        order = torch.randperm(len(episodes), generator=generator).tolist()
        for episode_index in order:
            episode = episodes[episode_index]
            if not episode:
                raise FormalIntegrityError("R3 ledger fit episode must not be empty")
            ledger = comparator.initial_ledger(device=comparator.head.weight.device)
            optimizer.zero_grad()
            losses: list[Tensor] = []
            for step in episode:
                selected = torch.tensor(
                    step.selected,
                    dtype=torch.long,
                    device=comparator.head.weight.device,
                )
                ledger = comparator.advance_ledger(ledger, selected, cut=False)
                encoded = comparator.encode_event(
                    evidence=step.evidence,
                    source=step.source,
                    channel=step.channel,
                    strength=step.strength,
                    delay=step.delay,
                ).to(comparator.head.weight.device)
                logits = comparator.logits(ledger, encoded)
                target = torch.tensor([step.label_index], dtype=torch.long, device=logits.device)
                losses.append(F.cross_entropy(logits.unsqueeze(0), target))
            torch.stack(losses).mean().backward()
            torch.nn.utils.clip_grad_norm_(comparator.head.parameters(), GRAD_CLIP_NORM)
            optimizer.step()


def _calibrate_ledger(
    comparator: EligibilityRouteLedgerV2,
    route_rows: Sequence[Sequence[Mapping[str, Any]]],
) -> None:
    before = _parameter_digest(comparator.head)
    with torch.no_grad():
        for episode in route_rows:
            ledger = comparator.initial_ledger(device=comparator.head.weight.device)
            for row in episode:
                selected = torch.tensor(row["selected"], dtype=torch.long)
                encoded = comparator.encode_event(
                    evidence=str(row["evidence"]),
                    source=str(row["source"]),
                    channel=str(row["channel"]),
                    strength=float(row["strength"]),
                    delay=float(row["delay"]),
                )
                pair = comparator.paired_logits(ledger, selected, encoded)
                if (
                    not torch.isfinite(pair.baseline_logits).all()
                    or not torch.isfinite(pair.cut_logits).all()
                ):
                    raise FormalIntegrityError("R3 ledger calibration emitted non-finite logits")
                ledger = pair.baseline_ledger.detach()
    if before != _parameter_digest(comparator.head):
        raise FormalIntegrityError("R3 ledger calibration mutated head weights")


def build_frozen_execution_state() -> FrozenExecutionState:
    fit = _materialize_development_episodes("fit")
    calibration = _materialize_development_episodes("calibration")
    native_config = replace(native_development_config(), seed=NATIVE_TRAINING_SEED)
    dense_config = replace(dense_recurrent_comparator_config(), seed=DENSE_TRAINING_SEED)
    native, _ = train_model(native_config, fit)
    dense, _ = train_model(dense_config, fit)
    native_calibrated = calibrate_ignition(native_config, native, calibration)
    dense_calibrated = calibrate_ignition(dense_config, dense, calibration)

    fit_routes = _collect_development_route_rows(native, fit)
    calibration_routes = _collect_development_route_rows(native, calibration)
    labels = tuple(native_config.labels)
    fsa = _fit_fsa(fit_routes, labels)
    _calibrate_fsa(fsa, calibration_routes)

    ledger = EligibilityRouteLedgerV2(
        native.encoder,
        encoder_provenance=ENCODER_PROVENANCE,
        module_count=native_config.module_count,
        event_dim=native_config.event_dim,
        labels=len(labels),
    )
    _configure_formal_eligibility_ledger(ledger)
    _fit_formal_eligibility_ledger(ledger, _ledger_fit_rows(fit_routes, labels))
    _calibrate_ledger(ledger, calibration_routes)
    return FrozenExecutionState(
        native=native,
        dense=dense,
        native_config=native_calibrated,
        dense_config=dense_calibrated,
        fsa=fsa,
        ledger=ledger,
        labels=labels,
    )


def _append_validated(rows: list[dict[str, Any]], row: dict[str, Any]) -> None:
    validate_prediction_raw_row(row)
    rows.append(row)


def _emit_model_episode(
    *,
    endpoint: str,
    model: nn.Module,
    config: Any,
    episode: Any,
    opaque_target_ids: Sequence[str],
    condition: str,
    retain_routes: bool,
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    labels = tuple(config.labels)
    route_rows: list[dict[str, Any]] = []
    examples = list(episode_examples(episode))
    if len(examples) != len(opaque_target_ids):
        raise FormalIntegrityError("R3 opaque target-id coverage drift")
    model.eval()
    model.reset_runtime()
    for example, opaque_target_id in zip(examples, opaque_target_ids, strict=True):
        pair = _paired_checked(model, example, condition=condition)
        baseline_probs = pair.baseline.probabilities.detach().cpu()
        cut_probs = pair.cut.probabilities.detach().cpu()
        baseline_label = labels[int(baseline_probs.argmax().item())]
        cut_label = labels[int(cut_probs.argmax().item())]
        _append_validated(
            rows,
            {
                "opaque_target_id": opaque_target_id,
                "endpoint": endpoint,
                "intervention_id": INTERVENTION_ID,
                "baseline_prediction": baseline_label,
                "cut_prediction": cut_label,
                "baseline_probabilities": baseline_probs.tolist(),
                "cut_probabilities": cut_probs.tolist(),
            },
        )
        if retain_routes:
            route_rows.append(
                {
                    **_event_payload(example),
                    "selected": list(pair.selected),
                    "route": pair.selected[0],
                    "opaque_target_id": opaque_target_id,
                }
            )
    return route_rows


def _emit_fsa_episode(
    comparator: FiniteStateRouteHistoryV2,
    route_rows: Sequence[Mapping[str, Any]],
    rows: list[dict[str, Any]],
) -> None:
    comparator.reset_episode()
    for route_row in route_rows:
        pair = comparator.predict_pair(unperturbed_rank1_route=int(route_row["route"]))
        _append_validated(
            rows,
            {
                "opaque_target_id": str(route_row["opaque_target_id"]),
                "endpoint": "FINITE_STATE_ROUTE_HISTORY_V2",
                "intervention_id": INTERVENTION_ID,
                "baseline_prediction": pair.baseline,
                "cut_prediction": pair.cut,
            },
        )


def _emit_ledger_episode(
    comparator: EligibilityRouteLedgerV2,
    route_rows: Sequence[Mapping[str, Any]],
    labels: tuple[str, ...],
    rows: list[dict[str, Any]],
) -> None:
    with torch.no_grad():
        ledger = comparator.initial_ledger(device=comparator.head.weight.device)
        for route_row in route_rows:
            selected = torch.tensor(
                route_row["selected"],
                dtype=torch.long,
                device=comparator.head.weight.device,
            )
            encoded = comparator.encode_event(
                evidence=str(route_row["evidence"]),
                source=str(route_row["source"]),
                channel=str(route_row["channel"]),
                strength=float(route_row["strength"]),
                delay=float(route_row["delay"]),
            ).to(comparator.head.weight.device)
            pair = comparator.paired_logits(ledger, selected, encoded)
            baseline_probs = torch.softmax(pair.baseline_logits, dim=-1).cpu()
            cut_probs = torch.softmax(pair.cut_logits, dim=-1).cpu()
            _append_validated(
                rows,
                {
                    "opaque_target_id": str(route_row["opaque_target_id"]),
                    "endpoint": "ELIGIBILITY_ROUTE_LEDGER_V2",
                    "intervention_id": INTERVENTION_ID,
                    "baseline_prediction": labels[int(baseline_probs.argmax().item())],
                    "cut_prediction": labels[int(cut_probs.argmax().item())],
                    "baseline_probabilities": baseline_probs.tolist(),
                    "cut_probabilities": cut_probs.tolist(),
                },
            )
            ledger = pair.baseline_ledger.detach()


def emit_prediction_rows_for_episode(
    *,
    state: FrozenExecutionState,
    episode: Any,
    opaque_target_ids: Sequence[str],
) -> list[dict[str, Any]]:
    """Emit target-blind predictions for one caller-supplied episode.

    This function never reads ``belief_truth``, world, seed, or split from the
    episode while producing raw rows. Scientific scoring remains a separate
    post-preserve operation in :mod:`h7_formal_r3_integrity`.
    """

    rows: list[dict[str, Any]] = []
    route_rows = _emit_model_episode(
        endpoint="native",
        model=state.native,
        config=state.native_config,
        episode=episode,
        opaque_target_ids=opaque_target_ids,
        condition="full",
        retain_routes=True,
        rows=rows,
    )
    _emit_model_episode(
        endpoint="ORDINARY_DENSE_RECURRENT_V1",
        model=state.dense,
        config=state.dense_config,
        episode=episode,
        opaque_target_ids=opaque_target_ids,
        condition="dense_recurrent",
        retain_routes=False,
        rows=rows,
    )
    _emit_fsa_episode(state.fsa, route_rows, rows)
    _emit_ledger_episode(state.ledger, route_rows, state.labels, rows)
    return rows


def execute_protected_evaluation_plan(
    plan: Sequence[ProtectedEpisodeSpec],
) -> list[dict[str, Any]]:
    """Future protected executor core; controller gating remains external.

    Cycle 11 may bind and validate this implementation only on synthetic or
    non-protected surfaces. Calling this function on protected evaluation data
    remains forbidden until a fresh Analyst authorizes the one-way chain.
    """

    validate_protected_evaluation_plan(plan)
    state = build_frozen_execution_state()
    rows: list[dict[str, Any]] = []
    for spec in plan:
        episode = generate_episode(
            spec.world,
            seed=spec.seed,
            split=EVALUATION_SPLIT,
            steps=STEPS_PER_EPISODE,
        )
        rows.extend(
            emit_prediction_rows_for_episode(
                state=state,
                episode=episode,
                opaque_target_ids=spec.opaque_target_ids,
            )
        )
    return rows


def synthetic_nonprotected_realization_probe() -> dict[str, Any]:
    """Exercise the protected executor mechanics without any held-out surface."""

    state = build_frozen_execution_state()
    seed = FIT_SEEDS.start
    episode = generate_episode(
        WORLDS[0],
        seed=seed,
        split=FIT_SPLIT,
        steps=STEPS_PER_EPISODE,
    )
    opaque_ids = tuple(
        hashlib.sha256(f"h7-r4-cycle11-nonprotected-{index}".encode()).hexdigest()
        for index in range(STEPS_PER_EPISODE)
    )
    rows = emit_prediction_rows_for_episode(
        state=state,
        episode=episode,
        opaque_target_ids=opaque_ids,
    )
    expected_rows = STEPS_PER_EPISODE * 4
    if len(rows) != expected_rows:
        raise FormalIntegrityError("R4 synthetic executor row-count drift")
    forbidden = {"world", "episode_seed", "step_index", "truth", "baseline_correct", "cut_correct"}
    if any(set(row) & forbidden for row in rows):
        raise FormalIntegrityError(
            "R4 synthetic executor leaked target-derived identity or correctness"
        )
    endpoints = Counter(str(row["endpoint"]) for row in rows)
    if set(endpoints.values()) != {STEPS_PER_EPISODE}:
        raise FormalIntegrityError("R4 synthetic executor endpoint coverage drift")
    return {
        "status": "H7_R4_CYCLE11_NONPROTECTED_EXECUTOR_REALIZED",
        "rows": len(rows),
        "endpoints": sorted(endpoints),
        "protected_evaluation_accessed": False,
        "scoring_performed": False,
        "scientific_result": None,
    }
