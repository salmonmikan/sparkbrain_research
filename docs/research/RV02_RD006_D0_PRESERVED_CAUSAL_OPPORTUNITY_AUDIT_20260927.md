# RV02-RD006 D0 preserved-result causal-opportunity audit

Date: 2026-09-27 JST

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Phase: `RESULT_EXPOSED_DEVELOPMENT`

Authority: Evidence Analyst R145, reaffirmed by R146

Classification: `DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT`

## Scope and preserved identity

This audit uses only the preserved Stage D0 v1 source and artifact. It does not
execute new dynamics, introduce a new seed, change a parameter, score capability,
use held-out data, or infer unobserved clocks.

- result head: `49b91ca801522f3d6685ebd22097a1e64f9234c9`
- preserved source head: `b4fbd9cc92f9e9d02f4ec1ff69084ab31f924b0c`
- preserved artifact SHA-256: `c27951973b25a83ea3a23ce16b97e6634ac513929aee605c8af417410e12209c`
- audit payload SHA-256: `269138e81d7c282cc809b2920f0b381e9afa6ab5a3e49a45c5f707a928763341`
- deterministic gzip audit file SHA-256: `0e500f9788aeddaa42e8db666568d1cc2122040a20fe350b6f855e6bb35b3dac`

The audit reconstructs the deterministic v1 topology and external schedule, checks
their digests against each preserved cell, and combines those structures with the
already-preserved per-clock hidden-spike rows.

### Verification-procedure nonconformance

During local verification, the pre-existing
`tests/test_rv02_rd006_external_learning_reachability.py` was initially invoked
alongside the new audit tests. That test module calls `run_cell` and `run_arm`, so it
performed non-persisted local dynamics despite the R145 audit restriction requiring
no new dynamic execution. Its outputs were not used, scored, or persisted, and it did
not alter the preserved v1 source or artifact. Once detected, no further dynamic test
was run; audit verification was restricted to the preserved-byte audit test module.

This is an execution-procedure nonconformance, not a new scientific result. It must
remain visible to the Evidence Analyst when reconciling the audit.

## Complete clock census

There are 816 preserved inspected clocks. One additional scheduled clock is the
recorded bounded-explosion decision point for `opposing-reversal / external_learning_on`;
the 16 clocks after that point remain unobserved and are not inferred.

| Failure class | Count |
| --- | ---: |
| `NO_STRUCTURAL_RETURN_EDGE` | 124 |
| `STRUCTURAL_EDGE_NO_HIDDEN_SPIKE` | 684 |
| `HIDDEN_SPIKE_OUTSIDE_LAG` | 8 |
| `ELIGIBLE_SINGLE_SOURCE_ONLY` | 0 |
| `ELIGIBLE_MULTI_SOURCE` | 0 |
| `BOUNDED_EXPLOSION_BEFORE_DECISION` | 1 |

Every family has at least one inspected clock whose scheduled visible target has a
structural incoming edge from a hidden unit. Structural return opportunity is
therefore not globally absent in v1.

The only eight inspected clocks with a spike from a structurally connected hidden
source occur in the ON arms of `shared-prefix` and `capacity-pressure`. In all eight,
the hidden spike is simultaneous with the scheduled visible return (`lag = 0.0 ms`).
The fixed eligible window is `0.5–6.5 ms`, so every such observation is 0.5 ms below
the lower bound. No eligible single-source or multi-source clock exists in the
preserved bytes.

## Ordinary external learner edge-class audit

The ordinary external learner creates traces only for externally scheduled unit
targets. In the fixed D0 schedule, all such targets are PORT units. A direct update
therefore requires both endpoints to be externally traced PORT units.

Across the preserved ON arms, all 356 ordinary updates are `PORT_TO_PORT`:

| Family | ON-arm ordinary updates |
| --- | ---: |
| disjoint-routes | 44 |
| shared-cue | 44 |
| shared-prefix | 44 |
| opposing-reversal | 36 |
| dense-load | 112 |
| capacity-pressure | 76 |

Under this actual trace rule and schedule, direct `PORT_TO_HIDDEN`,
`HIDDEN_TO_PORT`, and `HIDDEN_TO_HIDDEN` ordinary updates are impossible. The
observed hidden firing in ON arms is therefore an indirect consequence of changed
PORT-to-PORT dynamics, not direct hidden-return credit assignment.

## Bounded-explosion arm

Before the fixed event ceiling, the `opposing-reversal / external_learning_on` arm
preserved 32 of 48 planned clocks. All 32 have structural hidden-to-return edges but
no spike from a connected hidden source. The failing scheduled clock targets PORT 9,
which has five structural hidden incoming sources, but execution stopped before a
decision row could be produced. No pre-ceiling eligible causal opportunity was
observed, and no conclusion is assigned to the 16 unobserved clocks.

## Interpretation boundary

The preserved v1 result remains `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`.

This audit narrows the failure surface:

1. structural hidden-to-visible edges exist, so the failure is not a global absence
   of return edges;
2. most inspected clocks fail because a structurally connected hidden unit does not
   spike;
3. the few connected hidden spikes are simultaneous with the return and outside the
   fixed positive-lag window;
4. the ordinary external learner cannot directly update either side of the
   PORT/hidden boundary under the actual schedule;
5. one ON arm is additionally unstable under the fixed event ceiling.

These are preserved-result development diagnostics, not a capability result or a
scientific confirmation. A future versioned revision could be informative, but any
change to timing, schedule, topology, learner boundary, stability parameters, or the
event ceiling requires fresh Evidence Analyst authority. E0/E1/ES, scale expansion,
reservoir comparison, and v1 rerun/retune remain unauthorized.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_rv02_rd006_d0_causal_opportunity.py \
  --artifact artifacts/rv02_rd006/external_learning_reachability_a_v1/attempt-002/artifact.json.gz \
  --output /tmp/preserved_causal_opportunity_audit_v1.json

gzip -n -9 -c /tmp/preserved_causal_opportunity_audit_v1.json > \
  artifacts/rv02_rd006/external_learning_reachability_a_v1/audits/preserved_causal_opportunity_audit_v1.json.gz

python -m pytest -q \
  tests/test_rv02_rd006_d0_causal_opportunity_audit.py
```
