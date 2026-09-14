"""Fail-closed retained-identity registry construction for prospective RV02 RD005.

The registry is reconstructed only from retained repository evidence that predates
RD005 execution.  It does not inspect RD005 outcomes, construct D1, run a learner
or probe, or grant execution authority.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from .rv02_rd005_construction_artifact import RD005_FRESH_SEED
from .rv02_rd005_development_package import RD005CollisionRegistry
from .rv02_scale import ScaleStudyConfig, development_worlds

REGISTRY_SPEC_PATH = Path("docs/research/RV02_RD005_RETAINED_IDENTITY_REGISTRY.json")
RETAINED_ROOT = Path("artifacts/research/rv02")

_EXPECTED_ROOT_ENTRIES = frozenset(
    {
        "README.md",
        "development-feasibility-v1",
        "local-execution-history.bundle",
        "rd001",
        "rd002",
        "rd003",
        "rd004",
        "smoke-v1-invalid",
        "smoke-v2",
    }
)

_EXPECTED_MANIFESTS: tuple[tuple[str, str], ...] = (
    (
        "artifacts/research/rv02/development-feasibility-v1/manifest.json",
        "rv02-development-feasibility-v1",
    ),
    (
        "artifacts/research/rv02/smoke-v2/manifest.json",
        "rv02-development-feasibility-v1",
    ),
    ("artifacts/research/rv02/rd001/manifest.json", "rv02-rd001-development"),
    ("artifacts/research/rv02/rd002/manifest.json", "rv02-rd002-development"),
    (
        "artifacts/research/rv02/smoke-v1-invalid/manifest.json",
        "rv02-development-feasibility-v1",
    ),
)

_EXPECTED_REF_ANCHORS = {
    "preserve/rv02-rd002-accepted-development": "24af1858cb4a8930039b85442583d2bf535a3a49",
    "freeze/rv02-rd003-development-source": "79a949568b2a9a8ee18c40e9b356c564422c0127",
    "preserve/rv02-rd003-attempt-001": "cfe0903b6f2e1d16a6b5581ae004502dabdf62b5",
    "freeze/rv02-rd004-development-source": "75268dd804f0ef113869be172adf575ac22523a0",
    "preserve/rv02-rd004-attempt-001": "2efaf81119a32087b2102bbdbff1af61cbc6bf16",
}

_RD003_PATH = "docs/research/RV02_RD003_ONLINE_HIDDEN_ELIGIBILITY_PREREG.md"
_RD004_PATH = "docs/research/RV02_RD004_RELATIVE_PROBE_CLOCK_PREREG.md"
_README_PATH = "artifacts/research/rv02/README.md"
_AUDIT_PATH = "docs/research/RV02_RD005_RETAINED_IDENTITY_REGISTRY_AUDIT.md"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"retained evidence must be a JSON object: {path}")
    return value


def _git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def _validate_repo_root(repo_root: Path) -> Path:
    root = repo_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("RV02 retained registry repository root must be a directory")
    git_root = Path(_git(root, "rev-parse", "--show-toplevel")).resolve(strict=True)
    if git_root != root:
        raise ValueError(
            "RV02 retained registry repository root does not equal Git top-level: "
            f"expected {root}, got {git_root}"
        )
    return root


def _manifest_config(
    repo_root: Path,
    path: str,
    expected_protocol: str,
) -> ScaleStudyConfig:
    payload = _read_json(repo_root / path)
    if payload.get("protocol") != expected_protocol:
        raise ValueError(
            f"retained manifest protocol mismatch for {path}: "
            f"expected {expected_protocol!r}, got {payload.get('protocol')!r}"
        )
    config_value = payload.get("config")
    if not isinstance(config_value, dict):
        raise TypeError(f"retained manifest config must be an object: {path}")
    return ScaleStudyConfig.from_state_dict(config_value)


def _verify_text_provenance(repo_root: Path) -> None:
    readme = (repo_root / _README_PATH).read_text(encoding="utf-8")
    if "`smoke-v1-invalid`: retained unchanged, NOT valid evidence" not in readme:
        raise ValueError("RV02 retained README no longer classifies smoke-v1-invalid as invalid")
    if "`smoke-v2`: separate development-only smoke" not in readme:
        raise ValueError("RV02 retained README no longer classifies smoke-v2 as development-only")

    rd003 = (repo_root / _RD003_PATH).read_text(encoding="utf-8")
    if "RD003 reuses the already exposed RV02 development worlds" not in rd003:
        raise ValueError("RD003 prereg no longer binds to the exposed RV02 development worlds")

    rd004 = (repo_root / _RD004_PATH).read_text(encoding="utf-8")
    if "same exposed RV02 development worlds" not in rd004:
        raise ValueError("RD004 prereg no longer binds to the exposed RV02 development worlds")
    if "frozen first execution" not in rd004 or "attempt 001" not in rd004:
        raise ValueError("RD004 prereg no longer records RD003 attempt 001 as consumed")


def _verify_ref_spec(spec: dict[str, Any]) -> None:
    anchors = spec.get("immutable_ref_anchors")
    if anchors != _EXPECTED_REF_ANCHORS:
        raise ValueError(
            "RD005 retained registry immutable-ref anchors differ from reviewed anchors"
        )


def _verify_exact_retained_inventory(repo_root: Path, spec: dict[str, Any]) -> None:
    root = repo_root / RETAINED_ROOT
    actual = frozenset(path.name for path in root.iterdir())
    if actual != _EXPECTED_ROOT_ENTRIES:
        missing = sorted(_EXPECTED_ROOT_ENTRIES - actual)
        unexpected = sorted(actual - _EXPECTED_ROOT_ENTRIES)
        raise ValueError(
            "RV02 retained evidence root changed after registry review; "
            f"missing={missing}, unexpected={unexpected}. Re-audit before declaring completeness."
        )
    declared = spec.get("retained_evidence_root_entries")
    if declared != sorted(_EXPECTED_ROOT_ENTRIES):
        raise ValueError(
            "RD005 registry spec retained-root inventory is not the reviewed exact set"
        )
    bundle = root / "local-execution-history.bundle"
    if not bundle.is_file() or bundle.stat().st_size <= 0:
        raise ValueError("RV02 local execution history bundle is absent or empty")


def _verify_spec_shape(spec: dict[str, Any]) -> None:
    if spec.get("registry_id") != "rv02-rd005-retained-identities-v1":
        raise ValueError("unexpected RD005 retained registry_id")
    if spec.get("authoritative_complete") is not True:
        raise ValueError("RD005 retained registry spec must explicitly be authoritative_complete")
    prospective = spec.get("prospective_rd005")
    if not isinstance(prospective, dict):
        raise TypeError("RD005 retained registry prospective_rd005 must be an object")
    if prospective.get("fresh_seed") != RD005_FRESH_SEED:
        raise ValueError("RD005 retained registry prospective seed does not match package seed")
    if prospective.get("self_certification_allowed") is not False:
        raise ValueError("RD005 freshness must not be self-certified")
    if prospective.get("included_in_prior_registry") is not False:
        raise ValueError("prospective RD005 seed must not be inserted into the prior registry")


def build_authoritative_rd005_collision_registry(repo_root: Path) -> RD005CollisionRegistry:
    """Reconstruct the complete pre-RD005 retained collision registry.

    Completeness is fail-closed against the exact retained RV02 evidence-root
    inventory reviewed on 2026-09-14. Any new top-level retained artifact forces
    another audit rather than being silently ignored.
    """

    root = _validate_repo_root(repo_root)
    spec = _read_json(root / REGISTRY_SPEC_PATH)
    _verify_spec_shape(spec)
    _verify_ref_spec(spec)
    _verify_exact_retained_inventory(root, spec)
    _verify_text_provenance(root)

    configs = tuple(
        _manifest_config(root, path, expected_protocol)
        for path, expected_protocol in _EXPECTED_MANIFESTS
    )
    seeds = {config.seed for config in configs}
    world_ids = {
        str(world["world_id"])
        for config in configs
        for world in development_worlds(config)
    }

    declared_seeds = spec.get("consumed_or_reserved_seed_ids")
    declared_worlds = spec.get("consumed_or_reserved_world_ids")
    if declared_seeds != sorted(seeds):
        raise ValueError(
            "RD005 retained registry seed list does not equal identities reconstructed "
            "from the complete retained manifest inventory"
        )
    if declared_worlds != sorted(world_ids):
        raise ValueError(
            "RD005 retained registry world list does not equal canonical identities "
            "reconstructed from the complete retained manifest inventory"
        )
    if RD005_FRESH_SEED in seeds:
        raise ValueError("prospective RD005 seed collides with prior retained evidence")

    source_paths = tuple(
        sorted(
            {
                REGISTRY_SPEC_PATH.as_posix(),
                _AUDIT_PATH,
                _README_PATH,
                _RD003_PATH,
                _RD004_PATH,
                *(path for path, _ in _EXPECTED_MANIFESTS),
                "artifacts/research/rv02/local-execution-history.bundle",
            }
        )
    )
    registry = RD005CollisionRegistry(
        registry_id=str(spec["registry_id"]),
        source_paths=source_paths,
        consumed_or_reserved_seed_ids=tuple(sorted(seeds)),
        consumed_or_reserved_world_ids=tuple(sorted(world_ids)),
        authoritative_complete=True,
    )
    registry.validate()
    return registry


__all__ = [
    "REGISTRY_SPEC_PATH",
    "RETAINED_ROOT",
    "build_authoritative_rd005_collision_registry",
]
