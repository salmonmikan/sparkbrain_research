from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
from pathlib import Path
from typing import Any

import torch

from sparkbrain.learned.h7_dev_r1 import (
    CALIBRATION_SEEDS,
    DISCRIMINATOR_SEEDS,
    FIT_SEEDS,
    FROZEN_WORLDS,
    STEPS_PER_EPISODE,
    ContractConformanceError,
    dense_recurrent_comparator_config,
    native_development_config,
    paired_top1_selected_local_node_cut,
)
from sparkbrain.learned.h7_dev_r2 import CONTRACT_ID as DEV_R2_CONTRACT_ID
from sparkbrain.learned.h7_dev_r2 import (
    ENCODER_PROVENANCE,
    EligibilityRouteLedgerV2,
    FiniteStateRouteHistoryV2,
    InterventionConformanceSnapshot,
    LedgerFitStep,
    assert_dev_r2_contract,
    assert_intervention_well_posed,
)
from sparkbrain.learned.training import calibrate_ignition, episode_examples, train_model
from sparkbrain.tasks import generate_episode

PF_CONTRACT_ID = "H7-PF-R1-FROZEN-PANEL-DEVELOPMENT-EVALUATION-V1"
ANALYST_AUTHORITY = (
    "EVA-20260922T145734+0900-R64-F1A8C29D@"
    "0b201ca23c1de6fb568d78f320dc5a55ab85b70c"
)
SOURCE_HEAD = "d6655549c179caf391d4b43bd2ebea49f2bfc82b"
SOURCE_CONTRACT_BLOB = "82cb0fe44a958cda6d44758b0f15302f6e540793"
NO_CHANGE_TOLERANCE = 1e-7


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_json_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_bytes(payload)


def _tensor_digest(tensor: torch.Tensor) -> str:
    value = tensor.detach().cpu().contiguous()
    payload = value.numpy().tobytes()
    header = f"{tuple(value.shape)}|{value.dtype}|".encode()
    return _sha256_bytes(header + payload)


def _parameter_digest(model: torch.nn.Module) -> str:
    digest = hashlib.sha256()
    for name, parameter in sorted(model.named_parameters()):
        value = parameter.detach().cpu().contiguous()
        digest.update(name.encode())
        digest.update(str(tuple(value.shape)).encode())
        digest.update(str(value.dtype).encode())
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def _rng_digest() -> str:
    return _tensor_digest(torch.get_rng_state())


def _configure_runtime() -> dict[str, Any]:
    os.environ.setdefault("PYTHONHASHSEED", "0")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    return {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "platform": platform.platform(),
        "torch_threads": torch.get_num_threads(),
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "python_hash_seed": os.environ.get("PYTHONHASHSEED"),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
        "mkl_num_threads": os.environ.get("MKL_NUM_THREADS"),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_ref": os.environ.get("GITHUB_REF"),
    }


def _logical_episodes(name: str) -> list:
    ranges = {
        "fit": FIT_SEEDS,
        "calibration": CALIBRATION_SEEDS,
        "discriminator": DISCRIMINATOR_SEEDS,
    }
    seeds = ranges[name]
    return [
        generate_episode(
            FROZEN_WORLDS[index % len(FROZEN_WORLDS)],
            seed=seed,
            split="dev",
            steps=STEPS_PER_EPISODE,
        )
        for index, seed in enumerate(seeds)
    ]


def _assert_pf_contract(pf: dict[str, Any], source: dict[str, Any], source_path: Path) -> None:
    if pf["contract_id"] != PF_CONTRACT_ID:
        raise ContractConformanceError("PF-R1 contract id drifted")
    if source["contract_id"] != DEV_R2_CONTRACT_ID:
        raise ContractConformanceError("DEV-R2 source contract id drifted")
    assert_dev_r2_contract(source)
    created = pf["created_under"]
    binding = pf["source_binding"]
    scientific = pf["scientific_fields"]
    expected = {
        "development_phase": "RESULT_EXPOSED_DEVELOPMENT",
        "development_revision": "H7-PF-R1-FROZEN-PANEL-DEVELOPMENT-EVALUATION",
        "research_layer": "PRE_FORMAL",
        "claim_ceiling": "MECHANISM",
        "preformal_eligible": True,
        "preformal_readiness": "READY",
        "cycle": 4,
        "source_head": SOURCE_HEAD,
        "source_blob": SOURCE_CONTRACT_BLOB,
        "worlds": list(FROZEN_WORLDS),
        "fit": [FIT_SEEDS.start, FIT_SEEDS.stop - 1],
        "calibration": [CALIBRATION_SEEDS.start, CALIBRATION_SEEDS.stop - 1],
        "discriminator": [DISCRIMINATOR_SEEDS.start, DISCRIMINATOR_SEEDS.stop - 1],
        "tolerance": NO_CHANGE_TOLERANCE,
    }
    observed = {
        "development_phase": created["development_phase"],
        "development_revision": created["development_revision"],
        "research_layer": created["research_layer"],
        "claim_ceiling": created["claim_ceiling"],
        "preformal_eligible": created["preformal_eligible"],
        "preformal_readiness": created["preformal_readiness"],
        "cycle": created["cycle"],
        "source_head": binding["source_research_head"],
        "source_blob": binding["source_contract_blob"],
        "worlds": scientific["worlds"],
        "fit": scientific["fit_seed_range_inclusive"],
        "calibration": scientific["calibration_seed_range_inclusive"],
        "discriminator": scientific["discriminator_seed_range_inclusive"],
        "tolerance": scientific["numerical_no_change_tolerance"],
    }
    if observed != expected:
        raise ContractConformanceError(
            f"PF-R1 contract mismatch: expected={expected!r}, observed={observed!r}"
        )
    if source_path.name != "contract.json":
        raise ContractConformanceError("DEV-R2 source contract path drifted")


def _event_payload(example: Any) -> dict[str, Any]:
    return {
        "evidence": example.evidence_label,
        "source": example.source_id,
        "channel": example.channel,
        "strength": example.strength,
        "delay": example.delivery_delay,
        "step_index": example.step_index,
        "object_id": example.object_id,
    }


def _paired_checked(model: torch.nn.Module, example: Any, *, condition: str) -> Any:
    parameter_before = _parameter_digest(model)
    rng_before = _rng_digest()
    input_digest = _canonical_json_digest(_event_payload(example))
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
    parameter_after = _parameter_digest(model)
    rng_after = _rng_digest()
    if parameter_before != parameter_after:
        raise ContractConformanceError("INVALID_INTERVENTION: model parameters mutated")
    if rng_before != rng_after:
        raise ContractConformanceError("INVALID_INTERVENTION: RNG state mutated")
    snapshot = InterventionConformanceSnapshot(
        baseline_selected=pair.selected,
        cut_selected=pair.selected,
        baseline_output=pair.baseline.logits,
        cut_output=pair.cut.logits,
        baseline_input_digest=input_digest,
        cut_input_digest=input_digest,
        baseline_parameter_digest=parameter_before,
        cut_parameter_digest=parameter_after,
        baseline_rng_digest=rng_before,
        cut_rng_digest=rng_after,
        cut_state_carried_forward=not torch.equal(model.module_state, pair.baseline_post_state),
    )
    assert_intervention_well_posed(snapshot)
    return pair


def _collect_route_rows(model: torch.nn.Module, episodes: list) -> list[list[dict[str, Any]]]:
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


def _evaluate_paired_model(
    model: torch.nn.Module,
    config: Any,
    episodes: list,
    *,
    condition: str,
    retain_routes: bool,
) -> tuple[dict[str, Any], list[list[dict[str, Any]]]]:
    labels = tuple(config.labels)
    total = 0
    baseline_correct = 0
    cut_correct = 0
    tv_sum = 0.0
    rows: list[list[dict[str, Any]]] = []
    model.eval()
    for episode in episodes:
        model.reset_runtime()
        episode_rows: list[dict[str, Any]] = []
        for example in episode_examples(episode):
            pair = _paired_checked(model, example, condition=condition)
            baseline_probs = pair.baseline.probabilities.detach().cpu()
            cut_probs = pair.cut.probabilities.detach().cpu()
            baseline_label = labels[int(baseline_probs.argmax().item())]
            cut_label = labels[int(cut_probs.argmax().item())]
            total += 1
            baseline_correct += int(baseline_label == example.belief_truth)
            cut_correct += int(cut_label == example.belief_truth)
            tv = 0.5 * float(torch.abs(baseline_probs - cut_probs).sum().item())
            tv_sum += tv
            if retain_routes:
                episode_rows.append(
                    {
                        **_event_payload(example),
                        "truth": example.belief_truth,
                        "selected": list(pair.selected),
                        "route": pair.selected[0],
                        "baseline_label": baseline_label,
                        "cut_label": cut_label,
                        "baseline_probabilities": baseline_probs.tolist(),
                        "cut_probabilities": cut_probs.tolist(),
                        "total_variation": tv,
                    }
                )
        if retain_routes:
            rows.append(episode_rows)
    baseline_accuracy = baseline_correct / total
    cut_accuracy = cut_correct / total
    return (
        {
            "examples": total,
            "baseline_accuracy": baseline_accuracy,
            "cut_accuracy": cut_accuracy,
            "delta_accuracy": baseline_accuracy - cut_accuracy,
            "mean_total_variation": tv_sum / total,
        },
        rows,
    )


def _fit_fsa(route_rows: list[list[dict[str, Any]]], labels: tuple[str, ...]) -> Any:
    comparator = FiniteStateRouteHistoryV2(labels)
    for episode in route_rows:
        comparator.reset_episode()
        for row in episode:
            comparator.fit_step(
                unperturbed_rank1_route=int(row["route"]),
                label=str(row["truth"]),
            )
    return comparator


def _fsa_counts_digest(comparator: Any) -> str:
    rows = []
    for key, counts in sorted(comparator._counts.items(), key=lambda item: repr(item[0])):
        rows.append([repr(key), sorted(counts.items())])
    return _canonical_json_digest(
        {"counts": rows, "global": sorted(comparator._global_counts.items())}
    )


def _calibrate_fsa(comparator: Any, route_rows: list[list[dict[str, Any]]]) -> dict[str, Any]:
    before = _fsa_counts_digest(comparator)
    predictions = 0
    for episode in route_rows:
        comparator.reset_episode()
        for row in episode:
            comparator.predict_pair(unperturbed_rank1_route=int(row["route"]))
            predictions += 1
    after = _fsa_counts_digest(comparator)
    if before != after:
        raise ContractConformanceError("FSA calibration mutated frozen fit counts")
    return {
        "operation": "IMMUTABLE_TABLE_DIAGNOSTIC_ONLY",
        "predictions": predictions,
        "counts_digest_before": before,
        "counts_digest_after": after,
        "mutated": False,
    }


def _evaluate_fsa(
    comparator: Any, route_rows: list[list[dict[str, Any]]]
) -> tuple[dict[str, Any], list[list[dict[str, Any]]]]:
    total = 0
    baseline_correct = 0
    cut_correct = 0
    raw_rows: list[list[dict[str, Any]]] = []
    for episode in route_rows:
        comparator.reset_episode()
        episode_rows = []
        for row in episode:
            pair = comparator.predict_pair(unperturbed_rank1_route=int(row["route"]))
            truth = str(row["truth"])
            total += 1
            baseline_correct += int(pair.baseline == truth)
            cut_correct += int(pair.cut == truth)
            episode_rows.append(
                {
                    "truth": truth,
                    "route": int(row["route"]),
                    "baseline_label": pair.baseline,
                    "cut_label": pair.cut,
                }
            )
        raw_rows.append(episode_rows)
    baseline_accuracy = baseline_correct / total
    cut_accuracy = cut_correct / total
    return (
        {
            "examples": total,
            "baseline_accuracy": baseline_accuracy,
            "cut_accuracy": cut_accuracy,
            "delta_accuracy": baseline_accuracy - cut_accuracy,
            "mean_total_variation": None,
        },
        raw_rows,
    )


def _ledger_fit_rows(
    route_rows: list[list[dict[str, Any]]], labels: tuple[str, ...]
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


def _ledger_head_digest(comparator: EligibilityRouteLedgerV2) -> str:
    return _parameter_digest(comparator.head)


def _calibrate_ledger(
    comparator: EligibilityRouteLedgerV2, route_rows: list[list[dict[str, Any]]]
) -> dict[str, Any]:
    before = _ledger_head_digest(comparator)
    predictions = 0
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
                if not torch.isfinite(pair.baseline_logits).all() or not torch.isfinite(
                    pair.cut_logits
                ).all():
                    raise ContractConformanceError("ledger calibration emitted non-finite logits")
                ledger = pair.baseline_ledger.detach()
                predictions += 1
    after = _ledger_head_digest(comparator)
    if before != after:
        raise ContractConformanceError("ledger identity calibration mutated head weights")
    return {
        "operation": comparator.calibration_operation,
        "predictions": predictions,
        "head_digest_before": before,
        "head_digest_after": after,
        "mutated": False,
    }


def _evaluate_ledger(
    comparator: EligibilityRouteLedgerV2,
    route_rows: list[list[dict[str, Any]]],
    labels: tuple[str, ...],
) -> tuple[dict[str, Any], list[list[dict[str, Any]]]]:
    total = 0
    baseline_correct = 0
    cut_correct = 0
    tv_sum = 0.0
    raw_rows: list[list[dict[str, Any]]] = []
    with torch.no_grad():
        for episode in route_rows:
            ledger = comparator.initial_ledger(device=comparator.head.weight.device)
            episode_rows = []
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
                baseline_probs = torch.softmax(pair.baseline_logits, dim=-1).cpu()
                cut_probs = torch.softmax(pair.cut_logits, dim=-1).cpu()
                baseline_label = labels[int(baseline_probs.argmax().item())]
                cut_label = labels[int(cut_probs.argmax().item())]
                truth = str(row["truth"])
                total += 1
                baseline_correct += int(baseline_label == truth)
                cut_correct += int(cut_label == truth)
                tv = 0.5 * float(torch.abs(baseline_probs - cut_probs).sum().item())
                tv_sum += tv
                episode_rows.append(
                    {
                        "truth": truth,
                        "route": int(row["route"]),
                        "baseline_label": baseline_label,
                        "cut_label": cut_label,
                        "baseline_probabilities": baseline_probs.tolist(),
                        "cut_probabilities": cut_probs.tolist(),
                        "total_variation": tv,
                    }
                )
                ledger = pair.baseline_ledger.detach()
            raw_rows.append(episode_rows)
    baseline_accuracy = baseline_correct / total
    cut_accuracy = cut_correct / total
    return (
        {
            "examples": total,
            "baseline_accuracy": baseline_accuracy,
            "cut_accuracy": cut_accuracy,
            "delta_accuracy": baseline_accuracy - cut_accuracy,
            "mean_total_variation": tv_sum / total,
        },
        raw_rows,
    )


def _score(raw: dict[str, Any]) -> dict[str, Any]:
    native = raw["endpoints"]["native"]
    reductions = {}
    for name in ("dense_recurrent", "finite_state_route_history", "eligibility_route_ledger"):
        comparator = raw["endpoints"][name]
        reductions[name] = (
            comparator["baseline_accuracy"] >= native["baseline_accuracy"]
            and comparator["delta_accuracy"] >= native["delta_accuracy"]
        )
    positive = native["baseline_accuracy"] > (1.0 / 3.0)
    no_local_effect = (
        native["delta_accuracy"] <= 0.0
        and native["mean_total_variation"] <= NO_CHANGE_TOLERANCE
    )
    if not positive:
        disposition = "PHENOMENON_NOT_DEMONSTRATED"
    elif no_local_effect:
        disposition = "NO_LOCAL_EFFECT"
    elif any(reductions.values()):
        disposition = "REDUCED_BY_ORDINARY_COMPARATOR"
    else:
        disposition = "RESIDUAL_BEYOND_FROZEN_PANEL_PREFORMAL_NONCONFIRMATORY"
    return {
        "disposition": disposition,
        "positive_phenomenon_floor_passed": positive,
        "native_no_local_effect": no_local_effect,
        "ordinary_reduction_direction_met": reductions,
        "capacity_limit_status": {
            name: "NOT_ESTABLISHED_BY_FIXED_PROTOCOL" for name in reductions
        },
        "formal_uplift_authorized": False,
        "interpretation_ceiling": (
            "PRE_FORMAL development observation only; local existential responsibility within "
            "the frozen four-world/intervention-family regime at most."
        ),
    }


def _preflight(pf_path: Path, source_path: Path) -> dict[str, Any]:
    pf = _read_json(pf_path)
    source = _read_json(source_path)
    _assert_pf_contract(pf, source, source_path)
    expected_counts = {
        "fit": len(FIT_SEEDS),
        "calibration": len(CALIBRATION_SEEDS),
        "discriminator": len(DISCRIMINATOR_SEEDS),
    }
    if expected_counts != {"fit": 48, "calibration": 12, "discriminator": 24}:
        raise ContractConformanceError("frozen split counts drifted")
    return {
        "status": "PREFLIGHT_OK_NO_RESULT_SURFACE_ACCESSED",
        "contract_id": PF_CONTRACT_ID,
        "source_head": SOURCE_HEAD,
        "expected_counts": expected_counts,
        "worlds": list(FROZEN_WORLDS),
    }


def run(output_dir: Path, authority: str) -> dict[str, Any]:
    if authority != ANALYST_AUTHORITY:
        raise PermissionError("PF-R1 requires exact R64 Evidence Analyst authority")
    root = Path(__file__).resolve().parents[1]
    pf_path = root / "artifacts/preformal_h7_pf_r1/contract.json"
    source_path = root / "artifacts/architecture_h7_dev_r2/contract.json"
    _preflight(pf_path, source_path)
    runtime = _configure_runtime()

    fit = _logical_episodes("fit")
    calibration = _logical_episodes("calibration")

    native_config = native_development_config()
    dense_config = dense_recurrent_comparator_config()
    native, native_history = train_model(native_config, fit)
    dense, dense_history = train_model(dense_config, fit)
    native_calibrated = calibrate_ignition(native_config, native, calibration)
    dense_calibrated = calibrate_ignition(dense_config, dense, calibration)

    fit_routes = _collect_route_rows(native, fit)
    calibration_routes = _collect_route_rows(native, calibration)
    labels = tuple(native_config.labels)
    fsa = _fit_fsa(fit_routes, labels)
    fsa_calibration = _calibrate_fsa(fsa, calibration_routes)

    ledger = EligibilityRouteLedgerV2(
        native.encoder,
        encoder_provenance=ENCODER_PROVENANCE,
        module_count=native_config.module_count,
        event_dim=native_config.event_dim,
        labels=len(labels),
    )
    ledger.fit(_ledger_fit_rows(fit_routes, labels))
    ledger_calibration = _calibrate_ledger(ledger, calibration_routes)

    discriminator = _logical_episodes("discriminator")
    native_endpoint, discriminator_routes = _evaluate_paired_model(
        native,
        native_calibrated,
        discriminator,
        condition="full",
        retain_routes=True,
    )
    dense_endpoint, _ = _evaluate_paired_model(
        dense,
        dense_calibrated,
        discriminator,
        condition="dense_recurrent",
        retain_routes=False,
    )
    fsa_endpoint, fsa_rows = _evaluate_fsa(fsa, discriminator_routes)
    ledger_endpoint, ledger_rows = _evaluate_ledger(ledger, discriminator_routes, labels)

    raw = {
        "schema_version": 2,
        "classification": "PRE_FORMAL_DEVELOPMENT_NONCONFIRMATORY_RAW",
        "authority": authority,
        "contract_id": PF_CONTRACT_ID,
        "source_head": SOURCE_HEAD,
        "runtime": runtime,
        "surface": {
            "worlds": list(FROZEN_WORLDS),
            "steps_per_episode": STEPS_PER_EPISODE,
            "fit_seeds": [FIT_SEEDS.start, FIT_SEEDS.stop - 1],
            "calibration_seeds": [CALIBRATION_SEEDS.start, CALIBRATION_SEEDS.stop - 1],
            "discriminator_seeds": [DISCRIMINATOR_SEEDS.start, DISCRIMINATOR_SEEDS.stop - 1],
            "task_schema_split": "dev for all logical development partitions",
        },
        "training": {
            "native_history": native_history,
            "dense_history": dense_history,
        },
        "calibration": {
            "native": {
                "confidence_threshold": native_calibrated.confidence_threshold,
                "margin_threshold": native_calibrated.margin_threshold,
            },
            "dense_recurrent": {
                "confidence_threshold": dense_calibrated.confidence_threshold,
                "margin_threshold": dense_calibrated.margin_threshold,
            },
            "finite_state_route_history": fsa_calibration,
            "eligibility_route_ledger": ledger_calibration,
        },
        "endpoints": {
            "native": native_endpoint,
            "dense_recurrent": dense_endpoint,
            "finite_state_route_history": fsa_endpoint,
            "eligibility_route_ledger": ledger_endpoint,
        },
        "raw_discriminator_rows": {
            "native": discriminator_routes,
            "finite_state_route_history": fsa_rows,
            "eligibility_route_ledger": ledger_rows,
        },
        "integrity": {
            "intervention_checks_fail_closed": True,
            "discriminator_used_for_training_or_calibration": False,
            "post_outcome_retuning": False,
            "consumed_formal_identity_used": False,
            "official_test_started_formal_evidence_tag_created": False,
        },
    }
    raw_path = output_dir / "raw.json"
    _write_json(raw_path, raw)
    summary = {
        "schema_version": 2,
        "classification": "PRE_FORMAL_DEVELOPMENT_NONCONFIRMATORY_SUMMARY",
        "raw_sha256": _sha256_path(raw_path),
        "authority": authority,
        "contract_id": PF_CONTRACT_ID,
        "endpoints": raw["endpoints"],
        "fixed_scoring": _score(raw),
        "stop": "STOP_FRESH_EVIDENCE_ANALYST_REVIEW_NO_OUTCOME_RESPONSIVE_REDESIGN",
    }
    _write_json(output_dir / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/preformal_h7_pf_r1/result"),
    )
    parser.add_argument("--authority", default="")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    pf_path = root / "artifacts/preformal_h7_pf_r1/contract.json"
    source_path = root / "artifacts/architecture_h7_dev_r2/contract.json"
    if args.preflight:
        print(json.dumps(_preflight(pf_path, source_path), indent=2, sort_keys=True))
        return
    summary = run(args.output_dir, args.authority)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
