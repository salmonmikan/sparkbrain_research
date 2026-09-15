#!/usr/bin/env python3
"""Compatibility helper surface for the repaired P4 candidate.

The original candidate-001 CLI was superseded prospectively before STARTED
because its six-assay contract had three P1 integrity defects. The exact
execute-once workflow now uses ``run_v061_a01_md002_p4_candidate_001_v3.py``.

This module intentionally exposes only deterministic construction helpers used
by the repaired runner. It is not an acquisition/scoring entrypoint.
"""

from __future__ import annotations

from _run_v061_a01_md002_p4_candidate_001_legacy_core import (
    AMBIGUOUS,
    CANDIDATE_ID,
    EN_BLOC,
    INVALID,
    NO_EFFECT,
    PREMATURE_COLLAPSE,
    SUPPORTED,
    A01TransientCreditBridge,
    _boundaries,
    _changed_paths,
    _competition,
    _expectation,
    _lineage_proposals,
    _path_map,
    _prior_consistency,
    _pulse,
    _reliabilities,
    _setup_for_condition,
    _write_json,
)

__all__ = [
    "AMBIGUOUS",
    "CANDIDATE_ID",
    "EN_BLOC",
    "INVALID",
    "NO_EFFECT",
    "PREMATURE_COLLAPSE",
    "SUPPORTED",
    "A01TransientCreditBridge",
    "_boundaries",
    "_changed_paths",
    "_competition",
    "_expectation",
    "_lineage_proposals",
    "_path_map",
    "_prior_consistency",
    "_pulse",
    "_reliabilities",
    "_setup_for_condition",
    "_write_json",
]


def main() -> None:
    raise SystemExit(
        "superseded pre-STARTED P4 entrypoint; use "
        "scripts/run_v061_a01_md002_p4_candidate_001_v3.py"
    )


if __name__ == "__main__":
    main()
