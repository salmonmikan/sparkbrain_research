# M1 checkpoint compatibility and rejection-stage diagnostic

Current result (2026-10-01 UTC): the single frozen ten-case load diagnostic completed
with zero dynamics transitions. Both valid controls restored exactly, all seven
invalid schema/config cases rejected, and the outer boolean schema tag was accepted
and normalized to integer 1 on save-back. This is bounded source-contract behavior,
not a security vulnerability or general compatibility claim. Full retained results
and data-only verification instructions follow the historical protocol below.

## Historical prospective protocol and review record

Status: prospective source-only proposal; no fixture construction, checkpoint load
or dynamics execution has occurred for this diagnostic. Classification:
EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY, scientific credit 0.

## Useful gap and what this question does not assume

The public `IntegratedM1CheckpointManager.load(directory)` constructs a new
session. It does not accept an existing session or an expected deployment config.
It validates the outer identity and file digests, then loads predictive and scope
components, validates compositor bindings, reconstructs the world, and finally
checks the integrated state hash before returning.

Thus the relevant boundary is whether an invalid candidate is returned or input
files are changed. “Reject before any mutation” would be misleading: nested
validation may occur after temporary objects are constructed. This experiment
cannot establish atomic deployment replacement, crash recovery, concurrent
save/load safety, absence of every heap/global side effect, or arbitrary version
compatibility. A valid saved configuration that differs from current defaults is
not automatically an incompatible checkpoint; the API restores saved config.

The bounded new question is how the integrated loader rejects unsupported nested
schema identities and inconsistent/invalid config after transport checks pass,
and whether the rejection stage is early outer preflight or later component
construction. One prospective type-alias probe separately checks whether JSON
`true` is accepted where schema version integer `1` is expected. Source comparison
uses ordinary Python equality, so acceptance is a source-derived possibility,
not an executed result or a reason to silently change production code.

## Source and existing coverage

Source pin: `367904e10525ca43ac066ff9fc0701fa89e6b91e` (main after PR #170).
Repository AGENTS blob: `b5177647ef4f4b86f2c4208bd5e93008ec0a2d0b`.
Human Directive index: `ops/human-directives` at
`8ce979b9ec0bc7eede5225c0403698f8886d3e8d`. Integration/recovery work follows the
bounded engineering intent of HUMAN-20260928-001 without altering authority.

Relevant source paths and stages:

- `system_build/integrated_m1.py:738-778`: outer identity/inventory/digests,
  component loads, compositor/world reconstruction, final hash and return
- `system_build/predictive_revision.py:618-638` and `:500-585`: direct reference
  brain is loaded before predictive schema/config/hypothesis validation
- `system_build/causal_scope_revision.py:741-769` and `:923-941`: payload digest,
  schema/config, exact router-config agreement and restored hash
- `v032/checkpoint.py:369-421`: bounded bytes, exact envelope, schema/class,
  transport digest, strict canonical bytes, object reconstruction, restored hash

Paths above are relative to `src/sparkbrain/`; exact source SHA-256 values are in
the machine protocol. A source check is not an execution claim.

Existing tests already cover ordinary continuation, outer digest tampering,
no-clobber writes, unknown direct checkpoint classes/nodes/root attributes,
component state completeness and rejection of the old SB002 schema. PR #164 at
`16e5b3fc48edea770f93f119f6c9a63ba7c1f301` owns 64-cycle same-process replay and
transaction/receipt/event faults. PR #170 covers true cold same-version full-byte
continuation. This proposal repeats none of those matrices. It adds integrated
nested compatibility/rejection-stage cases with zero future transitions.

## Frozen ten-case matrix

Two positive controls, seven expected semantic rejections and one descriptive
schema-type probe, exactly one main loader call per case:

1. C01: untouched retained cut-7 checkpoint; expect acceptance and exact save-back
2. C02: new, zero-cycle session with predictive context_gate 0.25 and scope
   minimum_confidence 0.65; expect preserved valid nondefault configs
3. C03: outer manifest schema_version 2; expect outer identity rejection before
   either child loader
4. C04: outer manifest schema_version true; characterize acceptance/rejection
   and any save-back normalization, without assuming strict type rejection
5. C05: predictive pilot schema_version 2; expect predictive identity rejection
6. C06: direct reference-brain schema_version 2; expect direct schema rejection
7. C07: scope payload schema_version 3; expect scope identity rejection
8. C08: compositor schema_version 2; expect compositor identity rejection
9. C09: missing predictive config context_gate; expect config-shape rejection
10. C10: scope config minimum_confidence 0.65 while its router config stays 0.60;
    expect explicit router/config mismatch rejection

C01 and mutations use the already-published corrected PR #170 checkpoint at
`observed/checkpoints/step-007/`, from archive SHA-256
`8a4d423371ca1dc45d72d22a231c1651f839a975502f58b5834dd59495951210`.
This is deliberate reuse of an exposed engineering fixture, not an independent
scientific replicate. It requires no original matrix rerun. C02 uses public
constructors only and performs no observation, action, feedback or world step.

Mutations occur only in isolated temporary fixture copies. Change exactly the
listed semantic field and only the listed transport digests to isolate that defect:
outer file digest; scope payload digest for C07/C10; direct payload digest for
C06. The direct loader checks schema before payload digest; the C06 refresh keeps
its envelope consistent rather than being needed to reach that guard. Never repair
semantic state hashes, compositor/component bindings or the
inconsistent configuration. Preserve full before/after bytes and mutation lists.
No source archive or checkpoint is overwritten.

## Measurements, controls and stopping conditions

Record each loader return or exact exception, ordered delegated call/return/error
milestones, complete input-file hashes before and after, any returned inspection
and state hash, preserved config, and one save-back per accepted candidate.
Outcome-neutral wrappers must delegate unchanged functions and restore themselves
in finally; they may not inject state or change loader results. Phase-tag events
as setup, primary-load or save-back. DirectCheckpointManager.save internally calls
_load_bytes to reconstruct and validate its output, so save-validation events must
not be mistaken for the primary load’s rejection stage. Input-file equality
is reported separately from object-construction stage. Failed candidates produce
no public returned session; temporary allocations are not called persistent writes.

Budget: exactly ten planned primary integrated load attempts, zero dynamics
transitions, one new fixture save and at most ten accepted-candidate save-backs.
Those saves permit at most eleven additional mandatory direct reconstructions,
for at most twenty-one including direct loads inside the primary attempts.
Use one setup process and at most ten case processes, strictly sequential. Each
process is limited to 30 wall/CPU seconds and 1 GiB address space, activated before
runtime import; setup and save-back are included. The overall wall cap is 330
seconds and retained-output cap 32 MiB, enforced during writes and completion.
No clean reproduction or retry is allocated. Keep blocked/incomplete rows
and distinguish infrastructure failures from semantic rejection. Primary-load and
save-back outcomes are separate: a save-back error cannot turn an accepted primary
load into a reported rejection. An unexpected acceptance remains a result and never triggers outcome-dependent protocol repair.

The machine contract is `protocols/m1_checkpoint_compatibility_v1.json`. Commit it
and finish independent source-only scope review before any model import/fixture
construction. Then implement/source-review a runner and synthetic contract tests
before a separately recorded bounded execution go-ahead for this frozen matrix. No runtime
patch, migration policy, new hot-swap API, formal identity or broader compatibility
claim is authorized by this proposal.

## Why this matters for continuous learning

A durable learner needs to distinguish an unreadable candidate, a saved valid but
nondefault configuration and an actually incompatible schema/config combination.
This diagnostic can document where the current read-side guards sit and whether
saved configuration semantics are explicit enough for a future recovery controller.
It does not establish that online learning is safe, useful or scientifically novel.
If caller-selected deployment compatibility is needed, its expected-config and
adoption policy must be specified separately rather than attributed to load().

## Independent source-only review before execution

The independent review found the ten semantic cases coherent and complementary.
It confirmed the valid nondefault constructor path and identified two clarifications
adopted before execution: C06's inner digest refresh is a consistency control, and
mandatory save-time direct reconstructions must be counted and phase-tagged.
No runtime import, fixture construction, checkpoint loading or pytest execution was
used in that review. Source-derived expected rejection stages are:

- C03: before either child loader
- C05/C09: after direct reference-brain restoration, before predictive pilot construction
- C06: before direct brain reconstruction
- C07: after predictive restoration, before scope pilot construction
- C08: after both components and compositor construction, before world/session construction
- C10: after temporary scope pilot and router construction

These construction-stage expectations will be checked without equating temporary
candidate construction with publication or mutation of a live incumbent session.

## Pre-execution runner and input freeze clarification

A subsequent independent source-only runner review required durable primary-load
outcomes before save-back, explicit infrastructure-error classification, and child
input verification against the parent’s exact mutation inventory. Its corrections
are implemented before any runtime import or fixture execution. An append-only
stage journal and the initial full ten-row plan preserve incomplete/interrupted
attempts; observed entry counts are lower bounds when a worker is interrupted.

`protocols/m1_checkpoint_compatibility_inputs_v1.json` separately freezes all six
retained checkpoint file hashes and complete nondefault predictive/scope configs.
It was generated through data-only archive/JSON inspection; no checkpoint loader or
model constructor was called. The runner pins its hash and the updated protocol
hash. Original source-only protocol bytes remain in commit `4087cd4`.

The numeric output threshold remains 32 MiB, with more precise enforcement wording:
it is an admission/checkpoint threshold, not an OS-enforced instantaneous quota.
Project sizes before harness writes/copies, check immediately before and after
model serialization, and drain stdout/stderr through bounded pipes. The parent’s
overall deadline applies to preparation and writes too. Any observed excess stops
further runtime work and marks incomplete/blocked cases without retry. Available
raw bytes are preserved, and possible output truncation or overshoot is explicit.
After a stop, each error/summary reconciliation file may retain at most 256 KiB of
JSON metadata; its storage/time is reported rather than hidden as quota compliance.
No semantic case, expectation, dynamics allocation or claim changed.

The final pre-execution journaling contract distinguishes invocation intent from
observed completed method calls. A worker interrupted after an intent has an
unknown invocation/completion boundary, not a fabricated zero actual count. A
journal failure cannot replace an already-running method’s own return or exception:
retain that outcome, mark measurement incomplete, and admit no next primary or
save-back operation. The already-admitted call remains under its original process
deadline and may still be terminated externally, in which case its outcome remains
unknown. Pipe overflow or a child-reported budget stop is latched in the controller,
even if discarded output kept the retained directory below 32 MiB.

Independent final runner review approved the single frozen matrix after source
commit, with no remaining blocker. Reviewed SHA-256 pins:

- runner: `16798c355caa0f47e5f3653f8c94a7ef3adde5546670518d82156b946c8971a1`
- synthetic tests: `09b86b9528ea2ee372135178d9f3bd9a832c5e1841414c19777136104f06ce22`
- protocol: `0889e1984865a93c4663f9ca5bd6e29d2ccdd97cf523ceb62f80ce768ac84c14`
- input manifest: `974850e46c8e8e472b03ff341e821087481f9efe47f3138646f7147501d77100`

Thirty-five outcome-independent synthetic tests and Ruff passed before execution.
The reviewer inspected source and hashes only and did not independently run tests,
construct fixtures, import the runtime or load checkpoints. These checks authorize
no expansion of the fixed ten-case/zero-transition execution allocation.

## Completed single-run result

Execution source pin: `b76b1af42800871b89cf966718c1a1aeb602e5d6`, tree
`20c576c438d2fef2d7b589d6b0175b8b72d14c62`. The runner, protocol and input pins
listed above were committed, remotely read back and independently source-reviewed
before the first fixture construction. No rerun or reproduction was performed.
The ten primary load calls consume the entire allocated matrix; no further
execution is authorized by this protocol.

| Case | Observed result | Rejection or restoration boundary |
|---|---|---|
| C01 | Accepted; exact six-file save-back | Retained default cut-7 checkpoint |
| C02 | Accepted; exact six-file save-back | Full valid nondefault configs preserved, including context_gate 0.25 and minimum_confidence 0.65 |
| C03 | ValueError | Outer identity, before either child loader |
| C04 | Accepted | Boolean true treated as version 1; save-back changes only manifest.json to integer 1 |
| C05 | ValueError | Predictive identity after reference-brain restoration, before predictive pilot construction |
| C06 | ValueError | Direct schema guard before brain reconstruction |
| C07 | ValueError | Scope identity after predictive restoration, before scope pilot construction |
| C08 | ValueError | Compositor identity after both components/compositor exist, before world/session construction |
| C09 | ValueError | Missing predictive config field after reference-brain restoration, before predictive pilot construction |
| C10 | ValueError | Router/config disagreement after temporary scope pilot/router construction |

Every rejected case returned no session. Every retained input file matched its
before/after byte hash, and the original #170 archive/transport remained unchanged.
These measured boundaries do not prove absence of transient heap/global side
effects. There is no existing-session replacement API in this test: temporary
candidate construction must not be called mutation or publication of a live
incumbent session.

C04 has the same returned state hash as C01. Its save-back is exactly the original
six-file retained fixture: the sole difference from its mutated input is the outer
schema tag `true` becoming `1`. This follows the current Python equality guard and
manifest serialization contract. No arbitrary-class payload, pickle, hostile-input
attack, production repair or security inference was tested or introduced.

### Counts, resources and retained failures

- Ten integrated loader calls completed: three returned sessions and seven raised
  the prospectively specified ValueErrors
- Thirteen `_load_bytes` validation invocations completed: twelve returned and C06
  rejected early. The raw field named `direct_reconstructions_completed_observed`
  counts completed validator invocations, including that rejection; it does not
  mean thirteen successful brain reconstructions
- One zero-cycle setup save and three accepted-candidate save-backs; zero dynamics
  transitions, observe/outcome/feedback operations, or retry/reproduction runs
- Eleven sequential subprocesses; no timeout, capture truncation, observation
  failure or incomplete row
- Recorded total duration 3.276620659 seconds; slowest worker 0.342794947 seconds
- 206 retained files, 1,177,728 bytes including final metadata, below the 32 MiB
  admission/checkpoint threshold. CPU/address-space limits were configured as
  frozen; peak RSS was not measured. These timings are provenance, not speed or
  energy comparisons

The original prospective text remains above for chronology. Its source-only status
is historical, not the current execution status. The pre-execution review defects
concerned harness reliability and were corrected before this one run; they did not
consume or justify another diagnostic matrix. The boolean alias acceptance is a
retained compatibility boundary, not a failed result that was repaired afterward.

### Independent data audit

An independent standard-library/source-only audit recalculated every mutant byte,
input hash, saved configuration and journal sequence. It confirmed all ten outcomes
and their rejection stages, the accepted inspection/state hashes, unchanged source
transport, 160 tracked runtime/source assets, 15 schema assets, and all eleven
worker provenance records. It did not import the model, load a checkpoint or rerun
the matrix. Scientific credit remains 0 and no independent scientific replicate is
claimed.

### Artifact access and no-model verification

`artifacts/m1_checkpoint_compatibility_20261001/` contains the exact run in ordered
base64 transport plus manifest, the controller log, the machine verification result
and regression validation logs. The lossless xz archive is 34,500 bytes, SHA-256:

`ae440c596046867aacc4ef5b72a3b1b1e3bd3bdeef10e6fced37e57030a192d8`

`protocols/m1_checkpoint_compatibility_artifact_anchors_v1.json` binds all 206 raw
file hashes, the exact archive, and execution provenance outside the transport.
Its digest is pinned in the verifier. Source manifests were independently checked
against Git objects at the execution pin before anchoring. This is repository
integrity binding, not an external authenticity signature.

Run the standard-library verifier without any model import or execution:

```bash
python scripts/verify_m1_checkpoint_compatibility_artifacts.py
```

It independently rebuilds mutants in memory, checks every initial/final file,
configuration, protocol/source/worker binding, completed call journal, rejection
stage and raw-to-summary count, and rejects rewritten self-descriptions or optimized
Python that would disable assertions. The tests include transport replacement,
missing provenance, inconsistent records and a runtime-import blocker.

The recorded execution command was:

```bash
python scripts/m1_checkpoint_compatibility_diagnostic.py \
  --source-commit b76b1af42800871b89cf966718c1a1aeb602e5d6 \
  --output /absolute/absent/output
```

That command documents the exhausted allocation, not permission for another run.
Future execution needs a fresh bounded allocation and the appropriate frozen source.
Current-main regression tests are separate from this diagnostic and do not replay it.

### Operational implication and limits

Completed-cycle recovery can distinguish an invalid stored candidate from a valid
saved nondefault configuration. The current loader validates nested components at
different construction stages and restores the saved settings; it does not compare
them with a caller-selected deployment configuration. A future recovery controller
should define any expected-config/adoption policy explicitly. Whether schema tags
should require strict integer types is likewise a separate compatibility-policy
choice; no production loader change is made here.

The result is limited to these ten trusted synthetic/local-file cases at one source
pin and interpreter environment. It does not establish arbitrary version migration,
all schema aliases, concurrency, crash consistency, hostile-input safety, continual
learning capability, model superiority, novelty, biological fidelity or energy
benefit. Existing historical results, #164 ownership, formal identities, claim
grades, scheduler authority and PROJECT_STATUS are unchanged.

### Final integration validation

After integrating current main `9073a563dea936c6f76610387503f9583c0d3966`
(the merged #169/#170/#174 history, not the unmerged #171 branch):

- 883 default tests passed; 392 scientific/reproduction/external tests deselected;
  one existing Starlette/httpx deprecation warning; 116.87 seconds
- 47 focused synthetic/data-only checks passed
- Repository-wide Ruff, local readiness, standard demo, 40-episode/30-step legacy
  benchmark, bundle validation and data-only compatibility verification passed
- Regression outputs used separate scratch destinations; the generated bundle
  validation manifest was retained separately and the tracked manifest preserved
- The existing main Results Ledger is an unchanged prefix followed by one new
  standalone entry; no historical result was overwritten

These are regression checks separate from the exhausted ten-load, zero-transition
compatibility matrix. Logs are retained under the artifact's `validation/` directory.
Final-head remote CI and Codex review are still required before merge.
