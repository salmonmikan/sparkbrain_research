from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from .h7_formal_r1 import (
    ENDPOINTS,
    EVALUATION_SEEDS,
    INTERVENTION_ID,
    STEPS_PER_EPISODE,
    WORLDS,
    FormalIntegrityError,
    create_only_json,
    score_rows,
    sha256_path,
)

RAW_REQUIRED_KEYS: Final = frozenset(
    {
        "opaque_target_id",
        "endpoint",
        "intervention_id",
        "baseline_prediction",
        "cut_prediction",
    }
)
RAW_OPTIONAL_KEYS: Final = frozenset(
    {"baseline_probabilities", "cut_probabilities"}
)
RAW_ALLOWED_KEYS: Final = RAW_REQUIRED_KEYS | RAW_OPTIONAL_KEYS
TARGET_SIDECAR_KEYS: Final = frozenset(
    {"opaque_target_id", "world", "episode_seed", "step_index", "truth"}
)
_HEX = frozenset("0123456789abcdef")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_bytes(payload)


def prediction_raw_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join(
        json.dumps(dict(row), sort_keys=True, separators=(",", ":")).encode("utf-8")
        + b"\n"
        for row in rows
    )


def _assert_opaque_id(value: Any) -> str:
    token = str(value)
    if len(token) != 64 or any(char not in _HEX for char in token):
        raise FormalIntegrityError("opaque target id must be a lowercase SHA-256 token")
    return token


def _validate_probability_vector(value: Any, *, field: str) -> tuple[float, ...]:
    if not isinstance(value, list | tuple) or not value:
        raise FormalIntegrityError(f"{field} must be a non-empty numeric vector")
    result: list[float] = []
    for item in value:
        if not isinstance(item, int | float) or not math.isfinite(float(item)):
            raise FormalIntegrityError(f"{field} contains a non-finite value")
        result.append(float(item))
    return tuple(result)


def validate_prediction_raw_row(row: Mapping[str, Any]) -> None:
    keys = set(row)
    if not RAW_REQUIRED_KEYS <= keys or not keys <= RAW_ALLOWED_KEYS:
        raise FormalIntegrityError(
            f"R3 prediction raw schema violation: {sorted(keys)!r}"
        )
    _assert_opaque_id(row["opaque_target_id"])
    if str(row["endpoint"]) not in ENDPOINTS:
        raise FormalIntegrityError("R3 prediction raw endpoint drift")
    if str(row["intervention_id"]) != INTERVENTION_ID:
        raise FormalIntegrityError("R3 prediction raw intervention drift")
    for key in ("baseline_prediction", "cut_prediction"):
        if not isinstance(row[key], str) or not row[key]:
            raise FormalIntegrityError(f"{key} must be a non-empty label")
    has_baseline = "baseline_probabilities" in row
    has_cut = "cut_probabilities" in row
    if has_baseline != has_cut:
        raise FormalIntegrityError("probability vectors must be present as a pair")
    if has_baseline:
        baseline = _validate_probability_vector(
            row["baseline_probabilities"], field="baseline_probabilities"
        )
        cut = _validate_probability_vector(
            row["cut_probabilities"], field="cut_probabilities"
        )
        if len(baseline) != len(cut):
            raise FormalIntegrityError("baseline/cut probability vector length drift")


def validate_target_sidecar_row(row: Mapping[str, Any]) -> None:
    if set(row) != TARGET_SIDECAR_KEYS:
        raise FormalIntegrityError("R3 protected target sidecar schema drift")
    _assert_opaque_id(row["opaque_target_id"])
    if str(row["world"]) not in WORLDS:
        raise FormalIntegrityError("R3 protected target world drift")
    seed = row["episode_seed"]
    step = row["step_index"]
    if not isinstance(seed, int):
        raise FormalIntegrityError("R3 protected episode seed must be an integer")
    if not isinstance(step, int) or not 0 <= step < STEPS_PER_EPISODE:
        raise FormalIntegrityError("R3 protected step index drift")
    if not isinstance(row["truth"], str) or not row["truth"]:
        raise FormalIntegrityError("R3 protected truth must be a non-empty label")


def assert_target_sidecar_independence(
    raw_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
) -> None:
    if not raw_rows or not target_rows:
        raise FormalIntegrityError("R3 raw and target sidecar must both be non-empty")
    for row in raw_rows:
        validate_prediction_raw_row(row)
    for row in target_rows:
        validate_target_sidecar_row(row)

    target_ids = [str(row["opaque_target_id"]) for row in target_rows]
    if len(target_ids) != len(set(target_ids)):
        raise FormalIntegrityError("R3 protected target sidecar contains duplicate ids")
    raw_pairs = [
        (str(row["opaque_target_id"]), str(row["endpoint"])) for row in raw_rows
    ]
    if len(raw_pairs) != len(set(raw_pairs)):
        raise FormalIntegrityError("R3 prediction raw contains duplicate target/endpoint rows")
    expected = {
        (target_id, endpoint) for target_id in target_ids for endpoint in ENDPOINTS
    }
    if set(raw_pairs) != expected:
        raise FormalIntegrityError("R3 prediction raw and protected target coverage mismatch")


@dataclass(frozen=True)
class PreserveProof:
    raw_sha256: str
    preserved_raw_sha256: str
    preserve_manifest_sha256: str
    preserve_before_target_access: bool

    def assert_valid_for(self, raw_payload: bytes) -> None:
        actual = _sha256_bytes(raw_payload)
        if actual != self.raw_sha256 or actual != self.preserved_raw_sha256:
            raise FormalIntegrityError("R3 preserved prediction raw hash mismatch")
        if len(self.preserve_manifest_sha256) != 64:
            raise FormalIntegrityError("R3 preserve manifest digest is incomplete")
        if not self.preserve_before_target_access:
            raise FormalIntegrityError("R3 target access occurred before raw preserve")


def recompute_correctness_after_preserve(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    preserve_proof: PreserveProof,
) -> list[dict[str, Any]]:
    raw_payload = prediction_raw_bytes(raw_rows)
    preserve_proof.assert_valid_for(raw_payload)
    assert_target_sidecar_independence(raw_rows, target_rows)
    targets = {str(row["opaque_target_id"]): row for row in target_rows}
    result: list[dict[str, Any]] = []
    for row in raw_rows:
        target = targets[str(row["opaque_target_id"])]
        truth = str(target["truth"])
        baseline = str(row["baseline_prediction"])
        cut = str(row["cut_prediction"])
        tv: float | None = None
        if "baseline_probabilities" in row:
            baseline_probs = _validate_probability_vector(
                row["baseline_probabilities"], field="baseline_probabilities"
            )
            cut_probs = _validate_probability_vector(
                row["cut_probabilities"], field="cut_probabilities"
            )
            tv = 0.5 * sum(
                abs(left - right)
                for left, right in zip(baseline_probs, cut_probs, strict=True)
            )
        result.append(
            {
                "endpoint": str(row["endpoint"]),
                "world": str(target["world"]),
                "episode_seed": int(target["episode_seed"]),
                "step_index": int(target["step_index"]),
                "baseline_correct": int(baseline == truth),
                "cut_correct": int(cut == truth),
                "total_variation": tv,
            }
        )
    return result


def adapt_fresh_episode_ids_to_frozen_scorer_surface(
    rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    episode_steps: dict[tuple[str, int], set[int]] = {}
    for row in rows:
        world = str(row["world"])
        seed = int(row["episode_seed"])
        step = int(row["step_index"])
        episode_steps.setdefault((world, seed), set()).add(step)
    expected_steps = set(range(STEPS_PER_EPISODE))
    for key, steps in episode_steps.items():
        if steps != expected_steps:
            raise FormalIntegrityError(f"R3 incomplete protected episode surface: {key!r}")

    by_world: dict[str, list[int]] = {
        world: sorted(seed for seen_world, seed in episode_steps if seen_world == world)
        for world in WORLDS
    }
    if any(len(seeds) != 64 for seeds in by_world.values()):
        raise FormalIntegrityError("R3 protected surface must contain 64 episodes per world")
    if sum(len(seeds) for seeds in by_world.values()) != 256:
        raise FormalIntegrityError("R3 protected surface must contain 256 episodes")

    mapping: dict[tuple[str, int], int] = {}
    for world_index, world in enumerate(WORLDS):
        surrogate = list(EVALUATION_SEEDS[world_index:: len(WORLDS)])
        for actual_seed, surrogate_seed in zip(by_world[world], surrogate, strict=True):
            mapping[(world, actual_seed)] = surrogate_seed

    adapted: list[dict[str, Any]] = []
    for row in rows:
        copy = dict(row)
        key = (str(copy["world"]), int(copy["episode_seed"]))
        copy["episode_seed"] = mapping[key]
        adapted.append(copy)
    return adapted


def score_post_preserve_rows(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    preserve_proof: PreserveProof,
) -> dict[str, Any]:
    recomputed = recompute_correctness_after_preserve(
        raw_rows=raw_rows,
        target_rows=target_rows,
        preserve_proof=preserve_proof,
    )
    adapted = adapt_fresh_episode_ids_to_frozen_scorer_surface(recomputed)
    return score_rows(adapted)


def preserve_prediction_raw_create_only(
    *,
    raw_path: Path,
    preserve_dir: Path,
) -> PreserveProof:
    if not raw_path.is_file():
        raise FormalIntegrityError("R3 prediction raw path missing")
    preserve_dir.mkdir(parents=True, exist_ok=True)
    preserved = preserve_dir / "prediction_raw.jsonl"
    if preserved.exists():
        raise FormalIntegrityError("R3 preserve raw no-clobber violation")
    with raw_path.open("rb") as source, preserved.open("xb") as target:
        shutil.copyfileobj(source, target)
        target.flush()
        os.fsync(target.fileno())
    raw_sha = sha256_path(raw_path)
    if sha256_path(preserved) != raw_sha:
        raise FormalIntegrityError("R3 preserve byte mismatch")
    manifest = preserve_dir / "preserve_manifest.json"
    create_only_json(
        manifest,
        {
            "schema_version": 2,
            "raw_sha256": raw_sha,
            "preserved_raw": preserved.name,
            "preserve_before_target_access": True,
        },
    )
    return PreserveProof(
        raw_sha256=raw_sha,
        preserved_raw_sha256=raw_sha,
        preserve_manifest_sha256=sha256_path(manifest),
        preserve_before_target_access=True,
    )


def assert_paths_available_no_clobber(paths: Sequence[Path]) -> None:
    collisions = [str(path) for path in paths if path.exists()]
    if collisions:
        raise FormalIntegrityError(f"R3 no-clobber path collision: {collisions!r}")


def validate_runtime_binding(
    binding: Mapping[str, Any], observation: Mapping[str, Any]
) -> None:
    if binding.get("schema_version") != 2:
        raise FormalIntegrityError("R3 runtime binding schema drift")
    if binding.get("binding_mode") != "LITERAL_EXACT_NO_NORMALIZATION":
        raise FormalIntegrityError("R3 runtime binding mode drift")
    expected = binding.get("runtime_observation")
    if not isinstance(expected, Mapping) or dict(expected) != dict(observation):
        raise FormalIntegrityError("R3 literal exact runtime binding mismatch")
    recorded = str(binding.get("runtime_observation_sha256", ""))
    if recorded != str(observation.get("runtime_observation_sha256", "")):
        raise FormalIntegrityError("R3 runtime observation digest mismatch")


def validate_prior_surface_inventory(value: Mapping[str, Any]) -> None:
    if value.get("schema_version") != 2:
        raise FormalIntegrityError("R3 prior-surface inventory schema drift")
    surfaces = value.get("h7_prior_episode_surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise FormalIntegrityError("R3 prior-surface inventory is empty")
    roles = Counter(str(item.get("role")) for item in surfaces if isinstance(item, Mapping))
    if roles != Counter({"fit": 1, "calibration": 1, "evaluation": 1}):
        raise FormalIntegrityError("R3 prior-surface inventory role drift")
    if value.get("future_r3_evaluation_seed_values_recorded") is not False:
        raise FormalIntegrityError("R3 inventory must not contain future evaluation seeds")
    without_digest = {
        key: item for key, item in value.items() if key != "inventory_sha256"
    }
    if value.get("inventory_sha256") != canonical_json_sha256(without_digest):
        raise FormalIntegrityError("R3 prior-surface inventory digest mismatch")
