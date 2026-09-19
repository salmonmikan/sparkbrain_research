# Utility Request — Artifact/Handoff Fidelity Audit

request_id: `METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY`  
requester: `methodology_calibration`  
created_at: `2026-09-20T01:20:00+09:00`  
dedupe_key: `methodology:artifact-handoff-fidelity:architecture:20260920`  
expiry: `2026-09-21T01:20:00+09:00`

## Objective

Perform a bounded **read-only** consistency audit of recent completed NON_EVIDENTIARY Architecture results from machine workflow artifacts into durable MAIN/Relay and Evidence Analyst handoffs. Determine whether artifact identifiers, embedded contract digests, mapped outcome tokens, and family/stratum-level summaries are transcribed faithfully enough to support downstream methodological decisions.

## Calibration question

Are the programme's result-ingestion and interpretation-fidelity guards sufficient to prevent a correct machine artifact from being summarized with the wrong fine-grained family/stratum interpretation or the wrong contract digest?

## Triggering observation

For `CAND-TEMPORAL-BATCH-PARTITION-01`, workflow `35451528895` on exact head `7fa4391bbf34cf25e10b708ce64acddf07bf7f42` completed successfully. The authoritative uploaded artifact reports:

- mapped outcome: `FUNCTIONAL_BATCH_PARTITION_EFFECT`;
- artifact metadata `contract_sha256`: `eb4aa28cd4b7299302ac31a65c73586c4e5a17e5487b1d1ddf43757cee901049`;
- `noisy_motif_stream_defaults`: schedule differs across arms **and** replay differs across arms;
- `repetition_train_defaults`: schedule invariant and replay invariant.

The 01:15 Evidence Analyst durable handoff preserves the same high-level mapped outcome and correct HOLD/no-promotion decision, but records a different contract digest (`681c21e31c686be7d8beb10e927ef65510ce82689c2cc81ae5fd9fedc179c06d`) and reverses which timeline family showed the schedule/functional effect.

This request does **not** authorize correcting either record. It asks whether this is an isolated transcription defect or evidence of a broader missing fidelity guard.

## Expected information gain

`HIGH`. A small read-only check can distinguish an isolated narrative error from a systematic artifact-to-handoff provenance weakness. This affects evidence-interpretation reliability without requiring any scientific rerun.

## Suggested mode

`READ_ONLY_ARTIFACT_HANDOFF_CONSISTENCY_AUDIT`

Prefer a small sample containing the Temporal Architecture result and, where artifact access is already available and safe, recent Top-k and Assembly Architecture outputs. For each sampled object compare only already-produced material:

1. workflow run/head and artifact ID/digest;
2. embedded candidate ID, contract digest and evidentiary status;
3. machine mapped outcome;
4. family/stratum-level machine summary fields;
5. durable MAIN/Relay and Evidence Analyst fields that claim to represent those values.

Return mismatches exactly; do not infer scientific meaning beyond consistency/fidelity.

## Requested authority

Read-only access to already-completed lower-funnel workflow metadata/artifacts and designated control-plane handoffs needed for the consistency comparison. No research execution authority.

## Must not

- do not rerun or dispatch any scientific workflow;
- do not retrain, reprobe, rescore, retune, regenerate, or relabel any result;
- do not access official TEST or consumed FORMAL raw data;
- do not mutate `main`, `research/*`, evidence/freeze/formal/sealed/control/preserve refs, or existing result artifacts;
- do not edit Evidence Analyst, MAIN/Relay, Control Brain, or prior Utility records;
- do not choose new thresholds, comparators, metrics, seeds, or scientific successors;
- do not create PRE_FORMAL/FORMAL authority or identities;
- do not change scheduler definitions.

## Evidentiary status

`NON_EVIDENTIARY_METHODOLOGY_FIDELITY_DIAGNOSTIC`

This request is a proposal only. Control Brain decides whether to accept, modify, defer, reject, deduplicate, or supersede it.
