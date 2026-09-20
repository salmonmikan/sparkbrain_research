# EXPLORATORY / NON_EVIDENTIARY — v0.5 pre-semantic function-transfer discovery

## Prospective contract

- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- candidate: `CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01`
- cycle: `1/3`
- claim_ceiling: `MECHANISM`
- preformal_eligible_pre_outcome: `true`
- evidentiary_status: `NON_EVIDENTIARY`
- stable_base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260920T160240+0900-R16-3D7A91C4@eea87c0e67807605c8fdd10408650da4192fb06b`
- main_generation_observed: `MAIN-20260920T161602+0900-PRIMARY-FUNNEL21-HOLD-6D2B8C41`

Question: can an anonymous Assembly formed before any semantic outcome association later acquire a function from one member of its pre-existing cluster and transfer that function to another member that was never outcome-labeled and is below direct similarity threshold to the labeled exemplar?

This is a theory-backward test of pre-semantic activity acquiring later function. It is independent of MAIN because MAIN has no active scientific object under the current Analyst allocation, and it does not reopen any terminal candidate or H7.

## Fixed synthetic patterns

Use three development-only `ActivityPattern` objects with equal timing bins `(0, 1, 2, 3)`:

- prototype A ordered units `(1, 2, 3, 4)`;
- labeled exemplar B ordered units `(1, 1, 2, 3)`;
- unlabeled transfer target C ordered units `(1, 1, 3, 4)`.

Under the repository's existing `pattern_similarity`, the fixed construction is expected to satisfy A↔B and A↔C at or above the default Assembly threshold `0.66`, while B↔C is below threshold. These similarities are construction constraints, not scientific outcomes.

## Procedure

1. Create one default `TemporalAssemblyMemory` with `mature_episodes=3`.
2. Present A under three distinct synthetic episode IDs to create a mature anonymous Assembly before any semantic association.
3. Present B with `learn=false`; require it to activate the mature Assembly. Attach exactly one synthetic future label `future-X` to B's activation using `AssemblyPredictor.observe`.
4. Present C with `learn=false`; inspect whether it activates the same Assembly and whether `AssemblyPredictor.predict` emits `future-X`.
5. Compare against two fixed ordinary reductions:
   - direct labeled-exemplar nearest-neighbor: B→C using the same `pattern_similarity` and threshold;
   - fixed pre-semantic prototype-cluster lookup: A→C using the same threshold plus the same single label attached to the cluster identity.

## Prospectively fixed terminals

- `NO_FUNCTION_TRANSFER`: C does not produce `future-X`; reject the mechanism object.
- `DIRECT_EXEMPLAR_EXPLAINS_TRANSFER`: C produces `future-X` and B→C is above threshold; reduce to ordinary labeled-exemplar similarity and reject.
- `CLUSTER_LOOKUP_EXPLAINS_TRANSFER`: C produces `future-X`, B→C is below threshold, but fixed A-prototype clustering plus label lookup reproduces the transfer; reduce to ordinary pre-semantic clustering + lookup and reject.
- `TRANSFER_SURVIVES_FIXED_ORDINARY_REDUCTIONS`: C produces `future-X` while both fixed ordinary reductions fail; continue only to fresh Analyst review, with no automatic PRE_FORMAL action.

No thresholds, patterns, labels, comparator rules, or terminals may be changed after observing the result. Stop after the first mapped terminal; no rescue cycle in this run.
