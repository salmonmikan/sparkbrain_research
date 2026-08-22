# Prior Art and Research Gap Analysis

## 1. Executive conclusion

SparkBrain の基本思想を構成する部品の大半は既知である。

- 多数の局所処理が並列に走る
- activation、decay、threshold
- winner-take-all / soft competition
- 一時的 coalition
- global broadcast / workspace
- persistent activity / attractor
- sparse specialist modules
- prediction error
- spiking / event-driven execution
- Hebbian / reward-modulated learning

したがって、**「小さな発火が競争して閾値を超える」という説明だけでは新理論にならない。**

現時点の差分候補は、以下を現代的な学習可能アーキテクチャとして一体化し、同一条件下で反証可能にすることにある。

> 明示的で持続する複数belief、evidence identityを持つCoalition、敗者の復帰、Coalition-level ignition、no-ignition、真のevent-routed execution sparsity、学習可能routing、内部可視化

ただし、これは「完全一致する先行研究をまだ確認できていない」という状態であり、新規性が証明された状態ではない。

## 2. Mapping matrix

| SparkBrain element | Closest prior art | Overlap | Remaining difference candidate | Assessment |
|---|---|---|---|---|
| Spark as small local process | LIDA codelets; neural units | 小処理が独立・並列に働く | Sparkをpersistent semantic belief stateとして統一 | 基礎は既知 |
| activation / decay / threshold | LIDA, DFT, attractor networks, SNN | 活動値、減衰、閾値、持続peak | evidence provenanceとbelief revision指標への接続 | 基礎は既知 |
| soft winner-take-most | WTA, lateral inhibition, DFT | 局所興奮・周辺抑制、競争 | loser recoveryを主要設計目的・評価対象にする | 組合せ差分候補 |
| temporary coalition | LIDA | attention codeletがcoalitionを作る | evidence graph、source diversity、contradictionをscore化 | 差分候補 |
| coalition threshold | LIDA global workspace triggers | activation thresholdでworkspace競争 | score + margin + stability + diversityの複合gate | 形式差分は小〜中 |
| global broadcast | GWT/GNW, LIDA, Shared Global Workspace | 容量制限共有、winner broadcast | belief revision engineとしての用途 | 基礎は既知 |
| residual losing hypothesis | LIDA decay, attractor dynamics, ART search | 非勝者やactivityの残留、reset/search | explicit loser stateの復帰率・latencyを最適化 | 差分候補 |
| sparse modules | RIMs, MoE, modular networks | relevant moduleのみ更新、疎通信 | 実際に未選択Sparkを計算しないevent scheduler | 実装差分候補 |
| true event-driven execution | SNN, neuromorphic systems, Lava | event-based asynchronous processing | semantic belief/coalition層との統合 | 統合差分候補 |
| prediction-error activation | predictive coding | error最小化、反復推論 | competing beliefs + workspaceとの統合 | 基礎は既知 |
| mismatch and reset | Adaptive Resonance Theory | vigilance、resonance、category reset | loserを消去せず複数beliefとして保持 | 中程度の差分候補 |
| neural assemblies | Assembly Calculus | cell assembly、k-WTA、Hebbian plasticity | evidence coalitionとworkspaceの上位状態 | 隣接だが別形式 |
| spiking global workspace | Shanahan and later models | spiking competition and broadcast | learned evidence-based belief revision | 「spiking化」だけでは新規でない |
| semantic spiking cognition | NengoSPA / Spaun | semantic pointers、memory、action selection | dynamic evidence coalitionのfirst-class化 | 隣接が強い |
| belief revision benchmark | Belief-R | 更新すべき／維持すべき状況を評価 | architecture-level persistent stateで解く | 実証先として有力 |
| workspace-like LLM internals | 2026 transformer-circuits workspace study | LLMにもreport可能な特権表現の証拠 | 明示state、causal control、execution sparsity | 単純なLLM対Workspace二分法は不可 |

## 3. Strongest precedents

### 3.1 LIDA

最も直接的な先行例。Attention Codelet が workspace content を選び、Coalition を作り、Global Workspace へ追加し、competition と broadcast を行う。公式Java frameworkにも `Coalition`、`GlobalWorkspace`、`RefractoryPeriod`、threshold trigger が存在する。

**Implication:** coalition、threshold、broadcast、codeletという語だけでは新規性を主張できない。

### 3.2 Dynamic Field Theory

神経集団の連続的な活動場、local excitation、surround/global inhibition、self-sustained peak、working memory、peak間競争を形式化する。DFT自身が「thought」を複数peakの協調パターンとして説明している。

**Implication:** 「巨大関数ではなく活動の場」「局所peakが思考を形成」という思想も既知。

### 3.3 RIMs and Shared Global Workspace

RIMsは複数のrecurrent mechanismを持ち、関連する一部だけを更新し、疎に通信する。Shared Global Workspaceは専門モジュールが容量制限workspaceへのアクセスを競争する。

**Implication:** modularity、top-k activation、shared bottleneckを新規性にできない。

### 3.4 Adaptive Resonance Theory

top-down expectationとbottom-up inputの一致を評価し、vigilanceを満たせばresonance、満たさなければresetして別categoryを探索する。

**Implication:** mismatchにより仮説を再探索する原理も既知。

### 3.5 Spiking global workspace and NengoSPA

spiking neuronでcompetition/broadcastを実装した研究が存在する。NengoSPAは大規模spiking network上でsemantic representation、memory、action selection、question answeringを構築できる。

**Implication:** SNNへ移植しただけでは研究差分にならない。

### 3.6 Workspace-like representations in LLMs

2026年には、LLM内部にreport、modulation、flexible reasoningへアクセス可能な特権的表現集合が形成されるという研究報告がある。

**Implication:** 「LLMにはworkspaceがなくSparkBrainにはある」という対立図式は不正確。差分は、explicit persistent state、外部操作可能性、evidence provenance、execution routingに置く必要がある。

## 4. Plausible research gap

### Gap G1 — Persistent competing belief objects

複数beliefをfirst-class objectとして保持し、各beliefがactivation、evidence provenance、contradiction、history、recovery可能性を持つ。通常のlatent vectorや一回限りのcandidate samplingとは区別する。

### Gap G2 — Epistemic coalition

Coalitionを単なるprocessor集合ではなく、仮説と証拠源の一時的な部分グラフとして扱う。同じ情報の重複伝播を独立証拠と数えず、source diversity、contradiction、temporal coherenceを明示する。

### Gap G3 — Residual loser as a trained capability

loser retentionを単なるdecayの副作用ではなく、non-monotonic belief revisionの性能要因として学習・ablation・評価する。

### Gap G4 — No-ignition as a low-level state

「分からない」という文章出力ではなく、workspaceへの昇格自体が起きていない計算状態を持つ。

### Gap G5 — True execution sparsity

概念上のmaskだけでなく、unrouted Sparkに対する状態更新・edge evaluation・kernel launchを発生させない。GPUで遅い可能性と、アルゴリズム上疎であることを分離して評価する。

### Gap G6 — Unified inspectability

output explanationを後付けせず、evidence→Spark→Coalition→Ignition→broadcastを同じ実行traceとして保存し、causal intervention可能にする。

### Gap G7 — Learned transition from functional to spiking substrate

rate-based reference behaviorを先に固定し、その挙動を保ったままspiking backendへ移植し、理論の基板非依存部分と基板依存部分を切り分ける。

## 5. Claims permitted now

- 既存要素を統合した明示的な実験アーキテクチャを定義した。
- Python標準ライブラリでevent-driven reference engineを構築できる。
- canonical SwitchWorldでbelief維持・変更・復帰を可視化できる。
- Phase-0 ablationを再現可能に実行できる。

## 6. Claims prohibited now

- 新しい意識理論を確立した。
- 人間の脳を再現した。
- Transformerより優れている。
- 既存研究に同一構造がないことを証明した。
- event-drivenなので省電力である。
- Spark群が自律的に器官を形成した。

## 7. Novelty verification plan

### Search clusters

1. global workspace + cognitive architecture + codelets + coalition
2. dynamic neural field + belief revision + evidence accumulation
3. persistent competing hypotheses + neural architecture
4. non-monotonic reasoning + recurrent neural state
5. event-driven sparse graph + dynamic routing + working memory
6. spiking global workspace + semantic memory
7. loser retention + hypothesis recovery + attractor
8. epistemic graph + coalition + neural reasoning
9. global workspace + LLM / transformer internals
10. neuromorphic belief revision

### Sources

- Google Scholar / Semantic Scholar
- arXiv
- ACL Anthology
- NeurIPS / ICLR / ICML proceedings
- PubMed
- IEEE Xplore / ACM Digital Library
- Cognitive Computing Research Group
- Dynamic Field Theory community
- official software documentation

### Inclusion criteria

- explicit computational mechanism
- runnable model or enough equations to reproduce
- state persistence or sequential belief update
- competition, coalition, workspace, or event routing
- evaluation beyond purely philosophical description

### Review output

Each candidate receives:

- exact overlap
- exact non-overlap
- implementation availability
- benchmark availability
- license
- reproducibility status
- whether it invalidates a proposed novelty claim

## 8. Publication framing candidate

A defensible future paper title would focus on testable architecture, not brain reproduction.

> **Event-Routed Persistent Belief Dynamics with Evidence Coalitions for Non-Monotonic Revision**

Primary contribution candidates:

1. formal persistent belief/coalition state model
2. event-routed reference implementation
3. revision-focused benchmark protocol
4. causal ablations of residual, coalition, ignition, sparsity
5. rate-to-spiking behavioral equivalence study

## 9. Confidence assessment

| Question | Current confidence |
|---|---:|
| Most primitives are known | high |
| LIDA is the closest cognitive precedent | high |
| DFT is the closest field-dynamics precedent | high |
| RIMs/shared workspace are closest modern ML precedents | high |
| Exact full integration is absent | medium-low |
| Integration can yield measurable gains | unknown |
| True hardware efficiency will improve | unknown |
| Emergent organs will form | speculative |


## Local-first scope note — v0.2.1

The single-machine local-only requirement is an engineering and reproducibility constraint, not a novelty claim. Many prior cognitive architectures and neural simulators already run locally. SparkBrain must not present local execution itself as a scientific contribution.

The boundary is instead operational:

- core theory and evidence must remain testable without access to a proprietary remote service;
- the CPU reference engine defines semantics independently from acceleration substrates;
- local spiking simulation belongs to the core comparison program;
- dedicated neuromorphic hardware and physical energy measurement belong to Extension H;
- results from Extension H cannot retroactively validate biological fidelity or the cognitive theory.

Prior-art auditing should continue to include neuromorphic and hardware implementations because they may invalidate architectural novelty claims, even though reproducing those systems is not required for core completion.
