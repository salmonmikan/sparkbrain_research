# RV01 R01-16 preregistration amendment 001

Date: 2026-09-12  
Status: **PROSPECTIVE DEVELOPMENT-ONLY / BINDING BEFORE CAPABILITY / NOT EXECUTED**

This amendment binds the two review findings raised against
`rv01-r01-16-propagation-factorization-v1` before any R01-16 capability is
opened. It does not alter or reinterpret R01-15 evidence, does not execute an
R01-16 probe, and does not authorize held-out/formal capability.

## Binding

```text
parent protocol: rv01-r01-16-propagation-factorization-v1
amendment: rv01-r01-16-propagation-factorization-amendment-001
scope: exposed development only
formal / held-out authority: false
capability result present: false
```

The parent preregistration remains historical. This amendment is additive and
must be applied prospectively to every future R01-16 construction/result.

## 1. Causal reachability gate

A learned edge changing somewhere in the graph is not sufficient to open a
factor contrast. Before capability, each fixed world/probe cell must receive a
construction-only reachability certificate computed from:

- the complete registered physical unit inventory, including isolated units;
- the exact pre-training connection inventory;
- the exact post-training connection inventory;
- the preregistered cue source unit(s);
- the preregistered probe horizon.

The unit inventory is part of the certificate identity. A cue ID absent from
that inventory fails closed. A valid registered cue on an isolated unit is not
an error: it yields no reachable changed edges and therefore an ineligible
factor cell unless another simultaneous registered cue supplies causal reach.
All connection endpoints must themselves belong to the same registered unit
inventory.

Reachability is structural and outcome-blind. For each physical edge, traversal
uses the conservative delay `max(pre_training.delay_ms, post_training.delay_ms)`.
The earliest conservative arrival time is computed from the cue source(s).
A changed edge is **contrast-reachable** only when its source is reachable and
traversing that edge can arrive at its target no later than the fixed probe
horizon.

Factor conclusions may use only cells with at least one contrast-reachable edge
for that factor:

```text
weight-eligible cell: >=1 contrast-reachable learned-weight edge
delay-eligible cell:  >=1 contrast-reachable learned-delay edge
combined-eligible:    weight-eligible OR delay-eligible
```

A factor whose fixed grid has fewer than two independently generated eligible
worlds is `INSUFFICIENT_REACHABLE_REPLICATION` and cannot receive a supported or
unsupported causal classification. A structurally changed but unreachable edge
is retained in raw construction evidence but cannot count as a negative causal
probe.

## 2. Fixed primary endpoint and decision rule

The primary behavioral object is the exact pair:

```text
(emitted/generated unit sequence, common-breadth unit sequence)
```

For a matched arm contrast, the primary effect is binary and exact:

```text
PRIMARY_DIFFERENT = either sequence differs exactly
PRIMARY_IDENTICAL = both sequences are exactly identical
```

No post-hoc numeric effect-size threshold is used. The exact sequence change is
the preregistered primary effect. Event counts, revisit counts/rates,
first-visit positions, ordered-retention fraction, exact-route recovery,
contamination, and common-breadth reachability remain secondary magnitude and
interpretation fields only; they cannot change a primary classification.

### Weight classification

For every weight-eligible world/probe cell evaluate both matched contrasts:

```text
F0 vs FW
FD vs FWD
```

A cell is:

```text
WEIGHT_SUPPORT_CELL  if both contrasts are PRIMARY_DIFFERENT
WEIGHT_NEGATIVE_CELL if both contrasts are PRIMARY_IDENTICAL
WEIGHT_DISCORDANT    otherwise
```

Across the fixed grid:

```text
WEIGHT_SUPPORTED
  iff >=2 independent weight-eligible worlds exist and every weight-eligible
  cell is WEIGHT_SUPPORT_CELL.

WEIGHT_UNSUPPORTED
  iff >=2 independent weight-eligible worlds exist and every weight-eligible
  cell is WEIGHT_NEGATIVE_CELL.

WEIGHT_MIXED
  otherwise, when >=2 eligible worlds exist.
```

### Delay classification

For every delay-eligible world/probe cell evaluate both matched contrasts:

```text
F0 vs FD
FW vs FWD
```

The same non-compensatory rule applies:

```text
DELAY_SUPPORTED   = all eligible cells differ in both delay contrasts
DELAY_UNSUPPORTED = all eligible cells are identical in both delay contrasts
DELAY_MIXED       = any other replicated pattern
```

### Combined classification and precedence

`F0 vs FWD` is evaluated only on combined-eligible cells.

```text
COMBINED_SUPPORTED
  iff >=2 independent combined-eligible worlds exist and every combined-eligible
  cell is PRIMARY_DIFFERENT.

COMBINED_UNSUPPORTED
  iff >=2 independent combined-eligible worlds exist and every combined-eligible
  cell is PRIMARY_IDENTICAL.

COMBINED_MIXED
  otherwise, when >=2 eligible worlds exist.
```

Interpretation precedence is fixed:

1. report `WEIGHT_*` and `DELAY_*` independently;
2. report `COMBINED_*` separately;
3. do not let a combined effect rescue an unsupported individual factor;
4. do not let any secondary endpoint rescue or overturn the primary sequence
   classification;
5. any discordant/mixed pattern is retained as `MIXED`, not resolved by choosing
   a favorable endpoint after inspection.

A `COMBINED_SUPPORTED` result with both individual factors `UNSUPPORTED` is
reported descriptively as **combined-only / non-factorized propagation effect**;
it is not reassigned to either factor.

## 3. Construction evidence required before a runner

Every future R01-16 planned cell must retain, before capability exists:

- complete registered physical unit identities;
- cue source unit identities;
- fixed probe horizon;
- exact pre/post connection hashes;
- conservative earliest-arrival map hash;
- all learned weight-changed and delay-changed edges;
- reachable subsets for each factor;
- exact reachability certificate hash;
- queue-integrity disposition;
- factor eligibility status.

The capability runner must fail closed if the certificate does not reconstruct
from the retained unit/connection inventories and registered cue/horizon.

## 4. Negative stopping rule refinement

After the fixed development identity is opened, unreachable factor cells are not
converted into behavioral negatives. If the fixed grid lacks the required two
eligible worlds for a factor, that factor ends as
`INSUFFICIENT_REACHABLE_REPLICATION`; extending the grid would require a new
prospective protocol identity rather than adding worlds after inspecting output.

All other parent negative stopping rules remain unchanged.

## Next safe step

Implement and test the construction-only conservative reachability certificate,
then bind a fresh deterministic R01-16 development world/seed grid and collision
search before any capability runner is created.
