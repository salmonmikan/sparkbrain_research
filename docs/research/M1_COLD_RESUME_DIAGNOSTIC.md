# M1 cold-process serialized-state continuation diagnostic

Current result: corrected v2 passes this bounded engineering check. All 96 future
transitions and 103 complete checkpoint comparisons agree, including the observer
control. The first 54-commit run is preserved as an incomplete harness failure;
the corrected run made 144 commits, for 198 total. No runtime was changed.

Original status at protocol freeze: prospective source review; no fixture execution.
Execution and repair history are recorded separately below.
Classification: EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY, scientific credit 0.
The original machine contract is `protocols/m1_cold_resume_diagnostic_v1.json`.
The explicit corrective contract is `protocols/m1_cold_resume_diagnostic_v2.json`;
its execution and budget supersede the original reproduction allowance below.

## Question and complementary scope

At a completed M1 cycle boundary, does the supported file checkpoint preserve the
entire serialized state and future prediction/action/revision behavior in a fresh
Python interpreter? `inspect()` equality alone is not a completeness argument.
M1 uses explicit/reference predictive memory and online centroid/evidence state;
this diagnostic does not redescribe them as emergent learned assemblies.

Source baseline: `bd337bef2edddb2d388cbcf47bf176d469c2b180`.
Human Directive index: `ops/human-directives` at
`8ce979b9ec0bc7eede5225c0403698f8886d3e8d`; relevant directive is
HUMAN-20260928-001, independent integration replay support with no scientific uplift.

Main already tests a four-cycle save plus four-cycle continuation. Open PR #164
(head `16e5b3fc48edea770f93f119f6c9a63ba7c1f301` when inspected) owns a
64-cycle same-process robustness matrix, cuts 1/8/31/63, and fault/identity
handling. It compares cycle rows and inspect/state hashes. This work does not
repeat that matrix or touch its branch. PR #167 owns outcome-identity evidence;
PR #169 owns a restricted v0.5 temporal-loop checkpoint-eligibility wrapper.

## Source map and permitted API

- `src/sparkbrain/system_build/integrated_m1.py`: `IntegratedM1Session.cycle`
  is the normal observation/action/outcome/revision transaction. The checkpoint
  manager saves SB001, SB002, compositor and world state. `load()` constructs a
  new session, and validates canonical bytes, file digests and inspect hash
- `src/sparkbrain/system_build/predictive_revision.py`: SB001 persists explicit
  hypotheses/context and a direct v0.3.2 reference-brain checkpoint
- `src/sparkbrain/v032/checkpoint.py`: direct checkpoint encodes the exact
  registered object state, including RNG, field, evidence, coalition, histories
  and observer internals. This is trusted-local data, not authenticated data
- `src/sparkbrain/v032/runtime.py`: the facade contains a shared step RLock and
  has no documented deepcopy contract
- `tests/test_system_build_integrated_m1.py` and PR #164's
  `tests/test_system_build_m1_robustness.py` define prior coverage

No production runtime, fixture, scheduler, control-plane, formal identity,
PROJECT_STATUS, or PR #164 file is modified. The experiment uses the supported
`IntegratedM1CheckpointManager.save/load` API, with no JSON repair, private
state injection, or fallback serialization.

## Frozen matrix, counts and outcomes

Use the unmodified default deterministic world for 24 cycles. Its inputs are
source-fixed, with no data/model tuning or random fixture seeds. Record the
runtime config, interpreter, platform, source file SHA-256 values and process
hashseed. The exact model default seed is recorded before the first cycle.

1. Fresh-process uninterrupted run, hashseed 1: 24 commits, raw cycle and inspect
   hash at every step; only a final diagnostic checkpoint. The session itself
   always makes transaction checkpoints internally, so "uninterrupted" means
   no explicit stop/restore and no added inter-cycle diagnostic saves
2. Fresh-process checkpoint-observed run, hashseed 1: 24 commits, additionally
   save every cycle boundary 0..24. Compare all cycle rows/state hashes and final
   full checkpoint bytes to the uninterrupted run. This detects added-save
   observer effects at the externally visible/serialized boundary. It does not
   rule out transient hidden-state differences between measured boundaries
3. Six fresh-process restorations: cuts 2/7/15 crossed with PYTHONHASHSEED 1/37.
   Save back immediately and after every remaining cycle. Compare all file paths
   and exact file bytes to the observed timeline, plus full future cycle rows
   and inspect hashes. Per seed: (24-2)+(24-7)+(24-15)=48 commits; both seeds 96.
   Total primary expected/maximum completion: 24+24+96=144 committed cycles;
   retain actual row/commit counts on early stop

Serialized-byte divergence and future-cycle/action divergence are separate
outcomes; bytes alone do not establish behavioral corruption.

A cycle row includes observation, prediction/action, receipt and revision. Full
serialized file equality is exact, with no float tolerance or digest-field
normalization. File SHA-256 records summarize exact-byte comparisons, not just
inspect projections. Record first divergence with both complete payloads.
A PASS concerns this finite history in one interpreter environment, not every
reachable state, future input, Python version, or serializer completeness proof.

## Separate API-boundary diagnostics

At quiet cutpoint 7, try ordinary `copy.deepcopy` once and retain its exception
if unsupported. Do not bypass facade locking or call this file restoration.
No deepcopy result contributes continuation rows or the primary conclusion.

On a separately loaded cutpoint-7 session, obtain `session.world.next_observation()`
and pass exactly that to `pilot.observe` once, without `world.resolve`. This is a sequential pending state, not a concurrent save.
Save/load/save and compare bytes. Then call `Session.cycle` once: a pending event
may make it reject, because it begins with a new observe instead of completing
a pending action. Preserve the exact error and prove no-write with a new save.
A successful state roundtrip and lack of an automatic mid-cycle resume API are
separate outcomes. Do not call this an unsupported checkpoint corruption or a
failure of the documented quiet-boundary continuation contract. No outcome
commit is expected from these secondary probes. If `Session.cycle` unexpectedly
succeeds, retain the cycle output and record its actual commit count separately
rather than hiding a budget deviation.

## Freeze, resources and failure handling

Protocol is committed before any runtime/fixture call. Runner implementation is
source-reviewed and committed separately before running the matrix. Source SHA
and protocol SHA appear in STARTED and raw provenance. Outputs use an absent
explicit local directory; no overwrite and no hidden upload during execution.

Sequential workers: 120-second wall timeout each, 90 CPU seconds each, 1 GiB
address-space cap, 1,200-second overall wall deadline, 64 MiB retained-output cap.
Check the disk cap at every snapshot and worker completion. All completed raw
rows are flushed before the next transition; preserve stdout/stderr, STARTED,
exceptions and partial outputs. On any primary mismatch, retain both divergent
payloads and stop scoring that case. No failed row is dropped, no silent retry,
and no outcome-responsive retuning. A launch/timeout/resource/runner error is an
incomplete diagnostic, distinct from an observed continuation mismatch.

At most one separate clean reproduction may run the identical frozen matrix under
a new output path (another 144 primary commits, at most 288 across both matrices); retain both provenance records and compare deterministic raw
contents. Resource/output/time caps are per matrix, including secondary attempts. No formal
or historical experiment is executed or reclassified.

## Verification and boundaries

Add focused tool-contract tests for exact inventory/file comparison, first
mismatch reporting, output no-clobber and outcome aggregation. Those tests use
synthetic files and do not consume this runtime diagnostic. Run repo lint,
local readiness, default pytest and bundle validation; full scientific or
formal reproduction suites are out of scope. Preserve negative observations
in this report and a separate dated Results Ledger entry after coordination.

No external paper is needed to justify an exact replay engineering invariant.
Prior-art novelty is not asserted. Runtime source/API contracts are primary.

## Independent source-only review

Before M1 execution, a separate reviewer read protocol/source and confirmed the
fresh-interpreter/full-byte scope complements PR #164. Four requested boundaries
were clarified prospectively: per-matrix versus reproduction budgets, unexpected
pending-cycle commit accounting, observer-control limits, and separate byte/behavior
divergence classification. Review involved no runtime execution.

The independent runner audit caught a pre-execution error-handler no-clobber
defect: a rejected existing output directory could receive a new error file.
Output ownership is now tracked explicitly, with CLI-level synthetic regression
checks for all five modes proving every pre-existing byte remains untouched.
This repair occurred before any M1 diagnostic run.

Matched intermediate restored payloads are deduplicated only after exact byte
comparison: restore-<hashseed>-<cut>/file-records/step-NNN.json maps to the retained
observed/checkpoints/step-NNN directory. Initial/final restored checkpoints and
all divergent checkpoints are retained in full. STARTED also records schema-asset
hashes and installed jsonschema/NumPy/Torch versions without importing them.
Summary failures distinguish serialized bytes, future transitions, observer
effects, timeouts and incomplete worker/resource/runner paths.

## Preserved original run and explicit v2 repair

The original run at `3addef5bc9c4494f23b38b2e28e2f9e02958cdca` made 54 primary
commits: baseline24 + observed24 + six first resumed steps. All six restore
workers stopped at the first transition because the runner compared live nested
tuples with JSON-loaded lists. Their retained left/right JSON records, inspect
hashes and complete saved checkpoint bytes are identical. The original summary
and every raw file remain unchanged in `original.tar.gz`; a separate read-only
analysis records why the runner's original `future_transition_mismatch` labels
are not evidence of runtime behavior divergence.

The v1 protocol is preserved unchanged. The explicit v2 amendment changes only
cycle-row equality to exact canonical JSON bytes (the existing raw-row contract),
with a synthetic tuple/list regression and an int-versus-float non-normalization
check. It does not change runtime, inputs, cuts, seeds, horizon, thresholds or
state equality. Byte equality remains exact with no normalization.

Before correction execution, independently review and commit the amended runner
and `protocols/m1_cold_resume_diagnostic_v2.json`. Allow one corrected 144-commit
matrix only: at most 198 actual primary commits across the original and corrected
runs. No additional clean reproduction is authorized by this amended diagnostic
budget. Preserve both runs and report the failed/incomplete harness honestly.

Independent read-only review verified all six original JSON pairs and six full
checkpoint inventories agree, and source-traced live tuple preservation through
dataclasses.asdict. The canonical-row repair was reviewed with numeric and order
change rejection tests. The single corrected 144/total198 budget was approved
before execution. Original compressed bytes are transported in ordered base64
parts under `artifacts/m1_cold_resume_diagnostic_20261001/original.parts/`;
its manifest binds the reconstructed archive SHA-256.

## Corrected result and interpretation

Corrected execution pin: `642c61a3a950aea176cb284eb7df44f7bc09bcbc`.
Runner SHA-256: `3c5f8082a3a648c689757bfdd5c5e44fc108d59d73e41e6ec10e983b814b5504`.
V2 protocol SHA-256: `b61db091642a050441e06efebc92e7c1df8e1ca0cc81af91f04de60e76f105ec`.

- Both baseline and checkpoint-observed runs completed 24 cycles with equal raw
  JSON observations/actions/receipts/revisions and inspect hashes, plus equal
  full final checkpoint bytes
- All six true cold restorations completed their 48 + 48 = 96 future transitions
  without a prediction, action, outcome, revision, inspect-hash or file-byte
  mismatch. Six immediate restore/save-backs plus 96 future saves and the one
  observer final check give 103 complete six-file comparisons (618 file pairs)
- The sequence includes abstention, act_alpha and act_beta. This is one fixed
  deterministic two-region fixture, not a diverse task or generalization suite
- Ordinary deepcopy failed with TypeError: cannot pickle '_thread.RLock' object
- A sequential after-observe pending checkpoint roundtripped exactly. Calling
  Session.cycle then rejected the unresolved event, and every serialized byte
  remained unchanged. This separates checkpoint preservation from an automatic
  mid-cycle continuation API; no secondary probe committed a cycle

The corrected bundle contains 446 files  / 5,211,555 uncompressed bytes and stayed
within the frozen per-worker/overall/output caps. The longest observed worker
wall duration was about 1.47 seconds; this is execution provenance, not a speed or
energy comparison. Linux / Python 3.12.14 was used throughout. Installed dependency
versions were jsonschema 4.26.0, NumPy 2.5.3 and Torch 2.13.0+cpu; installation does
not imply those optional backends contributed to this default explicit/reference
path. Address-space and CPU caps were enforced; no peak-RSS measurement is claimed.

All results remain EXPLORATORY_NON_EVIDENTIARY with scientific credit 0. Exact
restoration of these serialized snapshots is not proof that the serializer covers
all future/alternative reachable states. No cross-version portability, concurrency,
crash consistency during a write, model capability, composition contribution,
scientific novelty, biological fidelity or energy claim follows.

## Artifact access and data-only verification

`artifacts/m1_cold_resume_diagnostic_20261001/` contains:

- original.parts/: ordered base64 chunks and manifest reconstructing the exact
  gzip original archive, SHA-256
  `89c9c964ecfcdf2abce2bb37111f53a4a814e15f0e8c5c3bd70d4519321a4794`
- original_analysis.json: separate read-only attribution of the preserved
  original harness failure; the original summary is not rewritten
- corrected.parts/: ordered chunks/manifest for a lossless xz archive, SHA-256
  `8a4d423371ca1dc45d72d22a231c1651f839a975502f58b5834dd59495951210`
- verification.json: data-only recomputation of counts, raw comparisons, source
  protocol bindings, archive integrity and the original failure attribution

Run without executing any M1 dynamics:

```bash
python scripts/verify_m1_cold_resume_artifacts.py
```

The verifier uses only the standard library, checks transport and raw inventories,
rejects unsafe/duplicate archive members and verifies the retained raw observations,
full initial/final snapshots and intermediate deduplication hash mappings. It does
not launch a model or replay the exhausted diagnostic. It also confirms the two
attempts' baseline and observed raw streams are identical.

### Review follow-up: independent integrity and provenance anchors

The first publication's verifier relied on self-described archive inventories and
underchecked execution provenance. Codex identified both as P1 verification gaps.
The unchanged original and corrected archives are now bound to
`protocols/m1_cold_resume_artifact_anchors_v1.json`, whose SHA-256 is pinned in the
verifier. This post-execution audit record was created from the already-published
bytes; it is not a prospective experiment protocol or fresh scientific evidence.

The anchors fix both archive digests/sizes and the complete 356-file original and
446-file corrected inventories, including their internal inventory files. Rewriting
the transport manifests and internal inventories cannot substitute a truncated or
changed archive. These are reviewed repository integrity anchors, not an external
signature against a party that can replace the verifier and its trusted source.

All 157 runtime-source and 15 schema hashes were independently checked against
Git objects at baseline `bd337bef` and both execution pins. Each frozen runner and
protocol was also checked against its execution commit. Verification checks the
top-level embedded protocol, execution commit, source/schema manifests, runner,
interpreter, dependency provenance and zero-credit binding, then all nine worker
STARTED records per attempt against expected mode/cut/hashseed/reference and
common runner/protocol/interpreter fields. Worker configurations and process
identities are checked too. Tamper tests exercise rewritten transport, missing raw
files, changed anchors, source metadata, every worker's protocol, mode parameters,
interpreter and configuration without importing or running M1.

### Recorded execution commands

The original and corrected matrix commands were, respectively, at their recorded
source pins, using the same interpreter executable:

```bash
python scripts/m1_cold_resume_diagnostic.py --output /absolute/absent/original
python scripts/m1_cold_resume_diagnostic.py --output /absolute/absent/corrected
```

These are provenance/reproduction instructions, not permission for another run
under the completed 198-commit budget. A new execution needs its own explicit
bounded diagnostic allocation. Read-only artifact verification does not.

## Next useful engineering boundary

If future integration needs recovery with an outstanding external outcome, define
an explicit receipt-journal/pending-action resume contract before adding a resume
entry point. The present result supports using completed-cycle checkpoints on
this reference path. It does not warrant a production checkpoint repair or a new
scientific claim.

The current runner additionally has an outcome-independent portability guard after
the recorded execution: Windows may import its pure file/row helpers, but bounded
execution fails explicitly if POSIX resource limits are unavailable. The data-only
verifier remains standard-library portable. Exact replay provenance refers to the
recorded execution pin, not an assertion that later wrapper edits were rerun.

## Local validation at publication

- Focused outcome-independent harness and data-only archive checks: 16 passed
- Default regression selection: 697 passed, 392 deselected, one existing
  Starlette/httpx deprecation warning, 45.10 seconds (Python 3.12)
- Repository-wide Ruff: pass
- Local readiness: pass, CPU-only reference path, no core runtime network dependency
- Standard demo and 40-episode/30-step benchmark commands: pass in separate absent
  scratch output directories, with no historical artifact overwrite
- Bundle validation: pass, 88 required files; its generated validation manifest
  was retained separately and the tracked shared manifest left unchanged
- Data-only diagnostic artifact verification: pass; no additional M1 matrix run

Logs are under the diagnostic artifact's `validation/` directory. These are
regression checks, separate from the 198-commit bounded diagnostic allocation.
The 392 scientific/reproduction/external-marked tests were not executed. Remote
CI and review must be checked on the final PR head before merge.

After the verifier review repair: 71 focused checks and 752 default tests passed
(392 deselected; the same existing dependency warning). Repository Ruff, local
readiness, bundle validation and data-only verification passed again. The generated
bundle-validation manifest was retained outside the tracked shared manifest.
`validation/pytest-review-fix.log` retains the default regression output. The two
original raw bundles, their protocol bytes and every result row remain unchanged;
no additional diagnostic matrix was executed.
