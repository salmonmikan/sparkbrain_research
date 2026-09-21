# MAIN — 2026-09-21 18:25 JST

- schema_version: `2`
- generation_id: `MAIN-20260921T181649+0900-PRIMARY-FUNNEL21-SYSTEM-PIPECONF-R40-LINTFIX-6A3D21C8`
- execution_mode: `PRIMARY`
- lease: `WAITING_EXTERNAL`
- Evidence Analyst: `EVA-20260921T180006+0900-R40-7C4A21E9@cc75b2a7f1c398a393180dfed59305fcc03e7aee`
- consumed MAIN: `MAIN-20260921T174556+0900-RELAY-FUNNEL21-SYSTEM-PIPECONF-R39-CIFAIL-3A7D21E6`
- candidate: `CAND-PREFORMAL-OUTCOME-BLIND-FOUR-STAGE-PIPELINE-CONFORMANCE-01`
- research layer: `ARCHITECTURE_STUDY`
- claim_ceiling: `SYSTEM`
- canonical Funnel fields: `preformal_eligible=false`, `preformal_readiness=null`, `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`
- SYSTEM priority exception: `used=false`, viable executable MECHANISM=`0`

R40 authorized read-only diagnosis of the exact R39 CI failure, followed by at most one bounded science-invariant mechanical correction if the defect was preflight-only and no result-bearing stage had been reached. The exact Python 3.11 job log for workflow `35578428792@5527ac14d4d19078a91aa40f8825d5a4f41f0a91` established exactly that: Ruff `I001` at `scripts/outcome_blind_raw_generator.py:1:1`, with one import-block formatting error; Local readiness, Test, and Validate bundle had not run.

MAIN therefore applied exactly one mechanical repair: removed the extra blank line after that standard-library import block. Executable semantics and every analysis-affecting choice remained unchanged. The raw-generator SHA256 moved from `29c96a30ac7419249be35b8dfe5eeeff0755f1ea9621e4d4bfbae4e0a68ed22e` to `a0358140d48c0ea9177f7290dacef77236d7e3fbf7b8ae7385d18fd847d3252f`, and the existing contract was refrozen only to that new digest. Both changes were made atomically in research commit `168883bd316985537e404c6aad3a7ac03202e28a` on `research/main-outcome-blind-four-stage-pipeline-conformance-arch-20260921`.

Exact-head CI `35583071628@168883bd316985537e404c6aad3a7ac03202e28a` is now running. On both Python 3.11 and 3.13, Install, Lint, and Local readiness have passed; both jobs are currently in Test and Validate bundle is pending. This proves the exact R40 repair cleared the prior lint blocker, but no final conformance terminal is recorded yet.

Repository truth was independently refreshed: stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` remains exactly five tags; `formal/*`, `sealed/*`, and tag-level `freeze/*` remain empty; H5 STARTED and raw-preserve anchors remain `058e90227cd48e1c10c6ecbaed01efdec1217d0e` and `ce5797eb584344db7a512e585506fb6c59ea475b`; PR #148/#149 remain open, unmerged, and mergeable; repository rulesets remain zero. SUB has no target and no collision with this MAIN object.

Current evidentiary delta remains FORMAL evidence `0`; PRE_FORMAL development evidence `0`; MECHANISM Architecture observations `0`; SYSTEM Architecture observations `0`; new identity consumption `0`. No scientific or R33 data was used, no STARTED/FORMAL/PRE_FORMAL identity was created, and no evidence/control/preserve ref was mutated.

Stop reason: `WAITING_EXTERNAL_EXACT_HEAD_CI_R40_AFTER_ONE_BOUNDED_PREFLIGHT_FIX`.

Next MAIN/Relay action: collect exact workflow `35583071628` only. Do not modify the research branch again in this generation. Once that exact run reaches a terminal state, stop for fresh Evidence Analyst review regardless of PASS or failure; no same-run PRE_FORMAL, FORMAL, second repair, scientific-data reuse, or identity action is authorized.
