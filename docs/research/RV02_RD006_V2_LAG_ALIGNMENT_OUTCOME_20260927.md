# RV02-RD006 v2 lag-alignment development outcome

Date: 2026-09-27 JST  
Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`  
Revision: `rv02-rd006-external-learning-reachability-a-v2-lag-alignment`  
Source head: `7896433af675b77b1f442e9efaf268d16564c564`  
Phase at execution: `OPEN_DEVELOPMENT`  
Claim ceiling: `SYSTEM`  
Classification: `DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT`

## Preserved execution

The one R147-authorized bounded paired matrix completed once from the exact
remote source head. The sole science-affecting change from v1 was within-route
external-event spacing `5.0 ms -> 5.5 ms`; initial connection delay and every
other fixed v1 condition were retained.

- artifact: `artifacts/rv02_rd006/external_learning_reachability_a_v2_lag_alignment/attempt-001/artifact.json.gz`
- manifest: `artifacts/rv02_rd006/external_learning_reachability_a_v2_lag_alignment/attempt-001/manifest.json`
- artifact payload SHA-256: `5898fdcb75b10747fb88f8a19329f2d063422bb5012e80683c2c413cbbfb76d6`
- deterministic gzip SHA-256: `7ce4ffa4366f60290b26ead6edd31f9a2083f0822949c7c11815aefe8df5c468`
- matrix status: `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`
- reachable cells: 0
- bounded cells: `opposing-reversal / external_learning_on`

The artifact contains all 816 inspected clocks from 832 planned arm-clocks,
complete raw/hidden spike rows, eligible connected-source rows, all 356 ordinary
updates, and the one bounded-failure decision point. Its embedded payload digest
and compressed-file digest were independently verified after execution.

## Gate result

No complete non-exploded cell contained a scheduled return with the required two
distinct structurally connected hidden sources inside the unchanged `0.5–6.5 ms`
lag window. `ready_cell_ids` is empty.

The largest eligible-source count at any inspected return was one:

- `shared-prefix / external_learning_on`: maximum eligible sources 1;
- `opposing-reversal / external_learning_on`: maximum eligible sources 1 before
  the bounded stop;
- every other arm: maximum eligible sources 0.

The timing revision changed the observed diagnostic surface but did not open the
prospective reachability gate. Several ON arms produced hidden activity (144
hidden spikes across the matrix), while OFF arms remained silent. Hidden firing
alone is not the gate and is not a capability result.

## Bounded arm

`opposing-reversal / external_learning_on` inspected 32 of 48 planned clocks and
then reached the unchanged `max_spikes_per_run` guard at event
`rd006-v2-ext-000032`. The ceiling was not raised and the remaining 16 clocks are
unobserved, not inferred.

## Disposition and claim boundary

The prospective v2 contingency is therefore:

`PRESERVE_INCOMPLETE_AND_STOP_NO_CEILING_INCREASE`

and, for every complete cell without an eligible two-source clock:

`PRESERVE_NEGATIVE_AND_STOP_NO_FURTHER_V2_TIMING_CHANGE`.

This result does not establish capability, comparative support, composition
contribution, or novelty. It does not authorize E0/E1/ES, scale expansion,
reservoir comparison, learner-boundary changes, topology/threshold/gain/stimulus
changes, lag-window changes, event-ceiling expansion, or a second v2 matrix.
Fresh Evidence Analyst reconciliation is required for any successor.

v1 and RD005 were not modified or reopened. No FORMAL identity was executed or
consumed, and no held-out or capability scoring occurred.
