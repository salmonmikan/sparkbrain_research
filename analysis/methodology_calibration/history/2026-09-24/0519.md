# SparkBrain Methodology Calibration Audit — R98

- schema_version: 2
- generation_id: `METHCAL-20260924T051916+0900-R98-7D3B4C91`
- produced_at: `2026-09-24T05:19:16+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260924T042120+0900-R97-C9CE09C7`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

R97 was read first. Two material calibration observations occurred after it.

First, R97's prospective H7 recommendation was partly implemented correctly. Under R105, the exact result-bearing one-way controller, protected-payload handoff, fresh-identity mechanics, create-only START, raw-before-score, preserve-before-read, frozen scorer/runtime/preserver bindings, and create-only formal/sealed/evidence path were materialized without creating an identity or scientific result. The exact controller head `042d00375278d551dbf643ad866a4c883852804d` and frozen science head `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80` remain unchanged; the launch-plumbing readiness run is green. Fresh Analyst R106 then restored exactly one conditional FORMAL authority.

However, the first post-R106 PRIMARY attempt exposed a second execution-readiness gap before identity/START: the frozen workflow can only be triggered by a fresh `launch/h7-r5-*` tag, while the authorized automation execution surface exposes neither tag creation nor workflow dispatch. MAIN correctly failed closed rather than alter the frozen trigger. No identity, START, protected evaluation read, raw result, score, preserve ref, or evidence mutation occurred. This is not a scientific-integrity incident, but R106's `QUEUED` / `effectively executable` classification was operationally too strong. Prospectively, scientific FORMAL authority and executor capability should be represented separately: exact scientific/integrity authority may remain valid, but `effectively_executable` should require a verified trigger capability available to the authorized executor. PASS is scientifically reachable without weaker standards, but is not currently autonomously executable by the observed lane.

Second, the first Analyst-gated TH-001 Forge probe executed on an exposed synthetic nonrescue surface and remained noncanonical/zero-credit. The probe itself is bounded and safe. But the original TH-001 proposal predeclared a minimal discriminator that constructs an ordinary predictive partition `Q0`, applies a frozen intervention family, and asks whether the intervention-stable quotient `QI` must split predictive-equivalent histories. The executed recurrent-continuation probe instead compares an explicit recurrent loop against a cut and does not construct predictive-equivalent `Q0` pairs or an actual `Q0`-vs-`QI` refinement test. It validly shows that this toy continuation is explained by ordinary recurrence, but it does not by itself falsify the predeclared TH-001 discriminator. R106's use of this probe as a Theory kill with no further burden absent new information is therefore slightly over-conservative. Completing the already-predeclared Q0-vs-QI discriminator would not be outcome-responsive rescue tuning; it would be contract-faithful testing of the original theory question. No canonical candidate or evidence was created, so this is a throughput/false-negative calibration issue, not an integrity breach.

Revisit remains conservative and unchanged: all 34 terminal current objects remain terminal, the ledger remains 1 `CLOSED_STRONG` / 19 `DORMANT_REVISITABLE` / 14 `DEFERRED_INDEPENDENT_REIDENTIFICATION` / 0 `REVISIT_TRIGGERED`, no old ID is reopened, and no historical outcome is rewritten. No live `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE` exists, so end-to-end changed-condition sensitivity remains unobserved.

Independent repository checks confirm stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; H7 frozen science and launch-controller refs are exact; authoritative `evidence/*` remains exactly five tags; tag-form `formal/*` and `sealed/*` are empty in the checked namespaces; H7 `control/h7*` and `preserve/h7*` heads are absent. The fixed H7 workflow is tag-triggered and explicitly re-fetches fresh Analyst authority before identity/START.

## Authority reconstruction

Prior methodology history: R97 classified the programme `MIXED_CALIBRATION`, tightened FORMAL authority sequencing so the materialized result-bearing launch path must pre-exist authority, kept Revisit bootstrap conservative, and left live Theory/Forge and Revisit execution as evidence gaps.

Designated Control history: Control R48 (`CTRL-20260924T045900+0900-R48-6F2C1A84`) records that the R105-authorized H7 launch plumbing is materialized and green, while R105 still required a fresh Analyst. It also observes Theory R1 awaiting/entering its bounded Forge stage. Control predates R106 and the later PRIMARY trigger-capability block.

Designated canonical gate: Analyst R106 (`EVA-20260924T050035+0900-R106-H7-LAUNCH-READY-THEORY-PROBE-KILLED`) independently re-fetched the exact H7 science/controller bindings and green non-result validation, restored one conditional one-way FORMAL authority, and kept identity uncreated/unconsumed. It also evaluated the first TH-001 Forge probe as an ordinary-recurrence reduction and a Theory kill.

Fresh MAIN: `MAIN-20260924T051305+0900-PRIMARY-H7-R106-FORMAL-LAUNCH-TRIGGER-BLOCKED` re-fetched R106, the exact source/controller/component bindings, and all H7 one-way namespaces. It stopped before identity because the runtime cannot create the prospectively required launch tag or dispatch the workflow, and changing the trigger would violate exact binding.

Theory/Forge: TH-001 remains noncanonical and zero-credit. The Forge branch `forge/20260924-recurrent-continuation-a@17b2673cd0417fdf931264a71d8df1f9c1c21f23` contains only an exposed synthetic recurrent-loop/cut probe. Its final lint repair is science-invariant. It does not touch H7 or Candidate #34/#35 rescue surfaces.

## Development iteration calibration

Development-phase semantics remain consistent. H7 remains `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`; materializing and validating the launch path did not reset it to OPEN. Candidate #35 remains result-exposed and terminal. No same-object science-affecting change is authorized after exposure.

Cycle 3 remains a mandatory reassessment point, not an automatic terminal cap. No current transition is driven solely by cycle count.

Science-invariant versus science-affecting repair remains correctly distinguished on H7. The new controller/workflow work binds execution, preservation, serialization, identity/no-clobber, runtime and hash plumbing without changing the frozen scientific source/protocol/scorer semantics. Any change to metric, threshold, comparator, intervention, seed/exclusion policy, resource/privilege contract, hypothesis, falsifier, or success criteria still requires a versioned revision or fresh successor.

Development observations remain outside independent confirmatory credit. TH-001 and its Forge probe are explicitly non-evidentiary; Candidate #34/#35 development observations remain zero/nonconfirmatory credit.

## PRE_FORMAL / FORMAL calibration

PRE_FORMAL remains genuine development. H7 can remain scientifically READY even when operationally not startable. The new trigger-capability block demonstrates that scientific readiness, integrity authorization, and executor capability are three separable axes and should not be collapsed into a single `effectively_executable` flag.

FORMAL one-way integrity is unchanged. The exact workflow is prospectively tag-triggered, re-fetches fresh Analyst state, checks unused one-way namespaces, reconstructs the locked runtime, creates a fresh identity/START once, produces target-blind raw, remotely preserves/freezes raw before target materialization, then scores and creates evidence refs without clobber. No H7 one-way transition has actually begun.

R97's `result-bearing launch path before FORMAL authority` tightening is now satisfied at the repository level. The remaining calibration issue is execution capability: a fresh authority should not imply `QUEUED/effectively executable` unless the authorized actor can invoke the frozen trigger without modifying it. Gate classification: `KEEP` for scientific/integrity authority binding; `TIGHTEN` for effective-executability labeling and prestart trigger-capability validation.

## Theory / Forge calibration

Theory/canonical separation remains `KEEP`. TH-001 created no candidate, evidence, or execution authority. The first Forge probe ran on an exposed synthetic surface and is zero-credit, with no H7 or terminal-rescue overlap.

Probe discipline is mixed. The actual toy correctly demonstrates that an explicit recurrent edge can explain continuation, so that prototype should be reduced/killed. But the predeclared TH-001 minimal discriminator was Q0 predictive-equivalence versus QI intervention-conditioned refinement. The executed test never instantiates that discriminator. Therefore `FORGE_KILL_ORDINARY_RECURRENCE` is justified for the prototype but not as a full Theory falsification. Prospectively, a Theory-level kill should require either the predeclared discriminator itself to fail or an ordinary reduction that logically subsumes it. Otherwise record a prototype reduction and leave the original bounded discriminator eligible without demanding genuinely new information.

This is an over-conservative false-negative risk, not rescue laundering. Running the already-specified Q0-vs-QI probe would not be a post-outcome change to the theory's metric/falsifier; it was frozen before the recurrent toy outcome.

## Revisit / resurrection calibration

The revisit axis remains orthogonal to terminal state. All 34 terminal objects remain terminal and no historical PASS/FAIL is rewritten.

Bootstrap coverage remains complete and conservative. The residual need is unchanged: broad class-level `what_would_change_our_mind` templates are discovery scaffolding, not sufficient trigger proof; a first live trigger must recover candidate-specific closure provenance or require independent re-identification.

No genuine independent Revisit trigger has traversed the system. The TH-001 Forge result is an ordinary recurrence reduction, not a candidate-specific material trigger that changes an old closure. Therefore leaving all ledger rows unchanged is calibrated.

Current rescue/zombie control remains strong. Candidate #35's immediate post-outcome successor family remains deferred and zero-credit. There is no fresh-ID laundering.

There is still no live `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE`, so whether Revisit Forge tests the new trigger rather than rerunning an old failure remains `INSUFFICIENT_EVIDENCE`.

## Funnel / mechanism supply / pass reachability

Claim ceilings remain enforced; no same-object SYSTEM->MECHANISM uplift is observed. Mechanism supply remains fragile: H7 is the only nonterminal MECHANISM object, and although Analyst R106 labels it queued/executable, the observed autonomous lane cannot invoke the frozen launch trigger. Effective autonomous MECHANISM execution count is therefore zero at this audit cutoff.

PASS remains scientifically reachable without weakening evidence standards, because no scientific criterion needs to change. Operationally it is not currently reachable by the observed executor until a permitted tag-creation/workflow-dispatch capability exists. The correct response is capability alignment or a correctly authorized trigger actor, not scientific relaxation or workflow-trigger mutation after R106 binding.

Theory supply is also slightly over-conservatively constrained by treating an off-discriminator prototype reduction as a whole-theory kill. This should be corrected prospectively without granting the theory evidence credit or canonical status.

## Gate classifications

- Hard integrity floor: `KEEP`
- Development-phase monotonicity: `KEEP`
- Cycle-3 mandatory reassessment: `KEEP`
- Cycle-3 automatic hard cap: `RELAX`
- Science-invariant vs science-affecting separation: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL as genuine development: `KEEP`
- Hidden second FORMAL gate: `KEEP`
- Materialized result-bearing launch path before fresh FORMAL authority: `KEEP`
- Scientific FORMAL authority exact binding: `KEEP`
- Effective-executability labeling requires trigger capability: `TIGHTEN`
- Executor trigger-capability check before queueing: `TIGHTEN`
- Fresh FORMAL one-way transition: `INSUFFICIENT_EVIDENCE`
- Terminal current object never reactivated: `KEEP`
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
- Theory Forge probe fidelity to predeclared discriminator: `TIGHTEN`
- Whole-Theory kill from non-diagnostic prototype reduction: `RELAX`
- Fast Forge/canonical separation: `KEEP`
- Claim ceiling enforcement: `KEEP`
- Mechanism-supply health: `CLARIFY`
- READY vs authority vs executable distinction: `CLARIFY`
- PASS reachability without weaker standards: `KEEP` scientifically / operationally blocked

## Mandatory questions

1. Development phases consistent end-to-end? **Yes** on current objects; FORMAL consumption remains unobserved.
2. Cycle 3 mistaken for a hard cap? **No**.
3. Science-invariant vs science-affecting changes distinguished? **Yes** on H7 and terminal paths.
4. Development observations kept out of independent evidence credit? **Yes**.
5. FORMAL one-way integrity unchanged? **Yes**. No H7 identity/START/preserve/result exists; the fixed workflow preserves one-way ordering.
6. Legitimate fresh SYSTEM->MECHANISM successors suppressed or manufactured? **No same-object manufacture observed.** However, noncanonical Theory supply is slightly over-suppressed by an off-discriminator kill.
7. PRE_FORMAL genuine development? **Yes**.
8. Terminal semantics calibrated? **Yes**; all 34 terminal current objects remain terminal.
9. Revisit catches genuinely changed conditions? **Not yet demonstrated live**; no current material trigger is being missed.
10. Revisit avoids rescue laundering/zombie inflation? **Yes in current observations**.
11. REVISIT_FORGE_TEST tests the new trigger rather than old failure? **Insufficient evidence**; no live Revisit Forge case exists.
12. Bootstrap complete and conservative? **Yes**, with candidate-specific provenance still required before live triggering.
13. PASS realistically reachable without weaker standards? **Scientifically yes; operationally not by the currently observed executor because the frozen trigger cannot be invoked.** No standard relaxation is needed.

## Risks

False-positive / zombie inflation: `LOW_CURRENT_MODERATE_FUTURE_TRIGGER_WATCH`.

False-negative / forgotten valuable lines: `MODERATE`, driven now both by untested live Revisit sensitivity and the overly broad TH-001 kill inference.

Moving-goalpost / rescue: `LOW_CURRENT`. H7 R5 remains unchanged; no terminal same-object rescue is admitted.

Over-terminalization / candidate starvation: `MODERATE`. Revisit has not missed a concrete trigger, but Theory supply should not be terminated by a probe that did not instantiate its frozen discriminator.

FORMAL integrity risk: `LOW_CURRENT`. The runtime failed closed before identity/START. Execution-readiness observability risk is `MODERATE` because queue/executable status did not include actual trigger capability.

Mechanism supply: `FRAGILE_ZERO_AUTONOMOUS_EXECUTABLE_CURRENTLY`.

## Prospective recommendations

1. Keep R106's exact H7 scientific/integrity bindings unchanged, but separate `FORMAL_AUTHORIZED` from `EXECUTOR_TRIGGER_CAPABLE`; only call H7 effectively executable when the authorized lane can invoke the frozen trigger without changing it.
2. Add a result-free capability check before queueing/marking effective execution: verify that the designated executor exposes the exact required tag-creation or workflow-dispatch primitive and permissions. If absent, HOLD rather than changing the frozen workflow.
3. Preserve all one-way H7 rules: fresh identity, no rerun/retune/rescore, raw-before-score, remote preserve-before-target-read, exact source/controller/runtime/input/scorer/preserver binding, create-only evidence refs.
4. Treat the recurrent-continuation Forge result as a reduction of that prototype, not sufficient falsification of TH-001's predeclared Q0-vs-QI discriminator. A single bounded probe implementing the already-frozen Q0/QI partition-and-intervention test remains methodologically legitimate and is not rescue tuning.
5. Keep TH-001 and all Forge/Theory outputs noncanonical and zero-credit unless a fresh Analyst prospectively creates a canonical object under independent criteria.
6. Keep all old terminal candidate IDs terminal forever. Require candidate-specific independent trigger provenance before any Revisit activation; do not auto-trigger from Theory freshness labels.
7. Do not weaken evidence standards to solve mechanism-supply or executor-capability shortages.

## Utility request

`NONE`. No Utility proposal is needed for this calibration finding; the missing launch primitive is an operational capability issue and the auditor does not dispatch or mutate operations.

## Hard-floor confirmation

This audit dispatched no experiment, created/consumed no identity, mutated no research/evidence/scientific refs, merged no PR, changed no scheduler, changed no scientific criterion, reran/retuned/rescored no consumed FORMAL identity, reactivated no terminal object, and rewrote no historical PASS/FAIL.

## Confidence

`HIGH` — 0.99. The H7 trigger-capability block and the TH-001 discriminator/probe mismatch are directly observable in current repository/history artifacts. Revisit live-trigger behavior remains an evidence gap rather than a demonstrated defect.

## Questions for Control / Analyst

- Distinguish scientific one-shot authority from actual executor capability: if the authorized lane cannot create the frozen launch tag, classify H7 as operationally HOLD/non-executable without changing R5 or the bound workflow.
- For TH-001, do not require genuinely new information merely to run the already-predeclared Q0-vs-QI discriminator that the recurrent toy did not instantiate; keep any such probe bounded, noncanonical and zero-credit.
- Continue candidate-specific Revisit trigger scans and expose the first genuine trigger -> decision -> optional Forge -> fresh successor chain for calibration.
