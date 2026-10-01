# Continuous temporal-reuse probe: source-audited design v2

Status: **DESIGN / EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**. Scientific credit: **0**.
Prepared 2026-10-01 UTC. No new model, stream generator, or scientific runner has been
executed for this document. This is an engineering diagnostic proposal, not a formal
preregistration, accepted build contract, or scientific allocation.

Source pin: `bd337bef2edddb2d388cbcf47bf176d469c2b180` (merged literature PR #168).
Human Directive index: `ops/human-directives:ops/human_directives/active.md`,
branch head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`,
index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, freshly read 2026-10-01 UTC.

## Amendment before execution

v1 was published at `250eee30df5768fd9bdc8e8a9b32a5fcc9e15cc5` before any new
model/stream execution. Independent source/protocol review found that zero-valued cue
records do not create identical inputs, native checkpoint coverage needs a quiet-boundary
restriction, and timing/metric/resource language needed tightening. This v2 addresses
those points prospectively; v1 remains immutable Git history. No result informed the changes.

## 1. The decision this would inform

The goal is an inspectable local computational theory in which experience changes
Spark/assembly state and that state causally changes later prediction or action.
A working provenance ledger, a change detector, or a visually distinctive activity
pattern does not establish that goal.

The immediate question is narrower:

> In a persistent prediction–outcome loop, does the existing v0.5 assembly path
> preserve useful cue-order information and reuse it after an intervening context,
> beyond an ordinary history model and a retained raw-history reuse model, with
> cue-specific effects of selective intervention?

A negative answer is useful: it distinguishes an input-access or interface failure,
a conventional-memory reduction, and dependence on acquired assembly state without
dependence on field weight/delay learning. It would decide whether a temporal-state
adapter deserves later integration design. This probe does not connect v0.5 to M1,
repair SB002, or establish that either integrated runtime has acquired this capability.

The [charter](../PROJECT_CHARTER.md), [v0.5 plan](../V05_MASTER_PLAN.md), and
[merged information-access report](nonstationary_evidence_capability_map_20261001.md)
supply the goal. Current
[HUMAN-20260928-001](https://github.com/salmonmikan/sparkbrain_research/blob/ops/human-directives/ops/human_directives/history/2026-09-28/HUMAN-20260928-001-accelerated-integrated-sparkbrain-completion.md)
prioritizes the continuous observation → state → competing alternatives → selection or
abstention → prediction/action → later outcome → selective revision → next prediction loop.

This work follows the user's separate explicit request for parallel autonomous research
with external papers and GitHub evidence. It does not assume a scheduled role, consume an
Analyst/Formal identity, or invoke role-specific build authority. Current common policy
allows development and separates non-evidentiary exploration from scientific confirmation;
the directive alone does not authorize a new scientific allocation. No scheduler,
control-plane, formal/sealed/evidence ref, PR #164, or PR #167 file is a write target.

## 2. Source feasibility and limits

The source supports an isolated wrapper, provisionally, without runtime edits:

- [`process_episode`](https://github.com/salmonmikan/sparkbrain_research/blob/bd337bef2edddb2d388cbcf47bf176d469c2b180/src/sparkbrain/v05/brain.py#L132-L245)
  retains the receptor/field/assembly/predictor state, creates patterns from internal
  reservoir spikes, selects the strongest mature non-suppressed assembly, and returns
  a prediction before the later outcome call.
- [`learn_outcome`](https://github.com/salmonmikan/sparkbrain_research/blob/bd337bef2edddb2d388cbcf47bf176d469c2b180/src/sparkbrain/v05/brain.py#L247-L263)
  updates the selected assembly's predictor and supports assembly-path suppression.
- [The bank](https://github.com/salmonmikan/sparkbrain_research/blob/bd337bef2edddb2d388cbcf47bf176d469c2b180/src/sparkbrain/v05/assemblies.py#L165-L291)
  acquires prototypes from experience and matches fixed similarity rules. A prototype is
  the first stored pattern; it is not a gradient-trained representation or moving centroid.
- [The readout](https://github.com/salmonmikan/sparkbrain_research/blob/bd337bef2edddb2d388cbcf47bf176d469c2b180/src/sparkbrain/v05/prediction.py#L9-L48)
  learns outcome counts per assembly. This supervised association is separate from
  unlabeled pattern acquisition and from field plasticity.
- [Existing status](../V05_STATUS.md) already records a controlled-synthetic positive
  assembly-path result, but no necessary/beneficial low-level weight/delay plasticity and
  substantial collateral damage for physical-unit ablation. Those results are prior
  exposure, not new evidence, and are neither rerun nor reinterpreted here.

The added diagnostic is fixed-window common-query aliasing, uninterrupted A→B→A reuse,
stronger raw-history alternatives, and same-checkpoint input/intervention contrasts.
The unchanged API pools cue and Q cascades within one call before strongest selection.
Thus this is a fixed-window temporal-pattern classification/reuse diagnostic, not evidence
that Q reads only an independently persisting post-cue latent state. It cannot establish an
event-by-event streaming representation or M1's complete hypothesis-selection loop.
It differs from the old alternating motif evaluation in its common query, intervening
context, matched raw-reuse alternatives and paired input controls. Existing
`v05.evaluation`, historical seeds/checkpoints, and consumed protocols are not invoked.

The wrapper may call existing APIs and inspect read-only state. It must not change
selection rules, delays, thresholds, routing, or low-level dynamics to rescue results.
If the common query monopolizes selection or the permitted window cannot preserve the
cue, report that interface failure rather than silently retaining the cue's earlier winner.

## 3. Common input and timing contract

Prediction is the only functional track. No policy, reward optimization, or action-success
claim is attempted.

Each independent stream has 96 fixed 200 ms observation cycles and one persistent model.
Each cycle receives exactly these raw pulses, all with constant source
`probe-input`, polarity +1, novelty 0, prediction_error 0, and empty metadata:

- cue: either A,F,C or C,F,A at cycle-relative times 8,13,15 ms, magnitude 1.18
- two distractors: channels sampled independently with replacement from H,I,J,K,L,M,
  magnitude 0.025, times uniform
  on [0,36] ms; sampling does not depend on cue/target
- common query: Q at 40 ms, magnitude 1.18

The two cues share event counts, channel counts, amplitudes, and timestamp multiset.
Every arm receives the same ordered raw pulse records. Current Q is identical in both
contexts; outcome is 0 after A,F,C and 1 after C,F,A.

The v0.5 call uses settle_ms=32. The Q drive necessarily exceeds the unchanged receptor
emission threshold from the positive direct term alone; its last raw event is at 40 ms,
so the expected model end is 72 ms. Assert end_ms == cycle_start+72 before scoring.
Score the prediction at 72 ms; deliver the outcome at logical time 80 ms, then process
the next cycle at +200 ms. No future outcome pulse is inserted into the input batch.

There are no extra padding pulses or reset calls. No per-motif boundary, switch marker,
block label, regime ID, future suffix, evaluator label, or target field reaches a model.
The fixed cadence is observable to every arm and is independent of context. An opaque
monotonic cycle occurrence ID is used only for maturity/receipt bookkeeping, never as an
input feature; it carries no seed, cue, condition, or target name. Predictions must
remain invariant under a bijective renaming of these IDs.

All earlier delivered outcomes are available equally through the outcome API. A model
may choose what to retain within its cap; different internal encodings are the compared
mechanisms. No arm may reread evaluator files or raw audit logs as extra memory.

Two suffixes branch from the same 64-cycle development/training history per seed:

1. **Return:** A for 32 cycles, B for 32, then A for 32
2. **Interleaved:** the same A32,B32 prefix, then 32 independently drawn fair A/B cues

RNG contract: independent Python `random.Random` generators seeded by the integer SHA-256
of UTF-8 `910071|prefix|0`-style strings: seed, stream key, and zero-based cycle/probe
index joined by "|". Keys are `prefix`, `return`, `interleaved`, `probe`.
For each cycle draw two distractor channels with `randrange(6)`, each followed by its
uniform time; suffix/probe cycles then draw three cue jitters; interleaved cycles finally
draw one cue bit with `randrange(2)`. Paired probe A/B variants reuse all sampled values.
Prefix indices are 0..63; suffix indices 0..31; probe indices 0..7.
The prefix uses exact cue timing. Each suffix cue gets independent uniform timing jitter
in [-0.35,+0.35] ms; Q remains at 40 ms. Order cannot change at that jitter. Fresh suffix
distractors differ from prefix. The prefix is development exposure, not evaluated evidence.
The first return prediction precedes the first return outcome; report it separately.
No model is told that suffix evaluation begins or that A returns.

This tests **cued recurring conditions**, not uncued nonstationarity or reversal of the
cue–outcome law. Outcome history can reveal the block context. The interleaved suffix and
paired cue interventions, rather than block accuracy alone, test the cue's added value.

## 4. Compared mechanisms and update rules

Five fixed arms, no tuning/search:

| Arm | Representation and learning | Forgetting/reuse |
|---|---|---|
| Q marginal | Beta(1,1) outcome counts; ignores earlier cue by design | No forgetting; weak limitation reference only |
| H raw recent memory | Current-window raw raster, k=3 nearest completed windows by L1 distance; Laplace-smoothed votes | FIFO 32 labeled windows; ordinary bounded history comparator |
| R raw retained prototypes | Same raster; nearest prototype if L1 distance <=0.25, else allocate a new prototype; incremental mean raster and two outcome counts | 32 slots; retain all allocated prototypes; when full use nearest existing, no eviction |
| S assembly | Existing v0.5 defaults with action disabled, topology_seed=41, AssemblyConfig(max_candidates=32) | Existing bank and count predictor; no added forgetting |
| F frozen weights/delays | Same as S except enable_weight_learning=False and enable_delay_learning=False | Assembly acquisition, predictor learning and homeostasis remain active |

H/R's common raster is magnitude in 1 ms bins 0..40 for the 10 literal channels
A,C,F,H,I,J,K,L,M,Q. Split each pulse linearly between floor(time) and ceil(time);
a pulse exactly on an integer occupies that bin. Normalize the complete raster by total
magnitude. Do not filter distractors, select channels with labels, or fit an encoder.
Distance is the L1 distance of these 410 entries. H uses the nearest min(3,N) records,
ties by insertion order; its p1=(1+sum(y))/(2+k). R creates the first prototype on its
first observed window; a new prototype predicts p1=0.5 before its first outcome.
R assignment is fixed at prediction time and updated only after that outcome.
Existing-prototype p1=(1+n1)/(2+n0+n1); new prototypes start with zero counts.
An exact distance-threshold tie matches; nearest ties use insertion order.

S/F receive only source-valid config changes listed above. Receptor, field, assembly
similarity/maturity, plasticity rates, and homeostasis defaults remain pinned.
Native predictor confidence is not calibrated probability. For common Brier scoring only,
derive p1=(1+n1)/(2+n0+n1) from the already selected assembly's existing two counts,
or 0.5 if no selected mature assembly has counts. This adapter cannot change selection,
native prediction, or training. Preserve native abstention and coverage separately.
S/F are described as acquired prototype-bank plus learned count-readout models; improved
prediction alone must not be called learned field dynamics.

Q/H/R hard decisions are 0 for p1<0.5, 1 for p1>0.5, and abstain at exactly 0.5.
S/F preserve the native predictor's decision, including its existing count-tie rule.
For every arm, accuracy counts an abstention as incorrect and uses all scored rows;
coverage is non-abstaining rows divided by all scored rows. Brier always scores p1,
including 0.5 for an abstention. Label native-decision results separately from Brier.

All arms learn from each outcome once, immediately after prediction. No offline extra
epochs, replay training, hyperparameter grid, restart at a block, or best-seed selection.
For H/R, earlier outcomes affect retained records/counts; they are not regime labels.

## 5. Prospective resource and execution bounds

Diagnostic seeds: 910071 and 910072, used only for new synthetic distractors/jitter/suffix
selection. They are not confirmatory seeds. One CPU process per arm, no GPU, network off
during diagnostic execution.

- One 64-cycle prefix plus two 32-cycle suffix continuations per arm/seed
- 32 representation slots for S/F/R and 32 example slots for H; Q has two counts
- 120 CPU seconds and 180 wall-clock seconds per 96-cycle trajectory
- 512 MiB address-space cap per process; maximum 64 MiB serialized full model checkpoint,
  including retained trace state; no unreported log deletion to satisfy the cap
- Full diagnostic cap: 30 CPU minutes, 45 wall minutes, 1 GiB output; stop, preserve,
  and report `resource_limit` if any required trajectory cannot finish
- Existing S/F event/spike/update safety caps remain unchanged and are separately logged
- Per-trajectory cost is measured prefix cost plus that suffix cost, including checkpoint
  serialization/restoration and measurement/output overhead; shared-prefix CPU is charged
  once to total diagnostic cost, while every suffix, causal fork and guard is charged
- No model execution is hidden outside these caps; implementation-only unit tests are
  reported separately. Unfinished or killed required runs have no complete-result status

Slot counts are not equivalent byte counts or compute. Record peak memory, state bytes,
CPU time, wall time, model queries, prototype comparisons, field processed events/spikes,
and eligibility/update work. The source's plasticity `update_count` is eligible-edge work,
even when both learning flags are disabled; it is not a count of learned changes.
Separately record pre/post weight and delay hashes and changed-parameter counts. All arms have the same outer cap, but **equal actual resources
are not established**. Do not claim efficiency or exact resource matching merely from
caps; report the observed resource/accuracy trade-off.

Duplicate receipt replay is a wrapper contract test with zero extra model updates.
Correction handling, transport retries, stochastic conflicting observations, general drift
detection, and delay/reward experiments are outside this bounded probe.

## 6. Frozen causal checks

Select targets using only the completed 64-cycle prefix; never use suffix truth or results.
For each S/F arm, count each selected assembly's occurrences on prefix cue A and cue B.
The target is the mature assembly with the most A selections among those with >=8 A
selections and zero B selections; ties by ascending ID. Its non-target match is a different
mature assembly with >=8 B selections, zero A selections, and prefix selection count within
25% of the target; choose the smallest count difference, then ascending ID.

No target or match means `intervention_not_identifiable`, not zero impairment or a pass.
Do not relax the criteria, replace a missing control with an inactive unit, or add training.

At the prefix checkpoint, evaluate 8 independent paired A/B presentations with new
distractors/jitter. Each paired fork begins from the identical checkpoint **before the first cue**, with
identical occurrence ID and presentation time across its A/B/removed counterparts,
uses cycle_start=12,800 ms (not sequentially increasing probe times), receives one
presentation, and stops before outcome learning. All probe forks set
`learn_assembly=False`, `learn_field=False`, and `explore_action=False`; pulse/receptor/
field state still evolves according to the existing dynamics. Future training cannot
differ between interventions:

- sham: unchanged checkpoint
- targeted: suppress the selected target assembly ID through the existing public API
- matched non-target: suppress the chosen B assembly ID
- observer-only: remove no state; omit the diagnostic display row only

The exact maximum matrix per seed is: for each S/F arm, 8 pairs × 2 intact cues ×
4 intervention states = 64 forks, plus 8 pairs × 2 identical removed-cue sham inputs
= 16 forks; for each Q/H/R arm, 8 pairs × 2 intact cues × sham plus 8 pairs × 2 identical
removed-cue sham inputs = 32 forks. Across two seeds this is at most 512 one-query forks.
If an S/F target/match is unavailable, skip only targeted and matched forks, record all
missing slots explicitly, and retain sham/observer/input-control forks; the causal gate
cannot pass. Each fork has a 10 CPU-second / 15 wall-second limit including checkpoint
load, prediction, serialization and measurement. No post-fork outcome update is performed.

This measures assembly-path/readout causality, not physical-unit specificity.
Require the observer-only prediction/state transition to equal sham exactly.

For the same eight pairs, use identical distractors and pre-cue checkpoint state, swap only the
A/C order while preserving Q, amplitudes and times. A prediction difference now has an
identified causal input difference. Cue removal **omits all three cue records**, leaving only the identical distractor and Q
records; do not pass zero-valued A/C/F records, since channel-specific receptor state can
still change or emit on those records. The target remains evaluator-side. On a removed-cue A/B pair the complete model-visible
prefix is identical, so deterministic predictions must coincide. This exact fork property
does not imply loss of every history advantage on an ordinary block stream.

## 7. Metrics, observable failures, and decision rule

Retain every pre-outcome probability, native prediction/abstention, selected assembly,
input digest, state digest, outcome receipt, counters and terminal reason. Primary
descriptive metric: suffix mean binary Brier loss (p1-y)^2. Also report coverage, native
accuracy including abstentions, first-return p1/loss, return loss for the first 4 and all
32 outcomes, and the interleaved suffix loss. Report both seeds separately. No p-values,
confidence intervals, population estimate, or general-performance claim from two seeds.

For each paired fork, impairment is intervened Brier loss minus sham Brier loss.
Report A-target impairment, B-collateral impairment, and targeted-minus-matched impairment.
A useful further integration proposal requires, descriptively in **both** seeds:

- return and interleaved S Brier are each at least 0.02 lower than both H and R
- first-return S confidence is 1-p1(A)>=0.75 before its outcome receipt
- mean A targeted-minus-matched impairment >=0.05, mean absolute B collateral <=0.02
- at least 6/8 intact sham swapped pairs have p1(B)>p1(A)
- identical removed-cue prefixes and observer-only forks produce identical outputs
- every execution/information/resource/replay guard passes

These thresholds are engineering decision thresholds only, not scientific evidence grades.
If raw retained reuse matches/beats S, report this conventional reuse model suffices here.
R's fixed raster and 0.25 threshold can be sensitive to suffix jitter; an S advantage is
relative to these specified alternatives, not conventional temporal-memory methods generally.
If F matches/beats S, no benefit of weight/delay learning is shown even if an assembly-path
effect exists. If S cannot use the common query, report that interface gap. If interventions
are unmatched, global, ineffective, or harm B similarly, no cue-specific causal conclusion.
A positive pattern is only a reason for a fresh independently authorized scientific contract.

## 8. Primary literature and what is inferred

Retrieved 2026-10-01 UTC; focused source check, not a systematic novelty review.

- R. Andrew McCallum, *Instance-Based State Identification for Reinforcement Learning*,
  NIPS 1994, pp.377–384:
  [publisher PDF](https://papers.nips.cc/paper_files/paper/1994/file/d2ed45a52bc0edfa11c2064e9edee8bf-Paper.pdf).
  Inspected §§3–4. **Source:** Nearest Sequence Memory stores action/percept/reward history,
  finds neighbors by sequence match and updates Q-values; a bounded FIFO buffer is discussed.
  **Our inference:** retained raw history is a necessary serious alternative.
  H is a small nearest-window predictor, not a reproduction of NSM or its RL results.

- Lucas N. Alegre, Ana L. C. Bazzan, Bruno C. da Silva, *Minimum-Delay Adaptation in
  Non-Stationary Reinforcement Learning via Online High-Confidence Change-Point Detection*,
  AAMAS 2021; arXiv:2105.09452v1 submitted 2021-05-20:
  [primary full text](https://arxiv.org/html/2105.09452v1).
  Inspected §4 and Algorithm 1. **Source:** MBCD stores context models/policies and can
  redeploy them when context recurs; its likelihood models and change-detection assumptions
  matter. **Our inference:** compare retained reuse, not only a forgetting model.
  R is a transparent cued prototype comparator, not MBCD and inherits none of its guarantees.

- Max Dabagia, Christos H. Papadimitriou, Santosh S. Vempala, *Computation with Sequences
  of Assemblies in a Model of the Brain*, arXiv:2306.03812v2, 2023-10-16:
  [primary full text](https://arxiv.org/html/2306.03812v2),
  [record](https://arxiv.org/abs/2306.03812).
  The abstract record shortens the title to *Computation with Sequences in a Model of the
  Brain*; the cited full-text title is reproduced here. Inspected §§1.1 and 2.1.
  **Source:** under a specified k-winner/Hebbian/homeostatic model, repeated temporal
  stimulation can form sequences later recalled from partial input; Theorem 1 includes
  explicit parameter and initial-rest assumptions.
  **Our inference:** distinguish recurrence, useful recall and dependence on learned
  synaptic changes. That theorem does not apply to v0.5's fixed-similarity prototype bank,
  continuous wrapper, or this diagnostic; no brain equivalence or novelty follows.

## 9. Freeze, review, publication, and stop contract

Publish this design before generating streams or running models. Obtain an independent
protocol review; any required change becomes an explicit v2/amendment before execution.
After clean review, freeze implementation/config/source hashes and guard tests separately.
No actual execution is authorized by this document alone; the task's already granted
non-formal diagnostic scope and applicable current repository policy must both be verified.

### Restricted checkpoint eligibility

Native v0.5 save/load omits live `CascadeTracker._pending`, `BurstDetector._window`
and emitted-key caches; field restoration also rebuilds outgoing lists ordered by current
(delay_ms,target_id), while live delay learning does not re-sort them. The wrapper must
not silently repair, clear, serialize new hidden fields, or claim general checkpoint fidelity.

Permit a saved-prefix fork only if read-only inspection proves all of:

1. the field event queue and CascadeTracker pending-spike list are empty
2. every buffered burst spike is strictly earlier than 12,800-8 ms, so it expires before
   any permitted next pulse; all old emitted-key times are earlier than the next cycle
3. each live outgoing list already equals sorting by current (delay_ms,target_id)
4. wrapper receipt/pending state is also saved and restored exactly

Pre-run hand-constructed fixtures must demonstrate direct versus native-save/load
continuation equality with nonzero learned delay changes at an eligible quiet boundary,
and rejection of pending-cascade, queued-event, live-burst, or noncanonical-outgoing cases.
Equality means returned outputs and checkpoint-visible operational state, not irrelevant
Python result/cache object identity. At the real 64-cycle prefix, recheck and record every
eligibility fact; stop with `checkpoint_boundary_ineligible` if any fails. No measured
suffix or intervention is run from an ineligible checkpoint. This can legitimately stop
the diagnostic after the prefix and expose a wrapper/integration constraint.

Before model execution: check input isolation and query-time cutoff, receipt idempotency,
ID-renaming invariance, paired-prefix equality, checkpoint continuation and budget enforcement.
Tests use hand-constructed fixtures, not measured suffix results. If a source-valid wrapper
cannot satisfy these guards without a runtime change, stop with the missing contract.
Do not search another configuration under this version.

After execution starts, preserve raw records before scoring; publish negative/failed/incomplete
trajectories as well as aggregates, environment versions, exact command and source hashes.
Reproduction uses only this fresh diagnostic identity and never invokes a historical runner.
No historical status/claim/result ledger is changed by design publication. A later result
will receive its own scoped report; any shared-ledger update requires coordination.

Current validation: source/API and primary-paper inspection only. No runtime tests,
benchmarks, new capability result, or resource feasibility result is claimed.
