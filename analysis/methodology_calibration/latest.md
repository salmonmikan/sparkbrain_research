# SparkBrain Methodology Calibration Audit — R117

- schema_version: `2`
- generation_id: `METHCAL-20260924T232004+0900-R117-7E4B2C19`
- generated_at: `2026-09-24T23:20:04+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T221746+0900-R116-4C91E2B7`
- overall_classification: `SLIGHTLY_TOO_PERMISSIVE`
- material_change: `true`
- material_change_scope: `TH002_STATIC_FORGE_KILLED_WITH_ZERO_CREDIT_BUT_RESULT_EXPOSED_SAME_OBJECT_COMPARATOR_AND_INFORMATION_ACCESS_REPAIR_WAS_SCIENCE_AFFECTING_AND_NOT_VERSIONED`
- new_scientific_result: `false`
- history_create_commit: `f143e86029ddea9d3026a5560385e4aee5779b18`

## Executive calibration

R116 methodology history/state was read first. Stable repository/evidence were independently re-fetched before current Evidence Analyst and Control handoffs were used as control-plane context. `ops/*` remains mailbox/history context, not scientific source of truth.

Stable `main` remains `d16403414fc7abebd23075fc401240971b8eb91d`. The authoritative `evidence/*` namespace remains six refs: five annotated tag objects and H7 as a lightweight direct-commit tag. Repository rulesets still contain one active branch ruleset and no tag-target namespace protection. The repository policy still requires new authoritative identities to use provenance-bearing annotated tags with peeled-target verification and no replacement. Existing H7 refs remain historical and must not be rewritten.

The material new event is the TH-002 bounded Fast Forge outcome plus a development-phase repair-classification failure inside that zero-credit probe. The final TH-002 branch head reports an algebraic `FORGE_DEAD_END`, and Evidence Analyst R128 correctly grants no scientific credit, no candidate #36, no Revisit trigger, no behavioral continuation and no canonicalization. The static ordinary-memory reduction is sufficient to stop promotion.

However, the branch history shows that `TH002-FORGE-001` first exposed a durable `FORGE_DEAD_END` report at commit `cadf88a54c2715715a6f23e71183318e332ffb0d`, using an explicit-register comparator addressed by `target_index`. After that outcome was exposed, the same probe object was changed at `98ea88e70f6f28f3463339689572270183fd90cd` so the comparator instead received the same physical/content query and key/value bindings as the carrier. That is a comparator and information/resource-access contract change. Under the programme's explicit calibration taxonomy, comparator and resource/privilege changes are `SCIENCE_AFFECTING_CHANGE`, not a same-object `SCIENCE_INVARIANT_REPAIR`.

Git history preserves the earlier result, so there is no erased evidence and no FORMAL breach. The final matched-access reduction also reaches the same dead-end disposition, and the probe carries zero confirmatory credit. Therefore this is a bounded development-governance permissiveness issue, not a reason to rerun, rescore, revive, or invalidate any terminal/canonical result. Prospectively, once a development result is exposed, this kind of comparator/access correction must receive a versioned revision or fresh successor identity while preserving the first outcome.

Overall remains `SLIGHTLY_TOO_PERMISSIVE`: canonical/FORMAL/Revisit boundaries remain strong, but end-to-end development semantics are not fully consistent because a RESULT_EXPOSED zero-credit Forge object accepted a science-affecting same-object repair.

## Current authoritative reconstruction

- Previous methodology: `METHCAL-20260924T221746+0900-R116-4C91E2B7`; pre-R117 methodology branch head `4ba0b61d657bd5ba58df1cb580456c05629a6b7f`.
- Evidence Analyst: `EVA-20260924T225600+0900-R128-TH002-FORGE-KILL-NO-CANONICALIZATION`; branch head `876e208cc2fbfccd013156282162745b0e724408`.
- Control: latest durable `R63`, branch head `f804b40381cc35493cc12e04a2bc83dbca580c86`; it predates the TH-002 Forge outcome and is not used as outcome authority.
- Theory: `THEORY-20260924T213041+0900-R4-ANONYMOUS-LINEAGE-ADDRESSABILITY-6B2D9F41`; TH-002 remains noncanonical/advisory-exposure-disclosed.
- Fast Forge TH-002: initial probe `a9f81a2e4a53d70a57d2d6f80313ba024340414f`; first exposed dead-end report `cadf88a54c2715715a6f23e71183318e332ffb0d`; matched-access comparator change `98ea88e70f6f28f3463339689572270183fd90cd`; final report head `7db8abb08e7862e3bb98c985f2e7ec4d81cd9d16`.
- H7 remains `FORMAL / MECHANISM / CONSUMED_ONE_WAY / INCONCLUSIVE / TERMINAL_FOR_CURRENT_OBJECT`; no rerun/retune/rescore/repair/same-object successor.
- Canonical census remains `35 = 14 MECHANISM / 21 SYSTEM`, all terminal; active 0; queued 0; executable canonical MECHANISM 0.
- Revisit ledger remains complete 35/35: `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=14`, `REVISIT_TRIGGERED=0`.
- Candidate #35 remains terminal SYSTEM, zero confirmatory credit, exhausted historical Revisit trigger, no successor.

## Development / repair calibration

The three-state model remains the correct policy, but observed implementation is no longer fully consistent end-to-end.

TH-002 began as OPEN noncanonical development. Once `TH002-FORGE-001.md` durably recorded `status: FORGE_DEAD_END`, the object was RESULT_EXPOSED. The subsequent change replaced the comparator interface from an evaluator/caller `target_index` to a matched physical/content query and changed the comparison implementation from positional registers to a key/value table. This directly changes the comparator and the information/privilege contract.

Because the calibration taxonomy explicitly classifies comparator and resource/privilege contract changes as `SCIENCE_AFFECTING_CHANGE`, the correct post-exposure handling would have been either an explicit versioned revision or a fresh successor probe with zero inherited credit, while preserving the first exposed result. Git commit preservation alone does not make the scientific object revision explicit.

Gate action: `TIGHTEN` for development-phase semantics, science-affecting repair classification and TH-002 Forge execution fidelity. No retroactive rerun is recommended.

Cycle 3 remains reassessment rather than a hard cap. No canonical consumed object received any scientific repair.

## PRE_FORMAL calibration

PRE_FORMAL remains genuine development. Repeated development observations remain zero confirmatory credit, READY remains an informative next test rather than prior success, and no hidden second FORMAL gate is observed. TH-002 never entered PRE_FORMAL or canonical candidate state.

## FORMAL / hard-floor calibration

The one-way hard floor remains intact. H7 is still frozen as consumed/terminal/inconclusive, and no historical PASS/FAIL is rewritten. No protected held-out/evaluator leakage is observed.

The future authoritative-publication gap remains: five evidence tags are annotated, while H7 is a lightweight direct-commit tag, and server-side tag namespace protection remains absent. Existing H7 stays untouched; future authoritative evidence should count as policy-conforming only after annotated provenance creation and peeled-target verification.

## Theory / Forge / successor calibration

Theory/canonical separation is healthy. TH-002 was not manufactured into candidate #36 merely to fill an empty queue. Evidence Analyst R128 correctly stops the line after the ordinary matched-access addressable-memory reduction, with zero scientific credit and no automatic successor.

The scientific kill itself is transparent: with pairwise-orthogonal content signatures, the delayed content signature functions as an address; an ordinary matched-access key/value memory reproduces the declared read/revision relations. That is enough to deny promotion. CI failure at lint means runtime/checker-pass wording is not independently validated, but the promotion decision does not require a runtime result because the kill is algebraic.

The methodology defect is narrower: after the first durable dead-end result, the comparator/access correction was made on the same `TH002-FORGE-001` identity. Future Fast Forge must apply the same RESULT_EXPOSED repair taxonomy as canonical development, even when scientific credit is zero.

Fresh SYSTEM→MECHANISM successor rules remain intact; no old terminal object was upgraded or renamed.

## Revisit / resurrection calibration

Terminal and Revisit axes remain orthogonal. No old ID is reopened. TH-002 supplies no Revisit proposal or independent Revisit trigger for Candidate #35, A01, C19, H7 or any terminal object. Candidate #35 remains terminal/deferred with its prior trigger exhausted.

The historical #35 Revisit remains a positive example of new-trigger-only probing followed by a kill without successor. `REVISIT_CANONICALIZE` remains unobserved and therefore `INSUFFICIENT_EVIDENCE`.

Source-isolation risk after HUMAN-009 exposure remains prospective: same-theme findings from an advisory-exposed route cannot alone establish independent Revisit provenance without demonstrable source isolation.

## Funnel / pass reachability / claim type

Canonical mechanism supply remains empty, but that does not justify weaker gates. TH-002 demonstrates live noncanonical question supply and also demonstrates why development repair discipline must remain explicit even at zero credit.

PASS remains realistically reachable under claim-matched prospective standards. R43-style interaction/coalitional burdens should stay limited to broad unique/privileged responsibility claims, not be imposed wholesale on narrow SYSTEM or exploratory claims.

## Gate classifications

- Hard scientific integrity floor: `KEEP`
- Development-phase semantics: `TIGHTEN`
- RESULT_EXPOSED science-affecting revision identity: `TIGHTEN`
- Cycle-3 reassessment, not hard cap: `KEEP`
- Science-invariant vs science-affecting distinction: `TIGHTEN`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY means informative next test, not success: `KEEP`
- FORMAL one-way integrity: `KEEP`
- Raw-before-score / preserve-before-read / exact execution binding: `KEEP`
- Post-FORMAL terminal absorbency: `KEEP`
- Authoritative tag form/provenance: `TIGHTEN`
- Authoritative tag namespace server-side protection: `TIGHTEN`
- External advisory scientific-authority isolation: `KEEP`
- Independent-trigger source/provenance isolation after advisory exposure: `TIGHTEN`
- Theory novelty vs independent-Revisit-trigger semantics: `CLARIFY`
- TH-002 one-fixture static Forge gate design: `KEEP`
- TH-002 Forge execution / repair fidelity: `TIGHTEN`
- Candidate #35 development provenance ref resolution: `CLARIFY`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Revisit Forge new-trigger-only scope: `KEEP`
- Revisit Forge prospective case binding: `KEEP`
- Revisit canonicalization: `INSUFFICIENT_EVIDENCE`
- Revisit bootstrap coverage/conservatism: `KEEP`
- Broad unique/privileged responsibility attribution: `SPLIT_BY_CLAIM_TYPE`
- Surrogate mechanism-discriminator adequacy: `SPLIT_BY_CLAIM_TYPE`
- Theory/canonical separation: `KEEP`
- Forge/canonical separation: `KEEP`
- Protected evaluation validity: `KEEP`
- Claim ceiling enforcement: `KEEP`
- External-science discovery liveness: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without standard relaxation: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **No, one bounded counterexample exists in TH002-FORGE-001 after its first exposed result.**
2. Cycle 3 mistaken for a hard cap? **No.**
3. Science-invariant vs science-affecting changes distinguished? **Not consistently in the TH-002 Forge repair; comparator/access change was science-affecting.**
4. Development observations kept out of independent evidence credit? **Yes. TH-002 remains zero credit.**
5. FORMAL one-way integrity unchanged? **Yes.**
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **No demonstrated case.**
7. PRE_FORMAL genuine development? **Yes.**
8. Terminal semantics calibrated? **Yes. All canonical current objects remain terminal.**
9. Does Revisit catch genuinely changed conditions? **Yes in the historical #35 case; no new trigger exists now.**
10. Does Revisit avoid rescue laundering and zombie inflation? **Yes currently.**
11. Are `REVISIT_FORGE_TEST` probes testing new triggers rather than old failures? **Yes for the observed #35 case. TH-002 is Theory Forge, not Revisit Forge.**
12. Is bootstrap coverage complete and conservative? **Yes, 35/35 and no systematic CLOSED_STRONG defaulting.**
13. Is PASS realistically reachable without weakening evidence standards? **Yes.**

## Risks and recommendations

False-positive/rescue risk remains low at canonical level because the repaired TH-002 probe still receives zero credit and is killed. Moving-goalpost risk is now `LOW_TO_MODERATE` in noncanonical RESULT_EXPOSED development because the same object accepted a post-result comparator/access change. Over-terminalization risk remains low; fresh Theory supply is alive and no legitimate terminal revisit trigger is being suppressed in the current evidence.

Prospectively enforce a small but important rule: after any durable development outcome is exposed, changing comparator semantics, information access, resource/privilege contract, metric, threshold, seed/exclusion policy, intervention, hypothesis, falsifier or success criteria requires an explicit revision/successor identity. Do not rewrite the old outcome. Science-invariant lint/import/build/path/serialization/logging/hash-plumbing corrections may remain on the same object when scientific meaning is unchanged.

Do not rerun or relabel TH002-FORGE-001 solely to repair methodology history. Treat its commit sequence as the calibration example, leave the zero-credit dead-end in place, and apply the revision rule prospectively.

Keep H7 and all existing authoritative refs untouched. Tighten only future authoritative-tag publication/protection through normal governance. Keep advisory-exposed Theory novelty distinct from independent Revisit provenance.

## Utility request

None. No bounded Utility action is needed to establish this calibration finding, and creating one would risk colliding with live governance work.

## Hard-floor confirmation

This audit dispatched no experiment; started no result-bearing workflow; created/consumed no identity; mutated no research/evidence/freeze/formal/sealed/preserve ref; merged no PR; changed no scheduler; reopened no terminal object; reran/retuned/rescored/repaired no consumed FORMAL object; rewrote no historical PASS/FAIL; accessed no protected held-out payload.

Confidence: `HIGH` for the observed TH-002 commit sequence and repair classification; `HIGH` for current canonical/Revisit/FORMAL integrity; `MEDIUM` for future enforcement until the development revision rule is reflected consistently in Forge/Analyst handling.

Questions for Control/Analyst:
- Treat post-outcome comparator or information-access corrections as `SCIENCE_AFFECTING_CHANGE` even in zero-credit Forge, and require an explicit revision/successor identity.
- Preserve the original TH002-FORGE-001 exposed result in history; do not retrospectively relabel it as if the matched-access comparator had been fixed before the first outcome.
- Keep R128's no-canonicalization/no-continuation decision; this finding does not authorize a TH-002 rerun.