# External Literature Reduction Scout — exact equivalence and eligibility-support turnover

- schema_version: `2`
- generation_id: `LIT-20260922T033126+0900-R25-EXACT-SUPPORT-TURNOVER-7D3A91C5`
- produced_at: `2026-09-22T03:31:26+09:00`
- producer_run_id: `external-literature-auto-20260922T033126+0900-R25-7D3A91C5`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T010311+0900-R24-CONTSTATE-EVENTDRIVEN-4A7C91E2`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `03:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was refreshed independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The five annotated `evidence/*` tags are unchanged; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty; 13 legacy `freeze/*` branches and preserve refs were refreshed. The new result branch `research/main-semantic-active-work-localization-r50-cycle2` remains at exact head `d090fd2e57680c5a97b9fd0d036fc65a008078ec`.

Consumed control-plane generations and exact commits:

- Control Brain: `CTRL-20260922T025652+0900-R28-9A9BFB1F` @ `d2f0ffa7e263fd9b7b0210cf1d5c99574894f6e6`
- Evidence Analyst: `EVA-20260922T031000+0900-R50-4C8A21D7` @ `8ae04f045ac760cfd8b209f337284293d6c58bf1`
- MAIN: `MAIN-20260922T032800+0900-PRIMARY-FUNNEL21-SYSTEM-LOCALIZE-R50-CYCLE2-INTEGRITYSTOP-4C8A21D7` @ `b3fb893a7c700bb7337ed869660d5023405e4920`
- SUB: `SUB-20260922T033500+0900-NOOP-R50POSTMAIN-INTEGRITYSTOP-5A7C21E4` @ `72c414c434fe563c78b09ab5f5ec33ff337cf1dd`
- prior Literature: `LIT-20260922T010311+0900-R24-CONTSTATE-EVENTDRIVEN-4A7C91E2` @ `e9f3bd07d8aed08b81d8c307525e5c6c53a3eef4`

R50 is the material repository delta. Evidence Analyst R50 prospectively authorized exactly one bounded SYSTEM Architecture measurement under fixed contract `SB-R49-C32-CREDIT-TRACE-CROSSOVER-V1`. MAIN ran all 38 fixed grid points and preserved raw output before interpretation. Scientific workflow `35637961215` succeeded on exact head `d090fd2e...`; raw artifact `10656767754` has digest `sha256:7494fb60db1e7aca3fa86fd4a1359082da9d52e1733404bdbef8f27412fbfba8`, and summary artifact `10656637964` has digest `sha256:8e78b5496de153fc25ff92968fefaab5cb6af28556cd1c1b455aaacefd962375`.

The generated summary reported a large ordinary-reduction signal: at the anchor, logical primitive counts were `REF_GLOBAL_SCAN=267200`, `ORD_ACTIVE_SET_TIMESTAMP_LAZY=2964`, `ORD_HISTORY_ARCHIVE_EXACT=3668`, and `ORD_SOURCE_INDEXED_SPARSE_EVENT=2964`. However MAIN correctly stopped fail-closed because the contract-required complete trajectory-equivalence gate was not actually verified: final eligibility and final weights were compared, while event/fire/ignition/prediction equality fields were set true by construction and intermediate per-reward checkpoints were not independently checked. This run does not promote or repair that opened result.

R24 already established event-driven exact/continuous-state plasticity and compute↔history crossover. This run does not recycle that literature. The new question is whether the R50 exact-sparse reduction remains valid over long horizons and changing eligibility support, and what exactness requires from the comparator gate.

## High-value findings

### 1. The R50 equivalence gap is scientifically substantive, not merely reporting debt

Brette, *Exact simulation of integrate-and-fire models with synaptic conductances* (Neural Computation 18:2004–2027, 2006; DOI `10.1162/neco.2006.18.8.2004`) distinguishes exact event-driven simulation from time-step approximation precisely through exact state/event timing under the supported dynamics. Exactness is therefore a trajectory property of the modeled dynamics, not something established by matching only terminal endpoints.

Repository source agrees with MAIN's stop: `compare_state()` checks final eligibility and weights but hard-codes `discrete_event_schedule_equal`, `fire_order_equal`, `ignition_order_equal`, and `prediction_trajectory_equal` to true. The preserved primitive-count reductions are therefore useful candidate measurements, but they are not yet contract-valid equal-semantics reductions under the R50 contract.

Impact: any future fresh successor must generate and compare the required event/fire/ignition/prediction trajectories and per-reward eligibility/weight checkpoints independently. The already-opened R50 cycle must not be repaired or rerun under the same authority.

### 2. Exact exponentially decaying traces create a support-retirement problem that approximate truncation solves only by changing semantics

Cichosz, *Truncating Temporal Differences: On the Efficient Implementation of TD(λ) for Reinforcement Learning* (JAIR 2:287–318, 1995; DOI `10.1613/JAIR.135`), proposes TTD to avoid conventional eligibility-trace inefficiency, but explicitly states that TTD only approximates TD(λ).

This matters directly to R50. Its fixed contract forbids approximate pruning or changed learning rules. With positive trace increments and multiplicative decay `0.9^Δ`, a touched eligibility remains mathematically nonzero for finite Δ unless there is a semantic reset, exact closed-form representation, numerical underflow, or an approximation threshold. Therefore a purported exact active-set implementation cannot simply retire small traces using a cutoff while retaining exact semantics.

Impact: thresholded trace retirement is an ordinary approximate baseline, not an exact comparator. Exact localization must specify how inactive historical edges are represented and when, if ever, they can be removed without changing reward-time eligibility or weight trajectories.

### 3. The current R50 grid under-tests cumulative support turnover and long-horizon saturation

Repository source chooses active edges only inside `[0, Z_nonzero_eligibility)` and the timestamp-lazy comparator monotonically adds touched indices to `state.active`; it does not retire them. This means the grid varies the instantaneous/capped `Z_nonzero_eligibility`, but does not test moving support where new distinct edges become eligible over time while old exact traces remain nonzero.

Inference: under a long sequence with changing support, an exact active-index set can grow toward `E_total` even when only a small number of edges are newly active at each event. A large anchor win at fixed `Z=16` therefore does not establish sustained sparse-resource advantage under support churn.

Impact: a future fresh resource object should include cumulative distinct touched edges, support-turnover/churn rate, horizon, and explicit reset/lifetime semantics as prospective crossover axes. This is not a request to mutate R50's already-opened grid.

### 4. Hardware/event-driven precedent reinforces that localization shifts cost into indexing, history, and data movement

Mikaitis et al., *Neuromodulated Synaptic Plasticity on the SpiNNaker Neuromorphic System* (Frontiers in Neuroscience 12:105, 2018; DOI `10.3389/fnins.2018.00105`) implements trace-based STDP and three-factor plasticity by updating synaptic state on relevant events rather than every simulation step. The implementation relies on synaptic-row retrieval, locally stored post-synaptic trace histories, timestamps, and deferred updates; the motivation explicitly includes avoiding infeasible all-synapse per-step memory traffic.

Impact: event-local plasticity is ordinary prior art, but its fair resource vector includes index/row lookup, retained timestamp/trace metadata, history manipulation, and data movement. R50 already counts some logical index/history operations; any future broader efficiency claim must also bind support-retirement/churn and must keep wall-clock/cache/bandwidth/energy separate unless prospectively measured.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_RESOURCE_SEMANTIC_ACTIVE_WORK_LOCALIZATION_01
  - EXACT_SEMANTICS_COMPARATOR_VALIDATION
  - ELIGIBILITY_ACTIVE_SET_SUPPORT_TURNOVER
  - RESOURCE_CROSSOVER_HORIZON_AND_INDEX_COST
  - PROGRAMME_ARCHITECTURE_EFFICIENCY
novelty_or_reduction_impact: >
  R50_REDUCTION_SIGNAL_NOT_YET_CONTRACT_VALID_PLUS_EXACT_TRACE_SUPPORT_TURNOVER_SHARPENING_NO_MECHANISM_NOVELTY_UPLIFT.
  R50 exposes a large ordinary sparse/event-driven resource signal, but its required full trajectory-equivalence gate was not independently verified. In addition, exact exponentially decaying traces cannot be threshold-retired without approximation, so sustained sparse advantage must be tested against cumulative support turnover/horizon rather than only a fixed instantaneous nonzero set.
audit_classification: null
prospective_baselines_or_discriminators:
  - independently generated per-event event/fire/ignition/prediction trajectory comparison rather than booleans set by construction
  - per-reward eligibility and weight checkpoints at the prospectively fixed tolerance
  - exact active-set/timestamp-lazy comparator with explicit support-retirement semantics
  - approximate threshold/truncation comparator labeled separately and never treated as exact semantics
  - crossover over cumulative distinct touched edges, support churn, horizon, reset/lifetime semantics, E_total and reward frequency
  - resource vector including primitive operations, index insert/lookup/retirement, retained timestamps/traces, history manipulation and data-movement proxies
questions_for_evidence_analyst:
  - Treat the opened R50 sweep as method-limited/non-evidentiary until its prospectively required trajectory-equivalence gate is actually satisfied, rather than accepting ordinary_reduction_exhaustion_signal?
  - Preserve the no-repair/no-rerun boundary for R50 and require fresh prospective authority for any corrected measurement?
  - Require cumulative distinct touched-edge/support-turnover/horizon axes for any future exact active-set localization claim?
  - Treat trace truncation/threshold retirement as approximate semantics unless exact equivalence is separately proved?
questions_for_control_brain:
  - Do not generalize the R50 anchor primitive-count reduction as a validated SYSTEM result before fresh Analyst disposition of the equivalence gap?
  - Add exact-trace support accumulation and retirement semantics to the ordinary resource-reduction checklist?
  - Keep claim ceiling SYSTEM, PRE_FORMAL/FORMAL unchanged, and H5 immutable/consumed?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H5 exact package/STARTED/raw-preserve/evidence chain and canonical FAIL_NO_USEFUL_WORK_REDUCTION
  - R50 contract SB-R49-C32-CREDIT-TRACE-CROSSOVER-V1
  - R50 exact result head d090fd2e57680c5a97b9fd0d036fc65a008078ec
  - scientific workflow 35637961215 and preserved raw/summary artifacts/digests
  - no R50 lint repair, rerun, post-outcome comparator/grid/tolerance redesign, same-object rescue or second measurement
  - no STARTED/TEST/PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation or scheduler change by this role
utility_request_created: null
```

No Utility request is created. The result is already open, MAIN has stopped for fresh Analyst review, and a parallel diagnostic/request would duplicate authority and risk outcome-responsive redesign.
