# RV02-RD001 independent engineering acceptance

Date: 2026-09-09. Disposition: **ACCEPTED at the development-diagnosis engineering boundary**.
This report grants no formal seal, held-out authorization, superiority, or claim-grade upgrade.

## Evidence identity

- Execution source: `d5e21cd2edec2b74238ac9c4603ae0014eea5708`.
- Retained bundle: `artifacts/research/rv02/rd001/`.
- Raw SHA-256: `d786fd242c1c6621b39a6700096536a96109a67333222304412be90e5e510d9d`.
- Gzip SHA-256: `d6507a988a3a2763742714993d2b420f735bf9fc76b45c308ce26b397d96e07e`.
- Exact completion: 18 family-by-scale cells; 252 probes. No missing, duplicate, or failed cell.
- Runtime, runner, and preregistered contract were not changed after execution started.
  The raw-reconstruction auditor and its six mutation tests were added afterward as independent
  acceptance checks, not as a repair or rerun of the experiment.

The frozen runner verifier checked compressed and uncompressed hashes, the exact source inventory,
configuration, 18 ordered identities, summary reconstruction, training cardinalities and learning
boundaries, fixed probe roles/horizons, actual positive-control spikes, exact extended prefixes,
observer/nonlearning hashes, and visible-state comparisons.

## Independent reconstruction

`scripts/audit_rv02_recruitment.py` reads the retained evidence without model execution. It requires
18 complete cells and 252 probes independently of the runner's weaker `integrity_verified` state,
which intentionally also permits structurally valid incomplete bundles.

For all 252 probes it reconstructs event-group counts, excitation/inhibition, membrane decay with
tau 18 ms, refractory integration, threshold 0.5, reset and spike correspondence, and per-hidden-unit
counts/currents/peak ratios/stored and projected potentials. Refractoriness uses the retained
1.25 ms physical-bridge setting. Float reconstruction tolerance is `1e-12`; discrete identities,
counts, condition membership, and spike correspondence are exact. Silent peak ratios remain null.
Zero-weight scheduled arrivals are distinguished from positive-current arrivals.

Measured maxima are 497 arrivals and 64 spikes per probe, below the frozen 4,096/512 limits.
All cell wall times and RSS records satisfy the 60-second and 1-GiB ceilings; the sum of recorded
cell wall times is 23.445713584 seconds, below the 600-second total budget. These are engineering
measurements, not resource-matched comparative or energy evidence.

## Reconstructed observations

| Condition | Probes | Probes with positive hidden current | Hidden spikes | Drained queues |
|---|---:|---:|---:|---:|
| Natural 40 ms | 78 | 78 | 0 | 72 |
| Natural 160 ms | 78 | 78 | 0 | 72 |
| Visible-hidden boundary zero, 40 ms | 78 | 0 | 0 | 72 |
| Direct hidden positive control | 18 | 18 | 18 | 18 |

All 78 natural/extended 40-ms prefixes agree. All 78 boundary ablations preserve the measured
visible final state; the source also records visible-spike equality. Boundary ablation changes
only visible-to-hidden and hidden-to-visible weights after training, retaining hidden-to-hidden
connections and the original trained snapshot. Hidden learning updates and hidden external traces
remain absent. Direct positive-control stimulation is neither a training observation nor evidence
of natural recruitment.

## Tests and commands

Pre-execution focused tests: 43 passed (24 preceding RV02 tests plus 19 RD001 observer/verifier
tests). Post-execution acceptance: **49 passed**, including six new raw-auditor mutation tests.
The pre- and post-execution test counts are deliberately not conflated.

```bash
PYTHONPATH=src python tests/test_rv02_scale_contract.py -q
PYTHONPATH=src python tests/test_rv02_bundle_verifier.py -q
PYTHONPATH=src python tests/test_rv02_recruitment.py -q
PYTHONPATH=src python tests/test_rv02_recruitment_verifier.py -q
PYTHONPATH=src python tests/test_rv02_recruitment_raw_audit.py -q
PYTHONPATH=src python scripts/run_rv02_recruitment.py --verify artifacts/research/rv02/rd001
PYTHONPATH=src python scripts/audit_rv02_recruitment.py artifacts/research/rv02/rd001
```

Tests use standard-library unittest, reserved synthetic states, and isolated temporary fixtures.
No test tampers with retained evidence. The full historical repository test suite is not claimed
as part of this focused acceptance. Existing RV01/v04 dynamics and RV02 scale implementation remain
unchanged from the preceding accepted development source.

## Interpretation boundary

The added hidden units **do receive subthreshold current and membrane-state changes**. Therefore
“zero hidden spikes” must not be paraphrased as “no hidden recruitment of any kind” or “inert units.”
Under the fixed natural probes, neither horizon produces hidden spikes or hidden external-learning
eligibility. Direct stimulation establishes excitability only. Six extended probes still have live
queues at 160 ms, so this experiment does not establish absence of all later activity.

Boundary ablation's unchanged visible state is bounded evidence of no detected visible contribution
in this diagnostic, not proof against other dynamics. The worlds were already exposed development
fixtures; no fresh generalization, Field/reservoir superiority, resource matching, or formal RV02
result has been established. Previous results and invalidated output records remain unchanged.
