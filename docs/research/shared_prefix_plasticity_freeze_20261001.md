# Shared-prefix plasticity source/input package (2026-10-01)

Status: **PREPARATION ONLY / UNEXECUTED / NONFORMAL / ZERO SCIENTIFIC CREDIT**.
This successor package does not alter, execute, or merge the paused PR171. The
copied proposed protocol is retained unchanged. There are no new measurements.

## Scope and immutable predecessor

The fresh worktree starts from main `367904e10525ca43ac066ff9fc0701fa89e6b91e`.
All production `src/` files are unchanged, including relative to the predecessor
execution source pin `0bcb2c1b23c29e5107111343a757c57c1f7bbb41`.
The complete predecessor script from that commit is retained verbatim at
`artifacts/research/shared_prefix_plasticity_20261001/source/predecessor_temporal_reuse_loop_probe.py`.
Its SHA-256 is `28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae`.
Only its `occurrence`, observation helpers, `Model`, checkpoint operations, and
live-prefix `eligibility` predicate are reused. Its old CLI, guards, old seeds,
Q/F arms, interleaved streams and diagnostic forks are never invoked.

The new script is `scripts/shared_prefix_plasticity_probe.py`. Its `prepare`
operation freezes two exact input streams per seed, resolved configuration,
runner/vendor/runtime/test/protocol hashes and Python dependency inventory.
`prepare` and its targeted tests tripwire Model, v0.5 and v0.4 constructors,
prediction/outcome, ingest and field-run entry points. Only immutable
configuration dataclasses, the pinned input generator and pure helper fixtures
are exercised. No model construction, prefix, suffix, baseline, smoke or
scientific trajectory is permitted during preparation.

## Prospective implementation clarifications

- W/D are interventions on enable flags. Plasticity eligibility, update-count
  accounting and reward-trace decay continue in all branches, including W-D-.
  Delay learning consults post-weight `edge.weight > 0`; therefore interaction
  includes this coupling and downstream receptor/homeostatic effects. These are
  conditional flag effects, not independently identified physical processes
- After each live prefix, wrapper pending must be empty and all 64 exact receipt
  IDs and values must match. Brain pending activation normally remains populated
  after learning an outcome; it is preserved. Inspect eligibility on the live
  prefix before restore loses transient facts. Never sort/reset a failed boundary
- A/B association is fixed using mature prefix candidates and strict label-count
  majority. Record set IDs, set sizes, B-routing-identifiable (B nonempty), and
  A-to-B-crossover-identifiable (A and B nonempty). Empty sets produce zero/null
  endpoints and remain in results; they do not support prevention or a mechanism
- Native v0.5 readout ties choose label 0. This differs from strict association
  membership and H/R probability-tie abstention. Frozen B membership continues
  counting a selected mature B candidate after suffix readout counts tie
- Matching scores are captured from each pattern's actual pre-observe bank.
  Multi-pattern earlier observations can allocate/prune/update candidates. The
  diagnostic wrapper calls original best_match exactly once, returns its result
  unchanged, and computes read-only scores at that boundary. All candidates,
  prototypes, counts, maturity/suppression, threshold margins, best/second
  margins and birth provenance are retained. The matching tie-break is lowest
  candidate ID; strongest activation selects the largest
  `(similarity, episode_count, assembly_id)` tuple
- Candidate origin reports first-seen time, prototype/source pattern, observed
  episode IDs and A-prefix/B-prefix/return birth phase separately from the
  frozen A/B/neither readout association. No assembly ordinal supplies labels
- Each branch is restored from the same exact supported checkpoint bytes.
  Supported payload equality is checked before intervention; normalization masks
  exactly four declared Boolean flags. All nested checksums and learned state
  remain compared. Supported checkpoint saves recompute transport checksums
- Branches run sequentially in fixed order W+D+, W-D+, W+D-, W-D-. Later branches
  compare their first prediction immediately against the retained first-branch
  projection before their first outcome or any later prediction. A mismatch is
  persisted and terminal. There is no concurrent four-worker barrier. The
  projection preserves exact emitted pulses, spike order/times, pattern bins,
  activations, prediction/confidence, p1, native value, counts and match records;
  intentional post-step state hashes are not compared
- Before/after prediction and after-outcome records retain complete connection
  parameters, unit state/thresholds, rate EMA, receptors, eligibility, counts,
  outgoing order and omitted transient-state facts. No observer snapshot advances
  field time. Full raw result is retained before feedback; post-outcome state is
  separately durable
- Loss contributions are divided by every return row, not subgroup size. Wrong,
  abstain and correct contributions sum to Brier. All numeric count/loss endpoints
  receive conditional W/D effects and factorial interactions per seed and
  unweighted across the two seeds. Nullable event indices are descriptive only

## Execution gate: required later, not granted here

The package fixes the one absent fresh output root:
`/workspace/shared/sparkbrain-shared-prefix-plasticity-run-20261001`.
No output directory is created during preparation. Source/input publication and
independent approval must precede the first transition. Neither is represented
as complete by this file. `run` and direct `worker` invocation both authenticate
source/input/dependency hashes, committed bytes, review and publication records
before any production module import/model construction. An exclusive worker
start record, exact pre-start directory inventory, fixed job name, single output
root and global reservation ledger prohibit append-resume or duplicate jobs.

The later review JSON must contain `approved_for_execution: true`, a nonempty
`independent_reviewer` and durable `review_record_url`, exact `source_commit`,
`manifest_sha256` and the fixed `output_root`. The separate publication JSON must
contain `verified_published: true`, `verified_by`, `verified_at`, the same commit
and manifest hash, and exact source URL
`https://github.com/salmonmikan/sparkbrain_research/tree/<commit>`.
The runner verifies local committed bytes. Actual remote publication is a
separately obtained, recorded attestation; an offline process does not prove
GitHub availability or authenticate a reviewer's real-world identity.

Run uses the same Python executable/dependency bytes as prepare, with
`PYTHONHASHSEED=0` and `-S -P -B`, no unexpected PYTHON environment variables,
validated stdlib/source search paths, and no runtime/vendor bytecode caches.
`-I` is deliberately not used because it ignores the requested hash seed.
Python executable and stdlib source/native-extension bytes are frozen; the OS
kernel and transitive system shared libraries are not included in that inventory.
No third-party runtime packages are required. Test-only pytest/ruff are external
to this dependency set.

## Resource and failure contract

There are 14 serial jobs: two 64-row prefixes, eight 32-row suffixes and four
96-row baselines. Driver reservations charge at most 768 prediction attempts and
768 outcome attempts even if a worker fails. Per-worker counters refuse extra
calls and outcome duplication. No guard or revalidation calls model dynamics.
Both prefix eligibility checks must pass before any suffix or baseline begins.

Every process has 512 MiB RLIMIT_AS and no core dumps; worker OS limits are set
before exec. Fractional PROF/REAL deadlines, OS CPU hard limits, and driver wall
supervision bound workers. Startup/import/source verification and all worker
serialization/output are included in the parent-measured launch. Shared prefix
cost is paid once globally but charged conservatively to each branch's 120 CPU/
180 wall-second allowance. Full checkpoint cap is 64 MiB, banks/history 32 slots,
and unchanged field/spike/plasticity-update caps come from the source freeze.

Resource timers/signals have OS scheduling granularity; success requires actual
inclusive accounting under the ceiling and zero process exit, not merely an
unchanged declaration. Driver and worker peak RSS are recorded, including
kernel wait4 RSS for a killed worker. No claim is made that Python socket audit
denial is OS network isolation; the runner does not enforce an OS network
namespace. The actual namespace identifier is recorded, without claiming it
proves offline isolation.

Global bounds are 1800 CPU seconds, 2700 wall seconds and 1 GiB output; closure
reserves are inside them. Each append/write checks aggregate bytes and fsyncs.
No-clobber source/freeze/checkpoints and fresh output directories preserve partial
failures. Failed resource/invariant/infrastructure attempts are terminal and
never automatically retried or replaced. A killed process may leave an incomplete
last record; earlier durable records stay visible. A missing success record or
nonzero exit cannot be interpreted as a result. Any amendment requires fresh
review and preserves the original failure.

## Allowed validation and intentionally unrun checks

Use only `tests/test_shared_prefix_plasticity_contract.py`, targeted ruff and
source checks during this phase. The repository full pytest/readiness/demo/
benchmark/reproduction sequence is intentionally not run: several suites exercise
model dynamics. No full-validation claim is made. The final preparation report
lists the exact commands, hashes and pure-test outcomes separately from the
unstarted execution.

Global CPU accounting includes all waited child processes, including source
verification's Git subprocesses, using RUSAGE_CHILDREN rather than summing only
model workers. Git-child CPU is deducted from fractional PROF allowance before
another operation. Parent launch accounting includes descendant CPU returned by
wait4; there is no double counting in the global total. A timer check after a
Git child returns can report a cap failure; it cannot retroactively prevent
OS-granularity overrun, and no model transition follows such a failure.
Positive accuracy effects are beneficial; coverage effects have no automatic
benefit interpretation. Positive adverse count/loss effects mean worse outcomes.
