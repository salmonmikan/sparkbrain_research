# Decision Log

## D-001 — Treat SparkBrain as brain-inspired, not a brain replica

**Decision:** Until anatomical and neurophysiological validation exists, describe the project as a brain-inspired dynamic cognitive system / artificial brain experiment environment, not a reproduction of the human brain.

**Reason:** Functional similarity does not establish biological equivalence.

## D-002 — Project code name is SparkBrain; theory name remains provisional

**Decision:** Use `SparkBrain` for repository/package identity. Do not publish `SFA` as the final acronym.

**Reason:** Naming conflicts and novelty boundaries have not been fully searched.

## D-003 — Reference engine precedes spiking implementation

**Decision:** Build and freeze rate-based behavior before local Norse/snnTorch/Nengo simulation. Dedicated-hardware mapping is Extension H.

**Reason:** Otherwise theory failure, training failure, and substrate failure cannot be separated.

## D-004 — Use a priority event queue, not one coroutine per Spark

**Decision:** Model logical concurrency using deterministic discrete events.

**Reason:** Thousands of Python tasks would obscure the algorithm and add scheduler overhead without providing physical parallelism.

## D-005 — Coalition is an evidence-bearing object

**Decision:** Coalition membership includes evidence identities/provenance, not only active processors.

**Reason:** Revision and interpretability require distinguishing independent support, duplicated propagation, and contradiction.

## D-006 — No-ignition is valid

**Decision:** The system may have no newly valid belief even when an output is requested.

**Reason:** Forced selection conflates uncertainty with belief.

## D-007 — Losers decay; they are not cleared by default

**Decision:** Standard architecture uses winner-take-most. Hard-WTA is an ablation.

**Reason:** Hypothesis recovery is a central falsifiable mechanism.

## D-008 — Current Phase-0 weights are hand-authored

**Decision:** Preserve them as a software validation fixture only.

**Reason:** They cannot support generalization or learning claims.

## D-009 — Algorithmic sparsity and energy efficiency are separate claims

**Decision:** Report active nodes/edges and local runtime separately. Reserve physical energy claims for direct Extension H hardware measurement.

**Reason:** Sparse dynamic Python or GPU execution can be slower despite less semantic work.

## D-010 — Codex tasks require acceptance tests and raw artifacts

**Decision:** No task is complete because code exists. It must meet explicit tests, outputs, and documentation criteria.

**Reason:** The project combines research and software; unverifiable output is not useful.


## D-011 — Core completion is local-only

**Decision:** The reference engine, simulator, visualizer, experiments, storage, and reproduction path must complete on one general-purpose local computer. CPU is mandatory; local GPU is optional. Remote APIs and cloud services are not core dependencies.

**Reason:** The project requires inspectable causal state, reproducibility, privacy, and independence from proprietary runtime services.

## D-012 — Dedicated hardware is a separate extension

**Decision:** Loihi, FPGA, ASIC, Lava/vendor mapping, and physical power measurement are assigned to Extension H and removed from core completion gates.

**Reason:** Algorithmic validity and local spiking equivalence can be established without specialized access; hardware availability must not determine whether the core theory is complete.

## D-013 — Package patch version and persisted schema version are distinct

**Decision:** Release v0.2.1 uses package/theory version `0.2.1` while retaining config/state/trace schema `0.2`.

**Reason:** The patch adds scope, explanations, and local validation without changing persisted dynamics contracts.

## D-014 — Maintain formal and beginner documentation together

**Decision:** Core terminology changes must update the formal theory, beginner foundation guide, and glossary in the same change.

**Reason:** A technically precise theory that cannot be followed by implementers or reviewers is not sufficient for this project, but analogies must not silently replace formal semantics.

## D-015 — Separate repository, archive, and private-review verification

**Decision:** Repository mode keeps Git tracked-file and ancestry checks. A no-`.git` release
archive must instead validate fixed release metadata, exact revision agreement, and manifest
contents without invoking Git. A private review bundle is a distinct packaging layer with its own
exact-content `REVIEW_BUNDLE_MANIFEST.json` and external ZIP SHA-256; it must not introduce
implicit exceptions into public release validation.

**Reason:** A public or review ZIP does not contain repository history. Treating Git failure as a
validation failure made standalone reproduction impossible, while treating it as success would
weaken provenance. Explicit modes preserve fail-closed evidence checks and keep private review
packaging separate from the owner-controlled public license gate.

## D-016 — Validate pristine integrity before archive runtime

**Decision:** Release validation classifies integrity, preparation, owner, and evidence problems.
Preparation-only success permits only the owner license blocker. Reproduction runs the shared
non-public integrity preflight before reading a revision, rendering, or creating staging/output.
For a no-`.git` package, pristine integrity validation precedes the runtime pytest phase; another
pristine audit requires a fresh extraction. Pytest cache output is disabled or placed outside the
archive root, and repository-only integration tests do not recursively invoke Git from archive
mode.

**Reason:** Package hashes must fail closed before a `status: pass` artifact can exist, while
ordinary documented Python commands must not be mistaken for content originally shipped in the
archive. The two phases preserve strict package integrity without requiring hidden user-supplied
environment variables or weakening the ban on cache files in a pristine release.

## D-V03-0001 — Preregister the C11 input-bottleneck diagnosis

**Decision:** Freeze protocol `c11-input-bottleneck-v1` before adding v0.3 source. Compare
`I0_whole_hash`, `I1_local_compositional`, and diagnostic-only `I2_symbolic_oracle` on the same
six pairs, deterministic seed, feature budget, frozen cosine evaluator, labels, and threshold.
The Oracle rejects ordinary text, unknown fields, and evaluator/target metadata, remains disabled
by default, and is excluded from autonomous-input claims. The official Belief-R test is not read.

**Reason:** C11 must localize information loss without tuning the production model or allowing
an Oracle result to be mistaken for language understanding. Any post-result protocol change
requires a new decision ID and a new protocol run.

## D-V03-0002 — Supersede C11 v1 with a five-seed statistical audit

**Decision:** Before accepting C11, supersede protocol `c11-input-bottleneck-v1` with
`c11-input-bottleneck-v2`. Keep the six pairs, input tracks, threshold, diagnosis rule, and
Oracle policy unchanged, but execute preregistered seeds 1729–1733. Report paired effect sizes
and 95% nonparametric bootstrap intervals over diagnostic-pair blocks using bootstrap seed 4311.
The deterministic frontends and evaluator are expected to be seed-invariant; that invariance is
reported explicitly rather than treating duplicate seeded executions as independent evidence.

**Reason:** Independent C11 review found that v1 met the task-specific criteria but did not meet
the v0.3 global rule requiring at least five seeds and an interval for a primary synthetic
comparison. This is a new protocol and run recorded before execution; it does not tune any
feature, threshold, pair, label, diagnosis gate, or checkpoint after seeing v1 results.

## D-V03-0003 — Preregister the C12 computational sensory gate

**Decision:** Freeze protocol `c12-sensory-field-v1` and run
`c12-sensory-field-main-v1` before C12 implementation or evaluation. Use primary seeds
2601--2605, the exact salience coefficients and adaptive threshold in
`docs/EXPERIMENT_PROTOCOL.md`, a channel-local goal request capped at 0.35 with requested/applied
trace, the unchanged G04 acceptance thresholds, and a paired 10,000-resample bootstrap over
episode/world blocks with bootstrap seed 4312. Keep channels inspected, features scored, state
updates, candidate channels, emitted Sparks, suppressed channels, and downstream active work as
separate counters. Explicit omission is an adapter observation of an expected missing channel.
Reject evaluator truth / target / label / test-only / contradiction / answer fields recursively
and reject any invalid multi-channel sample atomically before state mutation. Retain failed and
adversarial rows, and require state-neutral inspection plus exact serialized replay. Any
post-result score, threshold, seed, world, or counter-definition change requires a new Decision
ID and protocol.

**Reason:** C12 must test suppression, change recovery, and bounded goal modulation without
tuning after evaluation or relabeling dense sensory computation as sparse active work. The
bounded local hint may alter threshold crossing but cannot manufacture semantic evidence. This
is a computational sensory-gate test only and does not change accepted v0.2.1 results, protected
hashes, release/package/schema 0.2 contract, or scientific claim grades.

## D-V03-0004 — Accept C12 at the computational sensory-gate boundary

**Decision:** Accept C12 G04 for protocol `c12-sensory-field-v1` and run
`c12-sensory-field-main-v1`. Preserve the exact six artifacts under
`artifacts/v03/c12_sensory_field/`, including all five seeds, paired bootstrap intervals,
accepted/suppressed channel trace, ablations, explicit omission examples, and bounded-goal
adversarial rows. Stop C12 here. Do not infer reduced dense total work, energy efficiency,
biological sensory reproduction, semantic understanding, or a higher claim grade from the
passed gate.

**Reason:** All preregistered G04 thresholds passed and replay / atomicity / inspection contracts
are directly tested, while `channels_inspected`, `features_scored`, and `state_updates` remain
dense. The narrow acceptance is therefore reproducible without overstating what emission
suppression demonstrates. Accepted v0.2.1 protected results and release/schema contracts remain
unchanged.
