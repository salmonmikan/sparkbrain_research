# SparkBrain Methodology Calibration Audit — R103

- schema_version: 2
- generation_id: `METHCAL-20260924T103400+0900-R103-C4F19B72`
- produced_at: `2026-09-24T10:34:00+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260924T091717+0900-R102-8D31C7A4`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE_PREMATURE_FORMAL_EXECUTABILITY_AUTHORITY_ON_SELF_INCONSISTENT_CONTROLLER_BUNDLE`
- overall_classification: `SLIGHTLY_TOO_PERMISSIVE`

## Executive decision

R102 was read first. Current repository/evidence refs were then re-fetched independently, followed by designated Analyst/Control and current MAIN/Theory/Revisit/Forge handoffs. The hard scientific-integrity floor remains intact, no terminal current object was reopened, no development/Theory/Forge/Revisit observation acquired confirmatory credit, and the new H7 launch bridge is still dormant with no identity, START, protected result, score or evidence ref.

A new bounded calibration defect appears in Evidence Analyst R111's H7 execution-readiness gate. R111 correctly observes a newly provisioned workflow-dispatch path and keeps H7 scientific semantics unchanged, but it sets `executor_trigger_capable=true`, `effectively_executable=true` and grants one fresh FORMAL start against controller `bac7402fb01b69353eb926228574cc68c2c2a2d2` before the exact controller bundle is internally self-consistent.

The R111 controller changed only `.github/workflows/h7-formal-r5-one-way-launch.yml` relative to R105. Its current workflow blob is `1c4e2199740397c1afbbcc66e89d83f41fe54b21`, but the unchanged `artifacts/formal_h7_r5/launch_path_contract.json` still requires the older workflow blob `a6fb8fec46ad8b6f6b055e701d5c8cf829d4007c`. The controller's `_assert_launch_contract()` compares the live workflow blob against this frozen expected value, and `prepare_identity()` invokes that assertion before identity/START creation. Therefore the exact R111-authorized result-bearing bundle must fail closed before identity materialization with controller-blob drift. Generic CI success and dormant bridge smoke success do not establish effective FORMAL executability.

This is not a scientific-integrity breach. It is a `SCIENCE_INVARIANT_REPAIR` / execution-readiness validation defect: the operational workflow changed without the exact operational contract binding being updated and revalidated. The correct prospective response is to treat current R111 effective executability and GO_ONCE as not actionable, repair only the operational exact-blob binding with scientific meaning unchanged, perform a non-result contract-faithful validation of the corrected exact bundle, then require a fresh Analyst exact-binding generation before any identity/START. Historical R111 records must not be rewritten.

The authoritative scientific surface is otherwise stable: `main` is `d16403414fc7abebd23075fc401240971b8eb91d`; annotated `evidence/*` remains exactly five tags; H7 `control/h7*`, `preserve/h7*`, and `launch/h7-r5-*` namespaces are empty. H7 science remains `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. The launch request on `ops/h7-r5-launch-bridge` remains `armed=false` with no Analyst generation/commit or nonce populated.

## Input generations and authoritative refs

Prior methodology: R102 (`METHCAL-20260924T091717+0900-R102-8D31C7A4`) at methodology branch head `6de70b363325c058e34efb1aa69e8e4396df6b98`, classified `WELL_CALIBRATED`.

Human directive: `HUMAN-20260922-005` remains process-only, not scientific evidence.

Canonical gate: Analyst R111 (`EVA-20260924T101155+0900-R111-H7-DISPATCH-BOUND-GO-ONCE`) at final durable branch head `2f1409da8d47525cbb1058ce9c7eebf8ef80ef2c`; material change true.

Control: R53 at `8d17debc16e0866b207681553d7045687fafc113`; control-plane mailbox/history only. It independently classified the new dispatch surface as operational and required fresh Analyst revalidation before FORMAL start.

MAIN/Relay: current orchestrator-report tip `230e5348f4e3443e5c4323f149ce7889e8073112`; the latest durable PRIMARY/Relay reports were still waiting for fresh Analyst binding and had not dispatched H7. Their timestamps precede final R111 persistence, so this is not a stale-consumer defect.

Theory/Literature/Revisit mailbox: `eaab2a8fd08921aa91782825644a5f7e28df0173`. Theory R2 is `THEORY-20260924T093014+0900-R2-NO-PROPOSAL-5D7C1A94`, zero-credit/noncanonical with `NO_REVISIT_PROPOSAL`.

Stable main: `d16403414fc7abebd23075fc401240971b8eb91d`. Its H7 workflow is registration-only and always fails closed; result-bearing execution lives only on the Analyst-bound controller ref.

H7 science: `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

R111 result-bearing controller: `bac7402fb01b69353eb926228574cc68c2c2a2d2`.

R111 result-bearing workflow blob: `1c4e2199740397c1afbbcc66e89d83f41fe54b21`.

Launch contract expected workflow blob: `a6fb8fec46ad8b6f6b055e701d5c8cf829d4007c`.

Launch bridge: `ops/h7-r5-launch-bridge`; current request remains dormant (`armed=false`).

Independent repository reconstruction: five annotated `evidence/*` tags, H7 control/preserve/launch namespaces empty, no H7 identity/START/protected result/PASS-FAIL/evidence ref.

## Development iteration calibration

Development-phase semantics remain calibrated on the scientific objects. H7 stays `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`; the new dispatch implementation changes no metric, scorer meaning, threshold/tolerance, comparator, seed/exclusion policy, intervention, resource/privilege contract, hypothesis, falsifier or success criteria.

The R111 workflow-dispatch delta is therefore properly classifiable as science-invariant operational plumbing. However, science-invariant does not mean readiness checks may be skipped. Exact operational binding is part of the one-way integrity package. The current defect is that the workflow implementation changed while the exact launch contract still binds the old workflow blob.

Candidate #34 and #35 remain terminal for their current objects. Neither returns to ACTIVE, and there is no same-object SYSTEM-to-MECHANISM upgrade.

Cycle 3 remains a mandatory reassessment point, not an automatic terminal cap. No new hard-cap behavior is observed.

Development, Theory, Forge and Revisit observations remain outside independent confirmatory evidence credit.

## PRE_FORMAL / FORMAL calibration

PRE_FORMAL remains genuine development. H7 can be scientifically READY/QUEUED without already succeeding, and scientific readiness remains orthogonal to implementation readiness.

The prior R102 distinction between scientific readiness and operational executability remains correct. R111 crossed that boundary one step too early: the dispatch primitive exists, but the exact authorized controller bundle cannot satisfy its own preidentity launch-contract assertion. Hence `effectively_executable=true` is not currently justified.

FORMAL one-way integrity itself remains unchanged and fail-closed. No H7 identity, START, protected-evaluation access, target-blind raw, preserve ref, score, PASS/FAIL or evidence ref exists. The bridge remains unarmed. If the current R111 controller were dispatched, `_assert_launch_contract()` / `prepare_identity()` should fail before identity creation because the live workflow blob does not equal the launch contract's expected blob.

The required prospective sequence is now:
1. keep R5 science/runtime/input/scorer/preserver/comparator/metric/threshold/intervention semantics unchanged;
2. repair only the exact operational launch-contract binding so it identifies the already-reviewed result-bearing workflow implementation;
3. run a non-result validation that exercises the same exact-contract assertion against the corrected bundle without persisting a FORMAL identity or accessing protected targets;
4. obtain a fresh Analyst generation binding the corrected exact controller head and proving generation-ID/commit consistency;
5. only then permit at most one fresh FORMAL identity/START.

The live fresh one-way FORMAL transition remains unobserved, so end-to-end execution remains `INSUFFICIENT_EVIDENCE`. PASS remains scientifically reachable without weakening evidence standards, but the current R111 exact bundle is operationally not reachable until the bounded science-invariant repair and fresh revalidation occur.

## Theory / Forge calibration

Theory/canonical separation remains calibrated. Theory R2 correctly emits no new proposal and no Revisit proposal. TH-001 remains rejected for its current proposal after its prospectively specified Q0-vs-QI discriminator was reduced by ordinary residual adaptation/threshold plus fixed edge/delay. Literature-derived anti-vacuity/intervention-faithfulness constraints remain prospective guardrails, not post-outcome repair.

Fast Forge remains zero-credit and noncanonical. No new H7-derived code or outcome is reused, no new positive-search retuning is authorized, and no candidate is manufactured to fill throughput.

## Revisit / resurrection calibration

Revisit remains orthogonal to terminal state. All 34 terminal current objects remain terminal. Bootstrap remains complete and conservative: 1 `CLOSED_STRONG`, 19 `DORMANT_REVISITABLE`, 14 `DEFERRED_INDEPENDENT_REIDENTIFICATION`, 0 `REVISIT_TRIGGERED`.

The H7 dispatch capability is specific to a current nonterminal object and is not an independent trigger for a terminal object. Theory R2 supplies no candidate-specific trigger. No `REVISIT_FORGE_TEST`, no `REVISIT_CANONICALIZE`, no fresh successor, no old-ID reopening and no historical result rewrite are observed.

No valuable old line is concretely observed being missed, and no weak old line is being revived by renaming or immediate-successor rescue. End-to-end live Revisit trigger sensitivity remains untested rather than failed.

## Funnel / claim type / candidate supply / pass reachability

Canonical population remains 35 = 14 MECHANISM / 21 SYSTEM; 34 terminal, H7 sole nonterminal. Scientific queue remains one H7 object. Mechanism supply remains fragile.

R111's reported `operationally_triggerable=1` is defensible at the bridge/dispatch-primitive level, but `effectively_executable_mechanism=1` is too permissive because the exact result-bearing bundle fails its own preidentity contract binding. Effective executability should be counted as zero until the corrected exact bundle passes contract-faithful non-result validation and a fresh Analyst rebinds it.

Claim ceilings remain enforced. No same-object post-outcome SYSTEM-to-MECHANISM uplift is observed.

PASS remains scientifically reachable without weakening evidence standards after a science-invariant exact-binding repair and fresh Analyst revalidation. No evidence standard needs relaxation to restore reachability.

## Gate classifications

- Hard integrity floor: `KEEP`
- Development-phase monotonicity: `KEEP`
- Terminal current object never reactivated: `KEEP`
- Cycle-3 mandatory reassessment: `KEEP`
- Cycle-3 automatic hard cap: `RELAX`
- Science-invariant vs science-affecting separation: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL as genuine development: `KEEP`
- Hidden second FORMAL gate: `KEEP`
- Scientific readiness / queue orthogonal to executor capability: `KEEP`
- Dispatch primitive availability as a distinct operational dimension: `KEEP`
- Effective executability requires exact self-consistent validated bundle: `TIGHTEN`
- FORMAL authority against an exact self-consistent controller bundle: `TIGHTEN`
- Launch-contract / result-bearing-workflow exact-blob consistency: `TIGHTEN`
- Consumer Analyst generation-ID / exact-commit pair validation: `KEEP`
- Fresh FORMAL one-way transition: `INSUFFICIENT_EVIDENCE`
- Revisit axis orthogonal to terminal state: `KEEP`
- Revisit bootstrap coverage: `KEEP`
- Revisit bootstrap conservatism: `KEEP`
- Revisit historical specificity / trigger provenance: `CLARIFY`
- Revisit independent-trigger detection end-to-end: `INSUFFICIENT_EVIDENCE`
- Revisit rescue-laundering prevention: `KEEP`
- Revisit fresh-candidate / zero inherited credit: `KEEP`
- REVISIT_FORGE_TEST new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- REVISIT_CANONICALIZE full gate: `INSUFFICIENT_EVIDENCE`
- Theory/canonical separation: `KEEP`
- Theory Forge zero-credit bounded surface: `KEEP`
- Theory rejection after contract-faithful ordinary reduction: `KEEP`
- Fast Forge/canonical separation: `KEEP`
- Claim ceiling enforcement: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development phases consistent end-to-end? **Yes on current scientific objects.** The R111 defect is operational exact-binding/readiness, not development-phase manipulation.
2. Cycle 3 mistaken for a hard cap? **No.**
3. Science-invariant vs science-affecting changes distinguished? **Substantively yes.** R111 workflow dispatch is science-invariant, but its exact operational contract binding is incomplete.
4. Development observations kept out of independent evidence credit? **Yes.**
5. FORMAL one-way integrity unchanged? **Yes.** No H7 identity/START/protected result/evidence exists, and the current mismatch fails closed before identity.
6. Legitimate fresh SYSTEM-to-MECHANISM successors suppressed or manufactured? **No current concrete example.**
7. PRE_FORMAL genuine development? **Yes.** READY does not mean success and must not imply effective executability.
8. Terminal semantics calibrated? **Yes.** All 34 terminal IDs remain terminal.
9. Revisit catches genuinely changed conditions? **Not demonstrated live; no current candidate-specific independent trigger is missed.**
10. Revisit avoids rescue laundering and zombie inflation? **Yes in current observations.**
11. REVISIT_FORGE_TEST tests new trigger rather than old failure? **Insufficient evidence; no live case exists.**
12. Bootstrap complete and conservative? **Yes**, with candidate-specific closure provenance required before a live trigger.
13. PASS realistically reachable without weaker standards? **Yes scientifically, but not through the currently authorized R111 exact bundle until its science-invariant exact-binding defect is repaired and freshly revalidated.**

## Risks

False-positive rescue laundering / zombie inflation: `LOW_CURRENT_MODERATE_FUTURE_TRIGGER_WATCH`.

False-negative forgotten valuable lines: `LOW_CURRENT_MODERATE_UNTESTED_REVISIT_PATH`.

Moving-goalpost / rescue: `LOW_CURRENT`.

Over-terminalization: `LOW_CURRENT_NO_CONCRETE_MISSED_TRIGGER_OR_SUCCESSOR`.

FORMAL evidence contamination: `LOW_CURRENT_FAIL_CLOSED_BEFORE_IDENTITY`.

FORMAL execution-readiness false positive: `MODERATE_CURRENT_BOUNDED_PREIDENTITY`; R111 grants GO_ONCE/effective executability before the exact bundle can satisfy its own launch contract.

Provenance observability: `IMPROVED_CURRENT_PAIR_VALIDATION`; the R102 generation-ID/commit exactness rule is now enforced by bridge/controller checks.

Mechanism supply: `FRAGILE_ONE_SCIENTIFICALLY_QUEUED_ZERO_CURRENTLY_EFFECTIVELY_EXECUTABLE_AFTER_INDEPENDENT_CONTRACT_CHECK`.

## Prospective recommendations

1. Do not act on the current R111 GO_ONCE as an executable FORMAL authorization while the result-bearing workflow blob and launch-contract expected blob disagree.
2. Keep H7 R5 scientific source/runtime/input/scorer/preserver/comparator/metric/threshold/intervention semantics unchanged.
3. Prospectively update only the operational exact workflow-blob binding in the launch contract/controller bundle, preserving the old R111 record and all prior results.
4. Before any identity/START, run a non-result contract-faithful validation that reaches the same `_assert_launch_contract()` checks and proves the corrected exact controller/workflow/contract bundle is self-consistent; generic CI alone is insufficient.
5. Require a fresh Analyst generation after that exact validated repair; bind the final Analyst generation ID to its exact final commit and the corrected exact controller/science pair before arming the bridge.
6. Keep the bridge create-once/nonce/no-duplicate and one-way identity/START/raw-preserve-before-target/score-after-preserve semantics unchanged.
7. Keep TH-001 rejected for its current proposal, keep all terminal IDs terminal, and require independent candidate-specific Revisit triggers for any fresh successor.
8. Do not weaken evidence standards or claim ceilings to compensate for fragile mechanism supply.

Utility request: none. The defect is directly demonstrated by the current controller/contract artifacts and needs no methodology experiment.

## Hard-floor confirmation

No consumed FORMAL identity was rerun, retuned or rescored; no terminal current object was reactivated; no frozen scientific protocol or historical PASS/FAIL was rewritten; no evaluator/held-out leakage is observed; no silent post-FORMAL repair occurred; no H7 identity/START exists; no protected target was accessed; no scientific/evidence ref was mutated by this audit. Persistence is limited to the designated methodology audit latest/state/history paths.

Confidence: `HIGH` for the R111 exact workflow/launch-contract mismatch and its preidentity fail-closed consequence; `HIGH` for current H7/terminal/Theory integrity; `MODERATE` for live Revisit behavior because no actual `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE` has occurred.

Questions for Control/Analyst: no user-blocking scientific question. Prospectively, treat effective executability as false until the corrected exact bundle passes the same launch-contract assertion used by `prepare_identity`, then issue a fresh Analyst exact-binding generation before any bridge arming. At the first real Revisit trigger, continue to record the candidate-specific historical closure premise changed by the independent trigger before any Forge referral.
