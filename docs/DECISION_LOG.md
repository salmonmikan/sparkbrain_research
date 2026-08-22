# Decision Log

## D-001 — Treat SparkBrain as brain-inspired, not a brain replica

**Decision:** Until anatomical and neurophysiological validation exists, describe the project as a brain-inspired dynamic cognitive system / artificial brain experiment environment, not a reproduction of the human brain.

**Reason:** Functional similarity does not establish biological equivalence.

## D-002 — Project code name is SparkBrain; theory name remains provisional

**Decision:** Use `SparkBrain` for repository/package identity. Do not publish `SFA` as the final acronym.

**Reason:** Naming conflicts and novelty boundaries have not been fully searched.

## D-003 — Reference engine precedes spiking implementation

**Decision:** Build and freeze rate-based behavior before Norse/snnTorch/Nengo/Lava.

**Reason:** Otherwise theory failure, training failure, and substrate failure cannot be separated.

## D-004 — Use a priority event queue, not one coroutine per Spark

**Decision:** Model logical concurrency using deterministic discrete events.

**Reason:** Thousands of Python tasks would obscure the algorithm and add scheduler overhead without providing physical parallelism.

## D-005 — Coalition is an evidence-bearing object

**Decision:** Coalition membership includes evidence identities/provenance, not only active processors.

**Reason:** Revision and interpretability require distinguishing independent support, duplicated propagation, and contradiction.

## D-006 — No-ignition is valid

**Decision:** The system may have no newly valid belief even when an output is requested.

**Reason:** Forced selection conflates uncertainty with belief.

## D-007 — Losers decay; they are not cleared by default

**Decision:** Standard architecture uses winner-take-most. Hard-WTA is an ablation.

**Reason:** Hypothesis recovery is a central falsifiable mechanism.

## D-008 — Current Phase-0 weights are hand-authored

**Decision:** Preserve them as a software validation fixture only.

**Reason:** They cannot support generalization or learning claims.

## D-009 — Algorithmic sparsity and energy efficiency are separate claims

**Decision:** Report active nodes/edges first. Reserve energy claims for measured runtime/hardware.

**Reason:** Sparse dynamic Python or GPU execution can be slower despite less semantic work.

## D-010 — Codex tasks require acceptance tests and raw artifacts

**Decision:** No task is complete because code exists. It must meet explicit tests, outputs, and documentation criteria.

**Reason:** The project combines research and software; unverifiable output is not useful.
