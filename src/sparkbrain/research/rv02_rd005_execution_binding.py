"""Prospective exact runtime/command contract for RV02 RD005 D1 construction.

This module binds the *construction-only* invocation before D1 is opened. It does
not create a source manifest, allocate output, execute D1, open capability, or
grant held-out/formal authority.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass

RD005_D1_PYTHON_IMPLEMENTATION = "CPython"
RD005_D1_PYTHON_VERSION = "3.11.15"
RD005_D1_ENTRYPOINT_MODULE = "sparkbrain.research.rv02_rd005_bound_construction"
RD005_D1_INPUT_PLACEHOLDER = "{construction_input_path}"
RD005_D1_REPO_ROOT_PLACEHOLDER = "{repo_root}"
RD005_D1_COMMAND_ARGV_TEMPLATE = (
    "python",
    "-m",
    RD005_D1_ENTRYPOINT_MODULE,
    "--input",
    RD005_D1_INPUT_PLACEHOLDER,
    "--repo-root",
    RD005_D1_REPO_ROOT_PLACEHOLDER,
)


def _canonical_sha256(value: object) -> str:
    raw = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, slots=True)
class RD005D1ExecutionBinding:
    python_implementation: str = RD005_D1_PYTHON_IMPLEMENTATION
    python_version: str = RD005_D1_PYTHON_VERSION
    entrypoint_module: str = RD005_D1_ENTRYPOINT_MODULE
    command_argv_template: tuple[str, ...] = RD005_D1_COMMAND_ARGV_TEMPLATE

    def validate(self) -> None:
        if self.python_implementation != RD005_D1_PYTHON_IMPLEMENTATION:
            raise ValueError("RD005 D1 Python implementation must remain prospectively fixed")
        if self.python_version != RD005_D1_PYTHON_VERSION:
            raise ValueError("RD005 D1 Python version must remain prospectively fixed")
        if self.entrypoint_module != RD005_D1_ENTRYPOINT_MODULE:
            raise ValueError("RD005 D1 entrypoint module must remain prospectively fixed")
        if self.command_argv_template != RD005_D1_COMMAND_ARGV_TEMPLATE:
            raise ValueError("RD005 D1 command argv template must remain prospectively fixed")
        if self.command_argv_template.count(RD005_D1_INPUT_PLACEHOLDER) != 1:
            raise ValueError("RD005 D1 command must bind exactly one construction-input path")
        if self.command_argv_template.count(RD005_D1_REPO_ROOT_PLACEHOLDER) != 1:
            raise ValueError("RD005 D1 command must bind exactly one repository root")

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "python_implementation": self.python_implementation,
            "python_version": self.python_version,
            "entrypoint_module": self.entrypoint_module,
            "command_argv_template": list(self.command_argv_template),
            "construction_only": True,
            "capability_output_opened": False,
            "held_out_capability_allowed": False,
            "formal_execution_allowed": False,
        }

    @property
    def binding_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


RD005_D1_EXECUTION_BINDING = RD005D1ExecutionBinding()


def verify_rd005_d1_runtime(
    binding: RD005D1ExecutionBinding = RD005_D1_EXECUTION_BINDING,
) -> dict[str, str]:
    """Fail closed unless the live interpreter matches the prospective contract."""

    binding.validate()
    observed = {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }
    if observed["python_implementation"] != binding.python_implementation:
        raise RuntimeError(
            "RD005 D1 Python implementation mismatch: "
            f"expected {binding.python_implementation}, got {observed['python_implementation']}"
        )
    if observed["python_version"] != binding.python_version:
        raise RuntimeError(
            "RD005 D1 Python version mismatch: "
            f"expected {binding.python_version}, got {observed['python_version']}"
        )
    return observed


__all__ = [
    "RD005D1ExecutionBinding",
    "RD005_D1_COMMAND_ARGV_TEMPLATE",
    "RD005_D1_ENTRYPOINT_MODULE",
    "RD005_D1_EXECUTION_BINDING",
    "RD005_D1_INPUT_PLACEHOLDER",
    "RD005_D1_PYTHON_IMPLEMENTATION",
    "RD005_D1_PYTHON_VERSION",
    "RD005_D1_REPO_ROOT_PLACEHOLDER",
    "verify_rd005_d1_runtime",
]
