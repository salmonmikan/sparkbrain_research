# EXPLORATORY / NON_EVIDENTIARY — Plasticity Update-Cap Scaling Bias

## Discovery identity

- mode: `discovery`
- exploratory_target: `PLASTICITY_UPDATE_CAP_SCALING_BIAS_DISCOVERY`
- candidate_pool_id: none; safe bounded SUB self-selection
- exploration_cycle: `1/3`, stopped early after reduction
- source main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`

## Independence from MAIN

This diagnostic does not use, modify, or depend on the active MAIN
`CAND-TOPK-PA-01` architecture-study branch, signal, blocker, result, or
outcome-dependent successor. It uses only stable v0.5 topology/plasticity
substrate from `main` and a synthetic all-eligible plasticity condition.

No repository dataset, trained checkpoint, formal raw preserve, held-out TEST
surface, sealed input, official scorer, STARTED/control authority, or consumed
identity is used.

## Question

`V05PlasticityController.apply()` traverses `sorted(field.connections)` and
stops after the fixed `max_updates_per_step=2000` successful updates. Does that
fixed cap create arbitrary numeric-unit-ID privilege once the effective
plastic-edge count exceeds 2000, even when the semantic graph and activity are
otherwise identical?

The reduction question is whether any observed scale effect is fully explained
by the ordinary implementation mechanism `sorted edge keys + hard update cap`.

## Inputs and procedure

The topology family is the current `layered_reservoir_topology` with
`receptor_count=16` and `seed=505`. The diagnostic obtains effective edge keys
through `TemporalExcitableField`, matching the actual connection dictionary
used by the plasticity controller.

For each scale, 24 deterministic random permutations relabel reservoir numeric
IDs while receptor IDs and every semantic edge identity are preserved. The
synthetic step assumes every effective plastic edge is eligible for a nonzero
plasticity update. This deliberately isolates scheduling/resource behavior
rather than learning quality.

For each relabeling, the exact scheduling rule is mirrored: sort the relabeled
numeric edge keys and retain the first 2000. The selected edges are then mapped
back to semantic identities. Pairwise Jaccard overlap measures whether an
isomorphic numeric relabel changes which semantic edges receive the scarce
updates.

- topology seed: `505`
- relabel seed: `20260919`
- relabelings per scale: `24`
- update cap: `2000`

## Observations

| reservoir | effective edges | cap active | edges updated | mean semantic Jaccard | min–max Jaccard | mean reservoir sources touched |
|---:|---:|:---:|---:|---:|---:|---:|
| 8×6 (48) | 326 | no | 1.0000 | 1.0000 | 1.0000–1.0000 | 48.000 |
| 16×12 (192) | 1,193 | no | 1.0000 | 1.0000 | 1.0000–1.0000 | 192.000 |
| 20×15 (300) | 1,836 | no | 1.0000 | 1.0000 | 1.0000–1.0000 | 300.000 |
| 24×18 (432) | 2,628 | yes | 0.7610 | 0.6159 | 0.5717–0.6708 | 327.125 |
| 32×24 (768) | 4,648 | yes | 0.4303 | 0.2809 | 0.2346–0.3289 | 326.417 |

Below the cap, every edge is selected and the result is exactly invariant to
numeric relabeling. Immediately after crossing the cap, isomorphic relabelings
produce materially different semantic update sets. At 24×18, only about 76.1%
of effective edges receive an update and mean pairwise overlap falls to about
0.616. At 32×24, only about 43.0% receive an update and overlap falls to about
0.281.

The number of reservoir source IDs represented among selected edges also
saturates near 326 at both over-cap scales rather than scaling with reservoir
size. This is consistent with the lexicographically early source-ID prefix
induced by the fixed cap.

## Reduction and stopping decision

The observation is fully explained by the source-level mechanism already
visible prospectively: deterministic numeric-key sorting followed by a fixed
successful-update cap. There is no need for a second exploratory cycle to
rescue or retune this candidate.

This is therefore useful as a scaling/engineering failure mode and as a future
comparator/control requirement, but not as a scientific research object on the
current evidence.

A counterexample to this reduction would require an identity-neutral scheduler
with the same total update budget to preserve comparable semantic asymmetry.
That was not tested here because it would be a distinct prospective question,
not a rescue of this reduced candidate.

## Handoff to Evidence Analyst

- what_would_falsify_or_reduce_it: reduction is already achieved by
  `sorted numeric edge keys + hard cap`; an identity-neutral matched-budget
  scheduler showing the same semantic asymmetry would reveal an additional
  mechanism.
- candidate_next_research_layer: none scientifically; optionally record an
  architecture/infrastructure scaling constraint for any future v0.5 learning
  study that can exceed 2000 eligible edges per step.
- scientific_choices_still_open: whether a future engineering change should
  use randomized, round-robin, source-balanced, or otherwise identity-neutral
  quota scheduling; these are implementation choices, not choices to tune on
  formal outcomes.
- recommendation: `REJECT`
- utility_request: none
- consumed_identities: none
