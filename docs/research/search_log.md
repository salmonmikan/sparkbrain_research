# C09 Search Log

## Scope and status

- **Initial discovery pass:** 2026-08-23
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

## Verification locations

The initial pass verified the cited publication record at these source types:

- publisher DOI or proceedings page: PA-001, PA-002, PA-006, PA-007, PA-009, PA-013;
- PubMed or PMC primary-record page: PA-003, PA-004, PA-005, PA-010, PA-011, PA-012;
- ACL Anthology primary proceedings page: PA-014;
- first-party research page, explicitly marked unreviewed: PA-015.

The exact source URL and persistent identifier are recorded in `literature_matrix.csv`. Code availability and license are deliberately marked `not checked` unless an official repository and its license file have been separately reviewed.

## Required second pass

The following searches are required before any novelty wording is strengthened. Record the database, exact query, retrieval date, included/excluded items, and the reason for exclusion.

| Database or proceedings index | Required focus | Reason |
|---|---|---|
| Google Scholar | backward and forward citation chaining from PA-001, PA-005, PA-007, PA-009, and PA-013 | find nearer duplicates and later implementations |
| OpenReview / ICLR proceedings | RIMs and shared-workspace descendants | distinguish final papers, preprints, and implementations |
| ACL Anthology | belief revision, nonmonotonic reasoning, contradiction handling, and sequential evidence | avoid treating Belief-R as the only relevant benchmark |
| PubMed / Crossref | GNW, DFT, ART, predictive coding, and spiking systems | identify primary scientific sources rather than only reviews |
| IEEE Xplore / ACM Digital Library | event-driven sparse graph execution and neuromorphic cognitive systems | challenge the execution-sparsity claim |
| official repositories | source code and license for reproducible precedents | satisfy C09 implementation and license notes without guessing |

## Interpretation rules

1. `not retrieved` and `retrieved but inaccessible` are distinct states and neither proves novelty.
2. A mechanism-level overlap may invalidate a proposed mechanism claim even when the benchmark or implementation differs.
3. An evaluation precedent does not establish an architecture duplicate, but it prevents benchmark novelty claims.
4. An implementation or first-party report is not a substitute for a peer-reviewed scientific result; publication status remains explicit.
5. The strongest counterexample should control the public framing. The absence of a complete end-to-end duplicate is not evidence that the integration is novel.
