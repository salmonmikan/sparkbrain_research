# RV01 R01-15 Post-spike Suppression Discrimination Protocol

## Status

**PREREGISTERED_DEVELOPMENT_ONLY / IMPLEMENTATION_NOT_STARTED**

R01-15 is prospective work derived from the fixed R01-14A negative/scope-narrowing result. It does not rerun, repair, rescore or alter R01-12F, R01-13A or R01-14A evidence. R01-14A remains fixed: the Field showed a descriptive low-repetition traversal difference, but the registered interference-specific interpretation was not supported and the discovery-AUC endpoint in the historical artifact is excluded by the independent-review correction.

Protocol identifier:

```text
rv01-r01-15-post-spike-suppression-v1
```

No held-out or formal capability is authorized by this document.

## Question fixed before implementation

R01-14A localized the remaining descriptive difference to rollout/repetition dynamics rather than selective interference retention. The next question is therefore deliberately mechanistic and route-agnostic:

> Does ordinary Field-local post-spike suppression — absolute refractory state, adaptation state, or their interaction — causally account for the lower immediate-revisit / faster-first-visit traversal signature while learned connection state and the comparator contract are held fixed?

R01-15 does **not** ask whether the Field is more correct, more selective, or superior to the reservoir.

## Scientific firewall

1. R01-12F, R01-13A and R01-14A raw evidence and reports are read-only motivation.
2. No R01-14 world is rerun under the R01-14 identity.
3. The ordinary trained Field connection state is created once per fresh development world and cloned before the R01-15 rollout interventions.
4. The fixed `ResourceMatchedSparseReservoir` contract is not weakened or retuned.
5. No route label, correct-action label, reward, semantic class or future outcome may enter the intervention.
6. The intervention acts only during the probe rollout, after training is complete. It cannot alter learned weights/delays or training exposure.
7. The same probe cue, initial cloned Field state, horizon and native event/spike limits are used for every Field arm.
8. Exact-route recovery, contamination and ordered retention remain secondary firewall measures, not admission criteria for the mechanism claim.
9. Development failures and negative results are preserved. No intervention magnitude sweep is permitted under R01-15.
10. Held-out capability remains closed regardless of the development outcome until a separate claim target and freeze review exist.

## Fresh world namespace

A repository collision search found no use of the exact seed `141500` before this preregistration. R01-15 reserves a fresh, separated namespace:

```text
development seeds: 141500, 141501, 141502, 141503, 141504
reserved held-out: 141600..141609
```

The development grid keeps the same five topology-family geometries and 96-unit scale used by R01-13/R01-14, but must use a new R01-15 world-grid salt. Reserved held-out worlds may be instantiated and hashed only; capability execution is prohibited in the initial implementation.

## Fixed expression-only intervention design

For each trained development world and each registered route probe, serialize one pre-probe Field state. Every Field arm is restored from those exact bytes before the same cue is applied.

The intervention is implemented at the post-spike state boundary only. It must not change topology, connections, weights, delays, base threshold, membrane time constant, input gain, cue routing or the external training history.

### F0 — intact Field

Unmodified R01-14/R01-12 Field rollout. This is the within-world Field reference.

### FA — adaptation neutralized

After each emitted spike is fully recorded and its outgoing consequences are scheduled according to the ordinary runtime, set only that spiking unit's adaptation state to zero before later events are processed.

Do not change its refractory state, reset potential, connections, queue entries or any other unit field.

### FR — absolute refractory neutralized

After each emitted spike is fully recorded and its outgoing consequences are scheduled according to the ordinary runtime, set only that spiking unit's `refractory_until_ms` to the spike time, so subsequent arrivals are not rejected by the future absolute refractory interval.

Do not change adaptation, reset potential, connections, queue entries or any other unit field.

### FAR — both post-spike suppressors neutralized

Apply exactly the FA and FR post-spike state edits together. No additional parameter or state is changed.

These are fixed zeroing interventions, not parameter sweeps. If the implementation cannot isolate these state edits without changing other runtime semantics, the cell is incomplete and R01-15 must not be executed until the isolation contract is repaired prospectively.

## Shared reservoir reference

For each world/route, execute the same fixed resource-matched reservoir reference used by the accepted RV01 comparator contract. The reservoir is generated once per probe identity and is shared across comparison with F0/FA/FR/FAR; it is not retuned separately for each Field intervention.

R01-15's primary causal comparisons are among the four Field arms. Reservoir values provide the already-established external reference for whether the original Field/reservoir traversal gap is present on the fresh grid.

## Required retained evidence

Each probe must retain enough raw state to verify independently:

- exact pre-probe serialized Field bytes and hash;
- exact equality of the restored starting state across F0/FA/FR/FAR;
- cue identity, time and routing;
- ordered emitted spike/unit sequence for every arm;
- all post-spike intervention records with unit ID, spike time, field name, before value and after value;
- a proof that FA edits only adaptation, FR only refractory state, and FAR only those two fields;
- connection/topology hashes before and after every probe;
- native event/spike counts and any guard failure;
- route-agnostic event count, distinct count, revisit count/rate, new-state yield and first-visit positions reconstructed from raw emitted IDs;
- exact-route recovery, ordered retention and contamination only as secondary firewall outputs;
- one shared fixed-reservoir trace for the same probe identity.

The historical R01-14 `normalized_discovery_auc` is not an R01-15 endpoint. Do not reintroduce it under another normalization.

## Registered causal readout

For each probe, define `B` as the minimum distinct-state breadth reached by the intact Field F0 and the shared reservoir under the registered horizon. For F0/FA/FR/FAR, report the shortest original-order prefix needed to reach `B` where reachable; if an intervention fails to reach `B`, retain that failure explicitly rather than substituting another breadth.

Primary outputs are:

- events to reach the fixed intact/reference breadth `B`;
- revisits before reaching `B`;
- revisit rate;
- first-visit positions;
- whether the original F0-versus-reservoir event/revisit direction replicates on the fresh development grid.

No tuned threshold is used to define a positive result.

## Discrimination logic

Interpret the arm contrasts per family and across the complete development grid without selecting a favorable subset after execution.

### P15-A — adaptation contribution

Supported descriptively if FA consistently shifts the intact Field toward more revisits / more events to the same fixed breadth while FR does not show the same shift.

A result limited to one cherry-picked topology is insufficient; all family outcomes must be reported.

### P15-R — refractory contribution

Supported descriptively if FR consistently shifts the intact Field toward more revisits / more events to the same fixed breadth while FA does not show the same shift.

### P15-AR — interaction / redundant suppression

Supported descriptively if neither single neutralization explains the effect but FAR produces a substantially stronger, consistent shift than either single arm. This is an interaction/redundancy result, not permission to tune intermediate values.

### P15-N — none of the registered suppressors explains the signature

If F0's traversal difference replicates but FA/FR/FAR do not materially alter the registered event/revisit pattern, R01-15 is negative for post-spike suppression and the explanatory locus remains elsewhere in ordinary propagation/topology dynamics.

If the F0 traversal signature itself fails to replicate on the fresh grid, R01-15 ends as a failed replication and no suppressor mechanism is claimed.

## Selectivity firewall

Even a strong P15-A/P15-R/P15-AR result cannot establish clean route selection. Report exact-route recovery and contamination for every arm. If an intervention changes traversal while correctness remains tied or contamination worsens, retain that separation explicitly.

No R01-15 outcome may be imported into A01 as evidence of causal-lineage specificity. R01-15 concerns rollout repetition only.

## Prohibited adaptations

After the first R01-15 development execution begins, do not under the same identity:

- change the development seed set or world-grid salt;
- change the post-spike intervention from exact state neutralization to a tuned partial value;
- change horizon, cue strength, threshold, membrane/adaptation constants or resource limits;
- choose a different comparator or retune it;
- alter family inclusion based on observed outcomes;
- redefine traversal endpoints;
- rescue a failed replication with additional seeds.

Any such change requires a new protocol identity.

## Initial execution boundary

The next safe step is implementation plus tests proving exact-state cloning and one-field/two-field intervention isolation. After CI and independent code review, only the five-seed exposed development grid may run. The reserved held-out namespace remains sealed and no formal/held-out workflow should be created by the initial R01-15 implementation.
