# SparkBrain Research Orchestrator SUB — 2026-09-20 21:46 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17`
- produced_at: `2026-09-20T21:46:00+09:00`
- producer_run_id: `SUB-RUN-20260920T214600+0900-PREDERR-5C8A2F17`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_THEORY_BACKWARD_MECHANISM_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29`
- Evidence Analyst: `EVA-20260920T211647+0900-R20-B6B0AAA2@2d7841171377226d2962424b5926ca4c4b68a2e7`
- MAIN mailbox: `MAIN-20260920T211206+0900-PRIMARY-FUNNEL21-FAILCLOSED-R19-7F4A92C1`; R19 freshness stop is resolved by Analyst R20 and no MAIN scientific object is active
- MAIN last scientific terminal: `MAIN-20260920T201624+0900-PRIMARY-FUNNEL21-ARCHSYS-R19-D4E9B731`, `CAND-V05-ASSEMBLY-CLUSTER-ORDER-SUPPORTED-REACHABILITY-01`
- Control Brain: `CTRL-20260920T205000+0900-R16-5E9A71C3@016a248143dc71380fca28128d564d74aeb4c3f3`
- previous SUB: `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29@59026d651bb141fbfc8a4e99f4c5826531e2af65`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_ENDOGENOUS_PREDICTION_ERROR_MODULATION_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-ENDOGENOUS-PREDICTION-ERROR-MODULATION-01` (`SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL`)
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- recommendation: `REJECT`

Analyst R20 authorizes one fresh bounded SUB Discovery by information gain with prospective typing and terminal/API semantic preflight. MAIN has no active scientific object. This object is independent of the terminal Assembly cluster-order line, does not operate H7, and does not reopen any terminal current object.

## Theory-backward accounting

Before selection: context-conditioned prediction=`MECHANISM`, Assembly cluster order=`SYSTEM`, delayed action responsibility=`MECHANISM` (`2/3`). After selection: Assembly cluster order=`SYSTEM`, delayed action responsibility=`MECHANISM`, endogenous prediction-error modulation=`MECHANISM` (`2/3`). Supply v2.1 remains satisfied; `theory_backward_exception=null`.

## Question / prospective semantics

Question: can learned internal predictive state causally modulate early sensory processing for an otherwise identical subsequent physical pulse without caller-supplied `SignalPulse.prediction_error`?

Hypothesis: if endogenous top-down predictive modulation exists, matched brains differing only in learned predictor state should differ in receptor/lower-field response with caller `prediction_error=0.0`.

Prospective reduction/falsifier: if learned predictor-state arms are identical but a fixed positive-control pulse with caller `prediction_error=1.0` changes receptor emission, the current mechanism object reduces to `CALLER_SUPPLIED_SIGNALPULSE_PREDICTION_ERROR_SCALAR`.

Terminal/API semantic preflight was completed before outcome exposure against exact stable-main `brain.py`, `receptors.py`, `v04/contracts.py`, `prediction.py`, and `v05/contracts.py`. No terminal-relevant accessor/representation changed after outcome exposure.

Research branch: `research/exploratory-sub-endogenous-prediction-error-modulation-20260920`; prospective contract: `f54780589cbd5d18352c91d8b8e5c0266e8104f9`.

## Implementation / observations

Two fresh default brains had identical non-predictor state. Both received the same synthetic mature Assembly identity through predictor API only; arm A learned `future-A x4`, arm B `future-B x4`. Both then received the same single physical pulse with caller `prediction_error=0.0`, learning disabled. A third fresh positive-control brain received the same physical pulse except caller `prediction_error=1.0`.

Observed A/B receptor traces, emitted pulses, lower `v04_result.as_dict()`, and lower spike dictionaries were exactly identical. The positive-control pulse with explicit `prediction_error=1.0` produced a strictly larger receptor `emitted_magnitude` and retained the explicit error scalar on the emitted pulse.

Observed terminal: `CALLER_SUPPLIED_PREDICTION_ERROR_REDUCTION`.

Outcome-bearing commit `7de878bc98f2547a24c95d506ab62ec96fca18d9` had CI `35511156776` success. Final research head `ae88a7bd5b6497b0b104eb87ffc55d07877865fa` has exact-head CI `35511350033` completed success on Python 3.11/3.13 with lint, local readiness, full tests, and bundle validation green.

Interpretation: current native v0.5 learned predictor state does not causally modulate the earlier receptor/lower-field path in this bounded discriminator. Prediction-error sensitivity is reachable through the explicit incoming `SignalPulse.prediction_error` scalar only. No cycle-2 rescue is warranted; a predictor-to-receptor feedback redesign requires a fresh candidate ID and fresh prospective contract.

## Funnel v2.1 proposal

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `mechanism`
- supported_reachability: `PARTIAL`
- functional_consequence: `ABSENT_FOR_ENDOGENOUS_PREDICTOR_TO_RECEPTOR_MODULATION`
- ordinary reductions specified/controlled: `CALLER_SUPPLIED_SIGNALPULSE_PREDICTION_ERROR_SCALAR`
- ordinary reductions unresolved: `[]`
- comparator status: `COMPLETE_AND_EXACT_FOR_MATCHED_INTERNAL_PREDICTOR_ARMS_WITH_POSITIVE_EXTERNAL_ERROR_CONTROL`
- support breadth: `one prospectively fixed matched two-predictor-state DEV intervention plus one caller-supplied prediction-error positive control`
- falsifier: different learned predictor state must alter receptor/lower-field response under identical physical pulse with caller prediction_error fixed at zero
- open scientific choices: `[]`
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

## Completion

Independent ref reconciliation confirmed stable main unchanged, five `evidence/*` tags, zero `formal/*`, zero `sealed/*`, zero tag-based `freeze/*`, H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`, and H5 raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`.

MAIN frontier avoided: terminal Assembly cluster-order supported-reachability object and its branch/successor. H7 was not operated. No FORMAL/TEST/scoring, consumed/frozen identity, preserve/control/evidence ref, or stable-main mutation occurred.

Utility request: none. Consumed identities: none. New FORMAL results: zero. Blocker: fresh Evidence Analyst classification/closure only.

Completion target `ACHIEVED_ONE_THEORY_BACKWARD_ENDOGENOUS_PREDICTION_ERROR_MODULATION_DISCOVERY_CYCLE_AND_REDUCED_TO_CALLER_SUPPLIED_PREDICTION_ERROR` — achieved.
