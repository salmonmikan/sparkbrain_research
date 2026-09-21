# Prospective distributional-control contract

Candidate: `CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01`  
Layer: `ARCHITECTURE_STUDY`  
Claim ceiling: `MECHANISM`  
Evidence status: `NON_EVIDENTIARY`  
Analyst authority: `EVA-20260921T095900+0900-R32-6D2A91C4@6bf35ff0f08a981feb09abced00e157526a47cb0`  
Source contract: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Authorized scope

This cycle fixes an outcome-independent contract for a fresh Assembly-set causal-necessity question. It does **not** execute `suppress_units`, `suppress_assembly`, a lesion arm, or any intervention outcome. It does not reopen or relax `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01`; that exact-match object remains terminal.

`preformal_eligible=true` means only in-principle eligibility. Current `preformal_readiness.status=NOT_READY`. A well-defined contract is not prior scientific success and does not authorize PRE_FORMAL.

## Set-level claim

The only prospective claim is coalition/set-level causal necessity/selectivity:

> Suppressing the complete selected mature Assembly prototype causes greater loss of its already-supported motif prediction than ordinary same-cardinality nonmember lesions, including both an unconditional sparse-lesion distribution and a pre-intervention balance-aware lesion distribution, without relying on an out-of-support whole-field perturbation footprint.

This contract cannot support individual-unit responsibility, unique causal contribution of each unit, a new learning principle, or SYSTEM-to-MECHANISM upgrading of any predecessor.

## Fixed development surfaces

A future outcome-bearing continuation, only if separately authorized by a fresh Evidence Analyst generation, must use exactly these development seeds in this order:

`1701, 1702, 1703, 1704`

No replacement seed is allowed after any intervention outcome is opened. Retained v0.5 confirmatory seeds `601..604`, consumed FORMAL identities, official scorer inputs, and sealed/evidence fixtures are excluded.

For each seed:

- train with `train_brain(seed, count=24)` using the stable-main v0.5 API and topology contract;
- derive the target from training rows only;
- construct one fresh non-learning `motif_x` baseline probe beginning at `trained.current_time_ms + 100.0`;
- use `learn_assembly=false`, `learn_field=false`, `explore_action=false` for baseline and future evaluation episodes;
- no intervention result may select or alter the target, comparator pool, covariates, episode schedule, endpoint, footprint measure, or interpretation rule.

The fixed surface is invalid, with no replacement, if the source/API cannot produce the required target or comparator contract exactly as specified below.

## Target selection

For each surface, compute training counts by mature Assembly ID and motif label. Rank mature Assembly IDs by:

1. descending `(motif_x_count - motif_y_count)`;
2. descending `motif_x_count`;
3. ascending Assembly ID.

The first Assembly must have positive `motif_x_count - motif_y_count`. Its **entire prototype unit set** is the target coalition. The prototype cardinality must be in `2..4`; otherwise the surface is `INVALID_SURFACE`. The baseline probe must identify that Assembly as the strongest mature unsuppressed activation and must predict the probe's expected future event. Failure is `INVALID_SURFACE`; it must not trigger a seed substitution or target change.

Target selection uses only training and unsuppressed baseline information. It never uses a lesion result.

## Eligible nonmember lesion population

For a target of cardinality `k`, the eligible unit pool is every internal-reservoir unit that is neither a receptor unit nor a member of the target coalition. The eligible lesion population is the complete set of unique `k`-subsets of that pool.

A surface is comparator-infeasible if fewer than `320` eligible lesion sets exist. No unit may be added, removed, or reclassified after outcome inspection to repair this condition.

## Pre-intervention balance vector

For the target and every eligible comparator set, compute the following seven-component vector from the trained, unsuppressed checkpoint and the single fixed baseline probe:

1. total baseline-probe spike count across units in the set;
2. number of excitatory units;
3. total incoming edge count;
4. total outgoing edge count;
5. total incoming edges whose source is a receptor;
6. summed count of distinct internal-reservoir units reachable from each selected unit within one or two directed outgoing hops;
7. summed count of distinct internal-reservoir units able to reach each selected unit within one or two directed incoming hops.

These are ordinary pre-intervention covariates only. They are not treated as a privileged definition of causal equivalence.

## Two fixed comparator distributions

Each valid surface has two same-cardinality, nonmember control distributions, both fixed before any lesion outcome.

### A. Uniform sparse-lesion distribution

Select exactly `64` unique eligible comparator sets without replacement from the complete eligible population. The deterministic RNG seed is the unsigned first 64 bits of:

`SHA256(candidate_id + "|" + surface_seed + "|uniform-v1")`.

Sets are canonically encoded as ascending integer tuples and the eligible population is lexicographically ordered before sampling. The selected control sets are sorted lexicographically after sampling.

### B. Balance-aware distribution

For each of the seven covariates, compute the median and median absolute deviation over the complete eligible population. The scale is `max(MAD, 1.0)`. For comparator vector `v` and target vector `t`, define the pre-intervention balance distance:

`d(v,t) = sum_j abs(v_j - t_j) / scale_j`.

Rank all eligible sets by `(distance, lexicographic_set_tuple)`. The first `256` sets form the fixed balance reservoir. From that reservoir select exactly `64` unique sets without replacement using the unsigned first 64 bits of:

`SHA256(candidate_id + "|" + surface_seed + "|balanced-v1")`.

This is a distributional covariate-balance control, not a relaxation or rescue of the predecessor's exact-match rule. No lesion outcome enters the distance, reservoir, or sample.

Overlap between the uniform and balance-aware distributions is allowed and is reported; it does not cause resampling.

## Sham and matched privilege

The sham arm is the same trained checkpoint and exactly the same future episode sequence with no suppressed units.

Every future arm—sham, target, uniform comparator, and balance-aware comparator—must start from an independent deep copy of the same trained pre-intervention checkpoint for that surface. Every episode within an arm must itself start from a fresh copy of that arm's initial checkpoint so sequential non-learning policy/bookkeeping state cannot create unequal carryover.

All arms receive identical episode inputs and equal compute privilege. No branch may receive extra retries, longer runtime, extra episodes, alternate thresholds, or alternate target/comparator selection.

## Fixed future episode schedule and resource contract

If a fresh Analyst generation later authorizes an outcome-bearing Architecture or PRE_FORMAL continuation, each valid surface uses exactly the first `8` `motif_x` episodes from `held_out_episodes(seed=surface_seed, condition="jitter", count=<sufficient>, start_ms=trained.current_time_ms + 100.0)`, preserving generator order and discarding non-`motif_x` rows without replacement or retry until eight are obtained. If eight cannot be obtained from the source-defined bounded generator call chosen by the future harness without changing generator semantics, the surface is `INVALID_SURFACE` and stops.

Per valid surface the fixed arm budget is:

- `1` sham;
- `1` target-coalition lesion;
- `64` uniform same-cardinality lesions;
- `64` balance-aware same-cardinality lesions.

Total: `130` arms × `8` episodes = `1040` episode evaluations per surface; four fixed surfaces = at most `4160` episode evaluations. CPU execution is sufficient; no GPU, network service, hidden cache, adaptive retry, or extra seed is part of the contract.

The future harness must bind its exact Python/package/runtime/source SHA before opening lesion outcomes. This cycle consumes no identity and creates no FORMAL/TEST/STARTED/evidence tag.

## Primary observable

For each episode, the prediction-success indicator is `1` iff `result.prediction.value == episode.future_event`, otherwise `0`.

For arm `a` on a surface:

`accuracy(a) = mean(prediction_success over the fixed 8 episodes)`

`impairment(a) = accuracy(sham) - accuracy(a)`

The target impairment is compared separately to the two preregistered ordinary control distributions.

Define:

`D_uniform = impairment(target) - median({impairment(u): u in uniform_controls})`

`D_balanced = impairment(target) - median({impairment(b): b in balanced_controls})`

These sign-based discriminators avoid an outcome-responsive numeric success threshold. They may not be replaced after results are opened.

## Perturbation-footprint diagnostic

For each episode, compute the whole-field spike multiset from `result.v04_result.spikes` as counts by unit ID. Against the paired sham episode define:

- `footprint_count_delta`: absolute difference in total spike count;
- `footprint_unit_l1`: sum over all field units of the absolute difference in spike counts by unit ID.

For each arm, the footprint is the mean pair `(footprint_count_delta, footprint_unit_l1)` across the fixed episodes. The footprint is a support/confounding diagnostic only; it is never used to choose a comparator after outcomes are opened.

For each surface, target footprint is in ordinary-control support only if each target footprint component lies within the inclusive minimum/maximum envelope formed by the union of the two comparator distributions. Otherwise the surface is `FOOTPRINT_OUT_OF_SUPPORT` for the set-specific claim.

## Support rule

The fixed four-surface contract is conjunctive and non-adaptive:

- every listed surface must satisfy target/API validity and comparator-population feasibility;
- all arms must use matched source/runtime/resource privilege;
- no surface may be replaced or silently dropped after an outcome is opened;
- target footprint must remain inside the ordinary-control envelope on every surface for a positive set-specific interpretation;
- support breadth is reported per surface and across all four surfaces; no result from one surface upgrades another.

An invalid or infeasible surface stops the current future execution for fresh Analyst classification rather than shrinking the support set post hoc.

## Fixed falsifier / reduction decision

The fresh set-level mechanism question is falsified or reduced by ordinary lesion effects on a surface if **either**:

- `D_uniform <= 0`; or
- `D_balanced <= 0`.

It is also unresolved for an Assembly-specific interpretation if target perturbation footprint is outside the ordinary comparator envelope.

A future positive development signal therefore requires, on every fixed valid surface, `D_uniform > 0`, `D_balanced > 0`, and in-support target footprint. That condition is a development discriminator only. It is not a FORMAL PASS rule, does not imply novelty, does not establish individual responsibility, and does not by itself make PRE_FORMAL READY.

## Current-cycle feasibility conclusion

The contract is prospectively well-defined using source-supported operations already present on stable main: arbitrary deterministic development seeds, training rows and mature Assembly prototypes, deep-copy evaluation, unit suppression, held-out episode generation, predictions, field spikes, and the static field graph. Comparator construction depends only on training/baseline pre-intervention information. The resource budget is finite and fixed. No lesion outcome is needed to define any scientific choice above.

Therefore the R32 Architecture cycle reaches the prospective terminal `READY`: the **contract** is ready for fresh Evidence Analyst review. This does not mean the candidate beat ordinary reductions, survived its falsifier, or is likely to pass anything. No intervention is authorized or executed in this cycle.
