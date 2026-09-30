# Theory R27 — session-scoped causal frontier normalization

generation_id: `THEORY-20260930T132854+0900-R27-CAUSAL-FRONTIER-NORMALIZATION`
produced_at: `2026-09-30T13:28:54+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20260930T132854+0900`
authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
status: `INTEGRATION_DESIGN_PROPOSAL`
new_sparkbrain_scientific_result: `false`

## Freshness / role resolution

- role: `THEORY_SYNTHESIS_ARCHITECT`
- resolved slot: `13:30 JST`
- resolution source: `EARLY_GRACE`
- active Human Directive head: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- active-index blob: `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- directive delta from R26: `false`
- applicable directives read: HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001, HUMAN-20260928-002
- current Control authority: append-only R134
- current Evidence Analyst authority: R174
- Literature: R52
- Theory predecessor: R26
- Independent Audit: R14

Canonical science remains 35/35 terminal, active 0, queued 0, consumed FORMAL identities 8, scientific credit 0.

## Why a new integration revision is useful

Audit R14 isolated a composition defect: a wrapper could recreate the inner bounded-horizon object and thereby lose the pre-resynchronization watermark comparison. The focused repair at exact Forge head `fb42a34219e221ebb73140a56b743745a0febe37` is engineering-green and directly rejects same-session backward resynchronization without mutating WORLD/watermark/pending/epoch state. Control R134 records CI runs `36657549758` and `36665622816` as successful.

The immediate defect is repaired, but the failure class is broader: ordering and lineage are currently distributed across `world_session_id`, `world_cut_generation`, `recovery_epoch`, `outcome_sequence`, horizon floor, and consumed-anchor retention. A local inner object can be replaced while a stronger outer invariant remains necessary. R27 therefore proposes one durable frontier contract above replaceable horizon/dedupe implementations.

This is not a scientific mechanism. It is ordinary state-machine / WAL / fencing engineering.

## design_id

`ID-SB-FLY-CAUSAL-FRONTIER-001`

## target_capability

Prevent causal-time rollback, lineage relabeling, and hidden reset across horizon rotation, recovery-epoch transition, snapshot/rebase, checkpoint/restore, or implementation replacement while preserving bounded exact retention.

## component_map

1. **SessionCausalStamp**
   - fields: `world_session_id`, `world_cut_generation`, `recovery_epoch`, `outcome_sequence`
   - session mismatch is not an ordinary numeric ordering relation; it is an explicit namespace boundary.
   - `world_cut_generation` fences WORLD action tickets around an anchor cut.
   - `recovery_epoch` fences receipt/source lineage across successful resynchronization.
   - `outcome_sequence` is monotonic within one WORLD session and must never be reset by rotating an inner reconciler.

2. **Durable ReconciliationFrontier**
   - stores current session identity, cut generation, recovery epoch, accepted outcome watermark, exact-retention horizon floor, and observer-certainty state.
   - exists above replaceable bounded-horizon / exact-dedupe components.
   - an inner object may be recreated only from this frontier; it cannot become the source of the frontier's monotonic truth.

3. **Anchor coverage predicate**
   - valid same-session anchor requires matching session, current old recovery epoch, proposed epoch = current + 1, and covered outcome sequence >= current frontier watermark.
   - applied anchor atomically advances cut/epoch/frontier state or changes nothing.

4. **Lineage-bound issue stamps**
   - action tickets, source frames, execution journals, and validated receipts carry the relevant causal stamp components at issue/commit time.
   - a later layer may not re-stamp stale lineage with the current epoch/session merely to make it admissible.

5. **Bounded exact registry**
   - exact duplicate/conflict identity may remain window-bounded.
   - forgetting old exact identities never permits the durable frontier to move backward or reinterpret an old-session/old-epoch event as fresh progress.

## component_provenance / known reductions

- R25: bounded reconciliation horizon and unresolved causal gaps.
- R26: independently validated WORLD anchor and atomic recovery-epoch cut.
- Audit R14: concrete same-session backward-resync composition failure and required adversarial test.
- Forge repair `fb42a34219e221ebb73140a56b743745a0febe37`: current narrow monotonicity repair.
- Literature R52: stale-authority fencing and snapshot-boundary identity reduce to established distributed-systems engineering (Chubby/Raft-class primitives).
- A local single-writer WAL / transactional metadata row is an established replacement architecture and should remain the default simplification comparator.

No novelty credit is inherited from any of these components.

## interfaces_and_state_loop

`WORLD action ticket @ SessionCausalStamp`
→ WORLD commit ledger
→ typed ascending signal + source/journal stamp
→ receipt validation
→ frontier admission
→ bounded reconciliation observer
→ optional causal gap
→ validated WORLD cut/anchor
→ atomic frontier + recovery-epoch advance
→ next issued action/receipt lineage.

The durable frontier is the ordering authority for this engineering loop; the bounded inner gate supplies exact retained-history behavior, not global causal time.

## why_each_component_is_used

- session ID: makes legitimate sequence reset explicit instead of implicit.
- world cut generation: prevents pre-cut action tickets from committing after the causal cut.
- recovery epoch: prevents pre-resync receipt lineage from contaminating the post-resync observer.
- outcome watermark: prevents same-session history rollback.
- horizon floor: bounds what can still be exactly classified without pretending expired history is known.
- frontier-above-inner-gate placement: prevents the R14 class where recreating an inner object accidentally resets a stronger invariant.

## known_limitations

- The tuple is an engineering namespace/order contract, not a biological construct.
- A valid causal stamp does not prove a WORLD state is true; independent WORLD ledger / anchor provenance remains required.
- Bounded exact retention means sufficiently old identity conflicts may become unresolved rather than exactly classifiable.
- Multi-writer/distributed WORLD execution may require a stronger transaction/consensus substrate; R27 assumes the current bounded local/single-writer pilot unless SYSTEM_BUILD changes scope.
- Structured stamps add schema/versioning cost and should be removed if a simpler WAL transaction enforces the same invariants.

## acceptance_tests

1. Reproduce Audit R14 shape: reconcile through N, attempt same-session anchor M<N, require fail-closed with byte-equivalent observer/frontier/checkpoint state.
2. Rotate/recreate the bounded inner horizon from checkpoint while preserving the outer frontier; M<N must still be rejected.
3. After a valid rebase, an old-epoch receipt with sequence > new watermark must remain inadmissible.
4. Re-stamping old source/journal content with a current epoch/cut token must fail provenance validation.
5. Explicit new `world_session_id` may start a fresh sequence namespace; receipts/actions from the prior session remain inadmissible.
6. Crash injection between WORLD cut, frontier update, recovery-epoch advance, anchor registry update and finalization restores either the complete pre-state or complete post-state, never a mixed stamp.
7. Checkpoint restore rejects internally inconsistent tuples (for example lower outcome watermark paired with a later recovery epoch without an accepted session transition).
8. Long-run exact-memory usage remains bounded by configured windows while frontier metadata remains O(1).
9. Duplicate identical stamp/identity is idempotent inside the retained window; same identity with conflicting causal stamp fails closed.

## suggested component-replacement tests

- Replace the custom frontier layer with a local SQLite/WAL single-writer transaction containing one metadata row:
  `world_session_id, world_cut_generation, recovery_epoch, outcome_watermark, horizon_floor, observer_certainty`.
- Store retained receipt identities under a composite unique key and compare behavior under the same adversarial suite.
- If SQLite/WAL satisfies the contract with less bespoke state and comparable deterministic replay, prefer it.

## suggested interaction-ablation tests

- remove session identity: test ambiguity of legitimate sequence reset versus rollback;
- remove world cut generation: test action commit after snapshot cut;
- remove recovery epoch: test late old-lineage receipt after rebase;
- keep all fields but place watermark only inside the replaceable inner horizon: require the R14-style discriminator to fail this ablation;
- remove horizon floor while bounding identity memory: test whether expired identities become falsely fresh.

These are engineering interaction tests, not scientific ablations.

## alternative established architecture

Local SQLite/WAL, single-writer WORLD transaction boundary, versioned snapshot metadata, composite receipt identity, and one transactional frontier row. No custom distributed protocol is required for the bounded local pilot if this alternative meets the same invariants.

## scientific_claims_explicitly_not_made

R27 does not establish biological fidelity/equivalence, fly-topology necessity or superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity, emergence, or scientific novelty. Build/Forge observations remain NON_EVIDENTIARY/NONCANONICAL and scientific credit is 0.

## build_value_if_no_novelty_exists

A single explicit causal frontier can reduce cross-layer reset bugs, make checkpoint/replay invariants inspectable, simplify long-running acceptance, and let bounded horizon/dedupe implementations be replaced without redefining causal time.

## suggested SYSTEM_BUILD scope

Optional SB003 Milestone B/C hardening only after fresh Evidence Analyst reconciliation of the R14 repair and any scoped composed acceptance it requires. Do not make this an M1 gate, do not change SB003 activation conditions, and do not create a mandatory review gate.

## independence from current MAIN unknown outcomes

The proposal depends only on bounded engineering invariants and current non-evidentiary Forge state. It does not depend on M1-002 PR success, future MAIN behavior, or any unknown scientific result.

## status

`INTEGRATION_DESIGN_PROPOSAL`

## P0 note

P0 remains OPEN / root cause UNKNOWN under Control R134. The prior composed long-running R26 focused-test publication did not produce new acceptance evidence after five pre-GitHub refusals; R27 does not treat it as accepted. This publication is a separate Theory-stream persistence purpose under the shared five-attempt ceiling.
