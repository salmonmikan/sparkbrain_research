# Utility result — CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE

- schema_version: 2
- assignment_id: `CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE`
- assignment_generation_id: `UASSIGN-20260921T005250+0900-ELIGTIME-7D4A2C91`
- utility_status: `BLOCKED`
- evidentiary_status: `NON_EVIDENTIARY_READ_ONLY_ARCHITECTURE_AUDIT_ONLY`
- scientific_authority: `NONE`
- run_count: `1`
- assignment_terminal_classification: `NOT_EMITTED_AUTHORITY_SUPERSEDED_BEFORE_DIAGNOSTIC`

## Authority / freshness

The Control-owned assignment pointer was re-read immediately before persistence and still named this assignment/generation with `status: ASSIGNED`, `max_runs: 1`, and expiry `2026-09-28T00:00:00+09:00`.

However, a newer Evidence Analyst generation became authoritative after the assignment was issued:

- Evidence Analyst generation: `EVA-20260921T005854+0900-R23-9C4E71A2`
- Evidence Analyst branch head observed: `9efe48eea7e6655e7eae4b3f0afb3b0c0ed781be`
- authoritative main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

R23 created `CAND-V05-ELIGIBILITY-TIMEBASE-CONTRACT-01`, assigned the same central timebase question to MAIN as a static/read-only SYSTEM Architecture cycle, and explicitly prohibited a dynamic partition diagnostic in that same object/run. It requires any dynamic partition/timebase diagnostic to wait for fresh Analyst review and a fresh successor identity/contract.

MAIN subsequently completed that exact static Architecture lease:

- MAIN/Relay head observed: `a20207308c7203c597791c2371a3085d639a4a74`
- mapped observation: `TIMEBASE_CONTRACT_AMBIGUOUS`
- stop boundary: fresh Evidence Analyst review before any dynamic partition diagnostic

Therefore the older Utility assignment's conditional dynamic-diagnostic authority is no longer unsuperseded. Under the Utility freshness/collision rule, mutation beyond this Utility-owned report/state is blocked.

## Independent authoritative source audit

Read-only inspection was performed against exact stable main, not the mailbox branch.

Bindings inspected:

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- `src/sparkbrain/v05/plasticity.py`: blob `bb04eaac527aaa6343018ffb49347d087c6a29e5`
- `src/sparkbrain/v05/brain.py`: blob `652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
- `docs/THEORY_SPEC_v0.5.md`: blob `c1d3dbd041476428a103324b58616d3cc6534885`
- `docs/V05_EXPERIMENT_PROTOCOL.md`: blob `fce01cd448ad00e1d420e3cb73f6d0f32768df5d`
- `tests/v05/test_v05_homeostasis_plasticity.py`: blob `ba1763c8ceb441cc91ce7510a313548acbb29db9`
- `tests/v05/test_v05_brain.py`: blob `6a81994ac82a3f0660585ef0d95495aaaa336629`

Static findings:

1. `V05PlasticityController.apply()` multiplies every stored eligibility value by `config.eligibility_decay` exactly once per `apply()` call. The method has no elapsed-time/current-time/delta-time argument.
2. `IntegratedV05Brain.process_episode()` calls `self.plasticity.apply(...)` once when `learn_field=True` and does not call it when `learn_field=False`.
3. Current v0.5 theory/specification text states only that timing-dependent weight/delay updates are bounded and reward may modulate eligibility. It does not define the eligibility decay clock as episode count, apply count, elapsed/model time, or physical time.
4. The retained v0.5 experiment protocol fixes episode budgets and training/evaluation separation but does not define an eligibility-decay timebase.
5. Current v0.5 tests exercise plasticity mode separation and ordinary episode execution/checkpoint behavior, but no inspected test binds eligibility decay to a canonical episode/apply-count clock or asserts partition invariance.

Read-only conclusion: the implementation has an effective call-count clock, but the inspected current v0.5 contract surface does not explicitly make that clock semantic. This independently agrees with MAIN's later `TIMEBASE_CONTRACT_AMBIGUOUS` observation. Utility does not promote that MAIN observation into a scientific or candidate disposition.

## FUNNEL v2.1 preservation

The current Analyst object touched by this audit is `CAND-V05-ELIGIBILITY-TIMEBASE-CONTRACT-01`. Utility preserved the Analyst record exactly and made no typing changes:

- `claim_ceiling`: `SYSTEM`
- `preformal_eligible`: `false`
- `preformal_readiness`: field is absent for this SYSTEM object in Analyst R23; Utility did not synthesize a value
- `hold_class`: `null`
- `hold_reason`: `null`
- `terminal_state`: `ACTIVE`
- `queue_state`: `ACTIVE`
- `system_priority_exception`: `{used:false, reason_code:null, reason_detail:"SYSTEM work protects reproducibility/evidence interpretation; no comparable executable/informative MECHANISM exists.", compared_mechanism_candidate_ids:[]}`

MAIN's `TIMEBASE_CONTRACT_AMBIGUOUS` is a pending Architecture observation awaiting fresh Analyst canonicalization; Utility does not alter these R23 dimensions.

## Actions intentionally not taken

- no diagnostic branch created;
- no prospective dynamic contract created;
- no dynamic partition test executed;
- no training, workflow dispatch, rerun, retune, rescore, or scorer access;
- no scientific/research/main/evidence/formal/preserve/control ref mutated;
- no candidate created, promoted, downgraded, retyped, or reinterpreted;
- no scheduler mutation;
- no active MAIN/SUB/Relay branch used as a fixture.

## Stop reason

`BLOCKED_BY_FRESH_ANALYST_MAIN_OWNERSHIP_SUPERSESSION`

The static question is now MAIN-owned and has already reached a static terminal observation pending fresh Analyst review. Executing the Utility diagnostic would collide with the fresh ownership boundary and bypass the required successor/review step.

## Follow-up recommendation

Control Brain should treat this Utility assignment as blocked/stale for dynamic execution. If a dynamic partition-invariance diagnostic remains useful after fresh Evidence Analyst canonicalization, it should be authorized prospectively as a fresh successor with explicit ownership and no MAIN/SUB/Relay collision. Utility does not create or approve that successor.
