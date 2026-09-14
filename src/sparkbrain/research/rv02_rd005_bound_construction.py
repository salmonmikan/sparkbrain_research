"""Bound preflight for prospective RV02 RD005 D1 construction.

This module closes package/runtime integrity gaps without opening capability. It
recomputes the canonical :class:`RD005DevelopmentPackagePlan` digest, requires
the prospectively fixed CPython runtime, and delegates the exact same verified
input bytes to construction.

No D1 output is created until all preflight checks pass. Capability, held-out and
formal execution remain closed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.research.rv02_rd005_construction_runner import (
    _load_input,
    run_construction_from_bytes,
)
from sparkbrain.research.rv02_rd005_development_package import RD005DevelopmentPackagePlan
from sparkbrain.research.rv02_rd005_execution_binding import verify_rd005_d1_runtime


def verify_package_plan_binding(raw_input: bytes) -> str:
    """Return the canonical package-plan digest or fail closed on mismatch."""

    identities, collision_registry, source_manifest = _load_input(raw_input)
    plan = RD005DevelopmentPackagePlan(
        source_manifest=source_manifest,
        collision_registry=collision_registry,
    )
    plan.validate()
    expected = identities["package_plan_sha256"]
    actual = plan.package_plan_sha256
    if expected != actual:
        raise ValueError(
            "RD005 package_plan_sha256 does not match the canonical source/registry plan: "
            f"expected {actual}, got {expected}"
        )
    return actual


def run_bound_construction(
    *,
    input_path: Path,
    repo_root: Path,
) -> Path:
    """Verify runtime/package binding and construct from one in-memory identity."""

    verify_rd005_d1_runtime()
    raw = input_path.read_bytes()
    verify_package_plan_binding(raw)
    return run_construction_from_bytes(raw=raw, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run prospective RV02 RD005 D1 with exact runtime/package preflight."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args(argv)
    run_bound_construction(input_path=args.input, repo_root=args.repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "run_bound_construction", "verify_package_plan_binding"]
