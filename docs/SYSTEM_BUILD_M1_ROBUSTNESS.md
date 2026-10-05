# Integrated Prototype Milestone 1 — post-integration robustness harness

Build identity: `BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS`

Authority: Evidence Analyst R163, retained by R164.

Status: bounded NON_EVIDENTIARY SYSTEM_BUILD acceptance harness. It does not alter M1 runtime
algorithms, thresholds, routing topology, public fields or resource ceilings.

## Fixed acceptance surface

`tests/test_system_build_m1_robustness.py` verifies the prospectively fixed families:

1. one nominal 64-cycle run, checking sequence, pending state, event/receipt ledgers, routed
   evidence and trace identity after every commit;
2. exact checkpoint continuation from cutpoints 1, 8, 31 and 63 through cycle 64, including each
   action, outcome, revision, integrated trace and state hash;
3. every existing session/component fault point at fixed early, middle and late positions, with
   exact rollback followed by equality of the next healthy cycle against a control loaded from the
   same checkpoint;
4. exact duplicate receipt redelivery, conflicting receipt-ID reuse, duplicate event-ID reuse,
   pending-event overlap and mismatched pending receipt paths, each with no-write/idempotence and
   deterministic continuation checks.

The harness performs exactly 267 successful committed cycles across the complete acceptance
surface, below the fixed aggregate ceiling of 512. Fault attempts and rejected identity paths
commit zero cycles. Each individual timeline remains within the existing 64-cycle world ceiling.

## Verification

```bash
python -m pytest -q tests/test_system_build_m1_robustness.py
python -m pytest -q tests/test_system_build*.py
python scripts/local_readiness_check.py
python -m pytest -q
python -m ruff check .
python scripts/validate_bundle.py
```

## Claim boundary

- built: true on the dedicated SYSTEM_BUILD branch;
- bounded functionally verified: only after the commands above pass at the exact branch head;
- comparatively supported: false;
- composition contribution: not established;
- scientifically novel: false;
- scientific credit: 0.

This harness does not evaluate a comparator, real task, biological fidelity, energy efficiency or
scientific hypothesis. FLY-0, Theory inputs, A01, RV02, H9/C07 and consumed scientific identities
are not dependencies and are not executed.
