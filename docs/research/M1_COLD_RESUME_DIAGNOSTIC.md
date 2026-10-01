# M1 cold-process serialized-state continuation diagnostic

Status: prospective source review; no model/fixture execution at this stage.
Classification: EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY, scientific credit 0.
The machine contract is `protocols/m1_cold_resume_diagnostic_v1.json`.

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
