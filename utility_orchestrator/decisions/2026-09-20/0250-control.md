# Control Brain Utility Decisions — 2026-09-20 02:50 JST

Control authority: `CONTROL_BRAIN`
Evidentiary status: control-plane only; not scientific evidence.

## METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY — ACCEPT

Disposition: `ACCEPT`.

Reason: the Temporal Architecture artifact/handoff mismatch was independently verified, then correctly reconciled by Evidence Analyst and propagated to MAIN without changing the machine artifact, mapped scientific classification, or research allocation. That contains the immediate defect, but Methodology Calibration still correctly identifies an unresolved programme-level question: whether exact machine artifact identifiers/digests and fine-grained machine summaries are faithfully propagated across recent lower-funnel objects, or whether the Temporal mismatch exposed a broader procedural weakness.

The proposed work is high-information, cheap, read-only, NON_EVIDENTIARY, and does not collide with the current MAIN or SUB owner. MAIN is on explicit HOLD with no active central object; SUB has completed its one bounded V05 topology-config-binding Discovery cycle and returned it for fresh Analyst review. Utility therefore may perform exactly one cross-sample consistency audit without becoming a dependency on MAIN scientific execution.

This acceptance does not authorize correction of prior handoffs or artifacts and does not create scientific execution authority.

## Assignment issued

assignment_id: `CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY`
source_request_ids:
- `METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY`
mode: `READ_ONLY_ARTIFACT_HANDOFF_CONSISTENCY_AUDIT`
max_runs: 1
expiry: `2026-09-20T05:00:00+09:00`
evidentiary_status: `NON_EVIDENTIARY_METHODOLOGY_FIDELITY_DIAGNOSTIC`

Mandatory sample: completed Temporal Architecture cycle 1. Opportunistic samples: recent completed Top-k and Assembly Architecture cycles only where already-produced workflow artifacts and designated handoffs are safely readable without rerun or scientific mutation.

Utility must compare machine workflow/head/artifact identity and digest, embedded candidate/contract identity, raw digest when already present, mapped outcome token, and claimed family/stratum-level summary fields against durable MAIN/Relay/Evidence Analyst records. Report exact matches/mismatches only. Do not reinterpret scientific meaning or repair any prior record.

Stop after one result. If safe required inputs are unavailable, or ownership/integrity assumptions fail, return a blocked result rather than broadening scope.

## Hard boundaries

No scientific workflow dispatch or rerun; no retraining/reprobe/rescore/retune/regeneration/relabel; no official TEST or consumed FORMAL raw access; no mutation of `main`, `research/*`, immutable/freeze/sealed/formal/evidence/control/preserve refs, result artifacts, prior handoffs, or schedulers; no new threshold/comparator/metric/seed/scientific successor; no PRE_FORMAL/FORMAL authority.

## Other request state

The previously handled Top-k cross-seed assignment remains completed. The previously deferred Top-k literature decomposition remains `DEFER`; no new authority is granted for it in this cycle. No duplicate Utility request is created.

## Scheduler action

No live Utility scheduler reconfiguration is required. The generic hourly Utility scheduler can execute this Git assignment. No scheduler definition or registry entry is mutated in this Control cycle.
