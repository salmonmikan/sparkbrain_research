# Paired-input fixture reached acquired v0.5 state

2026-10-01 UTC. **EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**; scientific credit **0**.

## Decision

**The predeclared paired-input fixture reached actual acquired-state coverage.** After
exactly three target episodes, the real v0.5 producer held a mature, unsuppressed assembly
candidate containing exactly those three episode IDs. Its prototype and pending activation
passed both prospectively required retained-object identity checks.

This establishes an available bounded fixture for a later ownership test. It does **not**
establish transaction rollback/commit, resumability, producer-to-M1 coupling, predictive
benefit or a general acquisition ability. [PR176's coverage block and unexecuted P5/P6](v05_owned_state_results_20261001.md)
remain unchanged. No ownership test or old-probe rerun occurred here.

## Frozen question and observed result

The [prospective protocol](v05_paired_coverage_protocol_20261001.md) was published at
`b6819de0363fcd98b6bd844e0647c9a6aa9aae99`. The sole target was a 4-ms pair; single-pulse
and 40-ms spaced arms were fixed characterization controls, never alternate targets.

| Arm | Spikes in each of three episodes | Internal patterns per episode | Candidate episode count | Maturity |
|---|---|---|---|---|
| single | 2 receptor, 0 internal | 0 | no candidate | none |
| paired_4ms | 4 receptor, 6 internal | 1 | 1, 2, 3 | false, false, true |
| spaced_40ms | 4 receptor, 0 internal | 0 | no candidate | none |

All arms routed to receptors 0 and 1. The paired internal units were
`16, 23, 27, 34, 35, 46`; the pattern order was `16, 27, 23, 34, 35, 46`.
The candidate was `assembly-0001`, with mean recorded similarity 1.0 over three occurrences.
These anonymous identifiers label this run; they are not semantic or population identities.
All three first-episode immaturity gates passed.

At the target endpoint:

- `pending_activation` was mature, unsuppressed and bound to the existing candidate
- The candidate's episode-ID set was exactly the three predeclared target episode IDs
- The candidate prototype was the actual pattern object in retained result 0, pattern 0
- The pending activation was the actual activation object in retained result 2, activation 0
- The producer's retained results were the same objects returned by the three calls

These identity observations come from the reviewed live `is` checks. Saved object-ID numbers
or JSON value equality alone would not independently prove aliasing. The saved witnesses
and referenced values are consistent; no separate model reproduction was run for verification.

The expected descriptive target/control contrast was present. It is not a membrane-only
causal attribution: receptor normalization, endogenous plasticity/homeostasis, differing
call durations and persistent traces remain as specified. In each paired call, 11 edge weights
and 8 delays changed; controls changed no edges. All 64 unit thresholds changed each call. The
source-derived first-hop calculation motivated the input but did not assume these later
trajectories or guarantee maturity. No benefit of those weight/delay changes was tested.

## Execution and integrity

Independent pre-execution source review cleared exact source
`22d7aba1af0e55d58b6414cd55fe1c1ea1cd2b0d`. The runner SHA-256 was
`4b41b470bdf38ac2e7044f31345b6fc306bdb149a93c49316a926cdb3c78eeed`; the
[implementation freeze](../../artifacts/research/v05_paired_coverage_20261001/implementation_freeze.json)
SHA-256 was `349a9fbfcd92647eb9ab13c48d42f1655ac0e7bf9e8121d0729e6e4f6076ce23`.
It binds all 157 package-source files, supplementing the protocol's 27 v0.4/v0.5 hashes,
while preserving ordinary Python imports. No namespace substitution or runtime edit was used.

The cloud Linux run used Python 3.12.14 and completed once with process exit code 0:

```bash
PYTHONHASHSEED=920041 timeout -s KILL 120s \
  python scripts/v05_paired_coverage_probe.py --run-reviewed \
  --output <fresh-output-directory> \
  --source-freeze artifacts/research/v05_paired_coverage_20261001/implementation_freeze.json \
  --source-freeze-sha256 349a9fbfcd92647eb9ab13c48d42f1655ac0e7bf9e8121d0729e6e4f6076ce23
```

Actual use was exactly **3 fresh brains, 9 process attempts/completions and 15 raw pulses**.
There were no copies, native loads or outcome deliveries. No retry, extra episode, changed
input, alternate seed, threshold override, suppression or comparator search occurred.
The v0.5 prediction/action switches were disabled; the existing base v0.4 ActionAssociator
diagnostic remained active, with no outcome feedback or action-performance evaluation.

Before the manifest, the runner reported 0.972479 cumulative process CPU seconds,
0.928638 wall seconds since its internal timer started, and 25,296,896 bytes peak RSS.
These are pre-manifest samples, not exact whole-process totals. The timing origins differ;
these are resource observations, not efficiency/energy claims.
CPU 60 s, hard external wall 120 s, address space 512 MiB and artifact 32 MiB caps were not
reached. Network restriction was Python audit-hook enforcement, not OS network isolation.
The command set `PYTHONHASHSEED=920041`; the runner did not separately copy that environment
variable into preflight metadata. Source-freeze/argv and the command remain retained.

## Complete retained data and no-model checks

The run produced **92 raw files / 2,265,041 bytes**. All 91 entries in its inner manifest
match their saved bytes; the manifest intentionally excludes itself. Manifest SHA-256:
`36a92d98d094be01e6f5a58349f584a002e9e008d9e4be079e8c96567a756702`.
Raw inputs/results were preserved before gates and summaries. Initial complete configurations/topologies and initial/per-call fields/connections,
partial-capable retained-result views, native value views,
candidates, pending state, identity witnesses and first/target gates are included.

Native value views remain **incomplete ownership snapshots**. They are retained for
inspection and are not presented as complete restoration material. The empty, unwritten
runtime bytecode-prefix directory contains no evidence and is excluded from transport.

The [transport manifest](../../artifacts/research/v05_paired_coverage_20261001/transport_manifest.json)
binds two base64 parts. Their decoded xz-tar contains all 92 raw files, five exact frozen
source/protocol files and an outer manifest: **98 files / 57,948 compressed bytes**.
Archive SHA-256: `ec8046484daa8406784c60dd66d503df2568c6e03f3d4e4c254c555f589026d4`.
The deterministic archive was packaged from already saved files without importing a model.
It contains runtime source-hash manifests, not every runtime source file; those bytes remain
available at the pinned repository commit. Fresh-root distinctness likewise relies on the
reviewed constructor/retained-root checks, not independent serialized identity records.

The 13 model-free runner tests and complete-source checker passed before execution. An
independent source/data-only audit verified all raw hashes, bindings, count progression,
control rows, required raw fields, actual gate inputs and saved identity-index/value consistency.
The publication verifier independently derives the fixed result from raw rows rather than
trusting only terminal summaries. Its 13 unittest methods cover 33 validation cases; together
with the 13 runner methods, all 26 test methods pass. Scoped Ruff and whitespace checks pass.
No full local runtime/readiness/demo/benchmark sequence was rerun in this bounded scope;
exact-head CI/review are separate publication gates, not a dynamic reproduction of this run.

Verify the saved evidence without importing a model:

```bash
python scripts/verify_v05_paired_coverage_evidence.py
python -m unittest discover -s tests -p 'test_v05_paired_coverage*.py' -v
```

The verifier pins the original archive and checks safe members, source/transport/raw hashes,
fixed inputs/configs, selected result gates and saved identity-index/value correspondence.
It is an archive-consistency check, not an independent proof of live aliases, a complete
runtime-state audit or a new observation of model behavior.

## Next bounded step

A separate prospective test can now exercise a private candidate-copy transaction on an
actually acquired producer state, with complete owned-state comparisons and failure/commit
output boundaries. It must have a fresh finite contract and source freeze. It must not
relabel PR176's skipped cases as completed or infer M1 value from this fixture. The learned
representation's actual influence on prediction/action, counterfactual swaps, shams and
baselines remain later, explicit tests.
