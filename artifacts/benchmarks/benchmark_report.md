# SwitchWorld Phase-0 Benchmark

> This is a deterministic hand-authored evidence-routing experiment. It is a software validation result, not evidence of general intelligence or biological equivalence.

Episodes: 40; steps per episode: 30

| model | accuracy_all_steps | coverage | revision_recall | revision_precision | mean_switch_latency | unnecessary_revisions | recovery_rate | active_spark_fraction | spark_update_equivalent_ratio |
|---|---|---|---|---|---|---|---|---|---|
| sparkbrain | 0.6400 | 0.9367 | 0.6659 | 0.6142 | 1.3517 | 2.8000 | 0.6442 | 0.3628 | 1.8371 |
| sparkbrain_no_residual | 0.4567 | 0.8183 | 0.5726 | 0.4976 | 1.9367 | 2.4750 | 0.6169 | 0.3191 | 1.4684 |
| sparkbrain_single_spark_ignition | 0.5925 | 0.8900 | 0.6285 | 0.7396 | 2.0493 | 1.7750 | 0.6094 | 0.3287 | 1.6923 |
| accumulator | 0.6283 | 0.9042 | 0.6499 | 0.6482 | 1.4226 | 2.5500 | 0.6475 | 1.0000 | 1.0000 |
| hard_wta | 0.3375 | 0.9042 | 0.3776 | 0.0000 | 0.4730 | 0.0000 | 0.5077 | 1.0000 | 1.0000 |
| instant | 0.6025 | 1.0000 | 0.8399 | 0.4068 | 0.4817 | 12.8000 | 0.8367 | 1.0000 | 1.0000 |

## Interpretation limits

- All models receive the same hand-authored evidence weights.
- No representation learning or end-to-end learning is evaluated.
- `active_spark_fraction` is an algorithmic activity metric, not a hardware energy measurement.
- `spark_update_equivalent_ratio` may exceed 1 because one external event can trigger several recurrent/event-driven updates.
- The decisive research comparison requires learned routing and matched-parameter GRU/Transformer/RIM baselines.
