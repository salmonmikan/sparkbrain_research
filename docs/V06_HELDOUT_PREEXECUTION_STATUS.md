# SparkBrain v0.6 Held-Out Pre-Execution Status

## Current decision

```text
complete development qualification:       PASS
held-out world shape contract:            IMPLEMENTED
resource/privilege schema:                IMPLEMENTED
outcome-blind dry-run adapters:            8 / 8
adapter declarations:                   400 / 400
resource schema declarations:           400 / 400
unscored domain schema declarations:  3,600 / 3,600
preflight capability executions:            0
real held-out capability adapters:       NOT READY
held-out manifest ready:                 NO
code SHA frozen:                         NO
world-grid hash frozen:                  NO
manifest hash frozen:                    NO
3,600-record capability run:             NOT EXECUTED
PR #10 release-ready:                    NO
```

## Protocol boundary

Protocol Amendment 004 makes preflight and capability evaluation separate phases:

```text
docs/V06_PROTOCOL_AMENDMENT_004_HELDOUT_PREFLIGHT_AND_ONE_WAY_EXECUTION.md
```

Preflight may run repeatedly before freeze. Held-out capability may execute once only after all real
adapters, resource emission, thresholds, exclusions, schemas, code SHA, world-grid hash, manifest
hash, adapter inventory, command, and artifact paths are reviewed and frozen.

## What changed after development qualification

The complete 648-record development matrix showed that Primary, G3, G4, and G5 all solve the three
qualification families. Those worlds demonstrate capability but do not establish architectural
uniqueness.

The next work is therefore not another feature layer and not an early peek at held-out performance.
It is an outcome-blind pre-execution contract for a harder shared comparison.

## Pure held-out world specification

`src/sparkbrain/evaluation/v06_confirmatory_heldout_spec.py` defines 50 deterministic pure-data world
specifications:

```text
5 held-out families × 10 seeds
```

The generator runs no architecture and exposes no capability outcome.

The families are:

1. sparse identity/support permutation;
2. edge-lag dispersion and nonuniform episode spacing;
3. broad ordinary Field threshold/magnitude bands;
4. genuine three-branch competition with close exposure counts;
5. six-phase external contingency cycles with five changes.

Every condition must consume the exact same world specification for a given `(family, seed)`.

## Outcome-blind preflight matrix

The preflight constructs configuration declarations only:

```text
50 worlds × 8 conditions = 400 adapter declarations
400 adapters × 9 domains = 3,600 unscored schema declarations
```

Every domain declaration has:

```text
status = unscored
capability_result_present = false
```

There is no `passed` value, capability metric, success fraction, selective-effect score, architecture
ranking, or partial held-out family result.

The held-out manifest deliberately remains:

```text
adapter_ready = false  for all 8 conditions
code_ref = UNFROZEN
ready = false
```

## Preflight validation completed

The current suite checks:

- complete 50-world deterministic replay;
- one adapter declaration for every world and condition;
- byte-equivalent canonical world input across all eight conditions;
- complete consumption of all `HeldoutWorldParameters` fields;
- reflection of topology/support, threshold, magnitude, lag profiles, episode spacing, paths, ports,
  branches, relation re-entry gain, and contingency cycles;
- genuine three-way branch preservation for every condition;
- one complete resource-schema declaration per future world/condition cell;
- static G3/G4/G5 isolation from Primary runtime and Primary adapter imports;
- explicit threshold-bypass, Assembly, typed-head, and scalar-reward disclosure;
- fail-closed taxonomy, self-confirmation, Primary-inspection, capability-execution, and privilege
  guards;
- future result-schema shape without producing a result;
- independent full-matrix rebuild with identical hash.

GitHub Actions run `33271388509` passed installation, Ruff, local readiness, the default test suite,
and bundle validation on Python 3.11 and Python 3.13.

## Resource and privileged-information contract

`src/sparkbrain/evaluation/v06_confirmatory_resources.py` defines one mandatory evaluator-side
resource record per future `(family, seed, condition)`.

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

Condition-specific disclosure rules remain fail-closed:

- Primary and four controls: no Assembly, typed head, reward, or other privileged input;
- G3: external predictor and ordinary Field-threshold bypass disclosed;
- G4: explicit Assembly state and threshold bypass disclosed;
- G5: typed heads, scalar reward, and threshold bypass disclosed;
- missing, duplicate, or invalid records block completion.

The preflight declares the complete resource schema but does not invent dynamic measurements. Actual
values remain unavailable until frozen capability execution.

## Why capability outcomes remain sealed

Running held-out capability before all adapters and the full freeze would turn the held-out phase into
another development grid. A failure could influence threshold, gain, lag tolerance, branch policy,
resource budget, world shape, or scoring even without deliberate tuning.

The required order is:

1. validate and review the 50 pure worlds;
2. implement all eight real capability adapters against the shared contract;
3. validate shape, deterministic replay, isolation, input equality, parameter reflection, complete
   resource emission, output schema, and fail-closed guards without scoring outcomes;
4. perform code/protocol review;
5. freeze SHA, hashes, thresholds, exclusions, schemas, inventory, commands, and artifact paths;
6. cross the no-change boundary;
7. execute one fresh 3,600-record capability matrix;
8. preserve every Primary failure and comparator success without post-hoc edits.

## Remaining held-out blockers

### Primary capability adapter

Must actually consume per-edge lag profiles, sparse active support, genuine simultaneous
alternatives, broad threshold bands, and repeated contingency cycles without replacing them with
qualification defaults.

### Null/control capability adapters

- no-endogenous must remove all internal generation while preserving the same raw world;
- random-matched must match Primary event/time/current/energy profiles in each world;
- readout-only must retain structural proposals but never generate a Field Spark;
- shuffled-relation must preserve earlier Dynamics while breaking learned relation-to-reentry
  mapping.

### G3/G4/G5 capability adapters

Each must execute against the same held-out world and emit the same nine-domain and resource schemas.
Comparator privilege remains explicit. No comparator may inspect Primary runtime state.

### Freeze

Still unfrozen:

- full Git SHA;
- held-out world-grid hash as a normative artifact;
- confirmatory manifest hash;
- thresholds and exclusions;
- adapter version inventory;
- result and resource artifact schemas;
- execution command and artifact paths;
- local reproduction bundle.

## Scientific boundary

Passing the outcome-blind preflight establishes consistent experimental wiring only. It does not
upgrade the scientific claim, reveal held-out performance, or establish Level 1–3 generalization,
architectural superiority, or necessity.
