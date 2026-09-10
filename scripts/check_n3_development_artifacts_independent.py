"""Read-only independent N3-DEV-001 artifact audit; never executes a model."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode()


def logical_bytes(value):
    if value is None:
        return 0
    if type(value) is bool:
        return 1
    if type(value) in (int, float):
        return 8
    if type(value) is str:
        return 8 + len(value.encode())
    if type(value) is list:
        return 8 + sum(map(logical_bytes, value))
    if type(value) is dict:
        return 8 + sum(logical_bytes(k) + logical_bytes(v) for k, v in value.items())
    raise AssertionError(type(value))


def audit(output: Path):
    assert {p.name for p in output.iterdir()} == {
        "protocol.json", "source_manifest.json", "raw_rows.jsonl", "summary.json"}
    rows = [json.loads(line) for line in (output / "raw_rows.jsonl").read_text().splitlines()]
    summary = json.loads((output / "summary.json").read_text())
    protocol = json.loads((output / "protocol.json").read_text())
    manifest = json.loads((output / "source_manifest.json").read_text())
    assert manifest == protocol["authorization"]["source_manifest"]
    assert hashlib.sha256(protocol["preregistration"].encode()).hexdigest() == manifest[
        "docs/research/V061_A01_N3_DEV_001_PREREG.md"]
    assert len(rows) == summary["rows"] == 72
    assert summary["execution_status"] == "COMPLETE" and summary["failure"] is None
    assert summary["resource_matching"] == summary["full_md002"] == "NOT_EVALUATED"
    expected = itertools.product(("confirmation", "contradiction", "absence", "replay"),
                                 (0, 1, 4), ("first", "second", "both"), ("A01", "N3"))
    for row, (evidence, delay, ancestry, arm) in zip(rows, expected, strict=True):
        assert row["specification"] == dict(evidence=evidence, delay=delay, ancestry=ancestry)
        assert row["case_id"] == f"n3dev001:{evidence}:{delay}:{ancestry}"
        assert row["arm"] == arm
        assert (
            hashlib.sha256(canonical(row["inputs"])).hexdigest()
            == row["admissible_input_sha256"]
        )
        assert row["resources"]["resource_matching"] == "NOT_EVALUATED"
        cuts = row["checkpoints"]
        assert [c["cut"] for c in cuts] == ["initialization", "activity"] + [
            f"idle:{i}" for i in range(delay)] + ["pre-evidence", "post-evidence", "post-probe"]
        for cut in cuts:
            assert cut["canonical_bytes"] == len(canonical(cut["state"])) <= 65536
            assert cut["normalized_payload_bytes"] == logical_bytes(cut["state"])
        before, after = cuts[-3]["state"]["expectation"], cuts[-2]["state"]["expectation"]
        mechanism = after["n3_trace"] if arm == "N3" else after["a01_causal_support"]
        assert row["resources"]["mechanism_checkpoint_bytes"] == len(canonical(mechanism))
        assert row["resources"]["mechanism_normalized_bytes"] == logical_bytes(mechanism)
        for unavailable in (
            "shared_router_operations",
            "exact_transient_peak",
            "resident_duplicates",
        ):
            assert row["resources"][unavailable] is None
        if evidence in ("absence", "replay"):
            assert row["learned_unchanged"]
            assert row["learned_before_sha256"] == row["learned_after_sha256"]
            key = "a01_causal_support" if arm == "A01" else "n3_trace"
            assert before[key] == after[key]
        if evidence == "replay":
            assert row["replay_rejected"] is True
        if evidence in ("confirmation", "contradiction"):
            expected_status = (
                "exact-match" if evidence == "confirmation" else "exact-contradiction"
            )
            assert row["resolution"]["status"] == expected_status
        if arm == "N3":
            trace = after["n3_trace"]
            assert trace["tick"] == delay + 1
            assert trace["counters"]["hidden_writes"] == 2 * (delay + 1)
            assert row["resources"]["fixed_weight_scalars"] == len(trace["fixed"])
            assert row["resources"]["retained_hidden_scalars"] == len(trace["hidden"])
    pairs = list(zip(rows[::2], rows[1::2], strict=True))
    assert len(summary["comparisons"]) == 36
    for (a, b), comparison in zip(pairs, summary["comparisons"], strict=True):
        assert a["inputs"] == b["inputs"]
        assert a["admissible_input_sha256"] == b["admissible_input_sha256"]
        assert comparison == dict(
            case_id=a["case_id"],
            a01=a["confidence_after"],
            n3=b["confidence_after"],
            equal=a["confidence_after"] == b["confidence_after"],
        )
    assert summary["controls_learned_unchanged"] is True
    return dict(status="PASS", rows=72, cases=36, controls=36,
                equal_endpoint_cases=sum(c["equal"] for c in summary["comparisons"]),
                resource_matching="NOT_EVALUATED", full_md002="NOT_EVALUATED",
                artifact_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(output.iterdir())})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.output), sort_keys=True, indent=2))
