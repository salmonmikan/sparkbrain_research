import hashlib
import json

import pytest

from scripts.audit_temporal_reuse_saved_traces import audit, require, similarity


def pattern(units, bins):
    return {"ordered_units": units, "relative_bins": bins, "unit_ids": sorted(set(units))}


def test_identical_pattern():
    p = pattern([63, 45, 56], [0, 13, 14])
    assert similarity(p, p)["total"] == 1.0


def test_recorded_boundary_components():
    old_b = pattern([56, 45, 63], [0, 0, 4])
    changed_a = pattern([56, 45, 63, 45], [0, 0, 17, 32])
    parts = similarity(old_b, changed_a)
    assert parts["edit"] == 0.75
    assert parts["jaccard"] == 1.0
    assert parts["total"] == pytest.approx(0.7301930850213485, abs=1e-15)


def test_bin_tie_does_not_remove_order_sensitivity():
    p = pattern([45, 56, 63, 45], [0, 0, 14, 30])
    q = pattern([56, 45, 63, 45], [0, 0, 14, 30])
    parts = similarity(p, q)
    assert parts["timing"] == 1.0
    assert parts["edit"] == 0.5
    assert parts["total"] == 0.7250000000000001


def test_explicit_failure():
    with pytest.raises(ValueError, match="required"):
        require(False, "required")


def test_hash_mismatch_is_rejected_without_writing(tmp_path):
    (tmp_path / "raw.json").write_text("corrupted\n")
    manifest = {"files": {"raw.json": hashlib.sha256(b"original\n").hexdigest()}}
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    with pytest.raises(ValueError, match="hash mismatch"):
        audit(tmp_path)
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


def test_published_trace_arithmetic_bytes():
    import gzip
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    p = root / "artifacts/research/temporal_reuse_causal_triage_20261001"
    manifest = json.loads((p / "MANIFEST.json").read_text())
    for name, expected in manifest["files"].items():
        assert hashlib.sha256((p / name).read_bytes()).hexdigest() == expected
    raw = gzip.decompress((p / "TRACE_AUDIT.json.gz").read_bytes())
    assert len(raw) == manifest["output_json_bytes"]
    assert hashlib.sha256(raw).hexdigest() == manifest["output_json_sha256"]
    report = json.loads(raw)
    assert report["model_calls"] == 0
    assert report["retained_manifest_files_verified"] == 232
    assert sum(c["rows"] for c in report["cases"].values()) == 256
    assert sum(c["rows"] for c in report["ordinary_memory_cases"].values()) == 384
    assert (
        hashlib.sha256(
            (root / "scripts/audit_temporal_reuse_saved_traces.py").read_bytes()
        ).hexdigest()
        == manifest["audit_script_sha256"]
    )
