# MAIN RELAY — Delayed-outcome caller-contract Architecture cycle 1 completed

Timestamp: `2026-09-20 08:48 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst authority: `850b4502cf15d3f6118a487c5ab4ba81fbf7b75e`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01`  
Exploration cycle: `ARCHITECTURE_STUDY 1`

## Collision / authority reconciliation

The prior PRIMARY lease was `WAITING_EXTERNAL` with heartbeat `2026-09-20T08:21:00+09:00`, so it was not a fresh same-object `RUNNING` collision. Before mutation, RELAY re-read the MAIN lease/state/latest, fresh Evidence Analyst tip, exact research head, exact workflow result, and SUB state. Evidence Analyst tip remains `850b4502cf15d3f6118a487c5ab4ba81fbf7b75e`. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The active research branch still resolves exactly to `c79c5434222a6d018931dc1752e7f0074c23854b`.

SUB completed an independent bounded Discovery object and explicitly avoided the MAIN delayed-outcome branch/object; no MAIN/SUB collision was found. This Architecture object has no formal identity, STARTED ref, preserve ref, scorer, or evidence ref. Historical immutable control/preserve/evidence surfaces remain read-only and were not mutated.

## Exact continuation performed

RELAY collected ordinary CI run `35475862604`. GitHub reports `completed/success` on exact branch `research/main-v05-delayed-outcome-caller-contract-arch-study-20260920` and exact head `c79c5434222a6d018931dc1752e7f0074c23854b`.

The scientific/Architecture terminal had already been prospectively mapped and persisted by PRIMARY before this relay:

**`IMMEDIATE_ONLY_USAGE_BUT_PUBLIC_CONTRACT_UNSPECIFIED`**

The fixed static characterization remains unchanged: every bound observed caller uses `learn_outcome` immediately after the relevant `process_episode`; the single mutable pending credit state is overwritten by subsequent `process_episode` calls; `learn_outcome` carries no episode/decision identity; and no explicit immediate-only or delayed/interleaved public contract was found on the bound surface. The exact-head CI success validates repository integrity only and does not change that terminal or add new scientific information.

## Evidentiary / integrity status

This remains a **NON_EVIDENTIARY ARCHITECTURE_STUDY** result. New FORMAL scientific evidence from RELAY: **none**. New PRE_FORMAL evidence from RELAY: **none**. No dynamic interleaving probe, semantic redesign, same-object cycle 2, implementation fix, PRE_FORMAL promotion, FORMAL identity, STARTED, TEST, scorer, preserve/evidence mutation, consumed-identity retry, research merge, or Utility request occurred.

The prospectively fixed continuation is now complete. Stop reason: **`VALID_STATIC_TERMINAL_AND_EXACT_HEAD_CI_SUCCESS_STOP_FOR_FRESH_ANALYST_REVIEW`**.  
Final lease target: **`COMPLETED`**.  
Next MAIN action: wait for a fresh Evidence Analyst handoff. Do not continue this same object dynamically or promote it to PRE_FORMAL/FORMAL without new prospective authority.
