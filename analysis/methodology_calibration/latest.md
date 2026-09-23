# SparkBrain Methodology Calibration Audit — R97

- schema_version: 2
- generation_id: `METHCAL-20260924T042120+0900-R97-C9CE09C7`
- produced_at: `2026-09-24T04:21:20+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260924T032000+0900-R96-A61E94F2`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

R96 was read first. Two material changes occurred after it.

First, H7's R104 `GO_ONCE_CONDITIONAL_EXACT_BINDING` authority was correctly withdrawn by fresh Analyst R105 after Relay independently discovered that the repository had a green NON_RESULT readiness workflow but no prospectively fixed result-bearing H7 one-way launch controller/protected-payload/identity path. No FORMAL identity, START, protected evaluation read, score, preserve ref, or result was created. H7 remains scientifically `READY`, `RESULT_EXPOSED_DEVELOPMENT`, revision `R5_UNCHANGED`, and nonterminal, but is operationally on `NONTERMINAL_HOLD` with FORMAL authority STOP until the missing launch mechanics are implemented as strictly science-invariant, non-result plumbing and then re-reviewed by a fresh Analyst.

The current fail-closed behavior is calibrated. However, R104's earlier FORMAL authority issuance was slightly premature at the control boundary: exact result-bearing launch mechanics should be materially present and prospectively bindable before a one-shot FORMAL authority is issued, rather than discovered missing during the post-authority prestart step. This was caught before identity consumption, so there is no integrity incident. Prospectively the authority-issuance gate should be tightened while preserving the distinction that scientific READY can remain true even when operational executability is false.

Second, the dedicated Theory stream is now initialized. Theory R1 (`TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT`) is noncanonical, non-evidentiary, explicitly independent of the unknown H7 FORMAL outcome, and gives zero confirmatory credit to Candidate #34/#35 development observations. Analyst R105 classified it `THEORY_FORGE_TEST`, not canonicalization, with a bounded exposed-synthetic-surface discriminator, explicit ordinary reductions, informative negative outcome, and prohibited H7/Candidate-34/Candidate-35 rescue surfaces. This materially improves Theory/canonical separation observability. No Theory Forge probe has run yet.

Revisit remains conservative and unchanged from R96: all 34 terminal current objects remain terminal, the bootstrap remains 1 `CLOSED_STRONG` / 19 `DORMANT_REVISITABLE` / 14 `DEFERRED_INDEPENDENT_REIDENTIFICATION` / 0 `REVISIT_TRIGGERED`, no old ID is reopened, and no historical outcome is rewritten. There is still no live `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE`, so end-to-end changed-condition sensitivity remains unobserved. The candidate-specific closure-provenance requirement before the first live trigger remains necessary.

Independent repository checks confirm stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, authoritative `evidence/*` tags remain exactly five, tag-form `formal/*`, `sealed/*`, and `freeze/*` are empty in the checked namespaces, and H7 `control/h7*` and `preserve/h7*` heads are absent. The current controller contains the readiness workflow but no H7-specific result-bearing launch workflow. No terminal object has returned to ACTIVE.

## Authority reconstruction

Prior methodology history: R96 classified the programme `MIXED_CALIBRATION`; it accepted the 34/34 Revisit bootstrap, kept candidate-specific trigger provenance as a clarification, and considered H7 conditionally executable under R104 while noting that the live one-way transition remained unobserved.

Designated Control history: Control R47 (`CTRL-20260924T035154+0900-R47-9D2B6F41`) observed green readiness/CI and still described the R104 conditional prestart path. It predates Analyst R105 and is governance history only for the current H7 execution state.

Designated canonical gate: Analyst R105 (`EVA-20260924T040500+0900-R105-H7-LAUNCHPATH-HOLD-THEORY-FORGE-TEST`) is the newest canonical scientific classification. It supersedes R104's conditional FORMAL authority, retains H7 as scientifically READY but operationally held, and authorizes only strictly NON_RESULT science-invariant launch-path plumbing followed by a fresh Analyst generation.

MAIN/Relay: the fresh Relay generation failed closed before identity/START because `MISSING_PROSPECTIVELY_FIXED_RESULT_BEARING_H7_ONE_WAY_FORMAL_CONTROLLER_PATH`. Its inspection found green readiness/CI, untouched one-way namespaces, unchanged science bytes, and no protected evaluation access or scoring.

Theory/Revisit/Forge: Theory R1 is now durable and Analyst-gated for a bounded Forge falsification only. It emitted no Revisit proposal. Latest Forge state predates that gate and executed no Theory/Revisit probe. Candidate #35's post-outcome immediate-successor surface remains deferred as rescue-adjacent and zero-credit.

## Development iteration calibration

Development-phase semantics remain consistent on current objects. H7 stays `RESULT_EXPOSED_DEVELOPMENT` despite repeated non-result infrastructure work; green readiness did not reset it to OPEN, and the later launch-path hold also does not reset it. Candidate #35 remains result-exposed and terminal. No same-object science-affecting change is authorized after exposure.

Cycle 3 remains a reassessment point, not an automatic terminal cap. No current decision terminalizes or revives an object based on cycle count alone.

Science-invariant versus science-affecting repair is currently distinguished correctly. R105 limits H7 work to controller entry, protected-payload handoff, identity materialization mechanics without creating an identity, START no-clobber, preserve-before-read ordering, and frozen binding checks. Any need to change scientific threshold, comparator, metric, intervention, scorer, resource contract, falsifier, or success semantics requires stopping for a versioned development revision or fresh successor.

Development observations remain outside independent confirmatory credit. Candidate #34/#35 development observations are used by Theory only as constraints/reduction context, not as positive support. Theory output and future Forge output carry zero scientific credit unless separately admitted under a fresh prospective canonical contract.

## PRE_FORMAL / FORMAL calibration

PRE_FORMAL remains genuine development rather than a hidden second FORMAL gate. H7 retains `preformal_readiness=READY` while `formal_authority=STOP` and `queue_state=HOLD`. This is a useful calibration demonstration: READY means the next scientific question is well-defined and informative; it does not mean the operational one-way execution path is currently executable or that the candidate already succeeded.

The new H7 hold is not a hidden success gate. It is an integrity prerequisite required by the hard floor: the exact result-bearing workflow/controller/protected-payload/identity path itself must be prospectively fixed and bound before one-way consumption begins.

FORMAL one-way integrity is unchanged. The frozen R5 contract still fixes source/runtime/components/scorer/preserver, target-blind raw generation, preserve-before-target-access, and post-preserve scoring semantics. Fresh checks show no H7 identity, START/control ref, preserve ref, protected read, or score. The live `RESULT_EXPOSED_DEVELOPMENT -> CONSUMED_ONE_WAY` transition remains unobserved.

### Authority issuance calibration

This is the main new methodology finding. R104 issued one conditional FORMAL authority after NON_RESULT readiness became green, but the exact result-bearing launch path had not yet been materialized. Relay caught the missing path before consumption and R105 corrected the state.

Prospectively, a one-shot FORMAL authority should require all result-bearing launch mechanics needed for the frozen contract to exist and be prospectively bindable in NON_RESULT form before authority issuance. This does **not** require a scientific result, comparator win, falsifier survival, or hidden second FORMAL gate. It only moves an integrity/plumbing check earlier so authority means executable-if-exact rather than theoretically executable after further implementation.

Gate classification: `TIGHTEN` for FORMAL authority issuance; `KEEP` for the current R105 fail-closed hold and exact-binding hard floor.

## Revisit / resurrection calibration

### Orthogonality and terminal immutability

Still calibrated. All 34 terminal current objects remain terminal. Revisit metadata did not mutate `terminal_state`, and no historical PASS/FAIL was rewritten.

### Bootstrap quality

Coverage remains complete and conservative. There is no aggressive resurrection and no systematic `CLOSED_STRONG` default. The residual R96 issue is unchanged: many legacy rows use coarse R49 Funnel classes and class-level `what_would_change_our_mind` templates. Those are acceptable admission scaffolding but are not sufficient trigger proof. Before any row enters `REVISIT_TRIGGERED`, candidate-specific closure provenance must be recovered or the case must require independent re-identification.

### Changed-condition sensitivity

No genuine independent Revisit trigger has traversed the system. Theory R1 explicitly performed a terminal relevance scan and emitted no Revisit proposal. No new literature/capability/canonical-result event was accepted as changing a specific old closure. Therefore false-negative protection is structurally improved by the ledger but live sensitivity remains `INSUFFICIENT_EVIDENCE`.

### Rescue / zombie control

Current behavior remains strong. Candidate #35 is still the key negative control: its immediate post-outcome successor family is excluded, zero-credit, and not admitted as an independent trigger. Theory R1 also prohibits Candidate #34/#35 same-object and immediate rescue families from its Forge surface. No fresh ID has been manufactured to launder an old outcome.

### Theory as a possible future Revisit trigger

Theory R1 marks itself `genuinely_new_information=true`, but it is a new non-evidentiary programme-level theory proposal rather than new empirical evidence. Current routing is safe because Theory emitted no Revisit proposal and Analyst triggered no ledger row. Prospectively, the Theory field must never automatically satisfy Revisit independence/materiality: any Theory-derived Revisit trigger must still show candidate-specific independence, how it changes the old closure boundary, a meaningfully distinct new question, and zero inherited confirmatory credit.

### REVISIT_FORGE_TEST / REVISIT_CANONICALIZE

Still no live case. A Revisit Forge test must attack the **new trigger** cheaply and must not rerun/retune the old failed object. Canonicalization must leave the old object terminal, create a fresh candidate ID and fresh prospective reduction/comparator/falsifier contract, preserve informative negative outcomes, and inherit zero confirmatory credit from old/Forge/Theory/Revisit observations.

## Theory / Forge calibration

Theory/canonical separation is now directly observed and should be `KEEP`. TH-001 does not create a candidate, execution authority, or scientific evidence. Its proposed first discriminator is deliberately cheap and adversarial; failure is informative and should kill the stronger theory on that surface. It is explicit about close prior art and does not claim a new mathematical invention.

The Analyst's `THEORY_FORGE_TEST` decision is calibrated: the proposal is programme-level rather than an immediate Candidate #34/#35 rename, independent of unknown H7 results, and constrained to exposed synthetic nonrescue surfaces. Forge cannot self-promote; a survivor must return to a later fresh Analyst gate.

No Theory Forge probe has executed yet, so actual probe discipline is not yet observed. The current spec is good; execution remains an evidence gap for methodology calibration.

## Funnel / mechanism supply / pass reachability

Claim ceilings remain enforced. Candidate #35 stays SYSTEM and terminal. Candidate #34 stays terminal/reducible. No fresh SYSTEM->MECHANISM successor has been manufactured.

Mechanism supply is fragile: H7 is the only nonterminal MECHANISM line and is currently infrastructure-held, leaving effectively executable MECHANISM count at zero. Theory/Forge offers a noncanonical discovery path without manufacturing canonical activity, which is preferable to weakening candidate admission.

PASS remains realistically reachable without lowering evidence standards. The blocker is a science-invariant result-bearing launch-path implementation, not a requirement that H7 demonstrate success before FORMAL. After that plumbing is prospectively fixed and revalidated by a fresh Analyst, one fresh identity can still enter the unchanged one-way protocol. The current status is temporarily non-executable, not scientifically unreachable.

## Gate classifications

- Hard integrity floor: `KEEP`
- Development-phase monotonicity: `KEEP`
- Cycle-3 mandatory reassessment: `KEEP`
- Cycle-3 automatic hard cap: `RELAX`
- Science-invariant vs science-affecting separation: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL as genuine development: `KEEP`
- Hidden second FORMAL gate: `KEEP`
- Result-bearing launch path prospectively fixed before FORMAL authority issuance: `TIGHTEN`
- Current H7 fail-closed launch-path hold: `KEEP`
- Fresh FORMAL one-way transition: `INSUFFICIENT_EVIDENCE`
- Terminal current object never reactivated: `KEEP`
- Revisit axis orthogonal to terminal state: `KEEP`
- Revisit bootstrap coverage: `KEEP`
- Revisit bootstrap conservatism: `KEEP`
- Revisit bootstrap historical specificity / trigger provenance: `CLARIFY`
- Revisit independent-trigger detection end-to-end: `INSUFFICIENT_EVIDENCE`
- Revisit rescue-laundering prevention: `KEEP`
- Revisit fresh-candidate / zero inherited credit: `KEEP`
- Theory field `genuinely_new_information` as automatic Revisit trigger: `CLARIFY`
- REVISIT_FORGE_TEST new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- REVISIT_CANONICALIZE full gate: `INSUFFICIENT_EVIDENCE`
- Theory/canonical separation: `KEEP`
- Theory-to-Forge bounded falsification gate: `KEEP`
- Fast Forge/canonical separation: `KEEP`
- Claim ceiling enforcement: `KEEP`
- Mechanism-supply health: `CLARIFY`
- READY vs executable/FORMAL distinction: `KEEP`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development phases consistent end-to-end? **Yes** on current live/terminal objects; live FORMAL consumption remains unobserved.
2. Cycle 3 mistaken for a hard cap? **No**.
3. Science-invariant vs science-affecting changes distinguished? **Yes** in current H7 repair authorization and terminal paths.
4. Development observations kept out of independent evidence credit? **Yes**.
5. FORMAL one-way integrity unchanged? **Yes**. No H7 identity/START/preserve/result exists. Authority issuance should be tightened prospectively so launch mechanics pre-exist authority.
6. Legitimate fresh SYSTEM->MECHANISM successors suppressed/manufactured? **No manufacture observed**. Theory creates no candidate and Candidate #35 rescue-adjacent successors remain blocked.
7. PRE_FORMAL genuine development? **Yes**. H7 READY remains true while execution is held.
8. Terminal semantics calibrated? **Yes**. All 34 terminal objects remain terminal.
9. Revisit catches genuinely changed conditions? **Not yet demonstrated live**. Ledger exists and differential scans run, but no genuine trigger has traversed end-to-end.
10. Revisit avoids rescue laundering/zombie inflation? **Yes in current observations**.
11. REVISIT_FORGE_TEST tests new trigger rather than old failure? **Insufficient evidence**; no live Revisit Forge test yet.
12. Bootstrap coverage complete and conservative? **Yes**, with candidate-specific historical provenance still required before live triggering.
13. PASS realistically reachable without weakening evidence standards? **Yes**, after science-invariant launch-path plumbing and fresh Analyst review; currently not executable.

## Risks

False-positive / zombie inflation: `LOW_CURRENT_MODERATE_FUTURE_TRIGGER_WATCH`. Current anti-rescue controls are strong; broad bootstrap templates and Theory freshness labels must not become automatic trigger proof.

False-negative / forgotten valuable lines: `MODERATE_WATCH`. Ledger coverage is complete and Theory now performs terminal relevance scans, but no genuine trigger has proven end-to-end rediscovery sensitivity.

Moving-goalpost / rescue: `LOW_CURRENT`. H7 scientific R5 is unchanged; Candidate #35 rescue-adjacent family remains blocked; Theory/Forge is isolated and zero-credit.

Over-terminalization: `MODERATE_WATCH`. No material independent trigger is currently being ignored, but live Revisit sensitivity is still untested.

Formal authority / infrastructure sequencing: `MODERATE_PROCESS_RISK_CORRECTED_BEFORE_CONSUMPTION`. R104 authority preceded full result-bearing launch-path materialization; R105 corrected this without scientific exposure.

Mechanism supply: `FRAGILE_ZERO_EXECUTABLE_CURRENTLY`. This is a throughput risk, not a basis to weaken evidence or manufacture successors.

## Prospective recommendations

1. Require the exact result-bearing one-way launch controller/protected-payload/identity/preserve-before-read mechanics to exist and be prospectively bindable before issuing fresh FORMAL authority. READY may remain true independently.
2. Keep R105's allowed H7 launch-path work strictly NON_RESULT and science-invariant; after implementation, stop for a fresh Analyst before identity/START.
3. Keep all old terminal candidate IDs terminal forever and preserve zero inherited confirmatory credit.
4. Before any Revisit row becomes triggered, bind the new information to candidate-specific historical closure provenance; treat bootstrap templates only as discovery scaffolding.
5. Do not treat Theory `genuinely_new_information=true` as automatic Revisit independence/materiality. Require an explicit candidate-specific Revisit proposal and fresh Analyst decision.
6. If TH-001 Forge testing runs, keep it on the predeclared exposed synthetic nonrescue surface, attack ordinary reductions first, grant zero scientific credit, and return any survivor to fresh Analyst review.
7. Keep Candidate #35's immediate post-outcome successor family deferred unless independently re-identified through a genuinely new source/question.
8. Keep exact FORMAL raw-before-score, preserve-before-read, one-identity, frozen-binding rules unchanged.

## Utility request

`NONE`. No bounded Utility proposal is needed. The current issues are already observable from repository/control history and do not justify extra operational work.

## Hard-floor confirmation

Confirmed. This audit dispatched no experiment, consumed no identity, mutated no research/evidence/formal/sealed/freeze/immutable/scientific-preserve ref, merged no PR, changed no scheduler or scientific criterion, reran/retuned/rescored no consumed FORMAL identity, reopened no terminal object, and rewrote no historical PASS/FAIL. Persistence is limited to the designated methodology-calibration audit latest/state/history files.

## Confidence

`HIGH` (`0.98`).

## Questions for Control / Analyst

- Make prospectively materialized result-bearing launch mechanics a prerequisite for future FORMAL authority issuance, while keeping READY separate from executability.
- After H7 launch plumbing exists, require one fresh Analyst generation before identity/START and preserve unchanged R5 science.
- Keep Theory `genuinely_new_information` distinct from a candidate-specific Revisit trigger; no automatic ledger activation.
- Expose the first genuine Revisit trigger -> decision -> optional Forge test/canonicalization chain so Methodology can audit rescue-vs-rediscovery behavior end-to-end.
