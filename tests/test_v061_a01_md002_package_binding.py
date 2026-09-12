from __future__ import annotations

from dataclasses import fields

import pytest

from sparkbrain.v061_a01.md002_package_binding import (
    MD002ExecutionDisabledPackage,
    MD002RuntimeBinding,
    MD002SourceManifest,
)

_REQUIRED_PATHS = (
    "src/sparkbrain/v061_a01/credit_bridge.py",
    "src/sparkbrain/v061_a01/md002_bound_world.py",
    "src/sparkbrain/v061_a01/md002_fixtures.py",
    "src/sparkbrain/v061_a01/md002_p2_attribution_kernel.py",
    "src/sparkbrain/v061_a01/md002_p2_schedule.py",
    "src/sparkbrain/v061_a01/md002_p3_development_plan.py",
    "src/sparkbrain/v061_a01/md002_p3_fixture.py",
    "src/sparkbrain/v061_a01/md002_p3_harness.py",
    "src/sparkbrain/v061_a01/md002_p4_fixture.py",
    "src/sparkbrain/v061_a01/md002_p4_trace_binding.py",
    "src/sparkbrain/v061_a01/md002_protocol.py",
    "src/sparkbrain/v061_a01/md002_restore_adapter.py",
    "src/sparkbrain/v061_a01/md002_state_binding.py",
    "src/sparkbrain/v061_a01/md002_world_fixture.py",
    "src/sparkbrain/v061_a01/mechanism_discrimination.py",
    "src/sparkbrain/v061_a01/recurrent_adapter.py",
    "src/sparkbrain/v061_a01/recurrent_development.py",
)


def _manifest(*, omit: str | None = None) -> MD002SourceManifest:
    paths = tuple(path for path in _REQUIRED_PATHS if path != omit)
    return MD002SourceManifest(
        source_git_sha="a" * 40,
        file_sha256=tuple((path, "b" * 64) for path in paths),
    )


def _runtime() -> MD002RuntimeBinding:
    return MD002RuntimeBinding(
        python_implementation="CPython",
        python_version="3.13.7",
        python_executable="/opt/python/bin/python",
        command=("python", "-m", "sparkbrain.v061_a01.md002_runner", "--package", "x"),
    )


def _package() -> MD002ExecutionDisabledPackage:
    return MD002ExecutionDisabledPackage(
        source_manifest=_manifest(),
        runtime=_runtime(),
        protocol_sha256="c" * 64,
        matrix_sha256="d" * 64,
        n3_source_git_sha="e" * 40,
        n3_config_sha256="f" * 64,
        resource_matching_policy_sha256="1" * 64,
        raw_artifact_schema_sha256="2" * 64,
    )


def test_source_manifest_requires_all_boundary_critical_paths() -> None:
    value = _manifest(omit="src/sparkbrain/v061_a01/md002_protocol.py")
    with pytest.raises(ValueError, match="missing critical paths"):
        value.validate()


def test_source_manifest_rejects_path_traversal_even_with_required_files() -> None:
    value = MD002SourceManifest(
        source_git_sha="a" * 40,
        file_sha256=tuple(
            sorted(
                (*((path, "b" * 64) for path in _REQUIRED_PATHS), ("../escape.py", "c" * 64))
            )
        ),
    )
    with pytest.raises(ValueError, match="unsafe or non-canonical"):
        value.validate()


def test_package_identity_binds_source_runtime_matrix_n3_and_artifact_contracts() -> None:
    package = _package()
    package.validate()
    state = package.state_dict()

    assert state["source_manifest_sha256"] == package.source_manifest.manifest_sha256
    assert state["runtime_sha256"] == package.runtime.runtime_sha256
    assert state["n3_source_git_sha"] == "e" * 40
    assert state["formal_execution_allowed"] is False
    assert state["capability_output_opened"] is False
    assert state["execution_seal_issued"] is False
    assert state["started"] is False
    assert package.output_relpath.endswith(f"package-{package.package_sha256}")


def test_exact_package_identity_has_one_deterministic_output_namespace() -> None:
    left = _package()
    right = _package()

    assert left.package_sha256 == right.package_sha256
    assert left.output_relpath == right.output_relpath


def test_runtime_command_is_part_of_package_identity() -> None:
    left = _package()
    changed_runtime = MD002RuntimeBinding(
        python_implementation="CPython",
        python_version="3.13.7",
        python_executable="/opt/python/bin/python",
        command=("python", "-m", "sparkbrain.v061_a01.md002_runner", "--package", "y"),
    )
    right = MD002ExecutionDisabledPackage(
        source_manifest=left.source_manifest,
        runtime=changed_runtime,
        protocol_sha256=left.protocol_sha256,
        matrix_sha256=left.matrix_sha256,
        n3_source_git_sha=left.n3_source_git_sha,
        n3_config_sha256=left.n3_config_sha256,
        resource_matching_policy_sha256=left.resource_matching_policy_sha256,
        raw_artifact_schema_sha256=left.raw_artifact_schema_sha256,
    )

    assert left.package_sha256 != right.package_sha256
    assert left.output_relpath != right.output_relpath


def test_package_contract_has_no_caller_controlled_authority_fields() -> None:
    names = {field.name for field in fields(MD002ExecutionDisabledPackage)}

    assert "approved" not in names
    assert "execution_authority" not in names
    assert "formal_execution_allowed" not in names
    assert "started" not in names
