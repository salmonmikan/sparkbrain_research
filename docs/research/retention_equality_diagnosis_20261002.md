# Why changed weights produced identical retained predictions

2026-10-02 UTC. **POST-HOC / DATA-ONLY / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit 0. No model import, construction, transition, alternate input,
training, threshold search or original-result rescoring was performed.

## Decision

**Continue the real learned-state-to-M1 ownership/transaction gate before launching
another parameter search.** Existing traces already localize the L/Fw and L/G return
ties: continuous drive/potential changed, but the recorded discrete spike trajectory
and downstream representations did not. The result is neither universal weight
irrelevance nor evidence that the weight updates improved prediction.

The [audited retention result, PR186](https://github.com/salmonmikan/sparkbrain_research/blob/f382c2734e72aef3a7393c5aa117fa69047f1dde/docs/research/plasticity_retention_results_20261002.md)
remains a valid bounded execution with a failed predefined support gate. This additive
diagnosis does not revise its scores, criteria, raw files, consumed identity or claims.

## What the retained records show

The [derived diagnosis](../../artifacts/research/retention_equality_diagnosis_20261002/diagnosis.json)
compares all 32 rows in each selected branch, with exact paired input/occurrence/outcome
checks. Eight comparisons cover both fixtures: L/Fw return, L/G return, L/Fw novel,
and L/C return. These are reused, correlated development observations, not eight new
experiments or independent replications.

For every L/Fw comparison, in both return and novel conditions:

- L records **224 nonzero weight writes** across seven edges; Fw records zero. Neither
  arm records clipping in the inspected apply rows
- The first row's complete spike records match. On each subsequent row, exactly the
  fired units 45, 56 and 63 differ in excitatory drive and potential before reset
- Nevertheless, **all 32 spike unit/time sequences match exactly**, as do all patterns,
  assembly activations, selected assembly IDs, native predictions and probabilities
- Every pre-receipt and post-receipt readout count table matches exactly
- Serialized final assemblies, predictor, receptors and homeostasis match exactly. In the final
  field-unit records, only `excitatory_drive` differs, at units 45, 56 and 63

L/G return comparisons show the same event/representation/output equality and the
same 93 changed spike-potential records. G also makes 224 nonzero, unclipped writes.
The two arms' total absolute writes are close but not identical: approximately
0.16956 versus 0.16547 for fixture 910075, and 0.16939 versus 0.16529 for 910076.
G remains the registered analytic attenuation reference, not a retrospectively
certified finite-history dose match.

### Logged firing margins and amplitude differences

Margins below are only `potential_before_reset - dynamic_threshold` at already
recorded spikes of units 45/56/63, a post-hoc subset comprising the observed eligible
update-edge targets. They do **not** describe silent arrivals,
refractory arrivals, missing spikes or counterfactual thresholds. No additional
model state was reconstructed. Display values are rounded; the JSON retains floats.

| Fixture / condition | Minimum L firing margin | Minimum Fw firing margin | Maximum paired potential difference |
|---|---:|---:|---:|
| 910075 return | 0.422998 | 0.386674 | 0.0465454 |
| 910076 return | 0.418997 | 0.382714 | 0.0462390 |
| 910075 novel | 0.0252378 | 0.0215394 | 0.0459636 |
| 910076 novel | 0.501886 | 0.463235 | 0.0458915 |

These extrema need not occur on the same event and must not be used as an inferred
robustness bound. The direct observation is that the actual weight-associated
continuous changes **did not cross discrete event boundaries in these comparisons**.

### The stronger C perturbation does leave that trajectory

Both return fixtures first differ between C and L in spike unit/time sequence and
patterns at zero-based index 10; index 12 also differs. The selected assembly and
prediction first differ at index 14 and then differ for all remaining 18 rows.
Thus, changed spikes at indices 10/12 were initially absorbed by later processing;
the experiment is not completely insensitive to weight-treatment differences.

A concrete recorded index-14 example, fixture 910075:

- C's internal pattern is units `[56,45,63,45]`, bins `[0,0,17,34]`; it selects
  assembly-0002, native label 1, p1 approximately 0.962963
- L's pattern is `[63,45,56]`, bins `[0,11,17]`; it selects assembly-0001,
  native label 0, p1 approximately 0.0217391
- The recorded outcome is 0 in both paired rows

C's return absolute writes total approximately 1.49272/1.51834 across the two
fixtures, versus L's 0.16956/0.16939. C records no clipping in these rows either.
This is an exposed descriptive contrast, not a newly preregistered proof that a
particular edge, threshold or learning-dose law caused the performance difference.

## Source-backed explanation and its limits

Frozen execution source is `81088ae386cbc611fb9e6366d8ade1c2ea74b6b7`.

1. **Writes follow the current occurrence's spikes.**
   [`v05/brain.py:151–175`](https://github.com/salmonmikan/sparkbrain_research/blob/81088ae386cbc611fb9e6366d8ade1c2ea74b6b7/src/sparkbrain/v05/brain.py#L151-L175)
   finishes pulse ingestion before `plasticity.apply`. Patterns and prediction use
   those already-produced spikes. A row's positive writes cannot directly explain
   an improvement of that same row's prediction; their dynamical opportunity is later
2. **Learned weights are connected to propagation.**
   [`v04/field.py:256–266`](https://github.com/salmonmikan/sparkbrain_research/blob/81088ae386cbc611fb9e6366d8ade1c2ea74b6b7/src/sparkbrain/v04/field.py#L256-L266)
   schedules arrivals with `current=edge.weight`. The changed drive/potential at
   active target units rules out the blanket diagnosis that the changed weights have
   no observable field effect. It does not identify each edge's individual causal effect
3. **Event generation discards continuous amplitude differences.**
   [`v04/field.py:219–246`](https://github.com/salmonmikan/sparkbrain_research/blob/81088ae386cbc611fb9e6366d8ade1c2ea74b6b7/src/sparkbrain/v04/field.py#L219-L246)
   ignores positive current during absolute refractory periods, emits no spike below
   threshold, and resets potential after emitting a spike. For the same presynaptic
   spike times, fixed delays preserve candidate arrival times. Different drives can therefore yield the same event
   sequence. The retained equality supports this location of insensitivity; absent
   nonfiring-arrival records prevent attributing every erased change to threshold
   margin versus refractoriness
4. **The representation omits potential and drive.**
   [`v05/assemblies.py:81–160`](https://github.com/salmonmikan/sparkbrain_research/blob/81088ae386cbc611fb9e6366d8ade1c2ea74b6b7/src/sparkbrain/v05/assemblies.py#L81-L160)
   forms/matches internal unit order, membership and relative timing. For L/Fw and
   return L/G, equality already occurs at spike unit/time level, before pattern
   compression or final winner selection. Those later stages are not the first
   observed explanation of these particular ties
5. **Equal selected counts entail equal predictions.**
   The [native predictor](https://github.com/salmonmikan/sparkbrain_research/blob/81088ae386cbc611fb9e6366d8ade1c2ea74b6b7/src/sparkbrain/v05/prediction.py)
   selects the highest-count label. The [wrapper](https://github.com/salmonmikan/sparkbrain_research/blob/81088ae386cbc611fb9e6366d8ade1c2ea74b6b7/scripts/temporal_reuse_loop_probe.py#L265-L278)
   uses p1 = (1 + n1) / (2 + n0 + n1). Equal content is observed in separate branches;
   this is not evidence of accidentally shared live readout objects

**Fw is not an unlearned or fully frozen brain.** It inherits the learned prefix's
weights and delays. Only subsequent weight writes are disabled; assembly acquisition,
count readout and homeostasis remain live. Both fixtures begin with readout counts
30 for assembly-0001/label0, 25 for assembly-0002/label1, and 3 for assembly-0003/label1.
In novel Fw branches, new assembly-0004 ends with 10 or 6 label0 counts. Successful
novel behavior can therefore include genuine assembly/count learning without any
additional weight writes. This does not show that prefix learning was unnecessary.

### Attribution status

- Weight-bound clipping: not supported as the explanation; inspected updates have no clips
- Entirely inactive learned weights: contradicted by observed drive/potential changes
- Same discrete event trajectory despite continuous differences: directly supported
- Different L/Fw patterns hidden by winner/readout: not the observed case; patterns already match
- Universal irrelevance of weights, or general equivalence of L/G/Fw: not established
- Individual-edge necessity, silent-arrival margins or refractory mediation: not identified
- Homeostatic compensation as a necessary cause: not identified; L/Fw have identical recorded
  spike thresholds/stability and final homeostatic state

## Consequence for learned-state → M1

The immediate task remains [G0 real ownership/transaction eligibility, PR184](https://github.com/salmonmikan/sparkbrain_research/pull/184)
and its separately reviewed real-cloner continuation. Safe state ownership and a real
producer-to-consumer connection are useful even if later efficacy is negative.

A later M1 consumer must distinguish path contribution from incremental utility and
from weight-learning necessity. A deterministic consumer supplied only the same
recorded assembly features and the same consumer beforestate cannot reveal the hidden
continuous differences. That is a source-level implication, **not an executed M1 test**.
Do not append update counters, rescale similarities or expose drive values after seeing
these results just to manufacture a representation contrast.

## Conditional future discriminator, not authorized for execution

Only if a fresh, bounded weight-sensitivity question is needed after G0, preregister
this small factorial design rather than searching for a winning amplitude:

- Two fresh fixed nuisance/acquisition replicates; declare the topology and all inputs
  before any run. Use all replicates even if a dictionary or response is unsuitable
- Generate C/L/G/Fw donor weight states with identical fixed experience. Preserve the
  registered treatments; do not tune G retrospectively to match the measured L dose
- Put each complete donor weight map into otherwise identical, fully audited recipient
  states. Restore that identical recipient beforestate for **every donor × cell query**,
  including receptor, queue, membrane, homeostatic, dictionary, readout, episode and counter
  state. Keep delays fixed and disable learning updates, while ordinary within-query
  transient dynamics still evolve. Include an exact-copy sham. This isolates the weight
  intervention from donor differences and cross-cell carryover
- Use a complete fixed 3×3 grid, for example cue-strength multipliers `{0.75,1,1.25}`
  crossed with cue-timing offsets `{-1,0,1}` ms, for both cue orders. These are proposed
  design values, not cells tried on the retained run. Fix the exact timing transformation,
  input validity and current-Q treatment in the protocol before execution
- Every donor sees every identical cell. Report whole-grid paired changes and every
  cell, including no-match/abstention/rejection. A favorable strength cell or a within-arm
  amplitude effect is not evidence of learning benefit
- Primary mechanism endpoint: first divergence among logged arrival current, threshold/
  refractory status, spike unit/time, pattern, selected assembly and readout. A benefit
  endpoint must additionally compare fresh outcomes/actions and serious raw-history
  replacements under matched consumer access/capacity; crossing a threshold is not itself benefit

A two-replicate, four-donor, two-order, nine-cell query matrix is 144 queries; adding
one sham per order/cell/replicate gives 180. Acquisition/donor construction and copies
are additional costs that must be separately frozen. This is a design envelope, not
an implementation freeze or permission to run. No favorable-cell follow-up, enlarged
budget, threshold retuning or promotion of this consumed result is allowed.

## Exact evidence and data-only reproduction

The [input binding](../../artifacts/research/retention_equality_diagnosis_20261002/input_binding.json)
pins 48 raw files from 12 branches and seven frozen source files. It links the
byte-verified PR186 preservation archive, SHA-256
`75bee0d8ce010af13049f684651623a3257a00359966852ea6f0517516bce55d`.
Raw witnesses are `run/jobs/<fixture>-<condition>-<arm>/predictions.jsonl`,
`apply.jsonl`, `receipts.jsonl` and `final-state.json`. Row indices above are the
saved zero-based `index` values, not line selections invented by the report.
The complete archive is retained by
[PR186's transport manifest](https://github.com/salmonmikan/sparkbrain_research/blob/f382c2734e72aef3a7393c5aa117fa69047f1dde/artifacts/research/plasticity_retention_results_20261002/transport_manifest.json).

Run from the repository root, with a fresh extraction directory. Archived Python
is only hashed as source data; neither it nor the original execution runner is run.
The analyzer emits the exact pretty-printed saved diagnostic bytes:

```sh
python -S -P -B scripts/verify_retention_v5_evidence.py --extract /tmp/retention-equality-evidence
python -S -P -B scripts/analyze_retention_equality.py --run-root /tmp/retention-equality-evidence/run --source-root /tmp/retention-equality-evidence/frozen-sources > /tmp/retention-equality-diagnosis.json
cmp /tmp/retention-equality-diagnosis.json artifacts/research/retention_equality_diagnosis_20261002/diagnosis.json
python -B -m pytest -q tests/test_retention_equality_diagnosis.py
ruff check scripts/analyze_retention_equality.py tests/test_retention_equality_diagnosis.py
```

All 29 targeted data-only checks pass, including exact reproduction from the preserved
archive with a SparkBrain-import denial guard, raw/source hash binding, unchanged raw
bytes, pairing/completeness rejection and strict JSON parsing. Scoped Ruff passes.
These checks do not establish replay fidelity, a new scientific support gate or
counterfactual causality. Existing raw evidence and original scores are unchanged.
