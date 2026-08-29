# SparkBrain v0.6 Freeze Note

Status: **Frozen research milestone**  
Frozen branch: `archive/v06-pre-rv01`  
Frozen commit: `f55f2ad9df1484a7ffb88850097ec5c5a7a41791`  
Date: 2026-08-29

## Purpose

SparkBrain v0.6 is frozen as the last numbered pre-1.0 research milestone before moving to an explicitly named Research Version track.

This archive is not a declaration that v0.6 is complete in the sense of a finished cognitive architecture. It preserves the exact engineering and scientific state from which the next research program begins.

## What v0.6 established

v0.6 removed predeclared Assembly and functional taxonomy from the Primary runtime and demonstrated engineering candidates for:

- endogenous Spark generation under same-input/different-history conditions;
- sequential anonymous endogenous chains;
- anonymous Field-to-world boundary events;
- externally stabilized anonymous relations;
- relation reversal and reacquisition;
- re-entry of anonymous relation state through ordinary Field dynamics;
- observer/evaluator taxonomy isolation.

All prior claim boundaries remain in force.

## Principal unresolved architectural issue

The next research program is motivated by a remaining human-defined substrate in v0.6.

### G1

`LocalTemporalExpectation` explicitly defines the unit of learnable temporal relation as a source-target pair and stores lag, magnitude and polarity statistics. The system therefore does not discover the relation representation itself; it is given a local-transition abstraction.

### G2

`SparseLocalTransitionAdaptation` explicitly defines eligibility, confirmation, contradiction, reliability and confidence scaling for those paths. External consistency is correctly kept separate from semantic reward, but the adaptation form is still designer-specified.

Therefore v0.6 must **not** be interpreted as showing that reusable transition structure arises solely from generic Field plasticity.

## Transition rule

Future work must not be named `v0.7` merely because it follows v0.6.

The next program belongs to a Research Version series because it may replace or invalidate central abstractions rather than incrementally extend a stable architecture.

The first track is:

`RV01 — Endogenous Transition Substrate`

Primary question:

> Can the functional work currently performed by G1/G2 emerge from more general local Field/state plasticity without predeclaring source-target transition records, path identities, confirmation counters, reliability objects, or proposal-specific eligibility as privileged cognitive substrate?

## Preservation rule

- Do not rewrite v0.6 results to make later mechanisms appear inevitable.
- Do not silently replace G1/G2 in this archive.
- Later Research Versions must compare against frozen v0.6 as an explicit baseline.
- Negative results in RV01 do not invalidate v0.6 engineering findings; they constrain the stronger endogenous-plasticity claim.
