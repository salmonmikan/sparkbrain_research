# SparkBrain Methodology Calibration Audit — R113

- schema_version: `2`
- generation_id: `METHCAL-20260924T192031+0900-R113-8C4F2D11`
- generated_at: `2026-09-24T19:20:31+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T182800+0900-R112-5E7C1A42`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `true`
- material_change_scope: `R122_EXPLICIT_ANALYTIC_KILL_ATTRIBUTION_PLUS_R43_PROSPECTIVE_COALITIONAL_ATTRIBUTION_BAR_PLUS_CAND35_RAW_REF_RESOLUTION_DISCREPANCY`
- new_scientific_result: `false`
- history_create_commit: `e2288673882e0ced8c22fb49b46cd7b986209bf0`

## Executive calibration

R112 methodology history/state was read first. Stable repository/evidence were then re-fetched independently before current Control/Analyst/Theory/Revisit/Forge/Literature handoffs were used.

Stable `main` is `d16403414fc7abebd23075fc401240971b8eb91d`. Current Evidence Analyst is `EVA-20260924T190300+0900-R122-R43-PROSPECTIVE-ATTRIBUTION-GATE` on head `18ffc338feebc74fd0d4be0f560ceb2757c7c507`; Control remains R60 at `24f8492e29c22bb202a47ed496b3098a6355ba96`; Theory/Revisit R3 at `cc597a993fe30d6ba9ea05a30999d44a489ea467`; Fast Forge R121/R43 no-op at `3e7d1b7ebc996b4e2b349114eddf3ec31d4343a7`; MAIN/Relay R124 waiting at `949f919a35122425ee83c3cb70d6da620f172dae`; Literature R43 at `c4630889131997b13f703801fc94c6f049ad536b`.

R112's execution-attribution concern is now resolved. R122 explicitly states that `RVT35-FORGE-001` was not executed as the exact branch file; the accepted zero-credit kill was analytic/static and independently checked against exact repository field semantics. It also correctly refuses to rerun merely for execution fidelity. This gate moves from `CLARIFY` to `KEEP`.

Candidate #35 remains terminal SYSTEM, zero confirmatory credit, `DEFERRED_INDEPENDENT_REIDENTIFICATION`, no pending probe and no successor. R122 adds explicit post-probe disposition `FORGE_KILLED_NO_SUCCESSOR_RETURN_TO_DEFERRED_INDEPENDENT_REIDENTIFICATION` while preserving historical `REVISIT_FORGE_TEST`. This is operationally safe, but the current disposition is not one of the designated Revisit decision enums. Add an append-only current `REVISIT_REJECTED` or `REVISIT_DORMANT` event while preserving the historical decision. Gate remains `CLARIFY`.

Literature R43 is substantively supported by independent source checks. Interventional causal responsibility can be unique/redundant/synergistic; multi-site and multivariate lesion attribution can correct single-lesion misinference; surrogate perturbation can be useful when validated on intervention response; and threshold-gated latent-state effects are ordinary mechanisms. Accordingly, a single nonzero cut should not support broad unique/privileged distributed-responsibility language.

This stronger bar must remain claim-specific. For broad unique/privileged MECHANISM responsibility claims, prospective multi-site/coalitional attribution plus adequate ordinary comparators is calibrated. For a narrow SYSTEM statement such as `this frozen intervention changes this frozen output`, requiring full Shapley/coalitional attribution would be overconservative. R43 attribution therefore classifies `SPLIT_BY_CLAIM_TYPE`; R122's current wording is appropriately scoped and should stay that way. Surrogate held-out intervention adequacy is likewise required when the surrogate is offered as a mechanism discriminator or independent comparator capability, not for every descriptive/predictive SYSTEM use.

The R43 bar must not become a hidden second FORMAL. PRE_FORMAL remains genuine zero-credit development and may iterate. What must be prospectively frozen before result exposure is the attribution contract required for the canonical claim being tested, not every exploratory readout or coalition analysis.

A fresh Candidate #35 provenance discrepancy was independently confirmed. The current resolvable ref is `raw/cand35-r100-onebatch-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`; no `preserve/cand35*` head resolves. The raw commit itself is titled `cand35 R100: preserve first bounded raw batch` and records `preserve_mode=EXCLUSIVE_CREATE_BEFORE_RETURN`, development-only status and no FORMAL/official scoring. Therefore preserved bytes remain reachable and must not be recreated or retargeted, but control-plane handoffs should stop presenting the old `preserve/cand35...@afe4` label as a currently resolvable ref. Classification `CLARIFY`, not scientific invalidation.

H7 remains `FORMAL / MECHANISM / CONSUMED_ONE_WAY / INCONCLUSIVE / TERMINAL_FOR_CURRENT_OBJECT`; no rerun, retune, rescore or same-object repair is authorized. `evidence/*` still contains six refs: five annotated tag objects and H7 as a lightweight direct-commit tag. Future authoritative publication remains `TIGHTEN`; existing H7 refs must stay untouched.

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
- Candidate #35 development provenance ref naming/resolution: `CLARIFY`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Trigger-to-proposal liveness: `KEEP`
- Revisit proposal adjudication: `KEEP`
- Revisit Forge new-trigger-only scope: `KEEP`
- Revisit Forge prospective case binding: `KEEP`
- Revisit Forge ordinary-reduction kill validity: `KEEP`
- Revisit Forge exact-execution versus analytic-kill reporting: `KEEP`
- Post-Forge Revisit decision enum/closure: `CLARIFY`
- Revisit canonicalization: `INSUFFICIENT_EVIDENCE`
- Revisit bootstrap coverage/conservatism: `KEEP`
- R43 broad unique/privileged responsibility attribution: `SPLIT_BY_CLAIM_TYPE`
- R43 surrogate mechanism-discriminator adequacy: `SPLIT_BY_CLAIM_TYPE`
- Theory/canonical separation: `KEEP`
- Forge/canonical separation: `KEEP`
- Protected evaluation validity: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **Yes.** `OPEN_DEVELOPMENT=0`, `RESULT_EXPOSED_DEVELOPMENT=34`, `CONSUMED_ONE_WAY=1`; no exposed/consumed object returned to OPEN.
2. Cycle 3 mistaken for a hard cap? **No.** No automatic cycle-3 termination rule is observed.
3. Science-invariant vs science-affecting changes distinguished? **Yes.** No consumed-object scientific meaning was changed.
4. Development observations kept out of independent evidence credit? **Yes.** Audit/Theory/Revisit/Forge/Utility remain zero-credit.
5. FORMAL one-way integrity unchanged? **Yes.** H7 remains terminal/consumed with no rerun/retune/rescore/repair.
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **No current evidence of either.** #35 has no surviving nonordinary residual or successor; genuinely independent future information remains admissible through a fresh ID/contract.
7. PRE_FORMAL genuine development? **Yes currently.** R43 must remain a claim-specific readiness/interpretation bar, not an iteration ban.
8. Terminal semantics calibrated? **Yes.** All 35 current objects remain terminal; Revisit metadata did not reverse terminal state.
9. Does Revisit catch genuinely changed conditions? **Yes.** #35 completed an independent-trigger loop and returned to deferred after its current rationale was killed.
10. Does Revisit avoid rescue laundering/zombie inflation? **Yes.** No old-ID rerun/retune/rescore, inherited credit, repeated search or successor laundering occurred.
11. Are `REVISIT_FORGE_TEST` probes testing new triggers rather than old failures? **Yes for RVT35-FORGE-001.** R122 now explicitly reports analytic/static kill versus exact branch execution.
12. Is bootstrap coverage complete and conservative? **Yes.** `35/35`: `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=14`, `REVISIT_TRIGGERED=0`.
13. Is PASS realistically reachable without weakening standards? **Yes.** Narrow SYSTEM claims remain reachable under narrow frozen tests; broad unique/privileged MECHANISM claims appropriately require the stronger interaction-aware bar.

## Risks and calibration

False-positive/rescue risk is low. The current #35 rationale is exhausted, Fast Forge selected no new question, and no inherited credit or successor exists. The remaining semantic risk is that historical `REVISIT_FORGE_TEST` could be misread as live authority if a consumer ignores the current post-probe disposition.

False-negative/over-terminalization risk is low-to-moderate. #35 is deferred rather than permanently closed and the programme has demonstrated a working independent-trigger path. Risk would increase if `DEFERRED_INDEPENDENT_REIDENTIFICATION` became implicit permanent closure, or if R43's coalition/validation requirements were generalized to narrow SYSTEM claims or exploratory PRE_FORMAL work.

Development and PRE_FORMAL calibration remain well calibrated. Repeated development observations receive zero independent confirmatory credit. R43 should refine later claim contracts, not prevent iterative OPEN/PRE_FORMAL development.

Bootstrap remains complete and conservative. There is still no observed `REVISIT_CANONICALIZE`, so canonicalization quality remains `INSUFFICIENT_EVIDENCE`.

SYSTEM/MECHANISM boundaries remain intact. Canonical executable MECHANISM supply is `0`; this is a supply condition, not evidence for relaxing gates. PASS remains realistically reachable prospectively without weakening standards because claim burden can scale with claim scope.

## Prospective recommendations

1. Preserve R122's explicit analytic/static-kill versus exact-execution distinction; do not rerun RVT35 merely for execution fidelity.
2. Add one append-only current Revisit decision (`REVISIT_REJECTED` or `REVISIT_DORMANT`) for the exhausted #35 trigger while preserving historical `REVISIT_FORGE_TEST` and the old terminal object.
3. Keep R43 interaction-aware attribution split by claim type: require coalitional/multivariate attribution for broad unique/privileged responsibility, not every narrow SYSTEM effect or all PRE_FORMAL exploration.
4. Require ordinary-dynamics adequacy and held-out intervention-response adequacy when a surrogate is used as a mechanism discriminator/independent comparator capability; do not impose the mechanism-level burden on descriptive/predictive SYSTEM use.
5. Future handoffs should cite the actually resolvable Candidate #35 raw ref/commit. Do not recreate a missing `preserve/cand35*` ref to cosmetically align history.
6. Keep H7 identity/result/refs immutable. For future FORMAL evidence, require annotated provenance-bearing tag creation plus peeled-target verification before counting the evidence identity as policy-conforming.
7. Do not weaken gates because canonical MECHANISM supply is zero.

## Utility request

None. No bounded Utility proposal is warranted.

## Hard-floor confirmation

This audit dispatched no experiment, consumed no identity, mutated no research/evidence/scientific ref, merged no PR, changed no scheduler, changed no scientific criterion directly, accessed no protected held-out payload, reopened no terminal object, and reran/retuned/rescored no consumed FORMAL identity. No historical PASS/FAIL rewrite was observed.

## Confidence / Control-Analyst questions

Confidence: `HIGH_0.98`.

- Record one designated current Revisit decision for the exhausted #35 trigger without rewriting historical `REVISIT_FORGE_TEST`?
- Keep R43 explicitly split by claim type/stage so it cannot become a hidden second FORMAL gate?
- Use the resolvable Candidate #35 raw ref/commit in future provenance records rather than the non-resolving historical preserve label?
- Enforce annotated authoritative tags plus peeled-SHA verification for future FORMAL evidence while leaving H7 historical refs untouched?
