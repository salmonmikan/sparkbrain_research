# SparkBrain Methodology Calibration Audit — 2026-09-21 07:22 JST

schema_version: `2`  
generation_id: `METHCAL-20260921T072229+0900-R30-4A7D9C21`  
produced_at: `2026-09-21T07:22:29+09:00`  
producer_run_id: `methodology-calibration-auto-20260921T072229+0900-R30-4A7D9C21`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260921T062111+0900-R29-C5E1A7D2`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`WELL_CALIBRATED`** — unchanged.

The material update is that the first live qualitative theory-backward reframe requested by R29 actually executed and recovered a genuine prospectively typed MECHANISM question without weakening the quality floor. The four-check no-target episode `NTE-20260921-STABLEMAIN-H7UNRESOLVED-v1` is now canonically closed by a fresh mechanism selection rather than by quota-driven label inflation.

A second, smaller implementation finding is that the SUB producer proposed an invalid HOLD enum (`HOLD_MECHANISM_UNRESOLVED_REDUCTION`). Evidence Analyst correctly normalized it to canonical `HOLD_MECHANISM_UNRESOLVED`, so scientific disposition and completeness remain sound, but producer-side Funnel-v2.1 enum conformance should be clarified/enforced prospectively.

## Fresh independent reconstruction

Prior Methodology R29 was read first. Stable `main` was independently re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative refs remain `evidence/*=5`, `formal/*=0`, `sealed/*=0`, tag-based `freeze/*=0`.

Designated Control is `CTRL-20260921T065000+0900-R20-8E4C2A71@cae67ec0f8980e6125c578c3eb98d67e6da46a36`. Fresh designated Evidence Analyst is `EVA-20260921T065846+0900-R29-7B2C91E4@de3de2fcf0f21aa33ebfe417d210df1e96889a90`.

Fresh SUB `SUB-20260921T064900+0900-THEORY-ASMCAUSAL-7A4C91E2` created `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01`. Its prospective contract `eb5ae27f3ef7f8cca2bcc521e2c3f027a5ab6c42` fixed `claim_ceiling=MECHANISM`, one DEV seed/probe, target/comparator selection, an ordinary equal-cardinality activity-lesion reduction, terminal mapping, and a no-rescue rule before intervention outcome. The outcome-bearing commit is `1a571db21ff82001407f01cb2c5449f253bfd4e5`; final head `0c857a73cf34b58b737f686fd9af60769de3d306` only records the result and interpretation boundary. No same-object outcome-driven comparator redesign occurred.

The Discovery observation was selective on the fixed DEV probe, but the intended activity match was imperfect: target units each had one baseline spike while fixed nonmember comparators each had zero; topology/centrality reductions also remain unresolved. Evidence Analyst therefore closes the completed object as `HOLD / MECHANISM / preformal_eligible=false / HOLD_MECHANISM_UNRESOLVED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED / NOT_READY` and opens a fresh successor `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01` as `MECHANISM / preformal_eligible=true / ACTIVE / NOT_READY`.

Canonical funnel is now material candidates=`24`, MECHANISM=`12`, SYSTEM=`12`, classification completeness=`24/24`, Architecture active=`M1/S0`, PRE_FORMAL eligible=`1`, READY=`0`, viable executable MECHANISM=`1`. Rolling autonomous scientific selections are `SYSTEM / SYSTEM / MECHANISM = 1/3`. The historical four no-target checks remain outside candidate/conversion denominators and their episode is marked `CLOSED_BY_FRESH_MECHANISM_SELECTION_AFTER_QUALITATIVE_REFRAME`.

After Analyst review, MAIN prospectively opened only a non-intervention comparator-feasibility Architecture cycle on branch `research/main-v05-assembly-unit-causal-selectivity-matched-load-arch-20260921`, head `b2547429823be29a2547419c80c40fb2138dfdc9`. Its contract explicitly forbids suppression/intervention outcomes in this cycle, fixes activity/topology load signatures and sham/random controls prospectively, and states that `preformal_eligible=true` is in-principle eligibility while readiness remains `NOT_READY`; comparator feasibility alone is not scientific success and does not authorize PRE_FORMAL.

## Funnel v2.1 mandatory audit

1. `claim_ceiling` current-object semantics: **KEEP**. The fresh Discovery and fresh successor each receive their own prospective MECHANISM ceiling; no topic/prestige label behavior is observed.
2. completed SYSTEM→same-object MECHANISM upgrade: **KEEP**. None observed; the current mechanism successor is a fresh object.
3. `preformal_eligible` vs READY: **KEEP**, with stronger live evidence. The active successor is eligible=`true` and READY=`0` before any outcome-bearing continuation.
4. READY semantics: **KEEP**; `HIDDEN_SECOND_FORMAL_GATE=false`. MAIN explicitly says feasibility is not success and cannot itself authorize PRE_FORMAL. First READY→PRE_FORMAL remains **INSUFFICIENT_EVIDENCE**.
5. HOLD multidimensional model: **KEEP** canonically. The predecessor is terminal/not queued while the fresh successor is active. Producer enum conformance is separately **CLARIFY** because SUB emitted a noncanonical hold class that Analyst normalized.
6. MAIN MECHANISM priority / SYSTEM-priority exception: **KEEP**. A viable MECHANISM now exists and Analyst explicitly blocks the lower-value SYSTEM successor; genuine SYSTEM-over-comparable-MECHANISM exception count remains zero, so first genuine use is **INSUFFICIENT_EVIDENCE**.
7. `NO_COHERENT_MECHANISM_TARGET`: **KEEP**. The four-check episode was not an escape hatch; qualitative reframe found a new coherent mechanism family and closed the episode.
8. theory-backward selection quality: **KEEP**. The recovered object is intervention-based, falsifiable, and tied to an ordinary lesion reduction; it is not a relabeled SYSTEM question. Comparator weakness is surfaced rather than hidden.
9. SYSTEM architecture/testbed/reproducibility value: **KEEP**. SYSTEM work remains scientifically useful but is correctly deprioritized while the active comparable MECHANISM successor exists.
10. PRE_FORMAL/PASS reachability: **REACHABLE_BUT_NARROW**.
11. classification-completeness gating: **KEEP**. Canonical policy conclusions use Analyst-reviewed `24/24`; the active object is fully classified and no-target control events remain separate.
12. first READY→PRE_FORMAL empirical semantics: **INSUFFICIENT_EVIDENCE**.

## Material gate classifications

- hard integrity floor: `KEEP`
- prospective terminal/API semantic binding: `KEEP`
- producer API/source conformance preflight: `KEEP`
- pre-outcome science-invariant mechanical repair handling: `KEEP`
- outcome-exposed repair containment: `KEEP`
- current-object `claim_ceiling`: `KEEP`
- same-object SYSTEM→MECHANISM upgrade ban: `KEEP`
- fresh-successor discipline: `KEEP`
- `preformal_eligible` / READY separation: `KEEP`
- READY development-readiness semantics: `KEEP`
- first Analyst-authoritative READY→PRE_FORMAL transition: `INSUFFICIENT_EVIDENCE`
- HOLD multidimensional model / applicability semantics: `KEEP`
- **producer Funnel-v2.1 HOLD enum conformance: `CLARIFY`**
- classification-completeness gating: `KEEP`
- MAIN MECHANISM priority: `KEEP`
- prospective SYSTEM-priority exception: `KEEP`
- first genuine SYSTEM-priority exception use: `INSUFFICIENT_EVIDENCE`
- rolling one-in-three theory-backward supply: `KEEP`
- theory-backward quality floor: `KEEP`
- `NO_COHERENT_MECHANISM_TARGET` rule: `KEEP`
- repeated opportunity-local no-target use: `KEEP`
- no-target episode observability / stop-reframe semantics: `KEEP`
- **first live qualitative no-target-episode reframe execution: `KEEP`** (R29 `INSUFFICIENT_EVIDENCE` closed by fresh MECHANISM recovery)
- SYSTEM architecture/testbed/reproducibility value: `KEEP`
- general equal-privilege comparator / ordinary-reduction-first: `KEEP`
- signal-before-strong-claim: `KEEP`
- claim-type separation: `KEEP`
- research-worthiness vs novelty: `KEEP`
- external-validation competent-reference requirement for superiority/novelty claims: `TIGHTEN`
- relevant simple FSA/state-tracker reduction for applicable external-validation claims: `TIGHTEN`
- source/atomic-unit clustered inference when shared-source observations exist: `TIGHTEN`
- historical immutable-result interpretation ceiling: `KEEP`
- no universal numeric readiness/support threshold: `KEEP`
- legacy Top-k sparse-support weakness: `TIGHTEN`

## Calibration dimensions

`gate_drift`: low; one producer enum drift was normalized before canonical policy use.  
`justification_trace`: strong; the no-target episode has an explicit close reason and the fresh candidate has prospective contract→outcome commit→result lineage.  
`false_positive_control`: strong; a positive Discovery signal was not promoted because exact activity/topology reductions remain unresolved.  
`false_negative_risk`: reduced from R29; qualitative reframe successfully broadened discovery, though one recovered family is small-n and comparator feasibility is unresolved.  
`duplicate_guards`: none material.  
`moving_goalposts`: `LOW`; the completed Discovery object was closed and a fresh successor opened instead of repairing the comparator post outcome.  
`pass_reachability`: `REACHABLE_BUT_NARROW`.  
`comparator_calibration`: healthy and appropriately demanding prospectively; exact activity/topology matching is being tested before another intervention outcome.  
`signal_before_reduction`: healthy; the signal is recorded but reduction uncertainty blocks readiness.  
`claim_type_separation`: healthy.  
`research_worthiness_vs_novelty`: healthy; the reframe recovered a worthwhile mechanism test without calling the bounded positive signal novel/formal.  
`external_calibration`: unchanged; prior claim-type-specific tightenings remain prospective only.  
`opportunity_cost`: improved; persistent no-target scanning successfully transitioned into a different mechanism family, and a lower-value SYSTEM successor is currently deferred.  
`mechanism_supply_health`: `QUALITY_FLOOR_HEALTHY_REFRAME_RECOVERED_GENUINE_MECHANISM_SUPPLY_SMALL_N`.  
`funnel_observability`: `GOOD_24_OF_24_CANONICAL_EPISODE_CLOSED_ACTIVE_M1_ELIGIBLE1_READY0`.  
`preformal_gate_calibration`: `ELIGIBILITY_READINESS_SEPARATION_LIVE_ACTIVE_OBJECT_READY_TRANSITION_UNTESTED`.

## Remaining defects / watchpoints

The R29 live-reframe uncertainty is closed positively: the first qualitative reframe produced a distinct mechanism-level intervention question rather than another local rescan or SYSTEM relabel. The remaining new semantic defect is minor but real: producer-side hold enums are not fully conformant with the canonical Funnel-v2.1 vocabulary. Canonical Analyst normalization prevents metric corruption today, but prospective producer schema validation should reject or map unsupported enum values before handoff.

The main empirical watchpoint remains the first READY→PRE_FORMAL transition. A second watchpoint is comparator feasibility: exact activity/topology matching may be infeasible on the supported DEV surface. That must lead to HOLD/STOP, not threshold relaxation or outcome-informed matching. A third remains the first genuine SYSTEM-over-comparable-MECHANISM exception, still unobserved.

## Prospective recommendations

Keep scientific admission, novelty/reduction, comparator, PRE_FORMAL readiness, claim-type separation and hard-integrity floors unchanged. Keep the completed causal-selectivity Discovery object terminal; use only the fresh matched-load successor for comparator development.

Prospectively enforce the canonical HOLD enum set at producer handoff, while preserving orthogonal `hold_reason`, `terminal_state`, and `queue_state`. Do not reinterpret the historical producer string or rescore the object; the Analyst-normalized canonical record is sufficient.

For the active successor, complete only the already-bound non-intervention comparator-feasibility cycle. If exact matching is infeasible, HOLD/STOP. If feasible, return to fresh Analyst review before any suppression/intervention outcome. Do not let a positive feasibility result become READY or PRE_FORMAL success by itself.

Continue auditing the first READY→PRE_FORMAL transition and first genuine SYSTEM-over-comparable-MECHANISM execution.

## Utility request

None created. Live comparator-feasibility rollout is higher-information than a synthetic methodology probe.

## Hard-integrity-floor confirmation

**CONFIRMED / DO NOT RELAX.** No recommendation changes consumed/frozen identities, rerun/retune rules, prospective/frozen protocols, raw-before-score, preserve-before-read, exact identity/source/package/runtime/input binding, immutable evidence, evaluator/target leakage controls, or the prohibition on silent post-outcome repair.

## Current inputs / authoritative refs

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- previous Methodology `METHCAL-20260921T062111+0900-R29-C5E1A7D2@03964aa181c901b705bf3e2e5e7e3df82b724f40`
- Control `CTRL-20260921T065000+0900-R20-8E4C2A71@cae67ec0f8980e6125c578c3eb98d67e6da46a36`
- Evidence Analyst `EVA-20260921T065846+0900-R29-7B2C91E4@de3de2fcf0f21aa33ebfe417d210df1e96889a90`
- SUB prospective contract `eb5ae27f3ef7f8cca2bcc521e2c3f027a5ab6c42`
- SUB outcome-bearing commit `1a571db21ff82001407f01cb2c5449f253bfd4e5`
- SUB final result head `0c857a73cf34b58b737f686fd9af60769de3d306`
- fresh MAIN comparator-feasibility prospective head `b2547429823be29a2547419c80c40fb2138dfdc9`
- authoritative tags independently re-fetched: `evidence/*=5`; `formal/*=0`; `sealed/*=0`; tag-based `freeze/*=0`

## Confidence

**HIGH** overall. **HIGH** that the qualitative reframe policy has now worked once without quality-floor relaxation and that the previous no-target episode is legitimately closed. **HIGH** that eligibility and readiness are operationally distinct on the fresh active successor. **MODERATE-HIGH** on long-run mechanism-supply health because recovery is one small-n mechanism family. **INSUFFICIENT_EVIDENCE** remains for first READY→PRE_FORMAL and first genuine SYSTEM-over-comparable-MECHANISM exception.

## Questions for Control / Analyst

- Preserve the closed no-target episode and do not mechanically reopen it after the fresh MECHANISM surface change.
- Enforce canonical HOLD enum values at producer handoff; keep orthogonal reason/terminal/queue fields unchanged.
- Preserve the active successor's pre-outcome `eligible=true / NOT_READY` rationale so the first READY transition can be audited cleanly.
- If exact matched-load feasibility fails, HOLD/STOP rather than relaxing matching after outcome knowledge.
- For any future SYSTEM-over-comparable-MECHANISM execution, require the machine-readable exception before execution.
