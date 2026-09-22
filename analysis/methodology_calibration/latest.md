# SparkBrain Methodology Calibration Audit — R65

- schema_version: `2`
- generation_id: `METHCAL-20260922T201843+0900-R65-4B9E71C2`
- produced_at: `2026-09-22T20:18:43+09:00`
- supersedes: `METHCAL-20260922T192320+0900-R64-5E7A2C91`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- overall_classification: `MIXED_CALIBRATION`

## Material update

Candidate 33 has crossed an important development-observability boundary. Evidence Analyst R72 canonically classified it `SYSTEM / ARCHITECTURE_STUDY / OPEN_DEVELOPMENT` because exact-head CI `35713248880` stopped at lint before tests and therefore exposed no synthetic Architecture result. Since that mailbox was produced, authoritative repository evidence advanced the same branch to `71af7a36862eeb2b5d08c2a8f37462ed21acc972` via commit `cand33: fix architecture lint without science change`. The diff is formatting-only and is calibrated `SCIENCE_INVARIANT_REPAIR`.

At the repaired exact head, CI run `35715729340` now passes lint and local readiness on Python 3.11 and 3.13, then fails in the `Test` step on both versions. `Validate bundle` is skipped. The tracked tests are not generic plumbing only: they exercise SYSTEM-Architecture semantics including clean raw recomputation, mismatch verdicts, stale declared-digest rejection, and provenance-ledger binding failure. Therefore a meaningful synthetic development/conformance result has now been exposed even though no scientific claim or confirmatory evidence has been tested.

The exact failing assertion is not available from the structured job metadata. Accordingly the methodology auditor does not classify the next code change in advance. The correct prospective boundary is: preserve the failing run/provenance first; then a correction that merely makes implementation behavior conform to the already-fixed Architecture contract may remain same-object `SCIENCE_INVARIANT_REPAIR`. Any repair requiring change to raw schema, trust root, namespace/isolation semantics, resource caps, verdict vocabulary, comparator/provenance contract, or claim meaning is `SCIENCE_AFFECTING_CHANGE` and must use an explicit versioned development revision or fresh successor while preserving this failed result.

Because R72 predates this CI transition, its `OPEN_DEVELOPMENT` label is now stale relative to repository/CI state. Fresh Control/Analyst should explicitly decide the development-phase transition. Under HUMAN-20260922-005, the conservative calibration is to treat candidate 33 as `RESULT_EXPOSED_DEVELOPMENT` once the failed semantic conformance tests are durably acknowledged, rather than silently retaining OPEN while modifying science-facing semantics. This is an observability/state-lag defect, not an integrity breach: no post-test candidate-33 commit is observed yet.

H7 remains preidentity-only. The authoritative designated cycle-7 branch remains exactly `67ed8fad1d861463e4129d44efbb2540affd1889`. The latest MAIN stale-lease recovery independently observes that ref equality and records `identity_candidate_sha=null`, no FORMAL identity/result consumption, and explicit prohibition on identity, STARTED, protected evaluation and result-bearing execution.

## Authoritative refresh / hard floor

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Annotated `evidence/*` remains exactly five unchanged tag objects. Tag-form `formal/*`, `sealed/*` and `freeze/*` remain empty. No consumed FORMAL identity has been rerun, retuned, rescored or historically rewritten.

PF-R1 durable raw/summary byte preservation remains unresolved. The approved request `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` is still the latest request state and no execution completion is observed. This remains a preidentity H7 gate; rerunning PF-R1 is not an acceptable substitute.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase axis on active paths | `KEEP` |
| end-to-end through fresh consumed FORMAL | `INSUFFICIENT_EVIDENCE` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| candidate-33 lint-only repair before tests | `KEEP` |
| **development-phase transition after science-facing synthetic conformance result** | **`TIGHTEN`** |
| **candidate-33 next repair classification after test failure** | **`CLARIFY`** |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| repeated development rerun/retune non-independent accounting | `INSUFFICIENT_EVIDENCE` |
| prior-result semantic/hash lineage | `KEEP` |
| durable RESULT_EXPOSED raw/result byte preservation | `TIGHTEN` |
| mutable branch tip vs reviewed exact-head observability | `TIGHTEN` |
| FORMAL identity requires one freshly reviewed exact SHA | `TIGHTEN` |
| authoritative ref refresh over stale ops mailbox snapshot | `KEEP` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 mandatory reassessment with prospective information gain | `KEEP` |
| PRE_FORMAL as development surface | `KEEP` |
| `preformal_eligible` distinct from READY | `KEEP` |
| READY = well-defined/informative next test | `KEEP` |
| `HIDDEN_SECOND_FORMAL_GATE` | `false` / `KEEP` |
| current-object `claim_ceiling` | `KEEP` |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` |
| fresh terminal SYSTEM successor distinctness/non-rescue | `KEEP` |
| fresh SYSTEM→MECHANISM successor admission | `INSUFFICIENT_EVIDENCE` |
| `TERMINAL_FOR_CURRENT_OBJECT` topic scope | `KEEP` |
| successor potential ≠ automatic admission | `KEEP` |
| classification-completeness gating | `KEEP` |
| MAIN MECHANISM priority | `KEEP` |
| prospective SYSTEM-priority exception | `KEEP` |
| first genuine SYSTEM-over-comparable-MECHANISM exception | `INSUFFICIENT_EVIDENCE` |
| theory-backward quality floor / one-in-three supply | `KEEP` |
| `NO_COHERENT_MECHANISM_TARGET` liveness semantics | `KEEP` |
| SYSTEM architecture/testbed/reproducibility value | `KEEP` |
| PRE_FORMAL raw-before-score | `KEEP` |
| future FORMAL exact source/protocol/package/runtime/input/evaluator binding | `TIGHTEN` |
| FORMAL preserve-before-read / immutable evidence | `TIGHTEN` |
| comparator-equivalence verifier independence | `TIGHTEN` |
| protected/adaptive-evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Development phase end-to-end?** Mostly consistent through active development and H7 preidentity, but candidate 33 now exposes a state-lag stress case: the authoritative CI has a semantic conformance failure newer than the canonical OPEN label. Fresh consumed-FORMAL end-to-end remains unobserved.
2. **Cycle 3 a hard cap?** No. H7 remains in cycle 7 preidentity closure with prospective information gain.
3. **Repair split correct?** The lint repair is clearly science-invariant. The next candidate-33 repair cannot be classified until the exact test failure is known; contract-changing fixes must version.
4. **Rerun/retune laundering?** None observed. The failed candidate-33 test run must not be counted as confirmatory evidence or silently overwritten.
5. **Prior result preserved after exposure?** H7 semantic/hash lineage remains preserved but PF-R1 byte durability is unresolved. Candidate 33's first semantic conformance failure should now be preserved before any science-affecting redesign.
6. **FORMAL one-way integrity?** Unchanged; no new formal/sealed/freeze tag or H7 identity/result consumption exists.
7. **Fresh SYSTEM→MECHANISM successor?** Still unobserved. Candidate 33 remains a legitimate SYSTEM→SYSTEM fresh successor and does not reopen candidate 32.
8. **PRE_FORMAL hidden FORMAL?** No. PF-R1 remains development-only/nonconfirmatory and READY semantics remain development readiness.
9. **Terminal/supply calibrated?** Improving but thin: candidate 33 progresses as SYSTEM Architecture while MECHANISM supply remains essentially H7 alone.
10. **PASS reachable without weakening standards?** Yes conditionally; H7 still needs durable PF-R1 provenance, canonical identity-candidate fixation and remaining one-way binding/preserve/protected-evaluation closure.

## Funnel / supply / observability

The latest canonical Analyst population remains `33 = MECHANISM 13 / SYSTEM 20`, classification completeness `33/33`, `ACTIVE=2 / TERMINAL_FOR_CURRENT_OBJECT=31`, PRE_FORMAL eligible/READY `1/1`, fresh FORMAL authority `0`, and development phases `OPEN=3 / RESULT_EXPOSED=30 / canonical CONSUMED_ONE_WAY=0`. Those counts are retained as canonical until fresh Analyst review; they must not be silently recomputed from the new candidate-33 CI result.

Repository-level execution state is newer than the mailbox: candidate 33 exact head is `71af7a...`, lint/readiness are green, semantic tests fail, and no later candidate-33 commit is observed. The calibration issue is therefore classification/state lag, not post-result manipulation.

Mechanism supply health: `ONE_ACTIVE_MECHANISM_FORMALIZATION_LINEAGE_PLUS_ONE_SYSTEM_ARCHITECTURE_SUCCESSOR; QUALITY_FLOOR_INTACT_BUT_MECHANISM_SUPPLY_REMAINS_THIN`.

## Risks

False-positive risk: `LOW_TO_MODERATE_WATCH`. The localized risk is treating candidate 33 as still OPEN while making a science-facing contract change after a semantic conformance failure, which could launder result-responsive redesign as ordinary open development.

False-negative/opportunity-cost risk: `MODERATE_WATCH_IMPROVING`. Candidate 33 is active and terminal-topic suppression remains reduced, but MECHANISM supply is still a single effective lineage.

Moving-goalpost/rescue risk: `LOW_TO_MODERATE_WATCH_LOCALIZED_CAND33`. No rescue has occurred yet; the next repair is the stress point and must be classified from the exact failure before modification.

Over-terminalization risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. Candidate 32 remains terminal while distinct candidate 33 progresses.

## PASS reachability

PASS remains realistically reachable without lowering evidence standards. Development failures may be repaired or versioned, but none count as independent confirmatory evidence. H7 one-way consumption still requires a fresh exact identity candidate, durable PF-R1 development provenance, exact bindings, raw-before-score, preserve-before-read, immutable evidence and protected/adaptive validity.

## Prospective recommendations

Fresh Control/Analyst should durably acknowledge candidate-33 CI `35715729340` and decide whether the semantic test failure moves that object to `RESULT_EXPOSED_DEVELOPMENT`; the default should be yes unless the exact failure is shown to be purely non-semantic harness plumbing. Preserve the failing run/provenance before any science-affecting redesign. Only then classify the next fix: implementation conformance to already-fixed semantics may remain same-object invariant repair; any contract-semantic change must version or create a fresh successor.

For H7, keep `identity_candidate_sha` null until fresh authority explicitly fixes one reviewed exact SHA and all PF-R1 durability plus binding/preserve gates close. Do not infer identity readiness from ref equality or stale-lease recovery. Execute the existing PF-R1 preservation request rather than rerunning development.

## Utility / integrity / confidence

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the only bounded request relevant to current hard-preidentity provenance and is not observed executed.

Hard floor: `CONFIRMED / DO NOT RELAX`.

Confidence: `HIGH` that candidate 33 has advanced beyond lint to a failing science-facing synthetic test stage and that no post-failure candidate-33 commit exists; `MEDIUM` on whether the exact failing condition is science-invariant versus science-affecting because structured CI metadata does not expose the assertion; `LOW/UNOBSERVED` for fresh SYSTEM→MECHANISM and fresh consumed-FORMAL end-to-end.

Questions for Control/Analyst: will candidate 33 be transitioned from OPEN once this conformance failure is acknowledged? Will the exact failure be preserved and classified before repair? Will any contract-semantic fix be versioned rather than silently patched? Will H7 keep one-way identity blocked until PF-R1 byte durability and exact identity-candidate binding are closed?
