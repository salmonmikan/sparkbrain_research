from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import sparkbrain.research.rv01_r01_16_capability_package as capability_package
from sparkbrain.research.rv01_r01_16_capability_package import (
    R01_16_CAPABILITY_REQUIRED_SOURCE_PATHS,
    R0116CapabilityPackage,
    R0116RetainedCapabilityBinding,
    _atomic_write_started,
    load_retained_capability_binding,
    load_source_manifest,
)
from sparkbrain.research.rv01_r01_16_development_package import (
    R01_16_REQUIRED_SOURCE_PATHS,
    R0116SourceManifest,
    R0116SourceManifestEntry,
)
from sparkbrain.research.rv01_r01_16_worlds import (
    development_world_grid,
    development_world_grid_hash,
)

_VALID_SHA = "a" * 64


def _manifest(source_git_sha: str = "1" * 40) -> R0116SourceManifest:
    paths = sorted(R01_16_REQUIRED_SOURCE_PATHS | R01_16_CAPABILITY_REQUIRED_SOURCE_PATHS)
    return R0116SourceManifest(
        source_git_sha=source_git_sha,
        entries=tuple(R0116SourceManifestEntry(path=path, sha256=_VALID_SHA) for path in paths),
    )


def _retained_binding() -> R0116RetainedCapabilityBinding:
    worlds = development_world_grid()
    return R0116RetainedCapabilityBinding(
        construction_census_sha256=capability_package.R01_16_CONSTRUCTION_CENSUS_SHA256,
        construction_world_grid_sha256=development_world_grid_hash(),
        retained_reachability_sha256={
            world.world_id: {route_id: _VALID_SHA for route_id in world.probe_order}
            for world in worlds
        },
        retained_learner_api_hash={world.world_id: _VALID_SHA for world in worlds},
    )


def _synthetic_census() -> dict[str, object]:
    worlds = []
    for world in development_world_grid():
        worlds.append(
            {
                "world": world.state_dict(),
                "world_specification_sha256": world.specification_hash(),
                "learner_api_hash": _VALID_SHA,
                "cells": [
                    {
                        "probe_route_id": route_id,
                        "reachability_certificate_sha256": _VALID_SHA,
                    }
                    for route_id in world.probe_order
                ],
            }
        )
    return {
        "schema": "rv01-r01-16-construction-census-v1",
        "status": "CONSTRUCTION_CENSUS_COMPLETE_CAPABILITY_UNOPENED",
        "capability_output_opened": False,
        "probe_executed": False,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
        "same_identity_rerun_allowed": False,
        "world_grid_sha256": development_world_grid_hash(),
        "worlds": worlds,
    }


def test_local_started_claim_is_atomic_and_no_clobber(tmp_path: Path) -> None:
    path = tmp_path / "control" / "STARTED.json"
    payload = {"status": "STARTED", "identity": "first"}

    _atomic_write_started(path, payload)
    first_bytes = path.read_bytes()

    with pytest.raises(FileExistsError):
        _atomic_write_started(path, {"status": "STARTED", "identity": "second"})

    assert path.read_bytes() == first_bytes


def test_capability_package_identity_binds_source_retained_state_and_mode() -> None:
    package = R0116CapabilityPackage(
        source_manifest=_manifest(),
        retained_binding=_retained_binding(),
        control_mode="distributed-github",
    )

    first = package.state_dict()
    second = package.state_dict()

    assert first == second
    assert package.run_id.startswith("rv01-r01-16-capability-1111111111111111-")
    assert first["control_mode"] == "distributed-github"
    assert first["single_host_ownership_asserted"] is False
    assert first["retry_same_identity_allowed"] is False
    assert first["held_out_capability_allowed"] is False
    assert first["formal_execution_allowed"] is False


def test_local_mode_requires_explicit_single_host_ownership() -> None:
    with pytest.raises(RuntimeError, match="single-host ownership"):
        R0116CapabilityPackage(
            source_manifest=_manifest(),
            retained_binding=_retained_binding(),
            control_mode="local-offline",
        ).validate()

    package = R0116CapabilityPackage(
        source_manifest=_manifest(),
        retained_binding=_retained_binding(),
        control_mode="local-offline",
        single_host_ownership_asserted=True,
    )
    state = package.state_dict()
    assert state["control_mode"] == "local-offline"
    assert state["single_host_ownership_asserted"] is True


def test_load_source_manifest_requires_capability_boundary_files(tmp_path: Path) -> None:
    manifest = _manifest().state_dict()
    missing_path = "scripts/run_rv01_r01_16_capability.py"
    manifest["entries"] = [
        row for row in manifest["entries"] if row["path"] != missing_path
    ]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="missing required paths"):
        load_source_manifest(path)


def test_retained_binding_requires_exact_census_bytes_and_world_grid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = _synthetic_census()
    path = tmp_path / "construction_census.json"
    raw = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    path.write_bytes(raw)
    monkeypatch.setattr(
        capability_package,
        "R01_16_CONSTRUCTION_CENSUS_SHA256",
        hashlib.sha256(raw).hexdigest(),
    )

    binding = load_retained_capability_binding(path)

    assert len(binding.retained_reachability_sha256) == 25
    expected_route_counts = {
        world.world_id: len(world.probe_order) for world in development_world_grid()
    }
    actual_route_counts = {
        world_id: len(routes)
        for world_id, routes in binding.retained_reachability_sha256.items()
    }
    assert actual_route_counts == expected_route_counts
    assert sum(actual_route_counts.values()) == 100

    tampered = raw + b"\n"
    path.write_bytes(tampered)
    with pytest.raises(RuntimeError, match="digest mismatch"):
        load_retained_capability_binding(path)


def test_retained_binding_rejects_capability_already_opened(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = _synthetic_census()
    payload["capability_output_opened"] = True
    path = tmp_path / "construction_census.json"
    raw = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    path.write_bytes(raw)
    monkeypatch.setattr(
        capability_package,
        "R01_16_CONSTRUCTION_CENSUS_SHA256",
        hashlib.sha256(raw).hexdigest(),
    )

    with pytest.raises(RuntimeError, match="capability_output_opened"):
        load_retained_capability_binding(path)
