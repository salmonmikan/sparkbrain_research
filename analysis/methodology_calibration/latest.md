# SparkBrain Methodology Calibration Audit — R84

- schema_version: `2`
- generation_id: `METHCAL-20260923T152244+0900-R84-5D4A8C21`
- produced_at: `2026-09-23T15:22:44+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T143315+0900-R83-8B72F1C6`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The hard scientific integrity floor remains unchanged. Since R83, candidate #34's one-shot PRE_FORMAL response executor received exactly one observed repair: removal of an unused `typing.Any` import. Independent commit inspection shows a one-line import deletion and no change to cueing, intervention, timing, observables, comparator, resource contract, thresholds/tolerances, claim, falsifier, success criteria, queue semantics, or response meaning. The repaired exact executor head is `8ce961dc88fb52afa6399093fce1e3de7e982f2b`, and generic CI run `35824098828` completed successfully on that exact head.

Evidence Analyst R94 then prospectively re-fetched and bound the repaired exact executor head while preserving the already-closed R2 scientific contract at `43d0f25541a3c447d4c7156303647ae94f3119f4`. R94 authorizes exactly one bounded response-bearing PRE_FORMAL development execution, requires raw preservation before interpretation, requires STOP on the first meaningful exposure, grants zero confirmatory credit, and grants no FORMAL authority. This is a strong positive implementation of HUMAN-20260922-005: an implementation defect was repaired science-invariantly before exposure, then the exact repaired implementation was freshly rebound before any result-bearing execution.

No response-bearing execution or response workflow dispatch is observed as of this audit. Candidate #34 therefore remains `OPEN_DEVELOPMENT`, READY, zero response exposure, zero confirmatory credit. The next material calibration boundary is the first live OPEN_DEVELOPMENT→RESULT_EXPOSED_DEVELOPMENT transition. On first meaningful response, raw bytes must be preserved unchanged before interpretation and the object must return to Analyst before any repeat response or science-affecting redesign. R94 does not authorize repeated outcome-seeking execution.

H7 remains FORMAL-held. Its R5 research head remains unchanged at `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; no `control/h7*` branch ref is present. PF-R1 exact-byte preservation remains blocked by the non-scientific Control↔Utility pointer divergence: Control R42 carries active bounded preservation authority while Utility `assignment/current` remains IDLE. Utility continues to fail closed and has not rerun/reconstructed/regenerated/rescored PF-R1. No duplicate methodology Utility request is warranted.

Independent repository/evidence re-fetch confirms stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` remains exactly five annotated tag objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. No fresh FORMAL identity/result consumption or historical evidence rewrite is observed.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| candidate #34 READY based on informative next test rather than prior success | `KEEP` |
| exactly one bounded PRE_FORMAL development response authority | `KEEP` |
| additive response executor as implementation of frozen R2 semantics | `KEEP` |
| unused-import repair as SCIENCE_INVARIANT_REPAIR | `KEEP` |
| exact repaired executor re-binding before response | `KEEP` |
| exact executor/source/input provenance before response | `TIGHTEN` |
| green implementation CI counted as scientific support | `TIGHTEN` |
| science-affecting delta disguised as executor/plumbing repair | `TIGHTEN` |
| first meaningful response triggers RESULT_EXPOSED policy | `KEEP` |
| live OPEN→RESULT_EXPOSED transition after first response | `INSUFFICIENT_EVIDENCE` |
| repeat response under same READY authority after meaningful exposure | `TIGHTEN` |
| outcome-responsive science-affecting change | `TIGHTEN` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 as mandatory reassessment | `KEEP` |
| additional cycle with distinct prospective information gain | `KEEP` |
| development observations as independent confirmation | `TIGHTEN` |
| repeated result-bearing PRE_FORMAL live stress case | `INSUFFICIENT_EVIDENCE` |
| PRE_FORMAL as genuine development | `KEEP` |
| preformal_eligible distinct from READY | `KEEP` |
| READY = informative next test, not prior success | `KEEP` |
| HIDDEN_SECOND_FORMAL_GATE | `KEEP` |
| H7 PREIDENTITY COMPLETE distinct from FORMAL authority | `KEEP` |
| PF-R1 exact-byte preservation requirement | `KEEP` |
| PF-R1 original artifact availability | `KEEP` |
| Control↔Utility assignment pointer consistency | `TIGHTEN` |
| PF-R1 preservation execution state | `TIGHTEN` |
| Utility default-deny until exact assignment reconciliation | `KEEP` |
| duplicate request/rerun to bypass preservation flow | `TIGHTEN` |
| raw-before-score as file ordering only | `CLARIFY` |
| literal target-blind prediction raw | `TIGHTEN` |
| immutable preserve before target-side scoring | `TIGHTEN` |
| post-preserve scorer recomputation | `TIGHTEN` |
| target-sidecar independence | `TIGHTEN` |
| fresh concealed evaluation surface | `TIGHTEN` |
| exact source/runner/scorer/preserver/runtime/input binding | `TIGHTEN` |
| current-object claim ceiling | `KEEP` |
| same-object post-outcome SYSTEM→MECHANISM uplift ban | `KEEP` |
| fresh SYSTEM→MECHANISM successor specifically | `INSUFFICIENT_EVIDENCE` |
| TERMINAL_FOR_CURRENT_OBJECT closes only current object | `KEEP` |
| classification completeness | `KEEP` |
| MAIN MECHANISM priority | `KEEP` |
| genuine SYSTEM-over-comparable-MECHANISM exception | `INSUFFICIENT_EVIDENCE` |
| theory-backward quality floor | `KEEP` |
| NO_COHERENT_MECHANISM_TARGET liveness | `KEEP` |
| protected/adaptive-evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** Consistent through OPEN development, READY, exact implementation repair and fresh pre-response binding. The first live result exposure transition and a fresh post-HUMAN-005 CONSUMED_ONE_WAY completion remain unobserved.
2. **Is cycle 3 a hard terminal cap?** No. Candidate #34 legitimately continued beyond cycle 3 to resolve prospectively identified causal-opportunity and execution-integrity questions. It is now authorized for one informative response rather than continued cycles for activity.
3. **Are repair classes distinguished correctly?** Yes in the observed update. The new repair deletes one unused import only. The earlier R2 scientific redesign was prospectively versioned; no science-affecting meaning was smuggled through the lint repair.
4. **Are development reruns/retunes laundered as independent evidence?** No. No R2 response has executed, green CI has zero confirmatory credit, and R94 explicitly authorizes only one bounded response. Repeated result-bearing behavior remains untested.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** H7 R4→R5 remains a positive versioning case. PF-R1 exact-byte durability is still pending despite the original artifact remaining available.
6. **Is FORMAL one-way integrity unchanged?** Yes. Main/evidence refs are unchanged; formal/sealed/freeze tags remain empty; no fresh FORMAL consumption is observed.
7. **Are legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured?** No manufacture is observed. A specifically fresh MECHANISM successor from a terminal SYSTEM object remains unobserved.
8. **Is PRE_FORMAL development rather than hidden FORMAL?** Yes. #34 READY rests on a well-defined informative next test and implementation integrity, not prior scientific victory. CI success is not evidence.
9. **Are terminal semantics and candidate supply calibrated?** Yes/improving. #34 remains a viable MECHANISM lane, H7 is held rather than killed, and #35 remains SYSTEM without claim inflation.
10. **Is PASS reachable without weakening standards?** Yes. H7 remains `REALISTIC_NEAR_TERM_CONDITIONAL`; PF-R1 pointer reconciliation and exact-byte preservation, followed by fresh unchanged-R5 Analyst review, remain necessary.

## Development-iteration calibration

Candidate #34 is now an especially strong positive case for the development-axis policy. A pre-response implementation failure occurred, the repair was narrowly science-invariant, the repaired exact implementation was independently rebound, and no scientific result was generated during repair. This is legitimate iteration rather than evidence manipulation.

The crucial next rule is one-way at the development-result boundary: the first meaningful response must end OPEN_DEVELOPMENT for this revision. Raw must be durably preserved before interpretation. Any second response or science-affecting redesign requires fresh post-exposure review; repeated execution until a preferred outcome appears would be over-permissive rescue tuning.

Green CI and exact source binding are attribution/integrity prerequisites only. They must not become a hidden second FORMAL gate requiring scientific success, nor be credited as confirmatory evidence.

## Risk calibration

False-positive risk remains `MODERATE_WATCH`. The principal risk has shifted from a hidden science-affecting lint repair to what happens after the first development response: counting it as confirmation, repeating execution under the same authority, or adapting scientific conditions after seeing the outcome without explicit versioning.

False-negative/opportunity-cost risk remains `LOW_TO_MODERATE_WATCH_IMPROVING`. The lint defect is closed without scientific terminalization or demotion, and R94 permits the informative next test. H7 still incurs avoidable non-scientific delay from the Control↔Utility pointer divergence.

Moving-goalpost/rescue risk remains `LOW_WATCH_IMPROVING`: the repair was one-line and semantics-invariant, R2 remains closed, and exact repaired execution code was rebound before exposure.

Over-terminalization risk remains `LOW_WATCH_IMPROVING`: #34 is allowed to proceed, H7 remains viable despite provenance hold, and #35 stays a separate SYSTEM line.

## Funnel observability / mechanism supply

Evidence Analyst R94 is the newest canonical authority: `35 = 14 MECHANISM / 21 SYSTEM`; lifecycle `ACTIVE 0 / QUEUED 2 / HOLD 1 / TERMINAL_FOR_CURRENT_OBJECT 32`; development `OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`; PRE_FORMAL eligible/READY `2/2`; fresh FORMAL authority `0`; historical official consumed identities `7`; classification `35/35`.

Operational executor/CI state does not recanonicalize the funnel before a new Analyst generation.

Mechanism-supply health is `TWO_MECHANISM_LINEAGES_CAND34_READY_EXACT_EXECUTOR_GREEN_PRE_RESPONSE_PLUS_H7_FORMAL_HOLD_WITH_SYSTEM_DISCOVERY_BACKUP_QUALITY_FLOOR_INTACT`.

## Claim-type findings

Candidate #34 remains MECHANISM ceiling with narrow READY scope: one development-only local route-influence response under the frozen R2 source-only cue/intervention family. A positive development response cannot alone establish unique topology, broad perturbation informativity, robust polychrony, irreducibility or novelty; a null cannot establish absence of route causality outside the frozen local surface.

H7 remains MECHANISM and FORMAL-held without new evidence. Candidate #35 remains SYSTEM / OPEN_DEVELOPMENT. No same-object SYSTEM→MECHANISM uplift is observed.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. Candidate #34 is scientifically READY and implementation-ready after green CI, but has zero scientific support from the executor/CI itself. Exactly one bounded development response is prospectively authorized. After first meaningful response, it must transition to RESULT_EXPOSED before any repeat or redesign; correlated PRE_FORMAL observations must never be accumulated as independent confirmation.

H7 pass reachability remains `REALISTIC_NEAR_TERM_CONDITIONAL`. The obstacle remains pointer reconciliation and exact-byte preservation, not scientific rerun.

## Utility request

No new Utility request is created. Existing scientific preservation request: `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE`. Existing Utility reconciliation request: `UTILREQ-20260923T1323+0900-PFR1-ASSIGNMENT-POINTER-RECONCILIATION`. Preserve existing PF-R1 bytes only; no duplicate request, rerun, reconstruction, regeneration, retune or rescore is justified.

## Prospective recommendations

- Permit candidate #34's already-authorized one bounded PRE_FORMAL response only on the exact repaired executor head and unchanged closed R2 contract.
- Bind exact executor head, closed R2 head, fixed D34-Q002 queue/input identity and raw-output destination/provenance before response execution.
- Preserve raw bytes unchanged before interpretation. On first meaningful exposure, immediately classify #34 as RESULT_EXPOSED_DEVELOPMENT and return to Analyst before any repeat response or science-affecting redesign.
- Keep confirmatory credit zero for the development observation and any later correlated PRE_FORMAL sequence.
- Do not reinterpret green CI or exact provenance as scientific support.
- Reconcile PF-R1 Control authority with Utility assignment/current, preserve only the still-available original bytes, and never rerun/reconstruct/rescore.
- After PF-R1 preservation, keep H7 stopped until a later fresh Analyst exact-head one-way review.
- Preserve prediction-only raw, immutable preserve-before-score, concealed evaluation, exact binding, collision/no-clobber and no-historical-rewrite guards.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: FORMAL non-consumption `HIGH`; candidate #34 one-line unused-import repair classification `HIGH`; repaired executor CI success `HIGH`; R94 exact repaired-head binding and one-response scope `HIGH`; candidate #34 response non-exposure `HIGH`; future OPEN→RESULT_EXPOSED transition `UNOBSERVED`; repeated result-bearing PRE_FORMAL behavior `UNOBSERVED`; PF-R1 Control↔Utility pointer divergence `HIGH`; PF-R1 preservation completion `NOT_OBSERVED`; fresh consumed-FORMAL end-to-end `UNOBSERVED`; fresh specifically SYSTEM→MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will #34 be executed at most once under R94 and stopped immediately after the first meaningful response?
- Will raw development output be durably preserved unchanged before interpretation and before any repeat/design change?
- Will the first response trigger an explicit RESULT_EXPOSED_DEVELOPMENT transition with confirmatory credit remaining zero?
- Will any science-affecting redesign after exposure be versioned/fresh rather than repaired in place?
- Will Utility reconcile `assignment/current` to existing PF-R1 Control authority and preserve only original bytes without rerun/reconstruction/rescore?

## Authoritative refs used

- prior Methodology: `METHCAL-20260923T143315+0900-R83-8B72F1C6@fefb90a9892bc5919fc25cad8f23df9a8bf3f5f2`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-20260923T125800+0900-R42-7C9E41B2@7035ace9b0ef980602dcb124e8974be5640d7377`
- Evidence Analyst: `EVA-20260923T150251+0900-R94-8E6A31C4@5cee6ef496eb9465550fb9c0be5295e587027dfb`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- candidate #34 closed R2: `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`
- candidate #34 repaired executor: `research/main-cand34-assembly-route-preformal-r93-response@8ce961dc88fb52afa6399093fce1e3de7e982f2b`
- candidate #34 repaired-head CI: `35824098828=success`
- H7 R5: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- Utility mailbox head: `ops/utility-orchestrator-requests@6829ac17ed38cf01a5600dfa83baa45998dc5dc0`
