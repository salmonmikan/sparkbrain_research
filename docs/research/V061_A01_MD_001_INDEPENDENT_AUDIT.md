# A01-MD-001 independent audit addendum — 2026-09-09

## Scope and disposition

Review-only addendum. This document does not rerun, rescore, tune, or modify A01-MD-001, candidate-003, the bound protocol, the runtime, or preserved result bytes. Historical emitted verdicts remain unchanged in the raw artifact. Review disposition: **not ready for scientific completion approval**. This is a harness-validity and coverage finding, not evidence that the A01 mechanism is false.

Reviewed report HEAD: `19ffee619c065c33baf58f4c3232ab64749d5682`.
Executed source: `e5882c060bf3029415d49c22d9130d59ecbadd00`.
Mechanism-discrimination source content is identical at those two commits (blob `10b4071288974a8d896b766a6bb64fdadeadfceb`).
Base mechanism: `df18a3940a4d3385fa9debcd74b8014dea6238fa`.

## Evidence integrity

The preserved raw result was retrieved at reviewed HEAD and its actual bytes independently checked with SHA-256:
`361cc46b60ad9f09be7d71e69ecaabd82e9dada828dc64da46772c110e9f18f6`.
This matches the preservation manifest. No capability execution was performed. Internal digest was read, not independently recomputed.

The raw P5 persistent serialized-byte value is 155 for both candidate and N1, consistent with the report correction.

## Findings

### A01-AUD-01 — P2 intervention is confounded (blocking)

At `src/sparkbrain/v061_a01/mechanism_discrimination.py:567-579`, the two arms change `causal_path` and `causal_target`, while both use the same `PRIOR_TARGET`. In `_run_world_arm`, `relation_id` is an event prefix and reported label, not a changed world relation.

The preserved raw arms corroborate this: both use port `port:p`, target `world:x`, link `link:fe41885542f878c422cdc44f`, the same prior relation and the same relation reliability. Only recovered path and subsequent local support differ.

This demonstrates a credited-lineage swap with a later proposal-confidence change, but not the anonymous-world-relation intervention required by protocol section 11. The report's statement that only the anonymous world relation changed is not supported. Preserve the emitted P2 label as historical output; do not accept it as completion of registered P2.

### A01-AUD-02 — R-only transplant has no separately executed transplanted arm (blocking)

In `_return_address_attribution_cross`, baseline and donor both run external attribution before scoring. The trial constructs pre-attribution L/C hashes, then takes `selected_lineage_after` directly from donor post-attribution competition (`mechanism_discrimination.py:934-942`).

No third mechanism state is executed with baseline state and transplanted donor R. The observed donor outcome includes the donor's L update. This cannot validate the advertised isolated transplant, although the code's exact-parent routing logic and separate L-only transfer remain useful evidence. Corrected prospective testing must bind actual intervention state, execute it, and capture before/after hashes for each phase.

The F-only test is also explicitly metadata-scoped: it changes a Field-origin hash, not a full Field dynamics state. Its null outcome must not be generalized beyond A01's declared metadata interface.

### A01-AUD-03 — P4 merged-ancestry boundary is untested (blocking)

Protocol section 13 explicitly includes several candidate lineages irreducibly merged into one BoundaryEvent ancestry, with failure if later useful differentiation is prevented.

All P4 trials choose one causal lineage and create a singleton proposal boundary. Early/later active-lineage tuples are supplied as constants (`mechanism_discrimination.py:1060-1073`), not measured from a continuing Field execution. The observed two co-maximal proposal confidences and single-path support differentiation support a narrower component case, not unconditional completion of bounded-ambiguity continuation.

P5's unseen-lineage combination does exercise plural support updates, but is not a substitute for the registered P4 continuation case.

### A01-AUD-04 — Full P5 completion exceeds comparator coverage (blocking for full-stage claim)

The harness constructs N1 only. Protocol section 15 explicitly requires a resource-matched recurrent causal-trace comparator. No N3 outcome is present in the preserved result. N1 support-table reproduction is useful reduction evidence, but must be reported as N1-scoped rather than completion of the full registered P5 stage.

Several dynamic/resource dimensions are declarative rather than independently measured: `_dynamic_outcome` assigns one-step latency and local update locus; both arms share resolution-derived counts and boundary signatures; transient peak units are fixed to 6. Therefore the equality of these fields is not an independent measurement of arbitrary dynamic equivalence.

Sharing exact-parent provenance and anonymous classification with N1 is explicitly allowed by the protocol; that sharing itself is not a defect. The weakness is presenting common or hardcoded metadata and incomplete challenge execution as independent full-stage evidence.

### A01-AUD-05 — Preservation and handoff hazards (non-mechanistic)

The retained workflow still allows automatic pushes on the discrimination source branch and workflow dispatch to generate the same A01-MD-001 identity with another source SHA. Future maintenance must not trigger such a rerun. A separately reviewed guard or retired runner is appropriate; this addendum does not alter it.

The checksum sidecar names the original workflow output path rather than the preserved `raw_result.json` path. The bytes verify independently, but the packaged `sha256sum -c` instruction is broken.

Canonical A01 status/ledger synchronization is a separate documentation task. Any update must include the limitations above rather than copy historical SUPPORTED labels as accepted review conclusions.

## What can be retained

- P1's narrow component-level observation: independently registered exact-parent external match follows supplied causal provenance; contradiction corrects support; supplied absence/replay cases show no positive support leakage.
- Later local proposal confidences change when the explicit path-support counters change.
- L-only serialized-state transfer carries the support bias.
- N1's explicit path-local support rule reproduces the observed component outputs.
- No Field-emergence claim is justified.

These observations do not establish complete live Field causal-lineage discrimination, every registered P1-P5 condition, or universal dynamic equivalence.

## Safe next steps

1. Keep raw evidence, hashes, executed source and emitted labels immutable.
2. Record review caveats in the canonical status and ledger, with original versus reviewed interpretations separated.
3. Use a new bound diagnostic identity for any corrected P2 intervention, actual R transplant, merged-ancestry P4 continuation or N3 comparison; never silently repair A01-MD-001 after observation.
4. Do not merge PR24 as scientifically complete until scope and preservation hazards are resolved.

The seven existing unresolved PR24 review threads were read. Their P2, R-only, merged-ancestry P4 and N3 findings were independently checked against source and the bound protocol, not merely accepted on authority. No external review approval, merge, seal, runtime edit or experiment execution was performed by this audit.
