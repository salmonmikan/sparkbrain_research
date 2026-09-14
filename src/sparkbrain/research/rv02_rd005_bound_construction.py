"""Bound preflight for prospective RV02 RD005 D1 construction.

This module closes a package-integrity gap without opening capability. The legacy
construction runner already validates source/collision identities and performs
source-checkout verification before allocating an output identity, but its input
schema historically accepted any syntactically valid package-plan digest. This
wrapper recomputes the canonical :class:`RD005DevelopmentPackagePlan` digest and
requires an exact match before delegating to that construction-only runner.

No D1 output is created by the preflight itself. Capability, held-out and formal
execution remain closed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.research.rv02_rd005_construction_runner import (
    _load_input,
    run_construction,
)
from sparkbrain.research.rv02_rd005_development_package import RD005DevelopmentPackagePlan


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
    """Verify the bound package plan before invoking D1 construction."""

    raw = input_path.read_bytes()
    verify_package_plan_binding(raw)
    return run_construction(input_path=input_path, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run prospective RV02 RD005 D1 with canonical package-plan preflight."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    run_bound_construction(input_path=args.input, repo_root=args.repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "run_bound_construction", "verify_package_plan_binding"]
