# SparkBrain Methodology Calibration Audit — R118

- schema_version: `2`
- generation_id: `METHCAL-20260925T001948+0900-R118-D42E7B19`
- generated_at: `2026-09-25T00:19:48+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T232004+0900-R117-7E4B2C19`
- overall_classification: `SLIGHTLY_TOO_PERMISSIVE`
- material_change: `true`
- material_change_scope: `R117_REVISION_GUARD_ADOPTED_BY_ANALYST_CONTROL_AND_HONORED_BY_FORGE_WHILE_INDEPENDENT_AUDIT_DURABILITY_GAP_RAISES_DISCOVERY_FALSE_NEGATIVE_RISK`
- new_scientific_result: `false`
- history_create_commit: `8c72d3f93ccf9ae9d870ca1b07fbf3634d9192ac`

## Executive calibration

R117 methodology history/state was read first. Stable repository/evidence were independently re-fetched before current Control/Analyst/Theory/Forge mailboxes were used as control-plane context. `ops/*` remains mailbox/history context, not scientific source of truth.

Stable `main` remains `d16403414fc7abebd23075fc401240971b8eb91d`. The authoritative `evidence/*` namespace remains six refs: five annotated tag objects and H7 as a lightweight direct-commit tag. Repository rulesets still contain one active branch ruleset and no server-side tag-target protection. The repository policy still requires future authoritative identities to be provenance-bearing annotated tags with peeled-target verification and forbids replacement. Existing H7 refs remain historical and must not be rewritten.

The main methodology delta is positive: Evidence Analyst R129, Control R64 and Fast Forge R33 all explicitly adopt R117's prospective rule that, after a durable development result is exposed, comparator semantics, information/resource privilege, metric, threshold, seed/exclusion policy, intervention, hypothesis, falsifier or success criterion changes require an explicit versioned revision or fresh successor identity while preserving the prior outcome. Fast Forge R33 then declines any TH-002 replay or relabel solely to clean methodology history. This materially closes the observed TH002-FORGE-001 moving-goalpost pathway at the current control-plane gate level.

The historical TH-002 defect remains a calibration example and is not rewritten: one same-object science-affecting comparator/access repair occurred after result exposure, but both outcomes remain in Git history, scientific credit remains zero, and there is no FORMAL breach or rerun authority.

A separate negative delta is discovery liveness. Control R64 and Analyst R129 both report that the 22:30 Independent Auditor output did not become durable and the external-science branch remains at Theory R4, following an earlier delayed/missed external slot. This does not identify a specific missed Revisit trigger, and no scientific criterion should be relaxed. It does, however, raise false-negative / over-terminalization risk because one of the programme's independent trigger-discovery routes is not reliably producing durable outputs.

Overall remains `SLIGHTLY_TOO_PERMISSIVE`, not because current canonical/Revisit/FORMAL gates are weak, but because authoritative evidence immutability/publication remains partly convention-enforced rather than server-protected, while the newly adopted RESULT_EXPOSED revision rule has not yet been exercised on a fresh science-affecting repair. The independent-audit durability gap is tracked as an orthogonal discovery-liveness risk rather than evidence for relaxing terminal criteria.

## Current authoritative reconstruction

- Previous methodology: `METHCAL-20260924T232004+0900-R117-7E4B2C19`; methodology branch head before R118 persistence `8b88ef3ad173188a5219bfffeb8530901d36b678`.
- Stable main: `d16403414fc7abebd23075fc401240971b8eb91d`.
- Evidence namespace: 6 refs; 5 annotated tag objects; H7 `evidence/h7-r5-h7-r5-285a3a206b34c5982b9d4045` remains a lightweight direct-commit tag to `e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`.
- Repository rulesets: one active branch ruleset; no tag-target namespace protection observed.
- Evidence Analyst: `EVA-20260925T000135+0900-R129-METH117-CONTROL64-SCHEDULER-DURABILITY-NO-SCIENCE`; branch head `dd0a26b51f77ceafd333bab8a03c21100571c078`.
- Control: `CTRL-20260924T235000+0900-R64-TH002-KILL-METH117-SCHEDULER-DEGRADATION`; branch head `a92e0eaae0260152e311c1c5a4ca0294daf571a5`.
- Theory: `THEORY-20260924T213041+0900-R4-ANONYMOUS-LINEAGE-ADDRESSABILITY-6B2D9F41`; external-science branch head remains `87d206a3f62c70c393531413445703fd0baa108a` and no newer Independent Audit is durable.
- Fast Forge: `FORGE-20260924T233401+0900-R128-R117-NOOP`; it adopts the R117 revision identity guard and creates no new probe, prototype, candidate or promotion.
- H7 workflow `35951118916` remains completed `success`, attempt `1`, with exact controller head `af3aa97574c365e3e918c3d4d012faa4886760d0`.
- H7 remains `FORMAL / MECHANISM / CONSUMED_ONE_WAY / INCONCLUSIVE / TERMINAL_FOR_CURRENT_OBJECT`; no rerun/retune/rescore/repair/same-object successor.
- Canonical census remains `35 = 14 MECHANISM / 21 SYSTEM`, all terminal; active 0; scientifically queued 0; executable canonical MECHANISM 0.
- Development census remains `OPEN_DEVELOPMENT 0 / RESULT_EXPOSED_DEVELOPMENT 34 / CONSUMED_ONE_WAY 1`.
- Revisit ledger remains complete 35/35: `CLOSED_STRONG=1`, `DORMANT_REVISITABLE=20`, `DEFERRED_INDEPENDENT_REIDENTIFICATION=14`, `REVISIT_TRIGGERED=0`.
- Candidate #35 remains terminal SYSTEM, zero confirmatory credit, exhausted historical Revisit trigger, no successor.
- TH-002 remains noncanonical, zero credit, `FORGE_KILLED_NO_CANONICALIZATION`, with no candidate #36 and no Revisit trigger.

## Development / repair calibration

The current prospective semantics are materially improved. Analyst R129 adopts the explicit three-state repair rule across development lanes. Control R64 repeats the same rule, and Fast Forge R33 operationally honors it by refusing to rerun/relabel TH002-FORGE-001 solely to repair methodology history.

Accordingly, the current gate for `OPEN_DEVELOPMENT / RESULT_EXPOSED_DEVELOPMENT / CONSUMED_ONE_WAY` is now calibrated in specification and current lane behavior. The TH-002 same-object comparator/access change remains a historical counterexample, not a current authorization. Because no fresh result-exposed science-affecting repair has yet exercised the newly adopted rule, enforcement confidence remains `MEDIUM`, not `HIGH`.

Gate action: `KEEP` for the current three-state semantics and science-invariant/science-affecting taxonomy, with `TIGHTEN` retained specifically for enforcement/documentation of revision identity until a fresh case demonstrates compliant handling. Cycle 3 remains reassessment rather than a hard cap.

## PRE_FORMAL calibration

PRE_FORMAL remains genuine development. Repeated development observations remain zero confirmatory credit. READY remains an informative next test rather than prior success. No hidden second FORMAL gate is observed. TH-002 never entered PRE_FORMAL or canonical candidate state.

## FORMAL / hard-floor calibration

The one-way hard floor remains intact. H7 is still consumed/terminal/inconclusive, and workflow run `35951118916` remains attempt 1 only. No historical PASS/FAIL is rewritten. No protected held-out/evaluator leakage is observed.

The future authoritative-publication gap persists: five evidence tags are annotated while H7 is a lightweight direct-commit tag, and server-side tag namespace protection remains absent. Existing H7 stays untouched. Future authoritative evidence should count as policy-conforming only after annotated provenance creation and peeled-target verification, and server-side namespace protection remains desirable through normal governance.

## Theory / Forge / successor calibration

Theory/canonical separation remains healthy. TH-002 was not manufactured into candidate #36 merely because the canonical queue is empty. Its ordinary matched-access addressable-memory reduction remains sufficient for no promotion, and R129/R64/R33 all reject continuation or methodology-only replay.

The newly adopted result-exposed revision rule is now present in Analyst, Control and Forge handling. This resolves the immediate same-object rescue pathway prospectively, though no fresh compliant repair case has yet stress-tested the rule.

Fresh SYSTEM→MECHANISM successor rules remain intact. No old terminal object was upgraded or renamed. A fresh successor remains legitimate only with a new ID, independently motivated question, new reduction/comparator/falsifier contract and fresh development state.

## Revisit / resurrection calibration

Terminal and Revisit axes remain orthogonal. No old ID is reopened. Candidate #35 remains terminal/deferred with its previous trigger exhausted. TH-002 supplies no Revisit proposal or independent trigger for #35, A01, C19, H7 or any terminal object.

The historical #35 case remains a good example of a genuinely new trigger being probed cheaply and then killed without successor. `REVISIT_CANONICALIZE` remains unobserved and therefore `INSUFFICIENT_EVIDENCE`.

Bootstrap remains complete and conservative: all 35 terminal objects are classified, only 1 is `CLOSED_STRONG`, and there is no systematic closure default that suppresses future discovery.

The false-negative concern is now operational discovery liveness, not terminal semantics: the 22:30 Independent Auditor output is missing/delayed and the external-science branch has not advanced beyond Theory R4. No specific valuable old line is shown to have been missed, but trigger-discovery coverage is temporarily weaker. This should not be compensated by reopening old candidates or lowering Revisit standards.

## Funnel / pass reachability / claim type

Canonical mechanism supply remains empty, but this does not justify weaker gates. PASS remains realistically reachable under claim-matched prospective standards. Broad unique/privileged responsibility claims should retain interaction/coalitional and capacity-adequate comparator burdens; narrow SYSTEM or exploratory claims should not inherit that entire burden.

The absent Independent Audit output modestly increases mechanism-supply and Revisit false-negative risk because one external discovery lane is not durable, but it is not evidence that any existing terminal candidate should be revived.

## Gate classifications

- Hard scientific integrity floor: `KEEP`
- Development-phase semantics: `KEEP`
- RESULT_EXPOSED science-affecting revision identity enforcement: `TIGHTEN`
- Cycle-3 reassessment, not hard cap: `KEEP`
- Science-invariant vs science-affecting distinction: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY means informative next test, not success: `KEEP`
- FORMAL one-way integrity: `KEEP`
- Raw-before-score / preserve-before-read / exact execution binding: `KEEP`
- Post-FORMAL terminal absorbency: `KEEP`
- Authoritative tag form/provenance: `TIGHTEN`
- Authoritative tag namespace server-side protection: `TIGHTEN`
- External advisory scientific-authority isolation: `KEEP`
- Independent-trigger source/provenance isolation after advisory exposure: `KEEP`
- Theory novelty vs independent-Revisit-trigger semantics: `CLARIFY`
- TH-002 one-fixture static Forge gate design: `KEEP`
- TH-002 historical repair classification: `KEEP`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Terminal/Revisit orthogonality: `KEEP`
- Revisit trigger detection semantics: `KEEP`
- Revisit discovery-lane durability: `TIGHTEN`
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
- External-science discovery liveness: `TIGHTEN`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without standard relaxation: `KEEP`

## Mandatory questions

1. Development-phase semantics consistent end-to-end? **Prospectively yes in current Analyst/Control/Forge handling; the historical TH-002 counterexample remains preserved and the new rule has not yet been stress-tested by a fresh science-affecting repair.**
2. Cycle 3 mistaken for a hard cap? **No.**
3. Science-invariant vs science-affecting changes distinguished? **Yes in current policy/handoffs; TH-002 remains the historical misclassification example.**
4. Development observations kept out of independent evidence credit? **Yes. TH-002 remains zero credit.**
5. FORMAL one-way integrity unchanged? **Yes.**
6. Legitimate fresh SYSTEM→MECHANISM successors suppressed or manufactured? **No demonstrated case.**
7. PRE_FORMAL genuine development? **Yes.**
8. Terminal semantics calibrated? **Yes. All 35 canonical current objects remain terminal.**
9. Does Revisit catch genuinely changed conditions? **Historically yes for #35; current discovery coverage is degraded by a missing Independent Auditor output, but no concrete missed trigger is identified.**
10. Does Revisit avoid rescue laundering and zombie inflation? **Yes currently.**
11. Are `REVISIT_FORGE_TEST` probes testing new triggers rather than old failures? **Yes for the observed #35 case. TH-002 is Theory Forge, not Revisit Forge.**
12. Is bootstrap coverage complete and conservative? **Yes, 35/35 with distribution 1/20/14/0 and no CLOSED_STRONG defaulting.**
13. Is PASS realistically reachable without weakening evidence standards? **Yes.**

## Risks and recommendations

Canonical false-positive/rescue risk remains low. The prior noncanonical moving-goalpost risk has decreased because R117's revision guard is now adopted by Analyst, Control and Forge. It is still prudent to require explicit revision identity enforcement on the next fresh result-exposed science-affecting change before considering that risk fully retired.

Over-terminalization / false-negative risk rises from low to `LOW_TO_MODERATE_OPERATIONAL` because the Independent Auditor durability gap weakens one trigger-discovery route. This is not a reason to change terminal semantics. Fix discovery durability through normal operational governance; do not compensate by granting old candidates extra credit or reopening them.

Keep all consumed/frozen/terminal historical objects unchanged. Keep H7 and all existing evidence refs untouched. Tighten only future authoritative publication/protection. Preserve advisory-exposure provenance and continue requiring genuinely independent information before a same-theme Revisit trigger can fire.

## Utility request

None. A Utility action is not needed to establish the methodology finding, and scheduler/load changes belong to normal Control/user governance rather than this read-only methodology audit.

## Hard-floor confirmation

This audit dispatched no experiment; started no result-bearing workflow; created/consumed no identity; mutated no research/evidence/freeze/formal/sealed/preserve ref; merged no PR; changed no scheduler; reopened no terminal object; reran/retuned/rescored/repaired no consumed FORMAL object; rewrote no historical PASS/FAIL; accessed no protected held-out payload. Persistence is confined to the designated append-only methodology audit history plus its latest/state mailbox.

Confidence: `HIGH` for current canonical/Revisit/FORMAL integrity and the R117 guard adoption; `HIGH` for the observed evidence-tag/ruleset state; `MEDIUM` for future revision-identity enforcement until a fresh repair case exercises it; `HIGH` that the Independent Auditor durability gap is real at this snapshot, but only `MEDIUM` that it has caused any missed scientific trigger because none is presently identified.

Questions for Control/Analyst:
- Keep the R117 revision guard active across all development lanes and require an explicit revision/successor identity on the next result-exposed science-affecting change.
- Treat the missing Independent Auditor durability as a discovery-liveness problem only; do not relax Revisit or terminal criteria to compensate.
- Continue requiring source-isolated, genuinely new information for same-theme Revisit triggers after advisory exposure.
- Keep H7 and all existing authoritative refs unchanged; apply publication/protection tightening only prospectively.