# Restricted ownership of acquired v0.5 state was observed

Run: 2026-10-01 UTC. Report: 2026-10-02 UTC.
**EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**; scientific credit **0**.

## Decision

The one frozen ownership test met its restricted acquired-state boundaries. Both specified
transaction faults left the original producer's complete supported typed/reference graph
unchanged. The successful private-owner commit matched its direct reference and remained
unchanged after all nine caller/output metadata mutations.

This is a candidate-copy/abandonment strategy around this acquired producer. It is not a
native restoration algorithm, supported checkpoint API, arbitrary-backend guarantee,
full crash-recovery result, M1 joint transaction or learned prediction/action benefit.
The exact v0.5 prediction/action/reward-modulation switches remained disabled. Existing base
v0.4 action diagnostics and all other supported owned instance state were included.

[PR176's earlier coverage block and skipped P5/P6](v05_owned_state_results_20261001.md)
remain unchanged. [PR177](v05_paired_coverage_results_20261001.md) supplied an acquisition
sequence; this separate diagnostic used fresh identities and rechecked actual maturity.
Neither prior probe runner was imported or executed.

## Frozen plan and actual result

The [prospective protocol](v05_acquired_ownership_protocol_20261001.md) was published at
`9b936b4f2cbea3865b178e13e65e6906971ea586`. One private root received the fixed three
paired Q episodes at 8/12, 208/212 and 408/412 ms. Its candidate contained exactly the three
new episode IDs, with actual mature pending state and retained prototype/activation aliases.

All four whole-brain copies were created with separate deepcopy memos from that same
unchanged acquired beforestate, before any branch processing. Every copied graph matched
its complete typed/reference bytes. All ten pairwise mutable-identity intersection witnesses
among the root and four copies were empty. These are source-backed live observations;
serialized graph labels alone cannot independently prove live cross-copy identity.

Each branch then received the same fresh suffix ID and pulse bytes at 608/612 ms:

| Branch | Observed boundary |
|---|---|
| export_abort | Real processing returned mature four-episode state; detached output and graph were validated, then the specified export-boundary exception occurred through the owner transaction. The original graph/pointer remained exact |
| event_cap_abort | The private event-cap replacement was followed by a genuine field-processing exception and state changes beyond that replacement. The owner graph/pointer remained exact |
| direct_reference | Successful suffix produced the reference complete graph and detached output, without publishing the owner pointer |
| commit | Candidate graph and detached output exactly matched the reference before the sole owner-pointer assignment. It returned mature four-episode state and passed all external mutation controls |

Both fault branches traversed the same `PrivateOwner.transact` boundary as successful
commit. A source-preparation gap in their initial manual-fork placement was corrected before
the implementation freeze; no model ran with that earlier preparation. The direct-reference
branch alone deliberately remained outside the owner transaction.

The acquired original graph's canonical content digest was
`e7d18fd8f59c399a8d3fb136e73f273220f8293625d8e463051f3b5cc019482d`.
The successful direct/commit graphs shared digest
`17572a61a68edf01e39ed26a604b3e5e83378f1d72cfb0e9a54b024de35a47c9`.
The runtime comparisons used **complete canonical graph bytes**; these hashes merely locate
the retained inventories. Native/output hashes were not substituted for state equality.

## The processing fault changed real private state

The event-cap branch separately preserved its exact clone, after-config state and failed
processing state. Only that private candidate's `max_events_per_run` was replaced by 1.
The actual error was `RuntimeError("max_events_per_run exceeded")`.

Beyond the configuration replacement:

- Receptor Q observations advanced from 6 to 8, with its last observation moving from
  412 to 612 ms
- The total arrival counter advanced from 150 to 152; last-run arrival count was 2
- The queue counter advanced from 150 to 154, and two 612-ms arrivals remained queued
- Field clock stayed at 444 ms; no new spike occurred, with last-run spike count 0 and
  total spike count 30 unchanged

The exception occurs while collecting the second simultaneous arrival, before delivering
the group. No spike or field-clock advance was required. This is a real partially updated
candidate, not a successful fault witness obtained merely by changing its configuration.
The candidate was abandoned; the original retained its exact complete graph.

The separate `InjectedExportValidationError` was a deliberate boundary injection after
successful processing and output validation. It is not a claim of a naturally occurring
export defect. Both failures occurred before any owner-pointer commit.

## Commit, aliases and outward mutation

The successful candidate and direct reference ended with field clock 644 ms and receptor Q
clock 612 ms. Their pending activation was mature, unsuppressed and bound to exactly all
four episode IDs, in the newest retained result. The candidate prototype still referenced
the first retained pattern. Complete reference graphs also retained v0.5/v0.4 result links,
emitted/base input links, connection adjacency aliases, detector/memory state, topology/live
separations and all declared instance fields.

All fallible model, copy, export, inspection and comparison work preceded the pointer
assignment. After the actual return, nine externally held metadata dictionaries were changed:
two real caller-pulse dictionaries; exported top-level metadata; two exported raw-pulse,
two emitted-pulse and two nested v0.4 input-pulse metadata dictionaries. Each received the
predeclared nested value. The full committed graph and old acquired-root graph remained exact.
The driver retained the before/after external bytes and mutations.

Live identity witnesses and reviewed `is`/mutable-ID checks support these observations.
JSON values and numeric IDs do not independently recreate live aliases or establish
isolation from arbitrary external code. The test was single-threaded and exercised the
fixed owned graph and API paths, not concurrent callers or a public production interface.

## Execution, budget and limits

Independent pre-execution review cleared exact source
`6dd7e8a014d66232509355687b14579c03838962`. Runner SHA-256:
`d24730db318749deba4428ea7d26d283181bc3a91353d268eb2528f23db2bc7d`.
The [implementation freeze](../../artifacts/research/v05_acquired_ownership_20261001/implementation_freeze.json)
SHA-256 is `a1e405e6669d879d570d01d443e21df1c149a93f1c064790e15adae7462fe629`.
It binds the runner/tests, all 157 runtime source files, the 16-file/50-class graph schema
and the attributed reuse sources. Ordinary Python imports were preserved.

The sole Linux/Python 3.12.14 command returned process exit code 0. This abbreviated
display uses placeholders; preflight and the freeze retain the exact interpreter/output
paths, and the runner requires that exact frozen output directory:

```bash
PYTHONHASHSEED=920041 timeout -s KILL 120s \
  python -B scripts/v05_acquired_ownership_probe.py --run-reviewed \
  --output <fresh-output-directory> \
  --source-freeze artifacts/research/v05_acquired_ownership_20261001/implementation_freeze.json \
  --source-freeze-sha256 a1e405e6669d879d570d01d443e21df1c149a93f1c064790e15adae7462fe629
```

Actual use matched the complete plan: **1 fresh root, 4 whole-brain copies, 7 process
attempts, 14 submitted raw pulses, 6 process returns, 1 expected processing exception,
2 aborted transactions and 1 owner commit**. Input/output detachment was separate from the
four whole-brain copies. There were no native loads, outcomes, M1 calls, extra episodes,
retuning, retry or dynamic reproduction. Publication used the unchanged finalized raw files.

Before manifest writing, resources were sampled at 2.383781 cumulative process CPU seconds,
2.333607 wall seconds since the internal timer and 48,984,064 bytes peak RSS. These are
pre-manifest samples with different timing origins, not whole-process totals or efficiency
claims. The CPU 60 s, hard wall 120 s, address-space 512 MiB and artifact 32 MiB limits were
not reached. The actual timeout parent arguments were recorded. The command set
`PYTHONHASHSEED=920041`; the environment variable was not separately asserted/recorded by
the runner. Network denial was Python audit enforcement, not OS isolation. SIGKILL/OOM can
prevent finalization and was not exercised.

## Retained evidence and publication checks

All **160 raw files / 5,812,592 bytes** are retained. The inner manifest has 159 entries,
excluding itself; its SHA-256 is
`1643c08681d6ffd59aa839c05a28632770635fedd105e6b467aa9ed656243e95`.
There are **17 complete typed/reference graph inventories and 57 graph-pointer records**.
Raw results/errors and full graph data were preserved before gates and summaries.

The [transport manifest](../../artifacts/research/v05_acquired_ownership_20261001/transport_manifest.json)
binds four base64 parts. Their decoded xz-tar contains all 160 raw files, eight exact frozen/
provenance source files and an outer manifest: **169 files / 136,964 compressed bytes**.
Archive SHA-256: `632088e5618a035aec5a6b2fb6ba7ab1dd34510de53bac3b17fd681546ce7e0b`.
The deterministic packaging used saved bytes only. The data is synthetic; publication also
includes absolute cloud paths, process IDs, container hostname, platform/kernel/Python/compiler
versions, execution arguments, hashes and resource samples. Independent inspection found no
personal payloads or common credential patterns. The empty bytecode-prefix directory is
excluded. Runtime source hashes are retained; all runtime source bytes remain available at
the pinned repository commit rather than being duplicated in this archive.

The 16 model-free runner tests, exact source checker and scoped Ruff passed before execution.
Independent source/data/archive audit verified all raw bytes, graphs and reference structure,
actual maturity/count/fault gates, and all nine external mutations. The publication verifier
independently reconstructs the fixed result from saved graphs/rows rather than only trusting
terminal booleans. Its 12 unittest methods and the 16 runner methods all pass: **28 model-free
test methods**, with scoped Ruff and whitespace/link checks passing.

Validate the saved evidence without importing a model:

```bash
python scripts/verify_v05_acquired_ownership_evidence.py
python -m unittest discover -s tests -p 'test_v05_acquired_ownership*.py' -v
```

The verifier pins the original archive; checks transport/member/source/raw hashes, all graph
schemas/references and byte comparisons; and derives selected ownership, maturity, count,
fault and external-control checks. It establishes archive consistency supported by reviewed
live code, not dynamic reproduction or independent proof of former live object identity.
Exact-head CI/Codex review remain separate publication gates. Full local runtime/readiness/
demo/benchmark validation was outside this bounded scope; no model was rerun for publication.

## Consequence for the interface

For this restricted acquired-assembly state and these two precommit faults, the private
candidate-copy approach has an observed ownership boundary. Later work still needs an
explicit real representation export and consumer connection, receipt/context separation,
capacity prechecks, delayed-outcome binding, swap/sham controls and interchangeable
baselines. No learned prediction/action ownership, M1 contribution, arbitrary-state copy
support or general causal benefit was tested here.
