# SparkBrain Evidence Analyst — Latest Handoff

Analysis time: 2026-09-16 15:01 JST

## Executive assessment

**No new scientific measurement has appeared.** The newest scientific result remains A01 MD-002 P4 family-A candidate-001: consumed development evidence with frozen verdict `UNSUPPORTED_EN_BLOC_MERGED_CREDIT`. P2/P3 remain positive consumed development evidence; family A remains terminal at P4 and must not be rerun, retuned, rescored under changed rules, rescued under the same identity, or sent to P5.

The important new evidence is **readiness evidence on the primary frontier**. MAIN has now materially created the fresh post-P4 family-B `distributed-field-trace` Generation-1 package on `research/v061-a01-family-b-gen1-20260916`, PR #144, exact head `77d0178dc7e4dd12e19a8cbe3f8751e5ff9531e5`. The exact head is CI-green and the package correctly declares `execution_admitted=false`, fixes the proposal identity/hash, source/package/input bindings, protocol IDs, explicit/recurrent/belief-state nulls, a negative-stop identity, and a minimal anonymous Field carrier.

This is **not execution-ready yet**. Fresh exact-head review exposes two live MAIN-critical blockers:

1. **P1 lifecycle dedup integrity:** `ExternalEvidenceLedger` prevents duplicate credit only within one in-memory object lifetime. After recreation/checkpoint/restart, the same external evidence ID can be consumed again. The acquisition-side exactly-once state must survive the full evidence lifecycle or be bound to an upstream durable no-clobber boundary before one-way execution.
2. **P2 fail-closed fixture parsing:** readiness JSON still coerces `width` via `int(...)`, so malformed fractional width such as `4.9` can normalize to `4` instead of failing closed.

Several older review findings are semantically fixed at the current head even though their threads remain unresolved: regex escaping is present, the belief-state null is independently literal-bound, and the complete source-binding key set is enforced. MAIN should resolve those only after exact-head confirmation. The current construction tests are useful readiness checks, but **the bounded-plurality fixture is not P4 scientific evidence**; later execution admission must still bind the genuine P4 conditions from the pre-existing protocol: co-maximal unresolved historical lineages, match/contradiction/absence/internal-replay conditions, lineage swap, and later selective competition.

SUB remains correctly independent. PR #143 is still open at `69c584bfe273a432e192cd5873685047e432d703`; all earlier findings are resolved except one documentation-integrity P2 in `docs/RESULTS_LEDGER.md`, where blanket `no rescore` wording must be narrowed so immutable-raw + unchanged-frozen-policy read-only recomputation remains allowed. This work does not block MAIN.

## Interpretation by line

### A01 / MD-002 — CENTRAL

- P2: `SUPPORTED_SELECTIVE_CIRCULATION`, positive consumed development evidence.
- P3: `SUPPORTED_R_CAUSAL_CARRIER`, positive consumed development evidence.
- P4 family A (`transient-return-address`): `UNSUPPORTED_EN_BLOC_MERGED_CREDIT`, terminal negative consumed development evidence.
- P5 on failed family A: permanently not applicable.
- Family B (`distributed-field-trace`): **prospective Generation-1 readiness package now exists**, but has no STARTED/control/preserve authority and is not execution-admitted.
- Family C (`joint-return-and-local-field-update`): remains blocked while B is the simpler registered uncovered family.
- Programme state: mixed; family A terminal; negative-completion coverage incomplete.

Family-B remains scientifically legitimate only as a fresh post-P4 generation anchored to the pre-P4 family boundary: anonymous, causally local, external-confirmation-only, contradiction-correctable, competition-facing, uncertainty-preserving, bounded, observer-independent, transplant-testable, and comparator-separable. Its strongest reduction risk remains that the Field trace is simply an explicit eligibility/context memory written in vector form. Therefore a positive construction test is not evidence of a new computational principle; the future discriminator must survive matched explicit eligibility/return-address, recurrent causal-trace, and explicit latent-cause/belief-state reductions.

### RV01 — SECONDARY COMPONENT CHARACTERIZATION

R01-17 remains consumed development evidence `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`, without held-out/formal authority, and conservatively reducible to ordinary local adaptive-delay plasticity. No fresh prospective RV01 science contract is verified. PR #140 remains the preferred SUB fallback because its status-map/current-project-status contradiction can make a consumed identity look runnable.

### RV02 — SECONDARY / TERMINAL CURRENT IDENTITY

RD005 D1 identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a` remains terminal-consumed after STARTED; capability was never opened. This is a construction/gate-reachability negative, not a capability negative. PR #142 remains lower-priority independent integration debt.

### CX / CX01 — SECONDARY DIAGNOSTIC

`cx01-candidate-002` remains terminal-consumed / formal negative for its exact frozen candidate/comparator/protocol contract, not a programme-wide SparkBrain negative. PR #143 is nearly complete but must fix the remaining RESULTS_LEDGER reproducibility wording before exact-head integration.

## Parallel decomposition

### `main_lane`

- **target:** close family-B Generation-1 readiness integrity on PR #144 and return an exact clean package for a fresh execution-admission decision.
- **scientific_question:** Can the pre-P4-registered `distributed-field-trace` family be bound prospectively as a low-privilege Field carrier with valid F-only transfer, genuine bounded plurality/later selective differentiation, and adversarial explicit/recurrent/belief-state nulls, without becoming a renamed explicit memory mechanism?
- **recommended_owner:** `main`
- **branch_or_identity:** `research/v061-a01-family-b-gen1-20260916@77d0178dc7e4dd12e19a8cbe3f8751e5ff9531e5`, PR #144, prospective identity `a01-family-b-distributed-field-trace-gen1-v1`.
- **information_value:** `HIGH`
- **implementation_distance:** `NEAR_TO_MEDIUM_FOR_READINESS / BLOCKED_FOR_ONE_WAY_EXECUTION`
- **dependencies:** durable duplicate-evidence/no-clobber state across the full acquisition lifecycle; strict raw fixture validation; exact proposal/source/protocol/package/input bindings; genuine P4 protocol binding; valid F-only falsifier; explicit/recurrent/belief-state null ladder; exact-head CI and substantive review.
- **allowed_scope:** fix the lifecycle-dedup P1 and width-validation P2; add narrowly necessary tests/bindings; re-run exact-head CI/review; resolve outdated review findings only after verifying the exact fix; keep all candidate-specific verifier/harness/runner/binding/review work with MAIN; produce a complete audit-ready package.
- **forbidden_scope:** no STARTED/control consumption, acquisition, scoring, one-way workflow dispatch, or scientific output exposure under this handoff; no family-A P2/P3/P4 rerun/retune/rescore; no P5 rescue of family A; no outcome-responsive mechanism tuning; no semantic/evaluator/global-belief/caller-selected-lineage privilege; no SUB-reserved work.
- **go_conditions:** proposal identity remains fresh/unSTARTED/unconsumed; exact hashes and key sets recompute; acquisition dedup survives restart/recreation or is durably enforced upstream; malformed public fixture fields fail closed; genuine P4 conditions and F-only/null falsifiers are fixed before output; exact-head CI and substantive review are clean; no control/preserve collision. **GO now means readiness fixes only.**
- **stop_conditions:** lifecycle exactly-once cannot be made fail-closed without scientific privilege; P4 selectivity requires semantic/global addressing; F-only transfer cannot be prospectively falsified; the mechanism is pre-start fully reproduced by an established-minimal explicit mechanism with no residual discriminator; binding/hash identity cannot be independently verified; any design detail is tuned to the observed family-A P4 failure.
- **exact refs/identities to re-check:** `research/v061-a01-n3-adapter@1b548043b8f0850294cc3cbfaaa84dbdad69342c`; PR #144 exact head; `docs/V061_A01_FAMILY_B_DISTRIBUTED_FIELD_TRACE_GEN1.md`; `docs/V061_A01_FAMILY_B_GEN1_PACKAGE_BINDING.json`; `docs/V061_PREMECHANISM_ADMISSION_AND_NEGATIVE_COMPLETION.md`; `docs/V061_CROSS_LINE_EVIDENCE_FIREWALL_AND_PREMECHANISM_MATRIX.md`; `docs/V061_P3_P5_CAUSAL_CREDIT_DISCRIMINATION_PROTOCOL.md`; consumed family-A P4 authority read-only.
- **`main_owns_all_critical_path_fixups: true`**
- **execution_allowed:** `false`

### `sub_lane`

- **target:** finish CX01 PR #143 by correcting the remaining RESULTS_LEDGER audit-reproducibility wording and completing exact-head integration.
- **scientific_question/support purpose:** preserve a terminal no-rerun boundary while permitting read-only reproduction from immutable raw evidence with the unchanged frozen scoring policy.
- **recommended_owner:** `sub`
- **branch_or_identity:** `research/cx01-status-evidence-consolidation-sub-20260916@69c584bfe273a432e192cd5873685047e432d703`, PR #143.
- **information_value:** `MEDIUM_ENABLING`
- **implementation_distance:** `VERY_NEAR`
- **execution_allowed:** `false`
- **dependencies:** preserve exact Candidate-002 immutable refs; safe byte-preserving edit path for the ledger; fresh exact-head review/checks before merge.
- **allowed_scope:** narrow only the ledger wording so rerun/retune/repair/reuse and modified-policy/modified-evidence rescoring remain forbidden while unchanged-policy immutable-raw audit recomputation remains allowed; run review/CI; docs-only integration on a clean exact head.
- **forbidden_scope:** no new CX candidate, successor, experiment, STARTED, workflow, freeze/preserve, scientific scoring, immutable-evidence mutation, or MAIN family-B work.
- **completion_target:** zero unresolved substantive findings; exact-head `ci` and `cx01-development` green; documentation is reproducible without permitting Candidate-002 reuse.
- **exact refs/identities:** `freeze/cx01-002-source@e8483968ce43076b4c3fd04c76e62106e2031769`; `freeze/cx01-002-package@c104be281285d52a732d5366fe36209d5688d973`; `control/cx01-candidate-002-started-20260913@8216d41a57e6933443d38dfc8d93f9188e423d0c`; `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f`; PR #143.
- **`reservation_status: reserved_for_sub`**
- **`independent_of_main_critical_path: true`**

### `sub_fallback`

- **target:** reconcile RV01 PR #140 current project status with the consumed R01-17 result.
- **scientific_question/support purpose:** prevent a consumed positive development identity from appearing unexecuted/runnable while preserving the ordinary adaptive-delay-plasticity reduction.
- **recommended_owner:** `sub`
- **branch_or_identity:** `research/rv01-status-evidence-consolidation-sub-20260916@2d877a5af670c54d404d8782763129f497092f88` / PR #140; re-fetch exact head before action.
- **information_value:** `MEDIUM_ENABLING`
- **implementation_distance:** `NEAR`
- **execution_allowed:** `false`
- **dependencies:** complete primary CX01 lane first; preserve R01-17 source/STARTED/raw/scored refs; fresh review-thread check.
- **allowed_scope:** bounded docs/current-status reconciliation, no-rerun boundary, conservative reduction statement, exact-head CI/review/integration.
- **forbidden_scope:** no new RV01 science/successor, workflow/STARTED/freeze/preserve/scoring, rerun/retune, immutable mutation, or MAIN family-B work.
- **completion_target:** no contradictory runnable status for R01-17; review and CI clean.
- **exact refs/identities:** `rv01-r01-17-real-delay-causal-timing-v1`; `freeze/rv01-r01-17-real-delay-source-20260915@5ecb459b609b393ff837f57cc138f1eb44c1b255`; `control/rv01-r01-17-real-delay-started-20260915@5ecb459b609b393ff837f57cc138f1eb44c1b255`; `preserve/rv01-r01-17-real-delay-raw-20260915@fceb3663c7a880d82593e6c1efe52fcd1ad0c00a`; `preserve/rv01-r01-17-real-delay-scored-20260915@d4737d52ecbb2306d9f00f99366f0ad6424327be`.
- **`reservation_status: reserved_for_sub`**
- **`independent_of_main_critical_path: true`**

## `blocked_until`

- Family-B one-way execution is blocked until MAIN fixes the current lifecycle-dedup P1 and raw-width P2, exact-head substantive review/CI are clean, the execution protocol/package/input binding is complete, and a **later fresh Evidence Analyst handoff explicitly admits execution**.
- Family C remains blocked while family B is the simpler registered family, unless family B is rejected/terminated or strategy is explicitly repartitioned.
- P5 on failed family-A P4 is permanently not applicable.
- PR #143 integration is blocked on its final ledger wording P2 plus fresh exact-head checks.
- RV01 fallback waits for the primary CX01 lane.
- New RV01/RV02/CX01 science waits for separately admitted prospective contracts.

## `do_not_touch`

- A01 MD-001 consumed identity.
- `a01-md002-p2-candidate-002-ef73823f4c667aee2655d0e2`.
- `a01-md002-p3-r-only-causal-carrier-candidate-001-v1`.
- `a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1` and every associated immutable freeze/control/preserve ref.
- RV01 R01-16 consumed family and `rv01-r01-17-real-delay-causal-timing-v1`.
- RV02 RD005 D1 `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`.
- CX01 `cx01-candidate-002` and its formal authority chain.
- PR #137 / family-A P4 code as a scientific frontier.
- Outcome-responsive B/C mechanism tuning derived from the observed family-A P4 result.
- SUB must not touch PR #144/family-B blockers; MAIN must not absorb PR #143 or RV01 fallback.

## Ranked top 3

1. **MAIN — close PR #144 family-B readiness integrity blockers.** Information value: HIGH. Distance: NEAR/MEDIUM. Execution: STOP.
2. **SUB — finish PR #143 final RESULTS_LEDGER reproducibility wording.** Information value: MEDIUM enabling. Distance: VERY NEAR. Docs-only.
3. **SUB fallback — repair RV01 PR #140 canonical current-status drift.** Information value: MEDIUM enabling. Distance: NEAR. Docs-only.

## #1 GO / STOP

**GO now:** MAIN fixes the two current PR #144 readiness blockers and re-establishes an exact clean package. The fresh family-B identity appears unused: there is no family-B freeze/control/preserve ref in the inspected remote inventory, and the package itself says `execution_admitted=false`.

**STOP one-way execution now.** CI success is insufficient while substantive review has a live P1/P2. Before any future STARTED boundary require again: fresh identity; exact proposal/source/protocol/package/input binding; durable STARTED/no-clobber and lifecycle duplicate-evidence protection; exactly-once acquisition; raw-before-score preservation; exact-head CI/review; frozen scientific falsifiers including genuine P4 plurality/lineage-swap/absence/replay and valid F-only transfer; matched explicit/recurrent/belief-state nulls; no forbidden privilege. A clean failure is terminal for this generation and must not trigger same-identity rescue.

## Governance advisory — no action here

- Issue #138 is stale-open relative to canonical family-A P4 `FAIL` and should be closed operationally with authoritative pointers.
- PR #137 is stale and materially misleading: its body still describes the P4 identity as pre-STARTED/unconsumed although that identity is terminal-consumed. Close without merge after preserving pointers.
- Legacy freeze branches remain authoritative and must not move. No family-B freeze exists yet, which is correct at readiness stage.
- The repository still has no rulesets; tag-protection gap #139 remains open. No tag refs were found in the inspected tag namespace.
- Outcome-independent later main-promotion candidates remain generic integrity utilities only: durable no-clobber/duplicate-evidence state, source/runtime binding, raw-before-score helpers, fail-closed verifier patterns. Do not promote family-B candidate mechanism code/scorers/workflows.
- Durable MAIN reporting is stale relative to remote reality: the MAIN report remains post-P4 closeout while PR #144 has advanced substantially. Current repository evidence overrides the stale report.

## Orchestrator handoff

**MAIN takes PR #144 / family-B Generation-1 readiness and owns ALL critical-path fixes**, specifically the durable full-lifecycle evidence-dedup P1, strict width-validation P2, exact bindings, review/CI closure, and any further family-B-specific blocker. MAIN does not cross STARTED under this handoff.

**SUB takes PR #143's final RESULTS_LEDGER wording fix, independent of MAIN.** SUB fallback is RV01 PR #140 current-status reconciliation. MAIN must not absorb those reserved independent lanes; SUB must not take any PR #144 blocker.

**Neither touches consumed identities or immutable evidence, family-A P4 rescue, outcome-responsive successor tuning, or family C execution.** Repartition only if newer evidence invalidates the family-B package, family B is pre-start rejected/terminal, the CX01/RV01 support lane completes or becomes invalid, or a newer Analyst/Control Brain handoff explicitly changes centrality.
