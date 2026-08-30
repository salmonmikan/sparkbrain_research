# RV01 R01-12 Status

## Current decision

```text
R01-11 physical resource/safety boundary: complete
R01-12A world contract:                   complete
R01-12B development runner:               next
R01-12C reset/transplant/order controls:  pending
R01-12D reservoir comparison:             pending
R01-12E held-out review/freeze:            pending
held-out interference capability:         not executed
main merge:                               blocked
```

## R01-12A completed

The continual-interference programme now has a deterministic pure-data world contract:

```text
5 families × 3 development seeds = 15 development worlds
5 families × 10 held-out seeds   = 50 held-out worlds
```

Development seeds are `0, 1, 2`. Held-out seeds are `100` through `109`. The two sets are disjoint.

Families:

1. disjoint routes;
2. three shared-cue branches;
3. three shared-prefix branches;
4. opposing directed-edge reversal plus disjoint control;
5. dense route load exceeding the frozen active-edge budget.

Each world fixes:

- anonymous route units and exposure counts;
- training and probe order;
- ordinary Field threshold and cue magnitude;
- temporal lag;
- maximum active outgoing edges;
- maximum total active edges;
- reversal route identities where applicable.

The contract contains no runtime transition model, Assembly, route label available to the runtime,
correct branch, reward, utility, or semantic field.

## Held-out boundary

The 50 held-out worlds may be regenerated, hashed, and shape-validated. They must not be executed for
capability before R01-12B through R01-12D are complete and the following are frozen:

- physical learner configuration;
- Field and safety budgets;
- evaluation metrics and thresholds;
- comparator configuration and state budget;
- result/resource schemas;
- world-grid hash;
- full Git SHA.

No held-out pass/fail, route-retention score, branch-collapse result, or comparator ranking has been
created at R01-12A.

## Scientific purpose

RV01 currently demonstrates external-only learning in ordinary physical connection weights/delays,
with real Field continuation and a viable reservoir explanation. R01-12 asks whether that physical
edge state can coexist under multiple experiences or whether it behaves as a fragile pairwise edge
table.

Passing R01-12A establishes only that the falsification worlds were specified before capability
inspection. It supplies no new evidence for capacity, low interference, distributed memory, or
architectural uniqueness.

## Next implementation

R01-12B must:

1. reuse the current RV01 physical learner and ordinary Field runtime;
2. execute only the 15 development worlds;
3. train routes in the frozen order and probe every route after each phase;
4. record connection hashes, weights/delays, active-edge counts, branch coverage, contamination,
   queue/spike/safety status, ignored endogenous writes, persistent-state size, and wall-clock time;
5. preserve all failures without increasing edge budgets or changing world definitions;
6. leave the 50 held-out capability worlds untouched.
