from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import torch

from sparkbrain.learned.h7_formal_r1 import ENDPOINTS, INTERVENTION_ID
from sparkbrain.learned.h7_formal_r3 import (
    exact_runtime_observation,
    load_and_assert_r3_contract,
    preidentity_sentinel,
)
from sparkbrain.learned.h7_formal_r3_integrity import (
    PreserveProof,
    assert_paths_available_no_clobber,
    prediction_raw_bytes,
    recompute_correctness_after_preserve,
    validate_prior_surface_inventory,
    validate_runtime_binding,
)


def _pip_freeze() -> str:
    completed = subprocess.run(
        ["python", "-m", "pip", "freeze", "--all"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _raw_gate_sentinel() -> dict[str, object]:
    target_id = hashlib.sha256(b"H7-R3-SYNTHETIC-PREIDENTITY-TARGET").hexdigest()
    raw_rows: list[dict[str, object]] = []
    for endpoint in ENDPOINTS:
        row: dict[str, object] = {
            "opaque_target_id": target_id,
            "endpoint": endpoint,
            "intervention_id": INTERVENTION_ID,
            "baseline_prediction": "synthetic-a",
            "cut_prediction": "synthetic-b",
        }
        if endpoint != "FINITE_STATE_ROUTE_HISTORY_V2":
            row["baseline_probabilities"] = [0.75, 0.25]
            row["cut_probabilities"] = [0.25, 0.75]
        raw_rows.append(row)
    target_rows = [
        {
            "opaque_target_id": target_id,
            "world": "switchworld",
            "episode_seed": -1,
            "step_index": 0,
            "truth": "synthetic-a",
        }
    ]
    raw_payload = prediction_raw_bytes(raw_rows)
    raw_sha = hashlib.sha256(raw_payload).hexdigest()
    recomputed = recompute_correctness_after_preserve(
        raw_rows=raw_rows,
        target_rows=target_rows,
        preserve_proof=PreserveProof(
            raw_sha256=raw_sha,
            preserved_raw_sha256=raw_sha,
            preserve_manifest_sha256="0" * 64,
            preserve_before_target_access=True,
        ),
    )
    return {
        "synthetic_only": True,
        "prediction_rows": len(raw_rows),
        "target_rows": len(target_rows),
        "recomputed_rows": len(recomputed),
        "target_sidecar_independence": "PASS",
        "post_preserve_correctness_recomputation": "PASS",
        "scientific_scoring_performed": False,
        "protected_evaluation_accessed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build H7 FORMAL-R3 non-result preidentity integrity diagnostics."
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("artifacts/formal_h7_r3/contract_design.json"),
    )
    parser.add_argument(
        "--runtime-binding",
        type=Path,
        default=Path("artifacts/formal_h7_r3/runtime_binding.json"),
    )
    parser.add_argument(
        "--prior-surface-inventory",
        type=Path,
        default=Path("artifacts/formal_h7_r3/prior_surface_inventory.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/formal_h7_r3/preidentity_ci"),
    )
    args = parser.parse_args()

    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

    contract = load_and_assert_r3_contract(args.contract)
    runtime = exact_runtime_observation(_pip_freeze())
    runtime_binding = _load_json(args.runtime_binding)
    inventory = _load_json(args.prior_surface_inventory)

    # Persist/print the outcome-independent runtime observation before the exact-binding
    # check. If the literal binding fails, the mismatch remains diagnosable without
    # exposing any protected evaluation material or scientific result.
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(args.output_dir / "runtime_observation.json", runtime)
    print("H7_R3_RUNTIME_OBSERVATION_JSON=" + json.dumps(runtime, sort_keys=True))

    validate_runtime_binding(runtime_binding, runtime)
    validate_prior_surface_inventory(inventory)
    sentinel = preidentity_sentinel(contract)
    raw_gate = _raw_gate_sentinel()

    assert_paths_available_no_clobber(
        [
            args.output_dir / "FORMAL_IDENTITY.json",
            args.output_dir / "STARTED.json",
            args.output_dir / "official_prediction_raw.jsonl",
            args.output_dir / "official_preserve_manifest.json",
            args.output_dir / "official_score.json",
        ]
    )

    _write_json(args.output_dir / "runtime_binding_verification.json", {"status": "PASS"})
    _write_json(args.output_dir / "preidentity_sentinel.json", sentinel)
    _write_json(args.output_dir / "raw_gate_sentinel.json", raw_gate)
    _write_json(
        args.output_dir / "prior_surface_inventory_verification.json",
        {
            "status": "PASS",
            "inventory_sha256": inventory["inventory_sha256"],
            "future_r3_evaluation_seed_values_recorded": False,
        },
    )

    print("H7_R3_PREIDENTITY_SENTINEL_JSON=" + json.dumps(sentinel, sort_keys=True))
    print("H7_R3_RAW_GATE_SENTINEL_JSON=" + json.dumps(raw_gate, sort_keys=True))


if __name__ == "__main__":
    main()
