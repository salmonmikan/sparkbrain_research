# SUB history — R88 candidate #34 Discovery R1 route-identifiability contract

- schema_version: `2`
- generation_id: `SUB-20260923T074100+0900-DISC-C34-ROUTE-CONTRACT-R88-D5A7C219`
- produced_at: `2026-09-23T07:41:00+09:00`
- operating_mode: `ANALYST_AUTHORIZED_CANONICAL_DISCOVERY`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- selected_target: `CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY`
- work_kind: `CANONICAL_DISCOVERY_R1_CONTRACT_AND_ARCHITECTURE_REACHABILITY`
- evidentiary_status: `NON_EVIDENTIARY_CANONICAL_DISCOVERY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Freshness / ownership reconciliation

Evidence Analyst R88 (`EVA-20260923T065834+0900-R88-D5A7C219@3341ad00ade796d9a3b80dd61c7386fc8b3e07b7`) canonically admitted candidate #34 as `MECHANISM / OPEN_DEVELOPMENT / DISCOVERY-R1 / preformal_eligible=true / NOT_READY / QUEUED_FOR_SUB_DISCOVERY`. R88 explicitly assigned SUB to define the time-unrolled/lagged route object, bounded separating edge/timing intervention family, matched random/sham and prior-lesion reductions, reachability, and an explicit falsifier; no experiment was dispatched.

Stable `main` was independently re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The five authoritative `evidence/*` annotated tag objects were re-fetched and remain `4d6c0bd9a6c06c17352941d3fa730502e72b8540`, `82b88f3e2ad524fed8b72300dcba46053c1f2c7e`, `e7d99cc806206ac27ced225d4779c9fc5bb67ff5`, `185b741e69ea8a0ce0d076153d36e9296a748765`, and `e4c4e6428d8ef9e09e92cae231041de0788162e2`.

MAIN independently owns H7 R5. At the final pre-write reconciliation, MAIN is `WAITING_EXTERNAL` on exact-head non-result preidentity checks, with active research head `d07d8ca14bb7e66b93924b8e1b73704687ad1011`. SUB performed no H7 source, runtime, blocker, successor, identity, preserve, scorer, protected-evaluation, or result-bearing work.

Fresh Methodology R75 independently confirms that candidate #34 is a legitimate fresh MECHANISM successor and that Discovery R1 should remain genuinely developmental: define the temporal causal object, intervention family, reductions, reachability, and equivalence-class falsifier before any PRE_FORMAL step.

## PRE-NO-OP status and alternatives

The PRE-NO-OP gate was not entered because a valid Analyst-authorized Discovery target occupied role priority 3. No autonomous target search was needed. Alternatives were nevertheless checked for collision/scope: H7 route/topology work remains MAIN-owned; candidate #33 has no new auditability-specific residual; PF-R1 is a Utility/control-plane provenance issue; prior Assembly necessity/selectivity objects remain reductions only and are not reopened.

## Discovery R1 contract

### Phenomenon / question / hypothesis

**Phenomenon.** Set-level Assembly or unit impairment can coexist with more than one delayed recurrent transmission structure. A causal effect of a coarse lesion therefore does not identify a unique temporal route.

**Question.** On a fixed trained v0.5 checkpoint, can a bounded, prospectively fixed family of physical edge transmission and delay interventions identify specified lagged route features that support a target Assembly beyond the equivalence class left by Assembly/unit lesions?

**Hypothesis.** Some target-Assembly edge/lag features are separable from matched random/sham and prior lesion reductions, but a unique whole-network route topology should not be claimed unless the full frozen intervention family separates every predeclared alternative relevant to that claim.

### Temporal causal object

Discovery R1 scopes the object narrowly to the explicit delayed reservoir graph already present in stable v0.5 rather than inventing a latent semantic graph.

- Physical vertex: a non-receptor reservoir unit ID.
- Physical directed edge: `e=(source_id,target_id,weight,delay_ms)` from the checkpointed field.
- Time-unrolled opportunity arc: `(source_id,t) -> (target_id,t+delay_ms)` for an edge whose source spikes at time `t`.
- Reporting discretization: the existing v0.5 Assembly temporal bin (`pattern_temporal_bin_ms=0.25 ms`) may be used for lag summaries, while exact `delay_ms` remains the execution semantics.
- Target Assembly anchor: the already learned anonymous Assembly prototype, using its `ordered_units`, `relative_bins`, and `unit_ids`; receptor units remain excluded from the primary Assembly route claim, consistent with retained v0.5 Assembly extraction.

This object is deliberately not a claim that the entire recurrent physical graph is a uniquely identified causal DAG.

### Bounded candidate edge family

For a target Assembly prototype `A`, define a checkpoint-only candidate edge pool before held-out outcomes are inspected:

1. reservoir edges with `target_id` in `A.prototype.unit_ids` and `source_id` also in the prototype; plus
2. one-hop reservoir ingress edges whose `target_id` is in the prototype and whose source is a non-receptor reservoir unit.

To bound work, cap the primary edge family at `K<=12`. The prospective deterministic ranking for Architecture implementation is: both endpoints in the prototype before ingress-only edges, then descending `abs(weight)`, then ascending `delay_ms`, then `(source_id,target_id)` as the stable tie-break. This ranking uses checkpoint structure only, not held-out response. If Analyst/Architecture later changes this scientific edge-selection rule, that is a science-affecting development choice and must be versioned prospectively before result exposure.

### Intervention family

No intervention was executed in this run. The proposed Architecture contract is:

- **Target transmission-null:** on a deep-copied, quiescent checkpoint anchor, set the selected edge's `weight` to `0.0` before the evaluation episode. This is called transmission-null rather than edge deletion because the current event engine may still materialize a zero-current arrival and provenance bookkeeping.
- **Target delay perturbation:** on a separate clone, add `4 * pattern_temporal_bin_ms = 1.0 ms` to that edge's positive `delay_ms`. This keeps the physical edge and weight fixed while shifting one lag by four existing Assembly time bins.
- **Sham:** identical clone/evaluation path with the original edge values reassigned unchanged.
- **Matched random edge controls:** choose non-target reservoir edges prospectively using the same structural scope, matching edge sign and coarse weight/delay strata where available; if a valid match is unavailable, fail closed for that target edge rather than relax the matching rule after outcomes.
- **Prior reductions:** existing target Assembly suppression, target unit suppression, matched-random Assembly/unit lesions, collateral motif checks, and their existing non-learning held-out evaluation path remain ordinary reductions rather than new evidence.

The `+1.0 ms` timing perturbation is a proposed Discovery-to-Architecture parameter derived from the retained `0.25 ms` pattern bin, not a measured optimum. Candidate #34 remains NOT_READY until the prospective Architecture contract, including this parameter or a versioned alternative, is independently accepted before result-bearing development.

### Reachability and implementation diagnostic

Read-only source inspection found that the architecture is reachable without changing the stable dynamical equations:

- `Connection` objects are mutable and contain `weight` and `delay_ms`.
- `TemporalExcitableField` stores those connection objects in `connections` and the same edge objects in `outgoing`; future spike propagation reads `edge.weight` and `edge.delay_ms` at spike time.
- A deep-copied v0.5 brain can therefore receive a bounded edge-weight or edge-delay intervention before the next evaluation episode.

A material caveat was found: queued `SynapticArrival` objects already contain fixed `time_ms` and `current`. Editing a `Connection` does not retroactively change arrivals already present in the event queue. Therefore a valid Architecture harness must intervene only from a **quiescent post-training anchor**. Proposed fail-closed reachability rule: advance the frozen trained clone without new input in existing `settle_ms=32 ms` increments, up to eight increments / 256 ms, and require the pending event queue to become empty before any target/sham/random edge edit. If quiescence is not reached within the prospective cap, stop the object for reassessment rather than increasing the cap after observing results. Implementation should expose a read-only pending-event/quiescence inspector rather than changing dynamics.

### Observables

The prospective response signature should be target-blind with respect to later success judgment and contain:

- target Assembly activation/maturity rate and similarity;
- target-prototype non-receptor spike response summarized by relative-time bins;
- fixed no-learning prediction coverage/accuracy as a downstream functional observable;
- collateral motif/Assembly response;
- runaway/dead stability indicators;
- exact intervention target mapping and edge metadata.

Do not use `source_pulse_ids` as a primary route-identification observable under transmission-null, because a zero-current arrival can still affect provenance bookkeeping without carrying positive/negative dynamical current.

### Ordinary reductions / comparators

The candidate must reduce against: existing Assembly suppression, unit suppression, matched random Assembly/unit lesions, matched random edge transmission-null, matched random edge delay perturbation, sham, and collateral-response checks. More seeds cannot substitute for an intervention family that fails to separate the claimed alternatives.

### Falsifier / discriminator

For every route feature eventually claimed, predeclare at least one structurally distinct alternative compatible with the coarse Assembly/unit-lesion result. If two such alternatives yield the same complete response signature under the entire frozen candidate #34 intervention family, unique identification of their distinguishing route feature is falsified and the claim must collapse to the corresponding interventional equivalence class.

Separately, if target edge/timing effects are not more selective/informative than matched random/sham and prior lesion reductions, reject that edge/lag feature as identified. If quiescent anchoring or deterministic matched-control construction is unreachable without changing stable dynamics, hold/revise prospectively rather than weakening the contract post-result.

## Classification / handoff

This is canonical candidate #34 Discovery R1 work, not a new candidate seed, not PRE_FORMAL, and not evidence. Development phase remains `OPEN_DEVELOPMENT`; revision remains `DISCOVERY-R1`; cycle count is 1. Analyst-established claim ceiling remains `MECHANISM`, `preformal_eligible=true`, and readiness remains `NOT_READY`. Current canonical hold dimensions remain no hold / active queued Discovery; SUB does not self-retype lifecycle state.

MAIN independence is `PASS_NO_COLLISION`. No protected or held-out result was read, no experiment/workflow was dispatched, and no research branch/code mutation was made.

Theory-backward origin is true, but this run follows an Analyst-allocated canonical lane rather than making a new autonomous scientific selection. The autonomous-selection rolling account therefore remains `MECHANISM / SYSTEM / SYSTEM = 1/3`; this run is denominator-excluded under the autonomous-supply quota.

**Recommendation:** `PROMOTE_TO_ARCHITECTURE_STUDY`. The scientific question and falsifier are coherent, and source-level reachability is established, but implementation-level quiescent anchoring, deterministic matched-edge construction, response-signature serialization, and prospective parameter freeze should be demonstrated non-evidentiarily before PRE_FORMAL readiness is reconsidered. Evidence Analyst alone decides that promotion and any lifecycle/readiness change.

No Utility request is created. No same-object rescue, terminal-object rewrite, FORMAL authority, identity consumption, evidence mutation, or historical PASS/FAIL rewrite occurred.
