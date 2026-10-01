# Isolated temporal-reuse diagnostic execution

Status: implementation preparation, not an executed result. Scientific credit: 0.
The [v2 contract](temporal_reuse_loop_contract_20261001.md) was independently reviewed
at `7e4368550fb3826a2b9847e8275ef07849de33b0` before implementation. Its v1 history and
prospective amendments remain in PR #169.

`scripts/temporal_reuse_loop_probe.py` is a standalone POSIX/Python CPU diagnostic.
It imports the source-pinned v0.5 runtime unchanged and never calls its historical
evaluation runner. `tests/test_temporal_reuse_probe_contract.py` checks only pure
implementation helpers with hand-authored fixtures; no measured stream is generated there.

After implementation review and an exact source/config/test freeze, the intended command is:

```bash
PYTHONHASHSEED=0 python scripts/temporal_reuse_loop_probe.py --output /absolute/new/output
```

The output directory must not exist. Each run records source/contract hashes, Git head,
environment, input files, durable raw pre-outcome rows, native checkpoints, receipt state,
resource costs, failures, and SHA-256 inventory. Model-running guards are part of that
run's budget. Every prefix must meet the reviewed quiet-boundary checkpoint conditions
before any measured suffix or causal fork runs. An ineligible prefix stops the diagnostic
without changing runtime or claiming predictive/causal results.

Execution uses a Python audit hook to deny all socket operations in the driver and each
worker. The cloud container refused `unshare -n` with `Operation not permitted`; therefore
no OS-level network-namespace isolation claim is made. The inspected runner uses no remote
runtime API or network subprocess. This guard choice is disclosed before execution.

Model/state memory is bounded by address-space limits and complete native-plus-wrapper
checkpoint sizes. CPU and wall budgets include child startup, checkpoint work and output;
per-fork logged timestamps precede their final cost-row write, which remains inside the
enforced timer and is included in process/global measured cost. Actual S/F candidate
comparison work is not instrumented inside runtime: its reported bound is labeled an upper
bound, while H/R distance-call counts are direct counts. Slots are not equal actual bytes
or compute. No efficiency or inferential scientific claim follows.

One MiB of the 1 GiB output cap is reserved for terminal/cost/inventory records.
Two CPU seconds and five wall seconds of the global time caps are reserved for closure.
Inventory hashing precedes the final cost capture; closure records distinguish measured
pre-closure cost from its conservative upper bound including that reserve. The data
manifest excludes itself and the final report/cost records to avoid recursive hashing;
a later transport manifest can hash the complete finished directory. Completion requires
both a completed report and zero process exit, never the report file alone.

No new model or measured stream has been run as of this preparation document.
