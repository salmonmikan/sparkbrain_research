# SparkBrain v0.6 Held-Out Pre-Execution Status

## Current decision

```text
complete development qualification:       PASS
former 100-series capability calls:       QUARANTINED
fresh world generation:                   v06-confirmatory-candidate-002
fresh candidate seeds:                    1000 through 1009
fresh world specifications:               50
resource/privilege schema:                IMPLEMENTED
outcome-blind dry-run adapters:            8 / 8
adapter declarations:                   400 / 400
resource schema declarations:           400 / 400
unscored domain schema declarations:  3,600 / 3,600
candidate capability executions:            0
real candidate capability adapters:      NOT READY
held-out manifest ready:                 NO
code SHA frozen:                         NO
world-grid hash frozen:                  NO
manifest hash frozen:                    NO
execution seal issued:                   NO
formal 3,600-record capability run:       NOT EXECUTED
PR #10 release-ready:                    NO
```

## Correction to the earlier status

A repository review found that an older file named as an adapter preflight called actual capability entrypoints for a subset of held-out-labelled 100-series worlds. It created real Boolean result fields and dynamic resource measurements before the freeze boundary.

Those calls were not the complete formal 3,600-record run, but they were still capability exposure. They are therefore ineligible as confirmatory evidence.

The historical code is preserved at:

```text
archive/v06-pre-freeze-capability-exposure-20260830
```

The active `v06` branch removes the unsealed capability dispatcher, capability adapters, and execution tests. Ordinary CI now exercises development tests and schema-only candidate preflight only.

Normative correction:

```text
docs/V06_PROTOCOL_AMENDMENT_005_CAPABILITY_EXPOSURE_QUARANTINE.md
```

## Fresh candidate world generation

The contaminated 100-series seed range is excluded. The replacement candidate set is:

```text
generation: v06-confirmatory-candidate-002
seeds:      1000 through 1009
families:   5
worlds:     50
```

The new generation uses a new RNG salt and new unit/port identities, topology support, timing values, thresholds, branches, and contingency details. It may be built and hashed before freeze, but no capability runtime may consume it.

## Accepted outcome-blind preflight

The current preflight constructs configuration and schema declarations only:

```text
50 worlds × 8 conditions = 400 adapter declarations
400 adapters × 9 domains = 3,600 unscored domain schemas
```

Every domain schema remains:

```text
status = unscored
capability_result_present = false
```

Every resource schema remains:

```text
measurements_present = false
```

Preflight validates:

- exact deterministic world reconstruction;
- identical canonical world input across all eight condition declarations;
- propagation of topology/support, threshold, magnitude, lag, episode spacing, ports, branches, exposure counts, and contingency cycles;
- genuine three-way branch preservation;
- complete result/resource schemas;
- comparator isolation from Primary runtime;
- explicit comparator privilege and Field-threshold-bypass disclosure;
- fail-closed taxonomy, self-confirmation, observation, learning, and privilege guards;
- held-out manifest readiness remaining false.

It does not instantiate a capability result or dynamic resource measurement.

## Execution seal

`src/sparkbrain/evaluation/v06_confirmatory_execution_seal.py` defines the future hard gate. A valid freeze record must bind:

- full Git SHA;
- exact manifest hash;
- world-generation ID;
- 50-world grid hash;
- threshold hash;
- exclusion hash;
- result-schema hash;
- resource-schema hash;
- adapter-inventory hash;
- execution-command hash;
- artifact-path hash;
- explicit approval.

Any mismatch keeps execution prohibited. The current manifest remains `UNFROZEN`, all eight candidate capability adapters remain unready, and no seal exists.

## Remaining sequence

```text
1. Keep candidate-002 capability outcomes sealed.
2. Complete outcome-blind preflight and static review.
3. Rework/review the eight real adapters on development-only fixtures or an isolated staging branch.
4. Verify interface and resource-emitter shape without candidate execution.
5. Review code and protocol.
6. Freeze SHA, world-grid hash, manifest hash, thresholds, exclusions, schemas, inventory, command, and artifact paths.
7. Commit and verify the execution seal.
──────── no-change boundary ────────
8. Execute one fresh 5 × 10 × 8 × 9 = 3,600-record candidate matrix.
9. Preserve every Primary failure and comparator success without post-hoc edits.
```

## Scientific boundary

The current repository contains development qualification evidence and outcome-blind preflight infrastructure. It contains no scientifically valid held-out capability result for candidate-002 and no established architectural superiority or necessity.
