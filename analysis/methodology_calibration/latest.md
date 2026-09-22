# SparkBrain Methodology Calibration Audit — R71

- schema_version: `2`
- generation_id: `METHCAL-20260923T031749+0900-R71-B73D5A2C`
- produced_at: `2026-09-23T03:17:49+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `true`
- supersedes: `METHCAL-20260923T012000+0900-R70-4C8A1E73`

## Material change

The new material finding is a request-level authorization split between Control/Analyst prose and the Utility machine authority used to execute bounded PF-R1 provenance preservation.

Control R37 says `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` is Control-approved/open, and Evidence Analyst R83 treats the same existing request as outstanding/GO. The Utility orchestrator independently reconciled its own authoritative request/assignment/decision records and found no matching Control-owned decision or schema-v2 assignment: the request file remains `PROPOSED_NOT_APPROVED`, `assignment_id=null`, `assignment_generation_id=null`, and no matching Utility decision/assignment exists. Utility therefore correctly did not retrieve or archive PF-R1 bytes and did not infer execution authority from prose.

This is not a scientific-integrity breach. It is a control-plane authorization-observability defect that is now blocking an integrity-preserving hard gate. The PF-R1 Actions artifact remains live and unexpired at workflow `35695286240`, head `8681dcbbe2fff986c28a79057f557b35f3f0f752`, artifact `10680620448`, archive digest `sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`. The calibrated response is not to weaken Utility default-deny and not to duplicate the request; Control should materialize request-scoped machine-readable authority if it still intends the bounded NON_EVIDENTIARY preservation.

R70's separate R4 artifact-observability problem has improved: R83 now reconciles the authoritative R4 run-scoped artifact correctly as workflow `35748064227` / head `647253f4c0128ff09d47fdfce80dabf006863af1` / artifact `10703822275` / digest `sha256:54334fcb7ceb962e46f82712a36722a4a687d87e7d83dc32d86c61564e58e9d1`. The artifact remains live, but exact lock/manifest bytes are still not durably committed to the R4 branch, so one-way FORMAL authority remains zero.

## Input generations / authoritative refs

- prior methodology: `METHCAL-20260923T012000+0900-R70-4C8A1E73` @ `ops/methodology-calibration-audit@2663fca3580ae2f4524ebddc6cb7a9dd5ec3a75d`
- human directive: `HUMAN-20260922-005` — process directive only, not scientific evidence
- Control: `CTRL-20260922T235000+0900-R37-7A3E9C51` @ `ops/control-brain-handoff@23676a55c9473d1cfd22d982ffffd5d2ba18b557`
- Evidence Analyst: `EVA-20260923T020919+0900-R83-A6D4E219` @ `ops/evidence-analyst-handoff@ba109150205db0a30ce1c294ab8133fa6caa51b4`
- Utility reconciliation: `UTILITY-20260923T023100+0900-AUTO-PFR1-AUTH-CONSISTENCY-COMPLETED-4E7A2C91` @ `ops/utility-orchestrator-requests@b18a1d76c05efbbfacb9618ac1ca1e9941b17555`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- H7 R4: `research/main-h7-formal-r4-runtime-lock-r81-cycle10@647253f4c0128ff09d47fdfce80dabf006863af1`
- R4 materialization: workflow `35748064227`, artifact `10703822275`, digest `sha256:54334fcb7ceb962e46f82712a36722a4a687d87e7d83dc32d86c61564e58e9d1`
- PF-R1 development artifact: workflow `35695286240`, artifact `10680620448`, digest `sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`
- Utility request blob: `d0bcee3fe422925cfc999cf63cc5ba34375eb8b0`; current assignment-pointer blob: `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`
- annotated `evidence/*`: five unchanged refs; tag-form `formal/*`, `sealed/*`, `freeze/*`: empty

## Gate-by-gate classification

| Material gate | Classification | Finding |
|---|---|---|
| hard FORMAL integrity floor | `KEEP` | No fresh H7 identity/result; existing evidence refs unchanged. |
| orthogonal development-phase axis | `KEEP` | H7 remains RESULT_EXPOSED development; Utility reconciliation is non-evidentiary. |
| full OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live path | `INSUFFICIENT_EVIDENCE` | Fresh post-directive consumed FORMAL remains unobserved. |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` | Provenance retrieval/hash plumbing may remain invariant if science contract stays fixed. |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` | R3→R4 remains explicit/prospective. |
| request-scoped Utility execution authority machine-resolvable before work | `TIGHTEN` | Control prose approval has no matching decision/assignment object. |
| Control/Analyst prose as sufficient Utility execution authority | `CLARIFY` | Prose records intent/history; they are not a substitute for request-level execution authority. |
| Utility default-deny without matching decision/assignment | `KEEP` | Utility correctly stopped and did not infer/self-grant authority. |
| Utility self-approval prohibition | `KEEP` | No self-approval or Control-owned decision mutation occurred. |
| duplicate Utility request to bypass blocked authority | `KEEP` | No duplicate was appended; the existing request should be reconciled in place. |
| durable RESULT_EXPOSED development bytes | `TIGHTEN` | PF-R1 bytes remain live but not durably preserved. |
| non-rerun recovery of existing PF-R1 bytes | `KEEP` | Artifact is recoverable; rerun/reconstruction remains forbidden. |
| R4 authoritative run-scoped artifact discovery/binding | `KEEP` | R83 now uses the independently verified run/head/name/digest tuple. |
| copied ops-mailbox artifact pointer as provenance authority | `CLARIFY` | Mailbox pointers remain non-authoritative hints. |
| exact R4 lock/manifest bytes durable capture before identity | `TIGHTEN` | Artifact exists; final bytes are not yet committed/captured into the R4 durable path. |
| resolver/materializer shopping for preferred bytes | `TIGHTEN` | Existing one-shot bytes must be recovered, not regenerated to get a preferred result. |
| protected scientific runtime vs dev tooling separation | `KEEP` | Authoritative R4 contract remains the source of package/resource scope. |
| cycle 3 as automatic terminal cap | `RELAX` | H7 cycle 10 remains justified by prospective integrity information gain. |
| cycle 3 mandatory reassessment | `KEEP` | Continuation remains bounded and prospectively motivated. |
| raw-before-score as file ordering only | `CLARIFY` | Semantic prediction-only raw remains required. |
| literal target-blind prediction raw | `TIGHTEN` | R68 gate remains live. |
| scorer-side recomputation after immutable preserve | `TIGHTEN` | Remains a preidentity requirement. |
| target-sidecar independence | `TIGHTEN` | Remains a preidentity requirement. |
| preserve-before-read / immutable FORMAL evidence path | `TIGHTEN` | Still unproven end-to-end for fresh H7 FORMAL. |
| concealed fresh evaluation surface | `TIGHTEN` | R2 remains quarantined; concealed post-binding evaluation remains required. |
| development reruns ≠ independent evidence | `KEEP` | Tooling/provenance checks carry zero confirmatory credit. |
| repeated result-bearing PRE_FORMAL live stress case | `INSUFFICIENT_EVIDENCE` | Still not adequately observed. |
| PRE_FORMAL as genuine development | `KEEP` | Iteration remains allowed without confirmatory credit. |
| preformal_eligible distinct from READY | `KEEP` | Distinction remains live. |
| READY = informative next test, not prior success | `KEEP` | `HIDDEN_SECOND_FORMAL_GATE=false`. |
| current-object claim ceiling | `KEEP` | Ceiling remains object-specific. |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` | No laundering observed. |
| fresh terminal SYSTEM successor discipline | `KEEP` | Candidate 33 remains SYSTEM-only and terminal for current object. |
| fresh SYSTEM→MECHANISM successor | `INSUFFICIENT_EVIDENCE` | Genuine live case remains absent. |
| TERMINAL_FOR_CURRENT_OBJECT scope | `KEEP` | Topic death is not implied. |
| classification completeness | `KEEP` | R83 retains 33/33 classified. |
| MAIN MECHANISM priority | `KEEP` | H7 remains the viable MECHANISM lane. |
| prospective SYSTEM-priority exception | `KEEP` | No comparable-MECHANISM override observed. |
| genuine SYSTEM-over-MECHANISM exception | `INSUFFICIENT_EVIDENCE` | Still unobserved. |
| theory-backward quality floor / no-target liveness | `KEEP` | No candidate manufacturing to preserve activity. |
| protected/adaptive-evaluation validity | `TIGHTEN` | Concealed-evaluation/raw findings remain unresolved FORMAL gates. |

## Mandatory questions

1. Development-phase semantics remain coherent through R4 preidentity work; a fresh `CONSUMED_ONE_WAY` post-directive case remains unobserved.
2. Cycle 3 is not being used as a hard cap. H7 continues only for explicitly stated integrity/reproducibility information gain.
3. Repair classification remains calibrated. Recovering already-existing bytes, lint/path/hash plumbing and request-authority reconciliation are science-invariant; package/resource/scorer/seed/claim changes still require versioning.
4. Development reruns/retunes are not being laundered into independent evidence. Utility performed no PF-R1 retrieval, rerun, scoring or reinterpretation.
5. RESULT_EXPOSED semantic lineage is preserved, but PF-R1 exact bytes are still not durably preserved because machine execution authority is unresolved.
6. FORMAL one-way integrity is unchanged: stable main/evidence are unchanged and no H7 FORMAL identity/STARTED/protected result exists.
7. Candidate 33 remains a legitimate fresh SYSTEM successor without MECHANISM uplift; a genuine fresh SYSTEM→MECHANISM successor remains unobserved.
8. PRE_FORMAL remains development, not hidden FORMAL; READY remains development readiness.
9. Terminal semantics remain calibrated, but candidate/mechanism supply remains thin and the PF-R1 authority mismatch now adds avoidable throughput friction.
10. PASS remains reachable without weakening evidence standards. The missing action is to make existing preservation authority machine-resolvable, not to waive provenance or one-way gates.

## Risk / development calibration

False-positive risk: `MODERATE_WATCH`. The scientific risks remain concealed evaluation and semantic raw/preserve integrity. Utility's default-deny behavior reduces rather than increases contamination risk.

False-negative/opportunity-cost risk: `MODERATE_WATCH`. Mechanism supply remains one H7 lineage, and an authority-record mismatch now blocks preservation of already-existing development bytes required before FORMAL identity.

Moving-goalpost/rescue risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. R3 is preserved, R4 is explicit/prospective, package set is fixed, and neither Utility nor Analyst used the control-plane mismatch to mutate scientific criteria. Over-terminalization remains `LOW_TO_MODERATE_WATCH_IMPROVING`.

Development iteration is calibrated: iteration itself is not being punished. The new calibration requirement is that integrity-preserving support work must have request-scoped, machine-readable execution authority so default-deny does not silently convert a valid governance intent into indefinite provenance starvation.

## Funnel / mechanism supply / PRE_FORMAL

R83 canonical state: `33 = MECHANISM 13 / SYSTEM 20`; classification `33/33`; lifecycle `ACTIVE 1 / NONTERMINAL_HOLD 0 / TERMINAL_FOR_CURRENT_OBJECT 32`; development phases `OPEN_DEVELOPMENT 2 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`; PRE_FORMAL eligible/READY `1/1`; fresh FORMAL authority `0`; historical official consumed identities `7`.

Candidate 7/H7 remains `MECHANISM / FORMALIZE / READY(development-only) / RESULT_EXPOSED_DEVELOPMENT / ACTIVE`. Candidate 33 remains `SYSTEM / RESULT_EXPOSED_DEVELOPMENT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`. Mechanism supply remains `ONE_ACTIVE_MECHANISM_FORMALIZATION_LINEAGE; QUALITY_FLOOR_INTACT_BUT_MECHANISM_SUPPLY_THIN`.

PRE_FORMAL remains a nonconfirmatory development surface. PF-R1 contributes confirmatory count zero and has not been rerun/rescored. `HIDDEN_SECOND_FORMAL_GATE=false`.

## PASS reachability / prospective recommendations

PASS remains `REALISTIC_CONDITIONAL` without relaxing any evidence standard.

1. Keep Utility default-deny. Do not let Utility infer execution authority from Control/Analyst prose.
2. If Control still intends PF-R1 preservation, create the missing request-scoped schema-v2 decision/assignment/current pointer for the existing request; do not append a duplicate request and do not edit scientific state.
3. Once machine authority exists, preserve the already-existing PF-R1 artifact bytes only: no rerun, reconstruction, rescoring or reinterpretation; record exact workflow/head/artifact/digest and raw/summary checksums.
4. Keep R83's corrected authoritative R4 run/head/name/digest binding. Recover the existing R4 lock artifact; do not rematerialize merely because earlier mailbox metadata was wrong.
5. Keep R4 package/resource semantics fixed. If exact existing bytes prove incompatible with the fixed contract, STOP and version rather than silently rebind.
6. Preserve all literal prediction-only raw → immutable preserve → target-side scoring, concealed-evaluation, no-clobber/collision and exact runtime/source gates.
7. After all preidentity gaps close, require a fresh Analyst generation before any one-way FORMAL authority.

## Utility / hard floor / confidence

No new Utility request. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the sole request, but its request-level machine status is `PROPOSED_NOT_APPROVED` and no matching assignment/decision exists. The auditor does not dispatch or mutate Utility authority.

Hard floor: `CONFIRMED / DO NOT RELAX`.

Confidence: `HIGH` on the Utility authorization divergence, `HIGH` on continued FORMAL non-consumption, `HIGH` that R83 corrected the authoritative R4 artifact binding, `MEDIUM_HIGH` on final preidentity closure because both R4 durable lock capture and PF-R1 exact-byte preservation remain open. Fresh consumed-FORMAL end-to-end and fresh SYSTEM→MECHANISM successor remain `UNOBSERVED`.

Questions for future Control/Analyst: make the existing PF-R1 Utility authorization machine-resolvable if preservation is still intended; do not weaken Utility default-deny; confirm completed preservation is exact-byte/non-evidentiary only; keep R83's authoritative R4 tuple and R68 raw/holdout gates; and require a genuinely independent mechanistic residual plus fresh reduction/comparator/falsifier contract before any future SYSTEM→MECHANISM successor admission.
