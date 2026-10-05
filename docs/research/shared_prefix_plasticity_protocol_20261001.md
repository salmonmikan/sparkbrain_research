# Proposed shared-prefix suffix plasticity diagnostic

Status: **PROPOSED / UNEXECUTED / NONFORMAL / ZERO SCIENTIFIC CREDIT**. No runtime calls are authorized by this file alone. Independent source review and a separate runner/input freeze are required before execution. This is a fresh development diagnostic motivated by a result-exposed predecessor; it does not revise PR169.

**Question:** Is continuing weight and/or delay learning after the common A32/B32 history causally responsible for the subsequent A-to-B routing and loss, conditional on the current receptor/homeostatic mechanisms?

This is a small diagnostic follow-on, not a formal evaluation or an attempt to select a replacement configuration from the old test data.

### Design proposed for review

1. Keep the PR169 generator, timing, cue amplitudes, topology, thresholds, matcher, readout, and H/R algorithms unchanged. Use two explicitly prospective seeds, 910073 and 910074; freeze their inputs and hashes before runtime. They are not repetitions used to improve the old result
2. For each seed, train **one full-S A32/B32 prefix** with both learning flags enabled, then save a complete supported checkpoint at the predecessor's quiet boundary. Require an empty event queue and pending-cascade buffer; every burst-window spike must be older than `next_start_ms − window_ms`, every burst emitted key expired before `next_start_ms`, and every outgoing list in canonical `(delay_ms, target_id)` order. Preserve the source/state-inspection predicates in the pinned predecessor's `eligibility()` rather than assuming serialized equality proves these facts. The last prediction must have exactly one completed outcome receipt. Derive four fresh branches from those exact bytes: W+D+, W−D+, W+D−, W−D−. Change only `config.enable_weight_learning`, `config.enable_delay_learning`, `plasticity.config.enable_weight_learning`, and `plasticity.config.enable_delay_learning`, preserving weights, delays, eligibility, homeostasis, receptors, candidate bank, counts, and supported state. Assert normalized serialized payload equality with only those four declared flag paths exempted. Transport checksums are recomputed after any intentional flag changes and are not omitted learned state
3. Keep `learn_field=True`, `learn_assembly=True`, homeostasis/receptors enabled, and outcome learning identical in every branch. Use `dataclasses.replace` on the existing configuration objects in the diagnostic fixture, without changing production code. Do not reset eligibility or reward trace
4. Run the same 32 returning-A suffix observations in each branch, with one prediction and one later outcome receipt per cycle. Run unchanged H and R once per seed through the same 64-prefix +32-suffix stream. No other arms or jitter levels, no parameter grid, no discarded seeds, no repeat-until-success
5. Planned model budget: per seed, 64 full-prefix +4×32 suffix =192 v0.5 transitions, plus 2×96 ordinary-memory transitions =192. Two seeds total **384 v0.5 +384 baseline transitions =768 predictions and768 outcome receipts**. Setup/checkpoint verification does not call model dynamics. No automatic reproduction matrix; any infrastructure failure is retained and returned for review before an amendment

### Required invariant and outcomes

- First suffix emitted pulses, spikes, patterns, activations, prediction, and readout must be identical in the four branches. Weight/delay updates happen after those spikes; violation signals a fixture/state-isolation problem. Full operational hashes may differ because intervention flags and post-step updates are intentional
- Every branch emits a complete per-step record before receiving the outcome, including cue emissions, internal spike times/order/bins, all candidate scores and margins, selected ID, candidate origin, counts before prediction, p1/native/confidence, and no-pattern/immature/empty-readout classification
- Retain full per-step connection parameters, homeostatic thresholds/rates, eligibility, and receptor state rather than only endpoint parameter hashes. Record the intervention set separately from the learned state. Preserve no-clobber outputs and failed runs
- Fix the prefix B-associated candidate set before every fork as mature candidates whose readout has `count("1") > count("0")`, with at least one recorded outcome. Fix A-associated candidates analogously with strict zero-label majority. Ties and empty readouts belong to neither set; candidate IDs are recorded, never guessed from ordinal names. These sets do not change as suffix counts change
- **Primary endpoint:** count, from 0 to32, of returning-A rows whose selected mature activation belongs to the frozen prefix B-associated set, including rows with a newly tied suffix readout. Abstention with no selected activation is not a B selection
- Secondary routing endpoints: first zero-based B-selection index (null if none), and first B-selection index that has an earlier selection from the frozen A-associated set (null if absent). A first-row B selection is explicitly initial misrouting, not an A-to-B crossover
- Secondary order endpoint: first zero-based row whose sole retained internal pattern begins `[56,45]` after an earlier suffix row whose sole pattern begins `[45,56]`. Otherwise null. Multiple-pattern rows are reported separately and do not silently enter this narrowly source-motivated endpoint. Preserve exact spike times and timing bins; no tolerance adjustment
- Secondary performance endpoints: Brier, native accuracy (abstention wrong), coverage, the first return prediction before any return outcome, first-A recall (first zero-based suffix index with native prediction 0; null if absent), and wrong/abstain loss contributions. Report each seed and every branch, not a selected winner
- For each seed and each numeric count/loss endpoint `Y`, compute W effects `Y(W+,D) − Y(W−,D)` at each fixed D; D effects `Y(W,D+) − Y(W,D−)` at each fixed W; and interaction `Y++ − Y−+ − Y+− + Y−−`. Positive count/loss contrasts mean enabling that factor increases the adverse outcome. Report both seeds individually and their unweighted mean. Nullable first-event indices stay descriptive and are never imputed or included in arithmetic. With two seeds these are conditional intervention results, not population-level statistical proof
- Preserve actual work/memory/wall-time accounting and the inherited ceilings: 32 slots for each assembly/prototype bank and H history; 120 CPU seconds and 180 wall seconds inclusive of prefix+suffix trajectory; 512 MiB address space per process; 64 MiB full serialized checkpoint; 30 CPU minutes, 45 wall minutes, and 1 GiB output globally. Charge the shared prefix once to total cost and to each branch's inclusive trajectory; count all restore/serialization/output overhead. Preserve unchanged event/spike/update caps and record peak RSS for driver and workers. Eligibility/update work is not a count of weight changes. Explicit resource enforcement must be checked in the reviewed runner; declared limits or a Python socket hook alone are not OS isolation evidence

### Execution gate and artifact contract

The next source review must bind a runner and exact source hashes, a serialized
configuration, both input streams and their hashes, an empty fresh output root,
resource enforcement, and zero-model-call tests of the flag/state comparison and
endpoint arithmetic. This document alone is not an execution freeze. Preserve
the reviewer record before the first model transition. No hidden smoke run on
either prospective seed is allowed. A failed invariant, resource cap or execution
is terminal for that attempt: retain partial bytes and failure provenance, do
not add a replacement seed or automatic rerun. Any amendment is prospective and
must be reviewed separately; earlier failures stay visible.

Production restoration omits some burst-detector transient state and rebuilds
outgoing adjacency order. The pre-fork eligibility gate makes this omission
inactive at the declared next-input boundary; retain the actual facts for both
prefixes. Equal first outputs among four restored branches only check treatment
isolation, not arbitrary checkpoint continuation fidelity. If eligibility fails,
stop without a suffix rather than reordering learned connections, resetting
state, changing the boundary or increasing the dynamics budget.

### Falsifiable interpretation

- If W−D− still crosses to B with the same common starting state, continued weight/delay updates are not necessary for that failure; investigate persistent receptor/field/homeostatic trajectory next, not another weight sweep
- If removing one factor prevents the crossover across the declared seeds while the other matched branch still crosses, that supports a conditional causal contribution of that factor. It does not prove a universally better architecture
- If reduced loss is achieved through extra abstention, report that separately. It is not successful reuse or restored adaptation
- If all four branches avoid the old failure on the prospective seeds, retain the old negative result and label this follow-on inconclusive about its mechanism. Do not retrofit seeds, timing bins, or thresholds
- A same-prefix improvement still does not establish assembly advantage over H/R. A subsequent assembly-value study must separately require active matched representation controls and ordinary-memory comparison. No such further execution is included here


## Sources and predecessor

- [Read-only predecessor triage](temporal_reuse_causal_triage_20261001.md)
- [PR169 durable evidence](https://github.com/salmonmikan/sparkbrain_research/tree/b6a872642df6889e9c6ce82148a5a2430db2c114/artifacts/research/temporal_reuse_loop_20261001)
- Production v0.5 source unchanged at predecessor execution pin `0bcb2c1b23c29e5107111343a757c57c1f7bbb41`; exact successor runner/source/input pin remains pending
