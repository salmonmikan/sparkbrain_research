# SparkBrain Methodology Calibration Audit — R80

- schema_version: `2`
- generation_id: `METHCAL-20260923T121735+0900-R80-9C4F7A12`
- produced_at: `2026-09-23T12:17:35+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T111832+0900-R79-5B7C21D4`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

Two material control/methodology changes are present while the hard scientific integrity floor remains unchanged.

First, Control R41 now supplies machine-resolvable schema-v2 authority for the already-existing PF-R1 preservation request. The authority is narrowly bounded to retrieving the existing `raw.json` / `summary.json` bytes, verifying hashes, and persisting NON_EVIDENTIARY provenance. It explicitly forbids rerun, reconstruction, regeneration, rescore, retune, scientific-authority creation, or mutation of consumed/formal evidence. This resolves the prior *missing-authority* calibration defect, but preservation is not yet complete: the Utility branch remains unchanged at `b18a1d76...`. H7 therefore remains held. Preservation completion must still be followed by a later fresh Analyst exact-head review; preservation itself is not FORMAL authority.

Second, candidate #34 R2 is correctly stopped before response-bearing execution because its generated prospective closure is bound to a different Analyst authority string than the canonical Evidence Analyst R92. The authoritative research implementation contains `ANALYST_AUTHORITY = EVA-20260923T110053+0900-R92-A7B61F3C`, while the designated Evidence Analyst R92 is `EVA-20260923T105725+0900-R92-6B8E31D4@a05ab3f...`. No normalization or inferred equivalence is methodologically acceptable. Because no candidate response has been executed or exposed, this is a provenance/control-plane binding defect, not scientific-result contamination.

A repair that changes only the Analyst authority pointer/binding and consequent hashes, while proving every scientific field and meaning is unchanged, is calibrated as `SCIENCE_INVARIANT_REPAIR` / hash-plumbing-provenance repair. If metric/scorer meaning, thresholds/tolerances, comparator/reduction meaning, seed/exclusion policy, intervention, resource/privilege contract, hypothesis, falsifier, success criterion, or other scientific semantics change, the repair is science-affecting and must follow the appropriate prospective revision rule. Candidate #34 must remain stopped for response execution until exact authority reconciliation, NON_RESULT validation, and fresh review.

Independent repository/evidence re-fetch confirms stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, authoritative `evidence/*` remains exactly five tag objects, and tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. H7 R5 remains at `2f30b93f...`. No fresh FORMAL identity consumption or historical evidence rewrite is observed.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| OPEN science-affecting prospective pre-result revision | `KEEP` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| candidate #34 exact canonical Analyst authority binding | `TIGHTEN` |
| candidate #34 fail-closed stop on authority mismatch | `KEEP` |
| authority-pointer/hash-only repair with identical scientific semantics | `KEEP` |
| silent authority normalization/equivalence inference | `TIGHTEN` |
| candidate #34 response execution before authority reconciliation | `TIGHTEN` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 as mandatory reassessment | `KEEP` |
| additional cycle with distinct prospective information gain | `KEEP` |
| development results counted as independent confirmation | `TIGHTEN` |
| repeated result-bearing PRE_FORMAL live stress case | `INSUFFICIENT_EVIDENCE` |
| PRE_FORMAL as genuine development | `KEEP` |
| preformal_eligible distinct from READY | `KEEP` |
| READY = informative next test, not prior success | `KEEP` |
| HIDDEN_SECOND_FORMAL_GATE | `KEEP` — false |
| H7 PREIDENTITY COMPLETE distinct from FORMAL authority | `KEEP` |
| PF-R1 exact-byte preservation requirement | `KEEP` |
| PF-R1 machine-resolvable Control assignment | `KEEP` |
| PF-R1 preservation execution state | `TIGHTEN` |
| Utility default-deny before machine authority | `KEEP` |
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

1. **Are development-phase semantics implemented consistently end-to-end?** Consistent through the currently observed pre-result repair boundary. #34 remains OPEN_DEVELOPMENT and no response was exposed; the authority mismatch is safely stopped. A fresh post-HUMAN-005 CONSUMED_ONE_WAY completion remains unobserved.
2. **Is cycle 3 a hard terminal cap?** No. #34 reached cycle 4 for a prospectively identified information/provenance closure, while H7 stopped after its useful preidentity work closed.
3. **Are repair classes distinguished correctly?** Yes if the #34 repair is strictly authority-pointer/hash-plumbing with unchanged scientific semantics. Any scientific-field change must not be smuggled into that repair.
4. **Are development reruns/retunes laundered as independent evidence?** No laundering is observed. #34 R2 has no candidate response, and H7 tooling/preidentity work has confirmatory credit zero. A repeated result-bearing PRE_FORMAL live series remains unobserved.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** H7 R4→R5 remains a positive case. PF-R1 durability is still pending, although machine authority now exists.
6. **Is FORMAL one-way integrity unchanged?** Yes. Stable main/evidence tags are unchanged; formal/sealed/freeze tags remain empty; no fresh identity/result consumption is observed.
7. **Are legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured?** No manufacture is observed. A specifically fresh MECHANISM successor from a terminal SYSTEM object remains unobserved.
8. **Is PRE_FORMAL development rather than hidden FORMAL?** Yes. #34 is eligible but NOT_READY and can undergo bounded non-result provenance repair without needing prior comparator/falsifier victory.
9. **Are terminal semantics and candidate supply calibrated?** Yes/improving. Two MECHANISM lineages remain available (H7 held; #34 open) without claim inflation.
10. **Is PASS reachable without weakening standards?** Yes. H7 is `REALISTIC_NEAR_TERM_CONDITIONAL`; the former missing-authority blocker is now narrowed to Utility preservation completion plus later fresh Analyst one-way review.

## Risk calibration

False-positive risk remains `MODERATE_WATCH`. If #34 were allowed to run under an authority string that does not match the canonical Analyst generation, the scientific response might be technically generated but its prospective authorization provenance would be ambiguous. Existing raw/holdout/evaluator gates also remain open for H7.

False-negative/opportunity-cost risk is `LOW_TO_MODERATE_WATCH_IMPROVING`. Control R41 removes the previous PF-R1 missing-authority deadlock. #34 is paused on a narrow provenance repair rather than terminalized or forced into a new scientific object.

Moving-goalpost/rescue risk is `LOW_WATCH_IMPROVING`: the #34 mismatch was found before response exposure; the permitted repair need not alter scientific meaning.

Over-terminalization risk is `LOW_WATCH_IMPROVING`: neither H7 nor #34 is killed merely because a control/provenance gate remains open.

## Development-iteration calibration

Candidate #34 is an important distinction case. Its R2 non-result closure code is explicitly bound to an Analyst authority identifier. That identifier does not equal the canonical designated R92 authority. The programme correctly refuses to treat similar labels or matching R92 sequence numbers as equivalence.

Repair may remain same-object and same-R2 only if it is strictly provenance/hash plumbing: replace/reconcile the authority binding to the canonical R92 record, preserve the scientific contract fields and their meaning, regenerate dependent non-result closure hashes as necessary, validate without response-bearing execution, and STOP for fresh review. This is not a reason to create a new candidate, and it is not evidence.

PF-R1 supplies the complementary positive case. The earlier default-deny was correct while no machine authority existed. R41 now creates exact bounded authority, so continued permanent refusal would become over-conservative once Utility consumes that assignment. The calibrated next step is existing-byte preservation only, not rerun or reconstruction.

## Funnel observability / mechanism supply

Canonical funnel remains inherited from Evidence Analyst R92 because no newer Analyst generation exists: `35 = 14 MECHANISM / 21 SYSTEM`, `TERMINAL_FOR_CURRENT_OBJECT 32`, `OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`, PRE_FORMAL eligible/READY `2/1`, fresh FORMAL authority `0`, historical official consumed identities `7`, classification `35/35`.

Control R41 and the live #34 branch are treated as operational/provenance overlays only; they do not recanonicalize the population.

Mechanism-supply health is `TWO_MECHANISM_LINEAGES_H7_FORMAL_HOLD_CAND34_OPEN_R2_PROVENANCE_HOLD_WITH_SYSTEM_DISCOVERY_BACKUP_QUALITY_FLOOR_INTACT`.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. #34 does not need prior scientific victory to regain READY; it needs exact prospective authority/contract closure and an informative next test. Non-result validation is not evidence.

Repeated PRE_FORMAL observations, when eventually used, must remain one correlated development sequence rather than independent confirmation.

H7 pass reachability improves from the prior generation because machine authority for PF-R1 exact-byte preservation now exists. It is still conditional: Utility must preserve existing bytes only; then a later fresh Analyst must re-fetch the unchanged H7 R5 head and explicitly decide one-way authority. Prediction-only raw, immutable preserve before target-side scoring, concealed evaluation, no-clobber/collision, and exact binding remain mandatory.

## Utility request

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` now has bounded Control R41 machine authority, but Utility execution is not yet observed. No duplicate request, rerun, reconstruction, regeneration, retune, or rescore is justified.

## Prospective recommendations

- Keep candidate #34 response-bearing execution stopped while its bound Analyst authority differs from canonical R92.
- Reconcile only the exact authority/provenance binding and dependent hashes if all scientific fields and meanings remain unchanged. Treat any scientific-semantic delta as science-affecting, not plumbing.
- After repair, run NON_RESULT validation only and STOP for fresh Analyst/Control review before any candidate response.
- Let Utility consume the existing PF-R1 Control assignment and preserve existing bytes only; fail closed if the originals are unavailable.
- Even after PF-R1 preservation, keep H7 stopped until a later fresh Analyst exact-head review explicitly authorizes any one-way step.
- Preserve all existing raw-before-score, preserve-before-read, concealed-evaluation, exact-binding and no-historical-rewrite guards.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: FORMAL non-consumption `HIGH`; candidate #34 exact authority-binding mismatch `HIGH`; pre-response fail-closed calibration `HIGH`; PF-R1 Control machine authority issuance `HIGH`; PF-R1 preservation completion `NOT_OBSERVED`; fresh consumed-FORMAL end-to-end `UNOBSERVED`; fresh specifically SYSTEM→MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will #34 R2 authority binding be reconciled exactly to canonical R92 without changing scientific fields or meaning?
- Will the repaired R2 remain NON_RESULT-only and stop for fresh review before any response-bearing execution?
- Will Utility use the new PF-R1 assignment to preserve only existing bytes without rerun/reconstruction/rescore?
- After PF-R1 preservation, will H7 remain stopped until a later fresh Analyst exact-head review?
- When repeated result-bearing PRE_FORMAL observations eventually occur, will they remain one correlated development sequence rather than independent confirmation?

## Authoritative refs used

- prior Methodology: `METHCAL-20260923T111832+0900-R79-5B7C21D4@ba219b4c4c9c06913f151e61b2d70ef7cd9a60ab`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-20260923T115056+0900-R41-4C156929@27b6531b6b3a1d941a484aeee012d5c59fe63d79`
- Evidence Analyst: `EVA-20260923T105725+0900-R92-6B8E31D4@a05ab3f655a23eabd84c910ba337d64a948c168a`
- Independent Audit: `R8@6755579f5f21b19ca90788c948d8126529b648c6`
- Utility: `ops/utility-orchestrator-requests@b18a1d76c05efbbfacb9618ac1ca1e9941b17555`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- H7 R5: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- candidate #34 R2: `research/main-cand34-assembly-route-preformal-r92-cycle4@1f9c6cec8be0af900a801de17dcc91e57dd71d7a`
- #34 R2 bound authority: `EVA-20260923T110053+0900-R92-A7B61F3C` (noncanonical mismatch)
- evidence tags: 5; formal/sealed/freeze tags: none
