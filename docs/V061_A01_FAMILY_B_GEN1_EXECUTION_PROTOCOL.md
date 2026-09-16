# V061 A01 Family-B Generation-1 — Exact One-Way Execution Package

Status: **prospective package under construction; execution NOT admitted**  
Owner: MAIN  
Identity: `a01-family-b-distributed-field-trace-gen1-v1`

This document fixes the execution/scoring semantics before any scientific output is exposed. It does not itself authorize STARTED, dispatch, acquisition, raw exposure, scoring, or identity consumption. A later Evidence Analyst handoff must admit the exact final package.

## Fixed input

The only scientific input is `research/v061_a01/family_b_gen1_execution_input.json`. The package binding fixes its exact bytes. Width is `4`, decay is `0.5`, confirmation is `+1`, contradiction is `-1`, and all discriminator/null IDs must match the already-bound Generation-1 readiness contract.

The scientific input is intentionally distinct from the readiness fixture. CI/readiness tests must never call the `acquire` or `score` paths and therefore must not expose the scientific result before STARTED.

## Fixed candidate gates

The frozen scorer evaluates these non-compensatory candidate gates:

1. `circulation_external_required`: internal replay leaves the local competition contribution unchanged while an external confirmation changes it.
2. `lineage_swap_anonymous_selectivity`: the effect follows anonymous physical Field overlap for left/right footprints rather than a declared semantic lineage.
3. `contradiction_correction`: a matched negative world return corrects the previously confirmed local contribution.
4. `f_only_transfer`: exporting/importing exactly `(eligibility, credit, decay)` preserves the learned competition effect.
5. `bounded_plurality`: two coexisting anonymous footprints can be separately affected by anonymous boundary overlap and later differentiated locally.
6. `dedup_checkpoint`: one evidence identity cannot be consumed twice, including after export/restore of the acquisition ledger.

Any false candidate gate, any forbidden privilege, binding failure, bound failure, or dedup failure is `FAIL`.

## Prospectively fixed matched null implementations

Three null identities are executed in the same package and recorded in raw evidence.

- Explicit eligibility/return-address null: reproduces the same fixed causal arithmetic while explicitly retaining a return-address interpretation. Its lookup privilege rank is `1`.
- Resource-matched recurrent causal-trace null: independently implements the same anonymous fixed-width recurrent update arithmetic without importing candidate state/classes. Its resource and lookup-privilege budget is matched to the candidate.
- Explicit latent-cause/belief-state null: reproduces the fixed causal signature while carrying an explicit latent-cause interpretation and an additional persistent-state/lookup privilege cost.

The scorer compares each fixed null's complete measurement signature to the candidate's complete measurement signature. A null is an eligible reducer only when it exactly reproduces the signature and every frozen resource/privilege counter is less than or equal to the candidate counter. The first eligible reducer in the fixed order `explicit_memory`, `recurrent_trace`, `belief_state` yields `REDUCED_EXPLANATION`.

If every candidate gate passes and no eligible reducer exists, the verdict is `PASS`.

No `INCONCLUSIVE` class is defined in this package. Invalid provenance/binding/raw-order conditions are not scientific scorer outcomes; the one-way workflow terminalizes them as `INVALID_EVIDENCE`/post-START failure according to the Analyst contingency contract.

## Resource counters

Candidate and null resource profiles freeze these counters:

- persistent scalar state;
- peak transient scalar state;
- external observation count;
- active-output budget;
- lookup-privilege rank.

Lower is no more privileged/resource-expensive. The recurrent null is intentionally allowed to be a strong null; naming an internal state "Field" does not exempt the candidate from reduction to anonymous recurrent causal memory.

## One-way lifecycle

The exact source must later receive a fresh Evidence Analyst admission before any lifecycle transition below.

1. Create an immutable annotated source freeze tag pointing to the admitted exact package.
2. Atomically create the dedicated STARTED control ref at exactly the same commit.
3. The workflow creates a durable owner claim, then an acquisition claim before evaluating the scientific input.
4. Acquisition writes raw evidence once.
5. Raw artifacts are committed to a recovery ref and annotated raw-evidence tag before any scoring read.
6. A separate verifier checks the preserved raw bundle and its digest.
7. Only the verified preserved raw artifact is passed to the frozen scorer.
8. The scored result is committed and annotated with a scored-evidence tag.
9. A failure after STARTED is terminal for this identity unless the already-frozen protocol explicitly says otherwise; this package defines no same-identity retry.

The workflow is triggered only by the dedicated STARTED control branch. Ordinary package commits and PR CI cannot trigger acquisition.

## Stop boundary

No package file, scientific input, mechanism, null implementation, resource counter, success criterion, scorer rule, threshold, or identity may be changed in response to Generation-1 output. Any such change requires return to Evidence Analyst and a distinct prospective scientific object.
