# SparkBrain v0.6 Pre-Freeze Review Report

## Review verdict

```text
outcome-blind world/schema preflight:  ACCEPTED
active-branch capability seal:         PASS
fresh candidate world generation:     ACCEPTED FOR PREFLIGHT
real capability adapters:              NOT READY
resource measurement emitters:         NOT READY
code/manifest freeze:                  NOT APPROVED
3,600-record capability execution:     PROHIBITED
```

This review authorizes continued development-only testing and repeated schema-only preflight. It does not authorize any capability execution on `v06-confirmatory-candidate-002`.

## 1. Review correction

The review found that an earlier adapter-preflight implementation called real capability entrypoints on 100-series held-out-labelled worlds before freeze. Although it did not complete or formally score the 3,600-record matrix, it exposed capability behaviour and was not outcome-blind.

Actions taken:

- classified seeds `100..109` as contaminated development material;
- preserved the exact historical repository state on `archive/v06-pre-freeze-capability-exposure-20260830`;
- removed the unsealed capability dispatcher, Primary/control/comparator capability modules, and their execution tests from active `v06`;
- prohibited use of the former results for confirmatory evidence or tuning;
- created fresh candidate generation `v06-confirmatory-candidate-002` with seeds `1000..1009` and a new RNG salt;
- added an active-branch barrier test so ordinary CI rejects reintroduction of an unsealed held-out capability entrypoint.

The formal 3,600-record confirmatory matrix has not been executed.

## 2. Requested preflight checklist

### 2.1 All eight conditions read one shared world specification

**Status: PASS**

For each of 50 `(family, seed)` pairs, all eight declarations must contain identical:

- complete `HeldoutWorldParameters` mappings;
- world-specification hashes;
- canonical input-projection hashes.

Condition-specific differences are restricted to the declared architecture or control mechanism.

### 2.2 Fifty worlds reconstruct exactly from fixed seeds

**Status: PASS**

The complete world grid is rebuilt independently and compared byte-for-byte through canonical state and grid hashes. Every world has a unique specification hash. Candidate seeds are exactly `1000..1009` and are disjoint from quarantined seeds `100..109`.

### 2.3 Primary/control/G3/G4/G5 input conditions match

**Status: PASS at schema/configuration level**

The preflight verifies equality of:

- unit count and active/distractor support;
- main, alternate, control, and competition paths;
- branch exposure counts;
- threshold and cue magnitude;
- training and evaluation lag profiles;
- episode spacings and boundary lag;
- ports and raw external targets;
- contingency targets and phase lengths;
- relation re-entry gain;
- structural generation token.

This is not yet an execution-level equality result because real candidate capability adapters remain absent from the active branch.

### 2.4 Resource record coverage

**Status: PASS for schema; measurements not yet available**

Exactly 400 resource-schema declarations exist, one for every future world/condition execution cell. Required fields include training observations, generated events, persistent-state entries, interventions, parameter/state count, wall-clock time, Field-threshold use/bypass, Assembly entries, typed heads, scalar reward observations, and privilege inventory.

Preflight requires `measurements_present = false`. Dynamic values must not be fabricated before frozen execution.

### 2.5 Comparator isolation from Primary internal state

**Status: PASS for static preflight boundary**

AST/import checks reject comparator imports from `sparkbrain.v06` and the Primary confirmatory adapter. Dry-run modules must not import or call development capability entrypoints. Safety declarations with `reads_primary_runtime_state = true` fail closed.

The real candidate adapters require another review before freeze.

### 2.6 Branch competition remains genuinely three-way

**Status: PASS at configuration level**

For every branch-competition seed and all eight declarations:

```text
path count = 3
all paths distinct
one shared root cue
one exposure count per path
strongest > runner-up > third
strongest - third = 2
```

No adapter declaration may collapse the problem to one path before execution.

### 2.7 Threshold, lag, and topology changes reach adapters

**Status: PASS at configuration level**

The preflight checks direct equality between world fields and architecture projections. It additionally verifies:

- ten distinct Primary thresholds in the threshold-band family;
- ten distinct G3 evaluation-lag configurations in the lag-dispersion family;
- unique configuration hashes for all 50 worlds within every condition;
- exact active/distractor support and path propagation.

Primary and four Field controls declare ordinary Field thresholding as present. G3/G4/G5 receive the same threshold value but explicitly declare Field-threshold bypass.

### 2.8 Taxonomy, self-confirmation, and privilege guards fail closed

**Status: PASS**

Tests explicitly reject:

- Primary-runtime inspection;
- capability execution during preflight;
- generated events counted as external observations;
- generated events committing positive learning;
- hidden G3 threshold bypass;
- omitted G4 Assembly privilege;
- omitted G5 typed-head or scalar-reward privilege;
- incomplete or duplicate resource schemas;
- incomplete domain schemas;
- a capability result attached to an unscored row.

### 2.9 Output-schema-only dry run

**Status: PASS**

The safe preflight constructs:

```text
50 worlds × 8 conditions = 400 adapter declarations
400 declarations × 9 domains = 3,600 domain schema declarations
```

Every domain declaration remains:

```text
status = unscored
capability_result_present = false
```

No `passed` value, capability metric, success fraction, selective-effect score, ranking, or partial held-out result is created.

## 3. Execution barrier

The active `v06` branch now contains no unsealed held-out capability entrypoint or execution test. CI scans all active `v06_confirmatory_heldout*.py` modules and rejects capability-like entrypoint definitions/calls or direct `ConfirmatoryResultRecord` construction.

The future execution seal binds:

- exact 40-character Git SHA;
- exact manifest hash;
- world-generation ID;
- world-grid hash;
- thresholds and exclusions hashes;
- result and resource schema hashes;
- adapter inventory hash;
- execution command hash;
- artifact-path hash;
- explicit approval.

The current manifest has `code_ref = UNFROZEN`, all eight candidate capability adapters are unready, and `require_execution_seal(...)` rejects execution.

## 4. CI result

GitHub Actions run `33292753970` on active HEAD `77b0ba5aee5143a441db8876ffe4800d0c19cd30` passed on Python 3.11 and 3.13:

```text
Install:          PASS
Ruff lint:        PASS
Local readiness: PASS
Full pytest:      PASS
Bundle validation: PASS
```

CI contains development capability tests and candidate schema-only preflight. It contains no candidate-002 capability execution.

## 5. Remaining blockers before freeze

1. Rework and review all eight real capability adapters on development-only fixtures or an isolated staging branch.
2. Prove the real adapters consume the exact candidate contract by interface construction, without executing candidate events.
3. Complete result and resource emitter review, including unique execution identities and artifact atomicity.
4. Review comparator fairness, matched event/time/current/energy budgets, and declared privileges.
5. Review branching semantics so all alternatives remain present through the actual execution path.
6. Finalize the code SHA, world-grid hash, manifest hash, thresholds, exclusions, schemas, adapter inventory, command, and artifact paths.
7. Commit and independently approve the freeze record.
8. Cross the no-change boundary.
9. Execute the candidate-002 3,600-record matrix exactly once.

## 6. Scientific interpretation

Passing this review establishes that the experiment is currently wired for an outcome-blind preflight and protected against accidental active-branch execution. It provides no new evidence about whether Primary, G3, G4, G5, or any control succeeds on fresh candidate worlds.

The current scientific result remains the development finding: SparkBrain can execute the tested closed loop, but the demonstrated experience carriers are explicit anonymous transition/consistency states and the development tasks do not establish architectural uniqueness.
