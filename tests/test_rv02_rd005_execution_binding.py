from __future__ import annotations

import pytest

import sparkbrain.research.rv02_rd005_execution_binding as binding


def test_rd005_d1_execution_binding_is_exact_and_construction_only() -> None:
    state = binding.RD005_D1_EXECUTION_BINDING.state_dict()

    assert state["python_implementation"] == "CPython"
    assert state["python_version"] == "3.11.15"
    assert state["entrypoint_module"] == "sparkbrain.research.rv02_rd005_bound_construction"
    assert state["command_argv_template"] == [
        "python",
        "-m",
        "sparkbrain.research.rv02_rd005_bound_construction",
        "--input",
        "{construction_input_path}",
        "--repo-root",
        "{repo_root}",
    ]
    assert state["construction_only"] is True
    assert state["capability_output_opened"] is False
    assert state["held_out_capability_allowed"] is False
    assert state["formal_execution_allowed"] is False
    assert len(binding.RD005_D1_EXECUTION_BINDING.binding_sha256) == 64


def test_rd005_d1_execution_binding_rejects_runtime_or_command_drift() -> None:
    with pytest.raises(ValueError, match="Python version"):
        binding.RD005D1ExecutionBinding(python_version="3.11.14").validate()

    with pytest.raises(ValueError, match="command argv template"):
        binding.RD005D1ExecutionBinding(command_argv_template=("python", "script.py")).validate()


def test_rd005_d1_runtime_verifier_accepts_exact_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(binding.platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(binding.platform, "python_version", lambda: "3.11.15")

    assert binding.verify_rd005_d1_runtime() == {
        "python_implementation": "CPython",
        "python_version": "3.11.15",
    }


def test_rd005_d1_runtime_verifier_fails_closed_on_version_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(binding.platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(binding.platform, "python_version", lambda: "3.13.7")

    with pytest.raises(RuntimeError, match="Python version mismatch"):
        binding.verify_rd005_d1_runtime()
