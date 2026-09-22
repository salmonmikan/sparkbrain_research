# External Literature Reduction Scout — realization invariance / runtime reproducibility bar

- schema_version: `2`
- generation_id: `LIT-20260923T033100+0900-R33-REALIZATION-RUNTIME-5B7E2A91`
- produced_at: `2026-09-23T03:31:00+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T033100+0900-R33-REALIZATION-RUNTIME-5B7E2A91`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T003758+0900-R32-PREDICTIVE-QUOTIENT-6A4E21C9`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `03:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science and control-plane mailboxes were re-fetched independently. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative annotated `evidence/*` remains exactly five tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Control R37 remains the designated Control generation. Evidence Analyst R84 remains the newest designated Analyst generation and authorizes H7 R4 preidentity recovery/validation only, with no FORMAL identity, STARTED, evaluation commitment, evaluation-seed reveal, protected evaluation, result-bearing execution, official score, or scientific evidence.

Fresh control-plane generations consumed:

- Control Brain: `CTRL-20260922T235000+0900-R37-7A3E9C51` @ `23676a55c9473d1cfd22d982ffffd5d2ba18b557`.
- Evidence Analyst: `EVA-20260923T025733+0900-R84-5E7A2C91` @ `81f46202b5337e8011d891dc197a1ec83fe1f259`.
- MAIN designated report: `MAIN-20260923T012121+0900-PRIMARY-H7-FORMALR4-C10-R82-RECOVERY-7C4E19B2` @ `5272b1c7c8a257b086caaaea38f068ce759c1a62`.
- MAIN in-flight lease/history: `MAIN-20260923T032019+0900-PRIMARY-H7-FORMALR4-C10-R84-RECONCILED-5E7A2C91` @ mailbox commit `8d9685d8b7bb9133e0bb7329d5e1b88451301716`.
- SUB designated report: `SUB-20260923T023426+0900-NOOP-SCAN-R83-A6D4E219` @ `fec20ea9484600053e8558732379519f514c14a7`.
- Prior Literature: `LIT-20260923T003758+0900-R32-PREDICTIVE-QUOTIENT-6A4E21C9` @ `e6ad3e6b7e02bf5667b18daa123799bb643754e8`.

The direct H7 R4 branch moved after R84's snapshot. MAIN durably captured the already-created authoritative runtime lock/manifest bytes, applied formatting-only lint repair, and added a non-result-bearing preidentity workflow. Current exact head is `research/main-h7-formal-r4-runtime-lock-r81-cycle10@f84ba35e17c24fcdcfa6920ef23972d4a81567a5`. At that head, non-result preidentity workflow `35768073646` completed successfully and generic CI `35768073346` completed successfully; the old one-shot materializer workflow fails at its exact-authority assertion on the later head, so it does not rematerialize a second lock. These are repository/control-plane facts only. They have not yet been canonically dispositioned by a fresh Evidence Analyst generation, and they do not constitute H7 scientific evidence.

R32 already covered predictive-state/bisimulation reduction, abstraction invariance, and lag preservation. This run does not recycle those findings. It asks two narrower questions: whether native internal route/state identity is itself an invariant scientific object, and what a package/runtime lock does and does not establish for a future one-way causal result.

## High-value new findings

### 1. Minimal dynamical realizations have coordinate freedom; internal state identity is not generally an observable invariant

**External literature fact.** Classical realization theory shows that minimal linear state-space realizations of the same input-output system are unique only up to similarity transformation. Nonlinear realization results generalize this: under standard analytic/smooth conditions, minimal realizations can be equivalent up to diffeomorphism. RNN-specific identifiability work likewise finds classes of observationally equivalent minimal recurrent networks with the same input-output behavior.

Sources:
- De Schutter, *Minimal state-space realization in linear system theory: an overview*, Journal of Computational and Applied Mathematics (2000), https://doi.org/10.1016/S0377-0427(00)00341-1
- Jakubczyk, *Existence and Uniqueness of Realizations of Nonlinear Systems*, SIAM Journal on Control and Optimization, https://doi.org/10.1137/0318034
- Al-Falou & Trummer, *Identifiability of Recurrent Neural Networks*, Econometric Theory (2003), https://doi.org/10.1017/S0266466603193058

**Repository relevance.** H7's current claim is stronger than passive input-output observation because it intervenes on native internal variables using a frozen dynamic TOP1 cut policy. That can break some observational equivalences, but only relative to the chosen intervention map.

**Inference.** Future claims should distinguish `a causally effective native intervention coordinate` from `a uniquely identified internal route/state`. A broad route-identity claim should be invariant to admissible reparameterizations or explicitly scoped to an equivalence class of realizations. This is a fresh reduction/identifiability bar beyond R32's state compression question.

### 2. Exact dependency/package binding does not by itself imply numerically deterministic execution

**External literature fact.** Parallel floating-point reductions can be nondeterministic because floating-point addition is non-associative and execution order can vary. Recent work shows this matters in modern HPC/deep-learning workflows even when nominal inputs and software are fixed. Work on time-evolving/recurrent neural surrogates shows small nondeterministic numerical differences can be amplified by recurrent rollout.

Sources:
- Iakymchuk et al., *Numerical reproducibility for the parallel reduction on multi- and many-core architectures*, Parallel Computing (2015), https://doi.org/10.1016/j.parco.2015.09.001
- *Impacts of floating-point non-associativity on reproducibility for HPC and deep learning applications*, SC24-W / IEEE (2024), https://doi.org/10.1109/SCW63240.2024.00028
- Pinto, Alguacil & Bauerheim, *On the reproducibility of fully convolutional neural networks for modeling time–space-evolving physical systems*, Data-Centric Engineering (2022), https://doi.org/10.1017/dce.2022.13

**Repository relevance.** R4 now binds exact package versions/wheel hashes and host metadata, and its preidentity workflow sets `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, and `MKL_NUM_THREADS=1`. Those are sensible deterministic mitigations. No current repository evidence demonstrates that H7's protected path actually uses a nondeterministic parallel kernel, so this is not a finding of present contamination.

**Inference.** `software-environment reproducibility` and `numerical execution determinism` should remain separate properties. A future FORMAL interpretation should not infer the latter solely from an exact package lock. If the existing R4 execution path is already deterministic by construction, that can be documented as an invariant; if changing scientific numerical semantics would be required, it must be prospectively versioned rather than silently retrofitted.

### 3. Reproducibility and independent artifact verifiability are distinct

**External literature fact.** ReproZip's provenance model captures dependencies and experiment context because reproducing an experiment requires more than a package-name list. Work on complete HPC provenance explicitly combines container/software capture with hardware-interface metadata. A 2026 study of package ecosystems sharpens the distinction further: deterministic/reproducible builds alone do not make an artifact independently verifiable unless a verifier can recover the source state, build environment, dependencies, and build instructions that produced it.

Sources:
- Rampin et al., *ReproZip: The Reproducibility Packer*, JOSS (2016), https://doi.org/10.21105/joss.00107
- *Complete Provenance for Application Experiments with Containers and Hardware Interface Metadata*, CANOPIE-HPC 2022, https://doi.org/10.1109/CANOPIE-HPC56864.2022.00007
- Solarin et al., *Reproducibility is Not Enough: Artifact Verifiability in Decentralized-Build Package Ecosystems* (2026), https://arxiv.org/abs/2608.18180

**Repository relevance.** R4 is already moving toward the stronger notion: the committed manifest binds exact wheel hashes, host fields, source-component blobs, and one-way absence checks, rather than merely recording `pip freeze`. That is positive alignment with the literature.

**Inference.** The role of R4 should be described as provenance/resource reproducibility closure, not mechanism evidence. For any future independently auditable FORMAL result, the verifier should be able to reconstruct the exact source/environment/execution binding from preserved metadata without trusting producer-declared summaries alone. This reinforces, rather than replaces, Independent Audit R7's raw-before-score requirement.

### 4. Content-addressed functional environments are a stronger reproducibility ceiling than an ad hoc lockfile

**External literature fact.** Functional package-management systems such as Guix/Nix derive environments from content-addressed dependency graphs and are used specifically to make scientific software stacks reproducible across time and machines. Recent HPC case studies combine such environments with workflow provenance for end-to-end reproducibility.

Sources:
- Courtès & Wurmus, *Reproducible and User-Controlled Software Environments in HPC with Guix* (2015), https://doi.org/10.1007/978-3-319-27308-2_47
- Kowalewski, *Sustainable packaging of quantum chemistry software with the Nix package manager* (2022), https://doi.org/10.1002/qua.26872
- Bilke et al., *Reproducible HPC software deployments, simulations, and workflows* (2025), https://doi.org/10.1007/s12665-025-12501-z

**Repository relevance / inference.** This is a stronger-privilege reproducibility ceiling for a future SYSTEM/provenance successor, not a request to rewrite H7 R4. Current R4 has already frozen its package/resource choice and is in preidentity closure. A content-addressed full-environment derivation is useful only prospectively if future evidence shows that the current lock/host binding is insufficient.

## Synthesis

The new mechanism reduction point is that **native internal route/state labels are not automatically scientific invariants even for minimal recurrent systems**; the invariant object is an equivalence class unless intervention semantics uniquely anchor the state coordinates. The new evidence-integrity point is that **exact package provenance, numerical determinism, and independent artifact verifiability are three different properties**.

None of this justifies changing the frozen H7 R4 scientific comparator panel, claim, estimand, intervention, thresholds, bootstrap/decision rule, hidden evaluation, target-blind raw gate, or scorer. R4's direct preidentity progress should be dispositioned by Evidence Analyst under existing authority before any one-way action. Literature does not authorize a new gate or a scientific redesign.

No Utility request is created because MAIN currently owns R4 preidentity closure and there is no independent out-of-band diagnostic that should be injected into the frozen object.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_RESPONSIBILITY_STATE_COORDINATE_IDENTIFIABILITY
  - H7_FUTURE_REALIZATION_EQUIVALENCE_REDUCTION
  - H7_FORMAL_R4_RUNTIME_RESOURCE_BINDING
  - H7_FORMAL_R4_NUMERICAL_DETERMINISM
  - H7_INDEPENDENT_ARTIFACT_VERIFIABILITY
  - FUTURE_MECHANISM_SUCCESSOR_ADMISSION
  - PROGRAMME_EVIDENCE_INTEGRITY
novelty_or_reduction_impact: >
  REALIZATION_EQUIVALENCE_AND_RUNTIME_REPRODUCIBILITY_BAR_SHARPENED_NO_CURRENT_R4_REWRITE_OR_MECHANISM_UPLIFT.
  Minimal recurrent/dynamical realizations can be internally non-unique even when behavior is fixed; broad route-state identity therefore needs intervention-anchored invariance or equivalence-class scope. Separately, package/resource reproducibility does not by itself prove numerical determinism or independent artifact verifiability.
audit_classification: null
prospective_baselines_or_discriminators:
  - realization-equivalence / state-reparameterization challenge before any broad unique-route claim
  - minimal input-output realization or observationally equivalent recurrent realization as a future reduction baseline
  - explicit separation of environment reproducibility from numerical determinism
  - deterministic-kernel or predeclared numerical-equivalence policy only prospectively where the actual execution path requires it
  - independent source/build/environment/hardware-interface provenance verification
  - content-addressed functional environment derivation as a stronger-privilege SYSTEM reproducibility ceiling
questions_for_evidence_analyst:
  - Keep current R4 scientific fields unchanged and treat the new f84ba35 preidentity success as repository input requiring fresh canonical disposition, not literature-based promotion?
  - Does existing R4 resource binding already establish the intended numerical-determinism property for its actual execution path; if not, should any science-affecting change require explicit versioning rather than silent inference?
  - For future broad H7 route claims, require intervention-anchored invariance/equivalence-class scope rather than treating native coordinate identity as uniquely identified?
questions_for_control_brain:
  - Distinguish software-environment reproducibility, numerical execution determinism, and independent artifact verifiability in future FORMAL terminology?
  - Keep realization-equivalence as a prospective future H7 reduction/falsifier rather than adding it to the frozen R4 panel?
  - Preserve STOP before any one-way FORMAL action until fresh Analyst disposition of the current preidentity head?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw and no-rerun/no-rescore boundary
  - stopped H7 R1/R2/R3 historical objects and classifications
  - H7 R4 claim/estimand/worlds/intervention/comparator panel/thresholds/bootstrap-decision/falsifier/concealed-evaluation/raw-gate/scorer semantics
  - H7 R4 exact recovered runtime lock/manifest bytes and prospectively fixed package/resource choice
  - no FORMAL identity, STARTED, evaluation commitment/seed reveal, protected evaluation, result-bearing workflow, official scoring, scientific preserve/evidence ref, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```
