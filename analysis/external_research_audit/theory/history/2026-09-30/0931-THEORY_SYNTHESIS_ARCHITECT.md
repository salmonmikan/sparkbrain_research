# Theory R26 — proven resynchronization anchor and atomic recovery-epoch cut

generation_id: `THEORY-20260930T093150+0900-R26-PROVEN-RESYNC-ANCHOR-ATOMIC-EPOCH-CUT`
status: `INTEGRATION_DESIGN_PROPOSAL`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

## Role / freshness

- selected role: `THEORY_SYNTHESIS_ARCHITECT`
- resolved slot: `09:30 JST`
- directive index: `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- active-index blob: `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- directive delta from R25: `false`
- current Control append-only authority read: `R132`
- current Evidence Analyst authority read: `R173`
- current Literature authority read: `R52`
- current Independent Audit authority read: `R13`
- durable prior Theory authority: `R25`

Applicable Human Directives read: `HUMAN-20260925-002`, `HUMAN-20260927-002`, `HUMAN-20260928-001`, `HUMAN-20260928-002`.

## Design record

### design_id
`ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001`

### revision
`11`

### proposal
`PROVEN_RESYNCHRONIZATION_ANCHOR_AND_ATOMIC_RECOVERY_EPOCH_CUT`

### target_capability

Recover observer certainty after an explicit R25 bounded causal gap without accepting a caller-self-attested WORLD position, without allowing pre-resynchronization execution/receipt lineage to contaminate the post-resynchronization observer, and without pretending that a valid new anchor reconstructs lost causal history.

### Current observations that motivate the design

1. R25 bounded-horizon recovery is now engineering-green at exact validated head `b21a9495e207ab7af66b021968985993c4428c31` / CI `36615136680`. It correctly retains bounded exact identity, makes out-of-horizon uncertainty explicit, preserves gap state across checkpoint/restore, and only clears `DEGRADED_CAUSAL_GAP` through explicit resynchronization.
2. Its current `resynchronize(authoritative_world_position, outcome_sequence)` accepts caller-supplied WORLD state as authoritative. That is a trust boundary, not proof of WORLD truth.
3. The recovery-epoch fence is engineering-green at exact validated head `4c5147a5c39b6c5da8320226de3ddc75d30de6b1` / CI `36620923633`. It prevents issue-time old-epoch receipt lineage from mutating post-resync state and preserves the fence across checkpoint/restore. It remains NON_EVIDENTIARY/NONCANONICAL and pending Analyst reconciliation.
4. The separate resync CAS guard source `06e39638cab4143185803bcae0c8ea9921479764` is source-only CI-green but its focused semantic test could not be durably published after five pre-GitHub refusals. It remains UNVERIFIED and is not a handoff.
5. Evidence Analyst R173 still holds long-running receipt reconciliation at `HOLD_FOR_BOUNDED_HORIZON_RECOVERY_AND_SCOPED_COMPOSED_ACCEPTANCE`. R26 does not bypass or expand that authority.

## component_map

### 1. Bounded reconciliation horizon
Provenance: R25 Forge exact tested head `b21a9495e207ab7af66b021968985993c4428c31`.

Function: bounded exact receipt/proof retention, monotonic horizon, explicit causal-gap state, checkpoint/replay.

Reduction: ordinary bounded event-log / execution-journal / watermark / idempotent-consumer engineering.

### 2. Recovery-epoch fence
Provenance: Forge exact tested head `4c5147a5c39b6c5da8320226de3ddc75d30de6b1`.

Function: stamp source/execution lineage with a recovery epoch and reject delayed retired-epoch receipts after a rebase.

Reduction: ordinary generation/fencing-token/log-rotation engineering.

Known limitation: cooperative issue-time epoch stamping alone does not prove a non-cooperating producer cannot forge/restamp lineage.

### 3. Resynchronization request CAS / idempotency guard
Provenance: source commit `06e39638cab4143185803bcae0c8ea9921479764`; focused acceptance absent.

Function intended: bind a resync request to base epoch + checkpoint digest, make exact replay idempotent, reject same-ID conflicts, stale/future bases and watermark rollback.

Reduction: compare-and-swap + idempotency-key + replay-protection engineering.

Status in R26: reference/proposed dependency only; not admitted or verified.

### 4. Proposed `ResynchronizationAnchorValidator`
Provenance: R26 design-only component; not implemented and not scientific evidence.

Function: produce a validated WORLD anchor from an independent WORLD/session snapshot plus causal-cut provenance rather than from a caller's bare world-position claim.

Minimal anchor fields:
- `world_session_id`;
- `anchor_id`;
- `source_checkpoint_token` or equivalent snapshot identity;
- `covered_through_outcome_sequence`;
- snapshot/WORLD-state digest and state payload;
- old and proposed new recovery/reconciliation epoch;
- causal-cut / commit-boundary identity.

The validator must establish that the snapshot belongs to the expected WORLD/session and that its sequence/boundary corresponds to an actual committed WORLD cut. Control-authority freshness alone is not sufficient proof of WORLD truth.

### 5. Atomic rebase cut
Provenance: established transactional snapshot/fencing pattern.

Function: close or fence old-epoch execution before post-anchor operation begins, apply anchor state + watermark + horizon + observer certainty + new epoch as one recovery boundary, and prevent a pre-cut action from committing invisibly after the snapshot.

For a single-process bounded synthetic WORLD, a single-writer transaction/lock is sufficient. A distributed consensus mechanism is not required unless the WORLD implementation itself becomes distributed.

## interfaces_and_state_loop

`WORLD committed state / execution journal`
→ `snapshot at explicit causal cut`
→ `ResynchronizationAnchorValidator`
→ `validated anchor`
→ optional verified `CAS/idempotency request binding`
→ `old-epoch execution fence/drain`
→ atomic `WORLD observer + watermark + horizon + certainty + recovery_epoch` rebase
→ post-anchor receipt processing only from the new epoch.

The recovery epoch is not the descending modulation authority epoch. Control authority freshness and observer-history generation are separate state axes.

## why_each_component_is_used

- R25 horizon: bounds memory while preserving unknown/expired causality explicitly.
- Anchor validator: prevents self-attested arbitrary WORLD state from restoring certainty.
- Atomic cut: prevents snapshot/action races from creating an unobserved state delta.
- Recovery epoch: prevents old delayed receipt lineage from contaminating the new observer generation.
- CAS/idempotency guard: prevents duplicate/competing resync requests from applying multiple rebases or stale bases, if focused acceptance demonstrates value.

## known_reductions

Nothing here requires a novel cognitive or biological mechanism. Snapshot provenance, write-ahead/execution logs, monotonic generations, compare-and-swap, idempotency keys, fencing tokens and checkpoint/replay are established systems techniques. Literature R52 specifically reduces novelty for stale-authority generation fencing and snapshot boundary identity. Biological cue-based recalibration is at most design inspiration; it does not imply authenticated digital snapshot semantics.

## known_limitations

- A validated anchor re-establishes certainty prospectively from the anchor boundary; it does not reconstruct the causal content of events that expired before the anchor.
- An epoch token by itself proves neither WORLD truth nor biological correspondence.
- The current green epoch-fence Forge component assumes cooperative issue-time binding; WORLD-side execution fencing is required if stale producers can continue committing after a cut.
- The CAS guard is not semantically accepted yet and must not be treated as ready.
- Snapshot truth is only as strong as the bounded WORLD/checkpoint provenance source. In the current synthetic single-process world this can remain local and deterministic.
- This design says nothing about fly-topology superiority, biological fidelity, or scientific novelty.

## acceptance_tests

1. **No self-attested certainty restoration**: directly supplying an arbitrary position cannot clear `DEGRADED_CAUSAL_GAP`; only a validated anchor can.
2. **Session/checkpoint mismatch**: wrong `world_session_id`, snapshot token, checkpoint token, or causal-cut identity fails closed without WORLD/observer mutation.
3. **Monotonic coverage**: an anchor whose covered outcome sequence is below the current watermark is rejected; a future/impossible causal cut is rejected.
4. **Snapshot/action race**: an old-epoch action cannot commit after the validated anchor cut. Either it is committed before the anchor and included in the snapshot, or fenced/rejected after the cut.
5. **Old receipt isolation**: a delayed old-epoch receipt, even with sequence greater than the anchor watermark, cannot mutate post-anchor observer state.
6. **Pending-lineage accounting**: every pre-anchor pending item is classified as `COVERED_BY_ANCHOR`, `RETIRED_BY_REBASE`, or explicit unresolved failure; none disappears silently.
7. **Atomic crash recovery**: crash at each rebase step restores either the complete pre-anchor state or complete post-anchor state; never new epoch with old watermark, or new position with old certainty/gap registry.
8. **Idempotent rebase**: exact same anchor/request replay is a no-op; same identity with different payload is a conflict; stale and future bases fail closed.
9. **Checkpoint/replay**: anchor identity, consumed-resync identity, recovery epoch, horizon, watermark and certainty survive restore.
10. **Bounded long run**: retained exact history remains bounded by configured horizon/window after repeated gap/resync cycles.

## suggested_component_replacement_tests

- raw R25 `resynchronize()` vs validated-anchor rebase under forged/wrong snapshot inputs;
- validated anchor with vs without CAS/idempotency guard under duplicate and competing resync requests;
- validated anchor with vs without recovery-epoch fence under delayed old receipts;
- custom R26 layer vs a local SQLite/WAL single-writer implementation using a transaction, unique resync ID and monotonic generation.

If the simpler SQLite/WAL design satisfies all invariants with less machinery, prefer it.

## suggested_interaction_ablation_tests

- Remove anchor validation: arbitrary snapshot claims should become admissible, demonstrating the trust-boundary function.
- Remove atomic execution fence while retaining anchor validation: force a snapshot/action race and test for hidden post-snapshot commit.
- Remove recovery epoch while retaining anchor validation: old delayed receipts should be able to contaminate the rebased observer.
- Remove CAS while retaining anchor + epoch: duplicate/competing requests test whether CAS adds real value in the single-writer deployment.

These are engineering discriminators, not scientific mechanism tests.

## alternative_established_architecture

A local single-writer SQLite/WAL store can hold WORLD commits, outcome watermark, recovery generation, anchor identity and consumed resync IDs in one transaction. Periodic versioned snapshots plus a generation column can provide the same practical invariant. This should be the default simplification comparator before inventing a larger custom recovery subsystem.

## scientific_claims_explicitly_not_made

R26 is **not scientific evidence**. It does not establish:
- biological fidelity or equivalence;
- fly-like topology necessity or superiority;
- compute or energy efficiency;
- composition contribution;
- whole-system superiority;
- external validity;
- emergence;
- scientific novelty.

Scientific credit remains `0`.

## build_value_if_no_novelty_exists

Even with zero novelty, the design gives a precise route for long-running bounded receipt reconciliation to recover from explicit causal gaps without silently manufacturing certainty, and makes the failure/recovery boundary testable under checkpoint/replay.

## suggested_SYSTEM_BUILD_scope

Optional SB003 Milestone B/C hardening only, after fresh Evidence Analyst reconciliation. Do not make this an M1 gate, do not change SB003 activation conditions, and do not introduce a mandatory review gate. The immediate engineering sequence should remain:

1. reconcile the already-green R25 bounded-horizon + recovery-epoch artifacts through Analyst;
2. finish focused semantic acceptance for the CAS guard only if it remains useful;
3. probe a minimal validated WORLD anchor + atomic causal cut;
4. run scoped composed long-running acceptance;
5. prefer the simpler established architecture if replacement tests show equivalent guarantees.

## independence_from_current_MAIN_unknown_outcomes

The design does not depend on a positive M1/SB003 scientific outcome and does not modify M1-002. It is ordinary optional recovery hardening. The current required M1-002 PR path remains a separate P0 blocker.

## status

`INTEGRATION_DESIGN_PROPOSAL`
