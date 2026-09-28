# FLY-0 descending modulation authority contract

Status: **NON_EVIDENTIARY / NONCANONICAL Forge prototype**.

This prototype implements the narrow next-step boundary proposed by External
Science Theory R20 without allocating SB003 or touching the current M1 critical
path.

The local controller remains responsible for fast sensorimotor progression.
High-level state can interact with it only through a versioned
`ModulationFrame`.  The first bounded vocabulary is deliberately small:

- `neutral`: permit the ordinary local closed-loop step;
- `hold`: commit a high-level hold while issuing no local action.

Each frame binds a monotonic frame sequence, local sequence at issue time,
bounded TTL, and the exact local checkpoint token that supplied its provenance.
Stale, expired, future-issued, wrong-provenance, unknown-schema, and out-of-
contract frames fail closed.

The bridge checkpoint binds the modulation contract and fingerprint together
with the complete local-loop checkpoint. Restore is transactional: if either
the bridge layer or local layer fails validation, both are returned to their
pre-restore state.

## Bounded diagnostics

The same frame interface is exercised against:

1. structured fly-inspired topology;
2. semantic-surface-preserving degree rewiring;
3. semantic-surface-preserving random sparse topology;
4. ordinary reactive reference.

The probe requires:

- neutral modulation reproduces the existing local baseline;
- a `hold` frame changes behavior without direct local-controller commands;
- a descending cut removes only the high-level hold and restores the local
  baseline;
- the existing local-feedback cut still blocks dependent continuation;
- checkpoint/replay is exact;
- failed frame/local operations do not partially advance bridge state.

This is an engineering contract probe. It does **not** establish biological
fidelity/equivalence, topology necessity/superiority, resource or energy
efficiency, composition contribution, whole-system superiority, external
validity, scientific novelty, scientific credit, or SYSTEM_BUILD allocation.
