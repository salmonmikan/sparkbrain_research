# RV02-RD001 — hidden recruitment diagnosis

## Outcome

**All 18 development cells and 252 probes completed. Hidden units receive real
subthreshold current, but do not fire; the tested 40ms boundary ablations detect no
influence on visible continuation or final visible state.** No formal held-out or
comparative superiority claim is made.

This corrects a possible overinterpretation of the earlier feasibility result:
zero hidden spikes does NOT mean zero hidden state activity or zero synaptic input.

## Exact execution and evidence

- Executed source: `d5e21cd2edec2b74238ac9c4603ae0014eea5708`.
- Protocol: `RV02_RD001_RECRUITMENT_CONTRACT.md`; source frozen before execution.
- Raw uncompressed SHA-256: `d786fd242c1c6621b39a6700096536a96109a67333222304412be90e5e510d9d`.
- Raw gzip SHA-256: `d6507a988a3a2763742714993d2b420f735bf9fc76b45c308ce26b397d96e07e`.
- Evidence: `artifacts/research/rv02/rd001/` (manifest, summary, lossless gzip).
- Exact local executed history: `executed_source.bundle`, requiring original plan
  commit `2f2aae612ee6e0f08453c855a9910d965fa89bec` already present in the repository.

GitHub API publication may have a different commit SHA from the local execution.
The source file manifest and preserved Git bundle bind the actual executed source;
the publication commit must never be substituted for that execution identity.

## Observations

| Diagnostic | Result |
|---|---:|
| Natural 40ms route probes | 78 |
| Natural probes with positive current arriving at hidden units | 78 / 78 |
| Positive-current hidden arrivals in natural probes | 3,378 |
| Hidden spikes, natural 40ms | 0 |
| Hidden spikes, extended 160ms | 0 |
| Isolated direct-hidden positive controls | 18 / 18 fire at injection |
| Passive observer state/spike equivalence | 252 / 252 |
| Probe connection state unchanged | 252 / 252 |
| 160ms run agrees with 40ms spike prefix | 78 / 78 |
| Visible spike trace unchanged by boundary-zero ablation | 78 / 78 |
| Full visible final UnitState unchanged by boundary-zero ablation | 78 / 78 |
| Hidden external training traces / changed hidden edges | 0 / 0 |

Both horizons drained their queues in 72 / 78 natural route probes. Six reversal-family
probes retained live queues and generated additional spikes after 40ms; extending the
horizon did not recruit hidden spikes. Extended horizon is therefore not claimed to
leave every complete trace unchanged: only the 40ms prefix is required to be identical.

The maximum observed hidden pre-reset potential/threshold ratio remains below one;
the independent audit reports its scale-specific values and recomputes raw denominators.
Zero-weight boundary edges still schedule arrivals, so zero positive current must not
be confused with absence of scheduled events.

## What is and is not established

1. The positive control rules out a simple inability of the hidden units to execute a spike.
2. Natural route propagation reaches hidden units with subthreshold current. The mechanism
   does not recruit hidden spiking under these fixed inputs, weights, horizons and seeds.
3. Cutting visible↔hidden weights leaves both visible spikes and complete visible final
   state unchanged here; hidden state has no observed causal contribution to those outputs.
4. The existing external-only learner has no external trace at a hidden endpoint, and no
   hidden edge changes. This identifies a learning-eligibility limitation; it is not a
   justification to silently add endogenous credit or increase background gain.

These are diagnoses of already exposed development fixtures. They do not reject generic
capacity effects, all Field mechanisms, or distributed computation in other regimes.
No baseline parameters, old result bytes, reservoir rules, A01 mechanism, thresholds or
formal candidates were changed to produce this outcome.

## Engineering acceptance

The execution took about 23.45 seconds of summed worker wall time; peak reported RSS was
55,212 KiB. Every worker remained below the 60s / 1GiB limit and the overall 600s ceiling.
Native event/spike budgets and timeout failure semantics remained active.

Reserved observer/control tests and synthetic bundle-verifier tests passed before execution.
The 24 earlier RV02 tests also passed, for 43 focused tests at execution time. Local readiness
passed on Python 3.12.14. Full pytest, ruff, and the repository-wide validation sequence were
not available in this environment; this limitation remains open, not waived as a full-suite pass.

A separate post-execution observer-only audit reconstructs derived counts, currents, ratios,
projections and bounds from raw rows without re-executing the model. See
`RV02_RD001_INDEPENDENT_ACCEPTANCE.md` for final acceptance and exact audit commands.

```bash
python scripts/run_rv02_recruitment.py --verify artifacts/research/rv02/rd001
PYTHONPATH=src python -m unittest discover -s tests -p 'test_rv02*.py' -q
python scripts/local_readiness_check.py
```

Further mechanism changes require a separately declared development protocol. RV02 formal
evaluation remains blocked by the earlier resource-matching, common-geometry and statistical
design gates. No new formal candidate is generated or authorized by this report.
