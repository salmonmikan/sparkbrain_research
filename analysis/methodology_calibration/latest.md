# SparkBrain Methodology Calibration Audit — 2026-09-20 07:21 JST

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`MIXED_CALIBRATION`** — unchanged, but the previous handoff-fidelity gap is now prospectively closed at the methodology/doctrine level. The remaining material weakness is narrower: validity of decision-relevant machine-fact extraction before an artifact is produced.

The substantive scientific admission, novelty, reduction, comparator, STOP/reframe, and FORMAL evidence bars remain broadly well calibrated. No new evidence supports making the scientific bar globally stricter or looser.

## What changed since the 06:20 audit

### 1. Control prospectively adopted the validated handoff-binding guard

Control Brain `36a41bb720c051ee6d4563d7ecb6b720a8fc2c2d` explicitly adopted the already-validated handoff-binding design for future outcome-bearing lower-funnel closures. Before successor decisions depend on a result, Control now requires machine-bound checks of provenance, canonical machine-summary digest, exact mapped classification, and narrated decision-relevant fields.

This closes the prior *methodology-definition* gap around artifact-to-handoff fidelity. It does not rewrite historical Temporal/Top-k records and does not grant the prototype scientific execution authority. Therefore:

- generic handoff-binding requirement: `KEEP`;
- automated/live tooling coverage: `CLARIFY` rather than a new scientific gate — one future closure should demonstrate end-to-end use, but lack of scheduler wiring is an implementation issue, not a reason to tighten novelty/admission criteria.

### 2. A second independent brittle-extractor false negative appeared before outcome — and the repair boundary behaved correctly

The Refractory Architecture object failed preflight before any outcome-bearing job ran because the prospectively bound semantic comment was stored as one sentence in the contract but split across two `#` lines in the exact source. The harness used a literal representation-sensitive presence check.

Evidence Analyst authorized only a pre-outcome, science-invariant representation repair: normalize consecutive full-line comments against the same exact source blob and same already-bound semantic comment. Contract meaning, source bindings, input family, comparator, currents, timing, probe, tolerance, observables, and terminal mapping remained frozen.

The actual repair commit `4589192d927e40cf7a05cf8a94207efb42ebbc65` modifies only `analysis/architecture/refractory_current_accounting_cycle1_20260920.py`: it adds comment-block normalization and replaces the literal raw-source membership test. On that exact head, ordinary CI `35472786733` and Architecture workflow `35472786687` both completed successfully, and artifact `10593866036` was produced with archive digest `sha256:b4dfbf04ab2f1dbb69fcee3833890ce6ad30d85a0c095a4699cde356c43e9115`.

This is calibration evidence for a useful boundary: pre-outcome science-invariant representation/mechanical repair under unchanged prospective scientific bindings is legitimate; outcome-responsive semantic/protocol repair remains prohibited. `moving_goalposts` therefore remains `LOW`.

It also strengthens the case that decision-relevant machine-fact extraction is the remaining weak layer. Suppression showed a post-outcome static-fact false negative; Refractory independently showed a pre-outcome representation false negative.

### 3. The suppression extractor audit is now accepted and assigned

Control accepted `EVA-20260920-0502-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY` and issued `CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY` for one bounded read-only run. It may compare only the completed suppression artifact/contract/harness/workflow metadata with exact bound source, using deterministic source/AST/structural checks. It may not rerun, dynamically probe, repair, rescore, relabel `AMBIGUOUS_CONTRACT`, choose a successor, or touch TEST/FORMAL/immutable refs.

This is the highest-value unresolved methodology diagnostic. No duplicate Methodology Utility request is warranted.

### 4. Claim-type separation continues to work

SUB's fresh `OUTCOME_CREDIT_SLOT_OVERWRITE_DISCOVERY_CYCLE1` shows delayed outcomes can be redirected to the latest mutable pending activation/action slot, but the observation is fully reduced to ordinary single-slot bookkeeping and current repository callers use immediate outcome ordering. Evidence Analyst nonetheless admitted one queued fresh Architecture/API attribution question, with a prospective first question of whether delayed/interleaved outcomes are even supported. If the canonical contract is immediate-only, the line reduces to an engineering/API note instead of manufacturing a dynamic novelty experiment.

This is the desired distinction between research-worthiness and new-principle novelty.

## Authoritative repository/evidence state independently re-fetched

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- annotated `evidence/*` tags: `5`
- tag-based `formal/*`: `0`
- tag-based `sealed/*`: `0`
- tag-based `freeze/*`: `0`
- legacy `freeze/*` branches: `13`
- active Refractory Architecture head: `4589192d927e40cf7a05cf8a94207efb42ebbc65`
- Refractory ordinary CI `35472786733`: completed / success / exact head
- Refractory Architecture workflow `35472786687`: completed / success / exact head
- Refractory artifact: `10593866036`, archive digest `sha256:b4dfbf04ab2f1dbb69fcee3833890ce6ad30d85a0c095a4699cde356c43e9115`
- fresh SUB delayed-outcome Discovery head: `83eb00212eb9c877e8217c44dfb35a5563f04626`
- PR `#148`: open/unmerged
- PR `#149`: open/unmerged

No new FORMAL evidence or fresh FORMAL identity was observed. At the latest durable MAIN relay checkpoint, the just-completed Refractory workflow had not yet been reconciled into a machine-verified terminal handoff, so this audit does not infer or score its scientific result from workflow success alone.

## Gate calibration

| Gate / rule | Classification | Current finding |
| --- | --- | --- |
| No rerun/retune/rescore; immutable evidence; raw-before-score / preserve-before-read | `KEEP` | Still the hard integrity floor. |
| Prospective protocol / exact source-runtime-input binding | `KEEP` | Necessary and functioning. |
| Pre-outcome science-invariant representation/mechanical repair under unchanged bindings | `KEEP` | Refractory demonstrates a legitimate repair boundary without outcome-responsive redesign. |
| Any post-outcome semantic/protocol repair of the same consumed object | `KEEP` | Remains prohibited. |
| Positive signal before strong mechanistic claims | `KEEP` | No reason to change. |
| Equal-privilege comparator/resource matching | `KEEP` | No current evidence of systematic overmatching or undermatching. |
| Comparator semantics matched to the actual claim | `CLARIFY` | Refractory policy comparators should answer the declared API/model claim; do not impose a biological conductance comparator unless a biological claim independently appears. |
| New-computational-principle novelty bar | `KEEP` | Appropriate for the strongest claim type. |
| Applying that novelty bar to architecture/system/testbed value | `SPLIT_BY_CLAIM_TYPE` | Current lower-funnel handling remains healthy. |
| `NO_HIGH_VALUE_FORMAL_OBJECT => programme-wide HOLD` | `RELAX` | Productive Discovery/Architecture work continues while FORMAL remains empty. |
| Fresh independently motivated object requirement | `KEEP` | Prevents rescue of consumed/exhausted lines. |
| Stop after each Architecture cycle for fresh Analyst review | `KEEP` | No automatic escalation. |
| Legacy Top-k sparse-stratum support gate | `TIGHTEN` | Historical local weakness remains. |
| Programme-wide replacement support/uncertainty threshold | `INSUFFICIENT_EVIDENCE` | Do not fit a universal rule to completed outcomes. |
| Ordinary-control-first Architecture reduction | `KEEP` | Continues to separate ordinary semantics from novelty. |
| Negative-evidence claim-boundary narrowing | `KEEP` | H5 remains narrow to its registered work metric. |
| Generic artifact-to-handoff binding requirement | `KEEP` | Prototype validated and Control prospectively adopted it. |
| Automated/live handoff-guard tooling coverage | `CLARIFY` | End-to-end demonstration is desirable, but tooling coverage is implementation, not an extra scientific admission hurdle. |
| Decision-relevant machine-fact extraction from source/runtime | `TIGHTEN` | Suppression plus Refractory give two distinct false-negative examples. |
| Literal/format-sensitive semantic detectors used as scientific machine facts | `TIGHTEN` | Prefer structural/AST/typed/invariant checks when practical. |
| Documentation/comment-presence facts versus executable semantic facts | `CLARIFY` | Bind documentation concordance separately unless the claim itself is about documented API contract. |
| Post-outcome invalid-diagnostic fail-closed handling | `KEEP` | Preserve artifact; block only dependent continuation; no silent repair. |
| Automatic PRE_FORMAL promotion after Architecture signal | `KEEP` | Must remain absent. |
| Local Architecture thresholds as FORMAL/novelty thresholds | `CLARIFY` | Keep local triage claim-local. |

## Mandatory calibration dimensions

- `gate_drift`: evidence-driven procedural maturation. The handoff guard progressed recommendation -> bounded validation -> prospective Control adoption. No scientific novelty threshold was raised and no completed result was redefined.
- `justification_trace`: strong. Temporal/Top-k justify handoff binding; suppression and now Refractory independently justify extractor-validity checks.
- `false_positive_control`: strong at the scientific gate level and improved procedurally by handoff adoption. Remaining risk is an internally consistent but semantically wrong machine fact.
- `false_negative_risk`: the main live risk. Brittle literal/format-sensitive detectors can block otherwise valid objects before measurement. The narrow pre-outcome repair rule appropriately mitigates this without permitting post-outcome rescue.
- `duplicate_guards`: none to merge. Provenance binding, semantic extractor validation, artifact-to-handoff binding, and fresh Analyst review protect different stages.
- `moving_goalposts`: `LOW`. The Refractory repair occurred before outcome visibility, changed only detector representation, preserved all scientific bindings, and re-ran on a new exact head. Historical outcomes remain untouched.
- `pass_reachability`: `REACHABLE_BUT_NARROW`.
- `comparator_calibration`: broadly appropriate. External literature supports explicitly naming refractory input/state policy rather than treating one policy as universal; comparator choice must follow claim type.
- `signal_before_reduction`: healthy. Architecture/API findings are characterized before stronger novelty language and are ordinarily reduced first.
- `claim_type_separation`: healthy across new-principle, mechanistic, architecture/system, engineering, and testbed claims.
- `research_worthiness_vs_novelty`: separated. Delayed-outcome attribution can merit one Architecture/API check despite low novelty.
- `external_calibration`: current refractory literature strengthens ordinary-reduction and claim-scope discipline; it does not justify changing the scientific admission threshold.
- `opportunity_cost`: additional global scientific strictness has lower expected information gain than completing the suppression extractor audit and demonstrating the adopted handoff binding on one real successor decision.

## PASS reachability

**`REACHABLE_BUT_NARROW`**. A realistic prospective path remains:

positive native signal -> fresh exact-bound object -> claim-local adequate support -> matched equal-privilege comparator for mechanistic claims -> survive ordinary implementation/dynamical reductions -> semantically valid machine-fact extraction -> faithful machine-bound handoff -> fixed intervention/falsifier -> one-way preserved FORMAL evidence.

The Refractory preflight episode is evidence that integrity checks need not make measurement unreachable: a representation-only pre-outcome blocker was narrowly repaired while scientific bindings stayed frozen, after which exact-head CI and the Architecture workflow completed successfully.

## Prospective recommendations

1. Keep the four-layer funnel, strict FORMAL novelty bar, comparator discipline, ordinary-reduction-first interpretation, and hard integrity floor unchanged.
2. Treat Control's prospective handoff-binding adoption as the current method. On the next outcome-bearing closure, demonstrate that a successor decision actually consumes the checked machine binding; do not add a second redundant guard merely for ceremony.
3. Complete the already-assigned suppression static-detector consistency audit. Do not repair or relabel the completed suppression terminal.
4. For future decision-relevant source/runtime facts, prospectively bind the validity method. Prefer AST/structural/typed checks or explicit invariants over syntax/format-sensitive literal matching where practical.
5. Separate documentation/comment concordance from executable semantic facts unless the study claim itself is explicitly about the documented API contract.
6. Permit only science-invariant pre-outcome mechanical/representation repair under unchanged bindings; once outcome-bearing data are visible, retain the no-silent-repair rule.
7. On a disputed machine fact, fail closed only for decisions that depend on it. Do not automatically reject the candidate, inflate novelty/support thresholds, or demand universal replication.
8. Preserve Architecture/system/engineering/testbed value even when computational-principle novelty fails.
9. Never retroactively rescore, relabel, rerun, invalidate, or upgrade consumed/frozen experiments because methodology safeguards improve.

## Utility request

No new Methodology Calibration Utility request created. `CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY` already targets the highest-value unresolved extractor-fidelity question and is currently assigned.

## Hard-integrity-floor confirmation

Confirmed unchanged: no rerun/retune/rescore of consumed identities; frozen/prospective protocols; raw-before-score; preserve-before-read; exact identity/source/package/runtime/input binding; immutable evidence; no evaluator/target leakage; no silent post-outcome repair.

## Bottom line

The current methodology remains **`MIXED_CALIBRATION`**, but the mixture is now narrow. Artifact-to-handoff fidelity has moved from an identified weakness to a validated and prospectively adopted requirement. The remaining material calibration weakness is upstream machine-fact extractor validity, where suppression and Refractory provide independent false-negative examples. Tighten that layer prospectively; do not tighten the scientific novelty/admission bar itself.