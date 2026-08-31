# SparkBrain v0.6 Held-Out Preflight Engineering Report

## Scope

This report records the outcome-blind pre-execution validation requested before the frozen held-out
confirmatory run.

The preflight does **not** execute Primary, control, G3, G4, or G5 capability. It does not produce a
held-out pass/fail value, success fraction, selective-effect score, architecture ranking, or partial
family result.

Normative protocol:

```text
docs/V06_PROTOCOL_AMENDMENT_004_HELDOUT_PREFLIGHT_AND_ONE_WAY_EXECUTION.md
```

## Implemented contracts

```text
src/sparkbrain/evaluation/v06_confirmatory_heldout_dryrun_contract.py
src/sparkbrain/evaluation/v06_confirmatory_heldout_primary_dryrun.py
src/sparkbrain/baselines/v06/heldout_dryrun.py
src/sparkbrain/evaluation/v06_confirmatory_heldout_preflight.py
tests/v06/test_confirmatory_heldout_preflight.py
```

## Matrix shape

The preflight consumes the existing deterministic held-out world grid:

```text
5 world families × 10 seeds = 50 world specifications
```

For each world it constructs one outcome-blind declaration for all eight future conditions:

```text
50 worlds × 8 conditions = 400 adapter declarations
```

Each adapter declares the shape of all nine future evidence-domain records:

```text
400 adapters × 9 domains = 3,600 unscored schema declarations
```

These 3,600 rows are **not** `ConfirmatoryResultRecord` capability results. Every row has:

```text
status = unscored
capability_result_present = false
```

The schema says that the future frozen result will contain a Boolean `passed` field, but the preflight
does not instantiate or inspect that field.

## Shared-world equality

For every `(family, seed)` pair, the preflight verifies that all eight conditions receive:

- the same complete `HeldoutWorldParameters` mapping;
- the same world specification hash;
- the same canonical input-projection hash;
- the same unit identities and supports;
- the same paths and competing alternatives;
- the same exposure counts;
- the same threshold and cue magnitude;
- the same training/evaluation lag profiles;
- the same episode spacings;
- the same ports and raw external targets;
- the same contingency targets and phase lengths.

Condition-specific configuration differs only in the declared architecture/intervention mechanism.

## Parameter-reflection validation

The preflight checks that each adapter configuration visibly carries the held-out values rather than
replacing them with development defaults.

Verified fields include:

```text
unit_count
active_unit_ids
distractor_unit_ids
main / alternate / control paths
competition_paths
branch_exposure_counts
threshold
cue_magnitude
training_lag_profiles_ms
evaluation_lags_ms
episode_spacings_ms
boundary_lag_ms
ports
old / new / third raw targets
contingency_cycle_targets
contingency_phase_lengths
relation_reentry_gain
```

Primary and its four Field-based controls declare the ordinary Field threshold as present. G3, G4,
and G5 receive the same world threshold as part of the shared specification but explicitly disclose
that their comparator route bypasses ordinary Field thresholding.

## Branch-competition validation

For every branch-competition seed and every condition, the preflight requires:

- exactly three distinct paths;
- one shared root cue;
- one exposure count per path;
- strictly ordered close counts;
- strongest-to-weakest exposure difference equal to two;
- no branch collapsed or removed during adapter preparation.

This establishes configuration-level preservation of the genuine three-way problem. Whether an
architecture handles that competition successfully remains unobserved.

## Resource schema

Every future `(family, seed, condition)` cell has one complete resource-schema declaration:

```text
400 resource schema declarations
```

The declared future record includes:

- observed training events;
- generated internal events;
- persistent-state entries;
- interventions;
- parameter/state count;
- wall-clock time;
- ordinary Field-threshold presence and crossings;
- threshold bypass;
- explicit Assembly entries;
- typed-head count;
- scalar-reward observations;
- privileged-information inventory.

Dynamic values are deliberately absent in preflight:

```text
measurements_present = false
```

Actual resource measurements can be recorded only when the frozen capability run executes.

## Isolation and privilege disclosure

Static AST/import checks require G3/G4/G5 source to avoid imports from `sparkbrain.v06` and the
Primary confirmatory adapter.

Dry-run modules are also checked not to import or call the development capability entrypoints.

Declared comparator differences are explicit:

```text
G3  generic external transition predictor; Field-threshold bypass
G4  explicit Assembly state; Field-threshold bypass
G5  three typed functional heads + scalar reward; Field-threshold bypass
```

Primary and the four controls declare no Assembly, typed head, scalar reward, or privileged input.

## Fail-closed guards

The focused suite verifies rejection when a declaration attempts to:

- inspect Primary runtime state;
- execute capability during preflight;
- count generated activity as external observation;
- commit positive learning from generated activity;
- hide G3 threshold bypass;
- omit G4 Assembly privilege;
- omit G5 scalar-reward or typed-head privilege;
- omit a resource field;
- produce duplicate resource identities;
- create an incomplete domain schema;
- change adapter input away from the shared world;
- attach a capability result to an unscored row.

## Determinism

The complete 400-adapter preflight matrix is built independently twice. The matrix hash and world-grid
hash must match exactly.

The 50 world specifications also remain seed-deterministic and individually hashable.

## Validation

GitHub Actions run `33271388509` passed on Python 3.11 and Python 3.13. Both jobs completed:

```text
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

The later documentation-only synchronization is validated separately on the current branch head.

## Current readiness

```text
pure held-out world grid:                 implemented
outcome-blind adapter declarations:       400 / 400
unscored domain schema declarations:    3,600 / 3,600
resource schema declarations:             400 / 400
shared-input validation:                 pass
parameter-reflection validation:         pass
branch-preservation validation:          pass
static comparator isolation:             pass
fail-closed safety declarations:         pass
capability executions observed:             0
held-out manifest ready:                 false
held-out capability adapters ready:      0 / 8
code SHA frozen:                         false
confirmatory execution allowed:          false
```

The preflight is ready for code/protocol review. It does not make the held-out capability adapters
ready and does not cross the freeze boundary.

## Remaining sequence

1. implement all eight real held-out capability adapters against this exact shared contract;
2. validate adapter interface shape, deterministic replay, isolation, complete resource emission, and
   artifact paths without scoring outcomes;
3. review code and protocol;
4. freeze Git SHA, world-grid hash, manifest hash, thresholds, exclusions, result/resource schemas,
   adapter inventory, execution command, and artifact locations;
5. cross the no-change boundary;
6. execute the 3,600-record capability matrix once;
7. retain all Primary failures and comparator successes without post-hoc edits.

## Scientific boundary

This preflight establishes experimental wiring and outcome blindness only. It supplies no new
Level-1, Level-2, Level-3, generalization, superiority, or architecture-necessity evidence.
