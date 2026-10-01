# Continuous temporal reuse diagnostic results

Date: 2026-10-01 UTC. Status: **EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit: **0**.

**Decision: the prospective integration-proposal gate fails in both diagnostic seeds.**
The assembly arm recalls A correctly on its first return, but performs worse than both
raw-history alternatives over each complete suffix. Selective suppression demonstrates
dependence on the acquired assembly/readout path in this fixture; it does not establish
an incremental predictive benefit or a benefit from weight/delay learning.

This report follows the [v2 contract](temporal_reuse_loop_contract_20261001.md) and
[execution plan](temporal_reuse_loop_execution_20261001.md). Execution used source commit
`0bcb2c1b23c29e5107111343a757c57c1f7bbb41`. Runtime `src/` is unchanged from
`bd337bef2edddb2d388cbcf47bf176d469c2b180`. The frozen runner and its configuration
were not changed after results were observed. This diagnostic changes no historical
v0.5 acceptance decision, scientific allocation, or consumed identity. A unique
NON_EVIDENTIARY entry in the shared results ledger links this bounded report only.
It does not integrate v0.5 into M1 or resolve SB002.

## Prediction results

Q is the outcome-marginal reference; H is 32-window recent raw memory; R is retained
raw prototypes; S is the existing assembly path; F freezes weight/delay learning while
retaining assembly acquisition, count-readout learning, and homeostasis.

Each scored suffix has 32 predictions. Brier is mean `(p1 - outcome)^2`, including
abstentions. The native column gives **correct / non-abstaining / total**; accuracy
and coverage are the first and second counts divided by the third. S/F use the native
decision independently of the Laplace-smoothed probability adapter used for Brier.
Decimals below retain the recorded values; the full machine-readable summaries are in
the evidence archive's `run/report.json`.

### Seed 910071

| Arm | Return Brier | Return native | Interleaved Brier | Interleaved native |
|---|---:|---:|---:|---:|
| Q | 0.17051557570649925 | 31 / 31 / 32 | 0.25180862099989304 | 16 / 30 / 32 |
| H | 0.07250000000000001 | 30 / 32 / 32 | 0.0725 | 30 / 32 / 32 |
| R | 0.06415165974581612 | 28 / 28 / 32 | 0.0829709211814104 | 26 / 26 / 32 |
| S | 0.3118064367697691 | 14 / 29 / 32 | 0.38525721767823695 | 14 / 29 / 32 |
| F | 0.17750123043094132 | 10 / 10 / 32 | 0.14176847168490875 | 15 / 15 / 32 |

### Seed 910072

| Arm | Return Brier | Return native | Interleaved Brier | Interleaved native |
|---|---:|---:|---:|---:|
| Q | 0.17051557570649925 | 31 / 31 / 32 | 0.25278248376145496 | 15 / 30 / 32 |
| H | 0.07250000000000001 | 30 / 32 / 32 | 0.0725 | 30 / 32 / 32 |
| R | 0.07765357213323473 | 26 / 26 / 32 | 0.11001024118557297 | 23 / 23 / 32 |
| S | 0.3118064367697691 | 14 / 29 / 32 | 0.21724961907283546 | 21 / 29 / 32 |
| F | 0.15652362103072834 | 12 / 12 / 32 | 0.12546165075307938 | 16 / 16 / 32 |

### First return before feedback

The returning target is A, outcome 0. These predictions precede its first outcome receipt.

| Seed | Arm | First p1 | First Brier | First four mean Brier |
|---|---|---:|---:|---:|
| 910071 | Q | 0.5 | 0.25 | 0.2392092112759377 |
| 910071 | H | 0.8 | 0.6400000000000001 | 0.30000000000000004 |
| 910071 | R | 0.5 | 0.25 | 0.1684027777777778 |
| 910071 | S | 0.03125 | 0.0009765625 | 0.0008940536448182011 |
| 910071 | F | 0.03125 | 0.0009765625 | 0.1254737090363866 |
| 910072 | Q | 0.5 | 0.25 | 0.2392092112759377 |
| 910072 | H | 0.8 | 0.6400000000000001 | 0.30000000000000004 |
| 910072 | R | 0.029411764705882353 | 0.0008650519031141869 | 0.06311324584299952 |
| 910072 | S | 0.03125 | 0.0009765625 | 0.0008940536448182011 |
| 910072 | F | 0.03125 | 0.0009765625 | 0.1254737090363866 |

S passes the first-return confidence requirement: `1 - p1 = 0.96875` in both seeds.
Its subsequent native return sequence is identical across the two seeds: 14 correct A
predictions through `assembly-0001`, then three abstentions, then 15 incorrect B
predictions through `assembly-0002`. The three abstentions comprise two absent selections
and one newly selected assembly without learned outcome counts. First-return recall
therefore does not establish sustained reuse under continued learning.

## Causal checks and their limits

All targets were selected from the completed 64-cycle prefix. In both seeds, S's target
`assembly-0001` had 30 A and zero B selections; its matched `assembly-0002` had 25 B
and zero A selections. F's corresponding counts were 30 A and 26 B. These satisfy the
prospective count-matching rule. Each probe starts at the same quiet prefix checkpoint,
uses time 12,800 ms and occurrence ID `occ-000064`, and receives no outcome update.

Impairment is intervened minus sham Brier. A matched impairment is zero in every row
below, so A targeted impairment equals A targeted-minus-matched impairment.

| Seed | Arm | A targeted minus matched | B targeted signed | B matched signed | Mean absolute B collateral | Correct cue direction |
|---|---|---:|---:|---:|---:|---:|
| 910071 | S | 0.2490234375 | 0.0 | 0.0 | 0.0 | 8 / 8 |
| 910072 | S | 0.2490234375 | -0.172119140625 | 0.0 | 0.172119140625 | 6 / 8 |
| 910071 | F | 0.186767578125 | 0.0 | 0.155452806122449 | 0.0 | 8 / 8 |
| 910072 | F | 0.2178955078125 | 0.0 | 0.062181122448979595 | 0.0 | 8 / 8 |

S's prefix-valid matched B assembly is **inactive on the B probe shams**. Seed 910071
selects `assembly-0003` on all eight B probes. Seed 910072 selects that assembly on six
B probes, but incorrectly selects the A assembly on zero-based pairs 1 and 7. Targeted
suppression changes those two wrong, confident predictions from `p1=0.03125` to an
abstention at `p1=0.5`. Each Brier change is `-0.6884765625`; their mean is
`-0.172119140625`. This is improved loss through abstention, not improved correct
classification, and it violates the absolute-collateral bound of 0.02. The ineffective
matched B control also limits a strong cue-specific causal interpretation.

Removed-cue A/B inputs are identical after all A/C/F records are omitted, and their
predictions and recorded operational-state hashes match for every arm and pair.
Observer/sham rows match except for the external intervention label. However, the
observer branch executes the same model code as sham: it is a duplicate-sham control,
not an implemented renderer/display-removal test. The report field
`all_control_guards_passed` summarizes these fork equalities; it is not independent
certification of every isolation or resource requirement.

## What the result supports

1. **Acquired-path dependence:** suppressing the selected A assembly changes predictions
   and impairs A loss at the frozen prefix. This is assembly-path/readout dependence;
   it does not establish physical-unit specificity or a general memory mechanism.
2. **Incremental benefit:** none is shown here. H and R both beat S on return and
   interleaved Brier in both seeds, so the required 0.02 advantage fails throughout.
   These specified conventional raw-memory alternatives suffice for this comparison.
3. **Field-learning dependence:** no predictive benefit from weight/delay learning is
   shown. F has lower Brier than S on all four suffix comparisons. F also abstains much
   more, so lower Brier must not be reported as uniformly better native accuracy.
   Recorded F weight/delay changes are zero; its nonzero `eligibility_update_work`
   counts eligible-edge work, not learned parameter changes.
   F changes learning throughout the prefix as well as the suffix. This full-arm
   contrast does not isolate suffix-only plasticity effects from a common learned prefix.

These are two small synthetic diagnostic streams with fixed model topology, not a
population estimate, significance test, novelty claim, brain-equivalence claim, or
new acceptance result. The API pools cue and query cascades within a fixed window;
the result does not demonstrate that Q reads an independently persisting post-cue latent
state or implements an event-by-event integrated prediction/action loop.

## Integrity and resource audit

Independent read-only analysis recomputed all 20 suffix summaries and all reported
causal aggregates from raw rows. It also checked stored RNG realizations, cross-arm
input matching, paired swaps/removals, prediction-before-receipt timing, strongest
assembly selection, S/F count-readout probabilities/native decisions, checkpoint
predictor counts, wrapper receipt counts, checkpoint sizes, and top-level checkpoint
checksums. No independent full-model reproduction was run.

There are **1,792 raw rows**: 640 prefix rows, 640 scored suffix rows, and **512 causal
forks**. All 41 child jobs completed with exit code zero; the root zero exit was observed
by the execution task and is recorded in the transport manifest. All 232 files covered
by the run manifest match their hashes. The raw directory contains 235 files and
41,033,854 bytes; the three explicit run-manifest exclusions are its own manifest,
`execution-cost.json`, and `report.json`. The outer archive manifest covers those too.

The frozen runner SHA-256 is
`28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae`;
the v2 contract SHA-256 is
`83fe87ded3ac1b2797d46f64070f0197ef37db953d202099dcdefd4aca243f15`.
Both match the [source freeze](../../artifacts/research/temporal_reuse_loop_20261001/source_freeze.json).

| Measurement | Observed value | Contract bound |
|---|---:|---:|
| Maximum prefix plus suffix CPU | 15.290460000000003 s | 120 s |
| Maximum prefix plus suffix wall | 15.373862386011751 s | 180 s |
| Total CPU conservative upper bound | 180.970577896 s | 1,800 s |
| Total wall conservative upper bound | 184.73174911800015 s | 2,700 s |
| Maximum worker peak RSS | 46,137,344 bytes | 512 MiB address-space limit applied to workers |
| Maximum serialized full checkpoint/live-state accounting | 2,522,420 bytes | 64 MiB |
| Raw output | 41,033,854 bytes | 1 GiB |

All 512 per-fork timing records are below 0.348 seconds before the final cost-record
write; enclosing deadlines cover that write. Maximum recorded representation slots
are H 32, R 11, S 4, and F 3. Q uses two outcome counts; all arms additionally retain
receipt bookkeeping, included in state-byte accounting. Equal slot limits do not imply
equal byte use, computation, or efficiency.

Important enforcement limits remain:

- `RLIMIT_AS` is applied to workers only. The orchestration driver has no recorded
  peak RSS and no corresponding address-space limit; blanket per-process memory-cap
  compliance is not established.
- Network enforcement is Python socket-audit denial. An OS network namespace was
  unavailable, so this is not OS-level network isolation.
- Input metadata is empty, and source inspection confirms prediction receives only
  pulses, start time, and opaque occurrence ID. Targets in evaluator job files and
  raw audit rows are not prediction features; earlier delivered outcomes are available
  through the outcome API. This is source-level separation, not an OS label sandbox.
- Native checkpoint restoration has known omitted transient caches. Recorded real-prefix
  quiet-boundary checks and saved direct/restored fixture equality support only the
  contract's restricted continuation. They do not prove general checkpoint fidelity.

## Evidence package and validation

The [transport manifest](../../artifacts/research/temporal_reuse_loop_20261001/transport_manifest.json)
lists 27 base64 parts under `artifacts/research/temporal_reuse_loop_20261001`.
Concatenating their decoded bytes yields a 3,468,355-byte gzip archive containing 241
files: the 235 run files, five frozen source/contract files, and an outer archive manifest.
Archive SHA-256:
`2dfbe4f3afb8b046c1b465dcb52461daa027f72939dd85cf7dfad15670947082`.

From the repository root, verify the published bytes and descriptive arithmetic without
importing or running a model:

```bash
python scripts/verify_temporal_reuse_evidence.py
```

The standalone verifier passed, checking transport/archive/member hashes and suffix/
causal arithmetic. After Codex identified that the first publication verifier trusted the
reported proposal booleans, the verifier was corrected to independently reconstruct all
gate inputs, including cue direction and fork equalities, then compare per-seed control
guards, per-seed proposal gates, and the two-seed proposal gate. It checks exact seed/arm/
condition/fork inventories and rejects numeric substitutes for decision booleans.
Thirty-three no-model tests include coherently rehashed false reports, altered raw control
hashes, a passing hand-written arithmetic fixture, and failure of every gate predicate.
This repairs publication verification only: the frozen runner, protocol, raw evidence,
reported values, and negative decision are unchanged. Its role remains narrower than the
independent source/input audit above; neither is a fresh full-model reproduction.

At the frozen execution-source head, 659 configured pytest tests passed. After preserving
merged PR #167 and adding initial publication corruption checks, 691 configured tests
passed. After the verifier correction, the final local suite passed 721 configured tests
with 392 scientific/reproduction/external tests deselected. Ruff, local readiness, demo,
the 40-episode/30-step benchmark, and bundle validation also passed. These are repository
validation results, separate from the diagnostic run and its resource accounting.
At report preparation, exact-head CI and Codex review of the publication are pending.
No publication/merge readiness claim is made here.

## Smallest justified follow on

First perform read-only trace triage of the return transition from A selection through
abstention into B-assembly selection, and the inactive matched B probe control. Separate
selection, representation, and readout explanations using the preserved traces before
proposing a mechanism change. Any follow-on experiment requires a new prospective
design and applicable authorization. Do not tune, extend, reinterpret as confirmatory,
or replace this completed run to obtain a passing result.
