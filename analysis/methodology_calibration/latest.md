# SparkBrain Methodology Calibration Audit — R109

- schema_version: `2`
- generation_id: `METHCAL-20260924T152135+0900-R109-C4E92A1B`
- generated_at: `2026-09-24T15:21:35+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T141814+0900-R108-D7A41C9E`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `false`
- new_scientific_result: `false`

## Executive calibration

R109 independently re-fetched stable main, authoritative-tag policy, evidence refs, current Control and Evidence Analyst state, the current Theory/Revisit artifact, and the current Steward posture after reading prior Methodology R108 first. The only new upstream change since R108 is control-plane scheduler-health reconciliation: Control R57 restored the already-approved PRIMARY MAIN enabled state after a regression, and Evidence Analyst R118 reconciled that event without changing science, evidence credit, candidate state, Revisit state, or gate semantics.

Methodology calibration therefore remains unchanged. H7 is still `INCONCLUSIVE / CONSUMED_ONE_WAY / TERMINAL_FOR_CURRENT_OBJECT`; no second identity, rerun, retune, rescore, retry, post-outcome repair, or result-responsive comparator change is observed. Candidate #35 remains the sole `REVISIT_TRIGGERED` terminal object; no `REVISIT_PROPOSAL`, Revisit decision, Forge probe, canonicalization, or fresh successor exists. Canonical supply remains empty.

The standing provenance defect also remains unchanged: stable-main policy requires create-once annotated provenance-bearing tags for new authoritative identities when tooling permits, five pre-H7 evidence identities are annotated tag objects, while H7 `evidence/*` is still a lightweight direct-commit tag. Raw evidence refs remain 6 while policy-conforming annotated evidence identities remain 5. Steward G15's non-destructive adjudication remains the correct posture: preserve every existing H7 ref exactly; any future provenance supplement must be append-only, science-invariant, and point only to the already fixed preserve/result commits.

## Input generations and authoritative refs

- prior methodology: `METHCAL-20260924T141814+0900-R108-D7A41C9E`, audit branch tip before R109 persistence `0fff33c56461353207cdb3f358f35f94e0efbdac`
- stable main: `d16403414fc7abebd23075fc401240971b8eb91d`
- Evidence Analyst: `EVA-20260924T150100+0900-R118-POSTFORMAL-NOOP-CONTROL-R57-MAIN-R117`, branch tip `ec74807c04e23e561275f8a2900e11e8145076c3`
- Control Brain: `CTRL-20260924T145730+0900-R57-POSTFORMAL-TERMINAL-MAIN-RESTORED`, branch tip `376167105b9fb384efda60a98a1088809ddcca2d`
- Repository Steward: G15, branch tip `72fd00050786e41f1accae6a36efd9752183cd36`
- Theory/Revisit: `THEORY-20260924T093014+0900-R2-NO-PROPOSAL-5D7C1A94`, exact latest blob `6aa4fc2302336e887cf67070513948312fff0c98`
- Fast Forge: current durable no-op as reconstructed by Evidence Analyst R118; Revisit probes remain `0`
- authoritative tag policy: `docs/AUTHORITATIVE_TAGS.md`, blob `05905e23108722d759a06b226421fd6bbae93e38`
- H7 preserve commit: `a5e76e7eb117e0270cfdc138fb9da30d696aa7c0`
- H7 result commit: `e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`

Ops/control-plane branches are treated as role-separated mailboxes/history only; scientific claims are reconstructed from stable repository policy and exact scientific/evidence refs.

## Gate findings

- Hard scientific integrity floor: `KEEP`
- Development-phase semantics: `KEEP`
- Cycle-3 reassessment, not hard cap: `KEEP`
- Science-invariant vs science-affecting distinction: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY means informative next test, not success: `KEEP`
- FORMAL one-way integrity: `KEEP`
- Exact source/protocol/package/runtime/input binding: `KEEP`
- Raw-before-score: `KEEP`
- Preserve-before-read: `KEEP`
- Post-FORMAL terminal absorbency: `KEEP`
- Authoritative tag form/provenance: `TIGHTEN`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Triggered Revisit decision handoff: `KEEP`
- Trigger-to-proposal liveness: `CLARIFY`
- Revisit Forge new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- Revisit canonicalization: `INSUFFICIENT_EVIDENCE`
- Revisit bootstrap coverage/conservatism: `KEEP`
- Theory/canonical separation: `KEEP`
- Forge/canonical separation: `KEEP`
- Protected evaluation validity: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **Yes.** Current census remains `OPEN_DEVELOPMENT=0`, `RESULT_EXPOSED_DEVELOPMENT=34`, `CONSUMED_ONE_WAY=1`; H7 is the consumed object and no historical development result is retroactively upgraded.
2. Cycle 3 mistaken for a hard cap? **No evidence of that.**
3. Science-invariant vs science-affecting changes distinguished? **Yes.** H7 provenance/tag-form remediation remains governance-only and may not alter result, protocol, comparator, scorer, threshold, identity, or any existing authoritative ref.
4. Development observations kept out of independent evidence credit? **Yes.** Theory/Forge development remains zero-credit/noncanonical.
5. FORMAL one-way integrity unchanged? **Yes.** H7 remains terminal INCONCLUSIVE with no retry/rescore/repair path.
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **Neither observed.** Fresh successors still require a fresh ID, independent motivation/question, fresh reduction/comparator/falsifier contract, and fresh development state.
7. PRE_FORMAL genuine development? **Yes.** No hidden second FORMAL gate is observed.
8. Terminal semantics calibrated? **Yes.** All 35 current objects remain terminal; Revisit metadata is orthogonal.
9. Does Revisit catch genuinely changed conditions? **Yes.** Candidate #35 remains a concrete caught independent trigger.
10. Does Revisit avoid rescue laundering/zombie inflation? **Yes so far.** #35 remains terminal/SYSTEM/zero-credit and no successor or old-ID reopen was fabricated.
11. Do `REVISIT_FORGE_TEST` probes test new triggers rather than old failures? **Insufficient evidence.** No Revisit Forge probe has run.
12. Is bootstrap coverage complete and conservative? **Yes for all 35 terminal current objects.**
13. Is PASS realistically reachable without weakening standards? **Yes prospectively for genuinely fresh work.** H7 itself is permanently consumed and cannot be tuned toward PASS.

## Development / PRE_FORMAL calibration

Development semantics remain well calibrated. The current all-terminal census is internally coherent with `OPEN_DEVELOPMENT=0`, `RESULT_EXPOSED_DEVELOPMENT=34`, and `CONSUMED_ONE_WAY=1`. Repeated PRE_FORMAL or Forge observations carry no independent confirmatory credit. READY remains a statement about a well-defined informative next test, not a declaration of success.

Control R57's restoration of PRIMARY MAIN's already-approved enabled state is scheduler-health recovery only. It changes neither development state nor scientific readiness, and therefore does not justify a methodology-gate change.

## Moving-goalpost / rescue risk

Current rescue risk remains low. H7's main future hazard remains comparator laundering: its frozen result found all declared ordinary comparator families capacity-inadequate. A later capacity-adequate comparator capability may motivate a fresh question only if its development/motivation is independent of the observed H7 INCONCLUSIVE outcome. Building or tuning that capability because of the observed result would be outcome-responsive rescue.

Candidate #35 continues to show the opposite risk direction. A candidate-specific independent treatment-to-readout causal-opportunity mismatch is retained as a trigger without reopening the old object. The remaining liveness question is how an independently motivated `REVISIT_PROPOSAL` should arise without making trigger status itself automatic experiment permission.

## Revisit calibration / over-terminalization

The programme is neither visibly forgetting #35 nor reviving it as a zombie. #35 remains terminal/SYSTEM/zero-credit and is the sole `REVISIT_TRIGGERED` object. There is still no `REVISIT_PROPOSAL`, no dedicated Revisit decision, no Revisit Forge referral/probe, no canonicalization, and no fresh successor.

Current distribution remains `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=13`, `REVISIT_TRIGGERED=1`. H7 remains `DORMANT_REVISITABLE`; its INCONCLUSIVE outcome alone is explicitly not an independent trigger.

This remains calibrated but end-to-end trigger → independent proposal → trigger-focused Forge → reject/canonicalize behavior is still empirically untested.

## Bootstrap quality

Bootstrap remains complete and conservative. No historical evidence is reinterpreted, no old terminal ID is reactivated, no trigger is fabricated merely to fill an empty queue, and no inherited confirmatory credit is assigned from old/Forge/Theory/Revisit observations.

## Claim-type / mechanism-supply findings

SYSTEM/MECHANISM boundaries remain intact. No same-object post-outcome SYSTEM→MECHANISM upgrade and no manufactured successor is present. Canonical census remains `35 = 14 MECHANISM / 21 SYSTEM`, all terminal, with `0` active/queued/effectively executable canonical MECHANISM.

This is a real supply-health constraint but not evidence that scientific gates are too strict. The empty queue must not be repaired by weakening PRE_FORMAL/FORMAL/Revisit gates or by manufacturing Theory/Forge promotion.

## Pass reachability

PASS remains prospectively reachable without weakening evidence standards. The pipeline has already demonstrated that one-way START → target-blind raw preservation → protected target access/scoring can execute under the hard floor. A fresh candidate or independently motivated fresh successor can still pass if its prospective contract is met. The consumed H7 object cannot be used as a route to PASS.

## Provenance/publication calibration

Stable-main `docs/AUTHORITATIVE_TAGS.md` still specifies create-once annotated provenance-bearing tags with peeled-target verification for new authoritative tag identities when tooling permits. Fresh ref reconstruction still shows five evidence refs whose Git objects are annotated tags and one H7 evidence ref whose Git object is a direct commit (lightweight tag). No append-only H7 provenance supplement is observed.

Therefore `authoritative_tag_form_and_provenance=TIGHTEN` remains appropriate prospectively. Existing H7 refs must remain immutable historical artifacts; the defect is not repaired by rewriting or rerunning H7.

## Prospective recommendations

1. Keep every existing H7 identity/ref/result byte immutable. Never rerun, retune, rescore, retry, delete, move, replace, retype, or retarget them.
2. Keep policy-conforming annotated evidence identity count (`5`) separate from raw `evidence/*` ref count (`6`) until/unless a distinct append-only provenance attestation is created under Steward G15's constraints.
3. For future FORMAL publication, require annotated provenance-bearing tag creation and peeled-target verification before an evidence identity is counted policy-conforming.
4. Keep Candidate #35 terminal and its independent trigger visible. Do not fabricate a Revisit decision or Forge test while no independently motivated `REVISIT_PROPOSAL` exists.
5. If a fresh #35-like proposal later exists and `REVISIT_FORGE_TEST` is selected, Forge must cheaply attack only the new treatment-to-readout/observability rationale, never rerun or retune old priming.
6. Require any fresh #35-like canonicalization candidate to predefine a treated-state-sensitive observable or verified treatment-to-downstream path, falsifier, ordinary reduction ladder, and informative negative outcome; old/Forge/Theory/Revisit observations receive zero inherited confirmatory credit.
7. Treat any future H7 comparator-capability trigger as valid only with evidence that it was independently motivated/developed rather than tuned to the frozen INCONCLUSIVE result.
8. Do not relax gates because canonical MECHANISM supply is zero.

## Utility request

None.

## Hard-floor confirmation

This auditor dispatched no experiment, consumed no identity, mutated no research/evidence ref, merged no PR, changed no scheduler, and changed no scientific criterion. No consumed FORMAL rerun/retune/rescore, evaluator leakage, historical PASS/FAIL rewrite, silent post-FORMAL repair, or terminal-object reactivation was observed.

## Confidence

`HIGH`.

## Questions for Control / Analyst

- What explicit non-automatic mechanism, if any, should generate the first independent `REVISIT_PROPOSAL` for Candidate #35 without turning `REVISIT_TRIGGERED` into resurrection permission?
- Will future FORMAL publication make annotated provenance-bearing tag creation plus peeled-SHA verification a hard precondition for counting an evidence identity as policy-conforming?
- If H7 provenance supplementation is ever added, what create-only convention will ensure the supplement cannot be mistaken for a new scientific result or a replacement of any existing H7 ref?
- What evidence will establish that any future H7 capacity-adequate comparator capability was independently motivated rather than engineered in response to the observed INCONCLUSIVE outcome?
