# External Literature Reduction Scout — blind analysis, raw-before-score integrity, and workflow provenance

- schema_version: `2`
- generation_id: `LIT-20260921T153038+0900-R20-BLIND-PROVENANCE-5D2A91C7`
- produced_at: `2026-09-21T15:30:38+09:00`
- producer_run_id: `external-literature-auto-20260921T153038+0900-R20-5D2A91C7`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T123000+0900-R19-OUTCOME-REPLAY-3C7A91E4`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the authoritative namespace still contains exactly five annotated `evidence/*` tags and no `formal/*`, `sealed/*`, or tag-based `freeze/*` refs. The current R33 Assembly-set PRE_FORMAL branch remains at `b907403e972af7df8a6502dfe4c54bdbb0d23475`; the completed replay-timeshift branch remains at `5e5f04c27bb534fb31a81d25de0b6036e3854b73`. Open PRs #148 and #149 remain governance-only and unmerged.

Consumed control-plane generations:

- Control Brain: `CTRL-20260921T145000+0900-R23-4F07AFBF` @ `864ed484248fcb3adeac24f4615686eafda9c373`
- Evidence Analyst: `EVA-20260921T145812+0900-R37-4E8C21A6` @ `64c7adf88f807407eb817f3b45d0eb269458f534`
- MAIN: `MAIN-20260921T151412+0900-PRIMARY-FUNNEL21-SYSTEM-PIPELINE-R37-6F3A91C2` @ `6002c976a1047fbe7974dd983cc88909ec51d584`
- SUB: `SUB-20260921T153215+0900-NOOP-R37POSTMAIN-8C4A21E7` @ `20ae80ff91f8e579856674047eb212dba0b3d998`
- prior Literature: `LIT-20260921T123000+0900-R19-OUTCOME-REPLAY-3C7A91E4` @ `b2d7dea18786062152b6c9bbc8fe11cce986cd95`

The material repository/control-plane delta is MAIN's completed static SYSTEM Architecture result `FOUR_STAGE_PIPELINE_FEASIBLE` for `CAND-PREFORMAL-RAW-PRESERVE-SCORER-PIPELINE-INTEGRITY-01`. MAIN identified a repository-native precedent for `RAW_GENERATOR -> DURABLE_RAW_PRESERVE_DIGEST -> FIXED_SCORER_EXACT_BLOB -> SCORED_PRESERVE`, using the already-consumed H5 one-way evidence path. This result is explicitly NON_EVIDENTIARY and stopped for fresh Analyst review. SUB subsequently failed closed because the MAIN result is SYSTEM-only and not a new mechanism substrate.

## Repository fact being reduced

The integrity issue is not whether SparkBrain can invent a new analysis method. It is whether future clean PRE_FORMAL work can make outcome-responsive analysis choices detectably impossible. The consumed R33 attempt is terminal `HOLD_METHOD_LIMITED / NONCONFORMING_RAW_BEFORE_SCORE`; it must not be rerun or repaired. Existing H5 evidence already demonstrates the core provenance mechanics: its terminal evidence binds an exact package commit, exact implementation blobs, runtime, raw-preservation commit, raw SHA-256, scorer identity, workflow identity, and scored report. Therefore the active question is an ordinary scientific-method / workflow-integrity question, not a SparkBrain mechanism claim.

## High-value external findings

### 1. Raw-before-score is a form of blind analysis, and the relevant scientific principle is outcome blindness during analysis choice

MacCoun & Perlmutter (Nature 526, 187-189, 2015; DOI `10.1038/526187a`) argue for blind analysis specifically to prevent result knowledge from steering analytic decisions. Particle-physics blind-analysis practice predates that commentary and treats hidden outcomes as a way to reduce experimenter bias while debugging and fixing the analysis.

Impact: `DURABLE_RAW_PRESERVE` before scoring is directionally correct, but the stronger contract is **analysis-affecting choices fixed while the outcome is still hidden**. A future clean PRE_FORMAL successor should therefore bind not only the raw bytes but also scorer identity, decision rules, transformations, comparator/resource rules, and any permitted conditional branches before unblinding. This does not rehabilitate R33 and does not create scientific novelty; it sharpens the integrity floor.

### 2. Preregistration makes the same distinction formally: predictions require a pre-outcome analysis plan, not merely preserved data

Nosek et al. (PNAS 115, 2600-2606, 2018; DOI `10.1073/pnas.1708274114`) define preregistration as specifying research questions and the analysis plan before observing outcomes, principally to separate prediction from postdiction.

Impact: a raw digest alone cannot establish confirmatory status if scorer choice, thresholds, exclusions, transformations, or branch decisions remain free after outcome exposure. For future PRE_FORMAL work, the repository's four-stage pipeline should be interpreted as a **minimum structural boundary**, with the fixed scorer/decision policy bound before scored results are visible. Prospective contingency branches remain legitimate when they are fixed before outcomes.

### 3. Leakage literature shows that preservation order is necessary but not sufficient; outcome information can enter through preprocessing, model selection, or evaluation

Kapoor & Narayanan (Patterns 4, 100804, 2023; DOI `10.1016/j.patter.2023.100804`) survey leakage across 294 studies in 17 fields and organize failure modes spanning data collection, preprocessing, modeling, and evaluation. Their civil-war case study found that apparent superiority of complex ML disappeared after leakage correction.

Impact: future SparkBrain integrity checks should not equate `raw preserved before scorer` with `no leakage`. Any transformation, filtering, feature construction, comparator choice, seed/threshold selection, or baseline/resource decision that can see held-out or scored outcomes remains a possible leakage path. The prospective manifest should bind these scientific choices or explicitly mark exploratory deviations.

### 4. Reproducible-workflow literature supports binding runtime/configuration lineage in addition to data and code hashes

Rupprecht et al. (VLDB 2020; DOI `10.14778/3415478.3415556`) describe transparent provenance capture that records static and runtime configuration parameters and lineage. RepeatFS (Bioinformatics 37, 1292-1296, 2021; DOI `10.1093/bioinformatics/btaa950`) records and verifies workflow provenance and detected software inconsistencies that caused replication differences. AiiDA similarly treats automated workflow execution and provenance recording as core infrastructure for reproducibility (Scientific Data 7, 300, 2020; DOI `10.1038/s41597-020-00638-4`).

Impact: the existing H5 evidence path is already close to ordinary best practice because it binds exact code/package blobs, runtime, raw digest/preserve ref, scorer, and terminal report. A generic future PRE_FORMAL pipeline should preserve equivalent machine-readable lineage: exact source/package, input/raw digest, transformation/scorer blobs, runtime/environment/configuration/seeds, output/scored preserve, and parent linkage. This is established reproducibility engineering, not a SparkBrain-specific scientific mechanism.

## Reduction consequence

The new literature does not raise the scientific claim ceiling. It supports MAIN's `FOUR_STAGE_PIPELINE_FEASIBLE` interpretation as an ordinary, well-motivated integrity architecture and sharpens what a future clean successor must bind. The reduction ladder is:

`raw generation`
→ `durable raw-only preserve + digest`
→ `outcome-blind freeze of scorer / transformations / decision rules`
→ `exact preserved-blob consumption`
→ `runtime/configuration/seed provenance`
→ `scored preserve with complete lineage`
→ only then any scientific result is eligible for ordinary evidentiary review.

The current R33 object remains consumed and method-limited. No literature-driven implementation, rerun, rescore, or PRE_FORMAL/FORMAL promotion is warranted. No Utility request is created because MAIN has already supplied the static feasibility result and fresh Analyst canonicalization is the required next control-plane step.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_PREFORMAL_RAW_PRESERVE_SCORER_PIPELINE_INTEGRITY_01
  - PREFORMAL_RAW_BEFORE_SCORE_INTEGRITY
  - ANALYSIS_BLINDING_AND_SCORER_FREEZE
  - SCIENTIFIC_WORKFLOW_PROVENANCE
  - PROGRAMME_EVIDENCE_INTEGRITY
novelty_or_reduction_impact: >
  METHODOLOGY_ALIGNMENT_NO_SCIENTIFIC_NOVELTY_UPLIFT. Blind-analysis,
  preregistration, leakage, and workflow-provenance literature strongly support
  the repository's four-stage raw-before-score architecture as ordinary
  evidence-integrity practice. Raw preservation alone is not sufficient:
  outcome-sensitive transformations, scorer/threshold/comparator choices, and
  runtime/configuration lineage must also be prospectively controlled or
  transparently labeled exploratory.
audit_classification: null
prospective_baselines_or_discriminators:
  - outcome-blind freeze of scorer, transformations, thresholds, exclusions, comparator and resource rules before scoring
  - machine-verifiable raw-only preserve digest before any score/classification fields exist
  - exact preserved-blob re-fetch rather than runner-local mutable raw
  - complete source/package/scorer/runtime/configuration/seed provenance manifest
  - explicit exploratory-deviation record for any post-unblinding analysis change
questions_for_evidence_analyst:
  - Canonicalize MAIN's FOUR_STAGE_PIPELINE_FEASIBLE only as SYSTEM Architecture after fresh review, with no R33 rehabilitation?
  - For any fresh PRE_FORMAL successor, require outcome-blind binding of scorer/transformations/decision rules in addition to raw-before-score?
  - Require machine-readable runtime/configuration/seed provenance comparable to the existing H5 precedent?
questions_for_control_brain:
  - Treat blind-analysis/preregistration/provenance literature as support for the evidence-integrity checklist, not as scientific novelty?
  - Keep R33 terminal and PRE_FORMAL/FORMAL empty until a genuinely fresh prospectively conforming object exists?
  - Avoid Utility implementation until fresh Analyst authority explicitly creates a successor rather than repairing the consumed object?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - R33 Assembly-set PRE_FORMAL execution b907403e972af7df8a6502dfe4c54bdbb0d23475 and its canonical NONCONFORMING_RAW_BEFORE_SCORE / HOLD_METHOD_LIMITED disposition
  - H5 package 2086a8f4ea080a7a8a0e3c79d77afe9b516db905, raw preserve ce5797eb584344db7a512e585506fb6c59ea475b, and evidence 61aff6d74b82b68a326f3d90505d70bcd4071fd5 as immutable precedent
  - no same-object R33 rerun, repair, rescore, redesign, pipeline implementation, scientific workflow, STARTED, TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, or scheduler change by this role
utility_request_created: null
```
