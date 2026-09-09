# RV01 fixed-evidence audit — 2026-09-09

## Boundary

Append-only audit of PR #25 at `216eec3ae37c7a49f41d4631152d96b5d4a082bc`
and R01-13A/R01-14A evidence available at
`bc08eeb4e329e2bc8d5593ce468121cc9f64dacb`. No runtime, scoring function,
historical report, raw result, threshold, or seed is changed. No experiment was
rerun. R01-12F remains consumed; R01-13B remains not admitted; R01-14 held-out
capability remains closed. This audit does not raise a claim grade.

## Independently checked evidence

The existing GitHub Actions artifacts were downloaded and their JSON bytes hashed
before read-only recalculation. All three raw-file hashes match their manifests:

| Evidence | Artifact ID | Raw JSON SHA-256 |
|---|---:|---|
| R01-12F | 9965780771 | `e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4` |
| R01-13A | 10059084120 | `1ab43a8950be572b163e7bba4950b23d5258933e5463dc3d944f41eaea2adf60` |
| R01-14A | 10087415924 | `4a214059cacc66d473776de7b46455c959ce0ac5c7089c6acfafbc9e0ef91e25` |

Recalculation from R01-12F final probe rows gives 200 probes per architecture:
Field/reservoir mean ordered retention `1.0 / 0.9016666666666666`, exact-route
count `80 / 80`, and contamination `720 / 589`. These support PR #25's narrow
coverage/selectivity trade-off, not general memory superiority.

R01-13A breadth-matched family mean ordered retention is tied in all five families:
disjoint `1.0`, shared-cue `1.0`, shared-prefix `0.7777777777777778`, reversal
`0.8888888888888888`, and dense-load `0.875`. Thus R01-13B's admission condition
remains unsatisfied.

R01-14A raw common-breadth prefixes independently give 100 paired probes, mean
events `5.46 / 6.36`, 59 Field-fewer-event pairs, 41 ties, and no Field-more-event
pair. This is an emitted-event result, not measured wall-clock or physical-time
speed, energy efficiency, or better route correctness.

## Finding 1 — R01-14 AUC protocol/implementation mismatch

`RV01_R01_14_TRAVERSAL_DYNAMICS_PROTOCOL.md` describes normalized discovery AUC
as the mean cumulative distinct fraction normalized by final distinct count.
For trace length T, final distinct count D, and cumulative distinct counts C_t,
that description implies `sum(C_t) / (T * D)`.

The fixed `traversal_dynamics.py::_traversal_metrics` instead computes:

```text
sum(C_t) / (D * (D + 1) / 2 + D * (T - D))
```

The denominator is the area under the earliest-possible distinct discovery
curve for the same T and D. For `(1, 2, 3)`, the documented fraction is `2/3`
but the implemented metric is `1.0`. For `(1, 2, 1, 2, 3)`, they are `2/3`
and `5/6`, respectively. Empty traces return `0.0` by implementation convention.

Disposition: preserve the fixed formula and raw bytes. Interpret recorded AUC
values only as **ideal-front-loaded-discovery-normalized AUC** and explicitly
retain this discrepancy as a protocol deviation for that secondary endpoint.
Do not silently claim the protocol-defined AUC was evaluated. The independently
recalculated primary events-to-common-breadth endpoint does not use AUC and is
unaffected. Exact-formula synthetic regression tests are recommended on a
separate audit branch; no old execution-source pin is replaced.

## Finding 2 — PR #25 untrained-branch inference is unsupported

`future_untrained` identifies the probed route's training status; it does not
establish that generated units belong uniquely to that future route.

For each fixed Field probe before its route's exposure, this audit constructed
the union of units in routes already trained by that phase, then intersected
generated units with the future route's expected units outside that union.
The number of generated previously-unlearned expected-unit occurrences is zero
in every family. Before that subtraction, shared-prefix contributes 30
probe/unit overlaps; all are shared units already exposed through other routes.
The other four families contribute zero expected-unit overlaps.

Consequently, PR #25's statements that untrained branches activate before
exposure must not be used to strengthen the over-activation explanation.
Contamination and equal exact-route counts still support low selectivity,
without that unsupported inference. This corroborates the existing review
comment; it does not change any historical probe label or metric.

## PR #25 reproducibility follow-up

The PR changes only a report and a derived manifest. Its existing review asks
for retained R01-12D raw evidence, a deterministic manifest generator, and an
append-only Results Ledger entry. Those requests remain appropriate. This
audit independently recalculated R01-12F but did not obtain/recalculate the
R01-12D raw rows; no full PR #25 approval is implied. The missing intermediate
reservoir records also prevent phase-by-phase architecture superiority claims.

## Prospective protocol recommendation — not execution approval

A new protocol may investigate why repeated emissions differ. It must not
rescue the failed breadth-matched retention hypothesis or open old held-out
seeds. First preregister the exact local timing primitive after source review;
candidate mechanisms are refractory/reset behavior, propagation timing, and
recurrent residual state. These are hypotheses, not identified causes.

Use a fresh seed namespace, unchanged training/weights/topology and resource
contract, and probe-only paired intervention plus exact restoration and sham
controls. Retain disjoint routes as a positive diagnostic of general traversal
effects and shared-cue as a reference where the old difference tied. Record
unique-state first visits, repeats, event prefixes, layer/time grouping, and
censoring at a fixed horizon. Predefine breadth budgets independently of the
intervention so a reduced reachable set cannot manufacture apparent efficiency;
report non-reaching probes rather than dropping them.

Primary inference should be within-substrate causal change under the declared
intervention, with restoration, not an unrestricted Field-versus-reservoir winner
claim. Same-time output ordering and reservoir score-ranked layer flattening
require separate sensitivity checks before attributing event-index differences
to physical timing. Coverage, contamination, exact recovery, event work, and
elapsed time remain separate outcomes. No new experiment was run by this audit.
