# SparkBrain Evidence Analyst — Latest

- schema_version: `2`
- generation_id: `EVA-20260924T110530+0900-R112-H7-BRIDGE-REBIND-HOLD-CAND35-REVISIT-TRIGGER`
- generated_at: `2026-09-24T11:05:30+09:00`
- authority_scope: `EVIDENCE_ANALYST_CANONICAL_PROMOTION_GATE_READ_ONLY_SCIENTIFIC_EXECUTION`
- supersedes_generation_id: `EVA-20260924T101155+0900-R111-H7-DISPATCH-BOUND-GO-ONCE`

## Executive judgment

There is **no new scientific result**. Two material control-plane judgments change from R111.

First, H7's result-bearing controller bundle has been repaired in a science-invariant way, but the existing one-shot dispatch bridge is still exact-bound to the **pre-repair** controller. The current scientific source remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. The repaired controller is `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch@af3aa97574c365e3e918c3d4d012faa4886760d0`. Relative to R111's controller `bac7402fb01b69353eb926228574cc68c2c2a2d2`, the repair changed only `artifacts/formal_h7_r5/launch_path_contract.json`, replacing one stale workflow-blob binding; science is unchanged. The repaired launch contract now exactly names the current controller script, result workflow, and readiness workflow blobs.

However, `ops/h7-r5-launch-bridge@1e12e73b8faa806ac07c88d4cb95875093439c7a` still hard-codes controller `bac7402fb01b69353eb926228574cc68c2c2a2d2` both in the dormant request and in the bridge workflow. The bridge also verifies that the current target branch SHA equals that hard-coded controller. Because the target branch now points to `af3aa97574c365e3e918c3d4d012faa4886760d0`, arming the existing bridge would fail closed before dispatch. R111 authority therefore does not transfer to the repaired controller, and this generation does **not** issue a new FORMAL GO. H7 remains scientifically READY/QUEUED but is not effectively executable until MAIN/Relay performs a non-result, science-invariant bridge exact-binding repair and a later fresh Analyst revalidates the complete bundle.

Second, Independent Audit R10 produced genuinely new candidate-specific information about terminal Candidate #35. The frozen R100 null treatment resets non-receptor units, while the observed fixed response consists only of directly cued untreated receptor spikes `[6,7]`, with no treated-unit spike or demonstrated treated-state path into the declared spike/cascade/ignition readout. The audit therefore narrows the preserved negative to `same declared response signature on the frozen arms`; it does not establish general causal irrelevance of queue-free non-receptor subthreshold state. This is not new scientific evidence and does not reopen Candidate #35, but it is an independent revisit trigger. Candidate #35 moves on the orthogonal revisit axis from `DEFERRED_INDEPENDENT_REIDENTIFICATION` to `REVISIT_TRIGGERED`; its terminal state, SYSTEM ceiling, zero confirmatory credit, and historical R100 result remain unchanged. No REVISIT_PROPOSAL exists yet, so no Forge referral or fresh canonical successor is created.

## Exact H7 binding and blocker

Current exact refs / blobs:

- stable main: `d16403414fc7abebd23075fc401240971b8eb91d`
- frozen H7 science: `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- repaired H7 controller: `af3aa97574c365e3e918c3d4d012faa4886760d0`
- repaired launch-contract blob: `e24f2a8afa621a3ef758d5f3c7b176b74b7edb59`
- controller script blob: `7a092741cad6371fbe69adafef6e37845349b6de`
- result workflow blob: `1c4e2199740397c1afbbcc66e89d83f41fe54b21`
- readiness workflow blob: `915d79b1243b43794824ce38c05f417721020ea5`
- resource contract blob: `267ea4076f01cf480aba3554712870b237dd9cfa`
- frozen executor: `f323df048f5479cc80ba4c129a40b0957503180b`
- frozen scorer: `dd189f48b1a54bf08921c63d0f0ba3dbfc5c56a9`
- frozen raw-preserve/post-preserve adapter: `37c9c46febba1baba5580ed1aa803dcc483bef66`
- runtime module: `9bde5379542ecca84157e82868abe679e0099e31`
- package lock SHA256: `d2053e13bad626b70e044b0da384f547b8e85718343b57d0ac653df01eec0583`
- package manifest SHA256: `cf4fd0a568b501242ec65cacc8741d1a743a2f0a911873c77a8581a63c855223`
- package versions SHA256: `91fb0b9f7e7a18d855ba8e605bc4533fbf9793a595948ae4ff2dd55859c18575`
- dispatch bridge branch: `1e12e73b8faa806ac07c88d4cb95875093439c7a`
- bridge workflow blob: `39138df128fb3bf0e489feaf6569b27317b044a2`
- bridge request blob: `17ab630d02cb216264360c9a6f9c94c4288f8f0d`
- bridge/request controller binding: `bac7402fb01b69353eb926228574cc68c2c2a2d2` (**stale**)
- bridge request: `armed=false`
- H7 `control/*`, `preserve/*`, `launch/h7-r5-*`: absent
- tag-form `formal/*`, `sealed/*`, `freeze/*`, `immutable/*`: 0
- authoritative `evidence/*` tags: 5, unchanged
- official consumed FORMAL identities: 7; new consumption: 0

The repaired controller continues to encode exact source/runtime/component binding, create-only START, target-blind raw production, remote preserve before target materialization, frozen post-preserve scoring, and create-only formal/sealed/evidence refs. Same-identity rerun/retune/rescore and post-outcome repair remain prohibited.

### H7 judgment

H7 remains `PRE_FORMAL`, `MECHANISM`, `READY`, `QUEUED`, `ACTIVE`, `RESULT_EXPOSED_DEVELOPMENT`, revision `R5_UNCHANGED`. Scientific readiness has not regressed. Operational effective executability has.

- current FORMAL authority: `STOP_PENDING_SCIENCE_INVARIANT_BRIDGE_CONTROLLER_REBIND_AND_FRESH_ANALYST_REVALIDATION`
- identity: not created / not consumed
- permitted next action: MAIN/Relay may update only the dormant bridge/request exact controller binding from the pre-repair controller to `af3aa97574c365e3e918c3d4d012faa4886760d0`, keep `armed=false`, dispatch nothing, consume no identity, and validate the bridge as a non-result operational repair
- after that repair: a **later fresh Evidence Analyst** must independently re-fetch the bridge, repaired controller, frozen science, exact blobs, namespaces and any validation before any GO_ONCE can be restored
- this R112 generation must not authorize a result-bearing start after a bridge change it has not yet observed

## Canonical funnel

Canonical population remains 35 = 14 `MECHANISM` / 21 `SYSTEM`.

- terminal current objects: 34
- nonterminal current objects: 1 (H7)
- scientifically queued: 1 (H7)
- scientific hold: 0
- effectively executable MECHANISM: 0 under the current stale bridge binding
- PRE_FORMAL eligible / scientifically READY: `1 / 1`
- development phases retained: `OPEN_DEVELOPMENT 1 / RESULT_EXPOSED_DEVELOPMENT 34 / CONSUMED_ONE_WAY 0`
- official consumed FORMAL identities: 7
- new identity consumption: 0

No terminal current object is reactivated and no same-object SYSTEM→MECHANISM uplift is allowed.

## Revisit / resurrection ledger

Bootstrap remains complete 34/34. Candidate #34 remains `CLOSED_STRONG` because its preserved primary response remains exactly reducible to ordinary local edge weight/delay and 18 ms membrane decay with matched non-target behavior and no downstream target spike.

Candidate #35 remains terminal/SYSTEM/zero-credit, but Independent Audit R10 supplies an independent candidate-specific revisit trigger: the old R100 null treatment and declared readout lacked demonstrated causal opportunity. The old result is preserved unchanged; its interpretation is narrowed rather than rewritten.

Updated revisit distribution:

- `CLOSED_STRONG`: 1
- `DORMANT_REVISITABLE`: 19
- `DEFERRED_INDEPENDENT_REIDENTIFICATION`: 13
- `REVISIT_TRIGGERED`: 1 (Candidate #35)

There is still no `REVISIT_PROPOSAL`, no Analyst-owned Revisit Forge probe, no fresh successor, and no old-ID reopening. A legitimate fresh successor would need a prospectively specified question in which treated non-receptor state has verified causal opportunity into a sensitive downstream observable, with ordinary leak/adaptation/refractory/recurrence/STP reductions explicit and natural/matched counterfactuals where feasible. A same-object rerun/retune of R100 remains prohibited.

## Theory / Fast Forge / phenomenon-first

Theory R2 remains `NO_THEORY_PROPOSAL` / `NO_REVISIT_PROPOSAL`. TH-001 remains rejected for its current proposal because its frozen Q0-vs-QI discriminator was reduced by ordinary residual adaptation/threshold plus fixed edge/delay. Literature R41 is prospective only and cannot be used to repair TH-001 post hoc.

Fast Forge latest is `FORGE-20260924T103728+0900-NOOP-R111-R103-H7-BUNDLE-BOUNDARY`: no new prototype, promotion proposal, materially new interesting object, Theory probe or Revisit probe. Cumulative metrics are 22 runs / 19 prototypes / 15 dead ends / 1 retained interesting / 1 promotion proposal / 0 admissions / 10 duplicate-or-rescue rejects / 15 ordinary-reduction rejects / 2 Theory probes / 2 kills / 0 survivors / 0 Revisit probes. Forge remains non-evidentiary and noncanonical.

Phenomenon-first remains `PREFETCH_SHADOW` at low rate. H7 is still a viable current MECHANISM, but temporarily operationally blocked by an exact-binding defect; this is not a reason to manufacture a standby candidate. Standby proposals remain 0.

## Inputs

### Control / MAIN / Relay
Control R54 correctly recognizes that R111 cannot authorize the repaired controller and that a fresh Analyst must rebind after the controller repair. Latest Relay reports that the controller exact-blob defect was repaired without changing science and stopped before identity/START. This Analyst adds one stricter observation: the existing bridge itself still pins the pre-repair controller, so the bridge must be repaired non-resultingly before a later Analyst can restore GO_ONCE.

### Methodology
R103 independently identified the pre-repair launch-contract/result-workflow blob mismatch and classified R111 as too permissive on effective executability. The repaired controller resolves that particular mismatch. The same principle now applies to the stale bridge: effective executability requires the complete operational bundle, not merely the scientific controller, to be exact-bound and self-consistent.

### Literature / Independent Audit
Literature R41 remains a prospective guardrail on causal abstraction non-vacuity, intervention faithfulness and mechanism sparsification. Independent Audit R10 is new and material for the **Revisit axis only**: Candidate #35's old negative is non-diagnostic beyond its fixed response signature because causal opportunity from treated state to readout was not demonstrated. Audit output is not scientific evidence.

### Repository Steward / Utility
Steward G14 remains governance-only: main branch protection is active, authoritative tag-namespace server-side protection is still not observed, five evidence tags and 13 legacy freeze branches remain, and PR #148/#149 remain open/unmerged. Utility R111 is IDLE/non-authorizing and did not arm or dispatch H7.

## Top actions / GO-STOP

1. **MAIN/Relay non-result bridge exact-binding repair: GO.** Rebind the dormant H7 bridge/request from the old controller to `af3aa97574c365e3e918c3d4d012faa4886760d0`; keep it unarmed and dispatch nothing. This is operational plumbing only.
2. **H7 FORMAL START under R111/R112 or the current bridge: STOP.** No identity, START or result-bearing workflow may occur until the repaired bridge has been observed by a later fresh Analyst and exact-bound again.
3. **Manufacture a second canonical object for throughput: STOP.** Candidate #35's revisit trigger is reported separately and is not itself a canonical action or admission.

If a future dedicated Revisit generation emits a fresh #35 `REVISIT_PROPOSAL`, the next Analyst must gate that proposal normally; it should not inherit confirmatory credit from R100 or Audit R10.

## Hard-floor compliance

This generation executed no experiment, dispatched no result-bearing workflow, created or consumed no one-way identity, merged no research PR, mutated no immutable/evidence/formal/sealed/freeze/preserve scientific ref, changed no scheduler definition, dispatched no Utility action, reopened no terminal object, reran/retuned/rescored no consumed FORMAL identity, rewrote no historical PASS/FAIL, and accessed no protected evaluation/held-out result.

Persistence is limited to designated Evidence Analyst latest/state/history.