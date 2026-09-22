from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import torch
import torch.nn.functional as F
from torch import Tensor, nn

from ..tasks import generate_episode
from .h7_dev_r1 import (
    ContractConformanceError,
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
from .h7_formal_r1 import FormalIntegrityError, TargetBlindRawCollector, sha256_path
from .h7_formal_r1_preflight import RuntimeFreezeManifest, pip_freeze_digest
from .h7_formal_r2 import (
    CALIBRATION_SEEDS,
    DENSE_TRAINING_SEED,
    ELIGIBILITY_HEAD_SEED,
    EVALUATION_SEEDS,
    FIT_SEEDS,
    NATIVE_TRAINING_SEED,
    STEPS_PER_EPISODE,
    FutureIdentityBindingR2,
    episode_plan,
    load_and_assert_r2_contract,
    preidentity_sentinel,
)
from .training import calibrate_ignition, episode_examples, train_model


PACKAGE_MANIFEST_SCHEMA = 2
RUNTIME_MANIFEST_SCHEMA = 2


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324 - Git object identity uses SHA-1.


def _tensor_digest(tensor: Tensor) -> str:
    value = tensor.detach().cpu().contiguous()
    header = f"{tuple(value.shape)}|{value.dtype}|".encode()
    return _sha256_bytes(header + value.numpy().tobytes())


def _parameter_digest(model: nn.Module) -> str:
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


def build_package_manifest(root: Path) -> dict[str, Any]:
    paths = sorted((root / "src" / "sparkbrain").rglob("*.py"))
    pyproject = root / "pyproject.toml"
    if not paths or not pyproject.is_file():
        raise FormalIntegrityError("package source surface is incomplete")
    paths.append(pyproject)
    files = {
        path.relative_to(root).as_posix(): _sha256_bytes(path.read_bytes())
        for path in sorted(paths)
    }
    manifest = {
        "schema_version": PACKAGE_MANIFEST_SCHEMA,
        "kind": "H7_FORMAL_R2_PACKAGE_MANIFEST",
        "files": files,
    }
    manifest["manifest_sha256"] = _sha256_bytes(_json_bytes(manifest))
    return manifest


def build_runtime_manifest() -> dict[str, Any]:
    freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze", "--disable-pip-version-check"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    image_version = os.environ.get("ImageVersion") or os.environ.get("IMAGE_VERSION")
    if not image_version:
        image_version = platform.platform()
    runtime = RuntimeFreezeManifest(
        python_patch=platform.python_version(),
        torch_version=torch.__version__,
        os_runner_family="ubuntu-24.04",
        os_image_identifier=image_version,
        pip_freeze_sha256=pip_freeze_digest(freeze),
        device="cpu",
        cpu_threads=1,
        python_hash_seed=os.environ.get("PYTHONHASHSEED", ""),
        omp_num_threads=os.environ.get("OMP_NUM_THREADS", ""),
        mkl_num_threads=os.environ.get("MKL_NUM_THREADS", ""),
        torch_deterministic_algorithms=torch.are_deterministic_algorithms_enabled(),
    )
    value = {
        "schema_version": RUNTIME_MANIFEST_SCHEMA,
        "kind": "H7_FORMAL_R2_RUNTIME_MANIFEST",
        **runtime.as_dict(),
    }
    value["manifest_sha256"] = _sha256_bytes(_json_bytes(value))
    return value


def configure_runtime() -> None:
    os.environ.setdefault("PYTHONHASHSEED", "0")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def materialize_episodes(role: str) -> list[Any]:
    return [
        generate_episode(world, seed=seed, split=split, steps=STEPS_PER_EPISODE)
        for world, seed, split in episode_plan(role)
    ]


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


def _canonical_digest(value: Any) -> str:
    return _sha256_bytes(_json_bytes(value))


def _paired_checked(model: nn.Module, example: Any, *, condition: str) -> Any:
    parameter_before = _parameter_digest(model)
    rng_before = _rng_digest()
    input_digest = _canonical_digest(_event_payload(example))
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


def _collect_route_rows(model: nn.Module, episodes: Sequence[Any]) -> list[list[dict[str, Any]]]:
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


def _fit_fsa(route_rows: Sequence[Sequence[Mapping[str, Any]]], labels: tuple[str, ...]) -> Any:
    comparator = FiniteStateRouteHistoryV2(labels)
    for episode in route_rows:
        comparator.reset_episode()
        for row in episode:
            comparator.fit_step(
                unperturbed_rank1_route=int(row["route"]),
                label=str(row["truth"]),
            )
    return comparator


def _calibrate_fsa(comparator: Any, route_rows: Sequence[Sequence[Mapping[str, Any]]]) -> None:
    before = _canonical_digest(
        {
            "counts": [
                [repr(key), sorted(counts.items())]
                for key, counts in sorted(comparator._counts.items(), key=lambda item: repr(item[0]))
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
                for key, counts in sorted(comparator._counts.items(), key=lambda item: repr(item[0]))
            ],
            "global": sorted(comparator._global_counts.items()),
        }
    )
    if before != after:
        raise FormalIntegrityError("formal FSA calibration mutated fit counts")


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


def configure_formal_eligibility_ledger(comparator: EligibilityRouteLedgerV2) -> None:
    output_features = comparator.head.out_features
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(ELIGIBILITY_HEAD_SEED)
        comparator.head = nn.Linear(
            comparator.module_count + comparator.event_dim,
            output_features,
        )


def fit_formal_eligibility_ledger(
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
                raise FormalIntegrityError("formal ledger fit episode must not be empty")
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
                target = torch.tensor(
                    [step.label_index],
                    dtype=torch.long,
                    device=logits.device,
                )
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
                if not torch.isfinite(pair.baseline_logits).all() or not torch.isfinite(
                    pair.cut_logits
                ).all():
                    raise FormalIntegrityError("formal ledger calibration emitted non-finite logits")
                ledger = pair.baseline_ledger.detach()
    if before != _parameter_digest(comparator.head):
        raise FormalIntegrityError("formal ledger calibration mutated head weights")


def _emit_model_rows(
    *,
    endpoint: str,
    model: nn.Module,
    config: Any,
    episodes: Sequence[Any],
    condition: str,
    collector: TargetBlindRawCollector,
    retain_routes: bool,
) -> list[list[dict[str, Any]]]:
    labels = tuple(config.labels)
    route_rows: list[list[dict[str, Any]]] = []
    model.eval()
    for episode in episodes:
        model.reset_runtime()
        episode_routes: list[dict[str, Any]] = []
        for example in episode_examples(episode):
            pair = _paired_checked(model, example, condition=condition)
            baseline_probs = pair.baseline.probabilities.detach().cpu()
            cut_probs = pair.cut.probabilities.detach().cpu()
            baseline_label = labels[int(baseline_probs.argmax().item())]
            cut_label = labels[int(cut_probs.argmax().item())]
            collector.append(
                {
                    "endpoint": endpoint,
                    "world": episode.world_id,
                    "episode_seed": episode.seed,
                    "step_index": example.step_index,
                    "baseline_correct": int(baseline_label == example.belief_truth),
                    "cut_correct": int(cut_label == example.belief_truth),
                    "total_variation": 0.5
                    * float(torch.abs(baseline_probs - cut_probs).sum().item()),
                }
            )
            if retain_routes:
                episode_routes.append(
                    {
                        **_event_payload(example),
                        "truth": example.belief_truth,
                        "selected": list(pair.selected),
                        "route": pair.selected[0],
                    }
                )
        if retain_routes:
            route_rows.append(episode_routes)
    return route_rows


def _emit_fsa_rows(
    comparator: Any,
    route_rows: Sequence[Sequence[Mapping[str, Any]]],
    episodes: Sequence[Any],
    collector: TargetBlindRawCollector,
) -> None:
    for episode, episode_routes in zip(episodes, route_rows, strict=True):
        comparator.reset_episode()
        for row in episode_routes:
            pair = comparator.predict_pair(unperturbed_rank1_route=int(row["route"]))
            truth = str(row["truth"])
            collector.append(
                {
                    "endpoint": "FINITE_STATE_ROUTE_HISTORY_V2",
                    "world": episode.world_id,
                    "episode_seed": episode.seed,
                    "step_index": int(row["step_index"]),
                    "baseline_correct": int(pair.baseline == truth),
                    "cut_correct": int(pair.cut == truth),
                    "total_variation": None,
                }
            )


def _emit_ledger_rows(
    comparator: EligibilityRouteLedgerV2,
    route_rows: Sequence[Sequence[Mapping[str, Any]]],
    episodes: Sequence[Any],
    labels: tuple[str, ...],
    collector: TargetBlindRawCollector,
) -> None:
    with torch.no_grad():
        for episode, episode_routes in zip(episodes, route_rows, strict=True):
            ledger = comparator.initial_ledger(device=comparator.head.weight.device)
            for row in episode_routes:
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
                collector.append(
                    {
                        "endpoint": "ELIGIBILITY_ROUTE_LEDGER_V2",
                        "world": episode.world_id,
                        "episode_seed": episode.seed,
                        "step_index": int(row["step_index"]),
                        "baseline_correct": int(baseline_label == truth),
                        "cut_correct": int(cut_label == truth),
                        "total_variation": 0.5
                        * float(torch.abs(baseline_probs - cut_probs).sum().item()),
                    }
                )
                ledger = pair.baseline_ledger.detach()


def assert_started_marker(path: Path, binding: FutureIdentityBindingR2, actual_sha: str) -> None:
    marker = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "schema_version": 2,
        "identity_id": binding.identity_id,
        "state": "STARTED",
        "final_source_sha": actual_sha,
    }
    observed = {key: marker.get(key) for key in expected}
    if observed != expected:
        raise FormalIntegrityError("STARTED marker does not match exact H7 FORMAL-R2 identity")


def _assert_manifest_digest(path: Path, expected_sha256: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    recorded = str(value.get("manifest_sha256", ""))
    without_digest = {key: item for key, item in value.items() if key != "manifest_sha256"}
    actual = _sha256_bytes(_json_bytes(without_digest))
    if actual != recorded or recorded != expected_sha256:
        raise FormalIntegrityError(f"manifest binding mismatch: {path}")
    return value


def preidentity_preflight(root: Path) -> dict[str, Any]:
    r2_path = root / "artifacts" / "formal_h7_r2" / "contract.json"
    r1_path = root / "artifacts" / "formal_h7_r1" / "contract_design.json"
    r2, r1 = load_and_assert_r2_contract(r2_path, r1_path)
    plans = {role: episode_plan(role) for role in ("fit", "calibration", "evaluation")}
    expected_counts = {
        "fit": len(FIT_SEEDS),
        "calibration": len(CALIBRATION_SEEDS),
        "evaluation": len(EVALUATION_SEEDS),
    }
    observed_counts = {role: len(rows) for role, rows in plans.items()}
    if observed_counts != expected_counts:
        raise FormalIntegrityError("H7 FORMAL-R2 episode-plan count drift")
    splits = {role: sorted({row[2] for row in rows}) for role, rows in plans.items()}
    if splits != {"fit": ["train"], "calibration": ["dev"], "evaluation": ["test"]}:
        raise FormalIntegrityError("H7 FORMAL-R2 split binding drift")
    return {
        **preidentity_sentinel(r2, r1),
        "episode_counts": expected_counts,
        "splits": splits,
        "package_manifest": build_package_manifest(root),
    }


def run_result_bearing(
    *,
    root: Path,
    binding_path: Path,
    started_marker: Path,
    runtime_manifest_path: Path,
    package_manifest_path: Path,
    raw_path: Path,
    actual_sha: str,
) -> dict[str, Any]:
    configure_runtime()
    r2_path = root / "artifacts" / "formal_h7_r2" / "contract.json"
    r1_path = root / "artifacts" / "formal_h7_r1" / "contract_design.json"
    load_and_assert_r2_contract(r2_path, r1_path)
    binding = FutureIdentityBindingR2.from_mapping(
        json.loads(binding_path.read_text(encoding="utf-8"))
    )
    binding.assert_frozen_semantics()
    binding.assert_same_final_sha(actual_sha)
    assert_started_marker(started_marker, binding, actual_sha)
    runtime_manifest = _assert_manifest_digest(runtime_manifest_path, binding.runtime_manifest_sha256)
    package_manifest = _assert_manifest_digest(package_manifest_path, binding.package_manifest_sha256)
    if git_blob_sha(r2_path) != binding.contract_blob:
        raise FormalIntegrityError("H7 FORMAL-R2 contract Git-blob binding mismatch")
    runner_path = root / "scripts" / "run_h7_formal_r2.py"
    scorer_path = root / "src" / "sparkbrain" / "learned" / "h7_formal_r1.py"
    if git_blob_sha(runner_path) != binding.runner_blob:
        raise FormalIntegrityError("H7 FORMAL-R2 runner Git-blob binding mismatch")
    if git_blob_sha(scorer_path) != binding.scorer_blob or git_blob_sha(scorer_path) != binding.preserver_blob:
        raise FormalIntegrityError("H7 FORMAL-R2 scorer/preserver Git-blob binding mismatch")

    fit = materialize_episodes("fit")
    calibration = materialize_episodes("calibration")
    native_config = replace(native_development_config(), seed=NATIVE_TRAINING_SEED)
    dense_config = replace(dense_recurrent_comparator_config(), seed=DENSE_TRAINING_SEED)
    native, _ = train_model(native_config, fit)
    dense, _ = train_model(dense_config, fit)
    native_calibrated = calibrate_ignition(native_config, native, calibration)
    dense_calibrated = calibrate_ignition(dense_config, dense, calibration)

    fit_routes = _collect_route_rows(native, fit)
    calibration_routes = _collect_route_rows(native, calibration)
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
    configure_formal_eligibility_ledger(ledger)
    fit_formal_eligibility_ledger(ledger, _ledger_fit_rows(fit_routes, labels))
    _calibrate_ledger(ledger, calibration_routes)

    evaluation = materialize_episodes("evaluation")
    collector = TargetBlindRawCollector(raw_path, binding, actual_sha)
    evaluation_routes = _emit_model_rows(
        endpoint="native",
        model=native,
        config=native_calibrated,
        episodes=evaluation,
        condition="full",
        collector=collector,
        retain_routes=True,
    )
    _emit_model_rows(
        endpoint="ORDINARY_DENSE_RECURRENT_V1",
        model=dense,
        config=dense_calibrated,
        episodes=evaluation,
        condition="dense_recurrent",
        collector=collector,
        retain_routes=False,
    )
    _emit_fsa_rows(fsa, evaluation_routes, evaluation, collector)
    _emit_ledger_rows(ledger, evaluation_routes, evaluation, labels, collector)
    receipt = collector.close()
    return {
        "schema_version": 2,
        "identity_id": binding.identity_id,
        "final_source_sha": actual_sha,
        "raw_sha256": receipt["raw_sha256"],
        "raw_bytes": receipt["raw_bytes"],
        "target_blind": True,
        "decision_present": False,
        "runtime_manifest_sha256": runtime_manifest["manifest_sha256"],
        "package_manifest_sha256": package_manifest["manifest_sha256"],
        "raw_path": str(raw_path),
        "scoring_performed": False,
        "preserve_performed": False,
    }
