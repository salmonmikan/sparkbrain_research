#!/usr/bin/env python3
"""Production verifier for A01 MD-002 P4 candidate-001 preserved raw artifacts.

The historical verifier remains available as a compatibility layer for its
existing unit tests. The executable verifier used by the one-shot workflow adds
two independent fail-closed derivations before scoring:

1. active lineage rows are re-derived from retained ledger proposal validity at
   the bound measurement timestamps;
2. changed path IDs are recomputed from retained pre/post path reliability.

This module is read-only. It never imports acquisition or scoring entrypoints.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

try:
    from scripts import _verify_v061_a01_md002_p4_candidate_001_artifacts_base as _base
except ModuleNotFoundError:  # direct `python scripts/...py` execution
    import _verify_v061_a01_md002_p4_candidate_001_artifacts_base as _base


# Compatibility exports for the pre-existing structural-verifier unit tests.
CANDIDATE_ID = _base.CANDIDATE_ID
CONTRACT_SCHEMA = _base.CONTRACT_SCHEMA
EXPECTED_EXECUTION_IDS = _base.EXPECTED_EXECUTION_IDS
EXPECTED_PYTHON = _base.EXPECTED_PYTHON
RAW_SCHEMA = _base.RAW_SCHEMA
RUNTIME_SCHEMA = _base.RUNTIME_SCHEMA
_canonical_sha256 = _base._canonical_sha256
verify_raw_bundle = _base.verify_raw_bundle


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _number(value: Any, *, name: str) -> float:
    _require(
        not isinstance(value, bool) and isinstance(value, (int, float)),
        f"{name} must be numeric",
    )
    result = float(value)
    _require(math.isfinite(result), f"{name} must be finite")
    return result


def _active_lineage_trace_row(
    trace: Any,
    *,
    phase: str,
    execution_id: str,
) -> dict[str, Any]:
    _require(isinstance(trace, list), f"{execution_id}: retained trace missing")
    matches = [
        item
        for item in trace
        if isinstance(item, dict)
        and item.get("type") == "md002-p4-active-lineages"
        and item.get("phase") == phase
    ]
    _require(
        len(matches) == 1,
        f"{execution_id}: active-lineage {phase} cardinality mismatch",
    )
    return matches[0]


def _ledger_active_proposal_ids(
    row: dict[str, Any],
    *,
    at_ms: float,
    execution_id: str,
    phase: str,
) -> list[str]:
    ledger_state = row.get("ledger_state")
    _require(isinstance(ledger_state, dict), f"{execution_id}: ledger missing")
    proposals = ledger_state.get("proposals")
    _require(
        isinstance(proposals, dict),
        f"{execution_id}: retained ledger proposals missing",
    )

    active: list[str] = []
    for proposal_key, proposal in sorted(proposals.items(), key=lambda item: str(item[0])):
        _require(
            isinstance(proposal_key, str) and proposal_key,
            f"{execution_id}: retained ledger proposal key invalid",
        )
        _require(
            isinstance(proposal, dict),
            f"{execution_id}: retained ledger proposal row invalid: {proposal_key}",
        )
        proposal_id = proposal.get("proposal_id")
        _require(
            proposal_id == proposal_key,
            f"{execution_id}: retained ledger proposal identity mismatch: {proposal_key}",
        )
        created_at_ms = _number(
            proposal.get("created_at_ms"),
            name=f"{execution_id}: {proposal_key} created_at_ms",
        )
        valid_until_ms = _number(
            proposal.get("valid_until_ms"),
            name=f"{execution_id}: {proposal_key} valid_until_ms",
        )
        _require(
            created_at_ms <= valid_until_ms,
            f"{execution_id}: retained ledger proposal validity inverted: {proposal_key}",
        )
        if created_at_ms <= at_ms <= valid_until_ms:
            active.append(proposal_key)

    _require(
        active,
        f"{execution_id}: no runtime-active proposals re-derived for {phase}",
    )
    return active


def _verify_active_lineages_against_ledger(
    row: dict[str, Any],
    *,
    execution_id: str,
) -> None:
    condition_spec = row.get("condition_spec")
    _require(
        isinstance(condition_spec, dict),
        f"{execution_id}: condition spec missing",
    )
    if condition_spec.get("boundary_mode") != "merged":
        return

    trace = row.get("retained_runtime_trace")
    for phase in ("before", "after"):
        trace_row = _active_lineage_trace_row(
            trace,
            phase=phase,
            execution_id=execution_id,
        )
        _require(
            trace_row.get("derivation") == "ledger-proposal-temporal-validity-v1",
            f"{execution_id}: active-lineage {phase} derivation mismatch",
        )
        measurement_time_ms = _number(
            trace_row.get("measurement_time_ms"),
            name=f"{execution_id}: active-lineage {phase} measurement_time_ms",
        )
        proposal_ids = trace_row.get("proposal_ids")
        _require(
            isinstance(proposal_ids, list)
            and all(isinstance(value, str) and value for value in proposal_ids),
            f"{execution_id}: active-lineage {phase} proposal IDs invalid",
        )
        _require(
            len(proposal_ids) == len(set(proposal_ids)),
            f"{execution_id}: active-lineage {phase} proposal IDs duplicated",
        )
        independently_derived = _ledger_active_proposal_ids(
            row,
            at_ms=measurement_time_ms,
            execution_id=execution_id,
            phase=phase,
        )
        _require(
            proposal_ids == independently_derived,
            f"{execution_id}: active-lineage {phase} differs from retained ledger",
        )


def _path_reliability(
    row: dict[str, Any],
    *,
    phase: str,
    execution_id: str,
) -> dict[str, float]:
    state = row.get(phase)
    _require(isinstance(state, dict), f"{execution_id}: {phase} state missing")
    values = state.get("path_reliability")
    _require(
        isinstance(values, dict),
        f"{execution_id}: {phase} path reliability missing",
    )
    result: dict[str, float] = {}
    for path_id, value in values.items():
        _require(
            isinstance(path_id, str) and path_id,
            f"{execution_id}: {phase} path ID invalid",
        )
        result[path_id] = _number(
            value,
            name=f"{execution_id}: {phase} reliability {path_id}",
        )
    return result


def _verify_changed_paths_from_states(
    row: dict[str, Any],
    *,
    execution_id: str,
) -> None:
    before = _path_reliability(row, phase="pre", execution_id=execution_id)
    after = _path_reliability(row, phase="post", execution_id=execution_id)
    independently_derived = [
        path_id
        for path_id in sorted(set(before) | set(after))
        if before.get(path_id) != after.get(path_id)
    ]

    changed = row.get("changed_path_ids")
    _require(
        isinstance(changed, list)
        and all(isinstance(value, str) and value for value in changed),
        f"{execution_id}: changed path IDs invalid",
    )
    _require(
        len(changed) == len(set(changed)),
        f"{execution_id}: changed path IDs duplicated",
    )
    _require(
        changed == independently_derived,
        f"{execution_id}: changed path IDs disagree with retained pre/post states",
    )


def _verify_independent_derivations(raw: Any) -> None:
    _require(isinstance(raw, dict), "raw artifact must be an object")
    observations = raw.get("observations")
    _require(isinstance(observations, list), "raw observations must be a list")
    _require(
        len(observations) == len(EXPECTED_EXECUTION_IDS),
        "raw observation count mismatch",
    )

    seen: set[str] = set()
    for row in observations:
        _require(isinstance(row, dict), "raw observation row invalid")
        execution_id = row.get("condition_id")
        _require(
            isinstance(execution_id, str) and execution_id in EXPECTED_EXECUTION_IDS,
            "raw condition ID invalid",
        )
        _require(execution_id not in seen, f"duplicate raw condition ID: {execution_id}")
        seen.add(execution_id)
        _verify_changed_paths_from_states(row, execution_id=execution_id)
        _verify_active_lineages_against_ledger(row, execution_id=execution_id)

    _require(seen == set(EXPECTED_EXECUTION_IDS), "raw condition set mismatch")


def verify_preserved_raw_bundle(
    root: Path,
    *,
    expected_source_sha: str,
    expected_run_id: str,
    expected_owner_claim: str,
) -> None:
    """Run structural verification plus independent scientific re-derivations."""

    _base.verify_raw_bundle(
        root,
        expected_source_sha=expected_source_sha,
        expected_run_id=expected_run_id,
        expected_owner_claim=expected_owner_claim,
    )
    raw = json.loads((root / "raw.json").read_text())
    _verify_independent_derivations(raw)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--expected-source-sha", required=True)
    parser.add_argument("--expected-run-id", required=True)
    parser.add_argument("--expected-owner-claim", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    verify_preserved_raw_bundle(
        Path(args.root),
        expected_source_sha=str(args.expected_source_sha),
        expected_run_id=str(args.expected_run_id),
        expected_owner_claim=str(args.expected_owner_claim),
    )
    print("P4 raw artifact bundle verification: PASS")


if __name__ == "__main__":
    main()
