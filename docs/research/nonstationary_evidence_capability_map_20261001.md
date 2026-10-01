# Temporal evidence identity and the continuous SparkBrain loop

Status: **LITERATURE / SOURCE AUDIT / EXPLORATORY / NON_EVIDENTIARY**. Scientific credit: **0**.
Date: 2026-10-01 UTC. Runtime/source pin: `3cb955cd42474b36d2d37617e5390d08656c06f1`.
Human Directive index: `ops/human-directives:ops/human_directives/active.md`,
blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, read 2026-10-01 UTC.
No model, new diagnostic, or runtime test was executed for this report.

## Decision and connection to the goal

The ultimate goal is a mathematically specified, falsifiable computational theory of
Spark-based dynamic cognition, with a corresponding inspectable local/offline implementation.
It must connect persistent state and learning from sequential experience to prediction
or action. A
guard, router, provenance ledger, or change detector is a prerequisite or comparator,
not the goal itself. The [project charter](../PROJECT_CHARTER.md) calls for continual
adaptation, belief revision, matched alternatives, and causal inspection. The
[v0.5 plan](../V05_MASTER_PLAN.md) further asks whether unlabeled temporal experience
forms reusable assemblies whose selective intervention changes functional performance.
This report establishes none of those outcomes.

The current integration priority is the continuous loop in
[HUMAN-20260928-001](https://github.com/salmonmikan/sparkbrain_research/blob/ops/human-directives/ops/human_directives/history/2026-09-28/HUMAN-20260928-001-accelerated-integrated-sparkbrain-completion.md):
observation, persistent state, competing hypotheses/scopes, selection or abstention,
prediction/action, later outcome, selective revision, and the next prediction/action.
Interface gaps take priority over unrelated mechanism searches. Engineering completion,
functional benefit, causal contribution, and novelty remain separate conclusions.

The existing
[2026-09-25 advisory](https://github.com/salmonmikan/sparkbrain_research/blob/ops/human-directives/ops/human_directives/history/2026-09-25/HUMAN-20260925-001-advisory-v2-predictive-state-research.md)
already proposes learning when to update, separate, or reuse predictive states and calls
for an identifiability/input-access/comparator design first. It is an unvalidated
assistant-origin proposal with no execution authority of its own. This report narrows
one interface question within that direction; it does not introduce a new idea, reopen
a consumed research object, or supply scientific execution authorization.

The immediate useful question is therefore: **what information must cross the
observation–outcome interface for the loop to distinguish a repeated message, a new
occurrence, corrected evidence, and a changed or hidden context?** Removing an integrity
guard or adding a tiny feature offset cannot answer all four questions.

## What the present contract actually distinguishes

Pinned code links identify source facts, not new experimental results:

- M1 binds a fresh `event_id` to an observation and a `receipt_id` to its outcome.
  An identical committed receipt returns its previous revision; a conflicting receipt
  is rejected. Only one observation may remain pending at a time.
  [M1 observation/receipt handling](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L391-L468)
- SB002 separately hashes the routing-feature vector. Once that exact vector is bound
  to one candidate, a fresh evidence ID with another candidate is rejected by
  `identical_observation_conflict`. This is an intentional consistency contract.
  [SB002 identity checks](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/causal_scope_revision.py#L540-L613)
- M1 maps outcome sign to alpha/beta and passes the pending routing features to SB002.
  A scope rejection rolls back the integrated outcome transaction. Agreement between
  the predictive and scoped components is required to act.
  [Outcome integration](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L452-L526)
  and [selection](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L407-L440)

The existing [exploratory eight-case M1 report](https://github.com/salmonmikan/sparkbrain_research/blob/e806cab791d0a69da79cd41127826a10f64a53e1/docs/EXPLORATORY_M1_OUTCOME_IDENTITY.md)
records exact reversals rejected and
`0.000001` routing-only near-alias reversals accepted on the same route, followed by
abstention under tied supports/competing predictions. This report inspected that earlier
report, not a new run. Its publication is owned by the separate
[PR #167 workstream](https://github.com/salmonmikan/sparkbrain_research/pull/167),
and the linked result was read back at its complete publication pin
`e806cab791d0a69da79cd41127826a10f64a53e1`. That PR's initial source-only head
`93c7a05d6af5d69dc842d10619fe0821819d0122` is not the executed result.
The result is contextual prior exposure, not independent confirmation here;
its publication does not imply merge, CI completion or scientific acceptance.

Consequently, the eight cases establish a narrow identity boundary, not a general defect,
successful adaptation, or inability of all SparkBrain paths to learn. Historical SB002
and M1 acceptance is not reclassified. The present report proposes no production change.

## Four different problems that must not be collapsed

| Problem | What the incoming record means | Needed distinction | What success would show |
|---|---|---|---|
| Duplicate delivery | The same occurrence/receipt arrives again | Occurrence and receipt identity | No extra learning weight or state change |
| Evidence correction | A previously recorded observation/outcome is amended | Revision lineage and explicit supersession policy | Audit trail retained; original and correction not counted as independent occurrences |
| Temporal change | A later, genuinely new occurrence has a different conditional outcome law | New occurrence identity plus causal history/change inference | Adaptation after informative later evidence, with stationary false-switch controls |
| Perceptual aliasing | Different hidden states share the same current observed features | Informative past observations/actions/outcomes, when available | Distinct predictions from permitted history, without supplied regime labels |

Different values do not prove different occurrences; equal values do not prove the same
occurrence. A fresh event identifier prevents record collision but does not reveal the
world's latent context. A changepoint estimate does not automatically establish that an
earlier context has returned. Abstention is valid when the allowed evidence cannot decide.

## Primary-source comparison

Retrieval date for all sources: 2026-10-01 UTC. This is a focused comparison, not a
systematic novelty search. No source implementation was downloaded, executed, or copied.

### 1. Hidden state / history-dependent identification

R. Andrew McCallum, *Instance-Based State Identification for Reinforcement Learning*,
Advances in Neural Information Processing Systems 7, NIPS 1994.
[Publisher record](https://papers.nips.cc/paper/1994/hash/d2ed45a52bc0edfa11c2064e9edee8bf-Abstract.html)
and [full paper](https://papers.nips.cc/paper_files/paper/1994/file/d2ed45a52bc0edfa11c2064e9edee8bf-Paper.pdf).
No DOI or arXiv identifier is supplied by the inspected publisher record; no exact
day of publication was verified. Full text retrieved; pp. 377–380 inspected.

**Actual source claim:** current percepts can alias states requiring different actions;
Nearest Sequence Memory retains experience sequences and uses history matching to
disambiguate them. Keeping raw experience avoids irreversibly assigning data to an
incorrect initial state partition.

**SparkBrain inference:** a current-feature-only route is not itself a learned
history-dependent state. A history-aware comparator should precede an adaptation claim.
The paper does not prove that arbitrary hidden states are identifiable or that M1 is
defective. It is a direct precedent, not a source of SparkBrain novelty.

### 2. Online distribution change

Ryan Prescott Adams and David J. C. MacKay, *Bayesian Online Changepoint Detection*.
Preprint `arXiv:0710.3742v1`, submitted **2007-10-19**.
[Record](https://arxiv.org/abs/0710.3742v1),
[arXiv DOI](https://doi.org/10.48550/arXiv.0710.3742),
[full paper](https://arxiv.org/pdf/0710.3742). Full text retrieved; §§1–2 inspected.

**Actual source claim:** recursive inference maintains a posterior over time since the
last changepoint and combines run-conditioned next-observation predictions. Its model
uses independent segment parameters and conditionally IID observations within segments.

**SparkBrain inference:** run-length uncertainty is a principled small comparator for
abrupt temporal drift. It is not by itself a mechanism for recognizing and reusing a
previous context, correcting duplicate records, or learning causal assemblies. A toy
Bernoulli adaptation would be our implementation choice, not a reproduced paper result.

### 3. Change detection, policy adaptation and reuse

Lucas N. Alegre, Ana L. C. Bazzan and Bruno C. da Silva, *Minimum-Delay Adaptation in
Non-Stationary Reinforcement Learning via Online High-Confidence Change-Point Detection*.
AAMAS 2021, pp. 97–105; conference **2021-05-03–07**; `arXiv:2105.09452v1`
submitted **2021-05-20**.
[Record](https://arxiv.org/abs/2105.09452v1),
[arXiv DOI](https://doi.org/10.48550/arXiv.2105.09452),
[full paper](https://arxiv.org/pdf/2105.09452). Full text retrieved; §§2–4 inspected.

**Actual source claim:** MBCD couples context-change statistics with a library of
probabilistic dynamics models and policies, supporting new-context learning and reuse
when contexts recur. Its delay/false-alarm analysis relies on the stated likelihood and
change-detection assumptions; the implementation uses Gaussian predictive models.

**SparkBrain inference:** adaptation, context separation and reuse require separate
tests. The paper is a close known alternative for this goal. Its theoretical guarantees
must not be transferred to a different heuristic, unknown miscalibrated likelihoods,
or this report's unexecuted diagnostic.

### 4. Provenance and versioned evidence

Luc Moreau and Paolo Missier (editors), *PROV-DM: The PROV Data Model*.
W3C Recommendation **2013-04-30**, an official standard rather than an experiment.
[Dated normative source](https://www.w3.org/TR/2013/REC-prov-dm-20130430/),
[revision §5.2.2](https://www.w3.org/TR/prov-dm/#term-Revision),
[value §5.7.2.5](https://www.w3.org/TR/prov-dm/#term-value).
No DOI/arXiv identifier applies to this cited standard.

**Actual source claim:** revision is a derivation relationship; different entities may
have equal values, including entities generated by different activities.

**SparkBrain inference:** preserve an occurrence identifier separately from feature
content, and preserve correction lineage separately from fresh evidence. PROV does not
specify Bayesian independence, learning weights, supersession rules, or an RL algorithm.
Those would need an explicit application contract.

## Minimal next deliverable: an offline information-access contract

**Proposed only; not an execution preregistration and not an M1 repair.** Before writing
another runner, decide whether the intended next capability is temporal adaptation,
hidden-context separation, or recognition of a returning context. Each needs different
information and comparisons. Do not silently pick the easiest positive demonstration.

A useful bounded contract would supply identical data to three small offline reference
models: current-observation-only, history-aware prediction, and a time-change model.
The first is a limitation reference, not the strongest scientific baseline. A later
comparative claim needs an appropriate reuse-capable alternative and matched resources.
All models would predict before receiving the target outcome; no true regime IDs,
episode-boundary labels, future suffixes, or evaluator fields would enter model input.

The contract should first enumerate these four paired controls:

1. **Stationary distribution, repeated features:** new occurrences may legitimately
   differ in outcome. Separately inject exact duplicate deliveries; they must have zero
   incremental weight. This distinguishes stochastic evidence from transport integrity.
2. **Abrupt conditional change, unchanged current features:** preserve causal order and
   report post-change loss and false switches in the stationary control. No claim of
   anticipating the first unannounced change is possible from an identical prefix.
3. **Stationary hidden-context aliasing with an informative history cue:** the current
   feature is equal across contexts while a permitted earlier cue differs. Compare with
   a cue-removed paired control. Require loss only of the cue-specific incremental gain
   unless the complete allowed prediction-time prefix, including past actions/outcomes,
   is verified conditionally uninformative about the target. Removing one cue alone
   cannot justify requiring loss of every history-dependent advantage.
4. **Record correction:** mark a new record as revising an existing occurrence. Keep the
   raw history, define whether old estimates are recomputed, and verify no double count.

This differs from PR #167: it asks whether the available information and record semantics
can support the intended task, rather than probing M1's exact-versus-near-alias boundary.
The first output should be a prefix-collision/access table and explicit model contracts,
not a headline score. Fix stream budgets, seeds, parameters, scoring, memory limits,
duplicate/correction policies and stopping rules before executing any version. Preserve
negative and unidentifiable cases; do not add cues after seeing failure and call the
same result confirmatory.

**Go/no-go:** continue to a bounded offline diagnostic only if its outcome would decide
an integration interface or a specific fresh research question. Otherwise stop here.
Even a successful diagnostic would establish neither SparkBrain-specific causal benefit
nor assembly formation. Those require the functional reuse and matched intervention
tests in the broader goal.

## Scope and verification

Only this dedicated report is added. Runtime, defaults, shared status/result/claim ledgers,
scheduler/control-plane state, accepted historical contracts and formal identities are
unchanged. PR #164 and PR #167 branches are not modified. No package, schema, evidence
grade, or historical acceptance change is proposed.

Validation for this source-only artifact is source-link/path checking, whitespace/diff
checking and independent report review. Runtime tests and benchmarks are not represented
as executed. The report's source pin deliberately remains fixed if `main` later moves.
