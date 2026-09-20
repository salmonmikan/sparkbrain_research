# SparkBrain Evidence Analyst — 2026-09-20 08:59 JST

## Executive decision

No new FORMAL scientific evidence exists. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` remains five annotated tags; `formal/*`, `sealed/*`, and tag-based `freeze/*` remain empty. Fresh repository checks also show 13 legacy `freeze/*` branches, preserved `control/*` / `preserve/*` lines, zero repository rulesets, and no new one-way scientific identity.

Two lower-funnel updates are material. MAIN completed `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01` with valid NON_EVIDENTIARY terminal `IMMEDIATE_ONLY_USAGE_BUT_PUBLIC_CONTRACT_UNSPECIFIED`; current supported repository callsites are immediate, while the public contract does not explicitly promise delayed/interleaved credit. SUB independently completed `HOMEOSTASIS_RECEPTOR_DEAD_MASK_DISCOVERY_CYCLE1`: receptor-only spikes can keep public `StabilitySnapshot.dead=false` while the internal reservoir is silent because homeostasis accounts the entire field. This fresh Discovery is promoted to one static Architecture contract characterization as `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01`.

## MAIN result review — delayed outcome

MAIN exact head `c79c5434222a6d018931dc1752e7f0074c23854b` passed ordinary CI `35475862604`. Cycle 1 was static/read-only: no dynamic interleaving probe and no outcome-bearing scientific workflow was run. Raw facts were committed before interpretation under exact bound source/callsite scope.

The fixed repository surface contains one `learn_outcome` definition and three supported callers. Every observed caller invokes `learn_outcome()` after the relevant outcome is known and without an intervening `process_episode()`. `process_episode()` does overwrite the single mutable pending activation/action credit state and `learn_outcome()` carries no episode/decision identity, but there is no explicit supported delayed/interleaved caller and no explicit public immediate-only contract either. The prospectively fixed terminal is therefore `IMMEDIATE_ONLY_USAGE_BUT_PUBLIC_CONTRACT_UNSPECIFIED`.

Analyst disposition: `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01 = HOLD`. This is an API-contract ambiguity / unsupported-use hazard, not a demonstrated supported-path credit defect and not mechanistic novelty. Same-object dynamic cycle 2 is not authorized. A future delayed/interleaved question requires a genuinely fresh prospective object only if independent repository evidence first establishes that delayed/interleaved credit is a supported requirement.

## SUB Discovery review — homeostasis population semantics

SUB exact head `8a2fa2efa7ac13ea7a1a835c14e8ea0f8013d71f` passed exact-head CI `35476878641` and stopped after one bounded NON_EVIDENTIARY Discovery cycle.

The fixed synthetic field contained one receptor unit and one silent internal-reservoir unit. Across six windows, one receptor spike per window produced `dead=false`, `dead_streak=0`, and `active_unit_fraction=0.5` while the internal reservoir remained at `rate_ema=0.0`. Empty control and the matched receptor-filtered shadow both reached `dead=true`, `dead_streak=6`, `active_unit_fraction=0.0`.

Stable source independently confirms the ordinary reduction. `HomeostaticController.observe()` counts every supplied spike, resets `dead_streak` on any nonempty row set, computes `active_unit_fraction` against all field units, and updates rate/threshold state for every unit; there is no receptor filter. The public evaluation path consumes `result.stability.dead` and aggregates `dead_rate`. Thus the effect is a real architecture/testbed observability-contract issue, but it is fully explainable by all-field accounting; it is not a new stability mechanism or computational principle.

SUB review classification: `PROMOTE_TO_ARCHITECTURE_STUDY`. New candidate `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01` is admitted for one static/read-only Architecture cycle. The scientific/API choices still open are the intended population represented by `dead` and `active_unit_fraction`, whether receptor units are intentionally part of the same homeostatic population, and whether supported monitoring/evaluation consumers require reservoir-specific liveness. No matched dynamic comparator is authorized in the same run because choosing a receptor-aware population policy before the supported contract is characterized would bake in a semantic answer.

Claim-type separation is explicit: potential architecture/system-integration, engineering/reproducibility, and research/testbed value are high enough to study; new computational-principle and mechanistic-distinctness support are absent.

## Research funnel and allocation

- `DISCOVERY`: `OPEN`, SUB default, strictly `NON_EVIDENTIARY`.
- `ARCHITECTURE_STUDY`: `ACTIVE_AUTHORIZED_PENDING_MAIN_PROSPECTIVE_BINDING`; MAIN current object `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01`; queued `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` remains behind fresh review.
- `PRE_FORMAL`: `EMPTY_HOLD`; no fresh mechanism survives ordinary reductions strongly enough for admission.
- `FORMAL`: `EMPTY_HOLD`; no fresh formal object, identity, STARTED, TEST, scorer, preserve, or evidence authority.

`main_lane = V05_HOMEOSTASIS_POPULATION_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`.
`sub_lane = BOUNDED_SECONDARY_DISCOVERY`.
`sub_fallback = NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON`.

MAIN owns the entire static Architecture critical path: prospective exact-source/docs/tests/callsite binding, fact-type-appropriate structural extraction, CI/readiness, raw facts before interpretation, terminal mapping, and handoff fidelity. SUB must not continue Homeostasis, Assembly mature-capacity, delayed-outcome, Refractory, Suppression, Top-k/H7, MAIN blockers, Utility/control-plane tasks, or FORMAL/TEST/scoring/preserve/evidence surfaces.

## Current MAIN prospective contract

Cycle 1 is static/read-only only. Bind stable `main`, `src/sparkbrain/v05/homeostasis.py@67b87a4b4c91a7dba41670087a2d1803bb6e3e6c`, the v0.5 brain callsite that supplies `base_result.spikes`, the `StabilitySnapshot` contract, all stable-main evaluation/tests/docs that consume or define `dead`, `active_unit_fraction`, rate/threshold homeostasis, and exact source blobs before interpretation.

Decision-relevant machine facts must use an extraction/validation method appropriate to the fact type; executable structure should prefer AST/typed/structural checks over brittle raw-string matching. Record whether the public/source contract explicitly defines whole-field versus reservoir liveness, whether receptor inclusion is documented or tested, which supported callers consume `dead`/`active_unit_fraction`, and whether any supported contract contradicts all-field implementation. No dynamic receptor-aware comparator, policy change, production modification, official TEST, consumed raw, or formal surface is authorized.

Prospective terminals are fixed before result inspection:

- `EXPLICIT_WHOLE_FIELD_STABILITY_CONTRACT`: implementation and supported contract agree that receptor activity counts toward liveness; STOP and reduce current concern to architecture/engineering note only.
- `EXPLICIT_RESERVOIR_LIVENESS_CONTRACT_WITH_ACCOUNTING_GAP`: supported contract requires reservoir/internal-computation liveness but implementation accounts all field activity; STOP for fresh Analyst review. Any matched dynamic comparator is a fresh object.
- `WHOLE_FIELD_IMPLEMENTATION_WITH_PUBLIC_POPULATION_UNSPECIFIED`: implementation is all-field but supported public meaning is unspecified; STOP/HOLD as API/observability ambiguity.
- `MIXED_OR_CONTRADICTORY_STABILITY_POPULATION_CONTRACT`: docs/tests/callers disagree materially; STOP/HOLD.
- `INVALID_STATIC_CHARACTERIZATION`: discard and STOP.

Every valid terminal returns to fresh Analyst review. No same-run dynamic continuation and no automatic PRE_FORMAL/FORMAL promotion.

## Candidate pool

| Candidate | Classification | Question / information value | Ordinary reduction / open choices | Cycles / promotion condition |
| --- | --- | --- | --- | --- |
| `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01` | `ARCHITECTURE_STUDY` | What population does public homeostatic liveness/stability represent? High Architecture/testbed value, very near. Fresh independent Discovery, not a consumed-line rescue. | All-field accounting may be intentional; receptor-only silent-reservoir state may be edge-case; supported population/consumer semantics are open. | D1/A0. One static contract cycle. Any valid terminal STOPs; dynamic comparator needs fresh authority. |
| `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` | `ARCHITECTURE_STUDY` | Does mature retention create a hard lifetime learning cap under supported horizons? Medium-high Architecture value, near-medium. | Fixed resource budget, immature-only pruning, permanent-memory intent, and unsupported synthetic saturation. | D1/A0. Queued. First bind intended lifecycle and plausible default saturation; no comparator yet. |
| `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01` | `HOLD` | Is delayed/interleaved outcome credit supported? Static cycle found immediate usage but unspecified public contract. | Single pending-slot bookkeeping and unsupported async usage are ordinary explanations. | D1/A1. Closed current question; no dynamic cycle unless fresh supported requirement appears. |
| `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` | `HOLD` | Historical suppression API semantics. | Threshold blockade, retained state, lazy decay; completed artifact also had confirmed static-extractor false negative. | D1/A1/U1. Historical `AMBIGUOUS_CONTRACT` unchanged; no repair/relabel/rerun. |
| `CAND-H7-RESP-01` | `HOLD` | Native online/local responsibility-sensitive mechanism, if one independently appears. | Actual-causality and ordinary local-learning reductions; equal privilege unresolved because no native object exists. | PF0. No queue-filler construction. |

Completed Refractory, Temporal, Top-k, topology-config, Assembly cross-cascade/prototype-lockin, fanout-aliasing and other answered/rejected lower-funnel objects remain historical `do_not_touch` unless materially reframed as genuinely fresh questions.

## External / methodology inputs consumed

Control Brain 08:50 remains a strategic prior only: `FORMAL_HOLD_WITH_ACTIVE_LOWER_FUNNEL`, no doctrine change, and it independently reports the delayed-outcome terminal plus fresh Homeostasis Discovery pending Analyst review. Current repository evidence above determines this allocation.

Literature Scout has no newer run than 06:30; its latest material input remains the Refractory ordinary-reduction boundary and does not alter the current Homeostasis or Assembly ranking. Independent Audit remains H5 `ROBUST_SO_FAR` only for the exact registered aggregate algorithmic-work claim; H5 stays consumed/closed and does not imply a general event-routing/lazy-execution no-go theorem.

Methodology Calibration at 08:20 remains `MIXED_CALIBRATION`. The scientific hard floor and novelty bar remain unchanged. Keep prospective exact binding, raw-before-interpretation, claim-type separation, and stop-after-Architecture-cycle. Tighten only decision-relevant machine-fact extractor fidelity and handoff binding; this Homeostasis static cycle is a suitable real successor decision on which to apply those prospective safeguards.

Repository Steward 07:50 is governance advisory only. Fresh remote checks independently confirm five evidence tags, 13 legacy freeze branches, zero rulesets, Issue #139 open, and PR #148/#149 open/unmerged. These remain governance gaps rather than science blockers.

## Top 3 / GO-STOP

1. MAIN: `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01` static Architecture contract cycle — `HIGH / VERY_NEAR` — **GO_NON_EVIDENTIARY_STATIC_ARCHITECTURE_ONLY**.
2. MAIN future: `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` contract/reachability characterization after #1 fresh review — `MEDIUM_HIGH / NEAR_MEDIUM` — `HOLD_QUEUED_NO_PARALLEL_MAIN_EXECUTION`.
3. SUB: one genuinely independent bounded Discovery or explicit no-op — `MEDIUM / OPTIONAL` — `DISCOVERY_ONLY`.

#1 GO requires exact stable source/docs/tests/callsite scope, terminal mapping, machine-fact validity method, and machine-bound handoff fields to be fixed before interpretation, with ordinary exact-head CI/readiness green. STOP if scope requires a new semantic choice, if a dynamic receptor-aware comparator is desired, if official TEST/consumed/formal surfaces would be needed, on any binding mismatch, or after any valid terminal.

## Integrity / blockers / Utility

Consumed/no-retry identities are unchanged: `c19-external-v2-official-v4`; C19-R1 revision-authority official-v1 and official-v2; `c19-r2-fsa-state-tracker-official-v1`; `pd01-long-history-fading-memory-official-v1`; `ni01-no-ignition-selective-prediction-official-v1`; `h5-event-routing-work-reduction-official-v1`. No rerun, retune, rescore, relabel, post-outcome repair, consumed-identity retry, immutable evidence mutation, research merge, or scheduler mutation is authorized.

Real blockers are: no fresh PRE_FORMAL mechanism beyond ordinary reductions; no fresh FORMAL object/one-way authority; Homeostasis public population semantics are not yet bound; Assembly mature-memory intent and supported/default saturation relevance remain unresolved; delayed-outcome delayed/interleaved support was not established and the current object is closed.

No new Utility request is created. Existing methodology Utility assignments are completed/idle, and both the Homeostasis contract question and Assembly lifecycle question cleanly belong to MAIN scientific ownership rather than the Utility bus.

## Persistence

Persist only `analysis/orchestrator/latest.md`, `analysis/orchestrator/state.json`, and append-only `analysis/orchestrator/history/2026-09-20/0859.md` on `ops/evidence-analyst-handoff` in one fast-forward commit. No immutable evidence/control/preserve ref is modified.