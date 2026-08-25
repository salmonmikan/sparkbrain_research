# Results and Negative-Result Ledger

Append entries; do not rewrite prior outcomes to match later interpretations.

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
- `tests/test_scientific_integrity.py` freezes the reviewed C06, C08, primary-subset, and claim
  register SHA-256 values.

### Boundary and blocker

The runtime pytest phase follows pristine archive validation; a second pristine audit uses a new
extraction. Cache files remain forbidden in the shipped tree and are not added to the manifest.
The owner has not selected a license, so no public archive or tag is produced. C06 and C08 remain
negative, CL-007 and CL-008 remain E0, and the primary subset remains explicitly non-full.

**Claim impact:** no scientific evidence grade increase. This is a release-integrity and command
contract correction only.
