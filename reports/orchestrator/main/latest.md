# MAIN latest — R30 action-policy evaluation-isolation contract audit

Generation: `MAIN-20260921T081624+0900-PRIMARY-FUNNEL21-SYSTEM-ACTEVAL-R30-5C7A21E4`  
Analyst: `EVA-20260921T075832+0900-R30-9A4C2E71@773c88edcaf799140830f3d204d0f0ff82c9bcad`  
Stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`  
Candidate: `CAND-V05-ACTION-POLICY-EVALUATION-ISOLATION-CONTRACT-01`  
Layer / ceiling: `ARCHITECTURE_STUDY / SYSTEM`

## Result

Prospective static-audit terminal: **`MIXED_OR_UNRESOLVED_PUBLIC_CONTRACT`**. Analyst-mapped action: **`HOLD_CONTRACT_AMBIGUITY_AND_STOP`**.

The exact stable implementation is unambiguous: `AssemblyActionPolicy.choose()` increments `visits[assembly_id]` and sets `pending` after selecting an action even when `explore=false`. `IntegratedV05Brain.process_episode()` always calls that policy when action support is enabled; `explore_action=false` changes action selection but does not make the call observational. Action-policy state and `pending_action` are included in checkpoint/state hashing.

The retained evaluation callsites intentionally disable learning (`learn=False`, `learn_assembly=False`, `learn_field=False`, `explore_action=False`) and skip `learn_outcome()` on held-out episodes. `run_seed()` deep-copies the trained brain separately for each held-out condition, and ablation branches are also copied, so policy-state mutation is isolated between those top-level evaluation branches. Within a condition, however, held-out episodes run sequentially on one copy, so visit/pending state can advance across evaluation episodes.

The public scientific contract does not resolve whether that action-policy advance is intended. `THEORY_SPEC_v0.5.md` separates training from evaluation and permits held-out reactivation to feed prediction or action; `V05_EXPERIMENT_PROTOCOL.md` defines held-out budgets/gates. Neither those documents nor the Master Plan, status/completion reports, action API, or current unit tests explicitly states that held-out action choices are either (a) real policy visits that should consume visit/pending state or (b) observational probes whose policy state must remain immutable. The held-out unit test asserts only that the episode runs and has a state hash; it does not assert policy-state isolation.

Therefore MAIN does **not** infer either semantic contract post hoc. This is a bounded, NON_EVIDENTIARY SYSTEM Architecture observation only. No dynamic evaluation-interleaving probe is authorized or executed in this run.

Canonical Funnel dimensions are not invented post hoc: Analyst-provided `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE` remain recorded until fresh Analyst canonicalization. `claim_ceiling=SYSTEM`, `preformal_eligible=false`, and `system_priority_exception.used=false` remain unchanged.

## Workflow / integrity

- No research branch created; no workflow dispatched; no dynamic scientific execution.
- Previous MAIN research workflow `35541396714` and exact-head CI `35541396705` remain `completed / success` at `b2547429823be29a2547419c80c40fb2138dfdc9`.
- New scientific counts: FORMAL `0`; PRE_FORMAL `0`; MECHANISM Architecture observations `0`; SYSTEM Architecture observations `1`; identity consumption `0`.
- Stable main unchanged; authoritative `evidence/*` count `5`; `formal/*`, `sealed/*`, `freeze/*` tag counts `0`.
- Control/preserve anchors independently re-fetched; H5 STARTED remains `058e90227cd48e1c10c6ecbaed01efdec1217d0e` and H5 raw preserve remains `ce5797eb584344db7a512e585506fb6c59ea475b`.
- PR #148 and #149 remain open, unmerged, mergeable.
- No SUB collision was present at acquisition; latest observed SUB generation was `SUB-20260921T073900+0900-NOOP-NOMECH-4C7A91E2`.

Final lease: `COMPLETED`.  
Stop reason: `R30_STATIC_SYSTEM_TERMINAL_MIXED_OR_UNRESOLVED_PUBLIC_CONTRACT_HOLD_CONTRACT_AMBIGUITY_STOP_FRESH_ANALYST_REVIEW`.

Next action: fresh Evidence Analyst must canonicalize the reached `HOLD_CONTRACT_AMBIGUITY` contingency before any continuation. Do not run dynamic evaluation interleaving from this generation, and do not upgrade this SYSTEM object into MECHANISM.
