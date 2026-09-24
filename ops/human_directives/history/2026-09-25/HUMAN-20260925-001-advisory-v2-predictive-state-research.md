# HUMAN-20260925-001 — Advisory v2: learned predictive-state organization under matched constraints

Human status: `OPEN`  
Created: `2026-09-25 JST`  
Operation: `ADD`  
Origin: user-requested, assistant-researched follow-up to HUMAN-20260924-009  
Proposal status: `RESEARCH_PROPOSAL_NOT_EXPERIMENTALLY_VALIDATED`  
Scientific credit: `0`  
Execution authority: `NONE`

## Human intent and attribution

The user requested continuation of the general investigation, use of external literature, adjustment of the failed advisory into a better new advisory, and registration in the normal Human Directive channel. The user's correction was that the requested adjustment concerns the advisory (進言), not scheduler configuration.

The scientific analysis, candidate direction and proposed tests below were developed by the assistant for review. They are NOT scientific conclusions independently verified or endorsed by the human. Permission to record this proposal is not Control acceptance or experiment authority.

Japanese summary: 旧進言の棄却理由を保存したうえで、問いを「匿名な記憶を書き換えられるか」から「連続経験の矛盾を、既存記憶の更新・別状態への分離・過去状態の再利用としてどう学び分けるか」へ絞る。同じ入力情報・学習条件・記憶量・計算量で既知手法と比較する。普遍的な新計算原理を先に要求せず、限定した学習上の差、機構上の差、システム上の価値を分けて検証する。

HUMAN-20260924-009 and all old scientific/Forge results remain unchanged. This is a new follow-up proposal, not withdrawal of the old routing request, not a reopening of TH-002, and not an assertion of an independent rediscovery unaffected by prior outcomes.

## 1. What was actually checked

### Repository observations

The following were re-fetched through the GitHub connector on 2026-09-25 JST:

| Source | Observed content | Scope limit |
|---|---|---|
| Evidence Analyst latest R130, generation EVA-20260925T005800+0900-R130-LIT44-REDUCTION-LADDER-NO-SCIENCE, blob 3817561ee03ee6f519e6bdd07ffefeb5ca3ffa29 | Reports 35 canonical objects, all terminal, no active/queued canonical object; H7 remains consumed INCONCLUSIVE; TH-002 remains rejected after Forge | Current programme summary, not a new audit of every raw experiment |
| Analyst state R129, blob 86b48f9868695f9c7f3c6b70eb00408d70438575; historical R128 at 876e208cc2fbfccd013156282162745b0e724408 | Preserves H7, #34/#35 boundaries and Theory/Revisit dispositions | latest.md and state.json have different generations; do not pretend they are one atomic snapshot |
| forge/TH002-FORGE-001.md at 7db8abb08e7862e3bb98c985f2e7ec4d81cd9d16, blob e4c3639e2c01898cb9ed140e47aefa11f1656e8b | Exact three-key static associative-memory reduction; noncanonical and zero-credit | Not a general impossibility theorem about all learned state organization |
| Historical R128 state at the above commit | Gate basis is static algebraic matched-access equivalence; CI failed at lint and runtime tests were skipped | Do not call this a completed dynamic performance experiment |
| Methodology R119, generated 2026-09-25 01:19:59 JST, blob c99a73b03b361ebb05569de5201d01b6fbb10e9c | Requires the strengthened reduction ladder to be staged and claim-matched; READY/PRE_FORMAL must not require defeating every advanced comparator before development | A methodology recommendation, not a changed historical scientific result |
| src/sparkbrain/v05/assemblies.py at main d16403414fc7abebd23075fc401240971b8eb91d, blob a0a8c41e21db68cafc08ace8dac50b7a56607a52 | Hand-specified similarity, prototype search, explicit allocation, episode-dependent maturation and snapshots | Stable reusable implementation, not evidence of fully endogenous boundary-free state formation |
| Human Directive README, active file and HUMAN-009 history | Human-originated proposals require independent Control review | This write must remain on ops/human-directives |

The v0.5 similarity is 0.55 edit similarity + 0.25 Jaccard + 0.20 timing similarity. Its observe method requires episode_id and counts distinct episodes for maturation. These are concrete features of that inspected implementation, not accusations that its original bounded claims are invalid. Any future boundary-free claim must audit those signals and distinguish internal bookkeeping IDs from externally supplied privileged labels.

The current population was reviewed through its summaries and critical artifacts. This investigation did NOT re-audit all 35 objects' raw evidence, rerun old experiments, benchmark the external baselines, or prove novelty. Detailed closure-map coverage remains an explicit downstream deliverable rather than an accomplished fact.

### Pinning references

- https://github.com/salmonmikan/sparkbrain_research/blob/7db8abb08e7862e3bb98c985f2e7ec4d81cd9d16/forge/TH002-FORGE-001.md
- https://github.com/salmonmikan/sparkbrain_research/commit/7db8abb08e7862e3bb98c985f2e7ec4d81cd9d16
- https://github.com/salmonmikan/sparkbrain_research/blob/876e208cc2fbfccd013156282162745b0e724408/analysis/orchestrator/state.json
- https://github.com/salmonmikan/sparkbrain_research/blob/d16403414fc7abebd23075fc401240971b8eb91d/src/sparkbrain/v05/assemblies.py
- Moving Analyst/Methodology paths above must be re-fetched by the consuming worker; the quoted generation and blob identify what this advisory actually inspected.

## 2. Correct the earlier framing before proposing another theory

### 2.1 Preserve TH-002's actual rejection, without overgeneralizing it

Its construction uses three pairwise-orthogonal signatures k_i of squared norm four, M = sum_i(v_i k_i/4), query q = k_j, readout q dot M and update M' = M + delta q/4. Consequently q dot M = v_j, and a matched-access key-value memory reproduces its selective update. This is a valid static reduction of that construction. It does not establish that every possible learning process, streaming state-formation rule or finite-budget implementation has been evaluated.

No resurrection, dynamic extension, re-scoring or correction of the old TH-002 identity is proposed. The comparator/access amendment and the absence of completed runtime validation must remain visible in its historical interpretation. Any future object starts with a new prospective contract.

### 2.2 Replace universal non-reducibility with claim-specific tests

An implementation with B bits of complete persistent state has at most 2^B configurations and can in principle be represented as a finite-state system. That observation alone does not establish equal learning cost, transition complexity, memory footprint, resource use or intervention structure. Conversely, renaming an ordinary update rule does not create a new mechanism.

Distinguish:

- exact same update/learning mechanism under an admissible mapping and matched assumptions;
- a generic simulator with an unspecified or much larger resource cost;
- equal accuracy on one narrow test;
- a different learning rule with a measured finite-budget trade-off;
- a mechanistic causal difference demonstrated by a valid intervention.

Only the first directly establishes the claimed exact reduction. The other cases require narrower conclusions. Count actual stored bits/bytes and transition computation; an exponential number of possible FSA states is not by itself an exponential lower bound on memory, because the current-state index needs only logarithmically many bits and transitions may be factored.

These are reasoning constraints for designing the new study, not experimental findings.

### 2.3 Do not remove all information merely to defeat associative memory

If k balanced hidden targets induce exactly the same distribution of the COMPLETE allowed observation/action history and late cue, no predictor using only that information can identify the target with probability above 1/k. Recurrent state cannot recover a distinction absent from its inputs.

Therefore remove oracle IDs, supplied episode boundaries and privileged retrieval targets where the claim requires it, but retain learnable statistical or interaction-derived evidence equally available to every model. Distinguish an explicit answer key from legitimate sensory evidence. Ambiguous periods should be assessed with predictive probabilities, not demands for an unknowable unique answer.

### 2.4 Learning from failure is not rewriting failure

Hypotheses may legitimately be motivated by old failures, literature and observed implementation limitations. Disclose that origin. Do not relabel exploratory evidence as independent confirmation, revise a frozen result, or reuse a consumed one-way identity. New claims require fresh prospective tests and the normal gate [S13].

This proposal is advisory-exposed and outcome-informed. It is not itself an independent Revisit trigger. Control/Analyst should explicitly distinguish transparent fresh hypothesis generation from same-object rescue. A calendar delay or a new name provides no protection by itself.

### 2.5 Avoid a second FORMAL gate before development

Methodology R119 independently identifies this risk. Use the closest adequate comparators first, add further comparators when the claim actually implicates them, and retain genuine exploratory development. Do not require a proposal to defeat every FSA/RNN/Bayesian/associative model before it can be investigated. Do not weaken the eventual relevant comparison merely to produce a positive result.

## 3. External literature: what is already occupied territory

Primary publications, author abstracts and official publication records were inspected. The table states the retrieval level; a bibliography entry is not a claim that its code was reproduced. Publication facts and authors' results are separate from the proposed SparkBrain inference.

| Ref | Prior result relevant here | Consequence for the revised proposal | Read level |
|---|---|---|---|
| S1 | Fast-weight programmers formally connect linear attention with associative memory; keys/values and correction rates can themselves be learned | Self-created keys and selective key-value correction are not sufficient novelty claims | Official proceedings abstract |
| S2 | Gated Delta Networks combine recurrent forgetting with targeted delta-rule modification | Fixed recurrent state and selective updates need a learned-key recurrent comparator | Official author-lab publication/abstract |
| S3 | HRR binds and superposes distributed vectors with approximate retrieval and cleanup | Distributed/fixed-width representation alone is not novelty; capacity/noise/cleanup must be counted | Original article abstract |
| S4 | Latent-cause inference decides whether experience updates an existing memory or forms another | The central update-versus-separate question is already known; compare algorithms, not just the question's wording | Full eLife HTML, including model equations and assumptions |
| S5 | Structured Event Memory infers event boundaries and schemas with probabilistic dynamics over structured scenes | Endogenous segmentation is not a blank field; preserve its input assumptions when adapting it | Author-institution publication record and abstract |
| S6 | ART2 studies stable category formation from analog input | Stability/plasticity and mismatch-triggered category creation are established precedents | Original article abstract |
| S7 | Slot Attention learns object-specializing exchangeable slots | Unsupervised grouping is not automatically new; slots/attention/encoder costs and assumptions matter | Original proceedings abstract |
| S8 | Bayesian online change-point detection tracks uncertainty over run length | Useful closest boundary detector; its basic formulation is not automatically a returning-context memory model | Original preprint abstract |
| S9 | Predictive-state representations organize history through action-conditioned future predictions | Predictive state itself is established; characterize learning and causal/operational differences | Original proceedings record |
| S10 | Computational mechanics studies minimal predictive state organization under stated assumptions | Predictive causal states must not be confused with intervention-identified causes | Author publication record |
| S11 | Causal abstraction uses aligned variables and interchange interventions | Decodability or arbitrary lesion effects alone do not establish the proposed functional mechanism | Original paper abstract |
| S12 | e-prop provides online learning in recurrent spiking networks with local eligibility and learning signals | Local spikes and eligibility are comparator ingredients, not unique mechanisms | Original Nature Communications article |
| S13 | Preregistration separates hypothesis generation from testing with new data | Permit transparent fresh hypotheses without altering past results | Original article/search-accessible text |
| S14 | Unsupervised disentanglement needs appropriate inductive assumptions under the paper's setting | Declare biases rather than claim structure appears without assumptions | Official ICML proceedings abstract |

A current additional lead, S15 (Kalman Delta Networks, September 2026 preprint), was found at the author-abstract/search level. It concerns uncertainty-aware associative update. The full paper/implementation was not accessible in this pass; its exact assumptions and implementation remain to be checked before making it a mandatory comparator. The plan does not depend on S15 being the newest or strongest model.

No source above proves that SparkBrain wins or loses the newly proposed task. No universal absence-of-prior-art claim is made. MHT/data association and dynamic neural fields remain relevant expansion checks if the selected concrete mechanism requires them; they are not added as universal mandatory hurdles.

## 4. Revised direction: a bounded learning question, not a claimed new grand theory

Working description, NOT a candidate ID:

> Can a local, persistent predictive system learn when to update an existing internal model, maintain a separate model, or reuse a previous one from a continuous interaction stream, with no supplied regime/episode identities, and produce an informative error/interference/resource trade-off against the closest matched alternatives?

The proposed mechanistic variable is how prediction mismatch is assigned to updates of existing state versus retention/differentiation of competing state. The new study must specify a concrete update rule and its distinctive intervention prediction before claiming mechanistic novelty. If it is simply latent-cause inference, ART reset or gated associative memory implemented under a new name, report that reduction. A useful bounded SYSTEM implementation may still be worth studying, but must not be upgraded to MECHANISM novelty after seeing success.

Initial claim type is for Analyst to choose prospectively. Do not announce a new computational principle, concepts, consciousness, self-organized cognition or universal superiority. Avoid treating every known component as worthless: the question is which learning operation contributes under declared constraints.

## 5. Proposed investigation sequence and deliverables

This section is a plan for independent review. None of these new experiments was executed as part of recording the directive.

### Gate A — bounded closure/claim map

Use the 35-object inventory plus Theory/Forge history to make a compact map: original question, stage, original source, observation, rejection reason, exact scope, confound/capacity status, remaining question, and candidate-specific comparison surface. Separate formal negative, inconclusive, static equivalence, engineering failure, weak assay and untested idea.

Start with the critical sources already identified rather than rereading everything every run. Track explicit verified/missing coverage. Do not turn the reported 35/35 terminal census into a claim that 35 universal mechanisms were disproved. Search later research branches for the selected question before asserting it is untested.

Deliverable: one bounded claim/closure map and a decision whether there is a distinct study worth preparing. A conclusion of no useful new study is allowed.

### Gate B — establish an identifiable, informative testbed first

Design fresh development-only continuous streams with three contrasts:

1. Appearance/sensor changes while predictive dynamics stay the same: avoid gratuitous fragmentation.
2. Predictive action-outcome dynamics change, with enough shared admissible evidence to identify the change: adapt without destructive overwriting of unrelated situations.
3. A previous dynamics regime returns after intervening experience: assess reuse/recovery rather than learning everything again.

Do not expose latent regime IDs, truth labels, evaluator target indices or human-declared episode changes to any learner. Internally allocated IDs and a declared common capacity prior are permitted bookkeeping, not automatic leakage. Audit boundary/episode/maturity signals in reused code; do not silently inherit them from v0.5.

Begin with the same fixed interaction stream for all methods to isolate state learning. Active action selection is a later, separately specified study with matched exploration budgets; do not confuse that comparison with one requiring identical trajectories.

Include a deliberately non-identifiable control where calibrated uncertainty is the expected result, and an easy cue-rich control where ordinary associative memory should work. Use new fixtures rather than replaying TH-002 or consumed research data. A privileged generative oracle may diagnose task solvability only if clearly separated from the fair model comparison.

Deliverable: input-access table, generative assumptions, prospective observable/readout contract, and an assay-validity check. No candidate superiority claim.

### Gate C — closest comparisons and resource accounting

Choose two or three relevant families, not every paper in the literature table:

- latent-cause inference or an explicitly specified change-point/mixture model that can reuse past regimes; label any extension beyond vanilla BOCPD;
- learned-key delta/gated-delta associative recurrence with comparable sensory encoding and training opportunity;
- a matched recurrent/field control retaining ordinary adaptation/plasticity/eligibility but lacking the particular proposed state-allocation operation.

Add ART, SEM, slots, predictive states or HRR only where the actual mechanism/claim makes them decisive. S15 is optional pending full validation. A fixed-key straw model must not be the sole learned-addressability comparator.

Account for model state, precision, keys, codebooks, cleanup memory, optimizer state, queues, clocks, encoders, pretraining, replay buffers, update operations and hyperparameter-search budgets. Report several predeclared feasible resource levels or an error-cost frontier rather than selecting the winning budget after outcomes. Wall-clock speed and biological energy are separate claims; do not infer them from operation counts alone.

Check comparator capacity and correct implementation on separate development controls before a frozen decisive comparison. Underpowered or broken controls yield an inconclusive comparison, not a SparkBrain win. Capacity adequacy must not become a requirement that a model already win the target test before it may enter development.

### Gate D — one concrete mechanism and an adversarial pilot

Only after the above is coherent, specify one fresh local update/allocation mechanism and its strongest ordinary mathematical equivalent. A natural provisional contrast is prediction-sensitive selective updating versus the same system without that operation, tested for retention, appropriate separation and return-regime recovery.

The rule itself is not fixed or validated by this document. If no meaningful distinction from the closest prior algorithm can be written down, do not manufacture one. Either reduce the claim to a useful implementation/system study or decline the mechanism proposal with a precise reason.

Primary evaluation should use observable prediction quality, such as a proper scoring rule over later outcomes, plus prospectively defined recovery/interference measures. Latent-state counts and alignment are diagnostics, not proof of cognition. Set numerical thresholds, seed partitions, equivalence margins and power requirements in fresh development before formal outcomes; none are invented here as already approved.

Interventions should distinguish blocking learning/allocation from merely damaging readout. Use matched controls and a reachable treatment-to-output path. Natural donor states or matched-state substitutions need compatibility checks: combining individually natural components can still create an unnatural hybrid. Do not pick favorable lesions using protected outcomes. Require the claimed selective effect and its uncertainty, not merely any behavioral degradation.

### Gate E — explicitly separate possible outcomes

| Outcome | Appropriate meaning |
|---|---|
| No usable information about the required distinction | Task is non-identifiable; not a negative about intelligence |
| Manipulation cannot affect the declared readout | Non-diagnostic assay; do not infer state irrelevance |
| Exact update/learning equivalence to an admissible ordinary model | Reduce that mechanism claim; preserve any separately justified engineering value |
| No meaningful benefit against adequate relevant controls | Negative for this fixed fresh hypothesis and scope |
| Missing capacity, runtime validation or precision | Inconclusive; neither success nor a universal failure |
| Reproducible finite-budget predictive/recovery benefit | Bounded SYSTEM/learning result under the chosen contract |
| In addition, a distinct rule with valid selective causal intervention | Candidate for a bounded mechanism claim, subject to Analyst and fresh confirmation |

The first pilot has no confirmatory credit. Interesting results go back through Analyst; any canonical/formal object receives a fresh identity and prospective contract. No automatic success-based upgrade of claim type.

## 6. Routing, integrity and completion conditions

Suggested routing for consideration: Human Directive -> independent Control review -> Analyst with Methodology R119 calibration -> bounded Theory/Forge or tooling allocation under existing authority -> fresh canonical MAIN allocation only if admitted.

Do not create another scheduler, change cadence, silently disable a worker, or rewrite another worker's prompt as part of this directive. No special Detective role exists or is requested. No Control disposition is written here.

Preserve HUMAN-009, TH-001/TH-002, A01 families, C19, H7, #34/#35, consumed identities, protected targets and all frozen evidence. Result-informed development must retain versioned provenance. A new explanatory draft is not independently confirming evidence or an automatic Revisit trigger. Current gates remain in force unless properly reviewed prospectively.

A useful downstream response is a concrete ACCEPT/MODIFY/DEFER/REJECT decision, an identified next bounded deliverable and owner when accepted, or the exact scientific reason the lead has no value. Success is not a mandated new theory, prototype count or revived-candidate quota. Avoid both repeated empty high-level restatements and a requirement for universal novelty before doing informative development.

## 7. Sources and retrieval limits

S1. Schlag, Irie & Schmidhuber (2021), Linear Transformers Are Secretly Fast Weight Programmers. ICML/PMLR 139. https://proceedings.mlr.press/v139/schlag21a.html

S2. Yang, Kautz & Hatamizadeh (2025), Gated Delta Networks: Improving Mamba2 with Delta Rule. ICLR; arXiv:2412.06464. Official author-lab page: https://research.nvidia.com/index.php/publication/2025-04_gated-delta-networks-improving-mamba2-delta-rule

S3. Plate (1995), Holographic Reduced Representations. IEEE Transactions on Neural Networks. DOI:10.1109/72.377968. https://pubmed.ncbi.nlm.nih.gov/18263348/

S4. Gershman, Monfils, Norman & Niv (2017), The computational nature of memory modification. eLife 6:e23763. https://elifesciences.org/articles/23763 (version-of-record page indicates a correction; this review uses its displayed model and does not adjudicate the correction independently).

S5. Franklin, Norman, Ranganath, Zacks & Gershman (2020), Structured Event Memory: A Neuro-Symbolic Model of Event Cognition. Psychological Review 127:327-361. DOI:10.1037/rev0000177. https://collaborate.princeton.edu/en/publications/structured-event-memory-a-neuro-symbolic-model-of-event-cognition/

S6. Carpenter & Grossberg (1987), ART 2: Self-organization of stable category recognition codes for analog input patterns. Applied Optics. DOI:10.1364/AO.26.004919. https://pubmed.ncbi.nlm.nih.gov/20523470/ (abstract was search-accessible; a later direct fetch encountered a browser challenge).

S7. Locatello et al. (2020), Object-Centric Learning with Slot Attention. NeurIPS. https://proceedings.neurips.cc/paper/2020/hash/8511df98c02ab60aea1b2356c013bc0f-Abstract.html

S8. Adams & MacKay (2007), Bayesian Online Changepoint Detection. Original preprint, arXiv:0710.3742. https://arxiv.org/abs/0710.3742

S9. Littman, Sutton & Singh (2001), Predictive Representations of State. NeurIPS proceedings. https://papers.nips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html . Related discovery work: James & Singh (2004), Learning and discovery of predictive state representations in dynamical systems with reset, DOI:10.1145/1015330.1015359. Its reset assumption must not be silently removed.

S10. Shalizi & Crutchfield (2001), Computational Mechanics: Pattern and Prediction, Structure and Simplicity. Journal of Statistical Physics. Author record: https://csc.ucdavis.edu/~cmg/compmech/pubs/cmppss.html

S11. Geiger, Lu, Icard & Potts (2021), Causal Abstractions of Neural Networks. NeurIPS. https://arxiv.org/abs/2106.02997

S12. Bellec et al. (2020), A solution to the learning dilemma for recurrent networks of spiking neurons. Nature Communications. https://www.nature.com/articles/s41467-020-17236-y

S13. Nosek, Ebersole, DeHaven & Mellor (2018), The preregistration revolution. PNAS. DOI:10.1073/pnas.1708274114. https://www.pnas.org/doi/10.1073/pnas.1708274114 (publisher direct access was intermittent/403; bibliographic and search-accessible text verified, not a code or replication audit).

S14. Locatello et al. (2019), Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations. ICML/PMLR 97. https://proceedings.mlr.press/v97/locatello19a.html

S15. Bui, Huang & Ying (2026), Kalman Delta Networks: Uncertainty-aware Associative Memory. arXiv:2609.07816, preprint submitted 2026-09-07. https://arxiv.org/abs/2609.07816 . Author abstract surfaced in search; direct full-page access failed in this pass. Treat as provisional literature lead pending full-method verification; no reported benchmark is adopted here.

## Required independent review

Control Brain may ACCEPT, MODIFY, DEFER or REJECT the proposal. In particular, challenge the chosen update/separate/reuse direction against S4/S5/S6 and the learned-key baselines before assigning it scientific novelty. The objective is a tractable, honest next investigation, not rescue of the old advisory. Record Control/Analyst decisions only in their own streams, never by rewriting this human-originated history.
