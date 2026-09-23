# SparkBrain Methodology Calibration Audit — R81

- schema_version: `2`
- generation_id: `METHCAL-20260923T132108+0900-R81-7D3A6C91`
- produced_at: `2026-09-23T13:21:08+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T121735+0900-R80-9C4F7A12`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The hard scientific integrity floor remains unchanged, while candidate #34 now provides a strong positive example of correctly calibrated OPEN_DEVELOPMENT iteration.

The prior R80 audit correctly required exact Analyst authority reconciliation before candidate #34 could proceed, but its practical description of the admissible next change as only an authority-pointer/hash-plumbing repair was too narrow as a description of the already-authorized R2 development transition. The newest canonical Evidence Analyst remains R92, and R92 had already prospectively authorized an explicit same-candidate `PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION` before any response-bearing candidate result was exposed. That authorization explicitly permitted a science-affecting OPEN_DEVELOPMENT revision to repair causal opportunity and claim/observable alignment while preserving R1 non-result provenance and requiring a fresh Analyst READY review before any response.

The authoritative R2 research branch is now `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`. It is bound to canonical R92, contains the explicitly versioned opportunity-aware contract, and prospectively changes cue policy, opportunity policy, observation fields, claim scope and primary reduction in the direction R92 had already authorized. Those are SCIENCE_AFFECTING changes by category, but they are calibrated because they occurred in OPEN_DEVELOPMENT before response exposure, under explicit prospective version authority. They must not be mislabeled as a mere science-invariant pointer repair.

The exact R2 head passed both the dedicated non-result contract workflow `35814951495` and generic CI `35814951496`. The dedicated run produced exactly one non-expired contract artifact (`10730964708`, archive digest `sha256:4df7bac547df7db49c0c68108d8a0d2e40e129f4b0f7ce46ea45cf51c3a08c94`). The implementation explicitly sets response-bearing execution and FORMAL action to false and requires a fresh Analyst READY review. MAIN has subsequently preserved/revalidated the exact non-result contract provenance and remains stopped. This is implementation/provenance closure only, not scientific evidence and not READY.

H7 remains FORMAL-held. The original PF-R1 artifact remains independently available and unexpired (`10680620448`, digest `sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`), so there is still no justification for rerun, reconstruction, regeneration or rescore. Control R42 carries a bounded machine assignment for exact-byte preservation, but the independently re-read Utility `assignment/current.md` remains `IDLE` with no active assignment. The resulting Control↔Utility assignment-pointer divergence is a non-scientific control-plane defect that continues to block preservation and H7 one-way progression.

Independent repository/evidence re-fetch confirms stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, authoritative `evidence/*` remains exactly five annotated tag objects, and tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. No fresh FORMAL identity/result consumption or historical evidence rewrite is observed.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| OPEN science-affecting prospective pre-result revision | `KEEP` |
| candidate #34 R92-authorized opportunity-aware R2 version | `KEEP` |
| candidate #34 exact canonical Analyst authority binding | `KEEP` |
| treating the entire R2 transition as pointer/hash-only repair | `RELAX` |
| R2 non-result contract closure distinct from scientific evidence | `KEEP` |
| R2 green CI/artifact preservation distinct from READY | `KEEP` |
| response-bearing execution before fresh Analyst READY review | `TIGHTEN` |
| new science-affecting edits after closed R2 without fresh prospective review | `TIGHTEN` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 as mandatory reassessment | `KEEP` |
| cycle 4 with distinct pre-result information gain | `KEEP` |
| development results counted as independent confirmation | `TIGHTEN` |
| repeated result-bearing PRE_FORMAL live stress case | `INSUFFICIENT_EVIDENCE` |
| PRE_FORMAL as genuine development | `KEEP` |
| preformal_eligible distinct from READY | `KEEP` |
| READY = informative next test, not prior success | `KEEP` |
| HIDDEN_SECOND_FORMAL_GATE | `KEEP` — false |
| H7 PREIDENTITY COMPLETE distinct from FORMAL authority | `KEEP` |
| PF-R1 exact-byte preservation requirement | `KEEP` |
| PF-R1 original artifact availability | `KEEP` |
| Control↔Utility assignment pointer consistency | `TIGHTEN` |
| PF-R1 preservation execution state | `TIGHTEN` |
| Utility default-deny for PF-R1 until exact assignment reconciliation | `KEEP` |
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

1. **Are development-phase semantics implemented consistently end-to-end?** Consistent through the observed OPEN development boundary. Candidate #34 demonstrates that meaningful science-affecting iteration before response exposure can proceed under an explicit versioned prospective contract while retaining zero confirmatory credit. Fresh post-HUMAN-005 CONSUMED_ONE_WAY completion remains unobserved.
2. **Is cycle 3 a hard terminal cap?** No. Candidate #34 reached cycle 4 because a distinct pre-result causal-opportunity defect created prospectively stated information gain. H7 stopped once its useful preidentity work closed.
3. **Are repair classes distinguished correctly?** The current R2 transition must be classified more carefully than R80: authority reconciliation alone is science-invariant plumbing, but the opportunity-aware cue/observable/reduction changes are science-affecting. They are nevertheless valid because canonical R92 prospectively authorized the explicit R2 OPEN_DEVELOPMENT revision before result exposure.
4. **Are development reruns/retunes laundered as independent evidence?** No laundering is observed. Candidate #34 has no response-bearing R2 result and the non-result workflow/artifact has confirmatory credit zero. A repeated result-bearing PRE_FORMAL live series remains unobserved.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** H7 R4→R5 remains a positive case. PF-R1 exact-byte durability remains pending despite the original artifact still being available.
6. **Is FORMAL one-way integrity unchanged?** Yes. Stable main/evidence tags are unchanged; formal/sealed/freeze tags remain empty; no fresh identity/result consumption is observed.
7. **Are legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured?** No manufacture is observed. A specifically fresh MECHANISM successor from a terminal SYSTEM object remains unobserved.
8. **Is PRE_FORMAL development rather than hidden FORMAL?** Yes. Candidate #34 can undergo a genuine versioned science-affecting development revision before result exposure, yet remains NOT_READY until a fresh Analyst judges the next response-bearing test informative. Prior comparator/falsifier victory is not required.
9. **Are terminal semantics and candidate supply calibrated?** Yes/improving. Two MECHANISM lineages remain available (H7 held; #34 open/closed-nonresult awaiting review) and candidate #35 remains SYSTEM without claim inflation.
10. **Is PASS reachable without weakening standards?** Yes. H7 remains `REALISTIC_NEAR_TERM_CONDITIONAL`: the original PF-R1 bytes are available, but Utility assignment-pointer reconciliation, exact-byte preservation, and a later fresh Analyst exact-head one-way review are still required.

## Risk calibration

False-positive risk remains `MODERATE_WATCH`. The main current risk is treating candidate #34's green non-result contract closure as either READY or scientific support. Existing H7 prediction-only raw, preserve-before-target-side scoring, concealed-evaluation and exact-binding gates also remain open.

False-negative/opportunity-cost risk remains `LOW_TO_MODERATE_WATCH_IMPROVING`. Candidate #34 is no longer blocked by the stale Analyst-authority string, and its genuine development revision was not over-conservatively prohibited. H7 still suffers avoidable throughput friction because Control assignment state and Utility's active-assignment pointer disagree even though the original PF-R1 artifact remains available.

Moving-goalpost/rescue risk is `LOW_WATCH_IMPROVING`: candidate #34's science-affecting R2 changes were authorized and versioned before any response exposure, and R1 non-result provenance remains preserved. The now-closed R2 must not be further changed in response to future results without the appropriate prospective revision boundary.

Over-terminalization risk is `LOW_WATCH_IMPROVING`: neither #34 nor H7 is killed merely because a provenance/control gate is open, and candidate #35 remains a separate SYSTEM successor rather than claim-inflated supply.

## Development-iteration calibration

Candidate #34 is now the strongest live positive example for HUMAN-20260922-005. The correct distinction is not “science-affecting changes are forbidden in PRE_FORMAL”; it is “outcome-responsive scientific changes after meaningful exposure require explicit versioning/fresh succession, while OPEN_DEVELOPMENT may make bounded prospective science-affecting revisions with durable provenance.”

R92 authorized the opportunity-aware R2 revision prospectively after an independent static audit found the R1 causal-opportunity defect and before any candidate response was exposed. The implemented R2 version changes cue strategy, causal-opportunity ledger, response observables, claim scope and primary reduction. Those are correctly classified as SCIENCE_AFFECTING, and their legitimacy comes from the pre-result explicit versioned authority—not from pretending they are science-invariant plumbing.

The exact R2 closure now forbids response-bearing execution and FORMAL action and requires a fresh Analyst READY review. That is calibrated: non-result closure establishes that the proposed next test is executable and prospectively bound, but does not establish that it succeeds scientifically.

PF-R1 remains the complementary RESULT_EXPOSED durability case. Its original workflow artifact is still live and exactly bound, so the only calibrated operation is existing-byte preservation. Re-execution would weaken, not strengthen, methodology integrity.

## Funnel observability / mechanism supply

Canonical funnel remains inherited from Evidence Analyst R92 because no newer Analyst generation exists: `35 = 14 MECHANISM / 21 SYSTEM`, `ACTIVE 0 / QUEUED 2 / NONTERMINAL_HOLD 1 / TERMINAL_FOR_CURRENT_OBJECT 32`, `OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`, PRE_FORMAL eligible/READY `2/1`, fresh FORMAL authority `0`, historical official consumed identities `7`, classification `35/35`.

Control R42 and the live #34 branch are treated as operational/provenance overlays only; they do not recanonicalize the population. Candidate #34 remains MECHANISM / OPEN_DEVELOPMENT / PRE_FORMAL / eligible / NOT_READY. H7 remains MECHANISM / RESULT_EXPOSED_DEVELOPMENT / development READY / FORMAL-held. Candidate #35 remains SYSTEM / OPEN_DEVELOPMENT.

Mechanism-supply health is `TWO_MECHANISM_LINEAGES_H7_FORMAL_HOLD_CAND34_R2_NONRESULT_CLOSED_AWAITING_FRESH_READY_REVIEW_WITH_SYSTEM_DISCOVERY_BACKUP_QUALITY_FLOOR_INTACT`.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. Candidate #34 does not need to have already won its comparator/reduction/falsifier to become READY. It needs a well-defined, informative, prospectively bound next response-bearing test and a fresh Analyst decision.

Repeated PRE_FORMAL observations, when eventually observed, must remain one correlated development sequence rather than independent confirmation.

H7 pass reachability is `REALISTIC_NEAR_TERM_CONDITIONAL`. The original PF-R1 artifact remains unexpired and exactly identified, so the present obstacle is control-plane assignment-pointer reconciliation and preservation—not scientific rerun. Successful preservation still does not itself grant FORMAL authority. A later fresh Analyst must re-fetch unchanged H7 R5 and explicitly decide any one-way step. Prediction-only raw, immutable preserve before target-side scoring, concealed evaluation, no-clobber/collision, and exact binding remain mandatory.

## Utility request

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the only relevant request. Control R42 has bounded assignment authority, while Utility `assignment/current.md` remains `IDLE`; this pointer divergence must be reconciled. Preserve existing bytes only. No duplicate request, rerun, reconstruction, regeneration, retune or rescore is justified.

## Prospective recommendations

- Keep candidate #34 response-bearing execution stopped until a fresh Evidence Analyst re-fetches exact R2 head `43d0f255...` and the preserved non-result contract and makes a prospective READY decision.
- Treat the current opportunity-aware R2 as a legitimate explicit OPEN_DEVELOPMENT science-affecting version, not as a science-invariant pointer repair and not as evidence.
- Do not change the now-closed R2 comparator/metric/threshold/tolerance/intervention/claim/falsifier merely because future interpretation or literature suggests an improvement. If another pre-response defect is found, record a new explicit prospective development revision; after meaningful result exposure, follow the stricter version/fresh-successor rule.
- Reconcile Control's PF-R1 assignment authority with Utility's current pointer, then preserve only the still-available original bytes. Fail closed if exact originals cannot be retrieved or matched.
- Even after PF-R1 preservation, keep H7 stopped until a later fresh Analyst exact-head review explicitly authorizes any one-way step.
- Preserve all existing raw-before-score, preserve-before-read, concealed-evaluation, exact-binding and no-historical-rewrite guards.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: FORMAL non-consumption `HIGH`; candidate #34 canonical R92 binding and exact-head non-result closure `HIGH`; classification of the R2 opportunity-aware changes as science-affecting but prospectively authorized OPEN development `HIGH`; candidate #34 response non-exposure `HIGH`; PF-R1 original artifact availability `HIGH`; Control↔Utility pointer divergence `HIGH`; PF-R1 preservation completion `NOT_OBSERVED`; fresh consumed-FORMAL end-to-end `UNOBSERVED`; fresh specifically SYSTEM→MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will the fresh Analyst review treat the exact closed R2 as a candidate for READY based on informativeness, without requiring prior scientific success and without treating green non-result checks as evidence?
- Will any further science-affecting change to candidate #34 be recorded as a new explicit prospective development revision rather than silently rewriting the closed R2 contract?
- Will Utility reconcile its `assignment/current` pointer to the existing PF-R1 Control authority and preserve only the original bytes without rerun/reconstruction/rescore?
- After PF-R1 preservation, will H7 remain stopped until a later fresh Analyst exact-head review?
- When repeated result-bearing PRE_FORMAL observations eventually occur, will they remain one correlated development sequence rather than independent confirmation?

## Authoritative refs used

- prior Methodology: `METHCAL-20260923T121735+0900-R80-9C4F7A12@269fdfc699053318f8babbea09c007cbe9932cae`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-20260923T125800+0900-R42-7C9E41B2@7035ace9b0ef980602dcb124e8974be5640d7377`
- Evidence Analyst: `EVA-20260923T105725+0900-R92-6B8E31D4@a05ab3f655a23eabd84c910ba337d64a948c168a`
- Independent Audit used by R92: `R8@6755579f5f21b19ca90788c948d8126529b648c6`
- Utility: `ops/utility-orchestrator-requests@15c5b130c868f7a37ab03582ca0225f001c651f7`
- MAIN operational overlay: `ops/orchestrator-run-report@8f446170ba98142c13025067192fe0ebd4bc7172`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- H7 R5: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- candidate #34 R2: `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`
- candidate #34 R2 contract run/artifact: `35814951495 / 10730964708 / sha256:4df7bac547df7db49c0c68108d8a0d2e40e129f4b0f7ce46ea45cf51c3a08c94`
- PF-R1 original run/artifact: `35695286240 / 10680620448 / sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`
- evidence tags: 5; formal/sealed/freeze tags: none
