# FLY-0 descending modulation authority contract

Status: **NON_EVIDENTIARY / NONCANONICAL Forge prototype**.

This prototype implements the narrow next-step boundary proposed by External
Science Theory R20 without allocating SB003 or touching the current M1 critical
path.

The local controller remains responsible for fast sensorimotor progression.
High-level state can interact with it only through a versioned
`ModulationFrame`. The bounded v2 vocabulary remains deliberately small:

- `neutral`: permit the ordinary local closed-loop step;
- `hold`: commit a high-level hold while issuing no local action;
- `permit_side(left|right)`: permit the ordinary local action only when the
  local task-facing desired side matches the declared high-level side.

`permit_side` is intentionally a coarse permission gate, not a direct motor
command. A mismatch suppresses the local step; it does not inject an opposite
action, alter local controller internals, change topology, or introduce a
continuous gain/bias tuning parameter. A descending cut removes the high-level
gate and restores the ordinary local baseline.

Each frame binds a monotonic frame sequence, optional declared semantic side,
local sequence at issue time, bounded TTL, and the exact local checkpoint token
that supplied its provenance. Stale, expired, future-issued, wrong-provenance,
unknown-schema, invalid-side, and out-of-contract frames fail closed.

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
- `hold` changes behavior without direct local-controller commands;
- matching `permit_side` allows the local controller to produce its own
  ordinary action;
- mismatching `permit_side` vetoes that local step without issuing another
  motor command;
- a descending cut removes the high-level side veto and restores the local
  baseline;
- the existing local-feedback cut still blocks dependent continuation;
- checkpoint/replay is exact;
- failed frame/local operations do not partially advance bridge state.

This adds one inspectable directional modulation degree of freedom beyond the
v1 neutral/hold contract while deliberately avoiding richer policy semantics or
continuous tuning.

This is an engineering contract probe. It does **not** establish biological
fidelity/equivalence, topology necessity/superiority, resource or energy
efficiency, composition contribution, whole-system superiority, external
validity, scientific novelty, scientific credit, rich goal-conditioned
behavior, or SYSTEM_BUILD allocation.
