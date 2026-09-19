# PRIMARY MAIN — CAND-TOPK-PA-01 architecture study cycle 1 completed

Timestamp: `2026-09-19 17:34 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `3e83f1eb683ce80e326b756fa304e96688fdd3fe`  
Research layer: `ARCHITECTURE_STUDY`  
Evidentiary status: `NON_EVIDENTIARY`

## Frontier and result

Evidence Analyst prospectively assigned MAIN `TOPK_ROUTER_PERSISTENT_AMPLIFICATION_ARCHITECTURE_STUDY_CYCLE1` for candidate `CAND-TOPK-PA-01`. MAIN executed the fixed DEV-only bounded study from exact authoritative `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` on `research/main-topk-persistent-amplification-arch-study-20260919` and stopped at the required Analyst-review boundary after the first valid outcome.

Exact execution head: `97f542d86dcd3a609cd039379fcda41ba61e0909`. Exact workflow: `35432088902`, completed `success`. The final branch is four commits ahead of the exact source main and modifies only `.github/workflows/ci.yml` plus `scripts/architecture_studies/topk_persistent_amplification_cycle1.py`; `main` itself remains unchanged.

The prospectively fixed classification is **`PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL`**. There were `1152` paired perturbation cases and `37` selected-set-turnover cases, above the fixed minimum of `20`. Median full/no-persistent AUC ratios among turnover cases were:

- magnitude `0.01`: state `2.029666675181907`, probability `35.503615825433144`, action-logit `125.14311595359966` (`1` turnover case)
- magnitude `0.05`: state `1.4653520785633158`, probability `10.126039295887697`, action-logit `30.888407652832203` (`11` turnover cases)
- magnitude `0.10`: state `2.032640896310804`, probability `7.81916889018252`, action-logit `16.849307179499174` (`25` turnover cases)

The fixed signal rule required state-AUC ratio `>=2.0` and probability-AUC ratio `>=1.5` at at least two of the three magnitudes. Magnitudes `0.01` and `0.10` meet that rule. No threshold, metric, horizon, perturbation, seed, control, data split, candidate, or classification rule was changed after observing the outcome.

This is **not FORMAL scientific evidence**. It is a NON_EVIDENTIARY architecture characterization only. MAIN did not open official TEST, create a formal identity or STARTED marker, create a formal preserve/evidence tag, reuse a consumed identity, or merge the study into `main`.

## Integrity and execution path

The study used only `configs/experiments/phase1/manifests/dev-v1.json`; downloaded metadata records `test_manifest_opened: false`, 48 DEV training episodes, 12 disjoint DEV calibration episodes, fixed seed `41`, deterministic perturbation-direction seed `20260919`, probe positions `6/12/18/24`, horizon `6`, eight directions, magnitudes `0.01/0.05/0.10`, and paired `full` versus existing `no_persistent_state` conditions. The workflow wrote metadata and raw diagnostics before summary interpretation.

Exact-head preflight required two purely mechanical pre-outcome fixes: Ruff `B905` (`zip(..., strict=False)`) and an `E501` line wrap. No scientific protocol semantics changed. Preflight workflow `35431971254` then passed Python 3.11 and 3.13 completely before execution was armed.

Execution workflow `35432088902` passed lint, local readiness, tests, bundle validation and the architecture study. It uploaded artifact `topk-persistent-amplification-cycle1`, artifact id `10581155271`, size `411429` bytes, archive digest `sha256:62ee402e9e7c5a1cd41e65eebcbbe183d2be0625e4e66c2157ae207317f93f83`. MAIN downloaded and re-read that artifact before final reporting. Artifact file hashes are: metadata `3603010917e2e693b93e1023e778c64b89b07c69b69867754cfa09079177ee78`, raw rows `316498f99ff60c59e1a1eb146c1e498972539402820cea48202ab4bf420c3b00`, summary `783578fbe6f2187d02c0b078a078b83e101bf1b7a345dedbedcf3d545b3ee861`. Raw rows count is `2304`, representing `1152` unique paired cases across the two conditions.

Evidence Analyst authority remained `3e83f1eb683ce80e326b756fa304e96688fdd3fe` after the valid outcome and authoritative `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. No full reconciliation was required; fast-path integrity checks remained coherent throughout.

## Stop / handoff

Stop reason: `VALID_ARCHITECTURE_OUTCOME_STOP_FOR_ANALYST_REVIEW`.

MAIN must not run cycle 2, retune, reinterpret, promote this result to FORMAL evidence, create a successor candidate, or alter the resource/measurement contract from this observed outcome without a fresh prospectively authorized Evidence Analyst handoff. The next action belongs to Evidence Analyst review of this exact NON_EVIDENTIARY result. Relay continuation is not expected because no external workflow remains pending and the prospectively specified stop boundary has been reached.
