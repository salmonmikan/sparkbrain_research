# SparkBrain v0.6 Confirmatory Readiness Report

## Current decision

```text
qualification adapter-complete:    true
qualification execution-ready:     false
confirmatory execution-ready:      false
PR #10 merge-ready for release:    false
```

Qualification remains non-executable through the manifest only because `code_ref` is intentionally
`UNFROZEN`. The complete matrix has nevertheless been exercised as an engineering test at the branch
commit recorded by CI.

Confirmatory execution remains blocked because none of the eight adapters has passed the five-family
held-out world contract.

## Programme order completed before confirmatory work

The revised order requested after V06-11 has been implemented:

```text
V06-12  relation re-entry into later normal-rule Field Dynamics
V06-13  direct persistence-locus reset/transplant
V06-14  supporting validity assays
V06-15  complete eight-condition development qualification
```

Current engineering findings include:

- learned anonymous relation state re-enters and changes later normally thresholded Field Dynamics;
- reversal and reacquisition change that later Dynamics;
- demonstrated experience effects follow explicit anonymous G1 local-transition state and boundary-
  consistency state, not matched Field state alone;
- forward missing-middle, prefix, branching, omission, retrospective, and shortcut-control assays
  exist as supporting diagnostics;
- Primary and all required controls/comparators now implement one normalized nine-domain interface;
- strict scoring enforces null, intervention-selectivity, taxonomy, self-confirmation, and control-
  contract thresholds.

None of this is the frozen 5 × 10 held-out confirmatory execution.

## Complete development qualification matrix

```text
3 world families × 3 seeds × 8 conditions × 9 evidence domains
= 648 / 648 complete unique records
```

Condition coverage:

```text
Primary:                  81 records
no-endogenous:            81 records
random endogenous matched:81 records
readout-only:             81 records
shuffled relation:        81 records
G3 recurrent:             81 records
G4 explicit Assembly:     81 records
G5 typed functional heads:81 records
```

The complete matrix and deterministic replay passed on Python 3.11 and 3.13.

## Strict engineering score

```text
Primary overall success fraction:        1.00
Primary minimum family fraction:         1.00
null false-positive fraction:            0.00
minimum targeted-minus-matched effect:   1.00
taxonomy hash match fraction:            1.00
self-confirmation violations:               0
control contract fraction:               1.00
```

The strict scorer rejects Primary raw success if any control or safety gate fails. Missing or
inconsistent metrics also block scoring.

## Primary qualification

```text
worlds passed:          9 / 9
records passed:        81 / 81
deterministic replay:  PASS
```

The result spans identifier permutation, timing perturbation, and Field threshold/magnitude
perturbation.

The result preserves the persistence limitation:

```text
local-transition transplant  -> learned endogenous response transfers
local-transition reset       -> learned endogenous response disappears
matched Field state alone    -> learned response does not transfer

boundary-consistency transplant -> relation re-entry transfers
boundary-consistency reset      -> relation re-entry disappears
```

## Control qualification

```text
control worlds contract-complete: 36 / 36
control records complete:        324 / 324
self-confirmation violations:      0
taxonomy mismatch:                 0
```

Expected patterns:

| Condition | Positive evidence allowed in qualification |
|---|---|
| no-endogenous | taxonomy non-interference only |
| random endogenous matched | taxonomy non-interference only |
| readout-only | taxonomy non-interference only |
| shuffled relation | early Primary domains plus taxonomy; re-entry and persistence fail |

The matched-random condition matches Primary proposal count, scheduled time, effective current,
total energy, and generation-depth profile while removing learned sequential parentage.

## Comparator qualification

### G3 — generic recurrent/transition predictor

```text
worlds passed:  9 / 9
records passed: 81 / 81
```

A much simpler external transition predictor can reproduce the current development evidence. This
means the qualification worlds do not establish that excitable Field Dynamics are necessary.

### G4 — explicit Assembly-conditioned system

```text
worlds passed:  9 / 9
records passed: 81 / 81
```

An isolated comparator with explicit Assembly IDs and Assembly-conditioned rollout/relation state
also solves the development worlds. Observer-only Assembly is therefore not established as a
performance requirement.

### G5 — typed functional-head system

```text
worlds passed:  9 / 9
records passed: 81 / 81
```

An isolated system with explicit prediction, action, reward, and memory heads plus privileged scalar
reward also solves the development worlds.

## Development interpretation

The strict scorer returns:

> Primary and at least one comparator are supported; architectural uniqueness is not established.

All three comparators are supported in the current development grid.

This is not a failure of the Primary implementation. It is a failure of the current development
worlds to discriminate architectural necessity.

## Manifest state

### Qualification phase

All eight adapter paths are registered and marked qualification-ready. The manifest remains:

```text
code_ref = UNFROZEN
```

Therefore readiness remains false until a reviewed commit is frozen.

### Confirmatory phase

Qualification readiness is not reused. All eight adapters remain `adapter_ready = false` for the
five-family held-out phase until each implements and passes that world contract.

## Confirmatory target

```text
5 held-out families × 10 seeds × 8 conditions × 9 evidence domains
= 3,600 fresh records
```

Held-out family contracts:

1. sparse identity/topology permutation;
2. lag dispersion;
3. threshold/magnitude bands;
4. genuine branch competition;
5. repeated contingency cycles.

## Remaining blockers

### 1. Held-out world implementation

Current adapters accept only the three qualification families. The five held-out families must be
implemented for Primary, controls, G3, G4, and G5 without silently reducing them to renamed versions
of the development worlds.

Branch competition is especially important: it must contain real simultaneous alternatives rather
than a single deterministic stored chain.

### 2. Comparator fairness and resource accounting

Before freeze, the shared report must include at least:

- observed training events;
- generated internal events;
- persistent state size;
- intervention count;
- wall-clock time;
- condition-specific privileged information;
- whether normal Field thresholds are present or bypassed.

G5's scalar reward and typed heads must remain explicit rather than being hidden as ordinary
external events.

### 3. Code and manifest freeze

After held-out adapter qualification:

- freeze a full lowercase 40-character Git SHA;
- freeze the manifest hash;
- freeze thresholds and exclusions;
- freeze result/artifact schemas;
- prohibit post-outcome threshold or world changes.

### 4. Fresh held-out execution

The 3,600-record matrix must be generated after freeze. Development/qualification records cannot be
relabelled as held-out evidence.

## Persistence limitation carried into confirmatory work

The current architecture is best described as:

```text
Dynamic Field
+ explicit anonymous local-transition memory
+ explicit anonymous external-consistency memory
+ normal-rule reinjection and boundary coupling
```

Confirmatory work must test this architecture honestly. It must not add a new persistent mechanism
merely to rescue a distributed-Field interpretation after the direct reset/transplant result.

## Interpretation remains fail-closed

- Primary passes, comparators fail: Primary supported under the frozen scope.
- Primary and comparators pass: Primary capability supported; architectural uniqueness not
  established.
- Primary fails, comparator passes: comparator-only success; negative for the Primary hypothesis.
- all fail: tested capability unsupported.
- Primary raw success with any null/safety/control failure: Primary support rejected.

No control or comparator result may be relabelled as Primary success.

## Next implementation work

1. implement a common five-family held-out world specification;
2. adapt all eight conditions without tuning against held-out outcomes;
3. qualify the held-out adapter contract and resource accounting;
4. freeze code SHA, manifest, thresholds, exclusions, and schemas;
5. execute the fresh 3,600-record matrix;
6. preserve all negative results and strongest counterexamples;
7. proceed to V06-16 Brain Lab/audit/release only after the complete result review.

## Release boundary

`main` remains unchanged and PR #10 remains Draft while confirmatory readiness is false.
