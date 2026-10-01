# Plasticity retention after the temporal-reuse negative result

Date: 2026-10-01 UTC. **SOURCE-ONLY DESIGN / EXPLORATORY / NONCANONICAL /
NON_EVIDENTIARY. Scientific credit: 0. No execution allocation.**

## Recommendation and decision boundary

Prioritize one small counterfactual: remove cross-occurrence eligibility carry while
keeping current-occurrence STDP weight learning active. Compare it with the existing
carry rule, a prespecified global attenuation control, and a weight-frozen reference.
Hold delay values fixed in every arm at one common learned prefix. This asks whether
eligibility locality can improve sustained return retention without sacrificing new
learning. It does not assume that carry caused the observed failure.

This is a proposal, not a model patch, parameter search, implemented learning rule,
experimental result, M1 integration acceptance, or scientific promotion. No runtime
was imported and no new model, checkpoint load, trajectory or diagnostic was run for
this document. Existing results and allocations remain unchanged.

## 1. What is established, and what remains open

The [published PR169 result](temporal_reuse_loop_results_20261001.md) reports strong
first-return recall but unsuccessful sustained reuse: in both diagnostic seeds the
assembly arm made 14 correct return predictions, three abstentions, then 15 wrong
predictions through the B-trained assembly. Both ordinary-memory alternatives beat
it on complete return Brier. Freezing weights and delays from initialization improved
Brier but increased abstention; this did not isolate suffix-only plasticity from a
common learned state. That negative conclusion stands.

[PR173](https://github.com/salmonmikan/sparkbrain_research/pull/173) owns the separate
shared-prefix weight/delay-flag diagnostic. Its publicly published preparation at
`5db18164bad1c8cb46976da9e9422f2b0f13b3be` defines the conditional attribution question.
This document uses that question, not an unpublished outcome: it incorporates no
unreleased PR173 raw data, numerical results or evidence package. Any eventual
conditional weight-flag effect would still not identify eligibility carry, a specific
edge, changed spike timing, or assembly selection as its unique mediator.

The newly merged [PR176 ownership result](v05_owned_state_results_20261001.md)
left mature acquired-state abort/commit coverage blocked. This proposal neither
clears that prerequisite nor treats generic copying or a native persisted hash as
complete ownership proof. The intended common-prefix fork needs its own bounded
isolation/continuation checks; the v05 runtime source is unchanged in that merge.

Source inspection is pinned to main `51feb9de68713b864489540602c94b6080784e27`.
Relevant source paths below are relative to `src/sparkbrain/v05/`. Current AGENTS blob:
`b5177647ef4f4b86f2c4208bd5e93008ec0a2d0b`. The active directive index was read at
`ops/human-directives` head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`. This scoped design concerns future stable
learning in a continuous local system; it changes no scheduler or scientific authority.

## 2. Actual current rule

`plasticity.py:48–103` does the following on each `apply` call:

1. Decays every stored edge eligibility by ρ=0.90 per call, not by elapsed milliseconds
2. For a plastic edge with current pre/post spikes, sums signed all-pairs STDP terms Δ
3. Only when current Δ is nonzero, sets e = ρ·e_previous + Δ and, if enabled, changes
   weight by η·reward_trace·e, clipped to [-1.4,1.4], with η=0.001
4. Independently adapts delay toward mean positive pre/post lag when enabled and the
   post-weight-update weight is positive

Thus stored carry does not update inactive edges by itself. The signed current Δ
can cancel; eligible-edge processing can also occur without an actual weight change.
`update_count` is work accounting, not evidence of learning. The carry's interpretation
is restricted to this fixed occurrence cadence; it is not a physical-time credit trace.

`brain.py:154–198` produces spikes, applies plasticity, updates homeostasis, then
extracts patterns and selects the strongest mature assembly. A proposed gate cannot
silently use the later winning assembly as if it were a pre-write context signal.
`assemblies.py:205–278` keeps a candidate's original prototype fixed; its frequency
and episode membership can grow. Drift in generated field patterns is different from
movement of a stored prototype. `prediction.py:12–36` independently learns outcome
counts on the selected mature assembly.

In the published diagnostic, `temporal_reuse_loop_probe.py:341–343` supplies
`reward=None`; brain reward modulation is disabled by default. The multiplier starts
at +1 and relaxes toward +1. These results therefore do not test successful delayed
reward credit assignment. Input novelty and prediction-error fields are zero, although
receptor-internal novelty is computed from activity traces.

## 3. Three concrete mechanisms and their cost of adoption

### A. Context/state-gated learning: plausible, but not the first intervention

Masse, Grant and Freedman (2018) use task-specific sparse activity masks, combined
with synaptic stabilization, to reduce interference. Task identity selects masks;
this does not demonstrate unsupervised context inference. Their mechanism gates
forward activity, whereas an update-only gate here would be a different adaptation.
[Primary paper](https://arxiv.org/html/1802.01569), §§2.2–2.5.

A possible SparkBrain adaptation is a read-only match of current unlabeled spike
patterns to pre-existing mature prototypes before parameter writes, attenuating only
updates on participating familiar edges while leaving unmatched edges plastic. It
would need a nonzero learning floor, explicit behavior for ambiguity/no match, and
separate weight/delay gating in a coupled-system version. Using A/B labels, suffix
names or occurrence IDs as context would leak evaluator information. Protecting an
incorrectly selected familiar route could entrench the exact failure of interest.
The missing reliable pre-write context selector makes this larger than the first test.

### B. Eligibility locality: smallest existing-configuration counterfactual

Izhikevich (2007), equations 1–2, separates a local decaying STDP tag from dopamine-
modulated commitment. The model includes tonic dopamine; it is not simply zero
learning without reward. Bellec et al. (2020), equations 1–4, separate local
neuron-state-dependent eligibility from a neuron-specific learning signal. Neither
paper establishes that removing trace carry improves SparkBrain retention.
[Primary STDP paper](https://www.izhikevich.org/publications/dastdp.pdf);
[primary e-prop paper](https://www.nature.com/articles/s41467-020-17236-y).

The proposed first intervention only sets the existing `eligibility_decay` to 0.0
at the common-prefix fork. This is apply-local, equivalent to occurrence-local
only because the diagnostic wrapper calls apply once per occurrence. Each later
apply keeps current Δ but discards inherited tag mass; the first suffix apply clears
the inherited trace naturally, without a separate pre-fork state reset. No new context oracle, hidden memory, task boundary or supervised field
signal is introduced. This is an occurrence-local STDP hypothesis, not an implementation
of either cited three-factor method. A true outcome-bound tag/commit API would be a
separate change; converting the binary next-event target into a scalar reward would
also change the learning objective and requires its own prospective design.

### C. Consolidation: retain a slow reference without relabeling an activity proxy

Benna and Fusi (2016) couple expressed synaptic strength bidirectionally to slower
hidden variables. A minimal future adaptation could retain one slow reference per
edge: keep live STDP, add a bounded restoring term toward the slow reference, and
move that reference more slowly toward the weight. This can preserve mistakes and
slow useful adaptation too. It requires new serialized state, bounds and a resource
comparison; it does not inherit the paper's multiscale capacity results.
[Author manuscript](https://arxiv.org/abs/1507.07580), published as
*Computational principles of synaptic memory consolidation*.

Synaptic Intelligence instead estimates parameter importance from contributions to
loss reduction and stabilizes important parameters around earlier references.
SparkBrain's field has no such loss-gradient estimator. Spike frequency, |eligibility|
or weight magnitude must not be renamed SI importance. The slow-reference adaptation
is more honest but still larger than deleting cross-occurrence carry.
[Zenke, Poole and Ganguli, 2017](https://proceedings.mlr.press/v70/zenke17a.html),
equations 3–5 in the [primary PDF](https://proceedings.mlr.press/v70/zenke17a/zenke17a.pdf).

## 4. Minimal hypothesis and falsifiers

**H-locality:** conditional on fixed learned delays and live homeostasis, removing
cross-occurrence eligibility carry improves sustained return prediction relative
to the prespecified steady-state attenuation control, while retaining functional
novel-pattern acquisition.

For an edge active on every call with constant Δ, the carry reaches Δ/(1−ρ)=10Δ.
Therefore η×(1−ρ)=0.0001 is a prespecified *steady-state attenuation control*.
It is not exact gain matching for finite runs, a nonzero starting trace, skipped
updates, sign changes or clipping. No gain value may be selected from suffix results. Even if L beats G, this
discriminates only against that specified attenuation; finite-horizon and history-
dependent gain explanations remain unseparated. It cannot establish a universal
locality-specific mediation mechanism.

Four proposed arms, all copied from the same complete prefix state:

| Arm | Weight rule after fork | Eligibility decay | Weight rate |
|---|---|---:|---:|
| C | Current carry | 0.90 | 0.001 |
| L | Current-occurrence learning remains active | 0.00 | 0.001 |
| G | Analytic steady-state attenuation control | 0.90 | 0.0001 |
| Fw | Weight writes disabled; retention reference | 0.90 | 0.001, disabled |

All four freeze delay values at their common-prefix values, leave homeostasis,
receptors, assembly acquisition and count-readout learning active, and leave reward
modulation/action disabled. Do not use `learn_field=False`: it would also disable
homeostatic updates. Change the explicit plasticity config, not just the wrapper's
brain flag, and verify actual changed/unchanged parameter bytes.

This is a conditional weight-rule study. Keeping delay *flags* identically live would
not match delay *trajectories*: changed weights can alter spikes and later lag updates.
That coupled-system question is a separately justified follow-on, not another hidden
arm. No proposed outcome would establish that all plasticity or delay learning is bad.

H-locality is not supported if L fails to improve return behavior, if G explains the
same improvement, if gains are solely wrong-to-abstention conversions, or if L cannot
preserve novel learning/stationary performance. Even successful novel prediction with
Fw would show that assembly/readout learning may suffice; active weight changes alone
would not establish an incremental benefit from field plasticity.

## 5. Proposed bounded future test, not permission to execute

A later prospective protocol should freeze two new diagnostic seeds, source/runner,
input bytes, metric code and exact allocation before any model construction. Proposed
maximum: one 64-occurrence full-S A32/B32 prefix per seed, then independent suffix
forks of 32 occurrences for each of the four arms and three conditions below. This is
128 prefix + 768 suffix = **896 v0.5 prediction/outcome pairs maximum**, with no retry,
reproduction, extra trajectory or parameter grid. Stop rather than search if invalid.

Use the published PR169 pulse timing/amplitude/query and receipt boundaries, with
fresh prospectively frozen distractor/jitter bytes shared across arms:

- **Return:** 32 A cues, testing sustained retention after intervening B
- **Stationary:** 32 B cues, checking continued performance without a context switch
- **Novel acquisition:** 16 each of two new raw orders, A,C,F and C,A,F, at the same
  cue-time multiset; outcome mapping 0/1 fixed in advance. Use a prospectively frozen
  balanced order. The old cues are A,F,C and C,F,A; no new channel, hidden regime
  marker or increased input information is added

Unseen raw order does not guarantee an initially incorrect internal representation.
If the novel condition is already at ceiling or imposes no measurable acquisition
demand, report its learning-capacity conclusion as inconclusive; do not redesign it
based on its results. A new raw order also does not establish broad generalization.

For a later *benefit* comparison, include unchanged recent-memory H and retained-
prototype R from the published diagnostic with equal input/outcome access. Two arms
× two seeds × (64 prefix + three 32-row suffixes) adds **640 ordinary-memory pairs**,
for **1,536 total pairs maximum**. Each H/R arm forks its three suffixes
independently from its own completed 64-row prefix. This accounting is part of the proposed ceiling,
not authority to execute. No outcome-marginal-only comparison can justify superiority.

Required observations and guards (use the allocated trajectories or source/static
checks; extra runtime probes are outside this ceiling and need separate prospective
accounting before any execution):

- Predict before each later outcome. Keep receipt idempotency and occurrence-ID
  renaming invariance; no evaluator label or suffix marker reaches the model
- Prove restricted quiet-prefix restore eligibility and complete shared-prefix
  identity without silently repairing omitted transient caches. PR172's M1 loader
  result does not validate this different v05 checkpoint path
- Within the four v05 arms, verify identical first-suffix predictions from identical
  prefix/input state before
  divergent updates can affect a later occurrence. Hash and disclose every intended
  config change; hashes need not remain equal after the interventions
- Report all-row Brier including abstention, correct/total, correct/non-abstaining,
  coverage, selection identity, and wrong-to-abstention versus wrong-to-correct changes
- Keep the count-probability adapter and native confidence distinct. Report fixed
  probability-bin counts and empirical outcomes; do not tune a confidence threshold
  or call a small-bin diagram established calibration
- Report novel learning curves and stationary/return outcomes separately, including
  the first prediction and fixed early/late windows. Require meaningful acquisition
  evidence before calling learning capacity preserved
- Record actual per-edge weight/delay changes, clipping, proposed current Δ versus
  carry contribution, cumulative absolute update mass, spikes, assemblies and count
  updates. Do not substitute `update_count` for parameter learning
- A return-only win cannot pass. Before execution, freeze numeric improvement and
  non-inferiority margins for return, stationary, novel acquisition and coverage,
  plus how ceiling/abstention cases are classified. None is selected in this document
- Predefine driver and worker CPU/wall/RSS/output limits, STARTED/no-clobber behavior,
  preserved incomplete rows and a separate result package. Include observer overhead
  and every prefix/fork call. No runtime network dependence or cloud model is needed

The exact seeds, balanced sequence bytes, numeric decision margins, resource caps,
source-checked runner and independent review remain prerequisites. This intentionally
is a bounded design outline, not an execution-ready preregistration.

## 6. Search, provenance and completion

Focused primary-source searches on 2026-10-01 used “context-dependent gating synaptic
stabilization”, “STDP dopamine distal reward”, “eligibility learning signal recurrent
spiking e-prop”, “synaptic memory consolidation”, and “synaptic intelligence”. Primary
full texts or author manuscripts were checked, including the cited rule equations.
This is not a systematic novelty review, and no absence/novelty claim follows.

Source SHA-256 pins:

- plasticity.py: `3729e6f9556382988441116240ca0fa36897048b56e7e789a7ff453b444c3429`
- brain.py: `d11680e60ebd7d3301a81a1e0e6ffddf39f2d1707843892c241b0865734439c9`
- assemblies.py: `f2dc1b7bbe71fb70ea27bb661111dca2d68ebfeb3e6044e4ec221120d7d12394`
- prediction.py: `dcd8f45ba4cd1a0478685bf7f8f9764aeed135820f29d5b3381111631345e169`
- receptors.py: `4071d0d5d2f0ab487e3324528053997ecbdeb65953bfa211312d0da918c75942`

This report's completed work is literature/source comparison and hypothesis design.
No experimental acceptance criterion is claimed met. No production code, scientific
claim grade, consumed identity, scheduler state or blocked publication is altered.
