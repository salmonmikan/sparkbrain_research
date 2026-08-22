# C09 Search Log

## Scope and status

- **Initial discovery pass:** 2026-08-23
- **Adversarial second pass:** 2026-08-23
- **Reviewer:** Codex
- **Method:** web discovery followed by verification against publisher, proceedings, PubMed, PMC, ACL Anthology, OpenReview, or first-party research pages.
- **Purpose:** identify the strongest counterexamples to SparkBrain's proposed contribution candidates. This is not an exhaustive systematic review and does not support a universal novelty claim.
- **Inclusion rule:** a source must describe a concrete computational mechanism or a directly relevant evaluation task. Primary papers and official proceedings are preferred.
- **Exclusion rule:** blogs, search snippets, and citation counts are not decisive evidence. A source that was not retrieved is not evidence of absence.

## Query record

| Date | Discovery query | Target family | Verified matrix IDs | Result state |
|---|---|---|---|---|
| 2026-08-23 | `LIDA cognitive cycle attention codelets coalition Global Workspace primary paper` | LIDA / codelets / coalition / broadcast | PA-001 | reviewed |
| 2026-08-23 | `A neuronal model of a global workspace in effortful cognitive tasks` | Global neuronal workspace | PA-002 | reviewed |
| 2026-08-23 | `A Spiking Neuron Model of Cortical Broadcast and Competition` | Spiking global workspace | PA-003 | reviewed |
| 2026-08-23 | `Dynamic Field Theory local excitation inhibition persistent peak primary paper` | Dynamic field theory | PA-004 | reviewed |
| 2026-08-23 | `ART 2 self-organization stable category recognition primary paper` | Adaptive resonance and reset | PA-005 | reviewed |
| 2026-08-23 | `Recurrent Independent Mechanisms ICLR 2021` | Sparse modular recurrent learning | PA-006 | reviewed |
| 2026-08-23 | `Coordination Among Neural Modules Through a Shared Global Workspace ICLR 2022` | Shared global workspace | PA-007 | reviewed |
| 2026-08-23 | `Temporal Graph Networks Deep Learning on Dynamic Graphs` | Temporal event graphs | PA-008 | reviewed |
| 2026-08-23 | `Asynchronous Event-based Graph Neural Networks CVPR 2022` | True sparse event-routed graph execution | PA-009 | reviewed |
| 2026-08-23 | `A theory of cortical responses Friston 2005` | Predictive coding | PA-010 | reviewed |
| 2026-08-23 | `Brain computation by assemblies of neurons Assembly Calculus` | Cell assemblies | PA-011 | reviewed |
| 2026-08-23 | `A large-scale model of the functioning brain Spaun` | Spiking cognitive architecture | PA-012 | reviewed |
| 2026-08-23 | `abstract argumentation Dung 1995` | Nonmonotonic reasoning and contradiction graphs | PA-013 | reviewed |
| 2026-08-23 | `Belief Revision The Adaptability of Large Language Models Reasoning EMNLP 2024` | Belief-revision evaluation | PA-014 | reviewed |
| 2026-08-23 | `Verbalizable Representations Form a Global Workspace in Language Models` | Workspace-like organization in language models | PA-015 | reviewed; unreviewed source |
| 2026-08-23 | `HEARSAY-II speech understanding blackboard integrating knowledge uncertainty` | blackboard / competing hypotheses | PA-016 | reviewed |
| 2026-08-23 | `working memory attention salience active inference` | active inference / working memory | PA-017 | reviewed |
| 2026-08-23 | `probabilistic decision making slow reverberation cortical circuits` | attractor / probabilistic accumulation | PA-018 | reviewed |
| 2026-08-23 | `Rabiner hidden Markov models tutorial sequential inference` | probabilistic sequential inference | PA-019 | reviewed |
| 2026-08-23 | `event based asynchronous sparse convolutional networks ECCV` | asynchronous sparse execution | PA-020 | reviewed |
| 2026-08-23 | `bipolar argumentation support attack acceptability` | support / attack belief graphs | PA-021 | reviewed |
| 2026-08-23 | `dynamic neural fields cognitive neuromorphic architectures` | neuromorphic cognition | PA-022 | reviewed |
| 2026-08-23 | `sequential memory neuromorphic device dynamic neural fields` | neuromorphic sequential memory | PA-023 | reviewed |
| 2026-08-23 | `official repository license TGN AEGNN RIMs Belief-R` | code and license audit | PA-006, PA-008, PA-009, PA-014 | reviewed |

## Verification locations

The initial pass verified the cited publication record at these source types:

- publisher DOI or proceedings page: PA-001, PA-002, PA-006, PA-007, PA-009, PA-013;
- PubMed or PMC primary-record page: PA-003, PA-004, PA-005, PA-010, PA-011, PA-012;
- ACL Anthology primary proceedings page: PA-014;
- first-party research page, explicitly marked unreviewed: PA-015.

The exact source URL and persistent identifier are recorded in `literature_matrix.csv`. Code availability and license are deliberately marked `not checked` unless an official repository and its license file have been separately reviewed.

## Completed backward and forward chaining

| Seed | Direction | Included result | Why it challenges the claim |
|---|---|---|---|
| PA-001 LIDA | backward | PA-016 HEARSAY-II | older blackboard with asynchronous knowledge sources and alternative hypotheses |
| PA-007 Shared Workspace | backward | PA-006 RIMs | selective recurrent modules precede the shared-workspace integration |
| PA-009 AEGNN | backward | PA-020 asynchronous sparse convolution | event-triggered local sparse recomputation predates the graph formulation |
| PA-013 Dung | forward | PA-021 bipolar argumentation | explicit support as well as attack narrows any evidence-graph distinction |
| PA-004 DFT | forward | PA-022, PA-023 | cognitive neuromorphic and sequential-memory implementations narrow hardware claims |
| PA-002/PA-003 workspace | forward | PA-007, PA-015 | learned shared workspaces and LLM workspace-like representations narrow broad workspace claims |

This was bounded citation chaining through publisher records, paper bibliographies, first-party pages, and official repositories. Authenticated citation indexes were not available, so it is not an exhaustive citation-network census.

## Family and implementation coverage

| Family | Matrix evidence | Retrieval state |
|---|---|---|
| blackboard / cognitive architecture | PA-001, PA-016 | primary records reviewed |
| workspace / ignition / modular competition | PA-002, PA-003, PA-006, PA-007, PA-015 | primary or first-party records reviewed |
| attractor / active inference / sequential probabilistic inference | PA-017, PA-018, PA-019 | primary records reviewed |
| belief revision / support-attack argumentation | PA-013, PA-014, PA-021 | primary proceedings reviewed |
| asynchronous sparse event execution | PA-008, PA-009, PA-020 | primary proceedings and official repos reviewed |
| neuromorphic cognitive dynamics / memory | PA-012, PA-022, PA-023 | primary records reviewed |

Official code/license results: TGN is Apache-2.0; AEGNN is MIT; the inspected RIMs and Belief-R repositories have no repository license file, so reuse permission is not assumed. No official repository was identified for the 2026 workspace report or Shared Global Workspace during this pass.

## Residual uncertainty and exclusions

- Forward-citation coverage is incomplete without authenticated scholarly citation indexes.
- No retrieved work proves the exact end-to-end SparkBrain integration unique; equally, failure to retrieve one does not prove novelty.
- PA-015 is a first-party, unreviewed report. Its authors explicitly limit the analogy and do not claim a complete recurrent specialist-competition architecture.
- Hardware-energy claims remain outside C09: algorithmic sparsity and neuromorphic deployment do not establish lower energy without matched physical measurement.
- Search snippets, inaccessible secondary descriptions, and projects without a primary or official record were excluded from claim decisions.

## Interpretation rules

1. `not retrieved` and `retrieved but inaccessible` are distinct states and neither proves novelty.
2. A mechanism-level overlap may invalidate a proposed mechanism claim even when the benchmark or implementation differs.
3. An evaluation precedent does not establish an architecture duplicate, but it prevents benchmark novelty claims.
4. An implementation or first-party report is not a substitute for a peer-reviewed scientific result; publication status remains explicit.
5. The strongest counterexample should control the public framing. The absence of a complete end-to-end duplicate is not evidence that the integration is novel.
