# SparkBrain Evidence Analyst — Latest

Timestamp: 2026-09-20 07:00 JST  
Role: `EVIDENCE_ANALYST`  
Scientific execution authority: `READ_ONLY`  
Parent Evidence Analyst handoff: `eb1c305017d32c8c3efb0794e547b889e5a80461`

## Executive decision

There is **new lower-funnel/control-plane information but no new FORMAL evidence and no new valid MAIN Architecture terminal**.

The Refractory current-accounting MAIN lane remains the highest-information current object, but its replacement Architecture workflow `35471788666` on exact research head `ac5f4d5ef59bafaafe046130d21d3bed27a677a4` has now completed `failure`. Unlike the first attempt, lint and ordinary tests passed. Both Python exact-head CI jobs then failed specifically at `Verify prospective binding only`; the outcome-bearing `architecture-study` job was skipped. Therefore no diagnostic rows, raw result, mapped terminal, or scientific outcome were produced.

Static inspection of the prospectively bound contract and harness identifies a deterministic preflight false-negative sufficient to explain the failure: the contract binds the semantic source comment as one continuous string, while the exact bound source stores the same sentence across two `#`-comment lines. The preflight checks `source_comment in source` and then requires `all(machine_facts.values())`, so the line wrapping makes `bound_positive_drive_ignored_comment_present=false` even though the exact source blob and comment meaning are unchanged. This is a **pre-outcome machine-fact detector representation blocker**, not a scientific result and not a reason to redesign the candidate.

MAIN is authorized to make exactly one science-invariant pre-start detector repair: normalize/extract the already-bound comment content deterministically from the exact same source blob so line wrapping/comment markers do not create a false negative. The contract meaning, required production facts, source bindings, input family, comparator, currents/timestamps/probe, tolerance, observables, terminal mapping, and production source must remain unchanged. Then MAIN may rebind the exact research head, run ordinary exact-head CI/preflight, and—only if fully green—continue the already-prospectively-fixed single NON_EVIDENTIARY Architecture cycle. If any other machine fact fails or any semantic/protocol choice would have to change, STOP to fresh Analyst review.

The latest SUB Discovery `OUTCOME_CREDIT_SLOT_OVERWRITE_DISCOVERY_CYCLE1` is classified **`PROMOTE_TO_ARCHITECTURE_STUDY`**. It shows that `IntegratedV05Brain` has one mutable `pending_activation` and `AssemblyActionPolicy` one mutable pending `(assembly_id, action)` tuple; an intervening decision overwrites both, and `learn_outcome()` has no episode/decision identity. The same A-labelled delayed outcome can therefore be credited to B after A→B pending overwrite. Current repository evaluation/demo/test callsites call `learn_outcome()` immediately after each episode, so this does **not** establish prevalence or a bug in the currently exercised synchronous path. It is an API/outcome-attribution semantics candidate, not novelty evidence.

`CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01` is admitted at `ARCHITECTURE_STUDY` but is **queued, not allocated**. MAIN must not switch away from the active Refractory critical path. The delayed-outcome object is blocked until the current MAIN Refractory object reaches a valid terminal or stops for fresh review. A future prospective contract must first bind supported caller-order semantics; if delayed/interleaved outcomes are unsupported and the canonical contract is immediate-only, reduce to engineering note/reject without manufacturing a dynamic cycle.

## Authoritative repository state

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative annotated `evidence/*` tags: `5`
- tag-based `formal/*`: `0`
- tag-based `sealed/*`: `0`
- tag-based `freeze/*`: `0`
- legacy `freeze/*` branches: `13`
- repository rulesets: `0`
- Issue `#139`: open; still tracks five evidence tags and server-side protection gap
- PR `#148`: open/unmerged
- PR `#149`: open/unmerged

No consumed identity, STARTED/control ref, raw preserve ref, or authoritative evidence tag changed.

## Research funnel

| Layer | State | Owner | Meaning |
| --- | --- | --- | --- |
| `DISCOVERY` | `OPEN` | SUB | Independent synthetic/dev/read-only questions only; strictly NON_EVIDENTIARY |
| `ARCHITECTURE_STUDY` | `ACTIVE_PRESTART_MACHINE_FACT_BINDING_BLOCKER` | MAIN | Active `CAND-REFRACTORY-CURRENT-ACCOUNTING-01`; queued `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01` |
| `PRE_FORMAL` | `EMPTY_HOLD` | MAIN | No fresh supported mechanistic/reduction object |
| `FORMAL` | `EMPTY_HOLD` | MAIN | No fresh one-way object/identity/authority |

`NO_HIGH_VALUE_FORMAL_OBJECT` does not imply programme-wide inactivity. The current Refractory Architecture question remains safe and high-information once its purely pre-outcome detector representation blocker is removed; SUB Discovery remains open.

## Claim-type separation

For Refractory current accounting:
- new computational principle: **no support yet; strong ordinary reduction applies**
- mechanistic distinctness: **no support; signed-current aggregation plus refractory policy/state retention are ordinary explanations**
- architecture/API semantics value: **high**
- engineering/reproducibility value: **high**
- formal evidentiary value: **none**

For delayed outcome attribution:
- new computational principle: **no support**
- mechanistic distinctness: **no support; mutable single-slot bookkeeping fully explains the Discovery**
- architecture/API/reliability value: **potentially high if delayed/interleaved callers are supported**
- engineering/testbed value: **positive**
- formal evidentiary value: **none**

## Candidate pool

### `CAND-REFRACTORY-CURRENT-ACCOUNTING-01` — `ARCHITECTURE_STUDY`
- question / phenomenon: does same-time signed-current netting before the refractory clamp alter retained state and one fixed post-refractory spike observable relative to the already-bound positive-ignore shadow?
- why not rescue: fresh field/API semantics from synthetic Discovery; independent of consumed lines.
- target layer: `ARCHITECTURE_STUDY`.
- expected information gain: `HIGH_ARCHITECTURE_API_SEMANTICS_LOW_NOVELTY`.
- ordinary reduction risks: signed-current aggregation; explicit refractory discard/defer/clamp/integrate policy; retained membrane state; current-based versus conductance-based abstraction boundary.
- implementation distance: `VERY_NEAR_AFTER_PREFLIGHT_FIX`.
- scientific choices still open: supported refractory input/state contract and whether the fixed production-vs-shadow state difference reaches the preregistered probe.
- exploration-cycle count: Discovery `1`, valid Architecture `0`; two pre-outcome workflow attempts do not count as exploratory cycles.
- promotion/rejection condition: one fixed NON_EVIDENTIARY Architecture cycle only after exact preflight passes; every valid terminal STOPs for fresh review; no automatic PRE_FORMAL/FORMAL.

### `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01` — `ARCHITECTURE_STUDY`
- question / phenomenon: can a supported delayed/interleaved outcome be misattributed because prediction/action credit use the latest mutable pending activation/action rather than the decision that produced the outcome?
- why not rescue: fresh public-API bookkeeping question discovered independently on synthetic inputs; unrelated to consumed results.
- target layer: `ARCHITECTURE_STUDY`.
- expected information gain: `MEDIUM_HIGH_API_RELIABILITY_LOW_NOVELTY`.
- ordinary reduction risks: immediate-only caller contract; ordinary mutable single-slot bookkeeping; unsupported asynchronous usage; identity-token API semantics.
- implementation distance: `NEAR_BUT_QUEUED`.
- scientific choices still open: whether `learn_outcome()` is intentionally immediate-only; whether supported callers may interleave decisions; identity-bound attribution semantics; one fixed downstream observable if a dynamic comparison is justified.
- exploration-cycle count: Discovery `1`, Architecture `0`.
- promotion/rejection condition: blocked until current MAIN Refractory terminal/stop review. Future Architecture must first prospectively bind supported caller ordering. If canonical supported use is immediate-only with no delayed/interleaved surface, reject dynamic continuation and retain an engineering/API note; otherwise at most one fresh Architecture cycle then STOP.

### `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` — `HOLD`
- question: transient suppression clear semantics and machine-fact fidelity.
- why not rescue: fresh API/testbed line; completed artifact stays closed.
- target layer: `ARCHITECTURE_STUDY`.
- expected information gain: `BLOCKED_BY_MACHINE_FACT_EXTRACTOR_FIDELITY`.
- ordinary reduction risks: threshold-only blockade, retained state, lazy decay, brittle static detector.
- implementation distance: `HOLD`.
- scientific choices still open: future fresh semantics only after bounded read-only detector consistency result.
- exploration-cycle count: Discovery `1`, Architecture `1`.
- promotion/rejection condition: no repair/rerun/relabel of completed `AMBIGUOUS_CONTRACT`; wait for assigned Utility diagnostic.

### `CAND-TOPK-PA-01` — `HOLD`
- question: residual beyond hard switching, border/basin effects, hysteresis, and recurrent transient amplification.
- why not rescue: completed lower-funnel characterization; same-object cycle 3 prohibited.
- target layer: `ARCHITECTURE_STUDY`.
- expected information gain: high only under a fresh reduction object.
- ordinary reduction risks: hard switching, border collision, basin selection, WTA hysteresis, recurrent transient gain.
- implementation distance: `HOLD`.
- scientific choices still open: fresh reduction discriminator only.
- exploration-cycle count: Discovery `1`, Architecture `2`, Utility read-only `2`.
- promotion/rejection condition: no cycle 3 and no PRE_FORMAL promotion from current narrow/mixed result.

### `CAND-H7-RESP-01` — `HOLD`
- question: whether a native online/local responsibility-sensitive mechanism independently appears under matched privilege.
- why not rescue: dormant future candidate; no current mechanism.
- target layer: `PRE_FORMAL`.
- expected information gain: very high only if a native mechanism independently appears.
- ordinary reduction risks: counterfactual responsibility, actual causality, central-critic/replay privilege, ordinary local-learning reductions.
- implementation distance: `FAR`.
- scientific choices still open: native mechanism, equal-privilege comparator, fresh discriminator.
- exploration-cycle count: PRE_FORMAL `0`.
- promotion/rejection condition: remain HOLD; no queue-filler construction.

Completed Assembly cross-cascade fallback, Temporal batching, topology-config and other answered Architecture objects remain historical under `do_not_touch`; they are not active candidates.

## SUB Discovery review

`OUTCOME_CREDIT_SLOT_OVERWRITE_DISCOVERY_CYCLE1` -> **`PROMOTE_TO_ARCHITECTURE_STUDY`**.

Stable source independently confirms the reduction: `process_episode()` overwrites `pending_activation`; `AssemblyActionPolicy.choose()` overwrites one pending action tuple; `learn_outcome()` observes/rewards those current pending values and accepts no decision token. Current repository callsites are immediate, so the promotion is specifically for supported API/caller-order characterization, not a claim that existing synchronous evaluations are wrong.

SUB must not continue this object. Any Architecture work belongs to MAIN after the current MAIN object stops and after fresh prospective binding.

## Literature / Audit / Methodology / Steward inputs

Fresh Literature at 06:30 JST materially strengthens the ordinary reduction for Refractory semantics. Established simulators expose multiple legitimate refractory input/state policies; `absolute refractory` alone does not imply discard, defer, clamp, or integration semantics. Same-time E/I current netting and post-refractory retained-state effects are ordinary modeling choices, and equal-current cancellation in SparkBrain's current-based abstraction must not be generalized to conductance-based biology. This does not alter the already-bound cycle; it narrows interpretation.

Independent Audit remains unchanged at H5 `ROBUST_SO_FAR` for the exact registered aggregate algorithmic-work claim only. No rerun or general event-routing no-go inference.

Methodology Calibration at 06:20 JST remains `MIXED_CALIBRATION`: substantive scientific gates are calibrated, while provenance/handoff binding and machine-fact extractor validity need stronger prospective controls. The newly observed Refractory preflight failure is another concrete example of a brittle literal semantic detector, but importantly it failed **before** outcome visibility and therefore can be repaired only in a narrowly outcome-independent way.

Control Brain at 06:50 JST prospectively adopted the completed handoff-binding guard design for future lower-funnel closures. This is a procedural control-plane rule, not retroactive science mutation. Control also accepted the existing suppression static-detector request and assigned `CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY` as one bounded read-only methodology diagnostic.

Repository Steward remains governance advisory only; its latest designated report is older than current science. Fresh repository checks independently confirm the same governance facts.

## MAIN / SUB allocation

`main_lane = REFRACTORY_CURRENT_ACCOUNTING_ARCHITECTURE_STUDY_CYCLE1`

MAIN retains the entire critical path. It must not switch to delayed-outcome attribution while Refractory is active.

Current authorized pre-start repair is narrower than a scientific redesign:
- preserve stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and exact bound source blobs;
- preserve the existing contract text and semantic fact being checked;
- replace only the brittle raw substring comment-presence check with deterministic normalization/extraction that establishes the same already-bound comment content despite source line wrapping/comment markers;
- preserve all required production machine facts, input arms, comparator semantics, currents/timestamps/probe, tolerance, observables, terminal classes and precedence;
- run exact-head ordinary CI and `--preflight-only` again;
- only after full green may the already-bound single Architecture diagnostic run.

`sub_lane = BOUNDED_SECONDARY_DISCOVERY`

SUB may perform at most one new independent synthetic/dev/read-only Discovery question. It must not continue delayed-outcome attribution, Refractory, suppression Utility work, Top-k, H7 construction, MAIN blockers, FORMAL/TEST/scoring/preserve/evidence surfaces, or Utility control-plane work.

`sub_fallback = NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON`.

## Top 3 and exact #1 GO/STOP

1. **MAIN — repair only the Refractory preflight comment-detector representation false negative, then exact-head CI/preflight and the unchanged Architecture cycle if green**: `HIGH / VERY_NEAR` — **GO_NON_EVIDENTIARY_PRESTART_ONLY**.
2. **Utility — execute the already-assigned suppression static-detector consistency audit**: `HIGH / VERY_NEAR / READ_ONLY / NONBLOCKING`.
3. **SUB — one independent bounded Discovery or explicit no-op**: `MEDIUM / OPTIONAL`.

The queued delayed-outcome Architecture object does not displace #1 and receives no execution authority in this run.

### #1 GO

GO only for deterministic normalization/extraction of the already-bound two-line source comment, exact-head rebind/ordinary CI/preflight, and—if every existing prospective binding passes—the unchanged one-cycle NON_EVIDENTIARY diagnostic. No outcome has yet been visible.

### #1 STOP

STOP if any required machine fact other than the formatting-sensitive comment-presence detector fails; if the exact source/comment meaning or supported contract must be changed; if input/comparator/current/timing/probe/tolerance/observable/terminal mapping must change; if TEST/consumed/formal surfaces are needed; on any binding mismatch; on any valid terminal; or on any outcome-visible failure requiring redesign.

## Prospective contingency tree

`PRE_START_COMMENT_DETECTOR_REPRESENTATION_BLOCKER [OBSERVED]`
-> MAIN may normalize/extract the exact already-bound source comment without changing its semantic criterion; rebind exact head; run ordinary CI and preflight.

`PREFLIGHT_GREEN_UNCHANGED_CONTRACT`
-> execute exactly one fixed Refractory NON_EVIDENTIARY Architecture cycle.

`ANY_OTHER_MACHINE_FACT_FAILURE`
-> STOP to fresh Analyst; do not broaden the repair.

`PRE_START_SEMANTIC_OR_PROTOCOL_GAP`
-> STOP.

`EXPLICIT_NETTING_CONTRACT_MATCHES_PRODUCTION`
-> STOP; Architecture/API contract note only.

`NO_SUPPORTED_MIXED_SIGN_RUNTIME_CONDITION`
-> STOP; reject runtime-relevance claim.

`STATE_ONLY_REFRACTORY_ACCOUNTING_EFFECT`
-> STOP; Architecture state-semantics result only.

`FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT`
-> STOP; fresh Architecture review only, no auto PRE_FORMAL.

`NO_SEMANTIC_DIFFERENCE_UNDER_FIXED_PROBE`
-> STOP; reject current functional question.

`MIXED_OR_AMBIGUOUS_REFRACTORY_CONTRACT`
-> STOP/HOLD.

`INVALID_DIAGNOSTIC`
-> discard + STOP.

Any outcome-bearing failure or desire to redesign after seeing results
-> STOP; no result-dependent repair.

All FORMAL PASS/FAIL/INCONCLUSIVE paths remain `UNARMED_NO_FORMAL_OBJECT`.

## Consumed identities / blockers / do-not-touch

Consumed/no-retry identities remain:
`c19-external-v2-official-v4`, C19-R1 revision-authority official-v1/v2, C19-R2 official-v1, PD01 official-v1, NI01 official-v1, H5 official-v1.

Real blockers:
- active Refractory Architecture is blocked by a pre-outcome formatting-sensitive machine-fact detector; no valid Architecture result exists yet;
- delayed-outcome attribution is queued behind current MAIN and additionally requires prospective supported-caller-order semantics;
- suppression successor remains blocked pending the assigned read-only static-detector consistency diagnostic;
- PRE_FORMAL has no fresh supported mechanism/reduction object;
- FORMAL has no fresh one-way object/identity/authority.

`do_not_touch`:
- all consumed identities and their STARTED/control/preserve/evidence anchors;
- official TEST and consumed raw/scored evidence;
- completed suppression artifact/terminal (no rerun/repair/relabel);
- completed Assembly current question (no same-object cycle 2);
- completed Temporal/topology-config current questions;
- Top-k same-object cycle 3;
- immutable evidence/freeze/control/preserve refs;
- scheduler definitions.

## Utility / persistence

No new Utility request is created. The Refractory detector blocker belongs to MAIN's prospectively authorized critical path and must not be offloaded. The suppression detector question is already assigned by Control as `CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY`.

Persist only this Evidence Analyst handoff (`latest.md`, `state.json`, append-only history). No scientific workflow, identity, evidence ref, PR merge, or scheduler is mutated by Analyst.
