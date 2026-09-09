# RV02-RD002 independent engineering acceptance

Date: 2026-09-09. Disposition: **ACCEPTED at the development-diagnosis engineering boundary**.
This acceptance grants no formal seal, held-out authorization, superiority or claim-grade upgrade.

## Evidence identity and pre-execution gate

- Execution source: `58f196b006020b144cf62c695ca1c1fff8e7087e`.
- Retained bundle: `artifacts/research/rv02/rd002/`.
- Raw SHA-256: `3548b20d3e8e0003ffd6f5964888b948a9d3cf39c28b2167385ea9ff5a433ee4`.
- Gzip SHA-256: `8f5e2929d8f4ed9b4a91ecf9eef6434ef8812240220379c16db190fddb106257`.
- Exact completion: 18 family-by-scale cells; 468 probes; no missing or failed condition.

Independent review and 14 new reserved-synthetic tests passed before the source commit and
single grid execution. These test inbound-only gain isolation, original-state preservation,
exact gain-1 equivalence to RD001 execution, synthetic threshold crossing, boundary-cut isolation,
frozen gain/horizon rejection, observer noninterference, no-learning hashes, native-guard partial
retention and fail-closed observer divergence, task ordering/no-ignition/error scoring, and raw
score/observer/count mutation rejection. No RD002 development outcome was used to select gains.

Runtime, runner, preregistration, tests and independent auditor were committed before execution
and remain unchanged. The frozen source manifest includes the auditor and relevant tests.
No post-outcome runtime repair, replacement execution, changed gain or relaxed bound occurred.

## Independent retained-evidence reconstruction

The frozen `scripts/audit_rv02_boundary_recruitment.py` passed on the first closed bundle without
model execution. It checks the runner's manifest/raw/summary integrity, fixed ordered matrix,
all completed probes, resource fields, and the following independent reconstructions:

- RD001 baseline input identity is pinned by both its compressed and uncompressed hashes.
  All 78 gain-1 natural probes match every retained RD001 natural-probe field, including raw
  events, spikes, complete state hashes, visible final states and provenance-bearing spike rows.
- Training rows and world/topology audit records match RD001 exactly; hidden learning changes
  and hidden external traces remain absent. Trained-unit inventories, unchanged threshold 0.5,
  zero initial dynamic activity, and degree-eight edge counts are checked.
- Ordered gain intervention records and gained connection hashes are rebuilt from the complete
  trained connection records. Only visible-to-hidden weights are multiplied. Both directions
  of the cut boundary are rebuilt independently, retaining all other weights and edge slots.
- All three cut conditions per route have equal spikes, event observations, hidden statistics,
  visible final states, complete state hashes and resulting connection hashes. Stored pair
  comparison flags agree with their raw visible traces and states.
- The established RD001 arithmetic auditor reconstructs every event group's membrane decay,
  refractory integration, unchanged threshold, resets and spikes, plus hidden-unit current,
  arrival, ratio and final-potential aggregates. Float tolerance is `1e-12`; event identities
  and counts are exact. Silent peak ratios remain null and zero-current arrivals remain distinct.
- All task fields are independently reconstructed from time-ordered spikes strictly after
  100 ms, preserving later cue recurrence, duplicates and native same-time order. Hidden spikes
  are excluded from external contamination. Missing expected units and excess route events
  follow the preregistered definitions; they are not presented as edit distance.
- Observer state/spike equivalence and probe connection nonlearning hold for every probe.

Maximum probe counts are **185 arrivals and 23 spikes**, strictly below the 4,096/512 limits.
No native-guard failure occurred. Summed recorded cell wall time is **48.449659308 seconds**;
maximum cell time is **10.237765618 seconds**, and maximum recorded RSS is **92,272 KiB**.
All satisfy the 600-second total, 60-second cell and 1-GiB bounds. These are local engineering
measurements, not energy evidence or a resource-matched architecture comparison.

## Bounded observations

| Natural gain | Probes with hidden spikes | Hidden spikes | Visible trace differences versus cut | Visible final-state differences versus cut |
|---|---:|---:|---:|---:|
| 1 | 0/78 | 0 | 0/78 | 0/78 |
| 2 | 0/78 | 0 | 0/78 | 0/78 |
| 4 | 35/78 | 83 | 0/78 | 33/78 |

Every natural gain and every cut condition has 24/78 strict-exact routes, 492 raw off-route
events and 48 excess route events. Each condition has 72/78 drained queues; six nonempty
queues at 140 ms indicate horizon truncation, not automatically runaway. A bounded run does
not establish long-term stability. Gain 4 recruits hidden spikes and changes some visible
subthreshold/provenance state, without a detected visible spike-trace improvement. Scientific
usefulness is evaluated separately in the independent interpretation against the frozen rule.

## Reproduction and limits

```bash
PYTHONPATH=src python tests/test_rv02_boundary_recruitment.py -q
PYTHONPATH=src python tests/test_rv02_boundary_raw_audit.py -q
PYTHONPATH=src python scripts/run_rv02_boundary_recruitment.py --verify artifacts/research/rv02/rd002
PYTHONPATH=src python scripts/audit_rv02_boundary_recruitment.py artifacts/research/rv02/rd002
```

The two new test files contain 11 and 3 tests respectively. This report does not claim the
full historical repository suite. Raw reconstruction verifies internal numerical consistency
and frozen implementation contracts; retained hashes alone cannot prove execution honesty
independently of the reviewed local source. Already-exposed development worlds and dependent
route probes do not establish fresh generalization or statistical replication. Previous
RV02/RD001 evidence, formal boundaries and unsupported claims remain unchanged.
