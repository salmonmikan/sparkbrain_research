from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/experiments/ni01/preformal_contract.json"

EXPECTED_SOURCE_BLOBS = {
    "src/sparkbrain/tasks/worlds.py": "2478fba19d7276ebe30ec8f5811bf6d7b7414779",
    "src/sparkbrain/evaluation/runner.py": "90543b184c64981802560601b85edcdee4583a35",
    "src/sparkbrain/evaluation/ablations.py": "caa6a1c63fedc2222aa2e6ce708b66668943e8dd",
    "configs/experiments/phase1/main.json": "0134abeaf3d0551edeeb890502ffebe2c27867b0",
    "src/sparkbrain/evaluation/ni01.py": "37cf7f59725988155199148f1a62ba77ab6ca0cf",
}


def _read_contract() -> dict[str, Any]:
    data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("NI01 contract must be a JSON object")
    return data


def _git_blob(path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    contract = _read_contract()
    if contract["status"] != "PREFORMAL_REVIEW_ONLY":
        raise SystemExit("NI01 must remain preformal")
    if contract["formal_execution_authorized"] is not False:
        raise SystemExit("formal execution must remain unauthorized")
    identity = contract["formal_identity_plan"]
    if identity["state"] != "UNRESERVED":
        raise SystemExit("formal identity must remain unreserved")

    inputs = contract["inputs"]
    if inputs["worlds"] != [
        "reliability_world",
        "delayed_evidence_world",
        "contradiction_world",
    ]:
        raise SystemExit("unexpected NI01 world set")
    if inputs["steps_per_episode"] != 30:
        raise SystemExit("unexpected NI01 episode length")
    if inputs["dev"] != {
        "seed_start": 510000,
        "seed_end_inclusive": 510255,
        "episodes_per_world": 256,
        "total_episodes": 768,
        "target_visibility": "forbidden during threshold derivation",
    }:
        raise SystemExit("DEV schedule changed")
    if inputs["test"] != {
        "seed_start": 610000,
        "seed_end_inclusive": 610511,
        "episodes_per_world": 512,
        "total_episodes": 1536,
        "target_visibility_before_raw_preserve": "forbidden",
    }:
        raise SystemExit("TEST schedule changed")

    statistics = contract["statistics"]
    if statistics["resamples"] != 10_000 or statistics["bootstrap_seed"] != 74_017:
        raise SystemExit("bootstrap contract changed")
    if statistics["quantile"] != "Type-7":
        raise SystemExit("quantile contract changed")

    classification = contract["classification"]
    expected_fragments = {
        "PASS_NATIVE_NO_IGNITION_ADDS_SELECTIVE_VALUE": "effect_ci95_lower >= 0.02",
        "FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION": "effect_ci95_upper <= 0.005",
        "INCONCLUSIVE": "all other valid outcomes",
    }
    for key, fragment in expected_fragments.items():
        if fragment not in classification[key]:
            raise SystemExit(f"classification contract changed: {key}")
    if "<= 0.03" not in classification["coverage_guard"]:
        raise SystemExit("coverage guard changed")

    raw_contract = contract["raw_contract"]
    if raw_contract["expected_test_episode_count"] != 1536:
        raise SystemExit("TEST episode cardinality changed")
    if raw_contract["expected_test_step_count"] != 46_080:
        raise SystemExit("TEST step cardinality changed")
    if raw_contract["join_key"] != ["world", "seed", "step_index"]:
        raise SystemExit("join key changed")

    actual_blobs = {path: _git_blob(path) for path in EXPECTED_SOURCE_BLOBS}
    if actual_blobs != EXPECTED_SOURCE_BLOBS:
        raise SystemExit(f"source binding drift: expected {EXPECTED_SOURCE_BLOBS}, got {actual_blobs}")

    source_binding = contract["source_binding"]
    if source_binding["worlds_blob"] != EXPECTED_SOURCE_BLOBS["src/sparkbrain/tasks/worlds.py"]:
        raise SystemExit("worlds binding mismatch")
    if source_binding["runner_blob"] != EXPECTED_SOURCE_BLOBS["src/sparkbrain/evaluation/runner.py"]:
        raise SystemExit("runner binding mismatch")
    if source_binding["ablations_blob"] != EXPECTED_SOURCE_BLOBS[
        "src/sparkbrain/evaluation/ablations.py"
    ]:
        raise SystemExit("ablation binding mismatch")
    if source_binding["phase1_main_config_blob"] != EXPECTED_SOURCE_BLOBS[
        "configs/experiments/phase1/main.json"
    ]:
        raise SystemExit("phase1 config binding mismatch")
    if source_binding["ni01_scorer_blob"] != EXPECTED_SOURCE_BLOBS[
        "src/sparkbrain/evaluation/ni01.py"
    ]:
        raise SystemExit("NI01 scorer binding mismatch")

    hypothesis = (ROOT / "docs/HYPOTHESES_AND_FALSIFICATION.md").read_text(encoding="utf-8")
    if "### H4 — No-ignition is a valuable computational state" not in hypothesis:
        raise SystemExit("independent H4 motivation is missing from the authoritative source")

    print("NI01 preformal contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
