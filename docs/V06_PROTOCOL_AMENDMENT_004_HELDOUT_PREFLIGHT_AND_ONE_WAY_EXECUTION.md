# SparkBrain v0.6 Protocol Amendment 004
## Outcome-Blind Held-Out Preflight and One-Way Confirmatory Execution

**Amendment date:** 2026-08-30  
**Branch:** `v06`  
**Adopted before:** any held-out capability execution  
**Preserves:** all development qualification results and Protocol Amendments 001–003

## 1. Decision

Held-out preparation and held-out capability evaluation are separate phases.

Pre-execution validation may proceed immediately and repeatedly. The 3,600-record held-out
capability matrix must not execute until the world contract, all eight capability adapters, resource
accounting, thresholds, exclusions, schemas, code SHA, and manifest hash are reviewed and frozen.

```text
preflight validation       repeatable before freeze
held-out capability run    one fresh execution after freeze
```

## 2. Permitted before freeze

The following tests may run without exposing held-out capability outcomes:

- deterministic generation of all 50 held-out world specifications;
- exact shared-world equality across all eight conditions;
- adapter input and configuration shape;
- propagation of topology, active/distractor support, threshold, magnitude, lag profiles, episode
  spacing, branch alternatives, boundary ports, and contingency cycles;
- complete resource-record schema for every future `(family, seed, condition)` cell;
- comparator isolation from Primary runtime state;
- explicit comparator privilege disclosure;
- genuine three-branch preservation;
- taxonomy, self-confirmation, threshold-bypass, and privileged-information fail-closed guards;
- deterministic schema-only dry runs;
- output-field and artifact-schema validation;
- manifest readiness checks that remain false before freeze.

These tests may construct configuration projections and unscored schema records. They must not call a
capability entrypoint or populate a pass/fail result.

## 3. Prohibited before freeze

The following are prohibited:

- executing Primary or any control/comparator on held-out events to determine capability;
- creating a held-out `passed` value;
- calculating success fraction, selective effect, relation accuracy, or architecture ranking;
- inspecting partial family or seed outcomes;
- tuning threshold, gain, lag tolerance, branch policy, resource budget, scoring threshold, or world
  definition from held-out behaviour;
- changing a held-out world because an architecture failed it;
- marking held-out capability adapters ready merely because schema-only adapters pass.

Development and qualification capability tests may continue to run. Only held-out capability
outcomes remain sealed.

## 4. Required sequence

```text
1. Define and validate 50 pure held-out worlds.
2. Implement all eight capability adapters against exactly that shared contract.
3. Run outcome-blind validation only:
   - shape;
   - deterministic replay;
   - isolation;
   - world equality;
   - parameter reflection;
   - resource coverage;
   - fail-closed guards;
   - unscored output schema.
4. Perform code and protocol review.
5. Freeze:
   - full Git SHA;
   - held-out world-grid hash;
   - confirmatory manifest hash;
   - thresholds;
   - exclusions;
   - result schema;
   - resource schema;
   - adapter inventory;
   - execution command and artifact paths.
6. Cross the no-change boundary.
7. Execute one fresh 3,600-record capability matrix.
8. Preserve all Primary failures and comparator successes without post-hoc edits.
```

## 5. Schema-only dry-run contract

The preflight matrix has the same identity shape as the future result matrix:

```text
50 worlds × 8 conditions = 400 adapter declarations
400 adapters × 9 evidence domains = 3,600 domain schema declarations
```

A schema declaration is not a result record. It must contain:

```text
status = unscored
capability_result_present = false
```

It may declare that the future result has a Boolean `passed` field, but must not instantiate that
field before freeze.

## 6. Adapter-readiness distinction

Two different readiness concepts are mandatory:

### Schema/preflight ready

The adapter can consume the shared world contract, exposes complete configuration/resource/output
schemas, passes isolation and safety guards, and performs no capability evaluation.

### Capability ready

The implemented architecture can execute the complete held-out episode protocol and produce all
frozen result and resource artifacts. This status may be set only after code review and immediately
before freeze.

Schema readiness must never automatically set `ConditionRegistration.adapter_ready = true` for the
held-out manifest.

## 7. Shared-input invariant

For each `(family, seed)` pair, all eight conditions must consume byte-equivalent canonical world
input.

Condition-specific architecture projections may differ only in the preregistered intervention or
comparator mechanism. They may not change:

- unit identities or supports;
- main, alternate, control, or competing paths;
- exposure counts;
- thresholds or magnitudes;
- lag profiles or episode spacing;
- boundary ports or raw targets;
- contingency targets or phase lengths;
- structural seed/token.

## 8. Comparator isolation and disclosure

G3, G4, and G5 must not import or inspect Primary runtime state.

Their privileges remain explicit:

```text
G3: external predictor; ordinary Field threshold bypass disclosed
G4: explicit Assembly state; threshold bypass disclosed
G5: typed heads and scalar reward; threshold bypass disclosed
```

A missing privilege declaration is a preflight failure. Comparator privilege does not invalidate a
clean Primary result, but it changes scientific interpretation.

## 9. Fail-closed rule

Any of the following blocks freeze:

- missing adapter or domain schema;
- different world hash across conditions;
- unreflected threshold, lag, topology, branch, or contingency field;
- branch competition collapsed before capability execution;
- missing or duplicate resource schema;
- comparator access to Primary runtime state;
- generated activity counted as observation or positive learning;
- undeclared Assembly, typed-head, reward, or threshold-bypass privilege;
- capability entrypoint called by preflight code;
- nonzero capability-execution count;
- held-out manifest becoming ready before code/hash freeze.

## 10. Scientific boundary

Passing preflight supports only that the future held-out experiment is wired consistently and remains
outcome-blind. It supplies no evidence that Primary, G3, G4, G5, or any control succeeds or fails on a
held-out capability.

The 3,600-record matrix remains scientifically untouched until the one-way freeze boundary is
crossed.
