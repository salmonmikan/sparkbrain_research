# SparkBrain Methodology Calibration Audit — R111

- schema_version: `2`
- generation_id: `METHCAL-20260924T172000+0900-R111-C35A7F2E`
- generated_at: `2026-09-24T17:20:00+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T162019+0900-R110-A7D35F91`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `true`
- material_change_scope: `RVT35_UTILITY_TOOLING_AVAILABLE_AND_ANALYST_CONTROL_ACKNOWLEDGED_WITH_NO_CANDIDATE_SPECIFIC_PROBE_YET`
- new_scientific_result: `false`

## Executive calibration

R111 read Methodology R110 first, then independently re-fetched stable `main`, the authoritative tag policy, `evidence/*`, current Control R59, Evidence Analyst R120, Theory/Revisit R3, Utility R119 support tooling, current Forge refs, and the existing H7 result/evidence posture. The material delta is methodological and operational only: a reusable synthetic causal-opportunity/output-null diagnostic is now available on a dedicated Forge utility branch, Control has acknowledged the already-authorized `RVT35-FORGE-001` lane, and Evidence Analyst R120 explicitly records that no durable Candidate-35-specific Forge result exists yet.

The new utility harness is correctly labeled `NON_EVIDENTIARY_NONCANONICAL`, does not read Candidate #35 artifacts, R100 outcomes, protected evaluators, held-out payloads, formal results, or H7 material, and returns no promotion signal. Its implementation contains no internal fitting, threshold search, timing search, cue search, or result-responsive retuning. This is compatible with the anti-rescue design.

However, the harness is only supporting tooling, not the authorized Revisit Forge probe itself. It accepts an externally supplied JSON graph/readout/horizon/shift/sensitivity floor and does not cryptographically or procedurally enforce that those inputs were prospectively fixed before outcome inspection. It also directly screens only two ordinary failure modes — absence of a treated-to-observable path and output-null/cancelling readout projection — whereas `RVT35-FORGE-001` requires a broader ordinary-reduction and probe-faithfulness kill set. Therefore the tooling boundary is well calibrated, but execution fidelity and exact prospective input binding remain untested. The utility harness must not itself be counted as a Revisit Forge kill/survivor or as satisfaction of the whole probe contract.

Candidate #35 remains terminal `SYSTEM`, confirmatory credit `0`, `REVISIT_TRIGGERED`, with no fresh candidate ID and no canonical successor. Current Forge refs show no candidate-specific RVT35 result branch. The system is neither forgetting the valuable independent trigger nor reviving the old experiment.

H7 remains `INCONCLUSIVE / CONSUMED_ONE_WAY / TERMINAL_FOR_CURRENT_OBJECT`, with no rerun, retune, rescore or same-object repair. Independent `evidence/*` reconstruction still shows six refs: five annotated tag objects and H7 as a lightweight direct-commit tag. The prospective provenance/publication gate therefore remains `TIGHTEN`; no historical H7 ref should be rewritten.

## Input generations and authoritative refs

- prior methodology: `METHCAL-20260924T162019+0900-R110-A7D35F91`, audit branch head before R111 persistence `8b5be8eb9a1bf9b677c81c5837683fbc7f00e0dc`
- stable main: `d16403414fc7abebd23075fc401240971b8eb91d`
- Evidence Analyst: `EVA-20260924T170301+0900-R120-RVT35-FORGE-TOOLING-PENDING-PROBE`, branch head `3b7a3a0fd100614ed1b271ac14010e34683625ac`
- Control Brain: `CTRL-20260924T165135+0900-R59-CAND35-REVISIT-FORGE-TEST-AUTHORIZED`, branch head `6747ab029959abe7449a144fabbe212c3df7ed9f`
- Theory/Revisit: `THEORY-20260924T152849+0900-R3-CAND35-REVISIT-CAUSAL-OPPORTUNITY-9C61E2B4`, branch head `cc597a993fe30d6ba9ea05a30999d44a489ea467`
- MAIN: `MAIN-20260924T161228+0900-PRIMARY-R120-WAITING-CAND35-REVISIT-FORGE-TEST`, branch head `6f1f8ac373b99d4346894f9591e2feb5cc2bcc13`
- Fast Forge latest durable generation: `FORGE-20260924T153500+0900-NOOP-R118-RAW-CAND35-REVISIT-AWAIT-ANALYST`; durable Candidate-35-specific RVT35 result count `0`
- Utility: `UTILITY-20260924T163300+0900-R119-RVT35-CAUSAL-OPPORTUNITY-HARNESS-A7D13C2E`, ops branch head `e4e6e3f9628f1b766f195cb9579cf8b7e552f1e9`, support branch `forge/utility-rvt35-causal-opportunity-harness` head `7123c29804b4538d38c0c308451337279b31958d`, tool blob `6d9845cb39b0beaf4df4e576b65699fec66b8653`
- Repository Steward: `STEWARD-20260924T135000+0900-G15-9F3C6A21`, branch head `72fd00050786e41f1accae6a36efd9752183cd36`
- authoritative tag policy: `docs/AUTHORITATIVE_TAGS.md` blob `05905e23108722d759a06b226421fd6bbae93e38`
- H7 result commit: `e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`
- evidence refs: `6`, of which `5` resolve to annotated tag objects and H7 resolves directly to a commit

Ops/control-plane refs are treated as role-separated mailboxes and history only. Scientific state was reconstructed from stable repository content, exact scientific/evidence refs, and prospective contracts.

## Gate findings

- Hard scientific integrity floor: `KEEP`
- Development-phase semantics: `KEEP`
- Cycle-3 reassessment, not hard cap: `KEEP`
- Science-invariant vs science-affecting distinction: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY means informative next test, not success: `KEEP`
- FORMAL one-way integrity: `KEEP`
- Raw-before-score / preserve-before-read / exact FORMAL binding: `KEEP`
- Post-FORMAL terminal absorbency: `KEEP`
- Authoritative tag form/provenance: `TIGHTEN`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Trigger-to-proposal liveness: `KEEP`
- Revisit proposal adjudication: `KEEP`
- Revisit Forge new-trigger-only authorization contract: `KEEP`
- Revisit Utility tooling scientific boundary: `KEEP`
- Revisit Utility tooling sufficiency for full probe: `CLARIFY`
- Revisit Forge prospective input binding at execution: `CLARIFY`
- Revisit Forge execution fidelity: `INSUFFICIENT_EVIDENCE`
- Revisit canonicalization: `INSUFFICIENT_EVIDENCE`
- Revisit bootstrap coverage/conservatism: `KEEP`
- Theory/canonical separation: `KEEP`
- Forge/canonical separation: `KEEP`
- Protected evaluation validity: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **Yes.** Current census remains `OPEN_DEVELOPMENT=0`, `RESULT_EXPOSED_DEVELOPMENT=34`, `CONSUMED_ONE_WAY=1`; no result-exposed or consumed object was returned to OPEN.
2. Cycle 3 mistaken for a hard cap? **No evidence of that.** Reassessment remains informational rather than an automatic terminal rule.
3. Science-invariant vs science-affecting changes distinguished? **Yes.** The Utility harness is generic tooling only; metric/scorer meaning, scientific thresholds, comparator meaning, seed/exclusion policy, intervention, resource contract, hypothesis, falsifier and success criteria remain science-affecting and require prospective revision/fresh successor handling.
4. Development observations kept out of independent evidence credit? **Yes.** Audit, Theory/Revisit, Utility and future Forge observations retain zero confirmatory credit.
5. FORMAL one-way integrity unchanged? **Yes.** H7 remains terminal INCONCLUSIVE and consumed with no rerun/retune/rescore/repair path.
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **Neither observed.** Candidate #35 still has no new ID; any successor requires a meaningfully distinct fresh question, fresh reduction/comparator/falsifier contract and fresh development state.
7. PRE_FORMAL genuine development? **Yes.** No hidden second FORMAL gate is observed.
8. Terminal semantics calibrated? **Yes.** All 35 current objects remain terminal; Revisit status/decision is orthogonal metadata/control state.
9. Does Revisit catch genuinely changed conditions? **Yes.** Candidate #35's independent causal-opportunity/observability trigger progressed through proposal and bounded Forge referral without reopening the old object.
10. Does Revisit avoid rescue laundering/zombie inflation? **Yes so far.** Old #35 remains terminal SYSTEM with zero credit, no R100 rerun/retune/rescore, no fresh ID, and no canonical admission.
11. Do `REVISIT_FORGE_TEST` probes test new triggers rather than old failures? **Authorization and support-tool semantics: yes; actual probe execution: not yet observed.** The harness tests causal opportunity/output-null properties on synthetic prospective inputs and explicitly excludes old Candidate-35 artifacts, but exact fixed-case execution still needs independent verification.
12. Is bootstrap coverage complete and conservative? **Yes.** Legacy bootstrap covers 34 historical terminal/rejected objects and the current terminal ledger covers all 35; no historical outcome is rewritten and only one object is triggered.
13. Is PASS realistically reachable without weakening standards? **Yes prospectively for fresh canonical work.** Neither H7 repair nor inherited Candidate-35/Audit/Theory/Revisit/Forge observations create a PASS route.

## Development / PRE_FORMAL calibration

Development semantics remain well calibrated. Repeated PRE_FORMAL, Audit, Theory, Revisit, Utility and Forge observations do not accrue independent confirmatory credit. The new harness is a development support tool, not a hidden formal test and not a promotion signal.

## Moving-goalpost / rescue risk

Current rescue risk remains low at the authorization/tooling layer and moderate at the future candidate-specific Forge execution boundary. The Analyst-owned spec prospectively requires fixed substrate, observable, causal path, matched controls and sensitivity criterion, and prohibits result-responsive arm/cue/threshold/timing/readout changes.

The utility harness does not internally search those surfaces, which is good. But it accepts caller-supplied `horizon`, `treated_shift`, `sensitivity_floor`, graph edges and readout weights. Therefore the actual Forge runner must bind the exact case/config before observing output and must not rerun altered cases until one survives. Without that execution-level binding, the same neutral tool could still be used permissively by a caller.

## Revisit calibration / over-terminalization

Revisit liveness continues to improve without resurrection. Candidate #35 is not forgotten: the independent trigger has reached a dedicated Forge-test decision and now has neutral support tooling. Yet the old object remains terminal and no successor exists. This lowers false-negative risk without increasing current zombie inflation.

The crucial remaining empirical test is whether Fast Forge performs one bounded candidate-specific probe against the new trigger and then stops/returns to a fresh Analyst, rather than treating the generic harness as permission to search many synthetic cases.

Current distribution remains `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=13`, `REVISIT_TRIGGERED=1`.

## Bootstrap quality

Bootstrap remains complete and conservative. The Candidate #35 trigger narrows the interpretation of an old development result rather than rewriting it. No trigger condition was fabricated to fill the empty canonical queue, and the new Utility support does not add historical evidence credit.

## Claim-type / mechanism-supply findings

SYSTEM/MECHANISM boundaries remain intact. Candidate #35 remains a terminal SYSTEM object. A future successor is not pre-authorized as MECHANISM and would need a new claim ceiling and its own prospective scientific contract. H7 remains terminal MECHANISM/FORMAL INCONCLUSIVE.

Canonical executable MECHANISM supply remains `0`. The empty queue is a throughput condition, not evidence that standards are too strict, and the Revisit lane must not be used to manufacture supply.

## Pass reachability

PASS remains realistically reachable for genuinely fresh prospective candidates without relaxing evidence standards. The programme already demonstrated one-way START → target-blind raw preservation → scoring ordering. Future evidence publication still needs provenance-tag enforcement so a scientifically valid run also becomes policy-conforming evidence identity.

## Provenance/publication calibration

Independent ref reconstruction still shows five annotated `evidence/*` tag objects and the H7 evidence ref as a lightweight direct-commit tag. `authoritative_tag_form_and_provenance=TIGHTEN` remains prospective only. Existing H7 refs and result must remain untouched. The authoritative policy already states that metadata correction must not replace an existing authoritative tag and should instead use a separate audit/provenance record.

## Prospective recommendations

1. Treat the Utility harness as optional generic support only; it is not `RVT35-FORGE-001` itself and cannot by itself establish a Forge kill or survivor.
2. Before any candidate-specific Forge execution, durably bind the exact synthetic/candidate-specific case inputs that implement the Analyst-owned substrate/readout/path/control/sensitivity contract. Do not alter graph, readout, horizon, treated shift, sensitivity floor, cue, timing, seed, arm or comparator in response to observed output.
3. Apply the full Analyst kill/reduction set outside the two checks implemented by the utility harness; especially ordinary local-state/STP/recurrence/FSA/reservoir and probe-induced-reorganization alternatives must still be addressed prospectively.
4. If the bounded probe lacks a prospective causal path, requires result-responsive sensitivity changes, or collapses under ordinary reductions, prefer `REVISIT_REJECTED` or `REVISIT_DORMANT`; do not add exploratory rounds.
5. If bounded sensitivity survives, return zero-credit information only to a fresh Evidence Analyst. Do not auto-create a successor; `REVISIT_CANONICALIZE` still requires a fresh ID, meaningfully distinct question, fresh reduction/comparator/falsifier contract and informative negative outcome.
6. Keep H7 identity, outcome, result commit and every existing ref immutable. For future FORMAL publication, require annotated provenance-bearing tag creation and peeled-target verification before counting evidence as policy-conforming.
7. Do not weaken gates because canonical MECHANISM supply is zero.

## Utility request

None. Utility has already produced a bounded generic support harness in the existing authorized lane. Creating another Utility proposal would duplicate live work and risk widening the search surface.

## Hard-floor confirmation

This auditor dispatched no experiment, consumed no identity, mutated no research/evidence ref, merged no PR, changed no scheduler, and changed no scientific criterion. No consumed FORMAL rerun/retune/rescore, evaluator leakage, historical PASS/FAIL rewrite, silent post-FORMAL repair, or terminal-object reactivation was observed.

## Confidence

`HIGH` (`0.96`).

## Questions for Control / Analyst

- Before Fast Forge emits any Candidate-35-specific result, will it persist the exact case/config implementing the prospectively fixed substrate/readout/path/control/sensitivity contract so result-responsive case replacement is detectable?
- Will Control/Analyst explicitly reject treating the generic Utility harness's `CAUSAL_OPPORTUNITY_AND_FIXED_SENSITIVITY_PRESENT` output as a Revisit survivor unless the remaining ordinary-reduction and probe-faithfulness kills in `RVT35-FORGE-001` are also applied?
- After the first bounded candidate-specific probe, will review stop and classify rather than permit additional substrate/readout/horizon/threshold/timing/seed search rounds?
- If a bounded probe survives, what exact fresh-question and informative-negative-outcome criteria will be required before any `REVISIT_CANONICALIZE`?
- Will future FORMAL publication make annotated provenance-bearing tag creation plus peeled-SHA verification a hard precondition for counting an evidence identity as policy-conforming?
