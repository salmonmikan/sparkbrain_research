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

## D-V03-0005 — Freeze the C12-to-C13 lineage boundary and E0/E1 diagnosis

**Decision:** Preregister protocol `c13-evidence-entity-v1` and run
`c13-evidence-entity-main-v1` before implementing or evaluating C13. Preserve the C12 public
field names from `SensorySample` through `PerceptualSpark`: diagnostic `entity_hint` becomes
perceptual `entity_slot`. Convert that output explicitly at the C13 boundary into a versioned
evidence contract using `entity_key`, `hypothesis_id`, `polarity`, `strength`,
`parent_evidence_ids`, and `parent_spark_ids`. The conversion and every entity transition must
remain traceable. Do not replace these stage-specific names with one unified entity object.

C13 first compares `E0_global` with `E1_oracle_entity` using the same frozen input frontend,
G0 downstream path, episode inputs, seeds 2601--2605, cognitive core, budget, and evaluator.
Correlation discount is fixed at 0.20 and recency tau at 30.0. Same-ID redelivery must be an
exact no-op; identity-changing redelivery must fail closed. Removal and restoration use an
append-only immutable audit trail rather than deleting lineage. The E0/E1 scientific gap is
frozen before any `E2_learned_slots` implementation or run. Learned slots are only an interface
in C13 and must expose assigned, unassigned, and uncertain states with permutation-invariant
evaluation.

The C12 contract is pending an accepted merge. After that merge and before any C13 source
implementation, add a separate preregistration-amendment commit that pins the accepted C12 merge
hash without changing the frozen thresholds, seeds, conditions, or claim policy.

**Preregistration amendment (before source implementation):** C12 was accepted and merged as
`280516fb61eab7c7a96c109baefc82b333fcc367` from head
`50c2e67be73292b3a51737455597cd7aac4d8659`. The exact shared canonical inventory additionally
includes `schema_version` on both records and `omitted_channels` on `SensorySample`. This
dependency hash-pin and field-inventory correction changes no threshold, seed, condition, or
claim policy.

**Reason:** C12 and C13 share a serialization boundary, but entity meaning changes by stage.
Freezing the names, adapter, invariants, thresholds, seeds, and stop rules before results prevents
silent lineage reassignment, duplicate evidence inflation, post-hoc entity tuning, and an Oracle
entity result being mistaken for autonomous binding.

## D-V03-0006 — Clarify C13 state, control, metric, and lineage semantics before evaluation

**Decision:** Before any C13 test, runner, experiment, artifact generation, metric observation, or
threshold result, separate the restorable `active_state_hash` from the append-only
`audit_chain_hash`; freeze G0 as a non-Coalition probability control using
`sigmoid(effective_support - effective_contradiction)`, probability threshold 0.5, confidence
minimum 0.5, margin minimum 0.08, and budget one; and freeze a relation-free 24-episode-per-seed
MultiObjectWorld over two objects, two hypotheses, and the six event classes in the protocol.
Define prediction change as fixed-time absolute probability delta. Define cross-talk over directed
relation-free non-target intervention opportunities, misassignment over E1 evidence rows eligible
for assignment, and coverage over E1 eligible Sparks. The scientific E0-minus-E1 cross-talk gap
uses the point estimate with a descriptive paired interval and remains separate from engineering
acceptance.

Parent deactivation does not rewrite descendants. A row is effectively active only when its own
flag and every transitive parent flag are active; summary and decision exclude other rows, while
inactive lineage remains resolvable. Restore re-enables eligible descendants without mutation.
Unknown parents, self-parenting, and cycles fail closed. Strict `EntityBinding` and
`EvidenceAuditRow` field inventories, nullable-but-immutable correlation semantics, complete
Spark-to-sample lineage, condition-separated aggregation, and required artifact contents are
frozen in `artifacts/v03/c13_evidence_entity/protocol.json`.

**Reason:** The first implementation review found ambiguity in how an exact restored state could
coexist with a growing audit, what C13's pre-C14 G0 meant, how rates were denominated, and what
causal parent removal did to descendants. At that point only two uncommitted source drafts existed;
no test, runner, experiment, artifact, metric, or threshold result had been run or observed. This
clarification therefore prevents result-driven semantics rather than reacting to results, and it
changes no preregistered threshold, seed, E0/E1 condition, or claim policy.

## D-V03-0007 — Freeze the final C13 fixture, decision, identity, rejection, and slot rules

**Decision:** Still before any C13 test, runner, experiment, artifact, or numerical result, freeze
the 24 episodes per seed to the exact deterministic generator and per-seed SHA-256 values in the
protocol. Every episode has one target selected by the frozen seed/index parity rules and exactly
six ordered events: primary support, correlated support, exact late redelivery, contradiction,
primary deactivation, and exact restore, with frozen times, strengths, sources, and correlation
groups.

G0 sorts hypotheses lexicographically, keeps candidates meeting probability 0.5, confidence 0.5,
and margin 0.08, chooses the highest probability with lexical tie-break under budget one, and
otherwise abstains. Evidence identity is the exact canonical record, including schema, metadata,
nullable correlation, lineage, entity, and hypothesis. Evidence and binding IDs use the frozen
canonical SHA-256 derivations. Invalid payload rejection hashes a canonical type/reason envelope,
never raw invalid values or runtime `repr`. Slot scoring uses maximum-weight contingency matching,
zero-weight rectangular padding, lexical tie-break, assigned-only accuracy, separately reported
unassigned/uncertain/coverage, and an exact consecutive-assigned-pair switch denominator.

**Reason:** A read-only design audit found five remaining choices that could otherwise be selected
after seeing behavior: fixture distribution, multi-hypothesis selection, ID scope, hashing of
non-JSON rejection, and permutation matching. Freezing them now closes those degrees of freedom.
No test or result had yet been executed or observed, and no earlier threshold, seed, condition, or
claim policy is changed.
