"""Fresh-output construction runner for prospective RV01 R01-16.

This module is deliberately construction-only. It consumes retained pre/post
connection inventories, reconstructs the bound development-package identity,
builds the preregistered F0/FW/FD/FWD factorization and causal-reachability
certificate, and writes auditable artifacts into the package-derived output
path. It does not train a learner, run a probe, score capability, reveal held-
out data, or grant formal execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .rv01_r01_16_development_package import (
    R0116CollisionRegistry,
    R0116DevelopmentPackagePlan,
    R0116SourceManifest,
    R0116SourceManifestEntry,
)
from .rv01_r01_16_factorization import (
    R01_16_PROTOCOL_ID,
    ConnectionState,
    QueuedPropagationSnapshot,
    R01_16FactorizationConstruction,
)
from .rv01_r01_16_reachability import build_factor_reachability_certificate

_INPUT_KEYS = frozenset(
    {
        "source_manifest",
        "collision_registry",
        "package_plan_sha256",
        "registered_unit_ids",
        "cue_source_ids",
        "probe_horizon_ms",
        "pre_training",
        "post_training",
        "queued_propagation",
    }
)
_MANIFEST_KEYS = frozenset({"source_git_sha", "entries"})
_MANIFEST_ENTRY_KEYS = frozenset({"path", "sha256"})
_REGISTRY_KEYS = frozenset(
    {
        "registry_id",
        "source_paths",
        "consumed_or_reserved_seed_ids",
        "consumed_or_reserved_world_ids",
        "authoritative_complete",
    }
)
_CONNECTION_KEYS = frozenset(
    {"source_id", "target_id", "weight", "delay_ms", "plastic"}
)
_QUEUE_KEYS = frozenset(
    {"event_id", "source_id", "target_id", "queued_weight", "queued_delay_ms"}
)


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _require_hash(value: object, *, label: str, length: int) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if len(value) != length or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def _require_object(
    value: object,
    *,
    label: str,
    expected_keys: frozenset[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a JSON object")
    keys = frozenset(value)
    if keys != expected_keys:
        raise ValueError(
            f"{label} keys must exactly match {sorted(expected_keys)}; "
            f"got {sorted(keys)}"
        )
    return value


def _rows(value: object, *, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a JSON array")
    return value


def _string_tuple(value: object, *, label: str) -> tuple[str, ...]:
    rows = _rows(value, label=label)
    if any(not isinstance(row, str) for row in rows):
        raise TypeError(f"{label} must contain strings")
    return tuple(rows)


def _int_tuple(value: object, *, label: str) -> tuple[int, ...]:
    rows = _rows(value, label=label)
    if any(type(row) is not int for row in rows):
        raise TypeError(f"{label} must contain exact non-boolean integers")
    return tuple(rows)


def _source_manifest(value: object) -> R0116SourceManifest:
    row = _require_object(value, label="source_manifest", expected_keys=_MANIFEST_KEYS)
    entries = tuple(
        R0116SourceManifestEntry(
            path=str(
                _require_object(
                    entry,
                    label=f"source_manifest.entries[{index}]",
                    expected_keys=_MANIFEST_ENTRY_KEYS,
                )["path"]
            ),
            sha256=str(
                _require_object(
                    entry,
                    label=f"source_manifest.entries[{index}]",
                    expected_keys=_MANIFEST_ENTRY_KEYS,
                )["sha256"]
            ),
        )
        for index, entry in enumerate(_rows(row["entries"], label="source_manifest.entries"))
    )
    manifest = R0116SourceManifest(
        source_git_sha=str(row["source_git_sha"]),
        entries=entries,
    )
    manifest.validate()
    return manifest


def _collision_registry(value: object) -> R0116CollisionRegistry:
    row = _require_object(
        value,
        label="collision_registry",
        expected_keys=_REGISTRY_KEYS,
    )
    registry = R0116CollisionRegistry(
        registry_id=str(row["registry_id"]),
        source_paths=_string_tuple(row["source_paths"], label="source_paths"),
        consumed_or_reserved_seed_ids=_int_tuple(
            row["consumed_or_reserved_seed_ids"],
            label="consumed_or_reserved_seed_ids",
        ),
        consumed_or_reserved_world_ids=_string_tuple(
            row["consumed_or_reserved_world_ids"],
            label="consumed_or_reserved_world_ids",
        ),
        authoritative_complete=row["authoritative_complete"],
    )
    registry.validate()
    return registry


def _connection(value: object, *, label: str) -> ConnectionState:
    row = _require_object(value, label=label, expected_keys=_CONNECTION_KEYS)
    connection = ConnectionState(
        source_id=row["source_id"],
        target_id=row["target_id"],
        weight=row["weight"],
        delay_ms=row["delay_ms"],
        plastic=row["plastic"],
    )
    connection.validate()
    return connection


def _queued(value: object, *, label: str) -> QueuedPropagationSnapshot:
    row = _require_object(value, label=label, expected_keys=_QUEUE_KEYS)
    queued = QueuedPropagationSnapshot(
        event_id=row["event_id"],
        source_id=row["source_id"],
        target_id=row["target_id"],
        queued_weight=row["queued_weight"],
        queued_delay_ms=row["queued_delay_ms"],
    )
    queued.validate()
    return queued


def _load_construction(
    raw: bytes,
) -> tuple[
    R0116DevelopmentPackagePlan,
    R01_16FactorizationConstruction,
    tuple[int, ...],
    tuple[int, ...],
    float,
]:
    try:
        decoded = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("R01-16 construction input must be valid UTF-8 JSON") from exc
    payload = _require_object(
        decoded,
        label="construction input",
        expected_keys=_INPUT_KEYS,
    )
    plan = R0116DevelopmentPackagePlan(
        source_manifest=_source_manifest(payload["source_manifest"]),
        collision_registry=_collision_registry(payload["collision_registry"]),
    )
    plan.validate()
    expected_plan_sha = _require_hash(
        payload["package_plan_sha256"],
        label="package_plan_sha256",
        length=64,
    )
    if plan.package_plan_sha256 != expected_plan_sha:
        raise ValueError("R01-16 package plan digest does not match reconstructed plan")

    pre_training = tuple(
        _connection(row, label=f"pre_training[{index}]")
        for index, row in enumerate(_rows(payload["pre_training"], label="pre_training"))
    )
    post_training = tuple(
        _connection(row, label=f"post_training[{index}]")
        for index, row in enumerate(_rows(payload["post_training"], label="post_training"))
    )
    queued = tuple(
        _queued(row, label=f"queued_propagation[{index}]")
        for index, row in enumerate(
            _rows(payload["queued_propagation"], label="queued_propagation")
        )
    )
    registered_unit_ids = _int_tuple(
        payload["registered_unit_ids"],
        label="registered_unit_ids",
    )
    cue_source_ids = _int_tuple(payload["cue_source_ids"], label="cue_source_ids")
    probe_horizon = payload["probe_horizon_ms"]
    if isinstance(probe_horizon, bool) or not isinstance(probe_horizon, int | float):
        raise TypeError("probe_horizon_ms must be a real numeric value")

    return (
        plan,
        R01_16FactorizationConstruction(
            pre_training=pre_training,
            post_training=post_training,
            queued_propagation=queued,
        ),
        registered_unit_ids,
        cue_source_ids,
        float(probe_horizon),
    )


def _write_json(path: Path, value: object) -> None:
    path.write_bytes(_canonical_json(value))


def run_construction(*, input_path: Path, repo_root: Path) -> Path:
    """Run one package-bound construction into its deterministic fresh path."""

    # Read and validate the identity before consuming the deterministic output
    # path. Unreadable/unparseable input therefore cannot leave an empty run ID.
    raw = input_path.read_bytes()
    input_sha256 = _sha256_bytes(raw)
    plan, construction, registered_ids, cue_ids, horizon = _load_construction(raw)
    output_dir = repo_root / plan.output_relpath
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "construction_input.json").write_bytes(raw)
    _write_json(
        output_dir / "input_identity.json",
        {
            "construction_input_sha256": input_sha256,
            "package_plan_sha256": plan.package_plan_sha256,
            "output_relpath": plan.output_relpath,
        },
    )

    try:
        summary = construction.require_any_prospective_contrast()
        certificate = build_factor_reachability_certificate(
            construction,
            registered_unit_ids=registered_ids,
            cue_source_ids=cue_ids,
            probe_horizon_ms=horizon,
        )
        runtime = {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "runner_module": "sparkbrain.research.rv01_r01_16_construction",
            "protocol_id": R01_16_PROTOCOL_ID,
        }
        _write_json(output_dir / "runtime.json", runtime)
        _write_json(
            output_dir / "source_binding.json",
            {
                "source_git_sha": plan.source_manifest.source_git_sha,
                "source_manifest_sha256": plan.source_manifest.manifest_sha256,
                "collision_registry_sha256": plan.collision_registry.registry_sha256,
                "package_plan_sha256": plan.package_plan_sha256,
                "output_relpath": plan.output_relpath,
            },
        )
        summary_state = asdict(summary)
        _write_json(output_dir / "construction_summary.json", summary_state)
        certificate_state = certificate.state_dict()
        _write_json(output_dir / "reachability_certificate.json", certificate_state)

        arms_dir = output_dir / "arms"
        arms_dir.mkdir(exist_ok=False)
        for arm in ("F0", "FW", "FD", "FWD"):
            _write_json(
                arms_dir / f"{arm}.json",
                [row.state_dict() for row in construction.arm_inventory(arm)],
            )

        _write_json(
            output_dir / "COMPLETE.json",
            {
                "status": "CONSTRUCTION_COMPLETE_REACHABILITY_BOUND_CAPABILITY_UNOPENED",
                "construction_input_sha256": input_sha256,
                "construction_summary_sha256": _sha256_bytes(
                    _canonical_json(summary_state)
                ),
                "reachability_certificate_sha256": certificate.sha256,
                "weight_eligible": certificate.weight_eligible,
                "delay_eligible": certificate.delay_eligible,
                "combined_eligible": certificate.combined_eligible,
                "capability_output_opened": False,
                "learner_or_probe_executed": False,
                "formal_execution_allowed": False,
            },
        )
    except Exception as exc:
        _write_json(
            output_dir / "FAILED.json",
            {
                "status": "CONSTRUCTION_FAILED_TERMINAL_FOR_THIS_OUTPUT_IDENTITY",
                "construction_input_sha256": input_sha256,
                "package_plan_sha256": plan.package_plan_sha256,
                "output_relpath": plan.output_relpath,
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "retry_same_output_identity_allowed": False,
            },
        )
        raise

    return output_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build package-bound R01-16 construction evidence only."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    run_construction(input_path=args.input, repo_root=args.repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "run_construction"]
