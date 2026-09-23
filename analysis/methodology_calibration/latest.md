# SparkBrain Methodology Calibration Audit — R96

- schema_version: 2
- generation_id: `METHCAL-20260924T032000+0900-R96-A61E94F2`
- produced_at: `2026-09-24T03:20:00+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260924T021800+0900-R95-8D3A71C4`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

R95 was read first. The material improvement is that Evidence Analyst R104 has now implemented the one-time Revisit ledger bootstrap across all 34 terminal current objects while keeping every old candidate terminal and rewriting no historical outcome. The bootstrap distribution is deliberately non-uniform: 1 strong closure, 19 dormant/revisitable, 14 deferred pending independent re-identification, and 0 currently triggered. This materially reduces the prior structural false-negative risk without producing zombie inflation.

The implementation is not yet fully calibrated end-to-end. Most legacy rows derive `closure_reason` and `what_would_change_our_mind` from coarse historical Funnel classes in R49 rather than candidate-specific primary closure records. Those entries are conservative admission constraints rather than claimed scientific triggers, so this is not historical evidence reinterpretation; however, trigger provenance needs stronger per-candidate traceability before the first live Revisit activation. There is also no live REVISIT_FORGE_TEST or REVISIT_CANONICALIZE case yet, and the dedicated Theory/Revisit path is not initialized/persisted. Therefore actual independent-trigger routing remains insufficiently observed.

H7 also moved materially: the unchanged R5 science passed a fresh NON_RESULT protected-sidecar readiness attempt, and R104 grants one conditional FORMAL authority subject to exact revalidation and untouched H7 STARTED/preserve namespaces. No H7 identity or START exists yet. This makes PASS concretely reachable without lowering evidence standards while leaving the actual RESULT_EXPOSED -> CONSUMED_ONE_WAY transition unobserved.

Independent repository checks confirm stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, authoritative evidence tags remain exactly five, and H7 `control/h7*` and `preserve/h7*` namespaces are empty. No terminal current object has been returned to ACTIVE. Candidate #35's immediate post-outcome natural-history Forge surface remains deferred and zero-credit.

## Authority reconstruction

Prior methodology history: R95, read before current reconstruction, classified the programme `MIXED_CALIBRATION` because Revisit/resurrection policy existed but no durable ledger/trigger routing did.

Designated Control history: R46 predates Analyst R104 and is used as governance history only. It had already required conservative bootstrap and prohibited old-ID reopening.

Designated canonical gate: Analyst R104 (`EVA-20260924T031000+0900-R104-H7-GREEN-REVISIT-BOOTSTRAP`) is the newest canonical scientific classification. It reports 35 candidates, 34 terminal current objects, H7 active/queued under one conditional FORMAL authority, development phases OPEN=1 / RESULT_EXPOSED=34 / CONSUMED_ONE_WAY=0, and Revisit bootstrap coverage 34/34.

Theory/Revisit/Forge: no dedicated Theory/Revisit durable proposal stream is currently present. Fast Forge has no newly admitted object; Candidate #35's rescue-adjacent proposal remains deferred, zero-credit, and cannot count as an independent Revisit trigger.

## Development iteration calibration

Development-phase semantics are currently consistent. H7 remains `RESULT_EXPOSED_DEVELOPMENT` on unchanged R5 science despite green readiness and FORMAL authorization; readiness is non-result plumbing, not a reset to OPEN. Candidate #35 remains result-exposed and terminal. No same-object science-affecting repair is authorized after exposure.

Cycle 3 remains a reassessment point rather than a hard terminal cap. No current decision relies on numeric cycle count alone. Science-invariant vs science-affecting separation is respected on the H7 path: only authority/control metadata repin and exact readiness plumbing are permitted before the frozen FORMAL contract.

Development observations retain zero independent confirmatory credit. Candidate #35 development/Forge observations remain noncanonical and zero-credit.

## PRE_FORMAL / FORMAL calibration

PRE_FORMAL remains development rather than a hidden second FORMAL gate. H7 READY now means the next one-way test is well-defined and conditionally executable; it does not mean H7 has already passed comparator/falsifier requirements by development observation.

FORMAL integrity is unchanged. R104 requires exact source/protocol/package/runtime/input/component/scorer/preserver/workflow binding, untouched STARTED/preserve namespaces, one fresh identity, raw-before-target-read/score, and no same-identity retry. Independent checks show no H7 STARTED/control or preserve refs yet. The live transition into `CONSUMED_ONE_WAY` is still unobserved and remains an evidence gap for methodology auditing, not a reason to weaken or delay the gate.

## Revisit / resurrection calibration

### Orthogonality and terminal immutability

Implemented correctly in current state. The ledger is metadata alongside terminal_state; all 34 legacy objects remain terminal. No old candidate ID is reactivated and no historical PASS/FAIL is rewritten.

### Bootstrap coverage and conservatism

Coverage is complete: 34/34 terminal current objects are classified. The distribution avoids the two obvious bootstrap pathologies: it does not default everything to CLOSED_STRONG and it does not trigger any resurrection. Candidate #34 alone is strongly closed using preserved raw evidence plus independent reduction audit; Candidate #35 is deferred pending independent re-identification and explicitly blocks its immediate post-outcome Forge idea.

The main residual weakness is historical specificity. For legacy rows 1-31, many closure entries cite the R49 Funnel snapshot and use closure-class templates such as SYSTEM-current-contract-closed, prior prospective REJECT, method-limited, contract-ambiguous, or mechanism-unresolved. Their `what_would_change_our_mind` values are likewise broad class-level conditions. This is conservative enough for bootstrap because no row is triggered and each condition still requires independent new information plus a fresh question, but it is not yet strong provenance for deciding that a future concrete event is genuinely independent and material for that particular candidate. Before any row changes to triggered, the trigger decision should cite candidate-specific historical closure evidence or explicitly state that the old history is too coarse and require independent re-identification.

### False-negative direction

Prior forgotten-line risk is reduced from structural/high to moderate/watch. Nineteen terminal lines are explicitly dormant/revisitable and fourteen are visible for independent re-identification instead of disappearing. However, trigger ingestion has not been tested on a genuine new independent event and the dedicated Theory/Revisit stream is absent, so the programme cannot yet demonstrate end-to-end rediscovery sensitivity.

### False-positive / rescue direction

Current behavior is strong. There are zero triggered rows, zero Revisit successors, zero Revisit Forge probes, and zero old-ID reopenings. Candidate #35 remains the key anti-rescue control: its immediate successor idea was generated after exposed outcome on the same family and is explicitly not an independent trigger.

### REVISIT_FORGE_TEST and REVISIT_CANONICALIZE

No live case exists for either path, so both remain `INSUFFICIENT_EVIDENCE`. Prospectively, a Forge test must attack the NEW trigger cheaply rather than rerun/retune the old object. Canonicalization must leave the old object terminal, create a fresh ID and fresh prospective reduction/comparator/falsifier contract, preserve informative negative outcomes, and grant zero inherited confirmatory credit to old/Forge/Theory/Revisit observations.

## Funnel / Theory / Forge / mechanism supply

Claim ceilings remain enforced. Candidate #35 is still SYSTEM and cannot be uplifted on the same object. Fast Forge remains noncanonical/zero-credit and has no admission. Theory/Revisit stream absence is an observability limitation, not evidence that no future trigger exists.

Mechanism supply is improved but fragile: H7 is now one effectively executable MECHANISM under conditional one-way authority; there is still no independent backup executable MECHANISM. This is a throughput risk, not justification for manufacturing a successor or weakening standards.

PASS is realistically reachable without evidence relaxation because H7 now has a concrete exact-binding path to one fresh FORMAL identity. No PASS is inferred from readiness itself.

## Gate classifications

- Hard integrity floor: `KEEP`
- Development-phase monotonicity and current handling: `KEEP`
- Cycle-3 mandatory reassessment: `KEEP`
- Cycle-3 automatic hard cap: `RELAX`
- Science-invariant vs science-affecting separation: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL as genuine development: `KEEP`
- Hidden second FORMAL gate: `KEEP`
- Fresh FORMAL one-way transition: `INSUFFICIENT_EVIDENCE`
- Terminal current object never reactivated: `KEEP`
- Revisit axis orthogonal to terminal state: `KEEP`
- Revisit bootstrap coverage: `KEEP`
- Revisit bootstrap conservatism: `KEEP`
- Revisit bootstrap historical specificity / trigger provenance: `CLARIFY`
- Revisit independent-trigger detection end-to-end: `INSUFFICIENT_EVIDENCE`
- Revisit rescue-laundering prevention: `KEEP`
- Revisit fresh-candidate requirement / zero inherited credit: `KEEP`
- REVISIT_FORGE_TEST new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- REVISIT_CANONICALIZE full gate: `INSUFFICIENT_EVIDENCE`
- Fast Forge/canonical separation: `KEEP`
- Theory/Revisit/canonical separation: `CLARIFY`
- Claim ceiling enforcement: `KEEP`
- Mechanism-supply health: `CLARIFY`
- READY vs executable/FORMAL distinction: `KEEP`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development phases consistent end-to-end? Current live objects: yes. Fresh one-way transition itself is not yet observed.
2. Cycle 3 mistaken for hard cap? No.
3. Science-invariant vs science-affecting distinguished? Yes on current H7 and terminal paths.
4. Development observations kept out of independent evidence credit? Yes.
5. FORMAL one-way integrity unchanged? Yes; no new H7 identity/START exists yet.
6. Legitimate fresh SYSTEM->MECHANISM successors suppressed/manufactured? No manufacture observed; no independent trigger currently supports one.
7. PRE_FORMAL genuine development? Yes.
8. Terminal semantics calibrated? Yes; 34 terminal objects remain terminal.
9. Revisit catches genuinely changed conditions? Ledger coverage now exists, but no genuine trigger has traversed the path; end-to-end evidence insufficient.
10. Revisit avoids rescue laundering/zombie inflation? Yes in current observations, especially Candidate #35.
11. REVISIT_FORGE_TEST tests new trigger rather than old failure? No live case; insufficient evidence.
12. Bootstrap coverage complete and conservative? Coverage yes 34/34; conservatism yes at status/admission level, with historical-specificity clarification required before live triggering.
13. PASS realistically reachable without weakening standards? Yes; H7 has one conditional exact-binding FORMAL path.

## Risks

False-positive/zombie inflation: low current, moderate watch once triggers begin flowing because broad bootstrap trigger templates require candidate-specific provenance at activation.

False-negative/forgotten valuable lines: moderate/watch, materially improved from R95 because all terminal lines are now visible in the ledger; end-to-end trigger sensitivity remains untested.

Moving-goalpost/rescue: low current. Candidate #35 immediate-successor deferral remains a strong negative control.

Over-terminalization: moderate/watch rather than structural/high. The ledger removes silent forgetting but cannot yet prove it will recognize a genuine independent trigger.

## Prospective recommendations

1. Keep all old terminal IDs terminal forever and preserve current zero-credit rules.
2. Before any ledger row becomes `REVISIT_TRIGGERED`, bind the new information to candidate-specific historical closure evidence, not only a generic R49 closure class.
3. Treat broad `what_would_change_our_mind` bootstrap text as admission scaffolding, not proof that a concrete trigger is independent or material.
4. When the first genuine trigger appears, persist its independent source, why it changes the old closure boundary, and why the new question is distinct before any Forge or canonical action.
5. Use REVISIT_FORGE_TEST only to falsify that new trigger cheaply; do not rerun/retune the old experiment.
6. Keep REVISIT_CANONICALIZE fresh-ID/fresh-contract/zero-inherited-credit only.
7. Keep H7 FORMAL exact-binding one-way rules unchanged; green readiness is not scientific evidence.

## Utility request

`NONE`. No bounded Utility proposal is needed for this calibration finding.

## Hard-floor confirmation

Confirmed. This audit dispatched no experiment, consumed no identity, mutated no research/evidence/formal/sealed/freeze/immutable/scientific-preserve ref, merged no PR, changed no scheduler or scientific criterion, reran/retuned/rescored no consumed FORMAL identity, reopened no terminal object, and rewrote no historical PASS/FAIL. Persistence is limited to the designated methodology-calibration audit latest/state/history files.

## Confidence

`HIGH` (`0.97`).

## Questions for Control / Analyst

- Before the first live Revisit trigger, require candidate-specific closure provenance in addition to the coarse R49 Funnel class.
- Preserve Candidate #35's post-outcome Forge proposal as rescue-adjacent, not as independent trigger support.
- Expose the first genuine Revisit trigger -> decision -> optional Forge test/canonicalization chain end-to-end so Methodology can audit it.
- Keep H7 green-readiness authority distinct from actual one-way identity consumption and evidence.
