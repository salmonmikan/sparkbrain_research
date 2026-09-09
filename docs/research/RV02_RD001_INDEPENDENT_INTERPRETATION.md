# RV02-RD001 independent interpretation and acceptance

Date: 2026-09-09. Scope: development mechanism diagnosis only.

## Evidence identity

- Execution source: `d5e21cd2edec2b74238ac9c4603ae0014eea5708`.
- Uncompressed raw SHA-256: `d786fd242c1c6621b39a6700096536a96109a67333222304412be90e5e510d9d`.
- Compressed raw SHA-256: `d6507a988a3a2763742714993d2b420f735bf9fc76b45c308ce26b397d96e07e`.
- Independent audit read the retained compressed raw data, recomputed both digests,
  and reconstructed the observations below without executing another experiment.

## Engineering acceptance

PASS within the registered development scope: 18 complete family-by-scale cells,
252 probes (78 natural, 78 extended, 78 boundary-zero, 18 direct positive controls).
All observed probes match their unobserved reference clone's complete state hash;
all before/after probe connection hashes agree. Every family retains one evidence
hash across its scales. No hidden external learning traces or changed hidden
connections were recorded. All 18 direct hidden-unit positive controls passed.

The independent pre-execution source review confirmed that the observer calls the
native delivery method exactly once, reproduces its decay and refractory arithmetic
without mutating state, and separately records stored and projected potential.
The boundary intervention cuts only visible-to-hidden and hidden-to-visible weights,
preserving hidden-to-hidden edges and all connection slots. Zero-weight connections
still schedule arrivals, so positive-current arrivals are the relevant current-access
measurement, distinct from scheduled arrival counts.

## Reconstructed scale response

Each scale has 26 natural route probes. Counts below are **unit-probe pairs**, not
distinct units across the experiment or independent statistical replicates.

| Measurement | 1x: 48 units | 3x: 144 units | 10x: 480 units |
|---|---:|---:|---:|
| Hidden unit-probe pairs receiving positive current, 40 ms | 242 | 899 | 1,379 |
| Hidden unit-probe slots available | 312 | 2,808 | 11,544 |
| Positive-current hidden arrivals, 40 ms | 494 | 1,272 | 1,612 |
| Hidden spikes, 40 ms | 0 | 0 | 0 |
| Largest hidden pre-reset potential / threshold, 40 ms | 0.399477 | 0.399477 | 0.334436 |
| Hidden spikes, 160 ms | 0 | 0 | 0 |
| Largest hidden pre-reset potential / threshold, 160 ms | 0.469123 | 0.469123 | 0.412213 |
| Natural probes with drained queues at 40 ms | 24 / 26 | 24 / 26 | 24 / 26 |

The extended probes preserve the exact 40 ms spike prefix in all 78 comparisons.
Two opposing-reversal probes per scale retain live queues: their visible spike
counts rise from 16 to 64 when the horizon increases from 40 to 160 ms, with 16
queued arrivals remaining at both endpoints. Therefore the extended horizon does
change ongoing visible recurrence; it does not produce hidden spikes. It would be
incorrect to explain every extended result by an already drained queue.

For all 78 boundary-zero comparisons at 40 ms, both the visible spike trace and
the complete visible final UnitState hash remain equal to the natural condition.
Positive-current arrivals into hidden units become zero. Direct injection is an
artificial engineering control, not natural recruitment, training evidence, or a
capacity advantage.

## Interpretation and limits

Larger substrates receive more hidden subthreshold current. Thus the previous
spike-only observation must not be paraphrased as an absence of hidden state use:
hidden membrane state is recruited even though it does not generate spikes.

Under the fixed existing configuration, this recruitment does not become regenerative
hidden propagation. The external-only learner also leaves hidden connections
unmodified. Cutting access across the hidden boundary produces no observed visible
trace or final-state contribution in these 40 ms diagnostics. This is a measured
null effect, not proof that hidden state is irrelevant at every future horizon,
under other inputs, or in another learning mechanism.

The worlds are deliberately reused development fixtures, with one fixed seed and
truth-informed route edges inherited by the study. No reservoir comparison,
formal candidate, held-out generalization, general Field superiority, or scientific
claim-grade upgrade is accepted. Existing RV02 feasibility artifacts and earlier
formal experiments remain unchanged. No threshold, initial-weight, or learning-rule
repair was used to obtain this result.
