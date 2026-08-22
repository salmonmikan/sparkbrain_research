# C10 — Reproducibility, Technical Report, and Release Package

## Goal

Produce a clean, independently runnable research release whose written claims exactly match its code, raw data, statistical evidence, and limitations.

## Prerequisites

Primary results selected from C02–C07; C09 novelty audit current. C08 may be included as positive or negative exploratory work but must not block release.

## Required release artifacts

- pinned environment lock(s) and platform matrix;
- clean-install reproduction command;
- container image definition;
- dataset acquisition/checksum scripts;
- immutable experiment manifests;
- raw per-seed outputs;
- generated tables/figures from scripts only;
- technical report source and rendered output;
- model/system cards;
- license and third-party notices;
- security/privacy review for external data;
- software bill of materials where practical;
- archive checksum and release manifest;
- negative-result appendix;
- artifact evaluation guide.

## Technical report structure

1. problem and falsifiable hypotheses;
2. prior art and exact contribution boundary;
3. formal model;
4. implementation and trace semantics;
5. controlled worlds;
6. learned architecture;
7. matched baselines;
8. external validation;
9. spiking equivalence if complete;
10. ablations and causal interventions;
11. compute/resource accounting;
12. failures, threats to validity, and prohibited conclusions;
13. reproducibility instructions.

## Reproduction requirements

From a clean environment, one documented command must:

- validate versions and data checksums;
- run a smoke test;
- reproduce the primary table/figure subset;
- verify output hashes or tolerance-based numerical invariants;
- emit a machine-readable run manifest.

Full expensive runs may be separate, but sample artifacts cannot be mistaken for full results.

## Claim audit

Before release, inspect every abstract, README, figure caption, table takeaway, and conclusion against `CLAIMS_REGISTER.md`. Downgrade or remove unsupported wording. Report negative and null results.

## Acceptance criteria

- an independent clean-room run reproduces the primary result within documented tolerance;
- all figures/tables have scripts and raw inputs;
- code/data/model licenses permit the chosen release;
- report source, generated report, code tag, and artifact manifest agree;
- all primary claims cite the exact experiment/run IDs supporting them;
- release does not imply biological fidelity, consciousness, AGI, novelty proof, or energy gains without corresponding evidence grades.

## Non-goals

- polishing away scientific uncertainty;
- releasing restricted datasets;
- calling exploratory C08 results established organs;
- selecting only favorable seeds or runs.
