# SparkBrain v0.6 Held-Out Pre-Execution Status

## Current decision

```text
complete development qualification:  PASS
held-out world shape contract:       IMPLEMENTED
resource/privilege schema:           IMPLEMENTED
held-out condition adapters:         NOT READY
code SHA frozen:                     NO
manifest hash frozen:                NO
3,600-record confirmatory run:       NOT EXECUTED
PR #10 release-ready:                NO
```

## What changed after development qualification

The complete 648-record development matrix showed that Primary, G3, G4, and G5 all solve the three
qualification families. The current tasks therefore demonstrate capability but do not establish
architectural uniqueness.

The next work is deliberately not another feature layer. It is a pre-execution contract for a harder,
shared, held-out comparison.

## Pure held-out world specification

`src/sparkbrain/evaluation/v06_confirmatory_heldout_spec.py` now defines 50 deterministic pure-data
world specifications:

```text
5 held-out families × 10 seeds
```

The generator does not run any architecture and therefore does not expose a capability outcome.

The families are:

1. sparse identity/topology permutation;
2. edge-lag dispersion and nonuniform episode spacing;
3. a broad ordinary Field threshold/magnitude band;
4. genuine three-branch competition with close exposure counts;
5. six-phase external contingency cycles with five changes.

Every condition must consume the exact same world specification for a given family and seed.

## Resource and privileged-information contract

`src/sparkbrain/evaluation/v06_confirmatory_resources.py` defines one mandatory evaluator-side
resource record per `(family, seed, condition)`.

Required inventory:

- observed training events;
- generated internal events;
- persistent state entries;
- intervention count;
- parameter/state count;
- wall-clock time;
- ordinary Field threshold presence and crossings;
- explicit threshold bypass;
- explicit Assembly entries;
- typed-head count;
- scalar-reward observation count;
- complete privileged-information inventory.

Condition-specific disclosure rules are fail-closed:

- Primary and four controls must report no Assembly, typed-head, reward, or other privileged input;
- G3 must report that it is an external predictor and bypasses ordinary Field thresholding;
- G4 must disclose explicit Assembly state;
- G5 must disclose typed prediction/boundary/persistence heads and scalar reward;
- a missing or duplicate resource record blocks matrix completion.

These records belong only to evaluation and do not enter the Primary runtime.

## Why capability outcomes are not run yet

Running held-out capability tests before the world contract, adapters, resource schema, thresholds,
exclusions, code SHA, and artifact schema are frozen would turn the held-out phase into another
iterative development grid.

The correct order is:

1. validate the 50 pure world specifications;
2. review the exact branch and contingency semantics;
3. implement all eight adapters against the shared data contract;
4. validate only interface shape, deterministic replay, isolation, complete resource reporting, and
   result-record coverage;
5. freeze the full Git SHA and hashes;
6. execute one fresh held-out matrix;
7. preserve all failures and comparator successes without changing the worlds or thresholds.

## Remaining held-out blockers

### Primary adapter

Must consume per-edge lag profiles, sparse active support, real simultaneous alternatives, broad
threshold bands, and repeated contingency cycles without replacing them with qualification defaults.

### Null/control adapters

- no-endogenous must remove all internal generation while preserving the identical raw world;
- random-matched must match the Primary event/time/current/energy profile in each held-out world;
- readout-only must retain structural proposals but never generate a Field Spark;
- shuffled-relation must preserve earlier Dynamics while breaking the learned relation-to-reentry
  mapping.

### G3/G4/G5 comparators

Each must consume the same held-out world specification and emit the same nine-domain schema.
Comparator privilege must remain explicit in the resource record.

### Freeze

The following remain unfrozen:

- code SHA;
- held-out world-grid hash;
- confirmatory manifest hash;
- adapter version inventory;
- result and resource artifact schemas;
- complete execution command and local reproduction bundle.

## Scientific boundary

The new held-out specification and resource schema do not upgrade the scientific claim. Current
results remain development engineering evidence with an explicit-state-dominant persistence result
and no established architectural uniqueness.
