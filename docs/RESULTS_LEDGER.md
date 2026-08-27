# Results and Negative-Result Ledger

Append entries; do not rewrite prior outcomes to match later interpretations.

## 2026-08-28 — R-V03-0011 — C18 trace/checkpoint/Brain Lab contract smoke artifact

- Protocol/source: `c18-trace-checkpoint-brain-lab-v1`; source
  `f569cd3a1772e5c3240392e720825314f30e0bf3`; pin
  `5806d1758cc6bcbe521b216338b58283b137038d`.
- Status: engineering `accepted`; scientific `not_supported`.
- Evidence: the official and `PYTHONHASHSEED=1` reproduction have equal SHA-256
  values for all six exact files. Both replay the primary checkpoint to state
  hash `d779e559be9ac576bfe5ec1206780c27342c4ebfdc7c3b15ee11257caa3c5175`.
- Boundary: the export never invents attribution; missing evidence citations
  fail closed, inspection is state-neutral, and a fork retains parent lineage.
  This is no evidence of semantic understanding, organ formation, biological
  fidelity, energy efficiency, or external task performance.

## 2026-08-27 — R-V03-0009 — C15 v4 completed evaluation; engineering accepted

- Protocol/run: `c15-revision-objectives-v4` / `c15-revision-objectives-main-v4`.
- Source/pin: `1072a484f36fc8981622ed3de39d796b654698b9`; execution-pin head
  `49b40cee605d48e5f9dca243e2c23de43491c64e`; model seeds 2951--2955; bootstrap seed 4465.
- Status: engineering `pass` (8/8), scientific `not_supported`, `failed_seeds=[]`. The official
  bundle contains exactly eight artifacts and no failed seed was omitted.
- Retention: 21,760 prediction rows, 23,040 training-step rows, 540 independent objective rows,
  60 condition-seed rows, 170 seed and 34 aggregate confusion/calibration rows, 60 Pareto seed
  points, 12 aggregate points, and 66 pairwise comparisons.
- Engineering: each primary full/I1/E1/base seed 2951--2955 has 8/8 recovery successes without
  checkpoint restoration. The other seven engineering gates also pass, including explicit
  no-Ignition, exact-zero objective ablations, attribution-target coverage, and citation
  resolvability.
- Scientific boundary: `not_supported`. Full and no-residual recovery rates are both 1.0, so the
  registered strict residual-superiority gate is false. The full-minus-weighted-CE ECE effect and
  interval remain null because ECE is undefined; the paired bootstrap preserves 0 defined and
  10,000 undefined resamples rather than dropping or imputing them. Engineering acceptance does
  not convert this scientific result into support.
- Independent evidence: an external standard-library audit passed exact inventory, canonical
  JSON/JSONL, source/protocol pin and four-field amendment, protected 31/31, v3 evidence/transport
  hashes, pure fixture hashes, raw cardinalities, raw-to-confusion/calibration/engineering gates,
  context boundary, and all nine 10,000-draw paired bootstraps. A `PYTHONHASHSEED=37`
  reproduction is byte-identical to `PYTHONHASHSEED=1` for all eight files.
- Disposition: C15 is accepted for its registered engineering dependency, unblocking C17's
  C15-acceptance prerequisite. C15 v3 negative artifacts/transport remain immutable and are not
  superseded. Package 0.2.1, persisted schema 0.2, release manifests, C06/C08 findings, and
  claim grades remain unchanged.

## 2026-08-22 — R0001 — Phase-0 SwitchWorld software validation

**Code/version:** SparkBrain prototype v0.2 bundle  
**Command:** `python scripts/run_benchmark.py --episodes 40 --steps 30`  
**Data:** seeded synthetic SwitchWorld; hand-authored evidence mapping  
**Raw outputs:** `artifacts/benchmarks/benchmark_results.json`  
**Aggregate:** `artifacts/benchmarks/benchmark_aggregate.csv`

### Observations

- full SparkBrain all-step accuracy was 0.6400 and coverage 0.9367;
- accumulator all-step accuracy was 0.6283, so the full system did not clearly dominate this simple baseline;
- removing residual state reduced accuracy to 0.4567 and coverage to 0.8183 in this distribution;
- single-Spark ignition improved revision precision relative to full SparkBrain but worsened latency and recovery in some measures;
- instant classification revised rapidly but produced many unnecessary revisions;
- algorithmic active-Spark counts are not hardware energy measurements.

### Interpretation

This run validates that the software exposes a stability/revision trade-off and that the selected ablations alter it. It does not establish generalization, learning ability, biological fidelity, or modern-model superiority.

### Negative or inconvenient findings retained

- the accumulator baseline is competitive;
- the reference engine's event fan-out can yield more Spark updates than a scalar baseline;
- hand-authored evidence weights may encode much of the task solution;
- some Phase-0 metrics are sensitive to coverage and forced-prediction differences.

### Follow-up

C01 must audit counters and replay; C02 must add controlled distributions and confidence intervals; C04/C05 must replace hand-authored-only comparisons with learned matched systems.

---

## Entry template

```text
## YYYY-MM-DD — R#### — title
Code/version:
Command:
Data/splits:
Seeds:
Raw outputs:
Aggregate:
Hypothesis:
Result:
Negative findings:
Confounds:
Claim grade impact:
Next action:
```

## 2026-08-23 — R0009 — C05 matched-baseline reduced acceptance

**Command:** `python -m sparkbrain.evaluation.run_baselines --config configs/experiments/phase2/baselines_acceptance.json --output artifacts/phase2/baselines/c05-acceptance-final`
**Data/splits:** C02 frozen dev/test manifests; four episodes per world in this reduced run
**Seeds:** learned seeds 101, 211, 307, 401, 503; paired C02 episode seeds
**Raw outputs:** `artifacts/phase2/baselines/c05-acceptance-final/raw_results.json`
**Aggregate:** `artifacts/phase2/baselines/c05-acceptance-final/aggregate_metrics.json`

### Result

- all ten baseline families completed locally in 29.7 seconds on the recorded CPU setup;
- architecture-body parameter counts were within ±2% of the 32,100 target without a
  padding reserve; the common optimizer-work proxy was within ±5%;
- frozen C02 input-file SHA-256 values were identical before and after execution;
- the privileged Bayes diagnostic reached 0.8125 all-step accuracy and oracle 1.0, but
  these are explicitly privileged bounds and not matched competitors.

### Negative findings and confounds

- quality matching against accumulator dev accuracy/coverage was not achieved for every
  learned seed/family after ten optimizer steps;
- learned test accuracy varied widely by seed; the compact Transformer reached as low as
  0.0556 and explicit-state memory showed unstable/high loss in some runs;
- the reduced run executed one configuration per seed, not a completed 12-trial search or
  the full 1,000-episode-per-world frozen matrix;
- family-specific analytical work and CPU profiler results did not establish a scientific
  training-compute match; `scientific_compute_match` is retained as false;
- all timing and operation counts are local compute observations, not energy evidence.

**Claim impact:** CL-007 remains E0. The result validates the harness and records a negative
quality-matching outcome; it does not support general superiority.

---

## 2026-08-23 — R0006 — C02 controlled synthetic suite

**Code/base:** C02 branch from accepted C01 `c5178db`; schema remains `0.2`
**Command:** `python -m sparkbrain.evaluation.run_suite --config configs/experiments/phase1/main.json --output artifacts/phase1/c02-main-1000`
**Data/splits:** frozen local test seeds 200000–200999; 37 declared conditions; 1,000 episodes per condition
**Raw outputs:** `artifacts/phase1/c02-main-1000/raw/` (local, reproducible, approximately 492 MiB)
**Aggregate:** `artifacts/phase1/c02-main-1000/aggregate/metrics.json`

### Result

- SwitchWorld full accuracy was 0.5965, coverage 0.9234, revision recall 0.6839,
  revision precision 0.6761, and mean switch latency 1.6196.
- Removing residual state reduced SwitchWorld accuracy to 0.4180 and delayed-evidence
  accuracy from 0.7035 to 0.4573 in these frozen synthetic distributions.
- Hard-WTA reduced SwitchWorld recovery from 0.7240 to 0.5636 and delayed-evidence recovery
  from 0.9284 to 0.8136.
- GoalConflictWorld changed actions while the measured goal-only belief-flip rate remained
  zero. This is a narrow implementation observation, not a cognitive claim.

### Negative findings and confounds

- MultiObjectWorld full-system coverage and all-step accuracy were both zero: the frozen
  configuration did not ignite object-scoped beliefs. The failure is retained.
- Duplicate evidence produced a non-zero paired score change on average; evidence-record
  identity deduplication does not guarantee activation-level invariance.
- The supplementary frozen reliability run reported source-reliability sensitivity of
  0.0175 for the full condition; this small descriptive difference is not a calibrated
  reliability claim.
- Coalition softmax values were used only for descriptive Brier/ECE; they are not calibrated
  probabilities.
- The generators and evidence weights remain hand-authored, and no learned or modern matched
  baseline is present. No general superiority claim is supported.
- Main bootstrap intervals are descriptive. No p-value family or significance-ranking claim
  was made.

**Claim impact:** CL-003 and CL-006 remain E2; CL-007 remains E0.
**Next action:** C04/C05 consume the immutable Episode/split contracts without tuning on C02
test seeds. Multi-object ignition requires dev-only diagnosis before a new frozen evaluation.

---

## 2026-08-22 — R0002 — v0.2.1 local-scope and documentation expansion

**Code/version:** SparkBrain package v0.2.1; persisted schema v0.2  
**Nature:** documentation, local-execution contract, validation guard; no intended dynamics change  
**Primary commands:** `python scripts/local_readiness_check.py`, `python -m pytest -q`, `python scripts/validate_bundle.py`

### Changes under test

- core completion constrained to one general-purpose local computer;
- CPU reference path made mandatory;
- remote runtime services excluded from core dependencies;
- dedicated hardware moved to Extension H;
- beginner foundation guide and expanded glossary added;
- local-readiness checks added;
- package version advanced to 0.2.1 while schema remains 0.2.

### Scientific result

None claimed. This patch does not increase the evidence grade of H1–H10 or establish a performance improvement.

### Validation outcome

- local readiness: PASS on Python 3.13.5 / Linux x86_64;
- tests: 30 passing;
- canonical demo: CAT → TOY → CAT reproduced;
- checkpoint state hash: `cedc8543d87677d2cbf1707f0df2ec7d95e8a1d31b735a40a917d9de9d7ff13c`;
- bundle validation: 23 required artifacts validated;
- benchmark aggregate CSV: byte-identical to archived v0.2;
- canonical trace JSON: byte-identical to archived v0.2;
- ruff: not executed in the packaging environment because it was not installed.

### Compatibility target

The Phase-0 dynamics and persisted config/state/trace schema are intended to remain compatible with v0.2. The byte-identical benchmark aggregate and canonical trace support that narrow compatibility statement for the bundled scenarios; they do not prove compatibility for every possible checkpoint or graph.

---

## 2026-08-23 — R0003 — C01 deterministic reference and replay contract

**Code/version:** SparkBrain package v0.2.1; persisted schema v0.2
**Nature:** reference-engine hardening and compatibility validation; no intended dynamics change
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/local_readiness_check.py`, `python scripts/validate_bundle.py`

### Changes under test

- deterministic continuation includes the pending event queue, sequence counter, RNG, stability, Workspace, eligibility, counters, trace, and frame-local audit buffers;
- pure `inspect_snapshot()` is separated from backward-compatible recording `snapshot()`;
- generated config, checkpoint, trace, summary, and benchmark JSON are validated against schema `0.2`;
- `broadcast_listeners` is required by both runtime and JSON Schema validation;
- equal-time ordering, event-limit diagnostics, invalid payloads, evidence identity, contradiction provenance, no-ignition, recovery, cooldown, refractory, homeostasis, Workspace, and plasticity boundaries are covered by focused tests.

### Validation outcome

- local readiness: PASS;
- tests: 55 passing;
- Ruff: PASS;
- fresh canonical state hash: `ba166f0e801665e98c200f8a291fdf475f2dbbc6d86232867e21b1f08226caa5` on two independent runs;
- normalized fresh-run traces: identical;
- generated-artifact schema regression: PASS;
- Phase-0 benchmark aggregate values: unchanged; persisted JSON documents gained explicit schema metadata only.
- GitHub Actions CI: PASS on Python 3.11 and 3.13, run `32594805438`.

### Compatibility and limitations

Schema remains `0.2`; no migration is introduced. The stricter validators reject incomplete payloads that omitted required deterministic state, including `broadcast_listeners`. This is validation hardening rather than reinterpretation of valid v0.2 artifacts. The clean CI matrix passed on the two repository-supported Python versions; this does not establish compatibility with untested environments.

---

## 2026-08-23 — R0004 — C03 localhost Brain Lab acceptance

**Code/version:** SparkBrain package v0.2.1; persisted engine schema v0.2; Brain Lab schema v1
**Nature:** optional local UI/control plane; no intended core dynamics change
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/measure_brain_lab.py`, `python scripts/run_brain_lab.py`

### Changes under test

- loopback-only FastAPI control plane and bundled no-CDN frontend;
- nine UI regions for graph, timeline, belief, Workspace, inspection, control, intervention, comparison, and export/import;
- deterministic pause, single-step, run, reset, and validated event injection;
- parent-preserving checkpoint fork with edge, Spark, organ, and threshold interventions;
- frame-index synchronized comparison, blind-safe API/export, and local bundle import;
- static visualizer fallback and pure-inspection non-interference.

### Validation outcome

- tests: 68 passing, including 13 focused Brain Lab API/service/E2E contract tests;
- Ruff: PASS;
- canonical UI/API flow: CAT → TOY → CAT with evidence provenance;
- 2,000-Spark / 10,000-edge relevant-subset preparation: 0.9654 ms for 250 Sparks / 600 edges;
- 60 FPS preparation budget (16.6667 ms): PASS;
- loopback startup and non-loopback rejection: PASS;
- offline bundled assets, keyboard/focus/accessibility contract, blind truth removal, and import/export regression: PASS.

### Limitations retained

- the measured time covers deterministic subset preparation, not browser paint or end-to-end frame time;
- the run registry is in-memory and single-process; exported bundles are required across restarts;
- SSE reports a finite current-frame snapshot and does not create a background simulation queue;
- the native SVG graph is a functional view, not a biological anatomy claim;
- no energy-efficiency claim follows from UI timing.

---

## 2026-08-23 — R0005 — C07 reduced snnTorch hybrid equivalence

**Code/version:** `codex/c07-spiking-backend`; schema `0.2` unchanged
**Command:** `python scripts/run_spiking_comparison.py`
**Data/seed:** fixed seven-event SwitchWorld CAT→TOY→CAT; seed 7
**Raw outputs:** `artifacts/spiking/c07_comparison.json`, `rate_trace.json`, `spike_trace.json`
**Aggregate:** `artifacts/spiking/c07_report.md`

### Result

- all 9 frozen comparison checks passed;
- hybrid predictions exactly matched `[None, cat, cat, cat, toy, toy, cat]`;
- distinct ignition order matched `[cat, toy, cat]`;
- focused tests preserved no-ignition, duplicate evidence, residual recovery, Workspace
  capacity, directional edge ablation, protocol conformance, and state replay.

### Negative findings and confounds

- LIF threshold 1.1 produced no sensory spikes and no predictions;
- equivalence is parameter-sensitive and covers one hand-authored scenario;
- only sensory encoding is spiking; Coalition and Workspace remain algorithmic/rate;
- local wall-clock is not an energy measurement;
- no fully spiking, learned, surrogate-gradient, or local-plasticity comparison was done.

### Claim impact

CL-009 advances only to E1 for this reduced hybrid canonical fixture. It does not establish
general spiking equivalence, biological fidelity, efficiency, or multi-world robustness.

---

## 2026-08-23 — R0007 — C03 import boundary and C07 queue-order correction

**Nature:** acceptance and safety correction; no scientific claim increase
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/run_spiking_comparison.py`, `python scripts/validate_bundle.py`

### Corrected contracts

- Brain Lab import enforces a 25 MiB serialized limit and strict agreement among metadata, checkpoint, trace, figure data, and event manifest before creating a run;
- blind imports reject visible truth and export paths remain confined to the artifact root;
- hybrid LIF state advances when events leave the deterministic queue, preserving time, priority, and sequence order instead of caller scheduling order;
- pending LIF events remain checkpointable across an event-limit interruption;
- CI installs the optional spiking dependencies before executing the full test suite.

### Validation outcome

- focused Brain Lab/C07 tests: 25 passing;
- full tests: 113 passing;
- Ruff, local readiness, dependency check, and 55-file bundle validation: PASS;
- C07 frozen comparison: 9/9 checks remain PASS;
- trace schema, reset, internal generated events, reverse scheduling, equal-time ordering, checkpoint continuation, oversize import, malformed import, blind behavior, parent preservation, and artifact-root confinement are covered.

### Claim impact

None. The correction removes causal-order and import-validation defects without expanding the single-scenario hybrid evidence boundary recorded in R0005.

---

## 2026-08-23 — R0008 — C04 learned sparse routing on controlled held-out worlds

**Nature:** controlled synthetic learned-backend result with explicit negative diagnostics  
**Run:** `artifacts/phase2/learned-routing-v1/main`  
**Config:** `configs/experiments/phase2/main.json`

### Outcome

- 60 frozen test episodes / 2,160 steps completed on local CPU in 45.433 seconds;
- all-step accuracy 0.66343 exceeded chance 0.33333 and the training-majority non-learning baseline 0.33981;
- coverage was 0.77963, covered accuracy 0.85095, no-ignition count 476, and loser-recovery count 84;
- actual indexed recurrent work selected 8,640 module updates and evaluated 34,560 edges/messages from 25,920 conceptual candidates, while 4,320 dense encoder/router operations remained separately counted;
- all 11 required ablations and five sensitivity rows were emitted after development-only ignition calibration.

### Boundaries and negative findings

- the reduced smoke profile was below chance;
- the main router retained three dead modules, four overloaded modules, and normalized load entropy 0.6698;
- natural unseen evidence bigrams in the primary subset were zero, so compound/distractor stress tests remain separately labeled derived evaluations;
- only 60 of the frozen 1,000 C02 test seeds were evaluated, the encoder/router remain dense, and the random-router condition was not retrained;
- this result supports only controlled-synthetic learned no-ignition and routing behavior. It does not support CL-007, Transformer superiority, external generalization, biological fidelity, or energy claims.

### Verification

The integrated tree passed 134 tests, Ruff, local readiness, and bundle validation. C02 dev/test manifest SHA-256 values remained unchanged before and after the experiment.

---

## 2026-08-23 — R0010 — C08 bounded structural plasticity negative specialization result

**Nature:** mechanism acceptance with a preregistered negative scientific result  
**Run:** `artifacts/phase3/structural-plasticity-v1/main`  
**Config:** `configs/experiments/phase3/main.json`

### Outcome

- the fixed-capacity masked graph, bounded structural events, logical identities, lineage,
  tombstones, budgets, credit/homeostasis state, RNG, optimizer, and checkpoint continuation
  were implemented and serialized;
- the two-seed candidate pair `(9, 14)` passed multiplicity, with matching root-lineage and
  development functional-effect signatures;
- decisiveness failed at 0.0000 versus 0.05, fertility failed at 0.00893 versus 0.01, and
  specificity failed closed because development intervention could not fix a unique positive
  target;
- targeted, random, and degree-matched ablations all produced zero impairment, and the
  activation intervention effect was zero.

### Boundaries and claim impact

The primary graph was fragmented, only two controlled-synthetic seeds were evaluated, the
initial ring graph remains a confound, and there is no external reproduction. CL-008 remains
E0. The only permitted conclusion is that bounded structural plasticity was implemented and
the causal specialization criteria failed; no emergent-organ claim is permitted.

### Verification

The integrated tree passed 175 tests and Ruff. Frozen C04/C02 input hashes remained unchanged,
and selected-edge work, controls, sensitivity, Gate decisions, and negative findings are
retained in the run artifacts.

---

## 2026-08-23 — R0011 — C10 non-license reproducibility package

**Code/base:** C10 branch from integrated `be9cf70`; package `0.2.1`, schema `0.2`  
**Command:** `python scripts/reproduce_release.py --offline --output <LOCAL_OUTPUT>`  
**Inputs:** four committed Phase-0/C02/C04/C07 aggregate or comparison artifacts selected in
`artifacts/release/primary_subset.json`  
**Outputs:** generated primary Markdown table, SVG, and machine-readable clean-room run manifest

### Validation outcome

- the bounded primary table and SVG reproduced byte-for-byte from frozen input hashes;
- table SHA-256: `085f2a5f65d6e5069e3221042158eefdd4045f22c7b55c1b4c5644c95ed97765`;
- SVG SHA-256: `718b3f1ca2a668b61ea3e29401d686a6dbda82f9afd8c5eedae714f996a709ae`;
- 157 tests, Ruff, local readiness, 23-source/11-target prior-art validation, and 76-file
  bundle validation passed on Windows/Python 3.13.3 CPU;
- no network operation was used by the reproduction command after setup.

### Negative findings and blockers

- the primary subset is a smoke check, not the full C02-C08 evaluation;
- C05 checkpoint evidence lacks an integrated checkpoint-matched, hashed dev-only encoder
  vocabulary/feature manifest;
- final C06 model execution and C08 structural-plasticity evidence are not integrated;
- `LICENSE_NOT_SELECTED.md` remains, so no public archive, tag, or ready claim was produced;
- the tested lock is a Windows/Python 3.13 snapshot, not a universal cross-platform wheel lock.

**Claim impact:** no evidence grade increases. This is reproducibility engineering for selected
existing evidence. CL-011 remains E1 pending an independent clean-room reproduction.

---

## 2026-08-23 — R0012 — C06 official external zero-shot evaluation

**Code/base:** C06 final from integration `68fe8fb`; schema remains `0.2`
**Command:** `python scripts/run_external_validation.py`
**Data/splits:** pinned official Belief-R test only; Track B template-group train/dev/test
**Seeds:** C04 seed 41; first preregistered C05 seed 101; Track B split seed 1729
**Raw outputs:** `artifacts/external_validation/c06-final-official/belief_r_predictions.jsonl`
**Aggregate:** `artifacts/external_validation/c06-final-official/belief_r_metrics.json`

### Result

- the network-blocked runner completed all 1,744 official pairs without fitting, tuning,
  selecting, or splitting on Belief-R;
- Spark reached BU-Acc 0.0391, BM-Acc 0.0896, BREU 0.0643, and final coverage 0.2271;
- direct and uniform-chance conditions both reached BREU 0.25; the explicit-state condition
  abstained on every original Belief-R step; oracle reached 1.0 as a privileged upper bound;
- Track B disjoint group test, all six Track C transforms, categorized errors, calibration,
  and remove/duplicate/irrelevant intervention deltas completed.

### Negative findings and confounds

- Spark BREU was below both direct and chance; Gate P3's improvement criterion was not met;
- Spark predictions changed for 18.98% of same-ID duplicates and 21.90% of irrelevant
  distractors, indicating substantial non-causal sensitivity;
- the C05 dev-fitted encoder mapped unseen external categorical tokens to UNK, while C04
  hashed raw text; effective features, tokenization, parameters, and compute were not matched;
- C05's earlier quality/scientific-compute matching failures remain unresolved;
- checkpoint paths do not cite input evidence IDs, so attribution fidelity is N/A rather than
  zero; no language-encoder-only semantic ablation was available;
- exact overlap checking is string-level only and cannot rule out semantic or pretraining
  exposure.

**Claim impact:** CL-007 remains E0. This run establishes an offline external adapter and a
negative result, not external generalization or superiority.

---

## 2026-08-23 — R0013 — C01-C10 integrated non-license release candidate

**Code/base:** integrated `codex/c01-c10-integration`; package `0.2.1`, schema `0.2`  
**Primary validation:** `python -m pytest -q`, `python -m ruff check .`,
`python scripts/validate_release.py --preparation-only`  
**Offline reproduction:** `python scripts/reproduce_release.py --offline --output <LOCAL_OUTPUT>`

### Validation outcome

- 197 tests, Ruff, local readiness, the 23-source/11-target prior-art audit, and 88-file
  bundle validation passed on Windows/Python 3.13.3 CPU;
- the bounded primary Markdown table and SVG reproduced byte-for-byte with no network
  operations after setup;
- the release evidence map contains no pending C01-C10 entry and connects the C05 encoder
  manifest, C06 external artifacts, and C08 negative structural artifacts;
- tracked-file completeness, Windows absolute-path rejection, evidence/provenance ancestry,
  and project-license/SBOM consistency are fail-closed release gates.

### Boundary and blocker

- C05, C06, and C08 results remain negative and do not raise CL-007 or CL-008;
- the fixed primary smoke subset was not expanded after seeing C05/C06/C08 results;
- the owner has not selected a project license, so public validation remains blocked and no
  public archive or tag is produced.

**Claim impact:** no evidence grade increase. C01-C10 implementation and non-license release
preparation are integrated; public release readiness is not claimed.

---

## 2026-08-24 — R0014 — C10 standalone archive and private review correction

**Code/base:** C10 corrective branch from integrated `5495648`; package `0.2.1`, schema `0.2`

**Repository validation:** `python scripts/validate_release.py --preparation-only`

**Archive validation:** extracted package without `.git`; local readiness, offline reproduction
to an empty path outside the archive root, release preparation validation, and the full packaged
test suite

**Private review command:**
`python scripts/build_review_bundle.py --output <REVIEW_ZIP> --source-date-epoch <UTC_EPOCH>`

### Correction and validation outcome

- repository mode retains tracked-file completeness and Git-ancestry validation;
- archive mode uses fixed release metadata, exact cross-file revision agreement, and packaged
  file hashes without invoking Git;
- offline reproduction completes atomically from a no-`.git` extraction and retains the frozen
  primary table SHA-256 `085f2a5f65d6e5069e3221042158eefdd4045f22c7b55c1b4c5644c95ed97765`;
- the frozen SVG SHA-256 remains
  `718b3f1ca2a668b61ea3e29401d686a6dbda82f9afd8c5eedae714f996a709ae`;
- the private review ZIP now has a dedicated exact-content manifest and adjacent ZIP SHA-256;
  Unicode names, duplicate entries, traversal, symlinks, CRC failure, and content tampering are
  covered by focused tests;
- public validation remains blocked only by the owner project-license decision. No license was
  selected and no public archive or tag was produced.

### Scientific boundary

The primary subset remains a smoke check rather than a full evaluation. C06 remains a negative
external result: Spark BREU is `0.0643`, the language-encoder-only ablation is unavailable, and
attribution is N/A. C08 decisiveness, fertility, and specificity remain failed. CL-007 and CL-008
remain E0. No scientific artifact, negative result, or evidence grade is changed by this packaging
correction.

---

## 2026-08-25 — R0015 — C10 final fail-closed integrity correction

**Code/base:** final integrity branch from merged corrective `87aa538`; package `0.2.1`, schema
`0.2`

**Repository commands:** `python -m ruff check .`, `python -m pytest -q`,
`python scripts/local_readiness_check.py`, `python scripts/validate_bundle.py`,
`python scripts/validate_prior_art_audit.py`, and
`python scripts/validate_release.py --preparation-only`

**Archive contract:** fresh no-`.git` extraction; plain local readiness, offline reproduction,
preparation validation, and pytest commands without manually supplied cache-control variables

### Integrity correction and acceptance

- release results separate integrity, preparation, owner, and evidence problem classes;
- preparation-only validation exits nonzero for content, tree, metadata, revision, provenance,
  or generated-evidence tampering; only the owner license blocker may coexist with exit zero;
- reproduction calls the shared non-public integrity preflight before reading the accepted
  revision, rendering, or creating its staging/output directory;
- README byte tamper, bound-file deletion, unexpected file, metadata revision/hash mismatch,
  evidence revision mismatch, and primary-input tamper all fail without traceback or output;
- the repository test suite retains injected rename and staged-hash failures to prove that no
  partial `status: pass` output survives;
- the repository-side outer integration builds a fresh archive and proves the documented plain
  no-Git command sequence; repository-only recursive Git setup is skipped in archive mode;
- the private review builder retains 433 manifest-listed members plus its self-excluded manifest,
  exact-content validation, deterministic timestamp/order/mode, Unicode, CRC, traversal,
  duplicate, symlink, cache, external-data, and tamper checks;
- `tests/test_release.py` freezes the reviewed C06, C08, primary-subset, and claim-register
  SHA-256 values.

### Boundary and blocker

The runtime pytest phase follows pristine archive validation; a second pristine audit uses a new
extraction. Cache files remain forbidden in the shipped tree and are not added to the manifest.
The owner has not selected a license, so no public archive or tag is produced. C06 and C08 remain
negative, CL-007 and CL-008 remain E0, and the primary subset remains explicitly non-full.

**Claim impact:** no scientific evidence grade increase. This is a release-integrity and command
contract correction only.

## 2026-08-26 — R-V03-0001 — Accepted v0.2.1 baseline freeze for C11

- Engineering status: complete
- Scientific status: not evaluated
- Accepted Git baseline: `f692c984d6f3b15d883ced92f11a6f6ad491d4a7`
- Release source revision: `6aef0911dc9e363478c23f98241d80d60ac4fd71`
- Review archive SHA-256: `217771f2b602b32d8161017cd10c9db28206fcf35bd85c9a1ef9f71e88653313`
- Package/schema: `0.2.1` / `0.2`
- Protected C06, C08, primary subset, and claim-register hashes: all matched
- Existing full tests, local readiness, offline reproduction, and release preparation passed
- Release preparation retained the project-license owner blocker and no other problem
- C06 and C08 negative results and existing claim grades remain unchanged

## 2026-08-26 — R-V03-0002 — C11 input-bottleneck diagnosis

- Protocol: `c11-input-bottleneck-v1`, seed 1729, six preregistered synthetic pair families
- Engineering status: complete
- Scientific result: supported for the narrow statement that the input path is implicated
- I0 whole-hash: accuracy 0.5, coverage 1.0, mean similar-pair similarity 0.0
- I1 local-compositional: accuracy 0.5, coverage 1.0, mean similar-pair similarity 0.559798
- I2 symbolic Oracle: accuracy 1.0, coverage 1.0, mean similar-pair similarity 1.0
- Oracle gap over I0: 0.5; Oracle leakage/default-selection audit: pass
- Negative result: I1 did not improve frozen downstream accuracy over I0
- Strongest counterexample: I1 assigned similarity 0.737984 to the high-overlap negation pair
- Interpretation: local surface structure is recoverable, but the current I1 diagnostic does not
  establish meaning, solve rough-input processing, validate the cognitive core, or change C06
- Official Belief-R test: not read, evaluated, or used for tuning
- Final run: `artifacts/v03/c11_runs/c11-input-bottleneck-v1-run-004`
- Independent reproduction: run 005 matched all eight final artifact SHA-256 values exactly with
  a different `PYTHONHASHSEED`; sparse cosine accumulation now uses canonical sorted feature keys
- Runs 001–003 are retained as engineering previews before the executable Oracle audit and the
  cross-Python hash-order regression fix were finalized
- Focused v0.3 tests: 46 passed; Ruff and compileall passed
- Repository collection: 279 tests; full C11 tree result: 274 passed, 5 skipped
- Five frozen-release runtime tests are skipped only in the explicit v0.3 development tree. A new
  replacement test proves the unchanged v0.2.1 manifest remains internally bound and the validator
  fails closed on tracked C11 files. The accepted baseline suite passed before editing; release
  manifests remain unchanged until C20 rather than weakening the integrity validator.
- Local readiness, bundle validation, and prior-art validation passed. The generated v0.2.1
  validation manifest was not retained because C11 must not rewrite release evidence.
- Final artifact hashes:
  - `diagnosis.md`: `5393bc01666cce4a912981dfba61ac51d7bc82dcf96b5668381c9e7a9268638a`
  - `diagnostic_manifest.json`: `e85abecf0b9258a9448227f3720747b0db8aa631fd40a4aabf6d9e23ceda68ea`
  - `failure_examples.jsonl`: `417d1c65764ff2a93ff54fe2a5e55b69dae1805209b5f2c211cda6e176b64075`
  - `frozen_baseline_hashes.json`: `f12406a826b0143c7ccc28f84f6b480a19b6e1e85fa5c7dc0649a1e429458097`
  - `metrics_by_input_track.json`: `ea240709b09fcf59efb26bf5c663553e78cedeba2eee1890c27c45f86ff0c733`
  - `protocol.json`: `4652a53cac9549a8f8aa96091a1d99af79568fa92b0642f98885b328fd311d4f`
  - `raw_features.jsonl`: `3937e5198d5d73bad18a5df07019e6f8f60cb7b764c88703e7120d02bc5ca757`
  - `raw_predictions.jsonl`: `a8a0f6e1e3b9a549d1f786f281220c3585e8b089bb3a08ba0c2c7862359e373a`
- Protected C06/C08/primary/claim hashes: unchanged after C11
- Claim impact: none; `docs/CLAIMS_REGISTER.md` remains byte-identical

---

## 2026-08-26 — R-V03-0003 — C11 five-seed statistical-completeness audit

- Protocol: `c11-input-bottleneck-v2`; seeds 1729, 1730, 1731, 1732, 1733
- Reason: independent acceptance review found that v1 met the C11 task criteria but omitted the
  v0.3 global minimum-five-seed and interval requirements for a primary synthetic comparison
- Frozen from v1: all six pairs, input tracks, features, labels, threshold 0.5, diagnosis rule,
  Oracle policy, downstream evaluator, and the exclusion of official Belief-R data
- Statistical method: 10,000 paired nonparametric bootstrap resamples over diagnostic-pair
  blocks, 95% interval, bootstrap seeds 4311 and 4312
- Seed audit: all five deterministic seeded executions produced identical predictions and
  similarities; this is reported as invariance, not five independent stochastic replications
- I0/I1/I2 accuracy: 0.5 / 0.5 / 1.0; coverage 1.0 for every track and seed
- Oracle accuracy gap over I0: effect 0.5, 95% pair-block interval [0.166667, 0.833333]
- I1 similar-pair retention delta over I0: effect 0.559798, 95% pair-block interval
  [0.355270, 0.734712]
- Negative result retained: I1 did not improve accuracy and still misclassified the
  high-overlap negation pair at similarity 0.737984
- Oracle audit directly refuses evaluator `label`, `test_only`, recursive forbidden and unknown
  fields; ordinary text and default Oracle selection remain refused
- Final run: `artifacts/v03/c11_runs/c11-input-bottleneck-v2-run-003`
- Independent reproduction: run 004 used a different `PYTHONHASHSEED` and matched all eight
  checked-in final artifacts byte-for-byte
- Runs 001–002 are retained as engineering previews before the explicit label/test-only audit
  fields were added
- Focused C11/v0.3 tests: 47 passed; full development tree: 280 collected, 275 passed, 5
  explicit frozen-release skips; Ruff, compileall, local readiness, and prior-art validation passed
- Direct G00 rollback evidence: the clean accepted `f692c98` main worktree contains no v0.3
  namespace and its full 232-test suite passed independently
- Accepted baseline archive SHA-256 was re-read from the original ZIP as
  `217771f2b602b32d8161017cd10c9db28206fcf35bd85c9a1ef9f71e88653313`; the handoff baseline
  verifier passed package 0.2.1, schema 0.2, revision `6aef0911dc9e363478c23f98241d80d60ac4fd71`,
  and all five protected artifacts against the C11 tree
- Correction to R-V03-0002: its statement that run 005 matched all eight checked-in artifacts
  was too strong. Independent review found three semantically equal but differently formatted
  JSON contract files. v2 stores the runner-generated canonical files directly and proves 8/8
  byte identity.
- Final artifact SHA-256:
  - `diagnosis.md`: `c62c8dfdc403ca4f4de9baafed9bf3ef62af6536260444ea067d31d1e843c4f1`
  - `diagnostic_manifest.json`: `2a363f0e18512544103c5f5922ce5957360456f6288e13a5ad2be32664505a15`
  - `failure_examples.jsonl`: `2d7bd37db66e193f5d77400bbebcf603dcef4bd8f3d0a70b37cdc9f585a33e29`
  - `frozen_baseline_hashes.json`: `063465680f8e8e79aa1260b1acbaef44a5405bb012b1671b74cd59050c10bf8b`
  - `metrics_by_input_track.json`: `061791f784788aba78a89c75013c1720b57c2677376aba5d2564525e96ec66b2`
  - `protocol.json`: `b774783ffb1fc7e1a67e2234c9544a1013f003a7cc44d9458dbd8cc5298147d6`
  - `raw_features.jsonl`: `d88bef45dd25d88e8ed8439d004b4e5241a0009fe5f9a9cb7bc5c8952f25227c`
  - `raw_predictions.jsonl`: `d97d983fdaab2c08b78584090ba72ffb0eff379a3e9e702c5dbe63cfa49cc488`
- Scientific support remains narrow: the input path is implicated in this synthetic diagnostic;
  semantic understanding, autonomous rough-input success, cognitive-core validity, concepts,
  organs, biological fidelity, and external generalization remain unsupported or unevaluated
- Protected hashes and claim grades: unchanged

## 2026-08-26 — R-V03-0004 — C12 computational sensory-gate acceptance

- Dependency: accepted C11 merge `5bf5050`
- Protocol/run: `c12-sensory-field-v1` / `c12-sensory-field-main-v1`
- Seeds: 2601, 2602, 2603, 2604, 2605
- Statistical method: paired seed/world episode blocks (10 change/omission blocks; at least five
  blocks for every primary comparison); 10,000 nonparametric bootstrap resamples; bootstrap
  seed 4312; 95% intervals
- Worlds: HabituationWorld, UnexpectedChangeWorld with explicit omission, GoalTargetWorld,
  DistractorNoiseWorld, and StimulusSpecificityWorld
- Full-condition result: predictable-repetition emitted-Spark reduction 1.0; downstream-active-
  work reduction 1.0; change/explicit-omission recall 1.0; bounded-goal low-salience recall delta
  1.0; irrelevant false-activation increase 0.0 percentage points; stimulus-specificity recall
  1.0. All frozen G04 gates passed.
- Omission contract: a previously observed expected channel is explicitly marked absent, scored
  as value zero against its prediction, then value zero is committed as the latest local value.
  It is not inferred from a missing key and is not evaluator truth.
- Engineering evidence: schema-versioned strict canonical sample/Spark contracts; complete
  per-channel score trace; goal requested/applied cap trace; recursive truth/label/test-only
  refusal; atomic multi-channel failure; direct bypass; state-neutral inspection; canonical
  serialization and exact Spark ID/state-hash replay.
- Negative / limiting evidence retained: bypass eliminates repetition suppression; no-goal
  removes the goal recall gain; several ablations remain synthetic diagnostics. Every channel is
  still inspected/scored/updated, so only downstream active work decreased. No total-compute,
  latency, energy, biological, semantic, or external-generalization claim is supported.
- Raw rows: 2,590 trace rows and 70 change-recovery example rows under
  `artifacts/v03/c12_sensory_field/`.
- Artifact SHA-256:
  - `ablation_metrics.json`: `29196c2feaf202cc8a4ce819c53825f891e603385bdfa7c450b3267fe10b537f`
  - `change_recovery_examples.jsonl`: `246fbb500b52ac99900e9cda38da4575ff5ed046916b3e96cee1525c8058f0a8`
  - `goal_bias_adversarial.json`: `6f7f7c5ad38d7fe33235880958f5393ed922226adbd993bcd8bced6ca8b4ed4f`
  - `protocol.json`: `73ab1dfccf90feebd460b1811edf513e64e8f5cf3cbef107fe7dd1e13ea41de5`
  - `raw_trace.jsonl`: `341fe3f56d081223cb1f40096096804782140575335d6fd18bcb040bcfca83a6`
  - `report.md`: `a21c3e2611b339846b8b6fd41ad86047fde68cd20e06f1c26c3c8b0b0e383098`
- Claim-grade impact: unchanged. This accepts only the C12 computational sensory gate.

## 2026-08-26 — R-V03-0005 — C13 evidence/entity engineering acceptance

- Dependency/source: accepted C12 merge `280516fb61eab7c7a96c109baefc82b333fcc367`;
  frozen C13 source `03b26591c653592ec501177d9628bd2bea9b8ec4`
- Protocol/run: `c13-evidence-entity-v1` / `c13-evidence-entity-main-v1`
- Seeds/fixture: 2601--2605; 24 episodes and six ordered events per seed; all five preregistered
  fixture SHA-256 values matched
- Statistical method: five paired seed effects, 10,000 bootstrap resamples, bootstrap seed 4313,
  95% interval
- Engineering result: all G02/G05 gates passed; failed seeds 0; E2 execution rows 0
- E1 result: cross-talk 0/60, evidence misassignment 0/360, oracle entity coverage 360/360
- E0 result: cross-talk 60/60; E0-minus-E1 effect 1.0, 95% paired interval [1.0, 1.0]
- Invariants: exact late redelivery, immutable same-ID rejection, correlation discount, complete
  lineage, append-only deactivate/restore, fixed-time state/summary/probability/decision/citation
  restoration, orphan-free citations, condition separation, and permutation-invariant slot
  metrics passed focused tests
- Strongest counterexample/boundary: E0's reserved global scope produced cross-talk on every
  constructed directed opportunity. E1 uses explicit Oracle entity slots and therefore is not
  autonomous entity discovery or learned binding.
- Audit boundary: audit rows are hash-chained and semantically replayed, but the chain is not an
  externally anchored signature or independent trust root
- Reproduction: a different `PYTHONHASHSEED` reproduced all eight checked-in artifacts
  byte-for-byte
- Raw retention: `entity_condition_metrics.json` stores all 1,440 ordered execution rows and
  `evidence_invariant_tests.json` stores the before/after observations used to independently
  recalculate condition counts, E2 row count, E1 assignment/coverage, lineage, G02, and G05
- Artifact SHA-256:
  - `causal_removal_examples.jsonl`: `4135080fd29c2d5d0c13aec2aa1fbb6d2c83c5d0b0b8a0246744e2790f7d23b3`
  - `cross_talk_examples.jsonl`: `aff4a6f79df1cc144e1ca6a58ecb18b929efd18fd5fb9921fba757b5a63bbfd7`
  - `entity_condition_metrics.json`: `b0206eddde4ebe4c388df1b5819236cbfbd9ce60ea679cea919da032ff1739ca`
  - `evidence_invariant_tests.json`: `b59781773bbb6407ef7cf6c3d9568040d7052d0263be4aad7bd7412ef0f8f6dd`
  - `paired_statistics.json`: `7eff9c36d3d55c250565cb03dc2687bfa9dea36ec5499ac6dd4fb8f1f4d992af`
  - `protocol.json`: `e01330571ef77896356cb12b789ff5706e75f635a2d921c7116465dd53a25095`
  - `report.md`: `4f3746c36bad498d57937710208a576050d28afeb92dc9282aeb9757342c6bb3`
  - `run_manifest.json`: `a2dd2b76731476712a0964f4c6b8bd81b12e19ef77c45ab493cbb172fd46b7c3`
- Claim-grade impact: unchanged. C06/C08 negative results, protected hashes, package 0.2.1,
  persisted schema 0.2, and release metadata remain unchanged.

## 2026-08-27 — R-V03-0010 — C16 bounded proto-concept formation acceptance

- Protocol/run: `c16-proto-concepts-v1` / `c16-proto-concepts-main-v1`; source
  `4933a6059240875d0548fe602f114d768a49ef28`
- Execution lineage: `codex/c16-proto-concepts` pre-artifact head `3dd9593`, retaining source pin
  `b1c83e6` and source-only commit `4933a60`
- Seeds/statistics: run seeds 3601--3605; paired hierarchical bootstrap with 10,000 resamples and
  bootstrap seed 4366; failed seeds 0
- Engineering: 8/8 gates passed; raw retention is 990 lineage, 90 bank, 5 checkpoint, 5,760 held-out
  episode, 360 seed-summary, 72 utility-aggregate, 60 control-bank, 240 seed-comparison, 48
  aggregate-comparison, 1,920 causal, and 60 counterexample rows
- Scientific stages: CC0 supported (109 candidates); CC1 supported (6); CC2 not supported (0); CC3
  not supported (0). Counterexamples retain 46 `utility_regret` and 14 `no_failure_observed` rows.
- Independent audit: full audit PASS. Reproductions with `PYTHONHASHSEED=1` and
  `PYTHONHASHSEED=37` were byte-identical for the exact-eight bundle.
- Artifact SHA-256:
  - `protocol.json`: `122d3013ff859bba41314f2217f209b5573e1d3ae207b11132963cd7bb034174`
  - `candidate_lineage.jsonl`: `963d5f9c7d436b7d00c7310eb56502b0f907de3c1df2f6daa0580cee7ec46aa2`
  - `candidate_metrics.json`: `97ddf6d7a14e54456bbaa4f53e672cb955c672acbb8c79917e548e894878f9f6`
  - `held_out_utility.json`: `21ff8947dc9b82026f32d692f6299dfab1154026caf8a9a5d619860d04ca5c2b`
  - `causal_interventions.jsonl`: `1ae153d3f5b8f9e0aa064ce8118a8a8db3ad702b267bb10add16fe411ea4fff7`
  - `matched_controls.json`: `e7b48fd3df30206294985a5e0def1a7edb4af4c7e4516b74d4926d30f86d2baf`
  - `failure_examples.jsonl`: `223c21e6ca972e2795a0e1cf87c9508a8e1a34e681e9d4ca4232965915a054be`
  - `report.md`: `3c53f8cc435ec32240763a66e4c6af2a7c919aa463acb553f29c17e6d4b7b9ee`
- Claim boundary: this is not evidence of semantic understanding, an organ, biological equivalence,
  energy efficiency, or a claim-grade increase. Package/schema, release manifests, and metadata are
  unchanged.
## 2026-08-26 — R-V03-0006 — C14 attributable Coalition-gate acceptance

- Dependency/source: accepted C13 merge `06e13975b486548bb17924acc3b82786246ad6e1`;
  final C14 source `eb7f542963397eba1b7d9b4a66a7873b3ba17ac4`
- Protocol/run: `c14-coalition-gate-v1` / `c14-coalition-gate-main-v1`
- Seeds/statistics: 2701--2705; 10,000 paired bootstrap resamples; bootstrap seed 4314
- Engineering result: all 12 frozen G03 gates passed; failed seeds 0
- Raw retention: 360 raw rows, 15 causal-removal rows, 24 aggregate metrics, 120 seed rows,
  four paired statistics, and 50 reason references
- Causal/invariance results: independent-support Ignition 1.0; removal reversal 1.0; exact
  restoration 1.0; same-ID score delta 0.0; correlated-group inflation 0.0;
  contradiction score delta -0.1296997075145081
- Comparator result: G1 differed from both `G0_probability_margin` and
  `G1_no_coalition_ablation` on 0.9 of paired primary cases; fixed logits were unchanged
- Reproduction: all six checked-in artifacts reproduced byte-for-byte under a different
  `PYTHONHASHSEED`, and independent raw-only recalculation matched every derived output
- Artifact SHA-256:
  - `causal_evidence_removal.jsonl`: `f11aa38ac50a23665b7d9f21b87b11352c41842a396a679b1353f05e7b3e3e97`
  - `fixed_logit_interventions.jsonl`: `45c66151abed1d25badfa3755ca692256314eb03f1f8b33ef29f6b6f1b15b2ec`
  - `gate_ablation_metrics.json`: `b7030b45f79c388d5ba5a2bc422d3b0a744de5ee2bb91d5ca8f8323be65eb514`
  - `no_ignition_reasons.json`: `ea4fbd34976a083509253570622691ff81395ea0420bd572dbd121bd2f52dd16`
  - `protocol.json`: `aa5e405204832f5b76be2f9d7a1ad648f36b17b8309596c4a105e4d37fd344d0`
  - `report.md`: `19a666bd41567fbc60f1c8db94516224606fac2506522290f3217ed0efa966cb`
- Negative/boundary result: this is a fixed-logit, controlled-synthetic engineering result.
  It does not establish external accuracy improvement, learned Coalition formation, semantic
  understanding, biological fidelity, or energy efficiency.
- Claim-grade impact: unchanged. C06/C08 negative results, protected hashes, package 0.2.1,
  persisted schema 0.2, and release metadata remain unchanged.

## 2026-08-26 — R-V03-0007 — C15 v2 global aggregation failure and timeout noncompliance

- Protocol/run: `c15-revision-objectives-v2` / `c15-revision-objectives-main-v2`
- Audited source: `bb89797c92a8a5f38216dac00f48cfa59f66381f`; source-pin amendment:
  `b521249`; model seeds 2851--2855; bootstrap seed 4365
- Pre-run verification: 439 tests passed and five were skipped, including the clean-room
  archive suite; local readiness, Ruff, source-scope audit, and all 28 protected hashes passed.
- Environment correction: the first invocation stopped in preflight because the shared
  editable environment pointed to the main worktree. No model ran in that invocation. The
  subsequent invocation explicitly set `PYTHONPATH` to the C15 worktree's `src` directory.
- Failure: training/evaluation returned to global aggregation without a recorded failed seed,
  then `_comparison_effect` attempted `float(None)` inside `_bootstrap_intervals` and raised
  `TypeError`. No scientific metrics or support decision were printed or accepted.
- Contract gap: empty prediction-dependent metrics are frozen as null, whereas the bootstrap
  contract requires 10,000 finite effects and does not specify undefined resamples. Dropping,
  redrawing, or imputing such resamples is not authorized by v2.
- Additional protocol violation: the run exceeded the frozen 120-second timeout, which the
  source did not enforce. The elapsed execution is not a compliant v2 run.
- Artifact boundary: global aggregation failed before publication. The atomic runner removed
  staging and published no final eight-file bundle. In-memory prediction/training rows were
  not retained and are not claimed as validated evidence.
- Disposition: implementation failure plus protocol noncompliance, not a scientific negative
  or an inconclusive scientific finding. C15 is not accepted. Any corrected official execution
  requires a new Decision/protocol, fresh unused seeds, a newly audited source pin, explicit
  nullable-bootstrap behavior, and an enforced execution-budget contract.
- Claim-grade impact: none. C06/C08 negatives and accepted C11--C14 evidence remain unchanged.

## 2026-08-26 — R-V03-0008 — C15 v3 completed negative evaluation; engineering not accepted

- Protocol/run: `c15-revision-objectives-v3` / `c15-revision-objectives-main-v3`.
- Source: `eedb8b426f326c5dcb70bd548008695eb1652aee`; authorized execution tree:
  `6860c2ec4133a9debefdec0b92e33ab0e09b430f`; model seeds 2901--2905; bootstrap seed 4415.
- Status: engineering `fail` (7/8 gates), scientific `not_supported`, `failed_seeds=[]`.
  The runner completed and published exactly eight artifacts; no failed seed was omitted.
- Retention: 21,760 prediction rows, 23,040 training-step rows, 540 independent objective rows,
  60 condition-seed rows, 170 seed and 34 aggregate confusion/calibration rows, 60 Pareto seed
  points, 12 aggregate points, and 66 pairwise comparisons.
- Failed engineering gate: `continuous_recovery_all_seeds`. Primary full/I1/E1/base recovery
  successes/opportunities for seeds 2901--2905 were respectively 0/8, 0/8, 8/8, 0/8, 0/8 in
  both dev and test. Test stage histories show actual A-to-B-to-A recovery only for seed 2903
  (8/8); no checkpoint was restored. Seed 2905 reaches the final truth belief in 8/8 cases but
  predicts `update`, not `recover`, and has no A-to-B-to-A history. This is not counted as recovery.
- Limited positive observation: seed 2903, episode `ep-3da465ebad16b6d7`, retains beta activation
  0.30634395227432254 while gamma is the winner, then recovers beta with history
  `[beta, gamma, beta]`, latency 2, and no checkpoint restoration. This establishes an observed
  capability on that slice, not every-seed engineering acceptance or residual superiority.
- Seven passing engineering gates: raw/training cardinality, zero checkpoint restores, explicit
  no-Ignition (17,824 raw rows), exact-zero objective ablations, attribution-target coverage 1.0,
  and citation resolvability 1.0. Every one of the nine full-condition objectives has nonzero
  weighted-gradient observations. Zero-weight contributions and gradients remain exactly zero.
- Failed scientific gates: full recovery rate 0.2 equals no-residual 0.2, so strict residual
  superiority is false. ECE is 0.5228200732591222 for full versus 0.1174588372476693 for weighted
  CE; increase 0.40536123601145285 exceeds the registered maximum 0.03.
- Other scientific point gates pass: distractor changed predictions 4/160, same-ID 0/160,
  correlated-copy 1/160; the other four weighted-CE noninferiority dimensions; at least one
  required strict improvement. Passing these does not override either failed scientific gate.
- Nullable statistics: full-minus-weighted-CE ECE has 9,992 defined and 8 undefined resamples;
  its finite point effect is retained and both bounds are null. Each other comparison has
  10,000 defined and zero undefined resamples. No undefined draw was dropped or imputed.
- Independent audit: exact-eight inventory, canonical serialization, nested schemas, raw grids,
  source/protocol/fixture hashes and all 28 protected hashes pass. Confusion, calibration,
  objective gradients, engineering gates, report, Pareto/scientific point gates and all nine
  10,000-draw bootstraps recalculate exactly from retained rows without model/controller replay.
  A second execution from the same frozen execution tree with `PYTHONHASHSEED=37` reproduced all
  eight files byte-for-byte against the `PYTHONHASHSEED=1` original. The deterministic exact-eight
  transport ZIP is 17,301,391 bytes with SHA-256
  `1ef3ef26334c0854bc6d9e4695da4fd6a380930dece80ba4659364bf36000f32`. Its separate index
  preserves each uncompressed size/hash and explicitly excludes the transport from the canonical
  artifact directory and release surface.
- Canonical report limitation: the frozen report's generic sentence about scientific failures
  not invalidating separately passing engineering is conditional; engineering did not pass in
  this run. Preserve the report bytes and this explicit interpretation rather than editing it.
- CI/provenance: execution tree `6860c2e` has a known amendment-test fixture failure, reproduced
  locally and in CI run `32914883175` on Python 3.11/3.13. The real committed protocol amendment
  passes the production guard. D-V03-0025 and integration-only test fix `d465adf` normalize the
  synthetic fixture without changing runtime/protocol/artifacts; a green integration suite must
  not be reported as a green full suite or clean-room phase on the original execution tree.
  On integration source `d465adf`, all 50 runner tests pass and the full suite has 471 passed,
  five skipped (476 collected); Ruff and diff/UTF-8 checks pass. The post-pin guard rejects
  official execution on this integration tree before model evaluation or output creation.
- Disposition: retain a completed negative evaluation, but C15 engineering acceptance and its
  C17 dependency remain blocked. No threshold, loss, fixture, seed, target, or denominator is
  relaxed after inspection. C16's independently accepted C12/C13 prerequisites are unaffected.
- Claim-grade impact: none. C06/C08 negatives, accepted C11--C14 outputs, package 0.2.1,
  persisted schema 0.2, and release manifests remain unchanged.

## 2026-08-28 — R-V03-0011 — C17 v1 control-pool implementation failure

- Protocol/run: `c17-functional-organs-v1` / `c17-functional-organs-main-v1`; source
  `d407663bdfeb10a29ac5791d34bace6dfa7fbbef`; execution-pin head
  `4744ff7335ffcb1ad7510555db3b8b9ad4be383a`
- Execution: official seeds 4701--4705 all completed; `failed_seeds=[]`; exactly nine canonical
  artifacts were published; bundle-manifest SHA-256
  `9a3c50f3773d6dc40652adce06db6158a0aaeb3867fb0945078878614e58374f`
- Engineering result: `implementation_failure`. Fourteen of sixteen gates passed;
  `control_completeness` and the first-run `reproduction_exact` evidence gate did not. The later
  reproduction establishes byte identity but does not retroactively change the immutable v1
  acceptance matrix.
- Failure cause: all five candidate-present cells were R4. Each had candidate-bank size 2 and
  target-member count 2, hence eligible non-target control-pool size 0. Five required control
  types per seed were missing, for 25 missing slots. The other 20 cells had no primary candidate
  and are valid scientific-negative cells, not engineering failures.
- Scientific interpretation: the bundle displays `not_supported`, but the valid disposition is
  `not_evaluated_implementation_failure`; mandatory matched controls were unavailable, so the
  scientific hypothesis was not evaluated.
- Raw cardinalities: 25 candidate-discovery rows, 100 structural seed/split rows, 600 selectivity
  episode rows, 2,100 matched episode/branch rows, 2,100 held-out episode/branch rows, 125 control
  membership rows, 150 matched seed-effect rows, and 25 resource counters.
- Reproduction: a second run with `PYTHONHASHSEED=8675309` matched every exact-nine byte. The
  official hashseed was not recorded, so distinct hashseeds are not claimed.
- Disposition: v1 is immutable. A C17 v2 engineering correction requires a separate preregistration
  and audit; v1 source, thresholds, and evidence are not repaired in place.
- Claim-grade impact: none. Package/schema/release metadata and C06/C08 evidence remain unchanged.
