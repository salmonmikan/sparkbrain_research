# SparkBrain Methodology Calibration Audit — R108

- schema_version: `2`
- generation_id: `METHCAL-20260924T141814+0900-R108-D7A41C9E`
- generated_at: `2026-09-24T14:18:14+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T132112+0900-R107-5B7F2D9A`
- overall_classification: `MIXED_CALIBRATION`
- new_scientific_result: `false`

## Executive calibration

R108 finds a material governance/revisit update but no new science. Repository Steward G15 has now independently adjudicated the H7 authoritative-tag representation defect that R107 left pending. The adjudication is correctly science-invariant and non-destructive: the existing H7 lightweight `freeze/*`, `formal/*`, `sealed/*`, and `evidence/*` refs are historical and must never be moved, deleted, replaced, retyped, retargeted, or used as grounds to rerun/rescore H7. Any future provenance supplement may only be append-only and point to the exact existing preserve/result commits.

The representation defect itself is not repaired: stable-main policy still specifies annotated provenance-bearing tags for new authoritative identities when tooling permits, five pre-existing evidence identities are annotated tag objects, while the H7 evidence ref remains a lightweight direct-commit tag. Policy-conforming annotated evidence identities therefore remain 5 while raw `evidence/*` refs total 6. This keeps overall calibration mixed: the science is one-way and well calibrated, but publication/provenance tooling remains too permissive prospectively.

Evidence Analyst R116 has also completed the explicit handoff review for Candidate #35. The independent treatment-to-readout causal-opportunity trigger remains valid, the old #35 object remains terminal/SYSTEM/zero-credit, and no `REVISIT_PROPOSAL` object exists. R116 correctly refuses to fabricate a Revisit decision, Forge referral, or successor merely because a trigger exists. This improves the previous handoff ambiguity without demonstrating end-to-end Revisit Forge/canonicalization behavior.

## Authoritative reconstruction

Prior methodology R107 was read first. Stable main, authoritative-tag policy, current evidence refs, H7 freeze/formal/sealed refs, current Analyst R116, Control R56, Repository Steward G15, and current literature handoff R42 were then independently re-fetched. Ops branches were treated only as role-separated mailboxes/control history, not scientific source of truth.

Authoritative findings:
- stable main remains `d16403414fc7abebd23075fc401240971b8eb91d`;
- the latest main delta is a fail-closed H7 workflow-dispatch registration stub, not a scientific substrate promotion;
- H7 remains one consumed identity with official outcome `INCONCLUSIVE` and no same-object repair/retry path;
- five pre-existing evidence refs resolve to annotated tag objects;
- H7 `evidence/*` resolves directly to result commit `e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85` as a lightweight tag;
- H7 `freeze/*` resolves directly to preserve commit `a5e76e7eb117e0270cfdc138fb9da30d696aa7c0` as a lightweight tag;
- H7 `formal/*` and `sealed/*` resolve directly to the same fixed result commit as lightweight tags;
- stable-main `docs/AUTHORITATIVE_TAGS.md` still requires create-once annotated provenance-bearing tags for new authoritative identities when tooling permits and forbids updating an existing authoritative tag;
- Steward G15 has now explicitly classified any permissible H7 remediation as append-only provenance only, with destructive normalization forbidden;
- no append-only H7 provenance attestation has yet been observed;
- Candidate #35 remains the sole `REVISIT_TRIGGERED` object; no old ID reopen, Forge probe, Revisit decision, canonicalization, or fresh successor is present;
- Theory R2 remains no-proposal for current work, TH-001 remains rejected for its current proposal, and current Fast Forge state remains zero-credit/noncanonical with `Revisit probes = 0`.

## Gate findings

- Hard scientific integrity floor: `KEEP`
- Development-phase semantics: `KEEP`
- Cycle-3 reassessment, not hard cap: `KEEP`
- Science-invariant vs science-affecting distinction: `KEEP` — G15 now makes the provenance-only/no-science-change boundary explicit
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY means informative next test, not success: `KEEP`
- FORMAL one-way integrity: `KEEP`
- Exact source/protocol/runtime/input binding: `KEEP`
- Raw-before-score: `KEEP`
- Preserve-before-read: `KEEP`
- Post-FORMAL terminal absorbency: `KEEP`
- Authoritative tag form/provenance: `TIGHTEN`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Triggered Revisit decision handoff: `KEEP` — trigger reviewed, no decision fabricated without a proposal object
- Trigger-to-proposal liveness: `CLARIFY` — #35 is not forgotten now, but the programme has not yet demonstrated how a valid trigger becomes an independently motivated proposal without automatic resurrection
- Revisit Forge new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- Revisit canonicalization: `INSUFFICIENT_EVIDENCE`
- Revisit bootstrap coverage/conservatism: `KEEP`
- Theory/canonical separation: `KEEP`
- Forge/canonical separation: `KEEP`
- Protected evaluation validity: `KEEP`
- Mechanism-supply health: `CLARIFY` — canonical supply is empty, but this is not evidence for weaker gates
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **Yes.** H7 is consumed one-way; other historical development objects remain result-exposed rather than being retroactively upgraded.
2. Cycle 3 mistaken for a hard cap? **No evidence of that.**
3. Science-invariant vs science-affecting changes distinguished? **Yes.** The H7 provenance mismatch is now explicitly bounded as append-only, science-invariant governance; no existing scientific ref may be rewritten.
4. Development observations kept out of independent evidence credit? **Yes.**
5. FORMAL one-way integrity unchanged? **Yes.** H7 remains terminal INCONCLUSIVE and cannot be rerun, retuned, rescored, retried, or repaired on the same object.
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **Neither observed.** A successor still requires a fresh candidate ID, independent motivation/question, and fresh falsifier/reduction contract.
7. PRE_FORMAL genuine development? **Yes.**
8. Terminal semantics calibrated? **Yes.** Terminal objects remain terminal and Revisit metadata remains orthogonal.
9. Does the Revisit ledger catch genuinely changed conditions? **Yes.** Candidate #35 remains a concrete caught trigger.
10. Does Revisit avoid rescue laundering/zombie inflation? **Yes so far.** A trigger did not reopen #35 or create a successor automatically.
11. Do `REVISIT_FORGE_TEST` probes test new triggers rather than old failures? **Insufficient evidence.** No Revisit Forge probe has run.
12. Is bootstrap coverage complete and conservative? **Yes for all 35 terminal current objects.**
13. Is PASS realistically reachable without weakening standards? **Yes prospectively for fresh work.** H7 itself is permanently consumed and cannot be tuned toward PASS.

## Development / PRE_FORMAL calibration

Development calibration remains good. `OPEN_DEVELOPMENT=0`, `RESULT_EXPOSED_DEVELOPMENT=34`, and `CONSUMED_ONE_WAY=1` is internally coherent with the current all-terminal census. PRE_FORMAL remains development-only; repeated observations carry zero confirmatory credit. No hidden second FORMAL gate is observed.

## Moving-goalpost / rescue risk

Current rescue risk remains low. The main prospective H7 hazard is comparator laundering: the frozen result found all declared ordinary comparator families capacity-inadequate. A later capacity-adequate comparator capability can support a fresh question only if its motivation/development is independently evidenced. Building or tuning it specifically because the observed H7 outcome was inconclusive would be outcome-responsive rescue, not a valid Revisit trigger.

Candidate #35 shows the opposite side: a valid independent trigger is being held without reopening the old object. That is calibrated. The remaining liveness question is how the programme creates a genuinely independent `REVISIT_PROPOSAL` without treating `REVISIT_TRIGGERED` itself as permission to experiment.

## Revisit calibration / over-terminalization

The programme is neither visibly forgetting #35 nor reviving it as a zombie. #35 remains terminal/SYSTEM/zero-credit, while the candidate-specific treatment-to-readout causal-opportunity mismatch is retained as a valid trigger. Literature R42 sharpens the prospective observability requirement but does not create a second trigger, inherited evidence, or reopen authority.

R116 correctly states that no `REVISIT_PROPOSAL` exists to classify. Therefore issuing `REVISIT_REJECTED`, `REVISIT_DORMANT`, `REVISIT_FORGE_TEST`, or `REVISIT_CANONICALIZE` now would fabricate a decision object. The correct current posture is to keep the trigger visible and wait for an independently motivated fresh proposal. End-to-end Revisit Forge and canonicalization behavior remains untested.

Current distribution remains `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=13`, `REVISIT_TRIGGERED=1`.

## Bootstrap quality

Bootstrap remains complete and conservative. No historical outcome was reinterpreted, no old terminal ID was reactivated, and no fabricated trigger condition or confirmatory credit was observed. H7's later addition as `DORMANT_REVISITABLE` remains orthogonal to its terminal `CONSUMED_ONE_WAY` state.

## Claim-type / mechanism-supply findings

SYSTEM/MECHANISM boundaries remain intact. No same-object SYSTEM→MECHANISM upgrade and no manufactured successor is present. Canonical mechanism supply remains empty: 35 terminal current objects and 0 active/queued/executable canonical MECHANISM. This is a supply-health concern, not a reason to relax scientific criteria or manufacture Revisit/Theory/Forge promotions.

## Pass reachability

The formal pipeline has already demonstrated that START → raw preservation → target access/scoring can execute under the hard floor. PASS remains prospectively reachable for fresh candidates or truly independent successors without weakening evidence standards. H7's consumed identity is not a route to PASS and must remain fixed as INCONCLUSIVE.

## Prospective recommendations

1. Preserve every existing H7 scientific identity/ref and result byte exactly. Never rerun, retune, rescore, retry, delete, move, replace, retype, or retarget them.
2. Follow Steward G15's adjudication: keep policy-conforming annotated evidence count (`5`) separate from raw `evidence/*` ref count (`6`) until/unless an append-only provenance attestation is created. Any supplement must point only to the existing exact preserve/result commits and must not imply a scientific upgrade.
3. Tighten future FORMAL publication so an evidence identity is not counted policy-conforming until annotated provenance-bearing tag creation and peeled-target verification succeed. The current H7 mismatch should remain a historical example, not be normalized by rewriting history.
4. Keep Candidate #35 terminal and the trigger visible. Do not fabricate a Revisit decision while no `REVISIT_PROPOSAL` exists. If a fresh proposal later exists and `REVISIT_FORGE_TEST` is selected, Forge must cheaply attack the new treatment-to-readout/observability rationale only, never rerun or retune old priming.
5. Require a fresh #35-like proposal to establish a prospectively sensitive treated-state/downstream observable, explicit falsifier, ordinary reduction ladder, and informative negative outcome before any canonicalization.
6. Accept any future H7 comparator-capability trigger only with evidence that it was motivated/developed independently of the observed inconclusive outcome.
7. Do not weaken gates merely because canonical MECHANISM supply is currently zero.

## Utility request

None.

## Hard-floor confirmation

This auditor dispatched no experiment, consumed no identity, mutated no research/evidence ref, merged no PR, changed no scheduler, and changed no scientific criterion. No consumed identity rerun/retune/rescore, historical PASS/FAIL rewrite, or terminal-object reactivation was observed.

## Confidence

`HIGH`.

## Questions for Control / Analyst

- What explicit mechanism, if any, should generate the first independent `REVISIT_PROPOSAL` for #35 without making `REVISIT_TRIGGERED` itself an automatic resurrection permission?
- Will future FORMAL publication tooling make annotated provenance-bearing tag creation/peeled-SHA verification a hard precondition for counting an evidence identity as policy-conforming?
- If H7 provenance supplementation is ever added, what create-only identity convention will keep all original refs immutable and prevent the supplement from being mistaken for a new scientific result?
- What evidence will establish that any future H7 capacity-adequate comparator capability was independently motivated rather than tuned in response to the observed inconclusive result?
