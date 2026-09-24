# Utility terminal result — R119 RVT35 causal-opportunity harness

- schema_version: `2`
- generation_id: `UTILITY-20260924T163300+0900-R119-RVT35-CAUSAL-OPPORTUNITY-HARNESS-A7D13C2E`
- produced_at: `2026-09-24T16:33:00+09:00`
- mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `UTIL-AUTO-20260924T163300+0900-R119-RVT35-SECOND-LANE-CAUSAL-OPPORTUNITY-HARNESS`
- selected_task: `FAST_FORGE_SECOND_LANE_SYNTHETIC_CAUSAL_OPPORTUNITY_AND_OUTPUT_NULL_DIAGNOSTIC`
- fast_forge_support: `true`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_authority: `NONE`
- disposition: `FORGE_OBSERVATION`

## Ownership / authority checks

Utility assignment pointer was clean schema-v2 `IDLE` with no active assignment. Evidence Analyst R119 authorizes only the bounded zero-credit noncanonical `RVT35-FORGE-001` Fast Forge probe; it does not admit a fresh canonical successor. MAIN PRIMARY R120 has no executable canonical object and is explicitly waiting for the Fast Forge revisit probe. The latest durable Fast Forge mailbox still predates Analyst R119 and remains the no-op gate-wait generation, so no primary Forge implementation of the new probe had been claimed at mutation time.

Freshness was re-read immediately before each Utility mutation. No MAIN/Relay canonical collision, protected evaluator dependency, hidden MAIN outcome dependency, or fresh primary Forge implementation collision was observed.

## Implementation

Created Utility-owned branch `forge/utility-rvt35-causal-opportunity-harness` from stable main and added:

`tools/forge/utility_causal_opportunity_harness.py`

The tool is synthetic-only and standard-library-only. It accepts a prospectively supplied fixed weighted graph, treated node, fixed readout weights, fixed horizon, fixed treated shift and fixed sensitivity floor. It checks two ordinary screening failures without fitting or adaptive search:

1. no treated-node to declared-observable causal path within the fixed horizon;
2. a reachable declared observable whose fixed readout is output-null or cancelling for the treated-state perturbation.

The embedded deterministic toy checks cover a sensitive downstream path, an unreachable readout, and a cancelling readout. No Candidate #35 artifact, R100 outcome, H7 result, protected evaluator, held-out payload, canonical identity, scorer, preserver, or result-bearing workflow is read or used.

## Observation

The reusable diagnostic harness is materialized and can support prospective rough Forge screening, but it has not been run against Candidate #35 data and returns no scientific or promotion-support signal. A pass from this harness would only mean these two simple ordinary screening failures were not reproduced in the supplied synthetic/fixed graph; it would not establish a mechanism, successor, readiness, lifecycle change, or canonical admission.

## Forge metrics

- prototype_type: `REUSABLE_SYNTHETIC_CAUSAL_OPPORTUNITY_OUTPUT_NULL_DIAGNOSTIC`
- independent_from_forge_primary: `true`
- outcome: `TOOLING_READY_SYNTHETIC_ONLY`
- ordinary_reduction_tested: `NO_PROSPECTIVE_TREATED_TO_OBSERVABLE_CAUSAL_PATH; OUTPUT_NULL_READOUT_PROJECTION`
- branch: `forge/utility-rvt35-causal-opportunity-harness`
- branch_head: `7123c29804b4538d38c0c308451337279b31958d`
- latency: `PT10M_APPROX_SAME_RUN`
- promotion_support_signal_returned: `false`

This Utility work is not counted as canonical Discovery, PRE_FORMAL or Funnel activity.

## Exact refs

- stable_main: `d16403414fc7abebd23075fc401240971b8eb91d`
- utility_assignment_pointer_blob: `5b3385e2e763239555c03e2d2ccc0b0613424c30`
- prior_utility_tip: `69b373bb05ce1f11e3321ef71b30adc9622fadad`
- evidence_analyst_generation: `EVA-20260924T160200+0900-R119-CAND35-REVISIT-FORGE-TEST`
- evidence_analyst_commit: `b56a9c604f1e859076b2c721ffc53cc0c6739b21`
- evidence_analyst_state_blob: `e4981783c7551beb342bb6d1b7088ccf81d399fe`
- main_generation: `MAIN-20260924T161228+0900-PRIMARY-R120-WAITING-CAND35-REVISIT-FORGE-TEST`
- main_tip: `6f1f8ac373b99d4346894f9591e2feb5cc2bcc13`
- fast_forge_generation: `FORGE-20260924T153500+0900-NOOP-R118-RAW-CAND35-REVISIT-AWAIT-ANALYST`
- fast_forge_latest_blob: `1a2f7cdbcaa0110695e45e63331000569bd2c25a`
- control_generation: `CTRL-20260924T155021+0900-R58-CAND35-REVISIT-PROPOSAL-AWAIT-ANALYST`
- control_commit: `3352ed6c00297fb7d6d61f193e002513f3178cf3`
- utility_support_branch_base: `d16403414fc7abebd23075fc401240971b8eb91d`
- utility_support_branch_head: `7123c29804b4538d38c0c308451337279b31958d`
- utility_support_file_blob: `6d9845cb39b0beaf4df4e576b65699fec66b8653`

## Request / stop

No request was created. Analyst and MAIN already route the next canonical decision through Fast Forge and a fresh Evidence Analyst gate, so an additional Utility request would duplicate existing control-plane intent.

Stop reason: bounded independent tooling task completed. Utility must not execute the Candidate #35 probe as canonical science, must not use old R100 outcomes to tune this harness, and must not claim a kill/survivor decision for `RVT35-FORGE-001`. Return to clean IDLE and allow primary Fast Forge to own any candidate-specific probe execution.

Follow-up recommendation: Fast Forge may independently use or ignore the Utility harness as zero-credit tooling. Any probe kill/survivor observation must return to a fresh Evidence Analyst before any fresh successor could exist.

## Hard-floor actions

`NONE` — no consumed identity rerun/retune/rescore; no immutable/formal/sealed/evidence/control/preserve destructive mutation; no held-out/evaluator access; no post-outcome rescue tuning; no Formal action; no scheduler mutation; no research PR merge; no scientific ref mutation; no protected scoring; no result-bearing workflow dispatch.
