# Bounded plasticity-retention runner: source preparation

Status: UNEXECUTED, NONCANONICAL, NON_EVIDENTIARY, zero scientific credit.
This implements the prospective protocol merged in PR179. It does not change
production SparkBrain code or report a retention result. The protocol, inputs,
job allocations and decision thresholds are unchanged.

## Research question and allocation

Can apply-local eligibility preserve new learning while reducing return
interference in the two exposed PR169 native-restored prefixes? C retains
eligibility with rho=0.9 and eta=0.001; L uses rho=0 with the same eta; G uses
rho=0.9 and eta=0.0001; Fw disables weight writes. All learned delays remain
fixed. Receptors, homeostasis, assembly formation and count readout remain live.
G is an analytic constant-delta steady-state attenuation reference; the arms
are not finite-history dose matched.

The immutable [protocol](../../protocols/plasticity_retention_bounded_v1.json)
allocates 768 prediction/outcome pairs across 26 sequential suffix branches:
512 v05 pairs and 256 H/R memory pairs. It permits 26 wrapper constructions,
18 native v05 loads and the published loader's 36 nested v05 constructions.
There is no new prefix training, probe, replay, retry or parameter search.
Return, stationary-B and balanced novel suffixes start independently from
published prefix copies. The primary comparison is C versus L; novel
acquisition and preservation are required, including abstention, coverage,
unrounded Brier loss and per-label late accuracy. A novel ceiling makes the
acquisition question inconclusive. All nine paired C-to-L native transition
counts are reported. The overall gate rejects a return gain whose only favorable
native transition is wrong-to-abstain: at least one such transition and no
wrong-to-correct or abstain-to-correct transition. Probability-only gains with
unchanged native decisions are still subject to the original Brier, correct-count
and coverage gates. This operationalizes the published prose exclusion before
any outcome is observed; no numerical margin or input changes.

## Implementation and evidence boundaries

- `scripts/run_plasticity_retention.py` freezes actual source and interpreter
  dependencies, checks externally supplied review/publication/execution records,
  restores each branch once and supervises the allocated methods.
- `scripts/plasticity_retention_support.py` adapts supervision from the public
  PR173 runner at `5db18164bad1c8cb46976da9e9422f2b0f13b3be`. It uses no
  unpublished PR173 results or raw artifacts.
- `scripts/plasticity_retention_contract.py` contains model-free accounting,
  projected output admission, arithmetic observation and fixed decision gates.
- `scripts/verify_plasticity_retention_run.py` audits retained data without
  importing the execution runner or SparkBrain. It requires externally supplied
  exact source/freeze pins, independently pins the published inputs, reconstructs
  current STDP sums from raw spikes, and cross-checks trace carry, actual clipped
  writes, configuration, readout receipts, final state, method journals and costs.

L takes effect at the one existing `apply` call in each occurrence. The runner
changes only the declared brain/plasticity configuration fields after native
restore. It does not clear eligibility manually or reset another state. Before
and after configuration hashes bind the exact permitted difference. A read-only
observer records old eligibility, decayed carry, current delta, unclipped
proposal, actual signed/absolute write and clipping; it never calls `apply`.

An observation or journal failure is latched. An already admitted model method
finishes and its observed primary return or original exception is preserved;
no next top-level method is admitted. Resource interrupts remain interrupts.
Method intent, return and error records are distinct. An interrupted intent is
not proof that a method completed. Each completed raw prediction is written
before its outcome. A terminal record retains a bounded last-primary summary
when ordinary logging fails. OS termination may prevent that final record;
missing completion is unknown, never zero or success.

First-suffix equality compares emitted pulses, spikes, patterns, activations,
probability and native decision. It excludes the whole-state hash, which can
legitimately differ after the first configured weight update. Configuration,
trace, retained prefix and final-state records remain separately available.

## Enforcement and limits

Each v05 worker has a 16 CPU-second/20 wall-second allowance; H/R workers have
3/5 seconds. The whole driver, its child processes, imports, file hashing,
observation and scoring consume the 360 CPU-second/480 wall-second budget.
The driver reserves each child's complete CPU allowance before spawn, then
refunds only the measured unused portion after reaping it. Git gate subprocesses
also reserve CPU and have an OS CPU ceiling. Timer interrupts cannot bypass
post-spawn kill/reap cleanup. The driver keeps a 2 CPU-second/5 wall-second
terminal closure reserve inside that budget and clamps any failure write to
actual remaining headroom; when none remains it makes no emergency write. Linux RLIMIT_AS bounds each process to 512 MiB; `wait4` records
worker peak RSS separately from driver RSS. CPU and wall timers, parent process
identity, inherited anonymous-pipe supervision and a parent-death signal prevent
an unmonitored direct worker invocation from admitting a model.

The 256 MiB output limit contains 252 MiB ordinary output and a 4 MiB terminal
reserve. Each worker may write at most 128 KiB terminal metadata, and the driver
512 KiB. Their aggregate allowances fit inside the reserve. Writes use projected
byte admission, not an instantaneous filesystem quota. stdout/stderr each have
a 64 KiB cap; overflow fails the job and reports retained, consumed and known
discarded bytes, with unread bytes explicitly unknown after failure. A failure
stops subsequent branch admission and preserves the partial directory.

The offline enforcement layer is a Python socket audit hook. This is not an
OS network-isolation claim. The interpreter/stdlib inventory and loaded module
origin checks bind actual Python source, bytecode and native-extension files;
they are not a whole-machine attestation and exclude kernel and transitive
system shared libraries. Execution uses `-S -P -B` and `PYTHONHASHSEED=0`.

## Review and commands

Initial preparation validation on 2026-10-02: all 197 focused model-free tests passed,
repository-wide Ruff passed, the immutable input regeneration check matched,
and freeze readback matched all 191 source files plus 918 interpreter/stdlib
files. The original, unexecuted manifest SHA-256 was
`2bf0d222f3527aeb43cfc5ad22978dc8b4bb24409aee4384985192baa1c9fea3`;
the dependency inventory SHA-256 is
`4415be4c41f48275151ce266f517d75765d66f8b6b2e53a500ca335ae4aaff48`.
The original freeze is superseded for execution after source review found the
paired-abstention, prototype-audit and CPU-admission gaps. Its bytes remain
retained at `freeze/`. The planned output was absent and model calls remained zero. These tests include
plain dummy subprocesses and synthetic retained-data fixtures, not dynamics
execution or a full default runtime-test run.

The current `freeze-v2/` manifest is `aea34059f16562ee8242c195517c938afa89edb261852080c6fdb3e4f1a33b56`
and binds 193 source files, including the published design/protocol prose.
All 230 focused model-free tests pass, repository-wide Ruff passes, and the
immutable input and execution-freeze readbacks match. The repairs cover paired
native-transition exclusion, complete fixed-prototype history, child CPU
reservation before admission, interruption-safe reaping, and bounded terminal
closure. Independent model-free review found no remaining blocker in those
paths. New exact-head Codex review and CI are required before merge; separate
exact-freeze approval is required before execution.

The preparation commands are model-free:

```sh
PYTHONHASHSEED=0 python -S -P -B scripts/run_plasticity_retention.py freeze
PYTHONHASHSEED=0 python -S -P -B scripts/run_plasticity_retention.py check-freeze
python -B -m pytest -q tests/test_plasticity_retention_contract.py tests/test_plasticity_retention_runner.py tests/test_plasticity_retention_verifier.py
python -B -m ruff check scripts/plasticity_retention_contract.py scripts/plasticity_retention_support.py scripts/run_plasticity_retention.py scripts/verify_plasticity_retention_run.py tests/test_plasticity_retention_contract.py tests/test_plasticity_retention_runner.py tests/test_plasticity_retention_verifier.py
```

The run command additionally requires separate exact reviewed publication and
execution-approval records. Freeze creation never creates those records or
authorizes a model call. There are no execution results at source publication.
The retained run, if subsequently approved, must undergo independent data-only
audit and publication readback before any bounded finding is reported. The audit
checks retained-data consistency and the independently supplied source/freeze
pins; it does not cryptographically prove that a process produced those data.
The published raw archive digest must subsequently bind the retained bytes.

The prefixes are exposed development fixtures, not fresh training replicates.
This is a conditional fixed-delay question, with live homeostatic and matcher
feedback. It cannot establish universal retention, unique physical mediation,
assembly benefit, energy efficiency or scientific authority promotion.
