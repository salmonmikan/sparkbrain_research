# SparkBrain Methodology Calibration Audit — R89

- schema_version: `2`
- generation_id: `METHCAL-20260923T202015+0900-R89-4A7D91C2`
- produced_at: `2026-09-23T20:20:15+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T192251+0900-R88-9F4C2D61`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The hard integrity floor remains unchanged. The material change since R88 is that the previously required post-preservation fresh H7 review has now actually occurred: Evidence Analyst R97 prospectively authorized exactly one future FORMAL one-way action on unchanged H7 R5, and R98 freshly re-confirmed that authority without broadening it. This is a methodology-positive transition, not a scientific result.

Independent repository re-fetch supports the gate facts rather than relying on the Analyst mailbox alone. H7 remains at exact research head `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; exact-head generic CI run `35794233612` is successful and dedicated NON_RESULT preidentity run `35794233687` is successful. The R5 preidentity workflow checks exact inherited runtime bytes and explicitly asserts that evaluation payload, seeds, FORMAL identity, STARTED marker, official prediction raw and official score are absent. Direct ref inspection finds no `control/h7*` or `preserve/h7*` ref. Therefore no H7 FORMAL identity is yet consumed.

The R97/R98 authority is narrowly prospective: before START/identity consumption, MAIN must independently re-match exact source/package/runtime/input/component/scorer/preserver bindings, fresh untouched evaluation identity/surface, absence of collision, literal target-blind raw-before-score, and preserve-before-read. Any pre-start mismatch is STOP before consumption. After START, the identity becomes CONSUMED_ONE_WAY and same-identity rerun/retune/rescore or outcome-responsive science-affecting repair remains forbidden. This is calibrated and does not relax the hard floor.

Crucially, PF-R1 preservation is not being laundered into confirmation. The preserved PF-R1 observation remains development-only. Its role was to close a provenance blocker so that a fresh Analyst could decide whether an unchanged prospective FORMAL test was ready. The current FORMAL authority requires a fresh untouched identity; no development observation is counted as independent confirmatory evidence.

Mechanism-supply calibration materially improves. Canonical R98 now has one viable executable/informative MECHANISM path, H7, with fresh prospective FORMAL authority `1` and consumed identity `0`. Candidate #35 remains SYSTEM / OPEN_DEVELOPMENT / preformal_eligible=false and is deferred behind H7; its prior temporary no-coherent-MECHANISM priority exception expires rather than being used to inflate #35 into a MECHANISM claim. This is a strong positive sign against both candidate starvation and rescue/manufacture pressure.

Independent stable-repository checks remain unchanged: `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; annotated `evidence/*` remains exactly five objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. No historical PASS/FAIL rewrite or fresh evidence-tag mutation is observed.

Overall remains `MIXED_CALIBRATION`, not because the new H7 decision is too permissive, but because the most consequential new boundary—the actual fresh FORMAL START through preserve-before-read and post-START one-way behavior—has not yet been observed end-to-end. Candidate #34 provenance ambiguity also remains an append-only record-quality issue, and global protected/adaptive-evaluation validity still requires continued tightening/verification. The active H7 gate itself is well calibrated.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| PF-R1 preserved development result remains nonconfirmatory | `KEEP` |
| H7 post-preservation fresh unchanged-R5 Analyst review | `KEEP` |
| H7 exactly-one prospective FORMAL authority | `KEEP` |
| H7 fresh untouched FORMAL identity requirement | `KEEP` |
| H7 pre-start exact source/package/runtime/input/component/scorer/preserver match | `KEEP` |
| H7 STOP-before-consumption on pre-start mismatch | `KEEP` |
| H7 literal target-blind raw-before-score requirement | `KEEP` |
| H7 preserve-before-read/target-side scoring requirement | `KEEP` |
| H7 same-identity rerun/retune/rescore after START | `TIGHTEN` |
| H7 outcome-responsive science-affecting repair after START | `TIGHTEN` |
| PF-R1 preservation treated as FORMAL evidence | `TIGHTEN` |
| development observations treated as independent confirmation | `TIGHTEN` |
| exact-head CI/preidentity treated as scientific support | `TIGHTEN` |
| candidate #35 SYSTEM ceiling after H7 becomes viable | `KEEP` |
| candidate #35 former NO_COHERENT_MECHANISM_TARGET exception expiration | `KEEP` |
| candidate #35 automatic PRE_FORMAL/READY promotion from green implementation | `TIGHTEN` |
| candidate #35 response before fresh Analyst gate | `TIGHTEN` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 as mandatory reassessment | `KEEP` |
| additional cycle for prospectively stated information gain | `KEEP` |
| terminal current object != topic death | `KEEP` |
| immediate same-family post-result rescue successor | `TIGHTEN` |
| fresh independently motivated MECHANISM successor | `KEEP` |
| specifically terminal SYSTEM→fresh MECHANISM successor behavior | `INSUFFICIENT_EVIDENCE` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| RESULT_EXPOSED SCIENCE_AFFECTING_CHANGE requires explicit version/fresh successor | `KEEP` |
| PRE_FORMAL as genuine development | `KEEP` |
| preformal_eligible distinct from READY | `KEEP` |
| READY = informative next test, not prior success | `KEEP` |
| HIDDEN_SECOND_FORMAL_GATE | `KEEP` |
| candidate #34 raw execution-source provenance | `TIGHTEN` |
| candidate #34 contract-authority vs run-authority provenance | `CLARIFY` |
| candidate #34 append-only clarification without raw rewrite/rerun | `KEEP` |
| raw-before-score as mere file ordering | `CLARIFY` |
| global literal target-blind prediction raw enforcement | `TIGHTEN` |
| global immutable preserve before target-side scoring/read | `TIGHTEN` |
| post-preserve scorer recomputation | `TIGHTEN` |
| target-sidecar independence | `TIGHTEN` |
| fresh concealed evaluation surface | `TIGHTEN` |
| global exact source/runner/scorer/preserver/runtime/input binding | `TIGHTEN` |
| current-object claim ceiling | `KEEP` |
| classification completeness | `KEEP` |
| MAIN MECHANISM priority when viable comparable MECHANISM exists | `KEEP` |
| genuine SYSTEM-over-comparable-MECHANISM exception | `INSUFFICIENT_EVIDENCE` |
| theory-backward quality floor | `KEEP` |
| protected/adaptive-evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** OPEN and RESULT_EXPOSED remain positively observed. H7 now has a clean prospective RESULT_EXPOSED→CONSUMED_ONE_WAY gate, but actual fresh post-HUMAN-005 consumption has not yet occurred, so complete end-to-end evidence remains insufficient.
2. **Is cycle-3 review being mistaken for a hard terminal cap?** No. #35's cycle-3 R2 completed a distinct prospectively stated NON_RESULT exact-binding question; it was neither auto-terminalized nor allowed to produce a response.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Yes in the live recent cases. #35's repair remained import/order/non-result guard work; H7 R5 exact head records an import-whitespace repair while scientific/runtime identity stays content-addressed. Any science-affecting post-START change remains prohibited for the consumed identity.
4. **Are development rerun/retune/tolerance revisions logged without laundering into independent evidence?** No laundering observed. PF-R1 remains development-only despite preservation; #34 remains one development result with zero confirmatory credit; #35 has no response. H7 FORMAL authority requires a fresh untouched identity rather than reusing a development identity.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Yes for #34 and H7/PF-R1. No prior result is rewritten or rescored. The H7 formal gate is prospective and unchanged-R5.
6. **Is FORMAL one-way integrity unchanged?** Yes. No H7 STARTED/control/preserve ref exists, stable main and five evidence tags are unchanged, and formal/sealed/freeze tag namespaces remain empty. The new authority is prospective only and explicitly one-way after START.
7. **Are legitimate fresh SYSTEM→MECHANISM successors being suppressed or manufactured?** No manufacture observed. When H7 becomes viable, #35 remains SYSTEM and its temporary SYSTEM-priority exception expires. The specific terminal-SYSTEM→fresh-MECHANISM successor case remains unobserved.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes. PF-R1 is not counted as confirmatory evidence; #35 remains outside PRE_FORMAL despite green implementation; H7 readiness is based on a well-defined fresh one-way test, not a requirement that the development observation already prove the claim.
9. **Are terminal semantics and candidate-supply controls calibrated?** Improved. H7 restores one viable MECHANISM path without reopening #34 or inflating #35. Current-object terminal semantics remain intact.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes. H7 now has a prospectively authorized exact-once path, but PASS can arise only through the still-strict fresh identity, exact binding, target-blind raw, preserve-before-read and one-way consumption chain.

## Development-iteration calibration

H7 is the key new calibration case. A meaningful development observation existed and its exact original bytes were durably preserved. Instead of treating that observation as confirmation or rerunning it, the programme closed the provenance blocker and then performed a fresh unchanged-R5 readiness review. The result is a new prospective FORMAL authorization for a fresh identity, not an upgrade of PF-R1 itself. This cleanly separates RESULT_EXPOSED development from consumed evidence.

The transition remains incomplete until a fresh FORMAL identity actually crosses START. At that moment the development-phase axis must change to CONSUMED_ONE_WAY for that FORMAL object, and no same-identity scientific repair, rerun or rescore may occur. Any failure before START is allowed to fail closed without consuming the identity only if no START/identity boundary has actually been crossed and no target-bearing information has leaked.

#35 remains a complementary OPEN_DEVELOPMENT case. Its green exact implementation is not READY by itself and does not compete with H7 by being inflated to MECHANISM. The former temporary SYSTEM-priority exception appropriately disappears once H7 supplies a viable MECHANISM path.

## Risk calibration

False-positive risk: `LOW_TO_MODERATE_WATCH`. The main live risk is no longer provenance closure; it is accidentally treating prospective H7 authority as permission to relax an exact pre-start binding, reuse an exposed/development identity, score before immutable preserve, or repair a consumed identity.

False-negative/opportunity-cost risk: `LOW_WATCH_IMPROVING`. H7 now restores a viable MECHANISM path and removes the previous zero-supply pressure. No criterion relaxation is needed.

Moving-goalpost/rescue risk: `LOW_WATCH`. H7 uses unchanged R5 and a fresh identity; #34 remains terminal for its current object; #35 remains SYSTEM.

Over-terminalization risk: `LOW_WATCH`. Candidate-supply pressure is materially reduced by H7 becoming viable, while legitimate fresh successors remain allowed prospectively.

## Funnel observability / mechanism supply

Canonical authority is now Evidence Analyst R98. Funnel: `35 = 14 MECHANISM / 21 SYSTEM`; lifecycle `ACTIVE=0 / QUEUED=2 / HOLD=0 / TERMINAL_FOR_CURRENT_OBJECT=33`; development `OPEN_DEVELOPMENT=3 / RESULT_EXPOSED_DEVELOPMENT=32 / canonical CONSUMED_ONE_WAY=0`; current nonterminal PRE_FORMAL eligible / READY `1 / 1`; viable executable/informative MECHANISM `1` (H7); fresh prospective FORMAL authority `1`; consumed fresh FORMAL identity `0`; official historical consumed scientific identities `7`; classification completeness `35/35`; SYSTEM-over-MECHANISM priority exceptions `0`.

Mechanism-supply health: `ONE_VIABLE_MECHANISM_H7_WITH_EXACTLY_ONE_PROSPECTIVE_FORMAL_PATH_NO_SYSTEM_INFLATION`.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. H7's PF-R1 observation remains development-only and is not required to count as a comparator/reduction/falsifier win before READY. The new formal authority asks a fresh prospective question on a fresh untouched identity. #35 likewise remains allowed real development without needing prior scientific success.

H7 pass reachability is now `REALISTIC_NEAR_TERM_PROSPECTIVE_WITHOUT_STANDARD_RELAXATION`. The preservation blocker and fresh-review blocker are closed. Remaining requirements are execution-time exact binding, fresh untouched identity/surface, literal target-blind raw-before-score, immutable preserve-before-read/target-side scoring, evaluator/held-out isolation and strict post-START one-way behavior.

## Utility request

No new methodology Utility request. The PF-R1 preservation task is complete and must not be duplicated, rerun, reconstructed, regenerated, retuned or rescored. Utility grants no scientific authority.

## Prospective recommendations

- Keep H7's R97/R98 authority narrow: exactly one fresh untouched FORMAL identity on unchanged R5 and no silent binding substitution.
- Immediately before any H7 START, independently verify exact source/package/runtime/input/component/scorer/preserver and absence of existing STARTED/control/preserve collision. Any mismatch is STOP before consumption.
- Preserve literal target-blind prediction raw immutably before any target-side score/read. Do not treat file naming/order alone as proof of this boundary.
- Once H7 START is crossed, mark that FORMAL identity CONSUMED_ONE_WAY and prohibit same-identity rerun, retune, rescore, threshold/tolerance/comparator/metric mutation or outcome-responsive repair.
- Do not count PF-R1, #34 PRE_FORMAL, green CI or preidentity success as independent confirmatory evidence.
- Keep #35 SYSTEM and response-stopped until its own fresh gate; its prior no-target priority exception has ended now that H7 is viable.
- Continue independent mechanism discovery and allow legitimate fresh successors, but do not manufacture a successor from a disappointing outcome.
- Keep #34 raw immutable; any provenance correction remains append-only clarification only.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: stable main/evidence-tag nonmutation `HIGH`; H7 exact branch head `HIGH`; H7 generic CI and dedicated NON_RESULT preidentity success `HIGH`; absence of H7 control/preserve refs `HIGH`; H7 current identity nonconsumption `HIGH`; prospective exactly-one authority existence `HIGH`; actual execution-time exact binding `NOT_YET_OBSERVED`; fresh post-HUMAN-005 CONSUMED_ONE_WAY transition `UNOBSERVED`; protected target-blind preserve-before-read behavior in the coming H7 FORMAL run `UNOBSERVED`; repeated result-bearing PRE_FORMAL `UNOBSERVED`; terminal SYSTEM→fresh MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will H7 execution materialize exactly one fresh untouched identity and fail closed before START on any exact-binding mismatch?
- Will the first START boundary atomically end any same-identity rerun/repair authority even if execution later fails?
- Will prediction-only raw be durably preserved before any target-side scoring/read, with target-bearing data kept out of the prediction producer?
- Will PF-R1 remain development-only with zero independent confirmatory credit after H7 FORMAL begins?
- Will #35 remain SYSTEM/deferred rather than being promoted merely because its Architecture implementation is green?
- Will any future post-result science-affecting change remain explicit versioned development or a genuinely fresh successor preserving prior results?

## Input generations / authoritative refs used

- previous Methodology: `METHCAL-20260923T192251+0900-R88-9F4C2D61@55655e6e39432e09aa3389122acaa9ec57ab8af7`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-20260923T155900+0900-R43-A91C4E6B@1592c3b52a8a545aa2503fd4618c0a761921ef1e`
- Evidence Analyst: `EVA-20260923T200231+0900-R98-2B6F91C4@df2e59996409211a2b104918e01a7f61d0eb3c80`
- Evidence Analyst decision history: `EVA-20260923T192140+0900-R97-6D82A4F1`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- evidence tags: exactly five annotated `evidence/*`; tag-form `formal/*`, `sealed/*`, `freeze/*` empty
- H7 R5 exact head: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- H7 exact-head CI: `35794233612` success
- H7 dedicated NON_RESULT preidentity: `35794233687` success
- H7 `control/h7*`: absent
- H7 `preserve/h7*`: absent
- #35 exact head remains `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@8ea6581544c642ad74f1a95955ab2c5f795afccc`
- PF-R1 preservation completion remains the prerequisite closure from R88; no scientific authority was created by preservation
