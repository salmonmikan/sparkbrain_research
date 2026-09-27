# RV02-RD006 v3 preserved-result causal-opportunity audit

Date: 2026-09-27 JST

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Phase: `RESULT_EXPOSED_DEVELOPMENT`

Authority: Evidence Analyst R152

Classification: `DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT`

## Scope and preserved identity

This audit reads only the preserved R159 v3 D0 artifact. It does not run new
dynamics, alter the artifact, change a parameter, score capability, or use held-out
data.

- result head: `540fa54f45a8cdc467eb2695270035cb9332f2fb`
- execution source head: `8867c0565e25a0c76749c12eec7f4c03238b7aef`
- preserved artifact payload SHA-256:
  `a71e324014b92ecf5680608f60f78e431c192f353d29af0633193546eec7a8da`
- preserved gzip file SHA-256:
  `ad7dc60af79681a30d67f1c0d2a4e39607a8984122f52bf9a65949950772b3f9`
- audit payload SHA-256:
  `19d160df7d7e53d3bf8f038e6d5d314026a47f645c488615d146f78661b3c564`
- deterministic gzip audit file SHA-256:
  `f7515e286b6fc9a60b4553df5b6a4b78e7c9c88f9d29d5850cf69dfed1a9767c`

The fixed gate remains two distinct actually spiking hidden sources, each with a
non-negative edge to the current visible return target and an observed lag of
0.5–6.5 ms at the same scheduled return clock.

## Exhaustive clock classification

All 832 planned clocks receive exactly one mutually exclusive classification. The
816 inspected clocks are classified from preserved ON/OFF bytes. The 16 unobserved
`opposing-reversal / ON` clocks are identified from the preserved paired OFF
schedule and classified only as ceiling-censored; no ON-arm dynamics are inferred.

| Missing-second-source cause | OFF | ON | Total |
| --- | ---: | ---: | ---: |
| `NO_OTHER_SOURCE_IN_PRESERVED_CONSTRUCTION` | 188 | 184 | 372 |
| `NO_SECOND_HIDDEN_SPIKE` | 228 | 205 | 433 |
| `SPIKE_WITHOUT_ELIGIBLE_EDGE_TO_CURRENT_RETURN_TARGET` | 0 | 10 | 10 |
| `ELIGIBLE_EDGE_BUT_LAG_OUTSIDE_0_5_TO_6_5_MS` | 0 | 0 | 0 |
| `ADJACENT_CLOCK_NOT_SAME_CLOCK` | 0 | 1 | 1 |
| `CEILING_CENSORED` | 0 | 16 | 16 |
| **Total** | **416** | **416** | **832** |

The minimum observed deficit was one source, reached on seven ON-arm clocks. Every
other inspected clock was two sources short. Summed over the 816 inspected clocks,
the deficit was 1,625 source-clock opportunities. The 16 ceiling-censored clocks
are excluded from that sum.

### Complete versus bounded cells

| Arm / completion | Construction absent | No second spike | Spike without edge | Lag outside | Adjacent only | Censored | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OFF / complete | 188 | 228 | 0 | 0 | 0 | 0 | 416 |
| ON / complete | 176 | 185 | 7 | 0 | 0 | 0 | 368 |
| ON / bounded | 8 | 20 | 3 | 0 | 1 | 16 | 48 |

The sole adjacent-clock case is `opposing-reversal / ON` event
`rd006-v2-ext-000030`: source 36 is eligible on the immediately preceding clock and
source 37 on the immediately following clock, but neither forms a two-source set at
the current clock. This is temporal dispersion, not gate satisfaction.

## What the preserved ON activity shows

The seven clocks with one eligible source remain confined to:

- `shared-prefix / ON`: four clocks, always source 44 to target 34;
- `opposing-reversal / ON`: three clocks, source 37 to target 20 twice and source
  36 to target 8 once.

Ten ON clocks contain at least two distinct hidden sources firing, but fewer than
two have an eligible non-negative edge to the current return target. Seven of these
occur in the complete `capacity-pressure / ON` cell and three before the ceiling in
`opposing-reversal / ON`.

No clock fails because a second spiking source had a non-negative edge but missed
the fixed lag window. The preserved failure surface is therefore dominated by
construction coverage and absent second firing, with a smaller current-target edge
gap—not by the 0.5–6.5 ms window.

## Recommendation boundary

The v3 result remains `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`. E0/E1/ES, a second v3
matrix, ceiling changes, scale expansion, reservoir comparison, capability scoring,
and any implementation of a successor remain unauthorized.

If Evidence Analyst keeps the line open, this audit recommends at most one fresh
prospective revision with one changed invariant:

`ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY`

The prospective change would permit explicitly specified `PORT_TO_HIDDEN` ordinary
external updates while hidden-return learning remains disabled. The two-source
same-clock gate, 0.5–6.5 ms window, v3 topology and schedule, threshold, gain,
stimulus, and resource ceilings should remain fixed. This is a new learner-boundary
hypothesis, not a v3 rerun or a claim that it will succeed.

The reason is narrow: the preserved PORT-to-PORT-only learner occasionally creates
one eligible source but never two. Another timing/topology retune would be less
diagnostic than testing whether the ordinary learner's boundary prevents the second
hidden source from becoming reachable.

## Reproduction

```bash
python scripts/audit_rv02_rd006_v3_causal_opportunity.py \
  --artifact artifacts/rv02_rd006/external_learning_reachability_a_v3_d0_execution/attempt-001/artifact.json.gz \
  --output /tmp/preserved_causal_opportunity_audit_v3.json

gzip -n -9 -c /tmp/preserved_causal_opportunity_audit_v3.json > \
  artifacts/rv02_rd006/external_learning_reachability_a_v3_d0_execution/audits/preserved_causal_opportunity_audit_v3.json.gz

python -m pytest -q \
  tests/test_rv02_rd006_v3_causal_opportunity_audit.py
```
