# Retention v5: valid completion, predefined support gate failed

Status: `EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY`; scientific credit 0.
The single approved v5 execution completed all 26 branches and 768 pairs. The
independent retained-data audit is valid, but **both fixtures fail the predefined
support gate**. This is a negative bounded result, not an execution failure and
not evidence of general retention or learning superiority.

## Fixed question and comparisons

The unchanged [protocol](plasticity_retention_protocol_20261001.md) compares
C (eligibility rho=0.9, eta=0.001), L (apply-local rho=0, eta=0.001), G (rho=0.9,
eta=0.0001) and Fw (weight writes disabled). Delays remain fixed; homeostasis,
assembly formation and count readout remain live. H/R are the registered ordinary
memory baselines. The two prefixes are exposed development fixtures, not fresh
training replicates or held-out confirmation. G is a single analytic steady-state
attenuation reference, not a fully dose-matched finite-history control.

## Exact predefined failures

1. In both fixtures, return Brier(G) equals Brier(L) exactly:
   `0.0004998643892488487`. Their difference is `0`, below the required `0.02`.
   L therefore fails the required secondary comparison despite improving over C.
2. In fixture 910076, stationary Brier(L) is `0.12426372409809272` versus
   C `0.026253258300119514`. L minus C is `0.0980104657979732`, exceeding
   the allowed `0.02`. Its other stationary requirements still pass: L has
   14 correct versus C 15 (one fewer allowed) and greater coverage.

The primary C/L return, informative novel acquisition, novel preservation,
non-ceiling and native-transition requirements pass in both fixtures. Stationary
preservation passes in fixture 910075. The complete conjunction still fails in
both; no threshold, row, input, arm or criterion was changed after observing data.
All nine paired native-transition counts, early/late novel metrics and calibration
bins remain in the complete retained scores and [independent summary](../../artifacts/research/plasticity_retention_results_20261002/independent_summary.json).

## All registered branch comparisons

Brier below is rounded only for display. Decisions use the original unrounded
values; the [26-row TSV](../../artifacts/research/plasticity_retention_results_20261002/registered_arm_comparison.tsv)
retains them. All allocated branches are shown. H/R and Fw were not assigned to
stationary, and G was not assigned to novel; missing combinations are not claims.

| Fixture | Condition | Arm | Correct/total | Wrong | Abstain | Coverage | Brier |
|---|---|---|---:|---:|---:|---:|---:|
| 910075 | novel | C | 14/32 | 13 | 5 | 0.84375 | 0.324337101 |
| 910075 | novel | Fw | 27/32 | 0 | 5 | 0.84375 | 0.049191565 |
| 910075 | novel | H | 30/32 | 2 | 0 | 1.00000 | 0.076250000 |
| 910075 | novel | L | 27/32 | 0 | 5 | 0.84375 | 0.049191565 |
| 910075 | novel | R | 22/32 | 0 | 10 | 0.68750 | 0.127705897 |
| 910075 | return | C | 14/32 | 18 | 0 | 1.00000 | 0.322681329 |
| 910075 | return | Fw | 32/32 | 0 | 0 | 1.00000 | 0.000499864 |
| 910075 | return | G | 32/32 | 0 | 0 | 1.00000 | 0.000499864 |
| 910075 | return | H | 30/32 | 2 | 0 | 1.00000 | 0.072500000 |
| 910075 | return | L | 32/32 | 0 | 0 | 1.00000 | 0.000499864 |
| 910075 | return | R | 27/32 | 0 | 5 | 0.84375 | 0.078219908 |
| 910075 | stationary | C | 12/16 | 2 | 2 | 0.87500 | 0.155104560 |
| 910075 | stationary | L | 14/16 | 2 | 0 | 1.00000 | 0.124263724 |
| 910076 | novel | C | 14/32 | 12 | 6 | 0.81250 | 0.303356818 |
| 910076 | novel | Fw | 29/32 | 0 | 3 | 0.90625 | 0.032263386 |
| 910076 | novel | H | 30/32 | 2 | 0 | 1.00000 | 0.076250000 |
| 910076 | novel | L | 29/32 | 0 | 3 | 0.90625 | 0.032263386 |
| 910076 | novel | R | 24/32 | 0 | 8 | 0.75000 | 0.104633655 |
| 910076 | return | C | 14/32 | 18 | 0 | 1.00000 | 0.322681329 |
| 910076 | return | Fw | 32/32 | 0 | 0 | 1.00000 | 0.000499864 |
| 910076 | return | G | 32/32 | 0 | 0 | 1.00000 | 0.000499864 |
| 910076 | return | H | 30/32 | 2 | 0 | 1.00000 | 0.072500000 |
| 910076 | return | L | 32/32 | 0 | 0 | 1.00000 | 0.000499864 |
| 910076 | return | R | 26/32 | 0 | 6 | 0.81250 | 0.072882233 |
| 910076 | stationary | C | 15/16 | 0 | 1 | 0.93750 | 0.026253258 |
| 910076 | stationary | L | 14/16 | 2 | 0 | 1.00000 | 0.124263724 |

## Interpretation within the registered boundary

- L improves return versus C in both fixtures, with 32/32 correct versus 14/32.
  But L, G and Fw have identical probability/native prediction vectors across all
  allocated return rows. This does not establish locality-specific benefit.
- L and Fw also match across every allocated novel prediction row, although L
  makes positive actual weight writes. Novel success therefore does not establish
  a benefit caused by weight learning; live assembly/readout mechanisms remain.
- H makes more correct novel predictions with full coverage (30/32 in both)
  than L/Fw (27/32 and 29/32), while L/Fw have lower Brier. R has more abstentions
  and worse Brier. No general superiority or unassigned stationary comparison follows.
- The stationary tradeoff differs between fixtures. Neither averaging it away nor
  replacing the predefined conjunction with the favorable return result is valid.

Any follow-on attribution study needs a fresh prospective identity, fixed controls
and separate approval. This consumed execution is not rerun, retuned or promoted.

## Provenance, preservation and resource accounting

Reviewed execution source: `81088ae386cbc611fb9e6366d8ade1c2ea74b6b7`, published
by [PR183](https://github.com/salmonmikan/sparkbrain_research/pull/183) and merged
as `7e8d779a06d6cae6a2eda399de241d9b390efcde`. Execution used the reviewed PR
commit. Freeze SHA-256:
`272ed83bd0a520d8fc80a6e54b6145eaae76333f8866cba0d780bae76746a0b9`.
The [exact coordinator clearance](https://github.com/salmonmikan/sparkbrain_research/pull/183#issuecomment-5945374336)
is distinct from the original consumed v3 attempt's authority.

All 315 run files were copied and byte-verified before independent audit. The
canonical preservation archive includes those files, all 198 frozen sources,
freeze/dependency bytes, original authority records and invocation: 521 members,
1,150,200 compressed bytes, SHA-256
`75bee0d8ce010af13049f684651623a3257a00359966852ea6f0517516bce55d`.
The [transport manifest](../../artifacts/research/plasticity_retention_results_20261002/transport_manifest.json)
binds all 24 base64 parts. Terminal SHA-256:
`5b62860e7c17241c2136817c8f8915cf7099b2422507589277c2e1218d7c7a67`.
Before/after hashes verify that audit did not change any original raw file.

The original v3 failure remains consumed and preserved with terminal
`70a54d6f1c6b23809853e14901561bbda4aede73a885422e55a7ab6964caf223` and
0 admitted model pairs. Unexecuted v4 freezes remain history. Combined model
allocation is still 0 + 768 = 768; there was no retry or extra experiment.
Actual retained calls match the fixed allocation: 26 wrapper constructions,
18 native loads, 36 nested v05 constructions, 768 predictions/outcomes and
512 v05 episode/apply/outcome calls.

Terminal pre-closure samples report 162.08520759099997 aggregate CPU seconds,
161.2533364950068 wall seconds and 41,440 KiB driver peak RSS. They are not
complete process-lifetime cost or energy measurements. Per-worker costs/RSS,
output accounting and terminal reserves remain in the original terminal. Resource
ceilings remained 360 CPU/480 wall seconds, 512 MiB address space per process and
256 MiB output inclusive of the 4 MiB terminal reserve. Post-run preservation,
compression and audit are separate verification work, not added model evidence.
Offline enforcement was a Python socket audit hook, not OS network isolation.

## Independent audit and reproduction, without model rerun

The [data-only audit](../../artifacts/research/plasticity_retention_results_20261002/independent_audit.json)
reports valid completion, 0 runtime model calls, 256 reconstructed H/R rows and
512 recomputed apply-observation rows. Its source/freeze pins and all three
original-authority hashes were supplied independently before execution and
recaptured by the parent before the run. This validates retained-data consistency;
it does not cryptographically attest the historical process or confer scientific credit.

The portable byte-preservation verifier below imports no runtime and checks all
archive members, embedded frozen-source bytes and independently pinned authorities.
An explicit `--check-current-sources` additionally checks all current checkout bytes;
default preservation remains valid after unrelated future source development.
Extraction requires a fresh absent directory:

```sh
python -S -P -B scripts/verify_retention_v5_evidence.py
python -S -P -B scripts/verify_retention_v5_evidence.py --extract /tmp/retention-v5-evidence
```

The full existing data-only audit additionally requires the exact frozen Python
3.12.14 interpreter/executable, not an arbitrary platform interpreter. Run from a
fresh extracted source snapshot whose 198 hashes match the published freeze:

```sh
python -S -P -B /tmp/retention-v5-evidence/frozen-sources/scripts/verify_plasticity_retention_run.py --output /tmp/retention-v5-evidence/run --freeze /tmp/retention-v5-evidence/freeze --expected-source-commit 81088ae386cbc611fb9e6366d8ade1c2ea74b6b7 --expected-manifest-sha256 272ed83bd0a520d8fc80a6e54b6145eaae76333f8866cba0d780bae76746a0b9 --expected-review-sha256 3a6c848a0d91bbccd9af96453a1b440ae1e463b247e8d387eb218c09d3899789 --expected-publication-sha256 49b7b54c1151366dbf992bd4b52f4357d731ac1227540a15e251a8b8845d8a6c --expected-approval-sha256 7af778f61a311ad3ef405c64e267d2d4a99c997edf8524218276b5bc29347b3b
```

No execution-runner command is part of reproduction of this retained result.
Both valid completion and the failed support gate must remain visible.

## Publication validation

All 428 scoped model-free checks passed: the 414 previously passing retention
and native-history checks plus 14 new preservation/extraction tests. Full
repository Ruff passes. A separate explicit current-source preflight verifies all
198 source pins; ordinary archival tests deliberately do not require future
mutable checkout files to keep matching a historical freeze. Independent source
and report review checked all 26 report/TSV rows against retained scores and all
raw equality/attribution statements. Current-head remote CI and Codex review are
tracked on the publication PR, separately from these local source checks.
