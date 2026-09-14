"""Exact package binding for the prospective RV01 R01-16 capability stage.

This module is development-only. It binds the already-preserved construction
census to the frozen capability source/runtime and extracts only the retained
per-cell reachability identities required by the preregistered capability
runner. It grants no held-out or formal authority.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .rv01_r01_16_capability import run_development_capability_suite
from .rv01_r01_16_development_package import (
    R0116SourceManifest,
    R0116SourceManifestEntry,
)
from .rv01_r01_16_source_binding import verify_r01_16_source_checkout
from .rv01_r01_16_worlds import development_world_grid, development_world_grid_hash

R01_16_CONSTRUCTION_PRESERVE_REF = (
    "preserve/rv01-r01-16-construction-census-34881254582"
)
R01_16_CONSTRUCTION_CENSUS_RELPATH = (
    "artifacts/rv01/r01-16/development/"
    "rv01-r01-16-development-7ed3a7532fc66ac8-87634d034204/"
    "construction_census.json"
)
R01_16_CONSTRUCTION_CENSUS_SHA256 = (
    "7761c1f76485034fd2b6776413dfb95472f65c4ee29636f72ef661c62f456cb2"
)
R01_16_CAPABILITY_FREEZE_REF = "freeze/rv01-r01-16-capability-source-20260915"
R01_16_CAPABILITY_CONTROL_REF = (
    "control/rv01-r01-16-capability-started-7761c1f7-20260915"
)
R01_16_CAPABILITY_PRESERVE_REF = "preserve/rv01-r01-16-capability-20260915"
R01_16_CAPABILITY_PYTHON_IMPLEMENTATION = "CPython"
R01_16_CAPABILITY_PYTHON_VERSION = "3.11.16"
R01_16_CAPABILITY_OUTPUT_ROOT = Path("artifacts/rv01/r01-16/capability")
R01_16_CAPABILITY_CONTROL_ROOT = Path("artifacts/rv01/r01-16/capability/_control")
R01_16_CAPABILITY_REQUIRED_SOURCE_PATHS = frozenset(
    {
        "src/sparkbrain/research/rv01_r01_16_capability.py",
        "src/sparkbrain/research/rv01_r01_16_capability_package.py",
        "docs/research/RV01_R01_16_CAPABILITY_EXECUTION_AMENDMENT_002.md",
        "docs/research/RV01_R01_16_CAPABILITY_FINAL_REVIEW.md",
        "scripts/run_rv01_r01_16_capability.py",
        ".github/workflows/rv01-r01-16-capability-execute-once.yml",
    }
)

ControlMode = Literal["distributed-github", "local-offline"]


def _canonical_sha256(value: object) -> str:
    raw = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_source_manifest(path: Path) -> R0116SourceManifest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("R01-16 capability source manifest must be an object")
    raw_entries = payload.get("entries")
    if not isinstance(raw_entries, list):
        raise TypeError("R01-16 capability source manifest entries must be a list")
    manifest = R0116SourceManifest(
        source_git_sha=str(payload.get("source_git_sha", "")),
        entries=tuple(
            R0116SourceManifestEntry(
                path=str(row["path"]),
                sha256=str(row["sha256"]),
            )
            for row in raw_entries
            if isinstance(row, dict)
        ),
    )
    manifest.validate()
    paths = {row.path for row in manifest.entries}
    missing = sorted(R01_16_CAPABILITY_REQUIRED_SOURCE_PATHS.difference(paths))
    if missing:
        raise ValueError(
            f"R01-16 capability manifest is missing required paths: {missing}"
        )
    return manifest


def verify_bound_runtime() -> None:
    implementation = platform.python_implementation()
    version = platform.python_version()
    if implementation != R01_16_CAPABILITY_PYTHON_IMPLEMENTATION:
        raise RuntimeError(
            "R01-16 capability Python implementation mismatch: "
            f"{implementation!r}"
        )
    if version != R01_16_CAPABILITY_PYTHON_VERSION:
        raise RuntimeError(
            f"R01-16 capability Python version mismatch: {version!r}"
        )


@dataclass(frozen=True, slots=True)
class R0116RetainedCapabilityBinding:
    construction_census_sha256: str
    construction_world_grid_sha256: str
    retained_reachability_sha256: dict[str, dict[str, str]]
    retained_learner_api_hash: dict[str, str]

    def state_dict(self) -> dict[str, object]:
        return {
            "construction_preserve_ref": R01_16_CONSTRUCTION_PRESERVE_REF,
            "construction_census_relpath": R01_16_CONSTRUCTION_CENSUS_RELPATH,
            "construction_census_sha256": self.construction_census_sha256,
            "construction_world_grid_sha256": self.construction_world_grid_sha256,
            "retained_reachability_sha256": {
                world_id: dict(sorted(routes.items()))
                for world_id, routes in sorted(
                    self.retained_reachability_sha256.items()
                )
            },
            "retained_learner_api_hash": dict(
                sorted(self.retained_learner_api_hash.items())
            ),
        }

    @property
    def binding_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


def load_retained_capability_binding(path: Path) -> R0116RetainedCapabilityBinding:
    raw = path.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != R01_16_CONSTRUCTION_CENSUS_SHA256:
        raise RuntimeError(
            "R01-16 construction census digest mismatch: "
            f"expected {R01_16_CONSTRUCTION_CENSUS_SHA256}, got {actual_sha}"
        )
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise TypeError("R01-16 construction census must be an object")
    required = {
        "schema": "rv01-r01-16-construction-census-v1",
        "status": "CONSTRUCTION_CENSUS_COMPLETE_CAPABILITY_UNOPENED",
        "capability_output_opened": False,
        "probe_executed": False,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
        "same_identity_rerun_allowed": False,
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise RuntimeError(
                f"R01-16 retained census mismatch for {key}: "
                f"{payload.get(key)!r} != {expected!r}"
            )
    expected_grid_hash = development_world_grid_hash()
    if payload.get("world_grid_sha256") != expected_grid_hash:
        raise RuntimeError("R01-16 retained world-grid hash drifted")

    current_worlds = {world.world_id: world for world in development_world_grid()}
    raw_worlds = payload.get("worlds")
    if not isinstance(raw_worlds, list):
        raise TypeError("R01-16 retained census worlds must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    for row in raw_worlds:
        if not isinstance(row, dict) or not isinstance(row.get("world"), dict):
            raise TypeError("R01-16 retained world record is malformed")
        world_id = str(row["world"]["world_id"])
        if world_id in by_id:
            raise RuntimeError(f"duplicate retained R01-16 world identity: {world_id}")
        by_id[world_id] = row
    if set(by_id) != set(current_worlds):
        raise RuntimeError("R01-16 retained/current development world identities differ")

    reachability: dict[str, dict[str, str]] = {}
    learner_hashes: dict[str, str] = {}
    for world_id, world in current_worlds.items():
        row = by_id[world_id]
        if row.get("world_specification_sha256") != world.specification_hash():
            raise RuntimeError(
                f"R01-16 retained world specification drifted for {world_id}"
            )
        learner_hash = str(row.get("learner_api_hash", ""))
        if len(learner_hash) != 64 or any(
            char not in "0123456789abcdef" for char in learner_hash
        ):
            raise RuntimeError(
                f"R01-16 retained learner API hash is invalid for {world_id}"
            )
        learner_hashes[world_id] = learner_hash
        cells = row.get("cells")
        if not isinstance(cells, list):
            raise TypeError(f"R01-16 retained cells are invalid for {world_id}")
        route_hashes: dict[str, str] = {}
        for cell in cells:
            if not isinstance(cell, dict):
                raise TypeError("R01-16 retained capability cell must be an object")
            route_id = str(cell.get("probe_route_id", ""))
            cert_hash = str(cell.get("reachability_certificate_sha256", ""))
            if route_id in route_hashes:
                raise RuntimeError(
                    f"duplicate retained route identity: {world_id}/{route_id}"
                )
            if len(cert_hash) != 64 or any(
                char not in "0123456789abcdef" for char in cert_hash
            ):
                raise RuntimeError(
                    f"invalid retained reachability hash: {world_id}/{route_id}"
                )
            route_hashes[route_id] = cert_hash
        if set(route_hashes) != set(world.probe_order):
            raise RuntimeError(
                f"R01-16 retained probe grid drifted for {world_id}"
            )
        reachability[world_id] = route_hashes

    return R0116RetainedCapabilityBinding(
        construction_census_sha256=actual_sha,
        construction_world_grid_sha256=expected_grid_hash,
        retained_reachability_sha256=reachability,
        retained_learner_api_hash=learner_hashes,
    )


@dataclass(frozen=True, slots=True)
class R0116CapabilityPackage:
    source_manifest: R0116SourceManifest
    retained_binding: R0116RetainedCapabilityBinding
    control_mode: ControlMode

    def validate(self) -> None:
        self.source_manifest.validate()
        if self.control_mode not in {"distributed-github", "local-offline"}:
            raise ValueError("unsupported R01-16 capability control mode")
        if (
            self.retained_binding.construction_census_sha256
            != R01_16_CONSTRUCTION_CENSUS_SHA256
        ):
            raise RuntimeError("R01-16 retained construction binding drifted")

    @property
    def run_id(self) -> str:
        self.validate()
        return (
            "rv01-r01-16-capability-"
            f"{self.source_manifest.source_git_sha[:16]}-"
            f"{self.retained_binding.binding_sha256[:12]}"
        )

    @property
    def output_relpath(self) -> Path:
        return R01_16_CAPABILITY_OUTPUT_ROOT / self.run_id

    @property
    def local_started_relpath(self) -> Path:
        return R01_16_CAPABILITY_CONTROL_ROOT / f"{self.run_id}.STARTED.json"

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "protocol_id": "rv01-r01-16-propagation-factorization-v1",
            "stage": "exposed-development-capability",
            "source_git_sha": self.source_manifest.source_git_sha,
            "source_manifest_sha256": self.source_manifest.manifest_sha256,
            "retained_binding_sha256": self.retained_binding.binding_sha256,
            "construction_census_sha256": R01_16_CONSTRUCTION_CENSUS_SHA256,
            "construction_preserve_ref": R01_16_CONSTRUCTION_PRESERVE_REF,
            "world_grid_sha256": development_world_grid_hash(),
            "python_implementation": R01_16_CAPABILITY_PYTHON_IMPLEMENTATION,
            "python_version": R01_16_CAPABILITY_PYTHON_VERSION,
            "control_mode": self.control_mode,
            "freeze_ref": R01_16_CAPABILITY_FREEZE_REF,
            "remote_started_ref": R01_16_CAPABILITY_CONTROL_REF,
            "preserve_ref": R01_16_CAPABILITY_PRESERVE_REF,
            "run_id": self.run_id,
            "output_relpath": self.output_relpath.as_posix(),
            "local_started_relpath": self.local_started_relpath.as_posix(),
            "retry_same_identity_allowed": False,
            "held_out_capability_allowed": False,
            "formal_execution_allowed": False,
        }

    @property
    def package_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


def _atomic_write_started(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o444)
    try:
        raw = (
            json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)


def execute_capability_once(
    *,
    repo_root: Path,
    source_manifest_path: Path,
    construction_census_path: Path,
    control_mode: ControlMode,
) -> Path:
    """Consume one R01-16 development capability identity exactly once locally.

    In distributed mode the caller must have already acquired the immutable
    remote STARTED/control ref. This function owns the second, local atomic claim
    and has deliberately no retry path.
    """

    root = repo_root.resolve(strict=True)
    manifest = load_source_manifest(source_manifest_path)
    verify_r01_16_source_checkout(root, manifest)
    verify_bound_runtime()
    retained = load_retained_capability_binding(construction_census_path)
    package = R0116CapabilityPackage(
        source_manifest=manifest,
        retained_binding=retained,
        control_mode=control_mode,
    )
    package.validate()

    started_path = root / package.local_started_relpath
    output_dir = root / package.output_relpath
    if started_path.exists() or output_dir.exists():
        raise FileExistsError(
            f"refusing to reuse consumed R01-16 capability identity: {package.run_id}"
        )
    started = {
        "status": "STARTED",
        "package": package.state_dict(),
        "package_sha256": package.package_sha256,
        "human_review": "HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11",
        "execution_authorization": (
            "GLOBAL_EXPERIMENT_FORMAL_EXECUTION_PREAUTHORIZATION_2026-09-13"
        ),
    }
    _atomic_write_started(started_path, started)
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "STARTED.json").write_text(
        json.dumps(started, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    try:
        result = run_development_capability_suite(
            retained_reachability_sha256=retained.retained_reachability_sha256,
        )
        payload = {
            "status": "CAPABILITY_COMPLETE",
            "package": package.state_dict(),
            "package_sha256": package.package_sha256,
            "result": result,
            "held_out_capability_executed": False,
            "formal_execution_allowed": False,
            "retry_same_identity_allowed": False,
        }
        (output_dir / "capability_result.json").write_text(
            json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "COMPLETE.json").write_text(
            json.dumps(
                {
                    "status": "CAPABILITY_COMPLETE",
                    "run_id": package.run_id,
                    "package_sha256": package.package_sha256,
                    "suite_hash": result["suite_hash"],
                    "factor_classification": result["factor_classification"],
                    "held_out_capability_executed": False,
                    "formal_execution_allowed": False,
                    "retry_same_identity_allowed": False,
                },
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        (output_dir / "FAILED.json").write_text(
            json.dumps(
                {
                    "status": "CAPABILITY_FAILED_TERMINAL_IDENTITY_CONSUMED",
                    "run_id": package.run_id,
                    "package_sha256": package.package_sha256,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "retry_same_identity_allowed": False,
                },
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        raise
    return output_dir


__all__ = [
    "R01_16_CAPABILITY_CONTROL_REF",
    "R01_16_CAPABILITY_FREEZE_REF",
    "R01_16_CAPABILITY_PRESERVE_REF",
    "R01_16_CONSTRUCTION_CENSUS_RELPATH",
    "R01_16_CONSTRUCTION_CENSUS_SHA256",
    "R01_16_CONSTRUCTION_PRESERVE_REF",
    "R0116CapabilityPackage",
    "R0116RetainedCapabilityBinding",
    "execute_capability_once",
    "load_retained_capability_binding",
    "load_source_manifest",
    "verify_bound_runtime",
]
