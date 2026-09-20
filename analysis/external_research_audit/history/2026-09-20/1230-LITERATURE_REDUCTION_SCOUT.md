# SparkBrain Literature Reduction Scout — 2026-09-20 12:30 JST

- schema_version: `2`
- generation_id: `LIT-20260920T123000+0900-R11-ASSEMBLY-LIFECYCLE-7E4A1C2B`
- produced_at: `2026-09-20T12:30:00+09:00`
- producer_run_id: `external-literature-auto-20260920T123000+0900-R11-7E4A1C2B`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LEGACY_GENERATION_UNKNOWN`
- role: `LITERATURE_REDUCTION_SCOUT`
- selected_slot_jst: `12:30`
- schedule_inference_used: `false`

## Input generations / exact handoffs

- Control Brain: `LEGACY_GENERATION_UNKNOWN` @ `b35068cbee426c99c3cc1f6dd23053778a2bd88a`
- Evidence Analyst: `EVA-20260920T115704+0900-R12-A6B8DE50` @ `dcaa02fc25506ff4e8b14d7540b6c754a8a6da98`
- MAIN: `MAIN-20260920T121227+0900-PRIMARY-FUNNEL21-HOLD-7C41A2D9` @ `0d1371bee14b95e126cef203f516c0033d538363`
- SUB: `SUB-20260920T114400+0900-THEORY-ASMFB-6D2A91C4` @ `03c8981d86ce0086cf5a01798a80e8275e58b711`
- Prior Literature stream: `LEGACY_GENERATION_UNKNOWN` @ `f399e9d14ef6d491135d19161b8c1d7986b94e5b`

## Repository state independently re-fetched

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative `evidence/*` tag set remains five entries; tag-based `formal/*` and `sealed/*` remain empty. Legacy `freeze/*` branches, `preserve/*` refs, and `control/*` refs were independently re-fetched and remain present; no fresh FORMAL identity, STARTED transition, or immutable-evidence mutation was observed. PR #148 and #149 remain open, unmerged, and mergeable.

The most relevant completed lower-funnel repository object is `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` on `research/main-assembly-mature-capacity-lifecycle-contract-arch-study-20260920@13239163f6fecb2b61ea2189a5a94ba12b6cb3d6`, terminal `LIFECYCLE_UNSPECIFIED_AND_SUPPORTED_SATURATION_UNESTABLISHED`. Stable source fixes `max_candidates=256`; on a new unmatched pattern at capacity it prunes stale immature candidates and, if still full, declines to create a new candidate. The prune condition does not reclaim mature candidates. The repository result explicitly does not establish that supported/default execution reaches saturation or that mature turnover is required.

Fresh Evidence Analyst generation `EVA-20260920T115704+0900-R12-A6B8DE50` classifies this as `SYSTEM / HOLD_SYSTEM_TERMINAL / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED / preformal_eligible=false`; it also rejects `CAND-V05-ASSEMBLY-FEEDBACK-CAUSALITY-01` after a matched DEV-only probe found mature/suppressed Assembly recognition changed readout status but not the exact lower `v04_result` or lower field state. Current MAIN is intentionally idle with no active/queued Architecture object; SUB retains bounded Discovery ownership. No current object clears PRE_FORMAL or FORMAL.

Prior Literature through 09:30 was read first. This run does not recycle the earlier Homeostasis population/source, refractory, temporal batching, topology-config, Top-k/hysteresis, H7 causal-credit, eligibility, reservoir, or provenance reductions.

## Genuinely new external literature findings

### 1. Bounded prototype/category memory with explicit pruning is an established streaming-learning design, not a novel lifecycle principle

Cao et al., *Density-Based Clustering over an Evolving Data Stream with Noise* (SDM 2006, DOI `10.1137/1.9781611972764.29`) introduced DenStream for one-pass evolving streams under limited memory. It maintains compact potential/outlier micro-clusters and uses a pruning strategy tied to decayed support. More recently, Ye & Bors, *Online Task-Free Continual Generative and Discriminative Learning via Dynamic Cluster Memory* (CVPR 2024, DOI `10.1109/CVPR52733.2024.02476`) explicitly expands cluster memory when incoming knowledge is novel and prunes overlapping clusters to keep a fixed memory capacity while retaining diversity.

**Reduction impact:** if a future supported SparkBrain use case actually requires continual acquisition beyond Assembly capacity, `decay/prune/merge/replace under a matched fixed memory budget` is an ordinary baseline. Merely adding mature-candidate turnover would be engineering/lifecycle design, not computational-principle novelty. The current static terminal should remain closed rather than be rescued with a post-outcome saturation experiment.

### 2. Stability–plasticity and category recruitment already have a mature ordinary mechanism family

Adaptive Resonance Theory and related recurrent category-learning models were designed around the stability–plasticity problem: preserve learned categories while admitting new ones. Layher et al., *Adaptive learning in a compartmental model of visual cortex—how feedback enables stable category learning and refinement* (Frontiers in Psychology 2014, DOI `10.3389/fpsyg.2014.01287`) uses learned bottom-up/top-down category representations; a sufficiently large mismatch triggers recruitment of new representational resources and creation/refinement of categories. ART literature likewise uses mismatch-triggered reset/search for a better existing or novel category.

**Reduction impact:** a future claim that SparkBrain stably accumulates new Assembly categories while preserving old ones must beat ordinary match/reset/recruitment or bounded-prototype mechanisms under matched memory/resources. The interesting quantity is the prospective retention–adaptation trade-off under an explicit resource policy, not category persistence alone.

### 3. Pattern completion/regeneration requires a causal feedback/recurrent path; a post-field Assembly readout is not an associative-completion mechanism

Le Duigou et al., *Recurrent synapses and circuits in the CA3 region of the hippocampus: an associative network* (Frontiers in Cellular Neuroscience 2014, DOI `10.3389/fncel.2013.00262`) reviews sparse recurrent CA3 connectivity as the substrate for associative representations and recall of ensemble patterns from partial cues. Layher et al. likewise realizes associative/category effects through learned feedforward and feedback interactions, with top-down feedback modulating earlier representations.

**Reduction impact:** the rejected current-v0.5 Assembly-feedback candidate is consistent with a straightforward architectural distinction: recognition after lower-field computation is a readout, whereas pattern completion/regeneration requires a causal recurrent/top-down route (or an explicitly equivalent mechanism). Any future positive Assembly-completion claim must be a fresh prospective architecture/mechanism object with such a causal path; it cannot reinterpret the current negative Discovery.

### 4. Biological engram/assembly persistence does not imply permanent mature entries

Ryan & Frankland, *Forgetting as a form of adaptive engram cell plasticity* (Nature Reviews Neuroscience 2022, DOI `10.1038/s41583-021-00548-3`) frames natural forgetting as circuit remodeling that can move engram cells between accessible and inaccessible states, with forgetting rates sensitive to environmental conditions.

**Reduction impact:** a biological “cell assembly” analogy cannot justify `mature == permanent`. Both persistence and adaptive loss/remodeling are established biological possibilities. SparkBrain therefore needs an explicit computational lifecycle contract—lifetime store, bounded working set, decay, consolidation, replacement, or another policy—before mature-candidate persistence can carry scientific interpretation.

## Synthesis

The new literature strengthens the current Funnel v2.1 disposition rather than opening a successor. `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` has useful SYSTEM information, but the literature supplies several ordinary solutions if continual bounded acquisition ever becomes a supported requirement. `CAND-V05-ASSEMBLY-FEEDBACK-CAUSALITY-01` should remain rejected for the current architecture because the causal route required for completion/regeneration is absent in the bounded matched probe and source ordering.

A future fresh Assembly object should first prospectively bind: (1) supported learning horizon and whether saturation is reachable/relevant, (2) memory-resource budget, (3) retention versus adaptation objective, (4) lifecycle policy for mature versus immature prototypes, and, for pattern-completion claims, (5) an actual causal feedback/recurrent route. None of these should be retrofitted into the completed objects.

## Machine-usable handoff

```yaml
schema_version: 2
generation_id: LIT-20260920T123000+0900-R11-ASSEMBLY-LIFECYCLE-7E4A1C2B
produced_at: 2026-09-20T12:30:00+09:00
producer_run_id: external-literature-auto-20260920T123000+0900-R11-7E4A1C2B
authority_scope: EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF
supersedes_generation_id: LEGACY_GENERATION_UNKNOWN
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_ASSEMBLY_MATURE_CAPACITY_LIFECYCLE_01
  - CAND_V05_ASSEMBLY_FEEDBACK_CAUSALITY_01
  - V05_ASSEMBLY_MEMORY_LIFECYCLE
  - FUTURE_ASSEMBLY_PATTERN_COMPLETION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_LIFECYCLE_AND_ASSOCIATIVE_MEMORY_REDUCTION. Bounded streaming
  prototype memory already uses decay/pruning/merge or fixed-capacity memory
  management; stability-plasticity/category recruitment is an established
  mechanism family; and associative pattern completion requires a causal
  recurrent/feedback path. The completed Assembly lifecycle object remains
  SYSTEM/HOLD and the current-v0.5 Assembly-feedback mechanism remains REJECTED.
audit_classification: null
prospective_baselines_or_discriminators:
  - DenStream/DCM-style bounded prototype memory with decay/pruning/merge/replacement under matched memory budget
  - ART-style match/reset/category recruitment under matched similarity and resource constraints
  - prospectively fixed retention-versus-adaptation/load curve only for a genuinely fresh supported saturation object
  - explicit recurrent/top-down causal-feedback comparator for any future Assembly completion/regeneration claim
questions_for_evidence_analyst:
  - Keep the lifecycle object terminal SYSTEM/HOLD and prohibit same-object saturation/turnover rescue?
  - If supported saturation later becomes independently relevant, require matched bounded-memory lifecycle baselines and a prospectively fixed retention/adaptation objective?
  - Preserve current-v0.5 Assembly-feedback REJECT; require a fresh causal feedback path before any future completion/regeneration mechanism claim?
questions_for_control_brain:
  - Add bounded prototype lifecycle, stability-plasticity/category recruitment, and explicit feedback-path requirements to the ordinary Assembly reduction ladder?
  - Keep MAIN idle rather than create a literature-driven successor while no supported saturation/feedback object exists?
  - Keep PRE_FORMAL/FORMAL empty until a native positive mechanism survives these ordinary reductions under matched resources?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01 contract/raw/terminal and no same-object saturation or turnover experiment
  - CAND-V05-ASSEMBLY-FEEDBACK-CAUSALITY-01 negative Discovery result and no cycle-2 rescue
  - no official TEST, fresh FORMAL identity/STARTED, rescore, retune, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created: null
```

No Utility request was created. The obvious implementation ideas (saturation/turnover comparators or adding Assembly feedback) are explicitly outside the completed-object authority and would be outcome-responsive rescue if launched now.