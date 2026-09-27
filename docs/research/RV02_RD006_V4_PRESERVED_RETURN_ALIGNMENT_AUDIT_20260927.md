# RV02-RD006 v4 preserved-output return-alignment audit

Date: 2026-09-27 JST

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Phase: `RESULT_EXPOSED_DEVELOPMENT`

Authority: Evidence Analyst R157

Classification: `DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT`

## Scope and preserved identity

This audit reads only the preserved R162 v4 D0 artifact. It does not run new
dynamics, alter an artifact, rescore or reclassify the result, change a parameter,
score capability, or use held-out data.

- result head: `50112626ef6a4da364e3fa9268e8feb0d723ea7f`
- execution source head: `44bef35c90f24a11e27000e3c328778733da92b6`
- preserved artifact payload SHA-256:
  `e40a88cd596b79d1a6b78030c8f7ea3baac5fc5c8579551b7494b37f6b89d3ba`
- preserved gzip file SHA-256:
  `62b3ffb6d52926b583b006799d88511c9f840b626bc776cdcaf6ee2f857faf61`
- audit payload SHA-256:
  `0883e5ffc271f2a32eadb232178ef529f7256188f602869d8b5790a603bd55a5`
- rendered audit JSON SHA-256:
  `37cce402dcdd1a816117eca68284ccde48afea26923e2cad359aebf9aa2512a1`
- deterministic gzip audit file SHA-256:
  `7eea2a1dff11986e4431366da013ddcea170c190c21c609254ea575552baf589`

The fixed gate remains two distinct actually spiking hidden sources, each with a
non-negative edge to the current visible return target and an observed lag of
0.5–6.5 ms at the same scheduled return clock.

## Exhaustive ON-clock classification

All 416 planned ON clocks receive exactly one mutually exclusive classification.
The 400 inspected clocks are classified from preserved bytes. The 16 unobserved
`opposing-reversal / ON` clocks are identified from the paired preserved OFF
schedule and classified only as ceiling-censored; no ON dynamics are inferred.

| Missing-second-source cause | Complete ON | Bounded ON | Total |
| --- | ---: | ---: | ---: |
| `NO_OTHER_SOURCE_IN_PRESERVED_CONSTRUCTION` | 176 | 8 | 184 |
| `NO_SECOND_HIDDEN_SPIKE` | 185 | 20 | 205 |
| `SPIKE_WITHOUT_ELIGIBLE_EDGE_TO_CURRENT_RETURN_TARGET` | 7 | 4 | 11 |
| `ELIGIBLE_EDGE_BUT_LAG_OUTSIDE_0_5_TO_6_5_MS` | 0 | 0 | 0 |
| `ADJACENT_CLOCK_NOT_SAME_CLOCK` | 0 | 0 | 0 |
| `CEILING_CENSORED` | 0 | 16 | 16 |
| **Total** | **368** | **48** | **416** |

The minimum observed gate deficit is one source. Seven inspected ON clocks have
exactly one eligible source and the other 393 have none, for a summed deficit of
793 source-clock opportunities. The 16 censored clocks are excluded from that
sum.

The seven one-source clocks are unchanged from the preserved v3 surface:

- `shared-prefix`: events 35, 39, 43, and 47, source 44 to return target 34;
- `opposing-reversal`: events 27 and 31, source 37 to target 20, and event 29,
  source 36 to target 8.

No adjacent-clock pair supplies the missing second eligible identity, and no
clock fails because two current-target eligible-edge sources both spiked but one
missed the fixed lag window. Compared with the preserved v3 audit, the sole prior
adjacent-clock classification moves into current-target edge failure; the total
one-source eligibility surface remains seven clocks and no two-source clock
appears.

## PORT_TO_HIDDEN update-to-later-spike linkage

The preserved trace locates all 58 `PORT_TO_HIDDEN` update target spikes by target
source identity and target time inferred from the update's source return time plus
recorded lag.

| ON family | P2H updates | Later same-source spike | Later same-source eligible spike |
| --- | ---: | ---: | ---: |
| `disjoint-routes` | 0 | 0 | 0 |
| `shared-cue` | 8 | 6 | 0 |
| `shared-prefix` | 4 | 3 | 3 |
| `opposing-reversal` | 4 | 4 | 3 |
| `dense-load` | 16 | 16 | 0 |
| `capacity-pressure` | 26 | 22 | 0 |
| **Total** | **58** | **51** | **6** |

This is descriptive linkage, not causal attribution. Hidden spike rows do not
carry the update's `target_event_id`, so the join uses target source ID and the
exact time implied by source clock plus lag. More importantly, there is no
matched counterfactual trajectory with a particular update disabled. The bytes
therefore show that 51 update-target sources spike again later and six later
appear as dynamically eligible, but they do not identify whether the particular
P2H update caused that recurrence or eligibility.

## Trace sufficiency and unknown fields

The preserved trace is sufficient to classify each inspected ON return clock by
structural source coverage, actual hidden firing, current-target edge, fixed lag
window, and same-clock eligibility. It is also sufficient to test immediately
adjacent clocks and to describe same-source recurrence after P2H updates.

It is not sufficient to identify:

- outcomes for the 16 ceiling-censored clocks;
- a direct update-target-event to hidden-spike-event join;
- the later trajectory with each P2H update removed while all else is fixed;
- the causal contribution of an update to a later spike or eligible return clock.

## Disposition

`NO_PROPOSAL`.

The v4 result remains `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`. The preserved bytes
support failure classification and descriptive recurrence, but not a causal
separation between the P2H learner update and concurrent network state. They do
not identify one fresh scientific invariant that can be changed without mixing
multiple live explanations.

E0/E1/ES, another dynamics matrix, ceiling changes, scale expansion, reservoir
comparison, capability scoring, and successor implementation remain unauthorized.
Fresh Evidence Analyst reconciliation is required.

## Reproduction

```bash
python scripts/audit_rv02_rd006_v4_return_alignment.py \
  --artifact artifacts/rv02_rd006/external_learning_reachability_a_v4_d0_execution/attempt-001/artifact.json.gz \
  --output /tmp/preserved_return_alignment_audit_v4.json

gzip -n -9 -c /tmp/preserved_return_alignment_audit_v4.json > \
  artifacts/rv02_rd006/external_learning_reachability_a_v4_d0_execution/audits/preserved_return_alignment_audit_v4.json.gz

python -m pytest -q \
  tests/test_rv02_rd006_v4_return_alignment_audit.py
```
