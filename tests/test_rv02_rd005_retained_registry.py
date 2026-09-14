from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.research import rv02_rd005_retained_registry as registry_module
from sparkbrain.research.rv02_scale import ScaleStudyConfig, development_worlds


CONFIG = ScaleStudyConfig().state_dict()
WORLD_IDS = sorted(str(world["world_id"]) for world in development_worlds(ScaleStudyConfig()))


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def _build_fixture(tmp_path: Path) -> Path:
    root = tmp_path
    retained = root / "artifacts/research/rv02"
    for name in registry_module._EXPECTED_ROOT_ENTRIES:
        path = retained / name
        if "." in name and not name.startswith("smoke-"):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"bundle" if name.endswith(".bundle") else b"placeholder")
        else:
            path.mkdir(parents=True, exist_ok=True)

    (retained / "README.md").write_text(
        "- `smoke-v1-invalid`: retained unchanged, NOT valid evidence.\n"
        "- `smoke-v2`: separate development-only smoke after publication hardening.\n",
        encoding="utf-8",
    )

    for path, protocol in registry_module._EXPECTED_MANIFESTS:
        _write_json(root / path, {"protocol": protocol, "config": CONFIG})

    rd003 = root / registry_module._RD003_PATH
    rd003.parent.mkdir(parents=True, exist_ok=True)
    rd003.write_text(
        "RD003 reuses the already exposed RV02 development worlds\n",
        encoding="utf-8",
    )
    rd004 = root / registry_module._RD004_PATH
    rd004.write_text(
        "The frozen first execution is preserved as attempt 001.\n"
        "- same exposed RV02 development worlds;\n",
        encoding="utf-8",
    )
    audit = root / registry_module._AUDIT_PATH
    audit.write_text("reviewed\n", encoding="utf-8")

    spec = {
        "registry_id": "rv02-rd005-retained-identities-v1",
        "authoritative_complete": True,
        "retained_evidence_root_entries": sorted(registry_module._EXPECTED_ROOT_ENTRIES),
        "immutable_ref_anchors": dict(registry_module._EXPECTED_REF_ANCHORS),
        "consumed_or_reserved_seed_ids": [92001],
        "consumed_or_reserved_world_ids": WORLD_IDS,
        "prospective_rd005": {
            "fresh_seed": 92505,
            "self_certification_allowed": False,
            "included_in_prior_registry": False,
        },
    }
    _write_json(root / registry_module.REGISTRY_SPEC_PATH, spec)
    return root


def test_build_authoritative_registry_from_exact_retained_inventory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_fixture(tmp_path)
    monkeypatch.setattr(registry_module, "_validate_repo_root", lambda value: value.resolve())

    registry = registry_module.build_authoritative_rd005_collision_registry(root)

    assert registry.authoritative_complete is True
    assert registry.consumed_or_reserved_seed_ids == (92001,)
    assert registry.consumed_or_reserved_world_ids == tuple(WORLD_IDS)
    assert registry.registry_sha256
    assert 92505 not in registry.consumed_or_reserved_seed_ids


def test_registry_fails_closed_if_retained_root_gains_unreviewed_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_fixture(tmp_path)
    (root / "artifacts/research/rv02/unreviewed-rd000").mkdir()
    monkeypatch.setattr(registry_module, "_validate_repo_root", lambda value: value.resolve())

    with pytest.raises(ValueError, match="retained evidence root changed"):
        registry_module.build_authoritative_rd005_collision_registry(root)


def test_registry_rejects_candidate_self_certified_freshness(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_fixture(tmp_path)
    spec_path = root / registry_module.REGISTRY_SPEC_PATH
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["prospective_rd005"]["self_certification_allowed"] = True
    _write_json(spec_path, spec)
    monkeypatch.setattr(registry_module, "_validate_repo_root", lambda value: value.resolve())

    with pytest.raises(ValueError, match="must not be self-certified"):
        registry_module.build_authoritative_rd005_collision_registry(root)


def test_registry_rejects_manifest_identity_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _build_fixture(tmp_path)
    manifest = root / "artifacts/research/rv02/rd002/manifest.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["config"]["seed"] = 92002
    _write_json(manifest, payload)
    monkeypatch.setattr(registry_module, "_validate_repo_root", lambda value: value.resolve())

    with pytest.raises(ValueError, match="seed list does not equal identities reconstructed"):
        registry_module.build_authoritative_rd005_collision_registry(root)
