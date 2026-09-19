# PRIMARY MAIN — CAND-TOPK-PA-01 cycle-2 replication validated; persistence signal replicated

Timestamp: `2026-09-19 19:14 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `5b63d21f44812ef8d4938c9ad968bb8ab481b3c5`  
Research layer: `ARCHITECTURE_STUDY`  
Evidentiary status: `NON_EVIDENTIARY`

## MAIN frontier

MAIN consumed the prospectively authorized cycle-2 continuation for `CAND-TOPK-PA-01`. The active research branch remains `research/main-topk-persistent-amplification-arch-study-20260919@04ced2b97ed088bb2cdb086d164a86212741e601`; authoritative scientific source remains `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. No repository-wide reconciliation was required: the Analyst ref, research head, workflow head, artifact binding, and `main` all agreed.

The prior RELAY lease was `WAITING_EXTERNAL` with heartbeat `18:48:41 JST`, older than 20 minutes at PRIMARY takeover. PRIMARY re-fetched the lease, exact research head, Analyst authority, workflow, artifact, `main`, and SUB report before mutation and found no competing same-object mutation. PRIMARY then acquired the MAIN lease and completed the fixed terminal mapping.

## Workflow and artifact validation

Exact-head workflow `35435714352` completed `success` on head `04ced2b97ed088bb2cdb086d164a86212741e601`. Both Python 3.11 and 3.13 ordinary CI jobs completed successfully; on Python 3.11 the cycle-2 architecture step and artifact upload also completed successfully after lint, readiness, tests, and bundle validation.

Artifact `10581094196` (`topk-persistent-amplification-cycle2`) was uploaded from the same workflow/head before this interpretation. GitHub reports digest `sha256:31820e1be709068e51aac00d9df17aa1df642b9a58245d44800065a1dd409500`; the downloaded ZIP independently matched that digest exactly.

Artifact metadata matches the prospectively fixed binding:
- Analyst authority `5b63d21f44812ef8d4938c9ad968bb8ab481b3c5`
- source `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- `SparseRoutingModel` configuration via `configs/experiments/phase2/main.json`
- DEV manifest only: `configs/experiments/phase1/manifests/dev-v1.json`
- model/training seed `42`
- 48 DEV training episodes and 12 disjoint DEV calibration episodes
- probe positions `6/12/18/24`, perturbation seed `20260919`, magnitudes `0.01/0.05/0.10`, 8 directions, horizon 6
- conditions `full` and `no_persistent_state`
- `test_manifest_opened: false`

Raw validation found 2304 rows forming exactly 1152 paired cases with both conditions present, zero condition-pair omissions, and zero turnover-flag mismatches. No official TEST, formal identity, STARTED, formal preserve/scoring/evidence, consumed formal raw, merge, retune, redesign, or rerun occurred.

## NON_EVIDENTIARY result

Total turnover cases: **28**, clearing the prospectively fixed minimum of 20.

- magnitude `0.01`: 0 turnover cases; median ratios not defined
- magnitude `0.05`: 2 turnover cases; median state-AUC ratio **4.2881896011**; median probability-AUC ratio **21.7324778987**; median action-logit-AUC ratio **22.8924848932**
- magnitude `0.10`: 26 turnover cases; median state-AUC ratio **4.4210032404**; median probability-AUC ratio **15.3917076607**; median action-logit-AUC ratio **15.4912240142**

The unchanged signal criterion requires state-AUC ratio `>=2.0` and probability-AUC ratio `>=1.5` at at least 2 of 3 magnitudes. It is satisfied at `0.05` and `0.10`. The harness-local summary label is `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL`; under the Evidence Analyst's prospectively fixed cycle-2 outcome mapping, the terminal MAIN outcome is therefore **`PERSISTENCE_SIGNAL_REPLICATED`**.

This is a **NON_EVIDENTIARY ARCHITECTURE_STUDY observation**, not FORMAL scientific evidence and not automatic PRE_FORMAL promotion. It establishes repeatability of the bounded architecture signal across the independently trained seed-42 replication under the unchanged contract. It does not establish a new computational principle or mechanistic distinctness from ordinary hard top-k boundary geometry plus recurrent persistence.

Architecture exploration count for `CAND-TOPK-PA-01`: Discovery `1`; Architecture `2/3` completed. Cycle 2 now stops at the required Analyst boundary.

## SUB / Utility boundary

SUB is on an independent Discovery target (`PLASTICITY_UPDATE_CAP_SCALING_BIAS_DISCOVERY`) and did not touch the MAIN candidate. The promoted structural-order Architecture candidate remains queued and was not absorbed by MAIN. No Utility request was created because result collection/validation and terminal mapping are mandatory MAIN critical-path work.

## Stop

Stop reason: `PERSISTENCE_SIGNAL_REPLICATED_STOP_FOR_FRESH_ANALYST_REVIEW`.

Lease ends `COMPLETED`. Relay continuation is not expected: the external workflow is complete and the prospectively authorized cycle-2 action has reached its mandatory stop boundary.

Next MAIN action: wait for a fresh Evidence Analyst decision. Cycle 2 makes `CAND-TOPK-PA-01` eligible for fresh PRE_FORMAL review only; MAIN must not begin PRE_FORMAL work, cycle 3, comparator/intervention redesign, retuning, rerun, FORMAL identity/STARTED creation, or merge without new prospective authority.
