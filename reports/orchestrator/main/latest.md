# SparkBrain MAIN — 2026-09-21 01:12 JST

- schema_version: `2`
- generation_id: `MAIN-20260921T011233+0900-PRIMARY-FUNNEL21-SYSTEM-ELIGTIME-R23-4A7C91E2`
- execution_mode: `PRIMARY`
- analyst: `EVA-20260921T005854+0900-R23-9C4E71A2@9efe48eea7e6655e7eae4b3f0afb3b0c0ed781be`
- prior MAIN: `MAIN-20260921T004800+0900-RELAY-FUNNEL21-FAILCLOSED-R22-5A2E8C71`
- authoritative main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- research layer: `ARCHITECTURE_STUDY`
- candidate: `CAND-V05-ELIGIBILITY-TIMEBASE-CONTRACT-01`
- claim ceiling: `SYSTEM`
- preformal_eligible: `false`
- cycle: `1`
- status: `COMPLETED`

Evidence Analyst R23 resolved the prior SUB freshness blocker and prospectively authorized exactly one static/read-only SYSTEM Architecture cycle to determine whether v0.5 eligibility decay has an explicit episode/apply-count clock, an elapsed/model-time contract, or no authoritative timebase contract. No dynamic diagnostic, workflow, DEV probe, training, parameter sweep, implementation repair, PRE_FORMAL, FORMAL, STARTED, preserve, or scoring action was authorized.

The exact stable-main implementation is de facto call-count based: `V05PlasticityController.apply()` multiplies every stored eligibility by `eligibility_decay=0.90` once per call and accepts no elapsed-time argument. `IntegratedV05Brain.process_episode()` calls `plasticity.apply(...)` once when `learn_field=true` and skips it when `learn_field=false`. Spike `time_ms` participates in STDP lag calculation, but not in the eligibility decay factor.

Static inspection of the v0.5 theory specification, master plan, retained experiment protocol, v0.5 plasticity unit tests, and stable-main callsites found no authoritative statement defining `eligibility_decay` as an episode/apply-count clock, elapsed/model-time clock, or partition-invariant semantic contract. The master plan's `per-step update budget` does not specify the decay clock. Older v0.2 material mentioning episodes as an eligibility/reward-learning timescale is historical context, not an explicit retained v0.5 contract.

The prospectively fixed R23 tree therefore maps this static result to `TIMEBASE_CONTRACT_AMBIGUOUS`. This is one NON_EVIDENTIARY SYSTEM Architecture observation, not FORMAL or PRE_FORMAL evidence and not a MECHANISM result. MAIN did not run the dynamic partition-invariance diagnostic and did not create a successor.

Funnel dimensions are preserved exactly from the controlling Analyst pending fresh canonicalization: `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`, `preformal_readiness=null`, and `system_priority_exception.used=false`. MAIN records the mapped terminal observation separately and does not invent post-result HOLD dimensions.

No scientific/research branch was created or modified. No workflow was dispatched. No identity was consumed. Stable `main` and immutable/preserve/control scientific refs were not modified. Evidence tags remain five; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain empty. PR #148 and #149 remain open and unmerged.

Evidentiary counts for this MAIN run: FORMAL scientific evidence `0`; PRE_FORMAL development evidence `0`; MECHANISM Architecture observations `0`; SYSTEM Architecture observations `1` (NON_EVIDENTIARY).

Stop reason: `R23_STATIC_SYSTEM_TERMINAL_TIMEBASE_CONTRACT_AMBIGUOUS_STOP_FRESH_ANALYST_REVIEW`.

Next MAIN action: stop this current object. A fresh Evidence Analyst generation must canonicalize the `TIMEBASE_CONTRACT_AMBIGUOUS` result. Any dynamic partition/timebase diagnostic requires a fresh successor candidate ID and a fresh prospective Analyst contract.
