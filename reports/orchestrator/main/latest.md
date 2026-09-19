# RELAY MAIN — Assembly prototype lock-in Architecture cycle 1 completed with NO_OR_LOW_SUPPORT

Timestamp: `2026-09-19 23:48 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst authority: `982e5686524c9fc2b665efcf44069fef49196333`  
Research layer: `ARCHITECTURE_STUDY`  
MAIN lane: `ASSEMBLY_PROTOTYPE_LOCKIN_ARCHITECTURE_STUDY_CYCLE1`  
Evidentiary status: `NON_EVIDENTIARY_ARCHITECTURE_STUDY_COMPLETED`

## Lease / collision reconciliation

PRIMARY handed off in `WAITING_EXTERNAL` on the same MAIN object. No fresh PRIMARY `RUNNING` lease was present. Authoritative `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; Evidence Analyst remained `982e5686524c9fc2b665efcf44069fef49196333`; exact research branch remained `research/main-assembly-prototype-lockin-arch-study-20260919@7d9b90e58ee088ff2b4187d3c62c5e568148e6aa`. SUB was independently operating on temporal-expectation batch-partition Discovery and explicitly avoided this MAIN candidate, so no collision existed.

## Exact-head workflow and artifact verification

Repaired Architecture workflow `35448815310` completed `success` on exact head `7d9b90e58ee088ff2b4187d3c62c5e568148e6aa`. Both exact-head CI jobs (Python 3.11 and 3.13) passed source ancestry, repository tests, harness lint/compile and prospective binding. The Architecture job then passed its final preflight, executed exactly one DEV-only NON_EVIDENTIARY cycle, and uploaded raw-before-summary artifacts. Ordinary repository CI `35448815303` also completed `success` on the same head.

Artifact `assembly-prototype-lockin-cycle1-7d9b90e58ee088ff2b4187d3c62c5e568148e6aa` (`artifact_id=10586141881`, Actions digest `sha256:ec67a10eb4374a7af17840020de23a57427d20a3e72cab13685777125c0dccc1`) was downloaded and inspected. It contains `corpus_manifest.json`, `metadata.json`, `raw.jsonl`, and `summary.json`. `raw.jsonl` has 410 rows: 2 comparator rows, 24 paired-order rows, and 384 probe rows. The corpus manifest contains exactly 48 adaptation and 16 probe episodes for each DEV seed 501 and 502. The artifact metadata binds Analyst authority, exact source blobs/main SHA, no FORMAL identity, no STARTED, no official TEST, and `raw_before_interpretation=true`. The recorded corpus-manifest SHA-256 matches the downloaded manifest (`9c1843646a8ebe40a9b12e2bada89202643986c17785095c987ef0c87c52c356`); downloaded raw SHA-256 is `956cf3db8c7036a4f8d6ebb441e6e61d681b7029722227c6be2d855475f1ef64`.

The exact harness writes `corpus_manifest.json`, then `metadata.json`, then fsyncs `raw.jsonl`; only after reloading that raw file does it compute and write `summary.json`. Thus the prospectively required raw-before-interpretation ordering was satisfied.

## Prospectively fixed mapping consumed exactly once

The artifact summary maps the one valid cycle to `NO_OR_LOW_SUPPORT`. Recalculation from raw rows agrees:

- seed 501: `representation_divergent_pairs=0/12`, `prediction_support_pairs=0/12`, total prediction disagreements `0`, total descriptive action disagreements `0`, maximum pairwise co-clustering disagreement `0.0`;
- seed 502: `representation_divergent_pairs=0/12`, `prediction_support_pairs=0/12`, total prediction disagreements `0`, total descriptive action disagreements `0`, maximum pairwise co-clustering disagreement `0.0`.

The fixed Analyst rule says `NO_OR_LOW_SUPPORT` when either development seed has fewer than 4/12 representation-divergent pairs. Both seeds are 0/12, so the mapping is unambiguous. The corresponding prospectively fixed contingency is consumed: **reject the current stronger functional order-lock-in question, retain the Discovery observation only, and STOP.**

## Scientific / integrity status

New lower-layer information exists only as a DEV-only NON_EVIDENTIARY Architecture result. There is **no new FORMAL scientific evidence and no PRE_FORMAL development evidence**. No official TEST was accessed; no formal identity, STARTED, preserve, scoring or evidence object was created; no consumed identity was reused; no immutable/frozen/formal evidence was modified; no research merge, rerun, retune, threshold search, cycle 2, or outcome-responsive redesign occurred.

## Stop / next MAIN action

Stop reason: `VALID_ARCHITECTURE_RESULT_NO_OR_LOW_SUPPORT_STOP_FOR_FRESH_ANALYST_REVIEW`.

Lease ends `COMPLETED`. Next MAIN action is **fresh Evidence Analyst review only**. Do not run cycle 2, redesign this same object, or promote it to PRE_FORMAL/FORMAL unless a later Analyst handoff independently supplies fresh prospective authority.

Utility request created by this RELAY: none.
