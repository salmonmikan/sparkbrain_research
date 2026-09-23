# SparkBrain Methodology Calibration Audit — R99

- schema_version: 2
- generation_id: `METHCAL-20260924T062241+0900-R99-6E3A91B4`
- produced_at: `2026-09-24T06:22:41+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260924T051916+0900-R98-7D3B4C91`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

R98 was read first. The programme remains `MIXED_CALIBRATION` with the hard scientific-integrity floor intact.

Two material post-R98 observations matter.

First, MAIN Relay has now implemented the most important semantic separation requested by R98 without touching science. H7 remains scientifically `READY`, `ACTIVE`, `QUEUED`, `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`, and retains R106's exact one-shot FORMAL authority. The Relay no longer rewrites the scientific Funnel to `HOLD` merely because its own execution surface cannot create the frozen `launch/h7-r5-*` tag. Instead it records an orthogonal `operational_blocker.class=EXECUTION_CAPABILITY`, with `scientific_funnel_changed=false`. It again failed closed before identity/START, protected evaluation, raw output, scoring, or evidence mutation. This is a calibrated improvement: scientific readiness/authority and executor capability are now represented separately in the current MAIN mailbox.

A residual observability inconsistency remains. The designated Analyst R106 still reports `effectively_executable_mechanism=1`, while the independently observed PRIMARY and RELAY execution surfaces cannot invoke the prospectively frozen trigger. `queue_state=QUEUED` can remain valid if it means scientifically authorized queue membership, but `effectively_executable` must not mean operationally runnable until a permitted trigger actor is verified. The next fresh Analyst generation should reconcile this aggregate rather than forcing MAIN to alter the scientific Funnel.

Second, Fast Forge at 05:35:55 JST performed a no-op and rejected a TH-001 follow-up because the prior probe was treated as Theory-killed and no fresh bounded Theory probe had been supplied. That no-op is safe, noncanonical and zero-credit; it touched no H7, terminal candidate, held-out, or evidence surface. However, it consumed methodology R97 even though R98 had already been durably persisted before the Forge run. R98 had specifically found that the recurrent-loop probe did not instantiate TH-001's predeclared Q0-vs-QI discriminator and that completing that already-frozen discriminator should not require genuinely new information. The stale methodology input therefore had a real throughput consequence: the known over-conservative kill remained effective and the contract-faithful discriminator was not considered. This is not rescue laundering or an evidence-integrity incident; it is a control-plane freshness / false-negative problem.

Revisit remains unchanged and conservative. All 34 terminal current objects remain terminal. The ledger remains 1 `CLOSED_STRONG`, 19 `DORMANT_REVISITABLE`, 14 `DEFERRED_INDEPENDENT_REIDENTIFICATION`, 0 `REVISIT_TRIGGERED`; no live `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE` exists, no old ID has been reopened, and no historical outcome has been rewritten.

Independent repository checks at this cutoff confirm stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` remains exactly five tags; tag-form `formal/*`, `sealed/*`, `freeze/*`, and `immutable/*` are empty; H7 `control/h7*` and `preserve/h7*` heads are absent; and no `launch/h7-r5-*` tag exists. Therefore no H7 FORMAL one-way transition has begun.

## Input generations and authority reconstruction

Prior methodology: R98 (`METHCAL-20260924T051916+0900-R98-7D3B4C91`) at branch head `967cf3d244e19804c93368526cab4d9ef4b59e9c`, classified `MIXED_CALIBRATION`. R98 separated scientific authority from executor trigger capability and found the TH-001 whole-theory kill slightly over-conservative because the executed toy did not instantiate the frozen Q0-vs-QI discriminator.

Human process directive: `HUMAN-20260922-005` is consumed only as a process directive, never as scientific evidence.

Control: R48 (`CTRL-20260924T045900+0900-R48-6F2C1A84`) at `8b8cea6136d1b0e2d821fce1d4f75f8709a4fed0`, a designated control-history mailbox that predates R106 and the later capability observations.

Canonical gate: Analyst R106 (`EVA-20260924T050035+0900-R106-H7-LAUNCH-READY-THEORY-PROBE-KILLED`) at `770edcb0cf050ed7cdf41d4716ed645952e69475`. It keeps H7 `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`, `READY`, `ACTIVE`, `QUEUED`, grants one exact-binding FORMAL authority, and leaves identity uncreated/unconsumed. Its aggregate still says `effectively_executable_mechanism=1`.

Fresh MAIN Relay: `MAIN-20260924T054727+0900-RELAY-H7-R106-FORMAL-LAUNCH-CAPABILITY-BLOCKED` at mailbox branch head `e5a1927352b0671456dd8c1166cccea72a510817`. It preserves the Analyst Funnel exactly while recording the unavailable launch primitive as a separate operational blocker and fails closed before identity/START.

External Theory: TH-001 (`TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT`) remains noncanonical and zero-credit at external research handoff `226d812c96df3d71186ba5a4fb2ac1b27c0d6e25`.

Theory Forge prototype: `forge/20260924-recurrent-continuation-a@17b2673cd0417fdf931264a71d8df1f9c1c21f23` remains unchanged and zero-credit.

Fresh Fast Forge mailbox: `FORGE-20260924T053555+0900-NOOP-R106-R97-THEORY-KILLED`. It executed no probe and rejected a TH-001 follow-up because no fresh post-kill probe spec existed. Its methodology input was R97, not already-durable R98.

## Development iteration calibration

Development semantics remain consistent on canonical objects. H7 stays `RESULT_EXPOSED_DEVELOPMENT` with R5 unchanged; the launch-path work and Relay bookkeeping are science-invariant plumbing/control-plane reconciliation only. Candidate #35 remains `RESULT_EXPOSED_DEVELOPMENT`, `TERMINAL_FOR_CURRENT_OBJECT`, zero confirmatory credit, with no same-object rerun/retune/rescore and no same-object SYSTEM-to-MECHANISM upgrade.

Cycle 3 remains a mandatory reassessment point, not an automatic terminal cap. No current termination is driven solely by cycle count.

Science-invariant and science-affecting changes remain correctly separated. No metric/scorer meaning, threshold/tolerance, comparator, intervention, seed/exclusion policy, resource/privilege contract, hypothesis, falsifier or success criterion was changed in the fresh MAIN Relay or Fast Forge no-op.

Development/Theory/Forge observations remain outside independent confirmatory credit. No laundering into evidence is observed.

## PRE_FORMAL / FORMAL calibration

PRE_FORMAL remains genuine development. H7 being scientifically `READY` while the current executor is unable to invoke the frozen launch trigger is methodologically coherent so long as readiness, FORMAL authority, queue membership and operational executability are not conflated.

The Relay's new `operational_blocker` is a good correction. It should be retained as an axis orthogonal to the Analyst Funnel. The prior attempt to convert the scientific queue to HOLD because of local runtime capability was over-coupled; the current reconciliation correctly avoids that.

The residual problem is naming and aggregation. Analyst R106's `effectively_executable_mechanism=1` is false if `effective` means actually startable by the currently authorized/observed execution lane. Prospectively either (a) define `QUEUED` strictly as scientific queue membership and add a distinct `operationally_triggerable` / `executor_trigger_capable` field, or (b) keep an `effective_executable` aggregate but require both scientific authority and verified trigger capability. Do not solve this by mutating the frozen workflow trigger.

FORMAL one-way integrity remains unchanged. No H7 identity, START, protected evaluation read, raw production/preservation, official score, preserve ref, formal/sealed/freeze/immutable tag or evidence ref has appeared. Scientific PASS remains reachable without weaker standards once a permitted exact trigger actor exists.

## Theory / Forge calibration

Theory/canonical separation remains strong. TH-001 and its Forge outputs remain noncanonical and zero-credit.

The first recurrent-continuation prototype remains validly reducible by ordinary recurrence; that prototype should stay killed. But that result does not instantiate the predeclared TH-001 discriminator: predictive-equivalent Q0 histories followed by the same frozen intervention family and a test for QI refinement. Therefore the whole-theory kill remains too broad.

The fresh 05:35 Fast Forge no-op turns this from a merely theoretical calibration issue into an observed throughput issue. Forge rejected `TH-001 follow-up` because the prior Analyst-gated probe was already killed and no fresh post-kill bounded Theory spec existed. Yet R98, already durable before that run, had concluded that one bounded execution of the original Q0-vs-QI discriminator remains contract-faithful and does not require new information. The no-op itself is safe, but the selection path is stale and over-conservative.

There is a second control-plane issue: Fast Forge consumed methodology R97 even though R98 was already the designated latest history. Because methodology is advisory rather than scientific authority, this did not authorize an unsafe action. But stale methodology can suppress legitimate zero-credit exploration. Prospectively, Forge selection should read the latest completed methodology generation before deciding that an Analyst Theory kill leaves no eligible bounded test; if Analyst authority conflicts, Forge must still obey Analyst and remain no-op, while surfacing the discrepancy for a fresh Analyst rather than self-dispatching.

No Utility request is needed to test this. The discrepancy is already demonstrated by durable histories.

## Revisit / resurrection calibration

The Revisit axis remains orthogonal to terminal state. All 34 terminal current objects remain terminal, with no historical PASS/FAIL rewrite and no old candidate ID returned to ACTIVE.

Bootstrap remains complete and conservative: 34/34 classified, with no aggressive resurrection and no systematic `CLOSED_STRONG` default. Broad class-level `what_would_change_our_mind` templates remain only discovery scaffolding; candidate-specific closure provenance is still required before any live trigger.

No genuine material independent trigger is currently being missed in the inspected Revisit ledger. TH-001's recurrence reduction is not a candidate-specific trigger for any old terminal object. Candidate #35's rescue-adjacent family remains deferred correctly.

There is still no live `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE`. Thus end-to-end changed-condition sensitivity and the requirement that Revisit Forge kill the NEW trigger rather than rerun an old failure remain `INSUFFICIENT_EVIDENCE`.

## Funnel / candidate supply / pass reachability

Claim ceilings remain enforced. No same-object SYSTEM-to-MECHANISM uplift is observed.

Mechanism supply remains fragile. H7 is the only nonterminal canonical MECHANISM object. It is scientifically READY and FORMAL-authorized, but no observed autonomous lane can create the frozen launch tag. Thus scientifically queued count can be 1 while operationally triggerable count remains 0; these must be separately observable.

Theory supply is also unnecessarily constrained by the still-effective whole-theory kill. The 05:35 no-op demonstrates that the original bounded discriminator is currently suppressed pending a fresh Analyst correction. This is a moderate false-negative / throughput risk, not a reason to weaken canonical evidence standards.

PASS remains realistically reachable without weakening evidence standards. The blocker is operational trigger capability, not scientific criteria. The correct response is a permitted exact trigger actor and fresh pre-START checks, never trigger mutation, protocol relaxation, identity reuse, or post-outcome repair.

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
- Executor-capability axis orthogonal to scientific Funnel: `KEEP`
- Scientific queue membership may coexist with operational blocker: `CLARIFY`
- Effective-executability aggregate requires verified trigger capability: `TIGHTEN`
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
- Forge methodology-freshness before selection: `TIGHTEN`
- Fast Forge/canonical separation: `KEEP`
- Claim ceiling enforcement: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development phases consistent end-to-end? **Yes** on current canonical objects; H7 remains result-exposed R5 unchanged.
2. Cycle 3 mistaken for a hard cap? **No**.
3. Science-invariant vs science-affecting changes distinguished? **Yes** in the fresh MAIN/Forge observations.
4. Development observations kept out of independent evidence credit? **Yes**.
5. FORMAL one-way integrity unchanged? **Yes**. No H7 identity/START/result/evidence exists.
6. Legitimate fresh SYSTEM-to-MECHANISM successors suppressed or manufactured? **No same-object manufacture observed.** Theory supply is slightly over-suppressed by the overbroad TH-001 kill.
7. PRE_FORMAL genuine development? **Yes**.
8. Terminal semantics calibrated? **Yes**; all 34 terminal objects remain terminal.
9. Revisit catches genuinely changed conditions? **Not demonstrated live; no concrete current independent trigger is observed as missed.**
10. Revisit avoids rescue laundering and zombie inflation? **Yes in current observations.**
11. REVISIT_FORGE_TEST probes test new triggers rather than old failures? **Insufficient evidence; no live Revisit Forge test exists.**
12. Bootstrap complete and conservative? **Yes**, with candidate-specific provenance still required before live triggering.
13. PASS realistically reachable without weaker standards? **Scientifically yes. Operationally not yet from the observed lanes because the exact frozen trigger primitive is unavailable.**

## Risks

False-positive / rescue-laundering / zombie inflation: `LOW_CURRENT_MODERATE_FUTURE_TRIGGER_WATCH`.

False-negative / forgotten valuable lines: `MODERATE`, due untested live Revisit sensitivity plus observed Theory suppression from an off-discriminator kill and stale-methodology Forge selection.

Moving-goalpost / rescue: `LOW_CURRENT`. H7 R5 and all terminal objects remain unchanged.

Over-terminalization / candidate starvation: `MODERATE`. No concrete Revisit trigger is currently missed, but the predeclared TH-001 discriminator remains untested while downstream Forge now treats the theory as killed.

FORMAL integrity risk: `LOW_CURRENT`. MAIN repeatedly fails closed before identity/START.

Execution-readiness observability: `MODERATE_BUT_IMPROVING`. MAIN now has an orthogonal operational blocker, but Analyst's aggregate still reports one effectively executable mechanism.

Mechanism supply: `FRAGILE_ONE_SCIENTIFICALLY_QUEUED_ZERO_OBSERVED_TRIGGERABLE`.

## Prospective recommendations

1. Keep H7 R106 scientific authority, science/controller/runtime/input/scorer/preserver bindings and one-way rules unchanged.
2. Keep MAIN's new operational blocker orthogonal to the scientific Funnel. Define `QUEUED` as scientific queue membership if desired, but add/maintain an explicit `executor_trigger_capable=false` / `operationally_triggerable=false` field until a permitted actor can create the exact frozen tag.
3. On the next fresh Analyst pass, reconcile `effectively_executable_mechanism` with the executor-capability observation; do not alter the frozen workflow to make the metric true.
4. Require Forge selection to read the latest completed methodology generation. Methodology remains advisory only; if it conflicts with current Analyst authority, Forge must stop and surface the discrepancy rather than self-authorize.
5. For TH-001, keep the recurrent-loop prototype killed, but do not require genuinely new information merely to perform one bounded, zero-credit implementation of the already-predeclared Q0-vs-QI discriminator. A fresh Analyst should decide whether to restore that specific test as eligible.
6. Keep Theory/Forge outputs noncanonical and zero-credit; no promotion or evidence credit may inherit from the old toy, Theory proposal, or methodology finding.
7. Keep all old terminal candidate IDs terminal forever. Continue candidate-specific independent-trigger scans and require a fresh ID/falsifier/reduction ladder for any valid Revisit canonicalization.
8. Do not weaken evidence standards to solve trigger-capability, mechanism-supply or Theory-throughput problems.

## Utility request

`NONE`. The relevant calibration failures are already demonstrated by durable current-state observations; no new Utility experiment or operation is justified.

## Hard-floor confirmation

This audit dispatched no experiment, consumed no identity, mutated no research/evidence/scientific ref, merged no PR, changed no scheduler, changed no scientific criterion, reran/retuned/rescored no consumed FORMAL identity, reactivated no terminal object, and rewrote no historical PASS/FAIL. Persistence is limited to the designated append-only methodology-audit history plus its designated latest/state pointers.

## Confidence

`HIGH` — 0.99. The post-R98 MAIN and Fast Forge states are durable and directly inspectable; stable main and protected evidence namespaces were independently re-fetched. Uncertainty remains only for behaviors not yet exercised: actual H7 FORMAL consumption and live Revisit trigger/Forge/canonicalization.

## Questions for Control / Analyst

- Should `queue_state=QUEUED` be formally defined as scientific queue membership independent of operational triggerability, with a separate executor-capability axis?
- Will the next Analyst generation reconcile `effectively_executable_mechanism` to the observed trigger blocker rather than modifying the scientific Funnel?
- Will TH-001's already-predeclared Q0-vs-QI discriminator be restored as an eligible bounded zero-credit test without demanding new information, while keeping the recurrent-loop prototype killed?
- Will Fast Forge be required to consume the latest completed methodology generation before its selection scan, while preserving Analyst as the only canonical scientific gate?
