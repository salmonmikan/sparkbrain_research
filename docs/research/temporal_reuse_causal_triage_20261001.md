# PR169 temporal-reuse failure: source/trace triage and proposed next diagnostic

Status: read-only retrospective analysis, 2026-10-01. **No new diagnostic model execution.** The linked next protocol is a proposal, not a frozen or executed experiment. No scientific credit, formal identifier, runtime edit, threshold selection, or revision of PR169's negative result is requested by this document.

## Bottom line

The full v0.5 model initially remembers the returning A cue correctly. Its failure is a later change in the internal spike pattern that routes A to an old B-trained prototype. The readout then confidently inherits that prototype's B history. Frozen-plasticity F has lower loss largely because internal firing becomes too sparse to form a pattern, causing abstention. Neither result establishes a useful recurrent assembly mechanism or superiority to ordinary memory.

The most useful next bounded test is to start all four branches from **the same full-model prefix checkpoint** and vary only suffix weight-learning and delay-learning flags in a 2×2 design. This repairs the causal ambiguity in the existing whole-history S/F comparison. It would diagnose the failure, not rescue or promote the earlier result.

## Evidence and audit boundary

- Source/protocol/runner pin: [`0bcb2c1b23c29e5107111343a757c57c1f7bbb41`](https://github.com/salmonmikan/sparkbrain_research/commit/0bcb2c1b23c29e5107111343a757c57c1f7bbb41), PR169
- Durable evidence/report pin: [`b6a872642df6889e9c6ce82148a5a2430db2c114`](https://github.com/salmonmikan/sparkbrain_research/blob/b6a872642df6889e9c6ce82148a5a2430db2c114/docs/research/temporal_reuse_loop_results_20261001.md)
- Retained raw directory: `temporal-reuse-loop-diagnostic-20261001T1745Z`
- Retained manifest SHA-256: `f224981074dde62b0f3c9a4d9b075714140c83ac1476533d70580e281c6b2b05`
- All **232 files named by the retained manifest** were hashed successfully. This is integrity relative to that manifest, not an independent timestamp or a claim that its closure files are covered
- Eleven inspected source files were checked byte-for-byte against the pinned Git objects; hashes are in `SOURCE_PROVENANCE.json`
- `scripts/audit_temporal_reuse_saved_traces.py` imports only Python's standard library. It independently calculates similarity components, candidate creation/maturity, selection, count-readout probabilities/confidence, and final candidate/readout state for all **256 saved S/F suffix rows**. It also recomputes the Q/H/R metrics from **384 saved rows**. It never imports the driver, SparkBrain, or a model checkpoint loader
- `TRACE_AUDIT.json.gz` (decompressed JSON) contains the complete arithmetic, exact row indices, internal spike records, score components, changed edge parameters, and endpoint checks. `TRACE_AUDIT_RUN.log` is its execution log. Five focused synthetic auditor tests and Ruff pass.

The audit reconstructs already recorded decisions. It does not establish a counterfactual outcome under a different runtime, and does not claim to validate every possible matcher input or all original experiment guards.

## 1. Where the loss comes from

Return-A suffix, 32 predictions per seed. S means full learning; F disables weight and delay learning throughout both prefix and suffix. Abstentions have p1=0.5 and remain in Brier loss.

| Arm | Seed 910071: correct / abstain / wrong | Brier | Seed 910072: correct / abstain / wrong | Brier |
|---|---:|---:|---:|---:|
| Full S | 14 / 3 / 15 | 0.31180644 | 14 / 3 / 15 | 0.31180644 |
| Frozen F | 10 / 22 / 0 | 0.17750123 | 12 / 20 / 0 | 0.15652362 |
| Raw history H | 30 / 0 / 2 | 0.0725 | 30 / 0 / 2 | 0.0725 |
| Raw reuse R | 28 / 4 / 0 | 0.06415166 | 26 / 6 / 0 | 0.07765357 |

For each S seed, the 14 correct predictions contribute 0.00030519 to mean Brier, the three abstentions contribute 0.0234375, and the 15 wrong predictions contribute **0.28806374**, about 92.39% of the total. This is a late-routing failure after initial successful recall, not a failure to retain any A-associated memory.

F is not an adaptation success: **19/32 return rows in each seed contain exactly one internal spike**, below the two-spike minimum, so no pattern exists. The remaining abstentions are immature candidates or a mature candidate with no learned outcome. S produces three to five internal spikes per return row. The original negative gate remains failed.

## 2. Source-mapped explanatory chain

### A. The input cue survives receptor emission

On every one of the 256 S/F suffix rows, A, F, C, and Q appear in the emitted receptor output, and each has exactly the original input timestamp. Their internal representation can still be distorted downstream. This observation excludes dropped cue channels or shifted receptor timestamps as the explanation for these rows; it does not establish that perception is generally correct or that receptor gain/state is irrelevant.

Source: [`brain.py:145–175`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/brain.py#L145-L175), [`receptors.py`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/receptors.py).

### B. The current pattern changes; existing prototypes do not drift

The A prototype is fixed at ordered units `[63,45,56]`, relative bins `[0,13,14]`. The old B prototype is `[56,45,63]`, bins `[0,0,4]`. Matching updates occurrence/episode bookkeeping but never averages or replaces an existing prototype.

For both full-model seeds:

- Return indices 0–13 select old A `assembly-0001`
- At index 14, `[45,56,63,45]` has maximum existing score 0.525, below the frozen 0.66 threshold. It creates `assembly-0004`
- Indices 14 and 15 abstain because that candidate is immature. At 16 it becomes mature, but has no prior outcome count yet, so still abstains; its first A count is learned afterward
- At index 17, the first two internal spikes swap order, yielding `[56,45,63,45]`. The old B prototype wins and continues to win all remaining return rows

At index 17, independently reconstructed scores are:

| Candidate | Seed 910071 | Seed 910072 |
|---|---:|---:|
| Old A `0001` | 0.387500 | 0.387500 |
| Old B `0002` | **0.730193** | **0.742470** |
| Old B-related `0003` | 0.387500 | 0.387500 |
| New A-like `0004` | 0.632052 | 0.680760 |

In seed 910071, the first two index-16 spikes occur at 10.141186 and 10.146370 ms after cycle start, ordered 45 then 56. At index 17 they occur at 10.145465 and 10.156961 ms, ordered 56 then 45. Both are in relative timing bin zero. The matcher nevertheless preserves exact spike order in its edit-distance term. Its score is 0.55×order similarity + 0.25×unit-set similarity + 0.20×timing similarity. In the index-17 example, B gets order similarity 0.75 while new candidate 0004 gets 0.5. This is a concrete sub-bin order sensitivity in the current contract, not a newly established defect or permission to change the contract.

Source: [`assemblies.py:18–83`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/assemblies.py#L18-L83), [`assemblies.py:86–149`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/assemblies.py#L86-L149), [`assemblies.py:208–280`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/assemblies.py#L208-L280).

### C. Confidence and historical readout amplify wrong routing

At the fork, old B `0002` has 25 B outcomes and no A outcomes. When returning A first routes there, native prediction is B with confidence 1.0; the scoring adapter produces p1=26/27=0.962963. The 15 subsequent A receipts do update that same readout. Its final counts are A=15, B=25. Before the last receipt p1 is 26/41=0.634146, so all 15 predictions remain wrong.

Native confidence is the winning outcome count divided by total counts; it does not incorporate pattern similarity or ambiguity between candidates. Thus the high confidence is exactly explained by inherited label history, despite newly changed input-to-prototype routing. This is readout inertia conditional on the observed routing. It does not establish that a different readout alone would restore useful representations. The Laplace-smoothed scoring adapter is not a calibrated uncertainty model.

Source: [`prediction.py:13–34`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/prediction.py#L13-L34), [`temporal_reuse_loop_probe.py:263–286`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/scripts/temporal_reuse_loop_probe.py#L263-L286).

### D. Field plasticity is implicated but not yet isolated

S changes weights on seven edges during return. Exact serialized endpoint delays also differ on all seven, although two delay differences are only floating-point-scale (about 4.35×10⁻¹⁴ and 1.18×10⁻¹⁴ ms). All seven changed edges originate in receptor units and terminate at units 45, 56, or 63. F changes neither weights nor delays. However, F was already trained with those learning flags disabled, so its fork state, prototypes, counts, field parameters, and firing regime differ from S before the suffix begins. S/F therefore cannot identify a causal effect of *suffix-only* plasticity.

Homeostasis and receptor adaptation remain active in both arms. In particular, `learn_field=False` would also bypass homeostatic updates, so it is not a clean substitute for disabling only weight/delay learning. Source execution order is receptor → field spikes → plasticity → homeostasis → pattern/matcher → prediction. Current-step plasticity cannot retroactively change its already-computed spikes; it can affect future steps. The raw results do not identify weight learning, delay learning, homeostasis, jitter, or their interaction as the unique origin of the order reversal.

Source: [`brain.py:74–103`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/brain.py#L74-L103), [`brain.py:154–200`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/brain.py#L154-L200), [`plasticity.py`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/plasticity.py), [`homeostasis.py:35–60`](https://github.com/salmonmikan/sparkbrain_research/blob/0bcb2c1b23c29e5107111343a757c57c1f7bbb41/src/sparkbrain/v05/homeostasis.py#L35-L60).

## 3. What this says about assembly causal value

The audited suffix internal firing population is confined to units 45, 56, and 63 (F return uses only 45 and 63). The frozen topology has **no connections among those firing internal units**. The topology has recurrent connections elsewhere, and they receive propagated activity, but none of those other internal units fires in these audited suffix trajectories. Consequently this fixture does not demonstrate recurrently sustained collective firing among the active units. Its measured predictive memory is an acquired internal-pattern prototype bank plus outcome counts.

The existing target-suppression result establishes dependence on that selected representation/readout path in the tested forks. It cannot by itself distinguish assemblies from an ordinary prototype memory: disabling a useful ordinary-memory entry can also impair prediction. Moreover, in the full-S arm, the matched B candidate was not selected on the intact B probe shams, so its suppression is an inactive control there. This does not apply uniformly to F, whose matched candidate is selected on 5/8 and 2/8 B shams. A lower B loss after target suppression can mean a wrong confident prediction became an abstention, not that B was correctly recognized.

The operational question remains: does the internal dynamical representation deliver robust, resource-accounted prediction or reuse better than raw history/prototypes? On this frozen fixture, it does not. A future positive claim needs active matched controls, a comparable ordinary-memory entry intervention, and preserved coverage/accuracy as well as loss. Activity counts alone must not be described as energy efficiency.

## 4. What external research changes about the next test

This is a targeted primary-source check on 2026-10-01, not a systematic novelty
review. The searches were `Izhikevich 2006 Polychronization computation with spikes
pdf`, `Dohare 2024 loss of plasticity deep continual learning Nature`, and
`Gneiting Raftery 2007 strictly proper scoring rules prediction estimation pdf`.
The papers constrain interpretation; none validates SparkBrain's mechanism.

1. **Temporal groups require a dynamical account.** Izhikevich's
   [*Polychronization: Computation With Spikes*](https://www.izhikevich.org/publications/spnet.pdf),
   *Neural Computation* 18, 245–282 (2006), studies reproducible asynchronous
   patterns produced by conduction delays and STDP. The author's
   [implementation page](https://www.izhikevich.org/publications/spnet.htm) also
   provides a shuffled-connectivity comparison. Here, matching a stored ordered
   spike sequence is not sufficient to establish an analogous causal group:
   the audited suffix firing internal units have no edges among them. The concrete
   implication is to retain connection-level timing/weight changes and keep
   prototype routing separate from recurrent contribution. This does not imply
   that delay learning in SparkBrain implements the paper's mechanism.
2. **Continued learning can fail in more than one way.** Dohare et al.,
   [*Loss of plasticity in deep continual learning*](https://www.nature.com/articles/s41586-024-07711-7),
   *Nature* 632, 768–774 (2024), distinguish impaired learning on new tasks from
   forgetting old examples and examine internal activity alongside performance.
   Their backpropagation networks are different from this local STDP-like
   substrate. The applicable lesson is diagnostic separation: S's late
   wrong-route predictions and F's sparse-firing abstentions are different
   outcomes. The short A-return fixture does not establish the paper's
   long-horizon loss-of-plasticity phenomenon, and its remedy is not imported.
3. **A proper score does not identify a mechanism.** Gneiting and Raftery,
   [*Strictly Proper Scoring Rules, Prediction, and Estimation*](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf),
   *JASA* 102, 359–378 (2007), supply the probability-forecast evaluation
   rationale for quadratic/Brier scoring. Our inference is narrower: the
   observed reduction in Brier must be decomposed into correct predictions,
   wrong predictions and abstentions before it is called useful reuse. Native
   count confidence and the scoring adapter remain distinct; neither is
   established as calibrated by this two-seed analysis.

Together, these sources motivate the proposed factorial diagnosis and richer
state traces, not a runtime redesign or positive assembly claim. The connection
to the integrated project goal is useful experience-dependent prediction in a
continuous loop. A v0.5 diagnostic remains a component result; no capability is
thereby added to the M1 runtime.

## 5. Proposed next diagnostic

The separate [shared-prefix weight/delay protocol](shared_prefix_plasticity_protocol_20261001.md) fixes prospective endpoints, matched controls and a bounded budget. It is unexecuted and requires independent source review and a distinct runner/input freeze before any dynamics.

## Reproduce this read-only analysis

See the [artifact README](../../artifacts/research/temporal_reuse_causal_triage_20261001/README.md) for pinned input reconstruction, the zero-model-call auditor and retained output hashes.


## Publication verification

Independent source/data review reproduced the complete audit byte-for-byte and
checked all consumed-input manifest membership and eleven source blobs. Its four
corrections are included: exact delay differences versus floating-point scale,
full-S scope of the inactive B control, exclusive-output wording, and the proposed
successor's quiet-boundary eligibility gate. The amended package had no remaining
review blockers; this does not clear an unimplemented successor runner to execute.

Cloud CPU validation on Python 3.12.14:

- `python -m pytest -q tests/test_temporal_reuse_saved_trace_audit.py`: 6 passed
- Configured `python -m pytest -q`: 687 passed, 392 scientific/reproduction/external
  tests deselected; one existing Starlette/httpx deprecation warning
- `python -m ruff check .`: pass
- `python scripts/local_readiness_check.py`: pass
- `python scripts/run_demo.py`: pass, 7 trace frames
- `python scripts/run_benchmark.py --episodes 40 --steps 30`: pass, 240 episode rows
- `python scripts/validate_bundle.py`: pass, 88 required files

These standard engineering tests/smokes are separate from the data-only triage:
no PR169 diagnostic or prospective 910073/910074 trajectory was run again or
executed for this publication. The future protocol remains a proposal.


A subsequent GitHub Codex review identified that the published auditor reads
prefix checkpoints but does not reconstruct prefix spike populations. The firing
population/topology claim above is therefore restricted to audited suffixes.
No prefix-population verification is claimed by this published auditor; this
wording correction changes neither retained arithmetic nor the negative result.
