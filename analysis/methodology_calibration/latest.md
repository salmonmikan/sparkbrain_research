# SparkBrain Methodology Calibration Audit — R110

- schema_version: `2`
- generation_id: `METHCAL-20260924T162019+0900-R110-A7D35F91`
- generated_at: `2026-09-24T16:20:19+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T152135+0900-R109-C4E92A1B`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `true`
- material_change_scope: `FIRST_MATURE_REVISIT_PROPOSAL_AND_REVISIT_FORGE_TEST_REFERRAL_FOR_CANDIDATE_35`
- new_scientific_result: `false`

## Executive calibration

R110 read prior Methodology R109 first, then independently re-fetched stable `main`, `evidence/*`, current Control, Evidence Analyst R119, Theory/Revisit R3, Repository Steward posture, and MAIN R120. The material delta is methodological rather than scientific: Candidate #35 has progressed from a caught independent Revisit trigger to a bounded noncanonical `REVISIT_PROPOSAL`, and Evidence Analyst R119 has adjudicated that proposal as `REVISIT_FORGE_TEST`. No Revisit Forge probe has run yet, no fresh candidate ID exists, and no scientific result or evidence credit was created.

This is the first real end-to-end liveness advance for the new Revisit axis. The old Candidate #35 remains terminal `SYSTEM` with zero confirmatory credit. The proposal is driven by an independently identified treatment-to-readout causal-opportunity mismatch plus independent observability literature, and the authorized Forge contract is explicitly scoped to attack that new causal-opportunity/observability rationale rather than rerun or retune the old R100 priming experiment.

The referral is well calibrated at the authorization layer: preconditions must be fixed before probe outcome, old-ID reuse and R100 rerun/retune/rescore are prohibited, no seed/threshold/timing/readout optimization for success is permitted, protected evaluation is prohibited, and even survival returns only to a fresh Evidence Analyst with zero inherited confirmatory credit. Execution fidelity remains empirically untested because Fast Forge has not yet run `RVT35-FORGE-001`.

H7 remains `INCONCLUSIVE / CONSUMED_ONE_WAY / TERMINAL_FOR_CURRENT_OBJECT`; no same-object repair, rerun, retune, rescore, retry, or comparator rescue is permitted. Independent ref reconstruction still shows six `evidence/*` refs, with five annotated tag objects and the H7 evidence ref as a lightweight direct-commit tag. The prospective provenance/publication defect therefore remains and still warrants `TIGHTEN`, without rewriting any historical H7 ref.

## Input generations and authoritative refs

- prior methodology: `METHCAL-20260924T152135+0900-R109-C4E92A1B`, audit branch tip before R110 persistence `462299364d518c728795dc746be4f5ec323db6ae`
- stable main: `d16403414fc7abebd23075fc401240971b8eb91d`
- Evidence Analyst: `EVA-20260924T160200+0900-R119-CAND35-REVISIT-FORGE-TEST`, branch tip `b56a9c604f1e859076b2c721ffc53cc0c6739b21`
- Control Brain: `CTRL-20260924T155021+0900-R58-CAND35-REVISIT-PROPOSAL-AWAIT-ANALYST`, branch tip `3352ed6c00297fb7d6d61f193e002513f3178cf3`
- Theory/Revisit: `THEORY-20260924T152849+0900-R3-CAND35-REVISIT-CAUSAL-OPPORTUNITY-9C61E2B4`, branch tip `cc597a993fe30d6ba9ea05a30999d44a489ea467`, latest blob `4b537b407ab7961f6421bee14ed858f612f5b713`
- MAIN: R120 waiting for bounded Revisit Forge outcome, branch tip `6f1f8ac373b99d4346894f9591e2feb5cc2bcc13`
- Fast Forge: latest durable generation `FORGE-20260924T153500+0900-NOOP-R118-RAW-CAND35-REVISIT-AWAIT-ANALYST`; current Revisit probe count `0`
- Repository Steward: `STEWARD-20260924T135000+0900-G15-9F3C6A21`, branch tip `72fd00050786e41f1accae6a36efd9752183cd36`
- H7 result commit: `e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`
- evidence refs: `6`, of which `5` resolve to annotated tag objects and H7 resolves directly to a commit

Ops/control-plane branches are treated as role-separated mailboxes/history only. Scientific state is reconstructed from stable repository content, exact scientific refs, and prospective contracts.

## Gate findings

- Hard scientific integrity floor: `KEEP`
- Development-phase semantics: `KEEP`
- Cycle-3 reassessment, not hard cap: `KEEP`
- Science-invariant vs science-affecting distinction: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY means informative next test, not success: `KEEP`
- FORMAL one-way integrity: `KEEP`
- Raw-before-score / preserve-before-read / exact binding: `KEEP`
- Post-FORMAL terminal absorbency: `KEEP`
- Authoritative tag form/provenance: `TIGHTEN`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Trigger-to-proposal liveness: `KEEP`
- Revisit proposal adjudication: `KEEP`
- Revisit Forge authorization contract (new-trigger-only): `KEEP`
- Revisit Forge execution fidelity: `INSUFFICIENT_EVIDENCE`
- Revisit canonicalization: `INSUFFICIENT_EVIDENCE`
- Revisit bootstrap coverage/conservatism: `KEEP`
- Theory/canonical separation: `KEEP`
- Forge/canonical separation: `KEEP`
- Protected evaluation validity: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **Yes.** Census remains `OPEN_DEVELOPMENT=0`, `RESULT_EXPOSED_DEVELOPMENT=34`, `CONSUMED_ONE_WAY=1`; H7 is the consumed object and no historical development result is retroactively upgraded.
2. Cycle 3 mistaken for a hard cap? **No evidence of that.**
3. Science-invariant vs science-affecting changes distinguished? **Yes.** H7 provenance remediation remains science-invariant/append-only only; changes to metric, comparator, threshold, seed/exclusion, intervention, resource contract, hypothesis, falsifier or success criteria still require a revision/fresh successor.
4. Development observations kept out of independent evidence credit? **Yes.** Revisit Theory and any Forge probe carry zero confirmatory credit.
5. FORMAL one-way integrity unchanged? **Yes.** H7 remains terminal INCONCLUSIVE with no retry/rescore/repair path.
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **Neither observed.** Candidate #35 has no fresh ID yet; any later successor still requires fresh Analyst canonicalization, independent question, fresh reduction/falsifier contract and fresh development state.
7. PRE_FORMAL genuine development? **Yes.** No hidden second FORMAL gate is observed.
8. Terminal semantics calibrated? **Yes.** All 35 current objects remain terminal; Revisit metadata/decisions are orthogonal.
9. Does Revisit catch genuinely changed conditions? **Yes.** Candidate #35 progressed from an independently caught treatment-to-readout/observability trigger to a bounded fresh proposal.
10. Does Revisit avoid rescue laundering/zombie inflation? **Yes so far.** Old #35 remains terminal/SYSTEM/zero-credit, no new candidate ID exists, and the old R100 experiment is explicitly prohibited from rerun/retune/rescore.
11. Do `REVISIT_FORGE_TEST` probes test new triggers rather than old failures? **Authorization contract: yes. Execution: not yet observed.** `RVT35-FORGE-001` is scoped to the newly identified causal-opportunity/observability rationale, with fixed prospective substrate/readout/path and ordinary reductions, not old priming rescue.
12. Is bootstrap coverage complete and conservative? **Yes for all 35 terminal current objects.**
13. Is PASS realistically reachable without weakening standards? **Yes prospectively for genuinely fresh canonical work.** No pass route is created by repairing H7 or inheriting #35 observations.

## Development / PRE_FORMAL calibration

Development semantics remain well calibrated. Repeated PRE_FORMAL, Theory, Revisit, Audit and Forge observations remain development-only/non-evidentiary unless a later fresh prospective canonical object is created under the normal funnel. The new #35 Revisit referral does not create a hidden second FORMAL gate and does not convert development survival into scientific success.

## Moving-goalpost / rescue risk

Current rescue risk is low at the decision layer and becomes moderate only at the future Forge execution boundary. The Analyst-owned probe spec prospectively fixes treated substrate, observable, causal path, matched controls and sensitivity criterion before any probe outcome, and explicitly kills any path that requires result-responsive cue/threshold/timing/readout changes. This is the correct anti-laundering structure.

The main failure mode to watch is implementation drift: if Fast Forge starts searching substrates, thresholds, timings, readouts, seeds or comparator settings until a difference appears, the exercise would become rescue laundering. The correct response would be rejection/dormancy, not more probing.

## Revisit calibration / over-terminalization

Revisit liveness has materially improved. The system is no longer merely retaining a trigger: it produced an independently motivated proposal and a dedicated Analyst decision without reopening the old object. This lowers the false-negative risk that valuable old lines remain permanently forgotten.

At the same time zombie inflation remains controlled: only one of 35 terminal objects is `REVISIT_TRIGGERED`, only one proposal exists, only one bounded Forge referral exists, no fresh successor has been created, and all old/trigger/Theory/future-Forge observations retain zero confirmatory credit.

Current distribution remains `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=13`, `REVISIT_TRIGGERED=1`.

## Bootstrap quality

Bootstrap remains complete and conservative. The #35 trigger does not reinterpret the old frozen negative: it narrows what that negative established and asks a distinct causal-opportunity question. No historical PASS/FAIL is rewritten and no trigger is fabricated merely to fill an empty queue.

## Claim-type / mechanism-supply findings

SYSTEM/MECHANISM boundaries remain intact. Candidate #35 is still a terminal SYSTEM object; a future fresh successor is not pre-approved as MECHANISM and would require its own claim ceiling, comparator/reduction ladder, falsifier and fresh development state. H7 remains terminal MECHANISM/FORMAL INCONCLUSIVE.

Canonical executable MECHANISM supply remains `0`. That is a real throughput constraint but not evidence that gates are too strict. The Revisit lane should test scientific value cheaply without being used to manufacture canonical supply.

## Pass reachability

PASS remains realistically reachable for fresh prospective work without relaxing the evidence floor. The one-way pipeline has already demonstrated START → target-blind raw preservation → protected scoring ordering. Future evidence publication still needs prospective provenance enforcement so a scientifically valid run is also policy-conforming as an authoritative identity.

## Provenance/publication calibration

Independent ref reconstruction still shows five annotated `evidence/*` tag objects and the H7 evidence ref as a lightweight direct-commit tag. `authoritative_tag_form_and_provenance=TIGHTEN` remains prospective only. Existing H7 refs must remain untouched; no rerun or historical ref rewrite is justified.

## Prospective recommendations

1. Execute no action on old Candidate #35; if Fast Forge runs, enforce `RVT35-FORGE-001` exactly as written and terminate the probe if a sensitive path requires result-responsive substrate/cue/threshold/timing/readout/seed/comparator search.
2. Treat Forge survival as zero-credit information that returns only to a fresh Evidence Analyst; never auto-create a candidate from survival.
3. If the probe fails to demonstrate prospective treated→observable causal opportunity, or collapses under ordinary reductions, choose `REVISIT_REJECTED` or `REVISIT_DORMANT` rather than expanding the search surface.
4. If a later `REVISIT_CANONICALIZE` occurs, require a new candidate ID, fresh prospective question, fresh reduction/comparator/falsifier contract, informative negative outcome and zero inherited credit from #35/Audit/Theory/Revisit/Forge.
5. Keep every H7 identity/ref/result immutable and continue separating policy-conforming annotated evidence count (`5`) from raw evidence-ref count (`6`).
6. For future FORMAL publication, require annotated provenance-bearing tag creation plus peeled-target verification before counting an evidence identity as policy-conforming.
7. Do not relax scientific gates because canonical MECHANISM supply is zero.

## Utility request

None. No bounded Utility request is needed to test calibration at this stage; the already-authorized Revisit Forge probe is itself the next empirical methodology test and must remain within its existing lane.

## Hard-floor confirmation

This auditor dispatched no experiment, consumed no identity, mutated no research/evidence ref, merged no PR, changed no scheduler, and changed no scientific criterion. No consumed FORMAL rerun/retune/rescore, evaluator leakage, historical PASS/FAIL rewrite, silent post-FORMAL repair, or terminal-object reactivation was observed.

## Confidence

`HIGH` (`0.95`).

## Questions for Control / Analyst

- After `RVT35-FORGE-001` runs, will the review explicitly distinguish `NO_SENSITIVE_PATH`, `ORDINARY_REDUCTION`, and `BOUNDED_SENSITIVITY_SURVIVES` without adding extra search rounds?
- If sensitivity survives, what exact fresh-question/negative-informativeness test will be required before any `REVISIT_CANONICALIZE` decision?
- Will future FORMAL publication make annotated provenance-bearing tag creation plus peeled-SHA verification a hard precondition for counting an evidence identity as policy-conforming?
- What control will verify that a Forge implementation used the prospectively fixed substrate/readout/path rather than a result-responsive substitute?
