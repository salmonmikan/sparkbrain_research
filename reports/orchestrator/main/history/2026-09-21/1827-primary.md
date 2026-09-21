# MAIN PRIMARY history — R40 pipeline preflight repair and conformance

- schema_version: `2`
- generation_id: `MAIN-20260921T181649+0900-PRIMARY-FUNNEL21-SYSTEM-PIPECONF-R40-LINTFIX-6A3D21C8`
- Evidence Analyst: `EVA-20260921T180006+0900-R40-7C4A21E9@cc75b2a7f1c398a393180dfed59305fcc03e7aee`
- candidate: `CAND-PREFORMAL-OUTCOME-BLIND-FOUR-STAGE-PIPELINE-CONFORMANCE-01`
- layer / ceiling: `ARCHITECTURE_STUDY / SYSTEM`
- canonical dimensions preserved: `preformal_eligible=false`, `preformal_readiness=null`, `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`

Exact diagnosis of workflow `35578428792@5527ac14d4d19078a91aa40f8825d5a4f41f0a91` established a preflight-only Ruff `I001` import-block formatting failure in `scripts/outcome_blind_raw_generator.py`; Local readiness, Test, and Validate bundle had not run, so `result_bearing_stage_reached=false`.

Per R40 authority, MAIN applied exactly one bounded science-invariant correction: removed the extra blank line after the import block, and refroze only that file's SHA256 in the existing contract. Raw-generator digest changed `29c96a30ac7419249be35b8dfe5eeeff0755f1ea9621e4d4bfbae4e0a68ed22e -> a0358140d48c0ea9177f7290dacef77236d7e3fbf7b8ae7385d18fd847d3252f`. Analysis choices, fixture, raw schema, comparator, scorer, threshold, resource rule, runtime, seed, and terminal mapping were unchanged. The two-file atomic research commit is `168883bd316985537e404c6aad3a7ac03202e28a`.

Exact-head CI `35583071628` then completed `success`; Python 3.11 and 3.13 both passed Install, Lint, Local readiness, Test, and Validate bundle. Prospectively mapped terminal observation: `SYNTHETIC_LIVE_CONFORMANCE_PASS` (`SYSTEM_ARCHITECTURE_NON_EVIDENTIARY`). Same-run continuation stops here for fresh Analyst review.

Repository source-of-truth refresh: stable main `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; five authoritative evidence tags; no formal/sealed/tag-freeze refs; H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`; PR #148/#149 open, unmerged, mergeable; rulesets `0`; SUB collision `NONE`.

Evidentiary delta: FORMAL `0`; PRE_FORMAL development `0`; MECHANISM Architecture `0`; SYSTEM Architecture `1`; new identity consumption `0`.

Stop reason: `R40_SYNTHETIC_LIVE_CONFORMANCE_PASS_STOP_FRESH_ANALYST_REVIEW`.
