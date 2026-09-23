# SparkBrain Methodology Calibration Audit — R78

- schema_version: `2`
- generation_id: `METHCAL-20260923T101704+0900-R78-2B6F91C4`
- produced_at: `2026-09-23T10:17:04+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T092236+0900-R77-A7C43E19`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

A material calibration update is present and the hard integrity floor remains unchanged.

Fresh Evidence Analyst R91 canonicalizes candidate #34 Architecture R2 as prospectively frozen and exact-head green at `research/main-cand34-assembly-route-architecture-r90-cycle2@a6455a3929b86ad25fd106ea93a03604192fc3be`, CI `35802555790`. Independent repository re-fetch confirms that exact branch/head and successful CI. Direct commit inspection confirms that R2 freezes the checkpoint/prototype policy, edge/control family, fixed `+1ms` delay arm, `64ms` measurement window, response fields, reduction panel, fixed execution ordering, `256ms` no-extension quiescence cap, bounded resource/fail-closed semantics and interventional-equivalence policy. The frozen contract itself keeps `response_bearing_execution_allowed=false`, `preformal_execution_allowed=false`, and `formal_action_allowed=false`; no response-bearing candidate result is present in the R2 commit.

R91 then performs the required cycle-3 reassessment and moves candidate #34 to `MECHANISM / PRE_FORMAL / OPEN_DEVELOPMENT / preformal_eligible=true / READY`, queued for a fresh PRE_FORMAL R1 wrapper that must bind the unchanged R2 head plus one prospectively selected development evaluation surface/checkpoint. This is a strong positive calibration case: cycle 3 is being used as a reassessment point rather than a hard terminal cap, and READY is being granted because the next development test is now well-defined and informative, not because the candidate already won its comparator/reduction/falsifier.

The layer-authority split is also calibrated. R2 remains a frozen non-executable scientific contract, while a later PRE_FORMAL wrapper may authorize exactly one development-only response-bearing execution without editing R2 in place. Any resulting observation remains nonconfirmatory development evidence. Once meaningful output is exposed, science-affecting changes must use an explicit development revision or fresh successor and must preserve the prior result unchanged.

One clarification is needed prospectively: the programme must not generalize the current R91 instruction about future continuous-time/multi-resolution/synfire/FSM robustness into a rule that *every* pre-result OPEN_DEVELOPMENT scientific refinement requires a fresh candidate ID. Before the first meaningful result, OPEN_DEVELOPMENT may still use a prospectively versioned same-candidate development revision with durable provenance when the scientific question is genuinely the same. A fresh successor is appropriate when the question/claim is distinct, or when post-result changes would otherwise rescue the exposed object. This is a throughput/calibration clarification, not authority to alter candidate #34's already-frozen R2 in place.

Candidate #35 Discovery R1 is also prospectively closed without response exposure. R91 moves it to `SYSTEM / ARCHITECTURE_STUDY / OPEN_DEVELOPMENT / preformal_eligible=false`, queued for deterministic implementation and synthetic non-result validation only. Direct branch re-fetch finds no `research/main-cand35*` research branch yet, which is consistent with no response-bearing architecture execution having occurred. The SYSTEM ceiling remains calibrated while local membrane-potential/adaptation/threshold/decay reductions dominate.

H7 remains unchanged at exact R5 head `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`, PREIDENTITY COMPLETE but NON_EVIDENTIARY and held at `FORMAL_HOLD_PROVENANCE_GATE`. The PF-R1 artifact still exists and is unexpired at workflow `35695286240`, artifact `10680620448`, digest `sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`; however Utility still has no matching schema-v2 assignment/decision, so exact-byte preservation remains unexecuted. Utility default-deny is correct; rerun/reconstruction/regeneration/rescore remains prohibited.

Independent repository re-fetch confirms stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, authoritative annotated `evidence/*` remains exactly five tag objects, tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty, and no H7 control/freeze/preserve ref exists. No fresh FORMAL identity consumption is observed.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| OPEN development bounded instrumentation/synthetic reachability | `KEEP` |
| non-result tooling success does not imply RESULT_EXPOSED | `KEEP` |
| candidate #34 Architecture R2 prospective scientific contract freeze before outcomes | `KEEP` |
| frozen R2 contract separated from later layer execution authority | `KEEP` |
| candidate #34 cycle-3 reassessment to PRE_FORMAL READY without prior victory | `KEEP` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 as mandatory information-gain reassessment | `KEEP` |
| PRE_FORMAL one prospectively bound development surface/checkpoint | `KEEP` |
| PRE_FORMAL result remains nonconfirmatory development observation | `KEEP` |
| repeated result-bearing PRE_FORMAL observations counted as independent confirmation | `TIGHTEN` |
| repeated result-bearing PRE_FORMAL live stress case | `INSUFFICIENT_EVIDENCE` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| pre-result OPEN science-affecting refinement must always use a fresh candidate ID | `CLARIFY` |
| distinct robustness/claim extension after result exposure uses revision/fresh successor, not rescue | `KEEP` |
| candidate #35 Discovery→Architecture progression without response exposure | `KEEP` |
| candidate #35 SYSTEM ceiling under ordinary-reduction dominance | `KEEP` |
| candidate #35 same-object future SYSTEM→MECHANISM uplift | `TIGHTEN` |
| terminal current-object scope permits fresh successor topics | `KEEP` |
| fresh SYSTEM→MECHANISM successor specifically | `INSUFFICIENT_EVIDENCE` |
| H7 R5 PREIDENTITY COMPLETE distinct from FORMAL authority/evidence | `KEEP` |
| no extra H7 development merely to maintain activity | `KEEP` |
| PF-R1 exact-byte preservation requirement | `KEEP` |
| PF-R1 preservation execution state | `TIGHTEN` |
| Utility default-deny without schema-v2 machine authority | `KEEP` |
| duplicate request/rerun to bypass PF-R1 authority gap | `TIGHTEN` |
| final exact source/runner/scorer/preserver/runtime/input binding | `TIGHTEN` |
| hosted-runner/kernel/provisioning dimensions | `SPLIT_BY_CLAIM_TYPE` |
| claim-capable native/runtime dimensions | `TIGHTEN` |
| resolver/package/runner-image shopping | `TIGHTEN` |
| raw-before-score as file ordering only | `CLARIFY` |
| literal target-blind prediction raw | `TIGHTEN` |
| immutable preserve before target-side scoring | `TIGHTEN` |
| post-preserve scorer recomputation | `TIGHTEN` |
| target-sidecar independence | `TIGHTEN` |
| fresh concealed evaluation surface | `TIGHTEN` |
| PRE_FORMAL as genuine development | `KEEP` |
| preformal_eligible distinct from READY | `KEEP` |
| READY = informative next test, not prior success | `KEEP` |
| HIDDEN_SECOND_FORMAL_GATE | `KEEP` — false |
| current-object claim ceiling | `KEEP` |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` |
| fresh successor distinctness/non-rescue | `KEEP` |
| classification completeness | `KEEP` |
| MAIN MECHANISM priority | `KEEP` |
| SYSTEM work parallel to a nondisplaced MECHANISM lane | `KEEP` |
| prospective SYSTEM-priority exception rule | `KEEP` |
| genuine SYSTEM-over-comparable-MECHANISM MAIN exception | `INSUFFICIENT_EVIDENCE` |
| theory-backward quality floor | `KEEP` |
| NO_COHERENT_MECHANISM_TARGET liveness semantics | `KEEP` |
| protected/adaptive-evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** Consistent through the current development/preidentity surfaces. Candidate #34 now provides a stronger positive case: R1/R2 non-result development stayed `OPEN_DEVELOPMENT`, then cycle-3 reassessment moved the object to PRE_FORMAL READY without manufacturing a scientific result. A fresh post-HUMAN-005 `CONSUMED_ONE_WAY` completion is still unobserved.
2. **Is cycle 3 being mistaken for a hard terminal cap?** No. R91 explicitly performs cycle-3 reassessment and continues #34 to PRE_FORMAL because distinct prospective information gain remains. This is calibrated.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Yes in observed live cases. R2 was frozen before outcomes; a later execution-authority wrapper may bind it without changing scientific semantics. After meaningful PRE_FORMAL exposure, metric/intervention/comparator/input/resource/falsifier/success changes must be versioned or moved to a fresh successor. Clarification: before first meaningful exposure, same-question OPEN development may still use a prospectively versioned same-candidate revision rather than being forced into a new candidate ID.
4. **Are development rerun/retune/tolerance revisions logged without being laundered into independent evidence?** No laundering is currently observed. R91 explicitly requires PRE_FORMAL output to remain development-only and nonconfirmatory. The programme still lacks a live repeated result-bearing PRE_FORMAL series that stress-tests non-independence accounting.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Yes for the H7 R4→R5 lineage. Programme-wide exact-byte durability remains incomplete because PF-R1 existing bytes are not yet durably preserved under valid machine authority.
6. **Is FORMAL one-way integrity unchanged?** Yes. Main/evidence refs are unchanged, H7 has no fresh control/freeze/preserve identity, and no new formal/sealed/freeze tags exist.
7. **Are legitimate fresh SYSTEM→MECHANISM successors being suppressed or manufactured?** No manufacture is observed. #34 is a legitimate fresh MECHANISM question and #35 remains SYSTEM-scoped. A specifically fresh MECHANISM successor arising from a terminal SYSTEM object remains unobserved.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes. #34 becomes READY immediately after prospective R2 contract closure, without any requirement to have already won comparator/reduction/falsifier. Its future PRE_FORMAL output is explicitly nonconfirmatory.
9. **Are terminal semantics and candidate-supply controls calibrated?** Improved. Current-object closure continues to permit new questions without reopening history or inflating every successor to MECHANISM. #34 is now the queued PRE_FORMAL MECHANISM lane while #35 is a queued SYSTEM Architecture lane and H7 remains held.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes for H7: `REALISTIC_NEAR_TERM_CONDITIONAL`. Candidate #34 is now development-test reachable at PRE_FORMAL, not yet confirmatory/PASS-reachable. No evidence standard needs weakening.

## Risk calibration

False-positive risk remains `MODERATE_WATCH`: the main new risk is treating #34 PRE_FORMAL output as confirmatory evidence or accumulating repeated PRE_FORMAL runs as independent replication. R5 PREIDENTITY COMPLETE must also remain distinct from FORMAL authority, and claim-capable runtime/input/evaluator bindings remain mandatory.

False-negative/opportunity-cost risk remains `LOW_TO_MODERATE_WATCH_IMPROVING`: #34 has reached READY without a hidden second FORMAL gate, #35 continues as a lower-ceiling SYSTEM lane, and topic continuation is not being suppressed. A remaining throughput risk is over-fragmentation if every pre-result OPEN scientific refinement is forced into a fresh candidate rather than allowing a prospectively versioned same-question development revision.

Moving-goalpost/rescue risk is `LOW_WATCH_IMPROVING`: #34 froze its Architecture R2 contract before any response-bearing output, requires one prospectively bound PRE_FORMAL surface, accepts negative/equivalence outcomes, and forbids stronger post-outcome arms to obtain a preferred result.

Over-terminalization risk is `LOW_WATCH_IMPROVING`: #34/#35 continue to demonstrate that terminal current-object semantics do not imply topic death.

## Development-iteration calibration

Candidate #34 is now the clearest cycle-policy positive case. OPEN development supported substantial instrumentation and prospective scientific contract design; cycle 3 then reassessed information value rather than terminalizing by count. The object moves to PRE_FORMAL READY because the next test is now defined, not because development results already favor the hypothesis.

The correct next boundary is: bind exact R2 head plus one development surface/checkpoint in a fresh PRE_FORMAL authority wrapper, execute development-only, preserve the resulting observation as nonconfirmatory, and then switch to `RESULT_EXPOSED_DEVELOPMENT` semantics for any further science-affecting change. Same-object lint/path/serialization/hash-plumbing may remain invariant repair; outcome-responsive scientific rescue may not.

The R91 literature guardrail should remain interpretive, not silently alter R2. If a *distinct* continuous-time/multi-resolution/synfire/FSM question is later pursued, a fresh successor is appropriate. If a methodological defect in the same scientific question is discovered before any meaningful PRE_FORMAL result, OPEN development may instead create a clearly versioned same-candidate revision while preserving R2 history. This distinction protects both throughput and provenance.

## Funnel observability / mechanism supply

Fresh R91 canonical population remains `35 = 14 MECHANISM / 21 SYSTEM`. Lifecycle is `ACTIVE 0 / QUEUED 2 / NONTERMINAL_HOLD 1 / TERMINAL_FOR_CURRENT_OBJECT 32`. Development phases remain `OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`. PRE_FORMAL eligible/READY becomes `2/2`: H7 is READY but FORMAL-held, and #34 is READY for development PRE_FORMAL. Fresh FORMAL authority is `0`, historical official consumed identities remain `7`, and classification completeness is `35/35`.

Mechanism-supply health is `CAND34_READY_PREFORMAL_PLUS_H7_FORMAL_HOLD_WITH_CAND35_ARCHITECTURE_QUEUED_QUALITY_FLOOR_INTACT`. There is one executable development MECHANISM lane (#34), a second held MECHANISM lineage (H7), and a separate SYSTEM Architecture lane (#35) without claim inflation.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. #34 is now the strongest live example: it becomes READY without prior scientific victory, and its next result is explicitly development-only.

PRE_FORMAL may genuinely iterate, but repeated observations must remain a correlated development sequence rather than confirmatory replications. Once a meaningful result is exposed, science-affecting changes require an explicit development revision/fresh successor and prior results must remain durable and unchanged.

PF-R1 remains one nonconfirmatory development observation with confirmatory count zero. Its artifact is still recoverable, so durability should be closed from existing bytes without rerun/reconstruction/rescore.

H7 PASS reachability remains `REALISTIC_NEAR_TERM_CONDITIONAL`: establish valid schema-v2 Utility authority for the existing preservation request, preserve existing PF-R1 bytes/hashes, require a later fresh Analyst re-fetch of unchanged exact R5, and retain prediction-only raw → immutable preserve → target-side scoring, concealed evaluation, collision/no-clobber, and exact binding gates.

## Utility request

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the only request. Utility remains fail-closed without matching schema-v2 machine authority. Do not duplicate the request or rerun/reconstruct/regenerate/rescore PF-R1.

## Prospective recommendations

- Execute #34 PRE_FORMAL only through a fresh layer-authority wrapper that binds exact R2 `a6455a3929b86ad25fd106ea93a03604192fc3be` plus one prospectively selected development surface/checkpoint; do not edit R2's execution flags in place.
- Preserve the first meaningful #34 PRE_FORMAL output as a nonconfirmatory development result. Any later science-affecting change must be an explicit revision/fresh successor; repeated PRE_FORMAL runs must not accumulate independent-confirmation credit.
- Clarify programme-wide that OPEN_DEVELOPMENT before result exposure may use a prospectively versioned same-question revision; fresh candidate IDs are required for distinct successor questions or to prevent post-result rescue laundering, not for every pre-result scientific refinement.
- Keep #35 SYSTEM-scoped through Architecture while ordinary local reductions dominate and response-bearing execution remains unauthorized.
- Resolve PF-R1 machine authority on the existing request only; preserve existing bytes, then require fresh Analyst one-way review of unchanged R5.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: FORMAL non-consumption `HIGH`; #34 R2 exact-head prospective contract closure `HIGH`; successful CI at exact R2 head `HIGH`; #34 cycle-3 PRE_FORMAL READY semantics `HIGH`; #35 no-response Architecture transition `HIGH` from canonical history plus absence of a current research branch; PF-R1 artifact recoverability and authority blocker `HIGH`; fresh consumed-FORMAL end-to-end `UNOBSERVED`; repeated result-bearing PRE_FORMAL non-independence live stress case `UNOBSERVED`; fresh specifically SYSTEM→MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will #34 PRE_FORMAL R1 bind the exact unchanged R2 head and exactly one prospectively selected development surface/checkpoint before any response-bearing execution?
- Will the first meaningful PRE_FORMAL output be durably preserved as nonconfirmatory development evidence, with subsequent science-affecting changes versioned rather than repaired in place?
- Will Control/Analyst explicitly preserve the distinction that pre-result OPEN same-question refinements may use a versioned development revision, while fresh candidate IDs are reserved for genuinely distinct successor questions or post-result rescue prevention?
- Will #35 remain SYSTEM-scoped during Architecture unless a fresh independently motivated MECHANISM residual later justifies a new candidate ID?
- Can the existing PF-R1 preservation request receive matching schema-v2 machine authority without duplicate request or artifact rerun/reconstruction?

## Authoritative refs used

- prior Methodology: `METHCAL-20260923T092236+0900-R77-A7C43E19@bfcdff499b9dd9f28113a674b899a6bf7838db3e`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-20260923T085000+0900-R40-5E1C7A94@f25d48598584bffc5ca736c6ac52c50a94688d89`
- Evidence Analyst: `EVA-20260923T101328+0900-R91-C199605F@2840c4171fec8d09ad13e182c5221c2c35647328`
- Utility: `ops/utility-orchestrator-requests@b18a1d76c05efbbfacb9618ac1ca1e9941b17555`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative evidence tags: 5 unchanged
- tag-form `formal/*`: empty
- tag-form `sealed/*`: empty
- tag-form `freeze/*`: empty
- H7 R5 exact head: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- candidate #34 Architecture R2 exact head: `research/main-cand34-assembly-route-architecture-r90-cycle2@a6455a3929b86ad25fd106ea93a03604192fc3be`
- candidate #34 exact-head CI: `35802555790` success
- PF-R1 existing artifact: workflow `35695286240`, artifact `10680620448`, digest `sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`, unexpired
