from __future__ import annotations

import hashlib
import json
import math
import os
import random
import shutil
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CONTRACT_ID = "H7-FORMAL-R1-DYNAMIC-TOP1-CONFIRMATORY-CONTRACT-DESIGN-V1"
EVALUATOR_ID = "H7-FORMAL-R1-EVALUATOR-SPEC-V1"
INTERVENTION_ID = "TOP1_SELECTED_LOCAL_NODE_CUT_V1"
WORLDS = (
    "switchworld",
    "contradiction_world",
    "goal_conflict_world",
    "multi_object_world",
)
ENDPOINTS = (
    "native",
    "ORDINARY_DENSE_RECURRENT_V1",
    "FINITE_STATE_ROUTE_HISTORY_V2",
    "ELIGIBILITY_ROUTE_LEDGER_V2",
)
COMPARATORS = ENDPOINTS[1:]
STEPS_PER_EPISODE = 24
EVALUATION_SEEDS = tuple(range(8_846_030, 8_846_286))
BOOTSTRAP_RESAMPLES = 50_000
BOOTSTRAP_SEED = 8_885_678
SIMULTANEOUS_CONFIDENCE = 0.99375
CAPACITY_MARGIN = 0.0
EFFECT_MARGIN = 0.0
EXPECTED_CONTRACT_BLOB = "af26de3067263afcff0e727321fa173ea14de659"
EXPECTED_EVALUATOR_SHA256 = "10cb6e725954636ca9d32f6395e549af50d79ab4dc0b7bb2f063b1ecc4b24430"
EXPECTED_INPUT_SURFACE_SHA256 = "bbba6f0cf413e33b66b22c753916ab4db7d59e716bd0b840703a68b7ac3f0be6"


class FormalIntegrityError(RuntimeError):
    """Fail-closed integrity violation in the H7 FORMAL-R1 one-way path."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def create_only_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise FormalIntegrityError(f"no-clobber violation: {path}") from exc


def create_only_json(path: Path, value: Any) -> None:
    create_only_bytes(path, json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def assert_contract_design(contract: Mapping[str, Any]) -> None:
    if contract.get("schema_version") != 2 or contract.get("contract_id") != CONTRACT_ID:
        raise FormalIntegrityError("contract identity drift")
    evaluator = contract.get("evaluator", {})
    input_surface = contract.get("input_surface", {})
    binding = contract.get("source_protocol_package_binding", {})
    runtime = contract.get("runtime_contract", {})
    expected = {
        "evaluator_id": EVALUATOR_ID,
        "evaluator_sha": EXPECTED_EVALUATOR_SHA256,
        "input_sha": EXPECTED_INPUT_SURFACE_SHA256,
        "intervention": INTERVENTION_ID,
        "worlds": list(WORLDS),
        "steps": STEPS_PER_EPISODE,
        "eval_range": [EVALUATION_SEEDS[0], EVALUATION_SEEDS[-1]],
        "panel": list(COMPARATORS),
        "python": "3.11",
        "torch": "2.13.0",
        "device": "cpu",
        "threads": 1,
    }
    observed = {
        "evaluator_id": evaluator.get("id"),
        "evaluator_sha": evaluator.get("evaluator_spec_sha256"),
        "input_sha": input_surface.get("input_surface_sha256"),
        "intervention": binding.get("intervention"),
        "worlds": input_surface.get("worlds"),
        "steps": input_surface.get("steps_per_episode"),
        "eval_range": input_surface.get("formal_evaluation_seed_range_inclusive"),
        "panel": binding.get("ordinary_reduction_panel"),
        "python": runtime.get("python_major_minor"),
        "torch": runtime.get("torch_version"),
        "device": runtime.get("device"),
        "threads": runtime.get("cpu_threads"),
    }
    if observed != expected:
        raise FormalIntegrityError(f"frozen contract drift: {observed!r}")
    uncertainty = evaluator.get("uncertainty", {})
    if uncertainty.get("resamples") != BOOTSTRAP_RESAMPLES:
        raise FormalIntegrityError("bootstrap count drift")
    if uncertainty.get("bootstrap_seed") != BOOTSTRAP_SEED:
        raise FormalIntegrityError("bootstrap seed drift")
    if uncertainty.get("per_contrast_two_sided_confidence") != SIMULTANEOUS_CONFIDENCE:
        raise FormalIntegrityError("simultaneous confidence drift")
    criteria = contract.get("independent_capacity_and_effect_criteria", {})
    if criteria.get("capacity_noninferiority_margin_accuracy") != CAPACITY_MARGIN:
        raise FormalIntegrityError("capacity margin drift")
    if criteria.get("effect_reproduction_margin_delta_accuracy") != EFFECT_MARGIN:
        raise FormalIntegrityError("effect margin drift")


@dataclass(frozen=True)
class FutureIdentityBinding:
    identity_id: str
    final_source_sha: str
    contract_blob: str
    runner_blob: str
    scorer_blob: str
    preserver_blob: str
    package_manifest_sha256: str
    runtime_manifest_sha256: str
    input_surface_sha256: str
    evaluator_spec_sha256: str
    intervention_id: str
    comparators: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> FutureIdentityBinding:
        return cls(
            identity_id=str(value["identity_id"]),
            final_source_sha=str(value["final_source_sha"]),
            contract_blob=str(value["contract_blob"]),
            runner_blob=str(value["runner_blob"]),
            scorer_blob=str(value["scorer_blob"]),
            preserver_blob=str(value["preserver_blob"]),
            package_manifest_sha256=str(value["package_manifest_sha256"]),
            runtime_manifest_sha256=str(value["runtime_manifest_sha256"]),
            input_surface_sha256=str(value["input_surface_sha256"]),
            evaluator_spec_sha256=str(value["evaluator_spec_sha256"]),
            intervention_id=str(value["intervention_id"]),
            comparators=tuple(str(item) for item in value["comparators"]),
        )

    def assert_frozen_semantics(self) -> None:
        if len(self.final_source_sha) != 40:
            raise FormalIntegrityError("final source SHA must be an exact Git SHA")
        if self.contract_blob != EXPECTED_CONTRACT_BLOB:
            raise FormalIntegrityError("contract blob mismatch")
        if self.input_surface_sha256 != EXPECTED_INPUT_SURFACE_SHA256:
            raise FormalIntegrityError("input surface mismatch")
        if self.evaluator_spec_sha256 != EXPECTED_EVALUATOR_SHA256:
            raise FormalIntegrityError("evaluator mismatch")
        if self.intervention_id != INTERVENTION_ID:
            raise FormalIntegrityError("intervention mismatch")
        if self.comparators != COMPARATORS:
            raise FormalIntegrityError("ordinary comparator panel mismatch")
        required_digests = (
            self.runner_blob,
            self.scorer_blob,
            self.preserver_blob,
            self.package_manifest_sha256,
            self.runtime_manifest_sha256,
        )
        if any(len(value) < 40 for value in required_digests):
            raise FormalIntegrityError("incomplete implementation/runtime binding")

    def assert_same_final_sha(self, actual_sha: str) -> None:
        if actual_sha != self.final_source_sha:
            raise FormalIntegrityError(
                f"same-final-SHA gate failed: expected {self.final_source_sha}, got {actual_sha}"
            )


def create_started_marker(path: Path, binding: FutureIdentityBinding, actual_sha: str) -> None:
    """Future capability: create STARTED exactly once after identity authority exists."""
    binding.assert_frozen_semantics()
    binding.assert_same_final_sha(actual_sha)
    create_only_json(
        path,
        {
            "schema_version": 2,
            "identity_id": binding.identity_id,
            "state": "STARTED",
            "final_source_sha": actual_sha,
            "binding_sha256": canonical_json_sha256(binding.__dict__),
        },
    )


_FORBIDDEN_RAW_KEYS = {
    "decision",
    "disposition",
    "pass",
    "fail",
    "inconclusive",
    "falsifier",
    "score",
    "scored",
}


def _assert_target_blind(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if str(key).lower() in _FORBIDDEN_RAW_KEYS:
                raise FormalIntegrityError(f"raw artifact contains scorer field: {key}")
            _assert_target_blind(nested)
    elif isinstance(value, list | tuple):
        for nested in value:
            _assert_target_blind(nested)


class TargetBlindRawCollector:
    """Create-only JSONL collector. It cannot compute or store a decision token."""

    def __init__(self, path: Path, binding: FutureIdentityBinding, actual_sha: str) -> None:
        binding.assert_frozen_semantics()
        binding.assert_same_final_sha(actual_sha)
        self.path = path
        self.binding = binding
        self._handle = None
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._handle = path.open("x", encoding="utf-8")
        except FileExistsError as exc:
            raise FormalIntegrityError(f"raw no-clobber violation: {path}") from exc

    def append(self, row: Mapping[str, Any]) -> None:
        if self._handle is None:
            raise FormalIntegrityError("raw collector already closed")
        _assert_target_blind(row)
        self._handle.write(json.dumps(dict(row), sort_keys=True, separators=(",", ":")) + "\n")

    def close(self) -> dict[str, Any]:
        if self._handle is None:
            raise FormalIntegrityError("raw collector already closed")
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self._handle.close()
        self._handle = None
        return {
            "identity_id": self.binding.identity_id,
            "raw_sha256": sha256_path(self.path),
            "raw_bytes": self.path.stat().st_size,
            "target_blind": True,
            "decision_present": False,
        }


@dataclass(frozen=True)
class PreserveReceipt:
    identity_id: str
    raw_sha256: str
    preserved_raw: str
    preserve_manifest: str
    preserve_manifest_sha256: str


def preserve_raw_create_only(
    *,
    raw_path: Path,
    preserve_dir: Path,
    binding: FutureIdentityBinding,
    actual_sha: str,
) -> PreserveReceipt:
    """Copy exact closed raw bytes into a create-only preserve surface before any scorer read."""
    binding.assert_frozen_semantics()
    binding.assert_same_final_sha(actual_sha)
    if not raw_path.is_file():
        raise FormalIntegrityError("raw path missing")
    preserve_dir.mkdir(parents=True, exist_ok=True)
    preserved = preserve_dir / "raw.jsonl"
    if preserved.exists():
        raise FormalIntegrityError("preserve raw no-clobber violation")
    with raw_path.open("rb") as source, preserved.open("xb") as target:
        shutil.copyfileobj(source, target)
        target.flush()
        os.fsync(target.fileno())
    raw_sha = sha256_path(raw_path)
    if sha256_path(preserved) != raw_sha:
        raise FormalIntegrityError("preserve byte mismatch")
    manifest = preserve_dir / "preserve_manifest.json"
    manifest_value = {
        "schema_version": 2,
        "identity_id": binding.identity_id,
        "final_source_sha": actual_sha,
        "raw_sha256": raw_sha,
        "preserved_raw": preserved.name,
        "preserve_before_read": True,
    }
    create_only_json(manifest, manifest_value)
    return PreserveReceipt(
        identity_id=binding.identity_id,
        raw_sha256=raw_sha,
        preserved_raw=str(preserved),
        preserve_manifest=str(manifest),
        preserve_manifest_sha256=sha256_path(manifest),
    )


def _percentile_linear(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        raise FormalIntegrityError("cannot compute percentile of empty sample")
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def _ci(values: list[float]) -> tuple[float, float]:
    ordered = sorted(values)
    tail = (1.0 - SIMULTANEOUS_CONFIDENCE) / 2.0
    return _percentile_linear(ordered, tail), _percentile_linear(ordered, 1.0 - tail)


def _mean(values: Iterable[float]) -> float:
    materialized = list(values)
    if not materialized:
        raise FormalIntegrityError("empty mean")
    return sum(materialized) / len(materialized)


def _validate_and_index_rows(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, dict[int, list[dict[str, Any]]]]]:
    indexed: dict[str, dict[str, dict[int, list[dict[str, Any]]]]] = {
        endpoint: {world: {} for world in WORLDS} for endpoint in ENDPOINTS
    }
    expected_seed_set = set(EVALUATION_SEEDS)
    for row in rows:
        endpoint = str(row.get("endpoint"))
        world = str(row.get("world"))
        seed = int(row.get("episode_seed"))
        step = int(row.get("step_index"))
        if endpoint not in indexed or world not in WORLDS or seed not in expected_seed_set:
            raise FormalIntegrityError("raw row outside frozen endpoint/world/seed surface")
        expected_world = WORLDS[(seed - EVALUATION_SEEDS[0]) % len(WORLDS)]
        if world != expected_world:
            raise FormalIntegrityError("world assignment drift")
        if not 0 <= step < STEPS_PER_EPISODE:
            raise FormalIntegrityError("step index drift")
        for key in ("baseline_correct", "cut_correct"):
            if row.get(key) not in (0, 1, False, True):
                raise FormalIntegrityError(f"invalid {key}")
        tv = row.get("total_variation")
        if tv is not None and (not isinstance(tv, int | float) or not math.isfinite(float(tv))):
            raise FormalIntegrityError("nonfinite total variation")
        indexed[endpoint][world].setdefault(seed, []).append(row)
    for endpoint in ENDPOINTS:
        for world_index, world in enumerate(WORLDS):
            expected = set(EVALUATION_SEEDS[world_index:: len(WORLDS)])
            if set(indexed[endpoint][world]) != expected:
                raise FormalIntegrityError(f"incomplete evaluation seeds for {endpoint}/{world}")
            for seed, episode_rows in indexed[endpoint][world].items():
                steps = sorted(int(row["step_index"]) for row in episode_rows)
                if steps != list(range(STEPS_PER_EPISODE)):
                    raise FormalIntegrityError(f"incomplete/duplicate steps for {endpoint}/{seed}")
    return indexed


def _episode_metrics(rows: list[dict[str, Any]]) -> tuple[float, float, float]:
    baseline = _mean(float(bool(row["baseline_correct"])) for row in rows)
    cut = _mean(float(bool(row["cut_correct"])) for row in rows)
    tv_values = [
        float(row["total_variation"])
        for row in rows
        if row.get("total_variation") is not None
    ]
    tv = _mean(tv_values) if tv_values else math.nan
    return baseline, baseline - cut, tv


def _contrast_vector(
    indexed: dict[str, dict[str, dict[int, list[dict[str, Any]]]]],
    sampled_seeds: Mapping[str, list[int]],
) -> dict[str, float]:
    endpoint_metrics: dict[str, dict[str, tuple[float, float, float]]] = {}
    for endpoint in ENDPOINTS:
        endpoint_metrics[endpoint] = {}
        for world in WORLDS:
            episode_values = [
                _episode_metrics(indexed[endpoint][world][seed])
                for seed in sampled_seeds[world]
            ]
            endpoint_metrics[endpoint][world] = tuple(
                _mean(value[index] for value in episode_values) for index in range(3)
            )

    def equal_world(endpoint: str, index: int) -> float:
        return _mean(endpoint_metrics[endpoint][world][index] for world in WORLDS)

    native_baseline = equal_world("native", 0)
    native_delta = equal_world("native", 1)
    values = {
        "native_baseline_accuracy_minus_one_third": native_baseline - (1.0 / 3.0),
        "native_delta_accuracy": native_delta,
        "native_mean_total_variation": equal_world("native", 2),
    }
    for endpoint in COMPARATORS:
        slug = {
            "ORDINARY_DENSE_RECURRENT_V1": "dense",
            "FINITE_STATE_ROUTE_HISTORY_V2": "fsa",
            "ELIGIBILITY_ROUTE_LEDGER_V2": "eligibility",
        }[endpoint]
        values[f"{slug}_baseline_accuracy_minus_native_baseline_accuracy"] = (
            equal_world(endpoint, 0) - native_baseline
        )
        values[f"{slug}_delta_accuracy_minus_native_delta_accuracy"] = (
            equal_world(endpoint, 1) - native_delta
        )
    return values


def score_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Frozen evaluator. Intended for preserved raw only; no file IO occurs here."""
    indexed = _validate_and_index_rows(rows)
    observed_seeds = {
        world: list(EVALUATION_SEEDS[index:: len(WORLDS)]) for index, world in enumerate(WORLDS)
    }
    point = _contrast_vector(indexed, observed_seeds)
    rng = random.Random(BOOTSTRAP_SEED)
    bootstrap: dict[str, list[float]] = {key: [] for key in point}
    for _ in range(BOOTSTRAP_RESAMPLES):
        sampled = {
            world: [rng.choice(seeds) for _ in range(len(seeds))]
            for world, seeds in observed_seeds.items()
        }
        values = _contrast_vector(indexed, sampled)
        for key, value in values.items():
            bootstrap[key].append(value)
    intervals = {key: _ci(values) for key, values in bootstrap.items()}
    positive_ci = intervals["native_baseline_accuracy_minus_one_third"]
    native_effect_ci = intervals["native_delta_accuracy"]
    capacity: dict[str, bool] = {}
    reproduced: dict[str, bool] = {}
    conclusively_smaller: dict[str, bool] = {}
    for slug in ("dense", "fsa", "eligibility"):
        capacity_ci = intervals[f"{slug}_baseline_accuracy_minus_native_baseline_accuracy"]
        effect_ci = intervals[f"{slug}_delta_accuracy_minus_native_delta_accuracy"]
        capacity[slug] = capacity_ci[0] >= CAPACITY_MARGIN
        reproduced[slug] = capacity[slug] and effect_ci[0] >= EFFECT_MARGIN
        conclusively_smaller[slug] = capacity[slug] and effect_ci[1] < EFFECT_MARGIN

    if positive_ci[1] <= 0.0:
        decision = "FAIL_NO_POSITIVE_PHENOMENON"
    elif native_effect_ci[1] <= 0.0:
        decision = "FAIL_NO_NATIVE_LOCAL_EFFECT"
    elif any(reproduced.values()):
        decision = "FAIL_REDUCED_BY_ORDINARY_COMPARATOR"
    elif positive_ci[0] > 0.0 and native_effect_ci[0] > 0.0 and all(conclusively_smaller.values()):
        decision = "PASS_LOCAL_DYNAMIC_POLICY_MECHANISTIC_DISTINCTNESS"
    else:
        decision = "INCONCLUSIVE"
    return {
        "schema_version": 2,
        "contract_id": CONTRACT_ID,
        "evaluator_id": EVALUATOR_ID,
        "point_estimates": point,
        "simultaneous_intervals": {key: list(value) for key, value in intervals.items()},
        "capacity_adequate": capacity,
        "effect_reproduced": reproduced,
        "effect_conclusively_smaller": conclusively_smaller,
        "decision": decision,
        "bootstrap": {
            "method": "paired_stratified_cluster_bootstrap_percentile",
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed": BOOTSTRAP_SEED,
            "confidence": SIMULTANEOUS_CONFIDENCE,
            "percentile_interpolation": "linear_type7",
            "rng": "python_random_mt19937",
        },
    }


def score_preserved_raw_once(
    *,
    receipt: PreserveReceipt,
    output_path: Path,
    consumed_marker: Path,
) -> dict[str, Any]:
    """Read only preserved raw, consume scorer capability once, and create score output once."""
    preserved = Path(receipt.preserved_raw)
    manifest = Path(receipt.preserve_manifest)
    if not preserved.is_file() or not manifest.is_file():
        raise FormalIntegrityError("preserve receipt points to missing material")
    if sha256_path(preserved) != receipt.raw_sha256:
        raise FormalIntegrityError("preserved raw hash mismatch")
    if sha256_path(manifest) != receipt.preserve_manifest_sha256:
        raise FormalIntegrityError("preserve manifest hash mismatch")
    create_only_json(
        consumed_marker,
        {
            "schema_version": 2,
            "identity_id": receipt.identity_id,
            "state": "SCORER_CONSUMED",
            "raw_sha256": receipt.raw_sha256,
        },
    )
    rows = [json.loads(line) for line in preserved.read_text(encoding="utf-8").splitlines() if line]
    result = score_rows(rows)
    result["identity_id"] = receipt.identity_id
    result["raw_sha256"] = receipt.raw_sha256
    result["preserve_manifest_sha256"] = receipt.preserve_manifest_sha256
    create_only_json(output_path, result)
    return result


def preflight_sentinel() -> dict[str, Any]:
    """Outcome-blind capability check; never materializes H7 evaluation seeds or a decision."""
    sentinel = {
        "endpoint": "SENTINEL_NOT_SCIENTIFIC",
        "world": "SENTINEL",
        "episode_seed": -1,
        "step_index": -1,
        "baseline_correct": 0,
        "cut_correct": 0,
        "total_variation": 0.0,
    }
    _assert_target_blind(sentinel)
    return {
        "contract_id": CONTRACT_ID,
        "evaluator_id": EVALUATOR_ID,
        "intervention_id": INTERVENTION_ID,
        "target_blind_guard": "PASS",
        "no_identity_created": True,
        "no_started_created": True,
        "no_protected_evaluation_access": True,
        "no_official_raw_created": True,
        "no_scoring_performed": True,
        "sentinel_sha256": canonical_json_sha256(sentinel),
    }
