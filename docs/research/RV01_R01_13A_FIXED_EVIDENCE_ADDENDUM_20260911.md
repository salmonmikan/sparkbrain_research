# RV01 R01-13A fixed-evidence addendum — 2026-09-11

Status: **APPEND_ONLY_EVIDENCE_PRESERVATION / NO SCIENTIFIC RERUN**

This addendum resolves reviewability/reporting issues without rerunning R01-13A and without changing its fixed development raw evidence.

## Raw evidence retained in-repository

The successful development workflow artifact from run `34233875594` was downloaded and verified against the already recorded immutable hashes before being copied into the repository:

- artifact ID: `10059084120`
- artifact ZIP SHA-256: `84f393e25af3de848cf517872592885649801be2e0a3d3e98ccbc9f14a6c3bd5`
- retained raw path: `artifacts/research/rv01/r01_13/development_result.json`
- retained raw SHA-256: `1ab43a8950be572b163e7bba4950b23d5258933e5463dc3d944f41eaea2adf60`
- execution source SHA: `241669c92a0fd93b1f98ffe5e5dcaf8fd97c4de2`

No capability code was executed during preservation. The repository test suite now checks the retained file hash against the manifest so future drift fails CI.

## Runtime identity

The fixed evidence is bound to the runtime that reproduced its registered semantic/file hashes:

- implementation: `CPython`
- version: `3.11.15`

The manifest now explicitly records `portable_reexecution_claim=false`. The project may support newer Python versions generally, but this historical fixed artifact does not claim byte/semantic-hash portability across interpreter versions. In particular, a later interpreter with different low-order floating-point summation behavior must not be used to regenerate or silently replace this artifact.

## Near-zero world-count reporting

The historical fixed raw artifact contains a shared-prefix breadth-matched subtraction of approximately `-1.11e-16`. The scientific interpretation already treated this as floating-point roundoff and the family means tie at reported precision.

Future reporting code now classifies retention deltas with an explicit absolute tolerance of `1e-12` and mutually exclusive positive/tied/negative categories. This reporting correction does **not** rewrite the historical raw JSON, suite hash, or evidence digest. It prevents later reports from counting numerical roundoff as a scientific negative world.

## Scientific boundary unchanged

The accepted R01-13A development conclusion is unchanged:

- the raw R01-12-style retention signature reproduced;
- equal-event matching was non-specific because it also created a Field advantage in the disjoint reference family;
- equal distinct-candidate breadth collapsed the registered retention gap;
- the structured-over-activation / broader-candidate-availability null is sufficient for the registered retention difference;
- R01-13B state-locus admission remains **NOT ADMITTED**;
- R01-13 held-out capability remains **CLOSED / NOT EXECUTED**.

This addendum improves preservation and reproducibility metadata only. It does not reopen the consumed/fixed scientific boundary.
