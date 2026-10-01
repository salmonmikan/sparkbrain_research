# v0.5 owned-state probe: acquired coverage remained blocked

2026-10-01 UTC. **EXPLORATORY ENGINEERING / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit: **0**.

## Decision

**The acquired-producer transaction prerequisite is not cleared.** The three fixed Q
episodes generated receptor spikes but no internal activity patterns or assembly candidates.
The maturity gate therefore blocked P5/P6. No extra episodes, alternative stimulus, tuning,
or repeat of the model run was attempted.

Whole-graph copying did preserve the exercised fresh, receptor-only, hand-constructed
transient and changed-edge-order states. That narrower result does not establish rollback
or commit/output ownership for a mature acquired representation, nor the later M1 inlet.

The [reviewed proposal](v05_owned_state_rollback_20261001.md) was published at
`ee43c2141197ef9f094db56e4a8c9c5a42eb9edd`. Source review stopped the first implementation
before execution and required the corrections described there. The only model run used
reviewed source `7578f7aac1a915da9fc90541f71bdc6bb97b37f0`, runner SHA-256
`4ac7f630a0f1094a0952df28b0ec3313ecd5ae885d9c4b1d135bea7904f13913`.
Production runtime is unchanged from `00ef5bac171b3ec05f581a157cccd9528bb71e8f`.

## What happened

| Case | Observed result | Boundary |
|---|---|---|
| P1 fresh graph/isolation | Passed | Complete copied inventory matched; mutating the selected copied unit/edge did not change the original |
| P2 acquired prefix/end-episode | Coverage blocked | Each of the three prefix episodes emitted two spikes at receptor unit IDs 0 and 1; zero patterns, zero candidates, null pending activation |
| P2 continuation comparison | Copy matched direct | Fixed boundary was quiet-eligible; full copy inventories and suffix outputs matched direct; native full inventory differed but suffix output matched |
| P3 in-flight component fixture | Copy matched direct | Nonempty pending detector/queue state was preserved by the copy; native suffix contained one cascade versus two in direct/copy |
| P4 changed outgoing order | Copy matched direct | Copy preserved live order; native source-0 targets reordered from `[16,23,35]` to `[23,16,35]`; suffix outputs still matched |
| P5 acquired-state abort | Not executed | Required acquired-state coverage absent |
| P6 acquired-state commit/output isolation | Not executed | Required acquired-state coverage absent |

P2's first-episode immature control was preserved, and its prefix was exactly three
separately identified Q episodes at 8/208/408 ms. Three distinct episodes were necessary
for default maturity, but did not suffice: there was no assembly candidate to mature.
The six spikes were all receptors (the saved field has receptor IDs 0–15). This result
concerns this fixed input/configuration and does not show that v0.5 cannot acquire assemblies.

P3 is explicitly a hand-built component-state fixture: four valid spike objects at 0–3 ms
were inserted into detector/tracker state after the empty field advanced to 3 ms, with a
future arrival queued at 4 ms. Native loading lost the prepared 0–3 ms cascade. The actual
suffix spike sequences nevertheless matched across direct/copy/native. Hash differences
also include numeric normalization, such as clock `3` to `3.0` and later unit-0 update time
`4` to `4.0`. Do not attribute every hash change solely to a lost cascade or call this a
changed prediction; v0.5 prediction/action were disabled in this probe.

## Native differences, including initially unclassified regions

Native checkpoints did not preserve complete type/alias-aware state in any of P2/P3/P4.
The raw artifacts distinguish source-expected loss regions from other changed regions.
A read-only post-run inspection found:

- Connection dictionaries preserve identical type-tagged keys and values, but insertion
  order changes in all three native copies
- P2 rate-EMA and trace value trees agree, while dictionary insertion order changes;
  this includes 12 dictionaries in base trace and 30 in top-level trace
- P3 field clock is normalized from integer to float without a numeric-value change
- The already identified omissions, tuple/list conversion and reconstructed adjacency/aliases
  remain visible in the complete saved inventories

These distinctions prevent a diagnostic/hash mismatch from being presented as a prediction
or spike-trajectory failure. They do not rewrite the historical checkpoint's accepted scope.
A matching persisted hash would still be insufficient for a complete ownership snapshot.

## Execution and retained evidence

The command was run once in the cloud Linux workspace, using Python 3.12.14:

```bash
PYTHONHASHSEED=920041 timeout -s KILL 120s \
  python scripts/v05_owned_state_probe.py --out <fresh-output-directory>
```

The execution returned exit code 0 with status `coverage_blocked`, not a completed acquired
transaction result. Counts were four fresh v0.5 constructions, three native loads, four
whole-brain copies and 12 pulse-processing calls, below the fixed maxima of 11 constructions/
loads, seven copies and 28 calls. The worker reported 0.945033 cumulative process CPU seconds
and 0.905780 wall seconds after its initial source checks. These have different timing
origins and are not an efficiency comparison. Address space was limited to 512 MiB; peak
memory was not separately recorded. Network denial used Python socket audit, not an OS
network namespace.

All **47 raw files / 4,688,900 bytes** are preserved. The run manifest covers 46 files,
with itself intentionally excluded; its SHA-256 is
`8d5f2b3b194930535738be6b2b3aa48a355df460eaf8bebf9367a86dc7334d22`.
There are 16 unique complete graph inventories and 28 artifact links to those graphs.
The transport archive additionally contains the five exact source-freeze files and its
own member manifest, for **53 files total**. Archive size is 64,052 bytes and SHA-256 is
`cf0d5b5a57589f28a597ceded382c6334579ba1a8b5d1e2f7a795c3b31299405`.

The [transport manifest](../../artifacts/research/v05_owned_state_20261001/transport_manifest.json)
identifies two base64 parts. Validate hashes and selected raw assertions without importing
or running a model:

```bash
python scripts/verify_v05_owned_state_evidence.py
python -m pytest -q tests/test_v05_owned_state_evidence.py
```

The verifier checks the pinned archive, inventories/hashes, graph-content hashes, direct/copy
suffix comparisons, absent acquired state, blocked-case absence and source bindings. It is
an artifact-consistency check, not a new dynamic reproduction or proof of every runtime
invariant. Four no-model publication tests pass, along with scoped Ruff and whitespace checks.
Full runtime tests and historical experiments were not run as local validation in this
bounded scope; exact-head CI and Codex review are separate publication checks.

Independent read-only audit found no integrity discrepancy, verified all file/graph/source
bindings and graph references, independently checked the additional native regions, and
confirmed P5/P6 nonexecution. No model was rerun for that audit or for packaging.

## Consequence for the next step

Preserve this coverage block. It would be inappropriate to lengthen or retune this run
and turn it into an acquired-state success. A separately specified input-characterization
step could identify a fixed stimulus that actually reaches internal patterns before a new
ownership test is proposed. The current result supplies useful state-copy and native-loss
boundaries, while mature-state abort/commit, representation-to-M1 coupling and predictive
benefit remain untested.
