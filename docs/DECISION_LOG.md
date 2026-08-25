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
