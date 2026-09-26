# RV02-RD006 Stage D0 development contract

`RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A` is a fresh OPEN_DEVELOPMENT object.
It is not RD005, does not reopen RD005, and carries no inherited confirmatory credit.

Stage D0 runs the six exposed RV02 families at scale 1 (48 units, degree 8, seed
92701). Each cell clones one initial state into two arms. The only arm difference is
ordinary external-only Field learning OFF versus ON. Hidden-return learning remains
OFF in both arms. Threshold 0.5, initial weight 0.05, initial delay 5 ms, visible-to-
hidden gain 4, input magnitude 1, topology, schedule, and measurement clocks are
fixed across the pair.

The diagnostic reports whether at least two distinct hidden sources spike and have
a plastic, non-negative edge to the current visible return event within 0.5–6.5 ms.
It does not execute E0/E1/ES learning, score capability, use held-out data, expand
scale, or compare a reservoir. Any later step requires a fresh Evidence Analyst
reconciliation.
