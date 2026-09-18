# MAIN Orchestrator — PRIMARY PD0.1 authority package awaiting exact-head gates

Timestamp: `2026-09-18 11:24 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `91a05bad6d130f89975e776960a1d25d764fba32`

## MAIN frontier

The Evidence Analyst advanced PD0.1 to conditional exactly-one formal execution authority. MAIN consumed that fresh authority and retained the reviewed scientific object exactly: `research/pd01/formal_contract.json` remains blob `0ce03b01baf41a0c77c513835b1c6063e47b2614`, and `src/sparkbrain/external_validation/fading_memory.py` remains blob `16bbfb6ed57d6c9701e8437360692b62e7c36915` from reviewed scientific head `ea2a8b4a5f244d601782ecb302760c49ee27e8c1`.

MAIN advanced `research/pd01-fading-memory-preformal-20260918` science-invariantly to exact package head `9defd189963cde9e296df48adb56e374a3d51f2f` by adding only the Analyst-bound execution/admission envelope and one-way machinery:

- `research/pd01/execution_authority.json` binds Analyst `91a05bad...`, the reviewed science blobs, identity `pd01-long-history-fading-memory-official-v1`, no-retry semantics, namespaces, terminal rules, and the narrow fixed-reservoir interpretation cap;
- `scripts/check_pd01_execution_authority.py` fail-closes on exact science blobs and authority/binding drift;
- `scripts/run_pd01_official.py` implements the already-frozen DEV-only readout fit, target-blind 2,048-row TEST acquisition, and post-preservation deterministic scoring;
- `scripts/preserve_pd01_boundary.py` supplies the no-clobber raw/manifest/input-inventory preservation boundary;
- `.github/workflows/pd01-formal-one-way.yml` implements the prospectively fixed STARTED -> target-free TEST -> DEV fit -> target-blind raw -> immutable preserve -> independent refetch -> TEST targets -> total join -> deterministic evidence chain;
- the dedicated formal pre-START workflow now validates the authority package while also proving the reviewed scientific contract and implementation blobs remain unchanged.

No scientific field was altered: task/world, lags, SparkBrain config/plasticity, comparator, resource/readout privileges, seeds, inventory, runtime, metric, cluster unit, bootstrap, thresholds and terminal criteria remain the Analyst-reviewed contract.

## Exact-head workflow state

The head movement correctly restarted all required gates on `9defd189963cde9e296df48adb56e374a3d51f2f`:

- `pd01-preformal` compatibility `35299066433`: `queued` at checkpoint;
- ordinary CI `35299066497`: `queued` at checkpoint;
- `pd01-formal-contract-prestart` `35299066515`: `queued` at checkpoint.

There is no useful local critical-path work remaining until those external gates resolve, so PRIMARY is yielding with a durable `WAITING_EXTERNAL` checkpoint rather than idling.

## Collision and integrity reconciliation

The prior MAIN lease was a stale `BLOCKED` RELAY checkpoint from 10:45 JST, not a fresh conflicting RUNNING owner. MAIN recovered it only after re-fetching the Analyst tip, exact research head and PD01 namespace state. SUB remains `no_op` / `sub_lane=null`.

Before mutation, the proposed identity was fresh and no matching PD01 control/preserve/evidence refs existed. No STARTED has been created in this run. No official TEST inputs or TEST targets have been accessed, no raw has been generated or preserved, no scientific scoring has occurred, and no immutable/consumed evidence has been modified.

## Relay / next MAIN action

Collect exact-head runs `35299066433`, `35299066497`, and `35299066515`.

If a gate fails mechanically, inspect the exact job log, make only a science-invariant repair, and rerun every required gate on the new final SHA. If a scientific/semantic change would be required, STOP as `PRE_START_SEMANTIC_GAP`.

If all three are green, re-fetch the Evidence Analyst tip, exact research head, identity/consumed state, STARTED/control/preserve/evidence namespaces, and all exact source/protocol/package/input/runtime/candidate/comparator/scorer/preserver bindings. Only if every fresh GO check remains clean may MAIN create exactly one STARTED/no-clobber branch for `pd01-long-history-fading-memory-official-v1` and let the fixed one-way workflow proceed.

There is **no new scientific information** in this checkpoint.
