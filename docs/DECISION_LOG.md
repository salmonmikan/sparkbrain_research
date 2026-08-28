# Decision Log

## D-V03-0035 — Retain C19 as completed readiness, not accepted evaluation

**Decision (2026-08-28):** Retain the deterministic C19 blocked-readiness exact-nine bundle from
source `052413136229dcfa63f08cebe19585134f7cfb98`. The bundle records the exact ordered 85-row
official execution plan, dependency pins, strict validators, and atomic writer. It records no
official predictions or attribution and does not open or verify official Belief-R examples.

**Disposition:** Engineering readiness is complete, but C19 and G09 are not accepted. Scientific
status is `not_evaluated`, not a positive or negative C19 result. The preflight blocker is
`missing_truth_free_belief_r_symbolic_adapter`; evaluator truth must not be used to manufacture the
I2 symbolic representation. All four baseline matching axes remain false and winner claims remain
prohibited.

**Scope:** C06 remains the existing negative external result and is neither replaced nor upgraded.
Any official evaluation after the missing adapter is designed requires a new preregistration and
protocol; this blocked bundle is not amended in place. Initial C19 preregistration bytes, package
0.2.1, persisted schema 0.2, schemas, release files, C06/C08 evidence, and claim grades remain
unchanged.

## D-V03-0030 — Retain C18 v6 as engineering-only observability evidence

**Decision (2026-08-28):** Integrate the independently audited C18 v6
exact-seven official bundle from execution pin
`c0c242d848588d76015734a309f72fed0bd1d380` with fixed seed `1802`.

**Reason:** The retained preflight evidence, strict schema validation,
deterministic replay, parent-bound fork lineage, and static offline export
support the engineering observability/replay contract. They do not evaluate
scientific efficacy.

**Scope:** Engineering is `accepted`; science is `not_supported`. No claim
grade, v0.2 contract, C17 v1 artifact, C06/C08 finding, package version,
persisted schema, or release metadata changes.

## D-V03-0029 — Keep C18 trace/checkpoint integration isolated from v0.2

**Decision (2026-08-28):** Add C18 under `sparkbrain.v03_integration` with
schema `0.3`, explicit branch/checkpoint lineage, and state-hash replay. Do not
modify v0.2 schemas, readers, `/api` routes, existing Brain Lab, package
version, release manifests, C06/C08 findings, or C17 v1 artifacts.

**Reason:** C17 v2 is independently in progress. C18 can inspect only the
stable public C17-v1 contract without private restoration or reinterpretation.
Fail-closed evidence citations prevent the UI from presenting inferred
attribution as stored state.

## D-V03-0027 — Accept C15 v4 at the registered engineering boundary

**Decision (2026-08-27):** Accept C15 v4's engineering result from the exact-eight bundle under
source `1072a484f36fc8981622ed3de39d796b654698b9` and execution-pin head
`49b40cee605d48e5f9dca243e2c23de43491c64e`. All eight frozen engineering gates pass with no
failed seed; each of seeds 2951--2955 completes all 8/8 primary recovery opportunities without
checkpoint restoration. The completed independent audit includes all nine 10,000-draw paired
bootstrap recalculations and byte-identical `PYTHONHASHSEED=1`/`37` reproductions.

Scientific status remains `not_supported`: full and no-residual recovery are both 1.0, and the
weighted-CE ECE comparison is undefined under the registered null contract. These outcomes do not
block the separate engineering acceptance and are not reclassified as scientific support. C17's
C15 engineering-acceptance dependency is therefore unblocked, while C15 v3's completed negative
artifacts and transport remain immutable.

**Scope:** No threshold, seed, loss, fixture, source, release manifest, package/schema, C06/C08
finding, or claim grade changed. This decision does not assert semantic understanding, organ or
biological fidelity, energy efficiency, or external generalization.

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

Before the first fixture test, the protocol additionally records the exact canonical document,
episode, add-event, redelivery-event, and intervention-event key sets and JSON serialization call
used by the already-frozen per-seed hashes. This is a reconstructibility clarification only: no
fixture value, ordering rule, distribution, seed, threshold, metric, or expected hash changes.

## D-V03-0008 — Accept C13 at the oracle entity-scope diagnostic boundary

**Decision:** Accept C13 G02/G05 for protocol `c13-evidence-entity-v1`, run
`c13-evidence-entity-main-v1`, and source commit
`03b26591c653592ec501177d9628bd2bea9b8ec4`. Freeze the exact eight artifacts under
`artifacts/v03/c13_evidence_entity/`. Preserve strict immutable evidence identity, transitive
effective-active lineage, append-only deactivate/restore, semantic audit replay, fixed G0,
condition-separated E0/E1 rows, deterministic fixture hashes, and E2 execution row count zero.
Do not start E2 learned binding under this decision.

**Reason:** All frozen G02/G05 engineering gates passed over seeds 2601--2605 with no failed
seed. E1 cross-talk and misassignment were 0 and oracle coverage was 1.0; E0-minus-E1 cross-talk
was 1.0 with paired interval [1.0, 1.0]. The gap is narrow evidence that explicit Oracle entity
scope removes cross-talk in this constructed relation-free fixture. It is not autonomous entity
discovery, semantic understanding, biological fidelity, or external generalization. The audit
chain is not an external trust anchor. Independent regeneration under a different
`PYTHONHASHSEED` matched all eight artifacts byte-for-byte. Existing negative results, scientific
claim grades, protected hashes, package/schema, and release metadata remain unchanged.

**Raw-evidence correction:** Final acceptance additionally requires all 1,440 ordered execution
rows and the numeric/canonical G02 before/after observations to remain in the exact eight
artifacts. This correction changes no protocol, threshold, fixture, seed, metric definition, or
result; it makes the existing acceptance independently recalculable instead of boolean-only.
## D-V03-0009 — Preregister C14 Coalition-driven Ignition

**Decision:** Before C14 source implementation or evaluation, freeze protocol
`c14-coalition-gate-v1` and run `c14-coalition-gate-main-v1`. Compare the unchanged G0
probability/margin control, the G1 evidence-Coalition gate, and a no-Coalition ablation while
holding logits at `hypothesis-alpha=0.72` and `hypothesis-beta=0.28`. Use seeds 2701--2705 and a
paired 10,000-resample interval over seed-by-intervention-case blocks with bootstrap seed 4314.

Bound activation, effective support, source/group diversity, temporal stability, recency,
contradiction, and redundancy to `[0,1]` using the exact transforms and weights in
`artifacts/v03/c14_coalition_gate/protocol.json`. Freeze threshold 0.55, margin 0.10, minimum two
sources/groups/evidence, stability two, recency minimum 0.30, contradiction ceiling 0.35, budget
one, and the machine-readable reason priority. Run the ten frozen independent-support,
same-ID, same-source, correlated-copy, contradiction, instability, time-decay, low-score,
low-margin, and remove/restore interventions. Each case uses a fresh gate/ledger; stability uses
two identical evaluations, and remove/restore compares fresh-gate replays so intervention history
cannot alter the stability term. Retain every raw row and failed seed.

**Reason:** C14 must show that attributable evidence changes the actual v0.3 Ignition decision
while logits stay fixed. A probability copy, a post-result threshold reduction, or an ablation
that changes no decision would not establish Coalition causality. External accuracy improvement
is not required for engineering completion, and the accepted C06/C08 findings, claim grades,
package/schema, release metadata, and protected artifacts remain unchanged.

## D-V03-0010 — Freeze final C14 call-path, fixture, ablation, and artifact semantics

**Decision:** Before C14 source editing or any result, close the design ambiguities found by three
independent read-only audits. Freeze actual logits `ln(0.72)` and `ln(0.28)`, their probabilities,
canonical SHA-256, activation override, post-stability-update scoring, and the diagnostic actual
path `V03ReferenceLoop.settle -> CoalitionGate.evaluate -> IgnitionDecision -> belief update`.
Keep the legacy gate as default and enable `c14_bounded_v1` only explicitly. Do not change the
v0.2 learned backend.

Define no-Coalition as the exact G0 probability/margin decision with evidence constraints removed
and identical belief side effect. Freeze the canonical 10-case generator and five fixture hashes,
the exact evidence roles/strengths/times, each case's primary evaluation and expected reason, the
four paired comparators, both G1 decision-difference gates at 0.30, point-estimate gate policy,
360-row raw schema, 15 causal-removal rows, protected/source preflight, and source-pin procedure in
the protocol. `unstable_first_observation` alone uses evaluation one as primary; remove/restore
uses the removed stage. C13 decay in effective support and the separate C14 freshness term are
intentional and must both remain visible.

**Reason:** Without these definitions, an implementation could choose its fixture, stability
timing, ablation behavior, expected negatives, or aggregation after seeing results. The final
freeze makes the intervention result reconstructible and preserves an honest negative result if
the preregistered G03 gates fail. Source implementation may begin, but runner execution remains
forbidden until a separate amendment pins the source-only commit.

## D-V03-0011 — Close C14 fixture, stability, bootstrap, and artifact reconstruction gaps

**Decision:** Still before C14 source editing, tests, runner execution, artifact generation, or
numerical result observation, replace the identity-only fixture hash as the execution authority
with five full-fixture hashes. The canonical payload now includes the document prefix, ID
templates, every case's entity, time, activation mapping, primary stage/evaluation, expected G1
decision, complete evidence roles with hypothesis/polarity/strength/source/group/time/lineage and
metadata, and exact active/remove/restore stages. The earlier five identity hashes remain labeled
as audit continuity only.

Update an independent stability signature counter for every candidate before computing any score;
all unchanged candidates, including both candidates in the equal-score case, advance from one to
two on the second evaluation. Each case, condition, and causal replay starts with a fresh complete
reference loop, including a fresh belief field. Freeze the paired bootstrap vector membership,
with-replacement sample size, shared RNG stream, arithmetic estimand, linear percentile
interpolation, and non-rounded finite JSON serialization. Freeze exact nested candidate/decision,
causal-removal, no-Ignition-reason, metrics, manifest, sort, and unknown-key contracts so all
scores, margins, reasons, effects, and gates can be recalculated from the six artifacts.

**Reason:** Independent pre-implementation audits found that the prior identity hash did not bind
evidence content, equal-case behavior depended on an unstated stability update scope, bootstrap
percentiles were not byte-reproducible, and nested artifacts could omit recalculation inputs. This
amendment closes only those pre-result degrees of freedom. It changes no logits, score transform,
weight, threshold, seed, intervention expectation, claim policy, or source-pin sequence.

## D-V03-0012 — Freeze C14 nested artifacts and repair the weak-case activation conflict

**Decision:** Before source editing or result observation, require exact nested types, null/default
rules, cardinalities, and ordering for raw candidate terms, decisions, belief snapshots, evidence
IDs, causal replays, no-Ignition references, aggregate/seed metrics, paired statistics,
engineering gates, failed seeds, and the manifest. G0 and no-Coalition rows carry an empty
`candidate_terms` list because they do not consume the C14 score; G1 rows retain every candidate
term. All conditions still retain a decision and canonical before/after belief snapshot.

Repair `weak_low_score` without changing the frozen probability-to-activation mapping: keep alpha
and beta activation at 0.72 and 0.28, move the two strength-0.05 evidence records to time 65.0,
and evaluate at time 100.0. Freshness `exp(-35/30)` remains above the 0.30 hard minimum while the
bounded top score remains below 0.55. Recompute only the five full-fixture hashes; retain the
identity-only hashes unchanged for audit continuity.

**Reason:** A final read-only audit found that the previous weak case reached Ignition only by
overriding activation to zero, contradicting the fixed-logit mapping, and that nested artifact
containers were not independently validatable. This pre-source repair restores the intended
score-specific negative and makes exact artifacts implementable. No threshold, weight, seed,
expected reason, claim policy, or official result changed.

## D-V03-0013 — Freeze C14 metric placement and retain comparator observations

**Decision:** Before source editing or result observation, define every one of the 24 aggregate
and 120 seed metric rows by an exact condition-aware formula. Condition-local coverage,
accuracy, false Ignition, and mean consumed score use their own primary rows. The two G1 score
deltas are calculated only from retained G1 comparator observations and are exactly zero for both
probability controls. Each cross-condition decision-difference scalar is repeated unchanged in
all three condition rows. Numerators and denominators are retained.

Add an exact `comparators` object to every raw row without increasing the frozen 360-row count.
Only the specified G1 primary rows retain fresh-loop second-evaluation observations for the
primary-support-only or independent-support baseline; all other comparator slots are null. These
nested observations use the same decision, candidate-term, and belief schemas, making same-ID,
independence, correlated-group, and contradiction gates artifact-recalculable. Add the missing
G1-versus-G0 0.30 gate to the canonical engineering-gate set. Treat external accuracy as claim
scope, not as a boolean engineering-gate result row.

**Reason:** Independent implementation and reproduction audits found that exact row shapes still
allowed multiple metric placements and omitted the comparator observations required to audit
same-ID behavior. This amendment removes those final serialization choices without changing any
fixture, hash, score, threshold, seed, expected outcome, or claim boundary.

## D-V03-0014 — Pin the audited C14 source and authorize the frozen runner

**Decision:** After source implementation and focused tests, and before any official runner
execution or result observation, pin C14 source commit
`307bcb56f09e88b769cd863b1a6fead73a189936` and authorize the runner. Anchor protocol
authenticity to preregistration commit `79dfa6c612e1d3159aae8705be5e14833502ea96`
and its exact protocol blob SHA-256
`ce3fc31531f5ea7689cfcd3b07354508a67af9463ed3b9e1eebb613e0e9c4c8a`.
The runner must reject a noncanonical path, working bytes different from HEAD, a changed base
blob, any amendment beyond this source pin / execution flag / base identity, or any later change
to the four frozen source paths before creating an output directory.

The pinned source was independently audited after corrective implementation. Focused coverage
includes the actual bounded decision helper, a score-only `0.54` to `0.56` causal mutation,
protocol tampering, exact nested artifact validation, per-seed failure attribution, legacy
default behavior, fixture hashes, and the disabled-runner guard. The official C14 runner and
numerical evaluation had not been executed when this decision was recorded.

**Reason:** This separate amendment completes the preregistered source-pin sequence only after
implementation review closed the protocol-authenticity, call-graph, artifact-schema, and
failed-seed blockers. It changes no fixture, score, weight, threshold, seed, expected outcome,
metric definition, protected artifact, or claim boundary.

## D-V03-0015 — Record the stopped C14 attempt and repin the metric wiring fix

**Decision:** The first authorized C14 runner attempt under source pin `307bcb56...` stopped
before artifact publication when `_metric_rows` passed a complete raw row to a helper that
requires its nested decision object, raising `KeyError: 'ignited'`. The atomic staging directory
was removed; the requested output path did not exist afterward; no metric, gate result, report,
or numerical artifact was printed or committed. Preserve this failed attempt in the decision
history rather than treating it as an official result.

Repair only the raw-row-to-decision wiring. The initial narrow fix `d040539...` corrected metric
rows but independent audit found the same error in paired statistics and engineering gates before
any second official attempt. Final source commit
`eb7f542963397eba1b7d9b4a66a7873b3ba17ac4` corrects every affected call site. A write-free
in-memory regression executes raw evaluation, metrics, paired statistics, aggregate and per-seed
gates, and failed-seed attribution with exact counts `360 / 15 / 24 / 120 / 4 / 12`. Focused
tests pass and an independent re-audit confirms all seven decision-difference call sites receive
decision objects. Repin C14 to `eb7f542...` before the next and only remaining official attempt.

**Reason:** This is a mechanical acceptance-calculation correction after a fail-closed attempt,
not a result-driven protocol change. It changes no fixture, score, weight, threshold, seed,
expected outcome, metric formula, engineering gate, protected artifact, or claim boundary.

## D-V03-0016 — Accept C14 at the attributable Coalition-gate boundary

**Decision:** Accept C14 G03 for protocol `c14-coalition-gate-v1`, run
`c14-coalition-gate-main-v1`, final source pin
`eb7f542963397eba1b7d9b4a66a7873b3ba17ac4`, and artifact commit
`4c0d26cd0be862da63594f1f32e295127de72304`. Freeze the exact six artifacts under
`artifacts/v03/c14_coalition_gate/`.

All 360 raw fixed-logit rows, 15 causal removal rows, 24 aggregate metrics, 120 seed-level rows,
four paired statistics, 50 reason references, and 12 engineering gates are retained. All gates
passed with no failed seed. Independent support Ignition rate and removal reversal/restore-exact
rates are 1.0; same-ID score/decision delta is 0.0; correlated-copy independent-group delta is
0; contradiction score delta is -0.1296997075145081; and both G1-versus-control decision
difference rates are 0.9. All nine required reasons are represented. Fixed-logit integrity is
1.0 across every raw row.

The six artifacts reproduced byte-for-byte in a second process with a different
`PYTHONHASHSEED`. Raw-only recalculation reproduced all aggregate, seed, paired, gate, reason, and
failed-seed outputs. The complete test suite passed with five explicit frozen-release skips and
the existing Starlette deprecation warning only.

**Reason:** C14 now demonstrates the narrow engineering claim that an attributable, bounded,
evidence-bearing Coalition score causally controls the actual isolated v0.3 Ignition decision
while logits remain fixed. It does not establish external accuracy improvement, learned
coalition formation, semantic understanding, biological fidelity, energy efficiency, or a higher
scientific claim grade. The accepted C06/C08 negative findings, v0.2 package/schema, release
metadata, and protected artifacts remain unchanged.

## D-V03-0024 — Preregister bounded C16 proto-concept formation

**Decision (2026-08-26):** Freeze protocol `c16-proto-concepts-v1`, run
`c16-proto-concepts-main-v1`, in `artifacts/v03/c16_proto_concepts/protocol.json` before C16
source implementation or official sensory/model/controller evaluation. This independent stage
starts from accepted C14 merge `00dccf3dc8f6f70353a536dcf1db9ba0b19fc7b5` and consumes accepted
C12 sensory processing, C13 sample/Spark parent registration, and the unchanged CC0 concept seed.
It does not consume C15 runtime. Decision IDs D-V03-0017 through D-V03-0023 and experimental
section 14 belong to the separate C15 branch; C16 uses section 15 without rewriting that history.

Run seeds 3601--3605 determine both fixture phase/amplitude and initialization; bootstrap seed
4366 determines 10,000 paired hierarchical resamples. Four worlds expose recurrence across held-out
contexts, transitive bridge overmerge, frequency/distractor shortcuts, and decoy reversal.
Each seed has 32 train, 16 dev, and 16 test episodes of nine frames. Two independent pure
generators agreed on all 30 manifest/full-fixture hashes without running sensory, concept,
learned, or controller code. Those hashes and exact formulas are frozen in the protocol.

Compare immutable CC0, online prototypes, and a tied linear 12-to-4-to-12 autoencoder against
their matched-random and frequency-top-K controls. The encoder has exactly 48 weights and twenty
train-only full-batch SGD steps; no nonlinearities, biases, dev selection, or test adaptation.
Banks are bounded by eight live candidates, 32 lifetime births, 32 retained exemplars per
candidate, and 288 unique train observation identities. Same-ID redelivery is an exact state
no-op, including the CC0 wrapper. Merge/split, competition, dormancy, deletion, lineage and
unsupported-control no-ops are explicit. Bank input is only a numeric emitted vector and opaque
observation ID; independent episode/context recurrence remains evaluator-only.

Freeze next-channel MSE as the sole utility, the same eight-slot plus intercept ridge budget,
candidate-active held-out comparisons, and train-selected usage-matched interventions. A
candidate below three independent episodes/two contexts has null grade, not automatic CC0.
Control shortfalls prevent CC2/CC3. CC3 needs bounded collateral and the same functional-world
effect in at least three run seeds, not a cross-seed candidate-identity claim. Null grades,
clusters without utility, and negative scientific outcomes remain valid deliverables.

Freeze exactly eight new source/test paths, 29 inherited baseline/CC0 protected hashes, and four
direct runtime source pins. C16 source may be implemented only after this preregistration;
official execution remains disabled until an audited source-only commit and a separate amendment
of exactly the four root pin fields. Run the complete reserved-synthetic/pure-fixture suite both
before the source commit and after the pin amendment, before the first official evaluation.
Protocol tests must handle amended/unamended and no-Git contexts without treating the mutable
current protocol as its own unchanged base.

Freeze the exact eight-file artifact bundle and successful-seed-scaled cardinalities. Seed
failure discards that seed's whole buffer, remains visible, and disables scientific promotion;
missing results are never imputed. A parent-enforced 3,600-second worker deadline includes all
computation, validation, and staging writes after preflight. Only the parent publishes. Timeout
termination precedes cleanup; a surviving child leaves quarantined staging and never a published
result. Reproduction uses the recorded stage execution/artifact checkout: post-pin changes are
limited to the exact C16 artifacts and four named documents, not arbitrary later-stage source.

**Reason:** Candidate recurrence, stability, held-out reuse and causal contribution must be tested
separately from attractive clusters or names. Freezing resource bounds, raw denominators,
controls, leakage boundaries, failure semantics and source snapshots before implementation
prevents retrospective promotion. This decision registers an experiment, not a C16 result or
an increase in any existing scientific claim grade.

## D-V03-0028 — Accept the bounded C16 synthetic result at its registered boundary

**Decision (2026-08-27):** Accept C16 protocol `c16-proto-concepts-v1`, run
`c16-proto-concepts-main-v1`, source commit
`4933a6059240875d0548fe602f114d768a49ef28`, and the exact-eight artifact bundle under
`artifacts/v03/c16_proto_concepts/`. The recorded execution lineage is source-only commit
`4933a60`, pin `b1c83e6`, and integration branch `codex/c16-proto-concepts` pre-artifact head
`3dd9593`.

All eight engineering gates passed with zero failed seeds. The retained raw cardinalities are 990
lineage rows, 90 bank rows, 5 learned checkpoints, 5,760 held-out episode rows, 60 control banks,
1,920 causal rows, and 60 counterexample rows; utility and paired-control aggregates retain 72 and
48 rows respectively. CC0 is supported for 109 candidates and CC1 for 6; CC2 and CC3 are not
supported with zero qualified candidates. A full independent audit passed, and
`PYTHONHASHSEED=1` versus `PYTHONHASHSEED=37` reproduced all eight artifact bytes exactly.

**Reason:** The result supports only the preregistered synthetic recurrence/stability boundary and
next-channel-MSE result. It does not establish human semantic understanding, an organ, biological
equivalence, energy efficiency, or a higher claim grade. Existing C06/C08 negative findings,
protected evidence, package/schema, release manifests, and release metadata remain unchanged.
## D-V03-0017 — Preregister C15 persistent revision objectives before source editing

**Decision:** Freeze protocol `c15-revision-objectives-v1` and run
`c15-revision-objectives-main-v1` before adding C15 source or observing any C15 model result.
C14 merge `00dccf3dc8f6f70353a536dcf1db9ba0b19fc7b5`, final source
`eb7f542963397eba1b7d9b4a66a7873b3ba17ac4`, artifact commit `4c0d26c`, and the exact C12--C14
artifacts are dependencies. The C14 gate and its four pinned source paths remain unchanged.

Transition truth is evaluator-only and prediction-independent. Insufficient information has
first precedence; recovery is an exogenous A-to-B-to-A return within one entity and one episode;
update is a sufficient change from the immediately previous truth; maintain is the remaining
sufficient stable case. Assessment never starts from an unestablished state. Production input
recursively rejects truth, target, label, expected, evaluator, split, scenario, and test-only
fields. Identifier strings cannot encode targets or splits, and target permutation and causal
prefix tests must prove separation.

Use model seeds 2801--2805, bootstrap seed 4315 and 10,000 hierarchical paired resamples. Freeze
64 train and 32 dev/test episodes, balanced across four worlds, with split-disjoint families.
The dev set is deterministically divided into checkpoint-selection and calibration halves.
Source and focused tests are committed and independently audited, then a source-pin-only
amendment enables the first official runner before any official train/dev/test seed is executed.
Within that runner, checkpoint selection precedes temperature/abstention calibration; I2 Oracle,
official Belief-R, and test data are excluded from both. The official test is evaluated once.
Twelve primary conditions comprise the full separated objective system, each of nine
single-objective ablations, a matched one-weighted-CE baseline that never receives transition
targets, and no-residual. Five non-primary input/entity cells run the full condition only. Dev and
test retain exactly 21,760 prediction rows.

The nine separately logged terms are belief CE, maintain BCE plus temporal drift, update BCE plus
new-versus-old ranking, recovery BCE plus residual floor, explicit no-Ignition BCE, Brier
calibration, evidence-ID attribution BCE, routing sparsity, and load balance. Each term records
eligible count, unweighted and weighted value, and pre-update gradient norms. Zero-weight
ablations have exact zero weighted contribution and gradient. C14 evaluates before mutation;
learned abstention or transition heads may veto but never force Ignition. A no-Ignition decision
retains `evaluated_entity_key`, decays only that entity once, and never clears residual belief.

Engineering completion and scientific support remain separate. Continuous recovery without a
checkpoint, exact matrices/metrics, explicit abstention, ablations, raw reconstruction, atomic
failure, and byte determinism are engineering requirements. Distractor/same-ID/correlated-copy
limits, recovery over no-residual, and the frozen Pareto/noninferiority comparison against weighted
CE determine narrow synthetic scientific support; failure is retained as a negative result rather
than changing thresholds. Any test-driven threshold, loss, split, target, denominator, checkpoint,
or world change requires a new Decision ID and protocol.

Package 0.2.1, persisted schema 0.2, release files, existing schema files, C06/C08 negatives,
claim grades, official Belief-R, and C13 E2 learned slots remain frozen through C15. The C15
internal contract may identify itself as schema 0.3, but package 0.3.0, migration/release manifests,
no-Git archive, and private bundle remain C20 work.

**Reason:** Current v0.2 training implements revision and recovery largely as weights on the same
belief CE, so reuse would violate C15's stop rule and could hide a maintain/update trade-off.
Freezing independent targets, objectives, state semantics, selection order, raw cardinalities,
negative-result policy, and dependency hashes before source editing prevents prediction-derived
labels, test tuning, checkpoint-based pseudo-recovery, Oracle leakage, and retrospective metric
selection.

**Pre-source reconstructibility clarification:** The frozen eight-field fixture evidence remains
the hashed model/evaluator document. Before any C13 ledger insertion, a single frozen adapter
derives opaque sample and Spark IDs from `evidence_id`, registers sample then Spark lineage, and
constructs schema-0.3 `EvidenceRecord` with empty metadata/parent evidence and that one parent
Spark. Exact same-ID redelivery reuses the identical record. This adds no fixture value, target,
threshold, condition, seed, or result and closes the existing strict-ledger lineage boundary before
C15 source implementation.

## D-V03-0018 — Freeze C15 E0/E1 ledger scope and model-derived recovery floor

**Decision:** During source integration review, after pure fixture/model/controller drafts and
non-official self-checks but before any official train/dev/test seed, E0 evaluation, checkpoint
selection, calibration, or C15 result, close two composition boundaries without changing the
frozen fixture documents or their hashes.

`E1_oracle_entity` copies the fixture entity and evidence IDs. `E0_global` maps entity scope to
`__global__` and maps each fixture evidence ID deterministically to
`ev-<H(c15-e0|fixture_evidence_id)>`; all other evidence fields remain paired. Sample/Spark lineage
is then derived from the adapted ID. Same-ID redelivery therefore remains the same adapted ID,
while a distinct correlated-copy ID remains distinct. Attribution targets undergo the identical
ID mapping. This is the sole allowed entity-condition adapter and applies consistently to model
runtime, ledger, controller, citations, and raw trace.

For the recovery objective, `restored_prior_activation` is not a fixture constant and cannot be
set to zero. The runner's frozen training target builder replays that episode's visible context
and model head outputs through `RevisionController`, captures the target-truth activation from the
entity snapshot immediately before assessment delivery, and supplies only that detached numeric
value to the loss. The existing evaluator transition/truth target remains separate and model
predictions never define it.

**Reason:** The first integration review found that the strict fixture-ledger adapter copied the
E1 entity while the preregistered E0 diagnostic required global scope, and that the recovery-floor
formula required model-derived pre-assessment state not present in a static target envelope. The
explicit condition adapter preserves duplicate/correlation identity, and the controller replay
implements the already-frozen recovery formula without checkpoint restoration or prediction-
derived labels. No official numerical result had been executed or observed.

## D-V03-0019 — Freeze C15 stage-local active evidence scope

**Decision:** During focused source testing, before source pinning or any official train/dev/test
seed, the frozen recover fixture exposed an omitted composition boundary: evidence from the B
context stage remained active when the A recovery assessment reached the unchanged C14 gate. The
old A-contradiction rows therefore exceeded C14's frozen contradiction ceiling before the learned
recovery head could be evaluated.

For every C15 context or assessment stage, `RevisionController` keeps the same append-only C13
ledger and audit history but limits the C14 active candidate scope to the current stage. On a trial
ledger, before adding the current deliveries, it deactivates active rows for the evaluated entity
whose adapted evidence IDs are not present in the current stage, using the frozen stage settle time
as the intervention time. It then performs the existing deterministic lineage registration and
delivery sequence. An exact same-ID duplicate within the current stage remains a byte-identical
ledger redelivery no-op. Other entities are untouched. Belief history, residual activations,
citations, model hidden state, and the C14 gate instance remain continuous within the episode.

This stage-scope operation occurs before the already-frozen two C14 settle passes. It does not
change the fixture documents or hashes, evidence values, model inputs, targets, thresholds, C13 or
C14 protected source, objective weights, seeds, selection order, or result gates. A fixture that
would require restoring an inactive ID from an earlier stage is non-compliant; the frozen generator
does not create that case.

**Reason:** Accumulating mutually superseded observations as simultaneously active propositions
made the preregistered A-to-B-to-A world structurally unable to reach its recovery decision. An
audited stage-local active view preserves immutable evidence history while making each observation
stage, rather than the whole episode's superseded evidence, the attributable input to C14. This
closes an implementation boundary discovered by an acceptance test without tuning against any
official model seed or result. No official training, checkpoint selection, calibration, E0
evaluation, or test evaluation had been executed or observed.

## D-V03-0020 — Supersede unevaluated C15 v1 after a pre-pin fixture probe

**Decision:** Invalidate the C15 v1 execution procedure before source pinning. During focused
source testing, tests used v1 split episodes as inputs to deterministic `RevisionController`
probes. This violated the frozen order requiring focused tests to avoid official train/dev/test
seeds before the source-only commit, even though no learned training, checkpoint selection,
calibration, E0 diagnostic, test evaluation, artifact generation, or result-driven tuning had
occurred.

Protocol `c15-revision-objectives-v2` and run `c15-revision-objectives-main-v2` supersede v1.
Freeze fresh train/dev/test episode-seed bases 151000/251000/451000, model seeds 2851--2855, and
bootstrap seed 4365. Freeze the independently reconstructed split-manifest SHA-256 values as
train `0f33808ba39613c998a3015d1cf0aa2adbe2808d0c4c455a8da63dc6fe45489e`, dev
`e161c6bb652fd35a82e17e22003c792b3001f6b8a9d5c608c2e3e0caffb2b0b6`, and test
`e4dc44af60c268ac57ea38904cefd4f31bf6f35ac40178a319aa5d8688648fd5`; freeze full-fixture
SHA-256 as train `2d5de7eef61a4d92f8e1a83cf92670e42688f32ac0abe0295d0d736dbce2ff2b`, dev
`1714829588a605bfa6a38b443f452dc86b2bdcb71929631e7cc26e2c24b975d8`, and test
`6cf39d823996bd37c9bec4ee9bc7fd235b51da3e2931d3337190d50c60bfef64`.

All focused runtime/controller tests must use explicitly reserved synthetic fixtures and a
non-official model seed. Pure reconstruction of the frozen fixture documents for hash checks is
allowed and does not execute the model or controller. Carry forward D-V03-0017 through
D-V03-0019, every condition, objective, threshold, metric, gate, cardinality, output schema,
protected hash, and negative-result policy unchanged.

**Reason:** Replacing the unpinned, unevaluated seed surface restores a clean preregistered order
without hiding the procedural breach or reusing observed fixture-controller combinations. The
change is contamination control, not a response to learned performance or test metrics. v1 must
not be source-pinned or executed.

## D-V03-0021 — Freeze C15 failed-seed artifact semantics

**Decision:** Before the source-only commit or any official v2 execution, close the gap between
the requirement to retain failed seeds and the success-only fixed cardinalities. Treat one model
seed as the atomic execution unit across all twelve conditions. Buffer all rows for that seed. On
the first failure, discard its whole buffer, do not retry it, record exactly one row with fields
`model_seed`, `phase`, `condition_id`, `error_type`, and `error_hash`, then continue with the next
frozen seed. `error_hash` is SHA-256 of canonical `[phase, condition_id, error_type]`; exception
messages and machine-local paths are not artifacts.

Every JSON artifact with `failed_seeds` repeats the same list sorted by model seed. The raw JSONL
contains only complete successful prediction rows, and `report.md` names each failure. For S
complete seeds, raw, training-step, condition-seed, objective, confusion-seed, calibration-seed,
and Pareto-seed cardinalities are respectively `4352*S`, `4608*S`, `12*S`, `108*S`, `34*S`,
`34*S`, and `12*S`. When S is positive, descriptive aggregate/confusion, aggregate/Pareto, and
pairwise row counts remain 34, 12, and 66; when S is zero they are empty. No partial seed row is
published or imputed.

Any failed required seed fixes engineering status to `implementation_failure` and scientific
status to `not_evaluated_implementation_failure`. All nine bootstrap rows retain the frozen
resample count and bootstrap seed but use null effect/lower/upper. Successful rows and descriptive
aggregates remain inspectable but cannot support a scientific gate. If every seed fails, publish
the same exact eight files with static objective configuration, empty data/derived arrays, the
common failed-seed list, implementation-failure status, and null bootstrap results.

**Reason:** The preregistered v2 artifact schemas named `failed_seeds` and required null bootstrap
effects, but did not define an exact failure row or how fixed success cardinalities shrink. A
source review found the runner could only abort atomically and emit no failure evidence. This
amendment makes failure reporting reconstructible without inventing predictions, dropping a
failure silently, or mixing incomplete seeds into a scientific conclusion. No official v2 seed,
training result, checkpoint, calibration result, diagnostic, or test result had been executed or
observed.

## D-V03-0022 — Freeze the exact C15 implementation-failure objects

**Decision:** Before source pinning and while failure-path tests remain synthetic, make the
D-V03-0021 failure bundle byte-reconstructible. `pareto_frontier.scientific_support` retains its
normal seven fields. `status` is `not_evaluated_implementation_failure`. `variant_gates` retains
the exact three variant keys with zero changed pairs and denominator, null rate, the frozen
maximum, and `passed=false`. `residual_gate` retains null full/no-residual recovery rates and
`passed=false`. Each of the exact five weighted-CE noninferiority rows keeps its margin and
direction, uses a null effect, and fails. `strict_improvement` retains the exact five effect keys
as null plus the frozen minimum and `passed=false`. `all_gates_passed=false`. All nine bootstrap
entries keep resamples 10000 and seed 4365 with null effect/lower/upper.

`loss_ablation_metrics.scientific_gates` is byte-equal to that scientific-support object. Its
normal eight engineering-gate rows remain present; partial observations remain visible,
unavailable denominators are null, and the raw-count, training-step-count, and all-seed recovery
requirements fail, fixing overall engineering status to `implementation_failure`.

When no seed succeeds, `per_transition_predictions.jsonl` is exactly zero bytes. Prediction,
training, condition-seed, objective, confusion/calibration, Pareto point, and pairwise arrays are
empty. The normal dimensions and twelve static objective-configuration rows remain, with
parameter count 3132 and optimizer steps 384, and every JSON artifact repeats the common failure
list. Exception text is not included.

**Reason:** D-V03-0021 fixed seed atomicity and cardinality scaling but left multiple valid JSON
shapes for the required seven-field scientific object and empty JSONL. Freezing one representation
prevents implementation-dependent failure artifacts and makes zero-success behavior testable. No
official v2 source pin, seed, training result, checkpoint, calibration result, diagnostic, or test
result had been executed or observed.

## D-V03-0023 — Supersede failed C15 v2 with nullable statistics and a hard worker deadline

**Decision (2026-08-26):** Preserve R-V03-0007 and v2 source
`bb89797c92a8a5f38216dac00f48cfa59f66381f` as failed execution history. The official v2 run
reached global aggregation, where a nullable metric was coerced to float; its traceback does not
identify whether F1 or ECE was the first undefined operand. No final bundle or numerical evidence
was accepted. The run also exceeded the frozen 120-second limit, which the source did not enforce.
These are implementation failure and protocol noncompliance, not scientific negatives. Do not
rerun v2 or relabel global failure as a failed model seed.

Preregister protocol `c15-revision-objectives-v3`, run `c15-revision-objectives-main-v3` before
source correction. Model seeds are 2901--2905, bootstrap seed 4415, and train/dev/test episode
bases 152000/252000/452000. Pure fixture reconstruction, independently repeated without model or
controller execution, gives manifest SHA-256 train
`70d8b6a0ddd0aad7adeefbe4473c93cb74c25316f5435cc7ba09ebdd837b236d`, dev
`345b3d30f64017799329edeb9ec90afb6c994ffcae2160d0dc5be5300bdc00a8`, test
`c8c1ae76d103b0d375903f56d4089bf9fca62d597abaaba6507720fdcae71806`; full-fixture SHA-256 train
`6e3c82e943b52d4f5b140b60c871bfdbd962c930a0470f015e27e760d4aafd36`, dev
`77a6e6644220e7654dd8ab94eca27639e23a984e7fc674e529a1df6709113587`, test
`76f7945ff02b8689a8c341353278fa43354194963e344ed3e88d7930e4108510`.

Preserve the existing no-ignition F1 formula: harmonic mean of precision and recall, null when
either is undefined or their sum is zero. ECE remains null without decided rows. Paired effects
are null if either operand is null. Consume all 10,000 bootstrap draws without dropping,
redrawing, or imputing any undefined effect. Every interval has exactly effect/lower/upper,
resamples/bootstrap_seed, and defined_resamples/undefined_resamples. Counts are integers summing
to 10,000 on a completed bootstrap. Any undefined draw or point effect makes both bounds null;
a finite point effect remains visible. Failed-seed rules prevent bootstrap execution and leave
all five effect/bounds/count fields null. Null point effects fail their required residual or
noninferiority gate; strict improvement considers only finite effects. All required point gates
must pass for supported; otherwise the completed scientific result is not_supported. Descriptive
interval availability does not change a finite point-estimate gate.

Freeze a 3,600-second hard worker budget. Parent preflight is excluded; monotonic timing starts
immediately before spawning one worker. The parent must confirm worker exit by the deadline.
The worker performs training, selection, calibration, evaluation, aggregation, validation, and
staging writes; only the parent publishes after successful worker exit and exact eight-file
inventory validation. On timeout terminate/join for five seconds, then kill/join for five seconds
if alive. Even a later normal exit does not permit publication. Cleanup requires confirmed worker
termination; otherwise retain quarantined staging and report its absolute path on stderr. A new
output stays absent; an existing empty output stays empty. Raise `C15RunTimeoutError`, CLI exit
124, for global timeout including a surviving worker; other global failures exit 1. No local
path, exception message, or elapsed time enters scientific artifacts. Record any global timeout
as a resource-limited implementation failure, never a failed model seed.

All world formulas, architecture, losses, optimization, selection, calibration, scientific
thresholds, C14 dependency, protected hashes, package/schema freeze, and negative-result policy
remain unchanged. Tests use reserved synthetic data and non-official seeds until a source-only
commit and separate pin amendment authorize the new official execution.

**Reason:** Explicit nullable statistics repair a contract contradiction without inventing
observations. An enforceable worker deadline repairs resource control; the larger budget is not
a scientific threshold change. Fresh seeds isolate the failed execution from the new procedure.

## D-V03-0025 — Isolate the C15 post-pin test-fixture repair from scientific execution

**Decision (2026-08-26):** Preserve C15 v3 source
`eedb8b426f326c5dcb70bd548008695eb1652aee`, authorized execution tree
`6860c2ec4133a9debefdec0b92e33ab0e09b430f`, its protocol, and every generated artifact byte.
Repair only the synthetic base fixture in
`test_protocol_amendment_allows_exactly_four_dependency_fields` on a separate integration branch.
Remove the two base-provenance fields from that fixture and restore a pending synthetic source pin
and disabled execution guard before constructing the four-field amendment under test.

CI run `32914883175` failed on Python 3.11 and 3.13 after the execution-pin amendment. The same
single test fails locally on the unchanged execution tree: it reads the already-amended current
protocol as if it were the unamended base, while the production validator correctly removes the
two amendment-only provenance fields before comparing with the base. The real committed
preregistration-to-execution amendment passes validation; in-memory fixture normalization makes
both the permitted-amendment and forbidden-protocol-change assertions pass. No model, controller,
training, or scientific metric execution was needed for this diagnosis.

This is an administrative test-harness correction, not a scientific protocol amendment or a new
source pin. It does not authorize execution from the integration tree: the existing post-pin
source/test guard must reject that tree. Scientific reproduction must check out execution commit
`6860c2ec4133a9debefdec0b92e33ab0e09b430f` and use the unchanged source pin above. A later green
integration test suite must not be described as a green full suite or clean-room test phase on
the original execution tree; the original tree retains this known fixture failure.

The completed official v3 run reports engineering `fail`, scientific `not_supported`, and no
failed model seeds. Preserve those results independently of this fixture repair. In particular,
do not relax the all-seed recovery gate, reclassify C15 as accepted, or unblock the C17 dependency.
Independent byte reproduction is still pending at the time of this administrative decision.

**Scope:** No runner/runtime, world, objective, threshold, seed, protocol, release manifest,
package/schema, protected artifact, or canonical report changes. No public release or upload is
authorized by this decision.

## D-V03-0026 — Preregister C15 v4 assessment-only learned veto with fresh identities

**Decision (2026-08-27):** Preserve R-V03-0008, C15 v3 source
`eedb8b426f326c5dcb70bd548008695eb1652aee`, execution tree
`6860c2ec4133a9debefdec0b92e33ab0e09b430f`, protocol bytes, exact-eight transport, engineering
`fail` and scientific `not_supported` interpretations without amendment. V4 is a new experiment,
not a rerun, replacement, or favorable reinterpretation of v3. Its separate machine authority is
`artifacts/v03/c15_revision_v4/protocol.json`, initially with `c15_source_pin=null` and
`runner_execution_allowed=false`.

The correction was selected from retained v3 **dev rows only**. In the primary
full/I1/E1/base dev cell, all 200 context-stage C14 proposals ignited, but assessment-calibrated
learned abstention vetoed 136 of those 200 context stages. In the 40 recovery dev rows, all C14
proposal sequences were the correct A-to-B-to-A sequence. The recovery-head sigmoid reconstructed
from the retained abstention sigmoid and four-way transition-softmax log ratio was at least
`0.9204247345397955` for every row. Thus the observed blocker was a scope mismatch: supervision and
calibration covered assessment decisions, while the same veto was also applied to context state
construction. No v3 test row or v4 official seed informed this correction.

V4 therefore keeps learned belief probabilities as the input to unchanged C14 on every stage and
keeps every C14 rejection final. A context-stage C14 Ignition constructs persistent history without
an additional learned abstention or transition-head veto. The assessment stage alone retains the
development-calibrated learned abstention and maintain/update/recovery-head vetoes. Stage role is
fixed scheduler metadata and is not a model input; truth, transition labels, split, episode seed,
and test metadata remain unavailable to the model/controller.

Freeze model seeds 2951--2955, bootstrap seed 4465, and train/dev/test episode bases
153000/253000/453000. Merely changing episode bases would reuse v3 family IDs because the earlier
family derivation omitted the episode seed. V4 therefore freezes the distinct `c15v4-*` namespace
for family, episode, entity, evidence, source, group, correlated-copy, E0 mapping, sample, and Spark
derivations. Independent pure-fixture implementations, neither importing nor executing a model or
controller, agree on manifest SHA-256 train
`bfd3e031edcc9d0c23a55bac1f5797420f1f85d7fca0a0e689ca4ff414fc3266`, dev
`e4f7cc4ab4c2fa5c81a6d17c927424a3575431f0a6578ab87146c130ab87d6f7`, test
`66d580f4e63a55f4a26441709caf8b443bfe701fdac548ff22867a60b7a31cf6`; full-fixture SHA-256 train
`4bb90acded764199b912b712becc16252c791086dbddc9f80259dd99de5ea455`, dev
`8cec9458524b467c54927ba46a3055754e59aa531de21d8a8037bec993c04589`, test
`cd27e177476f5c0adba37bf7c4e5284996f6155dd4d61ed1547be2bf1a7051c6`.

All eight engineering gates, their denominators, the twelve conditions, objective weights,
training/selection/calibration budgets, exact-eight artifact inventory, failure semantics,
10,000-draw paired bootstrap, scientific thresholds, C12--C14 dependencies, package 0.2.1,
persisted schema 0.2, and C06/C08/C15-v3 negative-result boundaries remain unchanged. In
particular, no all-seed recovery, residual-superiority, ECE, or weighted-CE margin is relaxed.
Scientific `not_supported` remains compatible with engineering acceptance only if all eight
engineering gates independently pass.

Execution order is mandatory: commit this disabled preregistration; implement and commit only the
authorized source/test paths using reserved synthetic fixtures; complete focused/full/readiness and
independent source audit without executing v4 official train/dev/test seeds; amend exactly the four
source-pin fields and enable the runner; rerun full verification; execute the official train/dev/test
sequence once; independently recalculate raw-to-derived results; then require all eight files to be
byte-identical under a distinct `PYTHONHASHSEED`. Any source change after v4 test inspection requires
a new Decision ID, new namespace/seeds/splits/bootstrap, and a new protocol.

**Reason:** Restricting a development-calibrated veto to the decision scope on which it was trained
repairs a pre-test mechanism mismatch without forcing recovery, weakening C14, altering scientific
gates, or discarding the completed v3 negative result. Fresh identities prevent hidden reuse across
experiments.

## D-V03-0029 — Preregister label-blind C17 functional-organ evaluation

**Decision (2026-08-27):** Preregister protocol `c17-functional-organs-v1`, run
`c17-functional-organs-main-v1`, from accepted C15 v4 and C16 integration commit
`74fbf5c880d49291b087c9beecc255d838da49dd`. The machine-readable authority is
`artifacts/v03/c17_functional_organs/preregistration.json`, raw SHA-256
`736c122c4eb50e35d84bca548ccdea97d920ee75c860799a29003caa4fd71c5c`. This first commit has a
null source pin and disabled runner; it authorizes no official model, controller, train, dev,
test, held-out, or artifact-result execution.

Candidate discovery is train-only and blind to evaluator function names, truth, targets, rewards,
C15 decisions, and test metadata. It operates on opaque C16 online-prototype candidate activity
and message flow, then locks one structurally ranked candidate per seed/resource cell. Development
data maps that candidate to one evaluator function before any test or related-unseen held-out
evaluation. Candidate identities are never aligned across seeds.

The primary cell is capacity/bandwidth/workspace/compositionality `8/2/2/2`. Four secondary cells
change exactly one factor: `4/2/2/2`, `8/1/2/2`, `8/2/1/2`, and `8/2/2/3`. Secondary cells are
moderator analyses and cannot rescue a failed primary result. Targeted ablation is paired with
unablated, random-unmatched, size-, degree-, load-, and activity-matched branches selected from
train traces only. Every control is mandatory.

Freeze official run seeds 4701--4705, reserved test seeds 9901701--9901702, bootstrap seed 5717,
and split bases 171000/271000/471000/571000. Two independent pure-fixture implementations, neither
importing nor executing a model or controller, agreed exactly. The per-seed manifest hashes are
fixed for all five seeds together with the five full-fixture SHA-256 values in the preregistration
file; each corpus contains all five resource cells and all four splits.

Retain the G08 minima: seed consistency 3, structural cohesion 0.55, functional selectivity 0.20,
held-out causal reuse 0.20, targeted impairment 0.05, targeted-minus-each-control impairment 0.03,
and unrelated collateral 0.02 maximum. The primary result additionally requires the registered
paired bootstrap bounds. Candidate absence or a failed scientific gate is `not_supported`, not an
implementation failure; engineering completion remains possible with negative science.

C14 remains the only proposal source. The C15 v4 learned path can assess a C14 proposal only as
allow, veto, or abstain; it cannot create, replace, or revive a rejected proposal. C08's candidate
pair `(9, 14)`, unavailable development target, E0 grade, negative artifacts, and prohibited
"organs emerged" wording remain immutable and are not C17 labels or controls. C16 CC2/CC3 remain
not supported and are not promoted by dependency reuse.

Implementation may change only the eight preregistered C17 source/test paths. A separate
source-only commit, independent audit, and exact four-field protocol amendment must precede the
first official execution. Package 0.2.1, persisted schema 0.2, release manifests, C06/C08/C15
negative evidence, accepted C14--C16 source/artifacts, and claim grades remain frozen.

**Reason:** Label-blind structural discovery, a locked development mapping, all required matched
controls, fresh identities, causal held-out reuse, and an explicit proposal/assessment boundary
are the minimum falsifiable test that distinguishes a functional-organ candidate from the C08
router/cluster negative or incidental C16 recurrence.

## D-V03-0030 — Correct C17 dependency pin and pure-fixture specification

**Decision (2026-08-27):** Amend only the disabled C17 preregistration contract after independent
audit found that the abbreviated C16 pin and prose-only full-fixture description were insufficient
for a third party to reproduce the frozen hashes from the preregistration alone. Resolve `c16_pin`
to `b1c83e619e3c05215bb8878b8294367615b8e058` and add the complete standard-library construction
contract: exact object keys and types, array order, every SHA-256 identifier preimage and prefix
length, episode and frame formulas, entity/hypothesis/action fields, binary64 amplitude calculation,
ordered `base_values` writes, manifest transform, and canonical hash bytes.

The corrected machine-readable authority has raw SHA-256
`5722f4cdc1feb99e7213546365601c168499e5d2bbe31db49721e59350d069bf`. It supersedes only the raw
preregistration hash recorded by D-V03-0029. Protocol ID, run ID, seeds, split bases, resource cells,
thresholds, controls, exact-nine outputs, all five manifest hashes, all five full-fixture hashes,
claim boundaries, `source_commit=null`, and `runner_execution_allowed=false` are unchanged. No C17
source, test, model, controller, or official fixture execution is authorized by this amendment.

**Reason:** A frozen digest is auditable only when the hashed document is reconstructible without
consulting a future implementation. Expanding the machine contract removes that ambiguity without
changing experimental degrees of freedom or converting C08/C15/C16 negative evidence into support.

## D-V03-0031 — Preserve the C17 v1 implementation failure and separate its correction

**Decision (2026-08-28):** Preserve run `c17-functional-organs-main-v1` and its exact-nine
bundle as immutable failure evidence. The run completed all five official seeds with no failed
seed, but engineering status is `implementation_failure`: `control_completeness` failed because
each R4 seed discovered a two-member target from a two-candidate bank, leaving a zero-member
non-target pool for all five required controls (25 missing control slots in total). The artifact
reports scientific status `not_supported`; the valid scientific interpretation is instead
`not_evaluated_implementation_failure`, because incomplete mandatory controls prevent a scientific
evaluation.

The canonical bundle-manifest SHA-256 is
`9a3c50f3773d6dc40652adce06db6158a0aaeb3867fb0945078878614e58374f`. A second execution with
`PYTHONHASHSEED=8675309` matched all nine artifact bytes. The official execution's hashseed was not
recorded, so no distinct-hashseed claim is made. C17 v1 source, protocol, thresholds, and artifacts
must not be revised after inspection. Any engineering correction belongs to C17 v2 with a separate
decision, protocol identity, audit, and execution. Package 0.2.1, persisted schema 0.2, release
metadata, C06/C08 evidence, and accepted dependency evidence remain unchanged.

**Reason:** The observed failure is a design-level control-construction defect, not a failed seed
and not evidence for or against the preregistered organ hypothesis. Preserving the bytes and
separating a future correction prevents retrospective repair of the inspected v1 result.

## D-V03-0032 — Preregister the C17 v2 control-feasibility correction

**Decision (2026-08-28):** Preregister protocol `c17-functional-organs-v2`, run
`c17-functional-organs-main-v2`, as a new engineering correction under
`artifacts/v03/c17_functional_organs_v2/`. The machine-readable authority is the disabled
`preregistration.json`, raw SHA-256
`8c970b69fd2ded26d8eb49df9c88654d0991868d174ae081f253a4b57df25491`. Its base and source pins
are null and its runner is disabled. This decision authorizes no official model, controller, or
reserved-fixture model execution.

C17 v1 remains immutable engineering-failure evidence. Its empty R4 comparator pool is treated
only as `engineering_feasibility_failure`; v1 science is
`not_evaluated_implementation_failure`, not positive or negative organ evidence. V2 does not
change any scientific metric, threshold, primary/secondary resource cell, proposal/assessment
boundary, bootstrap method, claim boundary, package version, or persisted schema.

V2 adds one train-only candidate-eligibility invariant. A candidate of size `m` is rankable only
when the non-target pool has at least `m` members, equivalently when
`comb(non_target_pool_count, m) >= 1`. All five controls select exactly `m` members from this
same domain. The existing permission for different control types to reuse one subset remains;
requiring five distinct or disjoint subsets would introduce an unregistered scientific change.
Candidate absence remains a valid scientific negative and may be engineering-complete. Once a
candidate is selected, a missing, wrong-size, overlapping, or out-of-pool control fails the seed
closed before development, test, or held-out evaluation and leaves science unevaluated.

Freeze official seeds 4801--4805, reserved pure-fixture seeds 9901801--9901802, bootstrap seed
5817, split bases 181000/281000/481000/581000, and the distinct `c17v2` identity namespace.
Two independent standard-library implementations reproduced all five full-corpus and all five
manifest SHA-256 values without importing or executing model/controller code.

The final artifact inventory is exact-ten. Two isolated workers first generate pre-final
exact-nine staging bundles under `PYTHONHASHSEED=11801` and `21801`; neither worker may assert
reproduction. A separate compare/finalize mode validates both bundles, compares the nine raw byte
streams, emits `reproduction_compare_manifest.json`, and only then regenerates the final
acceptance matrix and report. The comparison manifest hashes neither itself nor those final two
files. The validator reconstructs their pending pre-final forms in memory, so reproduction
evidence is bound without a self-hash cycle.

The preregistration also freezes exact artifact and nested-row schemas, nullability, enums,
ordering, uniqueness, raw-row scaling, dynamic feasibility equations, zero-success behavior, and
external-finalization evidence. C17 v1 exact-nine and source bytes are directly protected; its
recursive protected manifest continues to bind C06/C08, accepted dependencies, package/schema,
release metadata, and claim boundaries.

Implementation may change only seven paths: C17 contracts, worlds, discovery, evaluation, the
existing runner, and its two test files. `v03_organs/__init__.py` is protected because no public API
change is required. After source-only implementation and independent audit, a separate amendment
may change exactly `base_commit`, `base_sha256`, `source_commit`, and
`runner_execution_allowed`. Any other preregistration change requires another protocol.

**Reason:** Train-only construction feasibility repairs the specific v1 engineering defect while
preserving the negative-result boundary and all scientific degrees of freedom. External evidence,
rather than a worker-controlled flag, is the minimum non-circular basis for byte-reproduction
acceptance.

## D-V03-0033 — Complete the disabled C17 v2 integrity schemas

**Decision (2026-08-28):** Correct only integrity omissions in the still-disabled C17 v2
preregistration. The corrected canonical raw SHA-256 is
`b9e4dcda26d5d85064b3fbf6d453a8ed9efe0b7541fd5cb617ef37868be918ca`.
Base/source pins remain null and the runner remains disabled; no source, model, test, controller,
reserved model fixture, or official execution is authorized.

Add `secondary_cell_status_rows` to the exact acceptance-matrix top-level schema. It contains
exactly four rows, ordered R1 through R4, with exact fields `condition_id`,
`primary_rescue_allowed`, `role`, and `scientific_status`; every row is secondary and cannot rescue
R0. Add `not_evaluated_implementation_failure` to the registered status categories so the v1 and
selected-candidate failure contracts use an explicitly valid status.

Complete the external comparison schema with exact top-level and nested keys, types, values,
nullability, enums, array order, and no-extra-key rules. `protocol_sha256` is the digest of the raw
pinned preregistration bytes, including exactly one LF. It is not the disabled preregistration hash.
The pinned preregistration contains no comparison-manifest or final acceptance/report hash, so both
staging runs and the final exact-ten bundle can share this byte string without a hash cycle.

Freeze the control-feasibility preimage and its SHA-256
`7a893c4f898e7bd560181e028efcaa4da790c6edab12ef2a5bc13ac4b638abd0`, plus the exact canonical
preimage for each `selection_input_sha256`. The feasibility requirement `n >= m` exists for the
four matched controls. Correct the earlier D-V03-0032 shorthand: random-unmatched is not
target-size matched. It retains the v1 size-hash behavior with a fresh `c17v2` preimage, requests
size one through four, clips that size to the non-target pool, and hash-ranks combinations. Size-,
degree-, load-, and activity-matched controls each retain target size `m`.

**Reason:** A validator cannot enforce cardinality, evidence provenance, or external reproduction
from prose-only or incomplete nested schemas. These additions remove ambiguity without changing a
science metric, threshold, resource cell, fixture, rank, proposal/assessment boundary, or claim.

## D-V03-0034 — Remove the final C17 v2 preregistration contradictions

**Decision (2026-08-28):** Correct two residual prose contradictions in the disabled C17 v2
machine preregistration. The corrected canonical raw SHA-256 is
`89773ca193e18784187926424a1490c9551b11d7511e51dd370d36aaa026d6ca`.
Base/source pins remain null and the runner remains disabled; no source, test, model, controller,
reserved model fixture, or official execution is authorized.

The validator and stop-condition wording now use one type-specific control rule. Random-unmatched
requests a hash-derived size from one through four and clips it to non-target pool length. The four
matched controls each require target size `m`. A complete row must satisfy its own registered size
rule, not a universal same-size rule.

The obsolete comparison-input summary that described an array preimage is replaced by a reference
to the already frozen exact-key object in `comparison_input_sha256_preimage`. This correction does
not alter that object's keys, types, ordering, serialization, or digest rule.

**Reason:** Contradictory summaries can cause a conforming implementation to reject valid random
controls or hash a different reproduction preimage. Removing them changes no experiment degree of
freedom.

## D-V03-0035 — Accept C17 v2 engineering evidence and retain the negative organ result

**Decision (2026-08-28):** Accept the independently audited C17 v2 official execution at its
registered engineering boundary and retain its final exact-ten bundle under
`artifacts/v03/c17_functional_organs_v2/`. The run completed official seeds 4801--4805 with no failed
seed and passed all 16 engineering gates. Every one of the 25 seed/condition cells recorded primary
candidate absence: 20 because no group passed the frozen activity filter and five because no
activity-eligible group also satisfied the train-only control-feasibility predicate. The
preregistered candidate-absence contract therefore makes this an engineering-complete scientific
negative. Scientific status is `not_supported`, all eight primary scientific gates remain false,
and CL-008 remains E0.

Two separately spawned staging workers, with fixed `PYTHONHASHSEED` values 11801 and 21801, produced
byte-identical registered exact-nine bundles. Their combined SHA-256 is
`177aca36f3f2def1b1b49f6760fd32c84418cfdda4f94415fc64b9ead3533d1a`. The runner validated worker
provenance and both pre-final bundles before emitting the canonical comparison manifest, raw
SHA-256 `a9bf16cc3d29f250fec18cac0e9821ba1f7ae02f6a7b9fe793f95419dfecc7c2`, and one final exact-ten
bundle. This decision does not assert byte equality between two final exact-ten directories.

C17 v1 remains immutable implementation-failure evidence. No v2 threshold, fixture, seed, resource
cell, metric, proposal/assessment boundary, or control rule is changed after inspection. Package
0.2.1, persisted schema 0.2, release files, C06/C08 evidence, accepted C14--C16 evidence, and all
other claim grades remain unchanged.

**Reason:** The corrected feasibility contract ran exactly as preregistered and preserved
candidate absence as a falsifiable negative result. Recording engineering acceptance separately
from scientific support prevents a completed pipeline from being mistaken for evidence that a
functional organ formed.

## D-V03-0036 — C20 private release-candidate evidence boundary

**Decision (2026-08-28):** Generate v0.3 release evidence only after the final source commit.
The artifact layer must bind source manifest, artifact metadata, evidence map, bounded primary
index, reproduction contract, SBOM, source-license inventory, report, and figures. C19 remains
the exact-nine blocked readiness record. No claim grade changes, public tag, public archive, or
public release are authorized while the owner license decision is pending.

## D-V03-0037 — Keep v0.3.1 corrective evidence separate from v0.3.0 release evidence

**Decision (2026-08-28):** Treat v0.3.1 as a future corrective version boundary, not as a reason
to rewrite `artifacts/release/v0.3/`. A later v0.3.1 source commit must generate a separately
versioned evidence directory and bind it only after its own source and artifact integration commits.

**Scope:** C11--C19 evidence retains its recorded disposition. In particular C19 remains blocked
until a truth-free adapter and a new preregistered protocol exist. No public archive, tag, release,
license selection, claim-grade increase, or modification of saved scientific outputs is authorized.

## D-V03-0038 — Version the future integrated Brain Lab surface

**Decision (2026-08-28):** Preserve legacy `sparkbrain.lab` and `/api/runs*` as the v0.2 reference
Brain Lab. The future v0.3 runtime surface is `sparkbrain.v03` with an explicit `/api/v03/*` API;
its intended names are `IntegratedV03Brain`, `V03BrainConfig`, `SensorySample`, and
`V03StepResult`.

**Reason:** Replacing the legacy UI or presenting the C18 manually recorded trace as a live C12--C18
execution would erase the compatibility and scientific-boundary distinction. C16 concept and C17
organ signals are observer-only until separately preregistered causal evidence permits a decision
role.

## D-V03-0039 — Accept the v0.3.1 integration as engineering evidence only

**Decision (2026-08-28):** Accept the explicit `sparkbrain.v03.IntegratedV03Brain` facade and
`/api/v03/*` Brain Lab as the v0.3.1 local engineering integration boundary. I3 uses the actual C15
`RevisionController`; I2/E1 require explicit Oracle-diagnostic permission; E2 is unavailable; and
C16/C17 outputs remain observer-only. The seven ablations and eight-world/ten-variant evaluator
must remain fixed-contract engineering evidence and must not be reported as external performance or
scientific superiority.

The Brain Lab preserves legacy `/api/runs*`. A causal evidence-removal or comparison generated by
the Lab rather than the runtime trace must identify itself as an observer counterfactual. World
feedback may re-enter only as truth-free sensory/evidence and must reject evaluator-owned fields.

**Reason:** Wiring modules into a persistent system is necessary software evidence, but it does not
repair C15's unsupported residual advantage, promote C16 candidates or C17 organs, or unblock C19.
Keeping those boundaries explicit prevents engineering completion from becoming a scientific
claim upgrade.
