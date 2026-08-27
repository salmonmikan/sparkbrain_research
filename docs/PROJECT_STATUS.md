# Project Status — SparkBrain v0.3.0

## v0.3 release migration boundary

The package version is now `0.3.0`. The accepted v0.2.1 reference engine retains
persisted config/state/trace schema `0.2`; it is not silently migrated or reinterpreted.
The additive C18 trace/checkpoint interface uses schema `0.3` only for its own explicit
payloads. Historical v0.2.1 artifacts, protected hashes, and C06/C08 negative evidence remain
available while the v0.3 release manifest is prepared. C19 external validation is not counted
as accepted release evidence until its independently pinned status is integrated.

## v0.3 C18 — trace, checkpoint and Brain Lab integration

C18 v6 retains the independently audited official exact-seven bundle under
`artifacts/v03/c18_brain_lab_v6/`, pinned by
`c0c242d848588d76015734a309f72fed0bd1d380` and fixed official seed `1802`.
The bundle records preflight evidence, strict schema validation, deterministic
checkpoint replay, parent-bound fork lineage, and a CDN-free static Brain Lab
export. Engineering status is `accepted` only for this deterministic
observability/replay contract; scientific status remains `not_supported`.

## v0.3 C17 v2 — engineering accepted; scientific support not supported

C17 v2 completed the preregistered official seeds 4801--4805 once under protocol
`c17-functional-organs-v2` and published the final exact-ten bundle under
`artifacts/v03/c17_functional_organs_v2/`. All 16 engineering gates passed, no seed failed, and the
registered candidate-absence contract was exercised in all 25 seed/condition cells: 20 recorded
`no_activity_eligible_candidate` and five recorded `no_control_feasible_candidate`. Candidate
absence is an engineering-complete scientific negative, so the engineering status is `accepted`
while the scientific status is `not_supported`.

Two separately spawned pre-final workers used fixed `PYTHONHASHSEED` values 11801 and 21801. Their
exact-nine bundles were byte-identical with combined SHA-256
`177aca36f3f2def1b1b49f6760fd32c84418cfdda4f94415fc64b9ead3533d1a`; the validated comparison
then produced the single final exact-ten bundle and
`reproduction_compare_manifest.json` (SHA-256
`a9bf16cc3d29f250fec18cac0e9821ba1f7ae02f6a7b9fe793f95419dfecc7c2`). This is not a claim that
two final exact-ten directories were compared. Independent source, pin, execution, and artifact
audits passed. CL-008 remains E0: no primary candidate was selected, all eight primary scientific
gates failed, and no functional-organ or emergent-organ claim is permitted. C17 v1, package 0.2.1,
persisted schema 0.2, release metadata, C06/C08 evidence, and accepted C14--C16 evidence remain
unchanged.

## v0.3 C17 v1 — immutable implementation failure

C17 v1 completed official seeds 4701--4705 and published the exact-nine bundle under
`artifacts/v03/c17_functional_organs/`, with no failed seed. Engineering status is
`implementation_failure`: the R4 candidate in every seed used both members of its two-candidate
bank, leaving a zero-member non-target pool and 25 missing mandatory matched-control slots. The
bundle's displayed `not_supported` scientific status is retained byte-for-byte, but the valid
interpretation is `not_evaluated_implementation_failure` because control completeness failed.

The bundle-manifest SHA-256 is
`9a3c50f3773d6dc40652adce06db6158a0aaeb3867fb0945078878614e58374f`; a reproduction with
`PYTHONHASHSEED=8675309` matched all nine files. The official hashseed was not recorded, so no
distinct-hashseed claim is made. C17 v1 is immutable. A C17 v2 engineering correction is planned
under a separate protocol and audit. Package 0.2.1, schema 0.2, release metadata, C06/C08 evidence,
and accepted C14--C16 evidence remain unchanged.

## v0.3 C16 — bounded proto-concept formation

C16 is accepted for the preregistered synthetic protocol `c16-proto-concepts-v1` and run
`c16-proto-concepts-main-v1`. The official exact-eight artifact bundle is retained under
`artifacts/v03/c16_proto_concepts/` from source commit
`4933a6059240875d0548fe602f114d768a49ef28`; the recorded integration branch is
`codex/c16-proto-concepts`, whose pre-artifact head `3dd9593` merges the source-only lineage
through pin commit `b1c83e6`. All eight engineering gates passed with zero failed seeds. The raw
bundle retains 990 lineage rows, 90 bank rows, 5 learned checkpoints, 5,760 held-out episode rows,
360 seed summaries, 72 utility aggregates, 60 control banks, 240 seed comparisons, 48 aggregate
comparisons, 1,920 causal rows, and 60 counterexample rows.

CC0 is supported for 109 recurring synthetic candidates and CC1 for 6 held-out stable candidates.
CC2 and CC3 are not supported (0 qualified candidates each). An independent full audit passed, and
reproductions with `PYTHONHASHSEED=1` and `PYTHONHASHSEED=37` matched all eight artifact bytes.
This is limited to unlabeled recurring structure and next-channel MSE in fixed synthetic streams;
it does not establish human semantic understanding, an organ, biological equivalence, or energy
efficiency. C06/C08 negative findings, claim grades, package version 0.2.1, persisted schema 0.2,
release manifests, and release metadata remain unchanged.
## v0.3 C15 v4 — engineering accepted; scientific support not supported

C15 v4 is accepted at the registered **engineering** boundary under protocol
`c15-revision-objectives-v4`, source `1072a484f36fc8981622ed3de39d796b654698b9`, and
execution-pin head `49b40cee605d48e5f9dca243e2c23de43491c64e`.  It published the exact eight
canonical artifacts with no failed seed. All eight engineering gates pass: the 21,760 retained
prediction rows and 23,040 training-step rows have been independently recalculated; every seed
2951--2955 completed 8/8 primary full/I1/E1/base recovery opportunities without checkpoint
restoration; no-Ignition, objective-ablation, attribution, and citation gates also pass.

Scientific status remains `not_supported`, and is retained rather than relaxed: full and
no-residual recovery rates are both 1.0, so strict residual superiority is false. Weighted-CE
ECE remains undefined in the primary comparison; its null semantics are retained in the
10,000-draw paired bootstrap. The other registered point/interval outputs remain available in
the raw and derived artifacts. This engineering acceptance unblocks the C17 dependency only; it
does not establish semantic understanding, biological fidelity, energy efficiency, or any claim
beyond the registered synthetic engineering evidence.

An independent full audit revalidated exact-eight inventory, canonical serialization,
source/protocol pins, protected 31/31 and immutable v3 transport evidence, pure fixture hashes,
raw-to-derived aggregates, context/assessment boundary, all engineering gates, and all nine
10,000-draw paired bootstraps. `PYTHONHASHSEED=1` and `PYTHONHASHSEED=37` reproductions are
byte-identical for all eight files. C15 v3 negative artifacts and transport, package 0.2.1,
persisted schema 0.2, and release metadata remain unchanged.

## v0.3 C15 v3 — completed evaluation, engineering acceptance blocked

The frozen C15 v3 execution completed all five seeds and published all eight artifacts, but
engineering passed only 7/8 gates and scientific support is `not_supported`. C15 v3 is not
accepted; its result had kept C17 blocked until the separate C15 v4 engineering acceptance. Valid
negative evidence is not a waiver of an unmet engineering gate. R-V03-0008 records the full
result without changing thresholds.

Primary full/I1/E1/base test recovery was 0/8, 0/8, 8/8, 0/8, and 0/8 for seeds 2901--2905.
Only seed 2903 showed the required continuous A-to-B-to-A recovery without checkpoint restoration.
Full and no-residual recovery rates were both 0.2; full ECE exceeded weighted CE by 0.4053612360,
failing the registered 0.03 noninferiority margin. These are retained failures, not missing seeds.
Independent raw-to-derived validation, including all nine 10,000-draw bootstraps, passed;
independent execution with `PYTHONHASHSEED=37` reproduced all eight files byte-for-byte from the
`PYTHONHASHSEED=1` original.

Scientific source remains `eedb8b426f326c5dcb70bd548008695eb1652aee` at execution tree
`6860c2ec4133a9debefdec0b92e33ab0e09b430f`. D-V03-0025 records a separate four-line synthetic
test-fixture correction after that tree's CI failure. The integration tree is deliberately
rejected by the unchanged official-runner post-pin guard; it is not a replacement execution pin.
No package/schema, claim grade, C06/C08 result, or accepted C11--C14 evidence changes.
The 17,301,391-byte deterministic evidence-transport ZIP is stored outside the canonical artifact
directory at `artifacts/v03/c15_revision_transport/`; it is neither a ninth canonical artifact nor
a release. Its index binds the exact-eight hashes, execution/source commits, and negative status.

## v0.3 C15 v2 — historical failed execution, superseded by v3

C15 v2 source `bb89797` passed focused and full source verification, but its official run
failed during bootstrap aggregation on an undefined metric and exceeded an unenforced
120-second protocol timeout. No final artifact bundle or scientific support decision was
published. R-V03-0007 retains this implementation/protocol failure. A corrected preregistration
and fresh unused seeds were required before another official execution; at that time C14 was the
latest accepted stage.

## v0.3 C14 — attributable Coalition-driven Ignition

C14 is accepted under preregistered protocol `c14-coalition-gate-v1`, using accepted C13
merge `06e13975b486548bb17924acc3b82786246ad6e1` and final source commit
`eb7f542963397eba1b7d9b4a66a7873b3ba17ac4`. The isolated `v03_seed` call path now evaluates
an attributable bounded Coalition before belief mutation while preserving the legacy gate as
the default and leaving the v0.2 learned backend unchanged.

Across seeds 2701--2705, all 12 frozen G03 engineering gates passed with no failed seed. The
run retained 360 raw rows, 15 causal-removal rows, 24 aggregate metrics, 120 seed rows, four
paired statistics, and 50 machine-resolvable reason references. Independent support Ignition,
removal reversal, and exact restoration were 1.0; same-ID and correlated-group inflation were
0; contradiction reduced the score by 0.1296997075145081; and G1 differed from both frozen
probability controls on 90% of paired primary cases. All six artifacts reproduced byte-for-byte
under a different `PYTHONHASHSEED`, and their derived results were recalculated from raw rows.

This accepts only attributable synthetic Coalition control at fixed logits. It does not show
external accuracy gain, learned Coalition formation, semantic understanding, biological
fidelity, or energy efficiency. C06/C08 negative findings, scientific claim grades, protected
hashes, package 0.2.1, persisted schema 0.2, and release metadata remain unchanged.

## v0.3 C13 — evidence ledger and oracle entity-scope diagnosis

C13 is locally accepted under preregistered protocol `c13-evidence-entity-v1`, using accepted
C12 merge `280516fb` and source commit `03b2659`. The isolated `v03_seed` path now has strict
canonical `EvidenceRecord`, `EntityBinding`, and `EvidenceAuditRow` contracts; deterministic
evidence/binding identities; correlation-aware immutable evidence; append-only deactivate and
restore; transitive effective-active lineage; complete Spark-to-sample resolution; semantic
audit replay; fixed G0 probability decisions; and condition-separated E0/E1 execution. E2
learned slots remain an interface only and have zero execution rows.

Across seeds 2601--2605, all G02/G05 engineering gates passed. E1 oracle-entity cross-talk and
misassignment were 0, oracle coverage was 1.0, and E0-minus-E1 cross-talk was 1.0 with the frozen
paired-bootstrap interval [1.0, 1.0]. This supports only the preregistered relation-free synthetic
diagnosis that explicit oracle entity scope removes the constructed global-scope cross-talk. It
does not demonstrate autonomous entity discovery, learned binding, semantic understanding,
biological fidelity, or external generalization. The audit chain is semantically replayed but is
not an externally anchored signature. C06/C08 negative findings, scientific claim grades,
protected hashes, package 0.2.1, schema 0.2, and release metadata remain unchanged.
The canonical metrics artifact retains all 1,440 condition-separated execution rows, and the
invariant artifact retains the before/after observations needed to recalculate G02/G05 rather
than relying on acceptance booleans alone.

## v0.3 C12 — computational sensory gate

C12 is locally accepted under preregistered protocol `c12-sensory-field-v1` after the accepted
C11 dependency merge `5bf5050`. The isolated `v03_seed` path now has versioned continuous
`SensorySample` / `PerceptualSpark` contracts, an adaptive multi-channel sensory gate, bounded
channel-local goal modulation, explicit omission, complete accepted/suppressed salience trace,
term ablations, current-input bypass, atomic failure, canonical state serialization, exact replay,
and state-neutral inspection. Habituation, unexpected change/omission, goal-target,
distractor/noise, and stimulus-specificity worlds execute locally on CPU.

Across primary seeds 2601--2605, predictable repetition reduced emitted Sparks and downstream
active work by 100%, change/explicit-omission recall was 100%, bounded-goal recall delta was
+1.0, irrelevant false-activation increase was 0 percentage points, and stimulus-specificity
recall was 100%. The frozen G04 gates passed. Every channel is still inspected and scored, so
this is not evidence of reduced dense total work or energy efficiency. It is a computational
sensory-gate result, not biological sensory reproduction or semantic understanding. C06/C08
negative findings, scientific claim grades, protected hashes, package 0.2.1, persisted schema
0.2, and release metadata remain unchanged. C12 stops at this boundary; later tasks require
their own accepted dependency and preregistration.

## v0.3 C11 — baseline freeze and input-bottleneck diagnosis

The accepted v0.2.1 baseline is frozen at Git commit `f692c98`, release source revision
`6aef091`, package `0.2.1`, and persisted schema `0.2`. Protocol
`c11-input-bottleneck-v2` supersedes the one-seed v1 engineering run for acceptance. It preserves
the frozen pairs, tracks, threshold, and diagnosis rule while executing seeds 1729–1733 and
reporting paired diagnostic-pair bootstrap intervals. C11 engineering is complete and the
synthetic diagnosis implicates the input path: I2 Oracle accuracy was 1.0 versus 0.5 for I0, with
an Oracle-gap effect of 0.5 and 95% pair-block interval [0.166667, 0.833333]. I1 retained local
surface structure but did not improve frozen downstream accuracy over I0 and failed the
high-overlap negation case. This is not evidence of semantic understanding or cognitive-core
validity. C11 v2 was reviewed and accepted in merge `5bf5050`, satisfying the C12 dependency.
Existing C06/C08 negative results, claim grades, package/schema, and release metadata are
unchanged.

Status date: 2026-08-27

## 1. Current maturity

The repository is a **Phase-0 local functional research prototype**. It demonstrates an inspectable event-driven state machine with persistent competing hypotheses, evidence provenance, Coalition scoring, ignition, Workspace broadcast, residual loser retention, and a minimal reward-modulated plasticity hook.

v0.2.1 fixes the core destination to one general-purpose local computer, adds a plain-language foundation guide and expanded glossary, and moves dedicated neuromorphic hardware to an independent extension track.

It now includes an optional controlled-synthetic learned-routing backend and a matched-baseline
harness. The reduced C05 run did not achieve scientific compute or dev quality matching and is
not evidence of a general comparison advantage. It is not a validated biological model. C07
adds only a reduced hybrid canonical comparison. C06 completed one frozen offline official
Belief-R run, but Spark BREU was below direct and chance; this is a retained negative result,
not external-generalization evidence.

## 2. Local execution contract

The core system must:

- run its reference behavior on CPU;
- require no cloud service or remote model API at runtime;
- keep config, trace, checkpoint, results, and reports on local storage;
- provide a static or localhost-only UI;
- remain runnable offline after dependencies are installed.

Local GPU and local SNN simulation are optional. Dedicated hardware is not a core exit criterion.

See `docs/LOCAL_EXECUTION_POLICY.md`.

## 3. Completed and runnable

| Deliverable | State | Evidence |
|---|---|---|
| Project charter | complete v0.2.1 | `docs/PROJECT_CHARTER.md` |
| Theory specification | working v0.2.1 | `docs/THEORY_SPEC_v0.2.1.md` |
| Beginner foundation guide | complete | `docs/FOUNDATIONS_FOR_BEGINNERS.md` |
| Plain-language glossary | expanded | `docs/GLOSSARY.md` |
| Local execution policy | complete | `docs/LOCAL_EXECUTION_POLICY.md` |
| Prior-art gap analysis | bounded adversarial second pass complete; monitoring remains continuous | `docs/PRIOR_ART_GAP_ANALYSIS.md`, `docs/research/` |
| Deterministic reference engine | runnable | `src/sparkbrain/engine.py` |
| Spark/Event/Coalition/Workspace model | runnable | `src/sparkbrain/model.py` |
| Canonical and randomized SwitchWorld | runnable | `src/sparkbrain/worlds.py` |
| Phase-0 scalar baselines and ablations | runnable; legacy imports preserved | `src/sparkbrain/baselines/`, `benchmark.py` |
| C05 matched baseline harness | implemented; reduced quality match negative | `src/sparkbrain/baselines/neural/`, `evaluation/run_baselines.py`, `artifacts/phase2/baselines/` |
| C02 controlled worlds and statistical suite | implemented with negative results | `src/sparkbrain/tasks/`, `evaluation/`, `artifacts/phase1/c02-main-1000/` |
| C04 learned sparse-rate backend | implemented with held-out synthetic result and collapse diagnostics | `src/sparkbrain/learned/`, `artifacts/phase2/`, `docs/C04_LEARNED_ROUTING_RESULTS.md` |
| C08 bounded structural plasticity | implemented with valid negative specialization result | `src/sparkbrain/structural/`, `artifacts/phase3/`, `docs/C08_STRUCTURAL_PLASTICITY_RESULTS.md` |
| C06 external validation | full pinned Belief-R zero-shot run completed with negative result | `artifacts/external_validation/c06-final-official/`, `docs/C06_EXTERNAL_VALIDATION_RESULTS.md` |
| Metrics for stability/revision/recovery | runnable | `src/sparkbrain/metrics.py` |
| Static replay visualizer | runnable locally | `artifacts/demo/visualizer.html` |
| Unit tests | integrated suite passing with learned/spiking extras available | `python -m pytest -q`; dated counts in `docs/RESULTS_LEDGER.md` |
| Local readiness audit | runnable | `scripts/local_readiness_check.py` |
| Generated Phase-0 report | complete with limitations | `artifacts/benchmarks/benchmark_report.md` |
| Codex repository instructions | complete | `AGENTS.md`, `.agents/skills/sparkbrain-research/SKILL.md` |
| Versioned checkpoint and trace replay | C01 accepted | `serialization.py`, `replay.py`, `schemas/`, `tests/test_schemas.py`, CI run `32594805438` |
| Interactive localhost Brain Lab | C03 accepted locally | `src/sparkbrain/lab/`, `docs/BRAIN_LAB.md`, `tests/test_brain_lab_*.py` |
| Reduced local spiking backend | hybrid canonical equivalence; fully spiking work remains | `src/sparkbrain/spiking.py`, `artifacts/spiking/` |
| Detailed Codex execution queue | complete | `docs/CODEX_EXECUTION_BRIEF.md`, `docs/codex/` |

## 4. Verified local commands

```bash
python scripts/local_readiness_check.py
python -m pytest -q
python scripts/run_demo.py
python scripts/checkpoint_demo.py
python scripts/replay_trace.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

The persisted config/state/trace schema remains `0.2`; package and documentation version is `0.2.1`.

## 5. Current Phase-0 observation

On the bundled 40×30 SwitchWorld run, the full SparkBrain configuration reached approximately:

- all-step accuracy: 0.640
- coverage: 0.937
- revision recall: 0.666
- revision precision: 0.614
- mean switch latency: 1.352 events
- recovery rate: 0.644

The accumulator baseline is close in this hand-authored setting. Therefore this result does **not** support a general performance advantage. The valid observation is narrower: residual removal materially harms the current scenario, while single-Spark ignition changes the revision/precision trade-off. These are hypothesis-generating results, not decisive evidence.

## 6. Major uncompleted work

| Priority | Missing capability | Codex task |
|---:|---|---|
| P1 | full-scale matched-baseline scientific run; reduced harness is complete | C05 follow-on |
| P2 | semantic language-encoder and citation-capable attribution follow-on; frozen external adapter run is complete | C06 follow-on |
| P2 | fully spiking and multi-world equivalence beyond the reduced hybrid | C07 follow-on |
| P2 | additional structural-plasticity hypotheses after negative causal result | C08 follow-on |
| continuous | systematic prior-art review and novelty audit | C09 |
| owner action | select a project license before any public archive/tag | C10 public gate |

### C10 release-candidate preparation

The non-license C10 package now pins the tested local environment, freezes a bounded primary
smoke subset, regenerates its table/SVG/report/negative appendix/SBOM deterministically, maps
claims to exact run/artifact evidence, and emits an offline machine run manifest. Repository
mode retains tracked-file and Git-ancestry checks. Standalone archive mode uses fixed release
metadata and manifest hashes, invokes no Git command, and fails closed for content, revision,
metadata, provenance, and tree tampering. The documented plain readiness, reproduction,
preparation validation, and pytest commands pass after extraction without `.git` or manually
supplied cache-control environment variables. Pristine integrity validation precedes the runtime
pytest phase. The private review bundle has its own exact-content manifest and ZIP SHA-256 rather
than treating `PACKAGE_MANIFEST.json` as an implicit exception list.

This is non-license release preparation, not public readiness. C05 checkpoint-matched encoder
evidence, the final C06 negative external run, and the C08 negative specialization result remain
integrated as negative evidence. CL-007 and CL-008 remain E0. Public validation remains blocked
only by the owner license decision after the non-owner integrity, preparation, and evidence
classes pass. The smoke subset is explicitly not the full evaluation.

## 7. Exit criteria for the core final system

The project reaches its stated core destination only when all are true:

1. Spark, interaction, Coalition, ignition, memory, learning, organ, and global state are formally versioned.
2. Every primary theoretical claim maps to code, tests, and an experiment.
3. The system runs continuously in at least three nontrivial worlds on one local machine.
4. A user can observe and causally intervene on Spark and connection state through a local visual interface.
5. Learned routing generalizes to held-out combinations.
6. Comparisons include matched modern neural and probabilistic baselines.
7. Belief maintenance, justified revision, no-ignition, and loser recovery are separately measured.
8. A local spiking backend reproduces predefined behavioral invariants or documents where equivalence fails.
9. Raw results, seeds, configs, code, and local commands reproduce reported figures.
10. CPU reference execution remains available without a remote API or cloud service.
11. Core UI and storage remain local/offline-capable.
12. Claims remain limited to evidence; biological and hardware-energy claims require separate validation.

Dedicated hardware execution is not required by these criteria.

## 8. Immediate execution order

```text
C01 ─┬─> C02 ─┬─> C04 ─┬─> C06 ─> C10
     │         └─> C05 ┘
     └─> C03

C04 ─> C07
C04 ─> C08
C09 runs continuously and must review C10 claims.
```

C01 is accepted: schema `0.2`, deterministic fresh-run replay, checkpoint continuation, pure inspection, bounded event failure, and counter contracts are covered locally and by the Python 3.11/3.13 CI matrix. C03 is locally accepted: loopback control, deterministic pause/step/reset, event injection, immutable-parent intervention forks, synchronized comparison, blind-safe export/import, bundled offline UI, API/E2E/accessibility contracts, and relevant-subset performance are covered.

C02 is locally implemented. The frozen main run completed 37 declared conditions with
1,000 episodes each and generated raw rows, bootstrap intervals, Pareto output, and three
deterministically selected failure visualizations. This is an E2 controlled synthetic result,
not external validation. MultiObjectWorld produced no full-system ignition under the frozen
configuration and is retained as a negative result; C04/C05 must not tune against its test
seeds. C04 and C05 must share this frozen data harness and its split manifests.

C04 is locally implemented on the immutable C02 manifests. Its 60-episode held-out CPU profile
beat chance and the training-majority baseline while retaining calibrated no-ignition and
non-hand-authored recovery cases. The router nevertheless exhibited dead/overloaded modules,
and the reduced smoke profile was below chance. These negative findings remain explicit.

C05 is locally implemented as a shared observation-only pipeline for accumulator,
privileged Bayes, train-only Laplace HMM, GRU, LSTM, causal Transformer, RIM-like modular
recurrence, explicit-state memory, oracle, and chance. The reduced five-seed acceptance
profile matched architecture-body parameter counts and retained paired raw outputs, but
scientific compute matching was false and no learned family met the accumulator
accuracy/coverage quality target at every seed after ten optimizer steps. CL-007 therefore
remains E0. The full frozen 1,000-episode-per-world run and a completed 12-trial search were
not executed by this integration profile.

C08 is locally implemented over the frozen C04 checkpoint and C02 manifests. Fixed-capacity
module/edge masks, deterministic boundary events, identity/lineage/tombstone tracking,
homeostasis, budgets, checkpoint continuation, actual selected-edge counters, paired causal
controls, and sensitivity artifacts are covered. The two-seed candidate passed multiplicity
only; decisiveness, fertility, and specificity failed. CL-008 remains E0 and no emergent-organ
claim is permitted.
C06 is locally implemented through a frozen adapter manifest that verifies the C04/C05
checkpoint, configuration, profile, encoder vocabulary, and input dimension. The
network-blocked official run evaluated all 1,744 Belief-R pairs without test fitting or
tuning. Spark BU/BM/BREU were 0.0391/0.0896/0.0643, below direct and chance BREU 0.25. The C05
external feature path maps unseen categorical tokens to UNK, parameter/compute matching is
false, and evidence attribution is unavailable. Gate P3 and CL-007 therefore remain unmet.
