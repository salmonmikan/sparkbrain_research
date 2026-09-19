# SparkBrain Literature Reduction Scout — 2026-09-20 03:30 JST

## Role

`LITERATURE_REDUCTION_SCOUT`

## Repository and control-plane state

Repository state was independently re-fetched before consuming the designated control-plane mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five authoritative `evidence/*` tags remain and no tag-based `formal/*`, `sealed/*`, or `freeze/*` state was observed. The current lower-funnel object is `CAND-V05-TOPOLOGY-CONFIG-BINDING-01` on `research/main-v05-topology-config-contract-arch-study-20260920@4a15a91edb8e92b89cda960f533590f7b46a70f2` under Evidence Analyst authority `9bb852bc1461755814d6a9a0e7ea561f1858a0da`.

The designated Control Brain, Evidence Analyst, MAIN, SUB, and role-suffixed report histories were read only from their mailbox paths; no `ops/*` branch was treated as a repository snapshot. Prior role-specific Literature state through 00:30 JST was read before searching, so the earlier temporal non-anticipation/event-time, Top-k, reservoir, causal-credit, provenance, eligibility, WTA, graph-rewrite, and other already-covered reductions are not recycled here.

A fresh read-only collection of exact-head workflow `35460876580` shows it completed successfully after the pre-diagnostic lint-only repair. Artifact `10589564435` (`sha256:e73909be3e647566540a06a4da94829b4737c3de3a24c5e0e54c697245be1970`) is bound to exact head `4a15a91edb8e92b89cda960f533590f7b46a70f2`. Its immutable run artifact maps the already-fixed cycle-1 contract to `SILENT_DECLARED_REALIZED_GEOMETRY_DIVERGENCE`: all five prospectively fixed configurations are accepted with zero construction errors/warnings; all share one realized topology signature; no explicit supported fixed-topology contract is found; and checkpoint round-trip preserves both the varying declared config values and the identical realized topology. This remains NON_EVIDENTIARY Architecture information and must stop for fresh Evidence Analyst review; this scout does not relabel or extend the object.

Current source independently explains the result. `V05BrainConfig` exposes `width`, `height`, and `receptor_rows`, copies them into the nested `V04BrainConfig`, and serializes them in `state_dict()`, but `IntegratedV05Brain` supplies `IntegratedV04Brain` an explicit `layered_reservoir_topology(seed=...)` without forwarding those fields. The topology constructor defaults to 16 receptors and an 8x6 reservoir. `load_checkpoint()` reconstructs the declared v0.5 config and then restores the saved v0.4 field, so a checkpoint can faithfully preserve both a non-default declared geometry tuple and the same fixed realized field.

## Genuinely new external literature findings

### 1. The five-config collapse is an ordinary inactive-configuration / observational-equivalence phenomenon, not architecture novelty

Reisner et al. (ICSE 2010, DOI `10.1145/1806799.1806864`) used symbolic evaluation to ask how run-time configuration options affect program behavior and found that apparently huge configuration spaces often collapse into much smaller groups of behaviorally equivalent configurations. That is a very direct ordinary reference for the current v0.5 object: the five prospectively factorized values differ at the declared interface but collapse to one realized topology signature on the current construction path.

A useful cross-domain analogy comes from structural identifiability. Raue et al. (Bioinformatics 2009, DOI `10.1093/bioinformatics/btp358`) and later identifiability literature formalize the problem of parameters that cannot be uniquely recovered from observed behavior; a particularly strong failure is when parameter variation leaves the relevant model output unchanged. Direct mathematical equivalence is not claimed here, but the diagnostic principle transfers cleanly: before treating `width`, `height`, or `receptor_rows` as operative scientific parameters, demonstrate a prospectively specified causal effect on the realized topology or an explicitly declared compatibility-only semantics.

**Reduction impact:** under the current integrated path, these fields are best treated as non-operative/inactive with respect to topology construction. The Architecture value is API truthfulness and reproducibility, not a new computational mechanism.

### 2. Silent acceptance of non-operative configuration has strong prior art as a configuration vulnerability / contract failure

Xu et al., *Do Not Blame Users for Misconfigurations* (SOSP 2013, DOI `10.1145/2517349.2522727`), treat configuration as a first-class interface problem and show that bad reactions to configuration errors include silent failures. Their Spex work infers configuration constraints from source and found hundreds of misconfiguration vulnerabilities and error-prone constraints across real systems. The broader configuration-error literature likewise emphasizes validating parameter values/relationships before they silently create incorrect behavior.

The current v0.5 result is narrower than a production outage, but the structural pattern is ordinary: exported dimension-like parameters are accepted and persisted, while the current runtime construction path ignores them and emits no warning. The clean prospective alternatives are therefore engineering semantics: either (a) explicitly declare the fields compatibility metadata/non-operative for v0.5, (b) reject unsupported non-default values, or (c) in a fresh implementation decision, bind them to the topology constructor. Which option is correct is a product/API decision, not something this outcome can choose retrospectively.

**Reduction impact:** `SILENT_DECLARED_REALIZED_GEOMETRY_DIVERGENCE` should remain an Architecture/configuration-contract finding. It is strongly subsumed by ordinary configuration-validation and interface-design concerns.

### 3. The current factorized matrix is already close to the right ordinary configuration-testing methodology; expanding the same object would add little

Configurable-software research has long treated option effects and interactions as a testing problem. Reisner et al. directly map option values to behavior; GenTree (ICSE 2021) learns logical interactions between configuration settings and program behavior; constrained covering-array work such as AutoCCAG (ICSE 2021, DOI `10.1109/ICSE43902.2021.00030`) exists because exhaustive configuration testing is usually infeasible and interaction coverage is the standard alternative.

For the present object, the prospectively fixed baseline plus width-only, height-only, receptor-only, and combined configurations already separates first-order field effects and one combined interaction. Because all five configurations map to exactly one topology signature and the source path shows why, a same-object combinatorial expansion would mostly re-measure an already-localized wiring omission. If a future version intentionally makes these fields operative, interaction testing becomes useful again and should be a fresh prospective correctness object.

**Reduction impact:** no cycle-2 rescue or broader fuzzing is justified from this result. The next decision is semantic ownership/validation, not more measurements on the unchanged constructor.

### 4. Checkpoint reproducibility requires configuration metadata to describe the operative experiment, not merely be serialized

Pineau et al. (JMLR 2021) frame reproducibility as obtaining comparable results from the same code/data and emphasize robust experimental workflows and complete reporting. A 2026 empirical study of 444 ML repositories by Foalem et al. (`arXiv:2603.23769`) reports that practitioners view missing hyperparameter logging and context-poor logging as materially harmful to reproducibility and trustworthiness.

Those papers do not directly study SparkBrain's exact failure mode, so the following is an inference rather than an external fact: faithfully serializing a declared configuration is insufficient when the declared parameter does not govern the realized object. In the current checkpoint path, different declared geometry tuples survive round-trip while the same realized topology survives too. That creates a provenance ambiguity unless the checkpoint schema or documentation makes the compatibility-only semantics explicit or records/validates the realized topology contract.

**Reduction impact:** this strengthens the Architecture/reproducibility interpretation, but does not support PRE_FORMAL or FORMAL promotion. Any schema/versioning or validation change is a separate fresh engineering decision.

## Inference for SparkBrain

The exact-head Architecture result is useful and should be retained exactly as produced, but the literature sharply limits its scientific meaning. The current line is best summarized as:

`public geometry-like config -> accepted + checkpoint-persisted -> explicit fixed layered topology constructor bypasses those fields -> multiple declared configs collapse to one realized topology -> checkpoint round-trip preserves the declared/realized mismatch`

That chain is well explained by ordinary configurable-software semantics, validation, and reproducibility concerns. It is not evidence for a new cognitive or dynamical mechanism.

The highest-value next step is fresh Evidence Analyst interpretation of the completed terminal Architecture artifact. Do not extend the same object to additional configs, implement a fix, or infer the intended geometry formula from the observed mismatch. No Utility request is created because the fixed cycle has already produced its terminal diagnostic and the contract explicitly requires fresh Analyst review before any successor; an extra request now would be outcome-responsive duplication.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_TOPOLOGY_CONFIG_BINDING_01
  - V05_CONFIGURATION_SEMANTICS
  - CHECKPOINT_REPRODUCIBILITY
  - ARCHITECTURE_API_CORRECTNESS
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_ARCHITECTURE_REDUCTION.
  The completed silent declared/realized geometry divergence is naturally
  explained by inactive configuration parameters, configuration-contract
  validation failures, and reproducibility/provenance semantics. The result is
  valuable Architecture/API correctness information but supplies no mechanistic
  or computational-principle novelty.
audit_classification: null
prospective_baselines_or_discriminators:
  - configuration-option liveness/effect mapping from declared field to realized topology
  - explicit constraint/validation contract for supported versus compatibility-only values
  - configuration-equivalence classes based on realized topology signatures
  - fresh t-wise/interaction testing only after fields become intentionally operative
  - checkpoint schema/provenance check that declared config and realized topology semantics agree
questions_for_evidence_analyst:
  - Accept the exact-head terminal Architecture label SILENT_DECLARED_REALIZED_GEOMETRY_DIVERGENCE and stop the current object for semantic/engineering review?
  - Treat width/height/receptor_rows as currently non-operative for topology construction unless an explicit supported contract says otherwise?
  - Require any future implementation object to prospectively choose one semantic policy: operative binding, explicit rejection, or documented compatibility metadata, rather than infer the answer from this result?
questions_for_control_brain:
  - Keep this line at Architecture/API correctness and out of PRE_FORMAL/FORMAL novelty accounting?
  - Add configuration-option liveness plus declared-versus-realized checkpoint consistency to the ordinary architecture reduction/reproducibility checklist?
  - Avoid a same-object cycle 2 or broad config fuzzing because source localization plus the fixed five-config result already resolves the current question?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - all canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - CAND-V05-TOPOLOGY-CONFIG-BINDING-01 prospective cycle-1 contract, exact research head, raw artifact, mapped outcome and stop boundary
  - no outcome-responsive implementation fix, cycle 2, extra configuration search, PRE_FORMAL or FORMAL promotion before fresh review
  - completed Temporal and Top-k current-object HOLD boundaries and rejected Assembly/Structural current questions
  - no official TEST, new formal identity/STARTED, rescore, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created: null
```

## Sources

- Reisner, Song, Ma, Foster & Porter, *Using Symbolic Evaluation to Understand Behavior in Configurable Software Systems*, ICSE 2010, DOI `10.1145/1806799.1806864`.
- Raue et al., *Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood*, Bioinformatics 25(15), 2009, DOI `10.1093/bioinformatics/btp358`.
- Xu et al., *Do Not Blame Users for Misconfigurations*, SOSP 2013, DOI `10.1145/2517349.2522727`.
- Nguyen & Nguyen, *GenTree: Using Decision Trees to Learn Interactions for Configurable Software*, ICSE 2021.
- Luo et al., *AutoCCAG: An Automated Approach to Constrained Covering Array Generation*, ICSE 2021, DOI `10.1109/ICSE43902.2021.00030`.
- Pineau et al., *Improving Reproducibility in Machine Learning Research*, JMLR 22(164), 2021.
- Foalem et al., *Empirical Characterization of Logging Smells in Machine Learning Code*, arXiv:2603.23769, 2026 (preprint).
