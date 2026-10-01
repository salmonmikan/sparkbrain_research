# M1 checkpoint compatibility and rejection-stage diagnostic

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
