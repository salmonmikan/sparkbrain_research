# SparkBrain Methodology Calibration Audit — R85

- schema_version: `2`
- generation_id: `METHCAL-20260923T161855+0900-R85-C41E72A9`
- produced_at: `2026-09-23T16:18:55+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T152244+0900-R84-5D4A8C21`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The hard scientific integrity floor remains unchanged. Since R84, candidate #34 crossed the first live HUMAN-20260922-005 development-result boundary. Evidence Analyst R94 had prospectively authorized exactly one bounded PRE_FORMAL R2 response on the unchanged closed R2 contract and exact repaired executor. A single response workflow run (`35826846989`) completed successfully. The workflow checked out exact executor `8ce961dc88fb52afa6399093fce1e3de7e982f2b`, executed D34-Q002 once, uploaded raw without interpretation, and a fresh preserve ref `preserve/cand34-d34-q002-r94-raw-20260923@4d45f1135bcb607f1e663648cd8335333eb98de4` now contains the development raw.

The preserved raw itself declares `PREFORMAL_DEVELOPMENT_RESULT_EXPOSED`, `PREFORMAL_DEVELOPMENT_ONLY_ZERO_CONFIRMATORY_CREDIT`, independent confirmatory credit 0, no official scoring, no FORMAL action, and no repeat permission. This is a strong positive calibration result: one bounded OPEN_DEVELOPMENT observation was obtained, raw was preserved, execution stopped, and the observation was not laundered into confirmatory evidence.

A material provenance defect is also present. The raw record's `execution_source_head` is `5e0cb8882a6f7afc684b11b97dddf30b573e7a43`, the ops dispatch/workflow commit, while the workflow definition independently proves that the scientific executor actually checked out and ran `8ce961dc88fb52afa6399093fce1e3de7e982f2b`. The raw also records R93 in generic `analyst_authority`/`analyst_commit` fields even though R94 separately authorized the repaired exact executor. This is not grounds to rerun, rewrite, or discard the preserved development result. The correct prospective repair is append-only provenance clarification: distinguish scientific-contract authority from execution authorization and record the actual checked-out executor from `git rev-parse HEAD` or an equivalent dedicated immutable field.

The newest designated Evidence Analyst snapshot remains R94 and therefore predates the actual response exposure. Methodologically, candidate #34 has crossed into `RESULT_EXPOSED_DEVELOPMENT`; fresh Analyst canonicalization is pending. Control R43 correctly stops all repeat/retune/rescore/science-affecting work and routes the preserved raw for fresh Analyst review. Any mailbox field still saying OPEN is stale process state, not authority to repeat.

H7 remains FORMAL-held. Control R43 has now published a machine-resolvable one-attempt PF-R1 preservation decision/assignment for existing original bytes only, but the Utility mailbox head still shows its prior state and has not yet reflected/completed the assignment. No PF-R1 rerun/reconstruction/regeneration/retune/rescore is justified. No new methodology Utility request is created.

Independent repository/evidence re-fetch confirms stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` remains exactly five annotated tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. No fresh FORMAL identity/result consumption or historical evidence rewrite is observed.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| live first OPEN→RESULT_EXPOSED boundary | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| exactly one bounded PRE_FORMAL response under R94 | `KEEP` |
| preserve raw before interpretation / STOP after first exposure | `KEEP` |
| development result confirmatory credit remains zero | `KEEP` |
| repeat result-bearing execution under exhausted R94 authority | `TIGHTEN` |
| immediate post-exposure phase canonicalization | `TIGHTEN` |
| raw execution-source provenance correctness | `TIGHTEN` |
| scientific-contract authority vs execution-authorization provenance fields | `CLARIFY` |
| append-only provenance sidecar for already-preserved raw | `KEEP` |
| rerun/rewrite raw to repair metadata | `TIGHTEN` |
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
| Control R43 machine-resolvable PF-R1 preservation assignment | `KEEP` |
| Utility execution/completion of PF-R1 preservation | `TIGHTEN` |
| Utility default-deny until assignment is observed exactly | `KEEP` |
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

1. **Are development-phase semantics implemented consistently end-to-end?** The first live OPEN→RESULT_EXPOSED boundary is now positively observed: exactly one bounded result, immediate preservation, zero confirmatory credit and STOP. Fresh post-result Analyst canonicalization and fresh CONSUMED_ONE_WAY completion remain unobserved. The stale OPEN mailbox field should be corrected by fresh Analyst before further work.
2. **Is cycle 3 a hard terminal cap?** No. #34 legitimately continued beyond cycle 3 for distinct prospective information gain, then stopped after the single authorized result rather than continuing for activity.
3. **Are repair classes distinguished correctly?** Yes in the observed execution sequence. The pre-result unused-import repair was science-invariant. No post-result science-affecting repair has occurred. Any future metric/intervention/comparator/threshold/resource/hypothesis/falsifier/success-criterion change now requires explicit versioning/fresh successor.
4. **Are development rerun/retune/tolerance revisions logged without laundering into independent evidence?** One result-bearing run is observed and explicitly carries zero confirmatory credit. No repeat or retune is observed. A repeated result-bearing sequence remains insufficiently tested, so correlated development observations must continue to count as zero independent confirmation.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** #34's first raw result is now durably preserved before interpretation, which is positive. H7 R4→R5 remains a positive versioning case. PF-R1 durable exact-byte preservation is still pending completion.
6. **Is FORMAL one-way integrity unchanged?** Yes. Stable main/evidence refs are unchanged; formal/sealed/freeze tags remain empty; no fresh FORMAL consumption is observed.
7. **Are legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured?** No manufacture is observed. A specifically fresh MECHANISM successor from a terminal SYSTEM object remains unobserved.
8. **Is PRE_FORMAL development rather than hidden FORMAL?** Yes. #34 obtained one development-only result with zero confirmatory credit. READY was based on informativeness, not prior success, and the result does not upgrade evidence status.
9. **Are terminal semantics and candidate supply calibrated?** Yes/improving. #34 remains a viable MECHANISM line now awaiting post-result review; H7 is held rather than killed; #35 remains SYSTEM without claim inflation. No new authoritative post-result funnel population snapshot exists yet.
10. **Is PASS reachable without weakening standards?** Yes. H7 remains `REALISTIC_NEAR_TERM_CONDITIONAL`: execute the existing PF-R1 preservation assignment on original bytes, then obtain fresh unchanged-R5 Analyst review; no evidence standard needs relaxation.

## Development-iteration calibration

Candidate #34 is now a live positive test of the HUMAN-20260922-005 boundary. The program allowed legitimate OPEN development and science-invariant repair, prospectively rebound the exact executor, permitted exactly one informative result, preserved the raw, assigned zero confirmatory credit, and stopped. Iteration was not treated as a defect, and result exposure did terminate the old one-shot authority.

The next rule is stricter because the result exists. #34 is methodologically RESULT_EXPOSED for this revision. Same-object SCIENCE_INVARIANT repair may remain permissible, but any science-affecting modification requires explicit versioned development revision or a fresh successor preserving this result. A second D34-Q002 run under R94 would be over-permissive rescue tuning.

The raw provenance defect must be fixed prospectively without touching the raw. `execution_source_head` currently names the dispatch commit even though the workflow checked out another exact executor. Future result records should record both dispatch/workflow provenance and actual checked-out scientific source separately, and should split scientific-contract authority from execution authorization.

## Risk calibration

False-positive risk: `MODERATE_WATCH`. The largest new risk is provenance misbinding: downstream tooling could trust the raw's ambiguous source/authority fields and attribute the observation to the wrong commit/authorization. This is mitigated because the exact executor is independently reconstructible from the workflow and the raw is development-only with zero confirmatory credit.

False-negative/opportunity-cost risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. The correct response to the metadata defect is not to invalidate, discard or rerun the development observation; append-only provenance clarification is sufficient. H7 still has non-scientific preservation latency.

Moving-goalpost/rescue risk: `LOW_WATCH_IMPROVING`. Exactly one result was obtained and the queue is now stopped pending fresh review.

Over-terminalization risk: `LOW_WATCH_IMPROVING`. #34 was allowed to reach an informative result beyond cycle 3 without topic death; #35 remains a separate SYSTEM line and H7 remains viable on hold.

## Funnel observability / mechanism supply

Evidence Analyst R94 remains the newest canonical population snapshot and predates the response: `35 = 14 MECHANISM / 21 SYSTEM`; lifecycle `ACTIVE 0 / QUEUED 2 / HOLD 1 / TERMINAL_FOR_CURRENT_OBJECT 32`; development `OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`; PRE_FORMAL eligible/READY `2/2`; fresh FORMAL authority `0`; historical official consumed identities `7`; classification `35/35`.

The preserved raw independently proves that #34 has now crossed the development-result boundary. Methodology therefore treats its current phase as RESULT_EXPOSED pending fresh Analyst canonicalization, without silently rewriting R94's historical snapshot. The stale mailbox/open count must not be used to authorize repetition.

Mechanism-supply health: `TWO_MECHANISM_LINEAGES_CAND34_RESULT_EXPOSED_PENDING_FRESH_ANALYST_PLUS_H7_FORMAL_HOLD_WITH_SYSTEM_DISCOVERY_BACKUP_QUALITY_FLOOR_INTACT`.

## Claim-type findings

#34 remains MECHANISM ceiling. The development observation is limited to the frozen local route-influence surface and has zero confirmatory credit. This audit does not interpret its numerical sign/strength and does not treat it as new scientific evidence.

H7 remains MECHANISM and FORMAL-held without new evidence. #35 remains SYSTEM / OPEN_DEVELOPMENT. No same-object SYSTEM→MECHANISM uplift is observed.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. The one #34 observation is a development result, not a confirmation. Any later PRE_FORMAL observation, if separately authorized after fresh review, remains part of a correlated development sequence rather than an independent replication.

H7 pass reachability remains `REALISTIC_NEAR_TERM_CONDITIONAL`. Control has published the missing bounded PF-R1 preservation assignment, but Utility has not yet reflected/completed it. Original bytes must be preserved as-is; rerun/reconstruction/regeneration/retune/rescore remain forbidden.

## Utility request

No new methodology Utility request. Existing request `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` now has Control R43 machine-resolvable decision/assignment. Await Utility exact uptake/completion; do not duplicate the request and do not rerun PF-R1.

## Prospective recommendations

- Do not rerun D34-Q002 to repair metadata. Keep the preserved raw immutable.
- Add append-only provenance clarification for #34 binding scientific contract R2, R93 scientific/READY authority, R94 exact-executor execution authorization, actual checked-out executor `8ce961dc...`, dispatch workflow/run identity, preserve ref and distinct digests.
- Future result emitters should record actual checked-out source from `git rev-parse HEAD` or a dedicated non-overridable source field; do not rely on GitHub's `GITHUB_SHA` to identify a separately checked-out ref.
- Split `scientific_contract_authority` and `execution_authority` explicitly in future result schemas.
- Fresh Evidence Analyst should first canonicalize #34 as RESULT_EXPOSED with confirmatory credit zero and exhausted R94 one-shot authority before any further result-bearing work.
- Any post-exposure science-affecting redesign must be an explicit versioned development revision or fresh successor preserving the current raw; same-object repairs must remain strictly science-invariant.
- Utility should execute the already-published PF-R1 one-attempt exact-byte preservation assignment and report completion/failure without inference or rerun.
- Preserve all FORMAL hard-floor guards unchanged.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: FORMAL non-consumption `HIGH`; #34 exactly-one result workflow `HIGH`; exact executor checkout `HIGH`; raw preservation and zero confirmatory credit `HIGH`; observed result-boundary crossing `HIGH`; raw source/authority provenance defect `HIGH`; post-result Analyst canonicalization `PENDING`; repeated result-bearing PRE_FORMAL behavior `UNOBSERVED`; PF-R1 Control assignment publication `HIGH`; PF-R1 Utility completion `NOT_OBSERVED`; fresh consumed-FORMAL end-to-end `UNOBSERVED`; fresh specifically SYSTEM→MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will fresh Analyst canonicalize #34 as RESULT_EXPOSED before any other #34 result-bearing action?
- Will the preserved raw remain byte-for-byte unchanged, with provenance correction only via append-only sidecar/record?
- Will future provenance distinguish actual checked-out executor source from workflow dispatch commit and distinguish scientific-contract authority from execution authorization?
- Will any second #34 response or science-affecting redesign require fresh post-exposure authorization/versioning?
- Will Utility take the existing PF-R1 assignment exactly once and preserve only original bytes without rerun/reconstruction/rescore?

## Input generations / authoritative refs used

- previous Methodology: `METHCAL-20260923T152244+0900-R84-5D4A8C21@f0d6b97c76878aada97794745c4b51f46bea18b0`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-20260923T155900+0900-R43-A91C4E6B@1592c3b52a8a545aa2503fd4618c0a761921ef1e`
- Evidence Analyst: `EVA-20260923T150251+0900-R94-8E6A31C4@5cee6ef496eb9465550fb9c0be5295e587027dfb`
- Utility mailbox: `ops/utility-orchestrator-requests@b2f1462aeb95707747f8b273c1b9a6ec678996bd`
- MAIN/orchestrator mailbox: `ops/orchestrator-run-report@692557e1e5d5deeb7d156db274ea2e71d323b1db`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative evidence tags: exactly 5; `formal/*=[]`; `sealed/*=[]`; `freeze/*=[]`
- #34 closed R2: `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`
- #34 exact repaired executor: `research/main-cand34-assembly-route-preformal-r93-response@8ce961dc88fb52afa6399093fce1e3de7e982f2b`
- #34 dispatch workflow commit: `5e0cb8882a6f7afc684b11b97dddf30b573e7a43`
- #34 response workflow run: `35826846989=success`
- #34 preserved raw ref: `preserve/cand34-d34-q002-r94-raw-20260923@4d45f1135bcb607f1e663648cd8335333eb98de4`
- #34 raw self-declared payload SHA-256: `9575791aa2286e5f3e20357696b9ddcb45ee8fd25c7f5ec6b0d5f6cdb5b4942a`
- #34 Actions artifact archive digest: `sha256:38a50cf3d63be3355d3d95387d155a6f0e550d998026ccdd38743a07520171f4`
- #34 Control-computed downloaded raw-file SHA-256: `f34e0e4a40228b5eb299b0c24cec0a6bc97bb37dd1fa5d0f63cf933027843846`
- H7 R5: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
