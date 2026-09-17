# EXPLORATORY / NON_EVIDENTIARY — H3 correlation-aware reduction probe

This artifact is an idle-capacity SUB incubator result. It is **not scientific evidence**, does not open a formal identity, and cannot satisfy any H3 gate or programme claim.

## Why this is independent of MAIN

MAIN owns C19-R1 and every readiness/execution/scoring blocker on that line. This probe uses only a new synthetic world built from stable `main`; it does not read Belief-R, C19-v4 outcomes, R1 package material, frozen evidence, sealed inputs, or any consumed identity.

## Reduction question

Can robustness to duplicate and correlated evidence that might look Evidence-Coalition-specific be reproduced by a simpler ordinary scalar mechanism if the comparator receives the same provenance/correlation-group information?

The fixed synthetic probe compares four deterministic readers:

1. `naive`: every delivered message is independent mass;
2. `source_dedup`: exact duplicate deliveries from the same source are collapsed;
3. `group_normalized`: exact source duplicates are collapsed and every known correlation group contributes one unit of scalar mass;
4. `group_majority`: a simple coalition-style proxy with one majority vote per known correlation group.

The synthetic grid contains 4,096 examples from five latent correlation groups. Group latent signs agree with the truth with probability `0.70`; source members agree with their group latent sign with probability `0.90`; group sizes and exact duplicate counts vary by a fixed pattern. Seed is `1337`.

## Observation

Accuracy on the fixed synthetic grid:

- naive: `0.737548828125`
- exact-source dedup: `0.753662109375`
- group-normalized scalar: `0.801513671875`
- group-majority proxy: `0.801025390625`

The group-normalized scalar and group-majority proxy agree on `0.97900390625` of examples.

A separate deterministic stress case uses one wrong correlation group containing `1/2/4/8/16` distinct source IDs and two independent correct singleton groups. Once the wrong group contains at least four distinct source IDs, both the naive and exact-source-dedup readers flip to the wrong answer, while both group-aware readers remain correct. Exact-ID dedup therefore does not solve correlation overcounting when correlated evidence arrives under distinct source IDs.

## Interpretation boundary

This is a reduction/specification warning, not evidence for or against H3. The strongest comparator is deliberately given **known correlation-group IDs**. That can be a large information privilege. A future formal H3 object must prospectively decide how correlation structure is known, estimated, or learned and must match that information access across Coalition and simpler scalar/Bayesian baselines.

The observation suggests that a future H3 test should not claim a Coalition-specific robustness benefit merely by beating a naive accumulator or exact-ID dedup. It should first beat an information-matched provenance/correlation-aware scalar or Bayesian reduction under matched calibration, reliability estimation, training/tuning budget, and resource accounting.

## What would falsify or reduce the exploratory idea

This reduction becomes uninteresting if correlation-group information cannot be supplied or learned under the same information/resource budget, if a matched group-aware scalar loses robustly once groups are noisy/latent rather than given, or if Coalition-specific interactions survive matched provenance/correlation correction on a prospectively fixed held-out task family.

## Candidate formal question

Under a prospectively fixed duplicate/correlation/contradiction task family and matched provenance information, calibration, learning budget, and resources, do Evidence Coalitions improve held-out robustness beyond strong correlation-aware scalar/Bayesian baselines?

## New choices required before any formalization

A fresh prospective object would need to freeze at least: task/world family; source and correlation structure; whether group identity is observed or inferred; source reliability process; contradiction/duplicate semantics; Coalition mechanism; scalar/Bayesian comparators; information privileges; calibration and training/tuning budgets; held-out split; primary robustness/calibration metrics; resource accounting; seeds/runtime; success/failure criteria; and fresh protocol/package/identity bindings.

`promotion_recommendation: CONTINUE_EXPLORING` only after Evidence Analyst classification. Do not automatically continue this toy, reuse its favorable settings, or relabel this branch as formal evidence.
