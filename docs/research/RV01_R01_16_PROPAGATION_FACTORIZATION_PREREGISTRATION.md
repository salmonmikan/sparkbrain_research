# RV01 R01-16 propagation-factorization preregistration

Date: 2026-09-12  
Status: **PROSPECTIVE DEVELOPMENT-ONLY DESIGN / NOT IMPLEMENTED / NOT EXECUTED**

## Inherited fixed evidence boundary

R01-15 is a consumed exposed-development identity and must not be rerun, repaired, rescored, or tuned in place. Its fixed result is negative mechanistic discrimination:

- all 100/100 registered probes were behaviorally identical across intact, adaptation-zero, refractory-zero, and combined arms;
- the registered refractory intervention physically changed state on every retained targeted record but changed no registered behavioral output;
- the registered adaptation intervention created no physical contrast.

A subsequent source-only audit established why the adaptation contrast was absent and narrowed the next causal locus without running capability:

- the accepted RV01 physical-field constructor fixes `adaptation_increment=0.0`;
- ordinary Field execution commits each spike's outgoing arrivals using the already-learned connection weight and delay before the R01-15 post-spike intervention can edit adaptation/refractory state;
- the accepted direct physical learner can change both `Connection.weight` and `Connection.delay_ms` during externally gated learning.

R01-16 is therefore a fresh prospective identity. It asks whether the retained traversal signature depends on the learned **propagation parameters** already committed into physical connections, rather than on the post-spike suppressors rejected/narrowed by R01-15.

## Protocol identity

```text
protocol: rv01-r01-16-propagation-factorization-v1
scope: exposed development only
R01-15 rerun: prohibited
R01-15 held-out execution: prohibited
formal / confirmatory authority: false
```

No R01-16 implementation, world grid, capability runner, result, score, source freeze, or execution authority exists at this preregistration commit.

## Primary question

Starting from one ordinary, freshly trained RV01 physical Field checkpoint, does expression-time removal of the **learned weight component**, the **learned delay component**, or both change the registered traversal/repetition signature under otherwise identical probe execution?

The purpose is causal factorization of already-learned physical propagation state. It is not to improve task success and is not an optimization study.

## Fixed intervention semantics

For each future R01-16 development world, construction must retain the exact pre-training connection inventory and the exact post-training learned connection inventory before any capability probe is opened.

Every probe arm must restore from the same post-training Field checkpoint and may differ only in the following connection-state intervention:

```text
F0  intact learned weights + intact learned delays
FW  pre-training weights + learned delays
FD  learned weights + pre-training delays
FWD pre-training weights + pre-training delays
```

The reset value is the exact value captured for the same physical edge before ordinary training. It is not a global default, fitted replacement, mean, nominal constant, or value chosen after observing R01-16 outcomes.

The following must remain identical across arms:

- topology and edge inventory;
- unit state at the common pre-probe checkpoint;
- receptor inventory;
- cue identity, magnitude and time;
- event queue before intervention, except for a separately justified fail-closed reconstruction rule if queued arrivals contain propagation values derived from the connection state being factorized;
- probe horizon and native guards;
- learned/non-learned plastic flags;
- probe non-learning contract;
- observer/scoring definitions;
- world and route identities.

No arm may retrain after intervention.

## Queue-integrity boundary

Connection weight and delay can affect the current and timing of downstream arrivals. A connection intervention performed after an arrival has already been queued could otherwise leave stale learned propagation values in that queue and create an invalid partial reset.

Therefore the implementation must fail closed unless one of these prospective conditions is established before capability:

1. the common checkpoint has no queued propagation arrival whose current/timestamp was derived from a connection value being reset; or
2. an execution-disabled construction layer can deterministically reconstruct the affected queued arrivals from the same pre-training/post-training inventories without changing any event identity or adding/removing events.

Post-hoc queue repair after seeing capability output is prohibited.

## Prospective contrast-reachability gate

Before any R01-16 capability runner exists, construction-only material must demonstrate the intervention is not structurally a no-op.

For each planned world retain:

- exact pre-training and post-training connection hashes;
- per-edge pre/post weight and delay values;
- count and identities of edges with nonzero learned weight change;
- count and identities of edges with nonzero learned delay change;
- whether each registered reset arm changes at least one physical value from F0;
- queue-integrity certificate for the common checkpoint.

The development matrix may open only if the planned grid contains at least one complete prospective world with a nonzero registered contrast for the factor under test. If learned weights never differ, `FW` is retained as structurally no-op and cannot support a weight conclusion. If learned delays never differ, `FD` is retained as structurally no-op and cannot support a delay conclusion. If neither differs, R01-16 stops before capability and a new prospective identity is required.

## Fresh development identity

R01-16 must use a new deterministic world-generation salt and a disjoint exposed-development seed/world inventory fixed before implementation results are opened. It must exclude:

- R01-15 development seeds `141500..141504`;
- reserved R01-15 held-out seeds `141600..141609`;
- any previously consumed RV01 formal/held-out world identity.

The exact fresh seed inventory and collision-search record must be committed prospectively before a capability runner is enabled.

## Registered evidence

For every future attempted probe, raw retained evidence must include enough information to verify without rerunning training:

- exact source SHA and transitive runtime-source inventory;
- world/schedule identity and hashes;
- common checkpoint hash;
- pre-training and post-training connection inventories/hashes;
- per-arm connection inventory after intervention;
- exact changed edge/field/value ledger;
- pre-probe queue inventory/hash and queue-integrity disposition;
- emitted unit/time trace;
- common-breadth trace and registered traversal metrics;
- native-guard/incomplete status;
- assertions that topology, unit state, cue, observer definitions and probe-learning state are otherwise identical.

## Registered endpoints

R01-16 reuses the already interpretable RV01 traversal endpoints rather than inventing a favorable new metric after execution:

- emitted/generated unit sequence;
- common-breadth unit sequence;
- common-breadth event count;
- common-breadth revisit count/rate;
- first-visit positions;
- ordered-retention fraction;
- exact-route recovery;
- contamination count;
- common-breadth reachability.

Connection-state effects are reported separately from behavioral interpretation. No single favorable endpoint can rescue a negative registered factorization.

## Development interpretation

The principal causal comparisons are:

```text
F0 vs FW   learned-weight contribution with learned delays retained
F0 vs FD   learned-delay contribution with learned weights retained
F0 vs FWD  combined learned-propagation contribution
FW vs FWD  delay contribution under pre-training weights
FD vs FWD  weight contribution under pre-training delays
```

A physical reset that produces no registered behavioral difference is an accepted negative result. A structurally no-op reset is reported as such and is not interpreted as causal evidence.

## Negative stopping rules

After R01-16 capability is opened, the same development identity must not be tuned and rerun if any of the following occurs:

- queue-integrity assumptions are violated;
- the retained connection ledger cannot reconstruct the registered arm state exactly;
- native guards prevent a registered cell from completing;
- all physically effective factorization arms remain behaviorally identical to F0;
- one factor is structurally no-op across the fixed grid;
- the registered endpoints fail to reproduce from retained raw traces;
- an arm changes topology, cue, unit checkpoint state, event identity, or probe-learning state outside the preregistered connection fields.

A continuation after such a result requires a new protocol identity and preserves R01-16 raw evidence unchanged.

## Formal and held-out firewall

R01-16 is development-only. It does not authorize use of the reserved R01-15 held-out worlds, any prior formal candidate, or any new held-out/formal execution. Any later confirmatory transition requires a fresh disjoint candidate, exact frozen source/package, outcome-blind review package, transparent governance record, and separate candidate-specific authorization before a one-way formal boundary.

## Next safe implementation step

The next source-only step is a construction-time factorization helper plus tests. It must:

1. bind exact pre/post connection inventories for one common checkpoint;
2. produce F0/FW/FD/FWD connection states without executing a probe;
3. prove only `weight` and/or `delay_ms` change according to the fixed arm definition;
4. fail closed on topology drift, missing edges, duplicate edges, non-finite values, or stale queued propagation state;
5. emit prospective non-no-op contrast counts/hashes;
6. contain no capability runner, task outcome, scorer, held-out path, or execution authority.
