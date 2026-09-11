# RV01 R01-15 exposed-development result

Date: 2026-09-11  
Status: **FIXED DEVELOPMENT RESULT / NEGATIVE MECHANISTIC DISCRIMINATION / NO HELD-OUT EXECUTION**

## Execution identity

```text
protocol: rv01-r01-15-post-spike-suppression-v1
phase: development
frozen source: freeze/rv01-r01-15-development-source
source SHA: a46096458446e3d101c5a951dba4efd7db1ee0ae
workflow run: 34612398956
artifact id: 10268643645
artifact digest: sha256:e349381d95fd47e09830e45723fa306419698fd226c8d87a1a7f3d7f77b9fe13
raw development_result.json SHA-256: e849acbd2a9acc14d87fdec58be398b6c4b1e53ec6b33aa5a77ace43d56d1dac
suite hash: a08bb873482e001a786ef4ec3a49be8afe8fc765df432ff37a3502178f5e28b3
world grid hash: 0a61fd90b2b2dfc3816029416183894d279ee5514dc271dc49ce3da4d66f2619
Python: 3.11.16
same-source rerun allowed: false
held-out capability executed: false
```

The one-shot workflow completed successfully and retained the raw development artifact. This report does not rerun the suite and does not open the reserved held-out phase.

## Fixed matrix

The development suite contains:

```text
25 worlds
100 probes
4 Field arms per probe:
  intact
  adaptation_zero
  refractory_zero
  both_zero
```

All 100 probes reached the registered common-breadth budget in all four Field arms.

## Main result

The four Field arms were behaviorally identical on **every one of the 100 development probes** under the retained registered outputs.

For all 100/100 probes, the following were identical across `intact`, `adaptation_zero`, `refractory_zero`, and `both_zero`:

- emitted/generated unit sequence;
- common-breadth unit sequence;
- common-breadth event count;
- common-breadth revisit count;
- ordered-retention fraction;
- exact-route recovery;
- contamination count;
- common-breadth reachability.

Overall retained summary:

| metric | intact | adaptation_zero | refractory_zero | both_zero |
|---|---:|---:|---:|---:|
| mean common-breadth events | 5.48 | 5.48 | 5.48 | 5.48 |
| mean common-breadth revisits | 0.03 | 0.03 | 0.03 | 0.03 |
| exact routes recovered | 40 | 40 | 40 | 40 |
| common-breadth unreached | 0 | 0 | 0 | 0 |

The intact Field produced `0.91` fewer mean common-breadth events than the fixed resource-matched reservoir reference across the suite, but that descriptive Field/reservoir difference is unchanged by every registered post-spike suppression arm.

## Intervention effectiveness audit

The retained intervention ledger contains 818 targeted post-spike records per single-field arm.

### Adaptation suppression

```text
adaptation_zero records: 818
records with nonzero pre-intervention adaptation: 0
records where adaptation value actually changed: 0
```

The targeted `adaptation` field was already `0.0` at every registered intervention point. Therefore the adaptation arm is a genuine registered negative/no-op observation, but it is **not evidence that an active nonzero adaptation state is causally irrelevant**; the development suite never encountered a nonzero value for this targeted field at the intervention boundary.

### Refractory suppression

```text
refractory_zero records: 818
records where refractory_until_ms actually changed: 818
```

The refractory intervention was a real state perturbation on every retained record. Nevertheless it changed none of the registered emitted/common-breadth/route/contamination outputs in any of the 100 probes.

`both_zero` likewise changed refractory state while adaptation remained already zero, and remained output-identical to intact.

## Scientific interpretation

R01-15 does **not** support the preregistered explanation that the R01-14 lower-repetition / faster-first-visit signature is caused by the registered post-spike refractory state. Refractory suppression was physically effective but behaviorally silent across the fixed development matrix.

The adaptation part of the explanation is not established either, but for a different reason: the targeted adaptation state was already zero at every intervention point, so this suite did not create an effective adaptation-state contrast.

The strongest fixed interpretation is therefore:

```text
registered refractory suppressor -> physical state change, no registered behavioral effect
registered adaptation suppressor -> no physical contrast available at intervention points
combined suppressor -> no behavioral effect
```

This is a negative mechanistic result. It must not be rescued by changing suppression timing, adapting the probe horizon, adding favorable seeds, or rerunning this same development identity.

## Relation to prior RV01 evidence

This result leaves the previously preserved R01-14 descriptive traversal difference intact as historical evidence, but it rejects the specific refractory-state explanation tested here. It does not improve exact-route recovery and does not alter the earlier conclusion that RV01 presently supports broad candidate retention / traversal differences more strongly than selective-memory superiority.

No inference from this development result is imported into A01 or CX01 formal evidence.

## Next safe question

Any continuation must use a fresh prospective identity. A useful source-only next-stage audit is to determine, without running new capability, whether the runtime has another actually nonzero post-spike state variable that could mechanistically account for the retained traversal timing/repetition signature, or whether the signature is instead determined earlier by propagation/topology and event scheduling.

If a new intervention is proposed, its target state must be shown prospectively to be nonzero/reachable on construction or development-only instrumentation before a suppression experiment is opened. Reserved R01-15 held-out worlds remain sealed.