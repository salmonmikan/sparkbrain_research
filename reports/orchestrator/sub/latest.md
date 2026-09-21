# SparkBrain SUB — R32 bounded SYSTEM Discovery

- schema_version: `2`
- generation_id: `SUB-20260921T104150+0900-SYSTEM-OUTREPLAYINVALID-7C2A91E4`
- status: `COMPLETED`
- analyst: `EVA-20260921T095900+0900-R32-6D2A91C4@6bf35ff0f08a981feb09abced00e157526a47cb0`
- MAIN observed: `MAIN-20260921T101710+0900-PRIMARY-FUNNEL21-MECH-ASMSET-R32-2F6C91A4`
- Control: `CTRL-20260921T085000+0900-R21-4F7C2A91@49ac783b5640b8250c19133f8842f0bf49867e8f`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- operating mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- target: `V05_OUTCOME_REPLAY_CREDIT_SEMANTICS_DISCOVERY_CYCLE1`
- candidate: `CAND-V05-OUTCOME-REPLAY-CREDIT-SEMANTICS-01`
- cycle: `1/3`

## MAIN independence

R32 assigns MAIN the active `CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01` MECHANISM Architecture object. This SUB object is an independent API/lifecycle question about `learn_outcome()` pending-credit consumption. It does not use or alter MAIN's lesion distribution, comparator/balance/resource contract, target surfaces, support rule, blocker, or successor; it does not reopen terminal Assembly predecessors or H7.

## Prospective question / reduction / falsifier

Question: after `process_episode()` establishes a pending mature Assembly/action association, does `learn_outcome()` consume it exactly once, or can an identical outcome be replayed without a new episode and apply additional prediction/action credit?

Hypothesis: replay sensitivity may occur because `learn_outcome()` forwards `pending_activation` to the predictor and the action-policy pending tuple to reward learning without an explicit consume/clear guard.

Ordinary reduction question: if replay sensitivity exists, is it completely explained by reuse of the same pending association plus `predictor count += 1` and `action score += learning_rate * reward`?

Falsifier: the second identical `learn_outcome(next_event="sub-replay-event", reward=1.0)` is rejected, becomes a no-op, or leaves learning state unchanged relative to the single-call arm.

The outcome-independent contract was fixed first at `de62d218cae1710f4f301023f2db942b99943765` on `research/exploratory-sub-v05-outcome-replay-credit-semantics-20260921`.

## Observation / terminal

The fixed comparator is invalid on the supported monotonic-time API before any replay outcome is exposed. The contract trains `training_episodes(seed=501,count=24)` and then fixes `training_episodes(seed=501,count=1)[0]` as the support probe. That probe uses default `start_ms=0.0`, while the trained brain clock has advanced; `IntegratedV05Brain.process_episode()` rejects any non-empty pulse sequence whose first pulse predates `current_time_ms`.

Prospective terminal: `INVALID_COMPARATOR_OR_RUNTIME`.

No replay `learn_outcome()` call was executed. No later start time, alternate episode, seed, threshold, count, reward, event label, support search, or rescue tuning was substituted. Result/final research head is `6fa2114ff5f68bb940abd21600a587b460293097`. Exact-head integrity CI `35551537415` completed successfully on that exact head.

## Funnel-v2.1 handoff

`evidentiary_status=NON_EVIDENTIARY`; proposed `claim_ceiling=SYSTEM`; proposed `preformal_eligible=false`; preliminary readiness=`N/A_FOR_SYSTEM_OBJECT`; `hold_class=null`; `hold_reason=null`; `terminal_state=TERMINAL_FOR_CURRENT_OBJECT`; `queue_state=NOT_QUEUED`; next layer=`NONE`; recommendation=`REJECT_CURRENT_OBJECT_CONTRACT_INVALID`.

A valid time-shifted replay-semantics question requires a fresh candidate ID and fresh prospective contract; it is not cycle-2 rescue.

## Theory-backward accounting

Current autonomous selection is SYSTEM. Rolling last three are `SYSTEM_DISCOVERY:V05_NONLEARNING_ACTION_VISIT_CARRYOVER / THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY / SYSTEM_DISCOVERY:V05_OUTCOME_REPLAY_CREDIT_SEMANTICS`, so the theory-backward floor remains `1/3`. `theory_backward_exception=null`. `system_priority_exception.used=false`: the coherent executable MECHANISM object is MAIN-owned and excluded from SUB duplication, while H7 remains uncontracted.

No FORMAL/PRE_FORMAL action, STARTED/TEST/scorer, held-out tuning, identity consumption, immutable evidence/control/preserve mutation, stable-main mutation, or Utility request occurred.
