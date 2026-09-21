# SparkBrain Methodology Calibration Audit — 2026-09-21 17:48 JST

schema_version: `2`  
generation_id: `METHCAL-20260921T174820+0900-R40-4C8E21A7`  
produced_at: `2026-09-21T17:48:20+09:00`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260921T162214+0900-R39-5A7C3E91`

## Result

`MATERIAL_CALIBRATION_UPDATE`

Overall classification remains **`MIXED_CALIBRATION`**.

Two material methodology-calibration observations are new.

First, Fresh Evidence Analyst R39 has added a phenomenon-first shadow supply path while preserving canonical Funnel-v2.1 separation. Canonical science remains `30/30` classification-complete, `MECHANISM=13 / SYSTEM=17`, Architecture `M0/S1`, PRE_FORMAL eligible=`0`, READY=`0`, viable executable MECHANISM=`0`. The open no-target episode `NTE-20260921-R34-POST-REPLAY-v1` is one episode at canonical check_count=`4`, not four independent scientific failures or successes. The retained shadow `SHADOW-PHENOM-SOURCE-RELIABILITY-ROLE-TRANSFER-01` is explicitly noncanonical, non-authorizing, unallocated, unexecuted, and excluded from executable Top-3. This is well calibrated as a candidate-supply pressure-relief mechanism: it can broaden discovery without manufacturing a MECHANISM object or contaminating conversion denominators. `phenomenon_first_shadow_supply_separation=KEEP`. However, no shadow has yet been promoted through a fresh mechanism bridge, ordinary reduction, resource contract, falsifier, and prospective claim ceiling, so `shadow_to_mechanism_admission=INSUFFICIENT_EVIDENCE`. A retained phenomenon must never itself count as the required one-in-three MECHANISM selection or close the no-target episode.

Second, live synthetic pipeline conformance has not yet been reached. On the active SYSTEM conformance branch, the first commit intended to execute frozen synthetic conformance failed at CI Lint before Local readiness/Test/Validate. Subsequent same-object commits repaired lint-only/preflight code and re-bound hashes; the current exact-head CI `35578428792@5527ac14d4d19078a91aa40f8825d5a4f41f0a91` again failed at Lint in both Python 3.11 and 3.13, with result-bearing stages skipped. Direct diffs show the repairs are currently non-scientific/preflight-only: an `os.fsync` import refactor, contract hash rebinding, and Ruff import-order suppression in the conformance test. No synthetic fixture/scorer result was observed.

This does **not** establish a hard-floor breach or post-outcome repair, but it exposes a semantic boundary that is too implicit. `pre_conformance_preflight_repair_boundary=CLARIFY`. In-place repair may be acceptable only while a machine-checkable `result_bearing_stage_reached=false` condition holds and the change is demonstrably preflight/non-analysis, with changed paths/hashes recorded and refrozen prospectively. Once raw fixture generation, scorer execution, conformance metrics, terminal classification, or any result-bearing stage is reached, visible output must force terminalization and a fresh successor for redesign. Generic wording such as “after output visibility” is insufficient because lint/build logs are outputs but do not reveal the synthetic/scientific result.

The exact-head CI failure is newer than the latest Analyst canonicalization, so it is not used to alter canonical funnel counts or dispositions. SUB correctly failed closed rather than inferring a repair, successor, or scientific target from the MAIN-owned CI event.

All mandatory Funnel-v2.1 semantics otherwise remain stable: `claim_ceiling` is current-object scoped; no completed SYSTEM object is upgraded to MECHANISM; `preformal_eligible != READY`; READY remains development/test readiness and `HIDDEN_SECOND_FORMAL_GATE=false`; canonical HOLD remains multidimensional; classification completeness gates policy conclusions; no genuine SYSTEM-over-comparable-MECHANISM exception has yet occurred; SYSTEM integrity work retains genuine architecture/reproducibility value.

Raw-before-score execution, preserve-before-score separation, durable immutable PRE_FORMAL raw preservation, and producer HOLD-enum conformance remain `TIGHTEN`. Causal comparator equivalence remains `SPLIT_BY_CLAIM_TYPE`. No universal numeric readiness/support threshold is recommended.

PASS reachability is **`PRE_FORMAL_REACHED; CLEAN_FOUR_STAGE_ARCHITECTURE_FEASIBLE; LIVE_SYNTHETIC_CONFORMANCE_NOT_YET_REACHED_DUE_PREFLIGHT_CI_FAILURE; LIVE_SCIENTIFIC_PASS_BLOCKED_PENDING_FRESH_CONFORMING_PIPELINE`**. The correct response is not to tighten READY or reuse R33, but to finish a fresh prospective conformance path without allowing preflight repair to become an output-driven redesign channel.

Authoritative source-of-truth was independently refreshed before strategy summaries: stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five annotated `evidence/*` refs remain present; `formal/*=0`, `sealed/*=0`, tag-based `freeze/*=0`. Control is `CTRL-20260921T145000+0900-R23-4F07AFBF@864ed484248fcb3adeac24f4615686eafda9c373`; fresh Analyst is `EVA-20260921T170125+0900-R39-4B7D21C8@773fb8a5b1a5cb87ff936c399872d6a5a2099b25`.

No Utility request was created. Hard floor remains **`CONFIRMED / DO NOT RELAX`**. Historical R33 remains terminal and may not be rerun, repaired, rescored, retuned, or upgraded.
