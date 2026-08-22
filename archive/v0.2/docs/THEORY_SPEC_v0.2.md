# Spark Dynamic Cognition — Theory Specification v0.2

> **Status:** working theory / falsifiable engineering specification  
> **Project code name:** SparkBrain  
> **Formal theory name:** not yet fixed

## 0. Scope

本仕様は、Spark を最小の機能的活動単位として、認知を一回の入力変換ではなく、外部イベントと内部イベントによって時間発展する状態系として定義する。

生物学的ニューロン、意識、主観経験を直接定義するものではない。既存の Global Workspace、LIDA、Dynamic Field、modular recurrent networks、predictive coding、adaptive resonance、spiking systems から着想を得た統合的計算モデルである。

## 1. 基本原理

1. **局所性:** すべての入力が全ノードを更新する必要はない。
2. **持続性:** 仮説、記憶、目的はイベント間でも状態を保持できる。
3. **多候補性:** 相互排他的な belief が同時に非ゼロで存在できる。
4. **通常失敗:** 多数の候補が成立しないことを例外ではなく探索の通常状態とする。
5. **連合判断:** 単一 Spark ではなく、異種かつ独立した証拠の Coalition を判断単位とする。
6. **閾値付き共有:** 十分に強く、安定し、競合との差がある Coalition のみを Global Workspace へ送る。
7. **敗者残留:** winner 以外を原則として即時消去しない。
8. **時間依存:** 同じ入力集合でも順序、時間差、残留状態によって結果が変わり得る。
9. **学習可能性:** 活性、閾値、重み、routing、構造の一部または全部を経験から変更可能とする。
10. **観測可能性:** theory-level state は trace として外部監査可能でなければならない。

## 2. Ontology

### 2.1 Event

外部または内部から生じる離散的状態変化要求。

\[
E_k = (t_k, q_k, src_k, dst_k, u_k, z_k, m_k)
\]

- \(t_k\): 発生時刻
- \(q_k\): event kind
- \(src_k\), \(dst_k\): 発生元と対象
- \(u_k\): 強度。正は興奮、負は抑制
- \(z_k\): evidence identity
- \(m_k\): metadata

Event kinds:

- external stimulus
- propagation
- inhibition
- workspace broadcast
- reward / punishment
- structural change

### 2.2 Spark

Spark \(S_i\) は機能的な局所活動単位であり、単一の生物ニューロンと同一視しない。

\[
S_i(t)=
(a_i, \theta_i, \theta_i^0, \tau_i, \rho_i, r_i, c_i,
\mathcal{P}_i, \mathcal{N}_i, v_i, o_i, k_i)
\]

- \(a_i\): activation
- \(\theta_i\): current threshold
- \(\theta_i^0\): homeostatic base threshold
- \(\tau_i\): decay time constant
- \(\rho_i\): refractory state
- \(r_i\): residual coefficient
- \(c_i\): confidence or reliability state
- \(\mathcal{P}_i\): supporting evidence records
- \(\mathcal{N}_i\): contradictory evidence records
- \(v_i\): semantic / latent representation
- \(o_i\): organ or functional group
- \(k_i\): role: sensory, feature, hypothesis, memory, goal, action, workspace

### 2.3 Connection

\[
W_{ij} = (w_{ij}, d_{ij}, p_{ij}, e_{ij})
\]

- \(w_{ij}\): signed strength
- \(d_{ij}\): propagation delay
- \(p_{ij}\): plasticity flag or rule
- \(e_{ij}\): eligibility trace

### 2.4 Organ

Organ は共通の機能、routing、競争範囲、時間定数を持つ Spark 集合。

\[
O_g(t) = \{S_i(t) \mid o_i=g\}
\]

v0.x では organ を設計者が割り当てる。将来版では、接続密度、情報量、再利用性、因果介入への応答から emergent organ を同定する。

### 2.5 Coalition

Coalition は、ある暫定的な認知内容を共同支持する一時的な Spark 集合と証拠部分グラフ。

\[
C_h(t)=\left(V_h(t), E_h(t), h\right)
\]

- \(h\): 中心仮説または認知内容
- \(V_h\): 支持・記憶・目的・文脈 Spark
- \(E_h\): それらの関係

### 2.6 Global Workspace

Global Workspace \(G(t)\) は容量制限された共有状態。

\[
G(t)=\{g_1,\ldots,g_M\}, \quad M \ll |S|
\]

Workspace は一つの永久中央制御装置ではなく、専門モジュールへ一時的にbroadcastする通信ボトルネックとして定義する。

### 2.7 Brain State

\[
B(t)=
(S(t), W(t), \mathcal{C}(t), G(t), M_s(t), M_l(t), Q(t), \Pi(t))
\]

- \(S(t)\): Spark states
- \(W(t)\): connection states
- \(\mathcal{C}(t)\): active coalitions
- \(G(t)\): workspace
- \(M_s, M_l\): short / long memory
- \(Q(t)\): unresolved beliefs and prediction errors
- \(\Pi(t)\): currently available policies/actions

中心式:

\[
B_{t+1}=F(B_t,E_t;\phi)
\]

ここで \(F\) は固定された巨大変換関数一回ではなく、event queue、局所更新、再帰イベント、競争、ignition を含む状態遷移作用素である。

## 3. Local dynamics

### 3.1 Lazy decay

イベントがない Spark は毎tick計算せず、次に触れた時点で閉形式により減衰させる。

\[
a_i(t_k^-)=a_i(t_{prev})\exp\left(-\frac{t_k-t_{prev}}{\tau_i}\right)
\]

これにより dormant Spark の存在コストと更新コストを分離する。

### 3.2 Event integration

\[
a_i(t_k^+)=a_i(t_k^-)+u_k+\eta_i(t_k)
\]

\(\eta\) は必要な実験だけで導入するノイズ項。

### 3.3 Firing

\[
F_i(t_k)=
\begin{cases}
1 & a_i(t_k^+)\geq\theta_i(t_k) \land t_k\geq\rho_i \\
0 & otherwise
\end{cases}
\]

発火後:

\[
a_i \leftarrow r_i a_i,
\quad
\rho_i \leftarrow t_k + T_{ref},
\quad
\theta_i \leftarrow \theta_i + \Delta\theta_{homeo}
\]

仮説・記憶 Spark は大きな residual を持てる。感覚・行動 Spark は小さな residual を持てる。

### 3.4 Propagation

\[
E_{i\rightarrow j}=
(t_k+d_{ij}, propagation, i,j,w_{ij},z_k,m_k)
\]

外部 evidence identity は sensory routing の間だけ保持する。仮説間抑制を外部証拠と誤認してはならない。

### 3.5 Homeostasis

活動しすぎる Spark は閾値が上がり、時間とともに基準値へ戻る。

\[
\theta_i(t)=\theta_i^0+
(\theta_i(t_{prev})-\theta_i^0)
\exp\left(-\frac{\Delta t}{\tau_{\theta}}\right)
\]

## 4. Competition

同一 competition group 内の候補は signed inhibitory connection または正規化抑制により競争する。

\[
I_i(t)=\sum_{j\in\Gamma_i, j\neq i}g_{ji}F_j(t),
\quad g_{ji}\leq0
\]

本理論では hard WTA を標準にしない。winner は競合を弱めるが、loser をゼロ固定しない。

### Winner-take-most requirement

任意の時刻で、上位候補が増幅され得る一方、少なくとも一定条件では下位候補が residual state として復帰可能であること。

## 5. Evidence semantics

各 external evidence \(z\) は source、time、signed strength を持つ。

\[
R_z=(source_z,label_z,t_z,s_z)
\]

同じ evidence id の重複伝播を独立証拠として数えない。source diversity は独立した情報経路の近似であり、真の統計的独立性を保証しない。

recency:

\[
\gamma_z(t)=\exp\left(-\frac{t-t_z}{\tau_{support}}\right)
\]

support strength:

\[
P_h(t)=\sum_{z\in\mathcal{P}_h}\max(0,s_z)\gamma_z(t)
\]

contradiction:

\[
N_h(t)=\sum_{z\in\mathcal{N}_h}|s_z|\gamma_z(t)
\]

## 6. Coalition score

v0.2 reference score:

\[
Q(C_h,t)=
A_h(t)
+\alpha P_h(t)
+\beta(D_h(t)-1)_+
+\chi K_h(t)
-\delta N_h(t)
\]

- \(A_h\): hypothesis activation
- \(P_h\): recency-weighted support
- \(D_h\): distinct source count
- \(K_h\): temporal stability count
- \(N_h\): contradiction

将来版では次を追加候補とする。

- causal source independence
- semantic coherence
- cross-modal diversity
- predictive success
- goal relevance
- uncertainty / entropy
- metabolic or compute cost

## 7. Ignition

Coalition \(C^*\) がworkspaceへ昇格する条件:

\[
Q(C^*) \geq \Theta_I
\]

\[
Q(C^*)-Q(C^{(2)}) \geq \Delta_I
\]

\[
D(C^*)\geq D_{min}
\]

\[
K(C^*)\geq K_{min}
\]

加えて、再broadcastの無限ループを避けるcooldownまたはstate-change条件を置く。

### No-ignition state

どのCoalitionも条件を満たさない場合、システムは有効beliefを新規確定しない。この状態はエラーではなく、未解決状態である。

## 8. Workspace broadcast

IgnitionしたCoalitionは、memory、language/readout、planner、action、critic等のlistenerへ内部eventとしてbroadcastされる。

\[
Broadcast(C^*) \rightarrow \{O_{memory},O_{action},O_{critic},\ldots\}
\]

broadcast先は新しいSpark activityを生み得るが、external evidenceとしては扱わない。

## 9. Belief revision

belief revision は、単なる出力トークン変更ではなく、workspaceの有効仮説が時間発展により置換されることとして定義する。

### Necessary revision

world state が変化し、十分な新証拠が到来した場合に新beliefへ移る。

### Unnecessary revision

world state が維持されているのにnoiseだけでbeliefを変更する。

### Recovery

過去にworkspaceから外れた仮説が、後続証拠により再びignitionする。

### Stability–plasticity target

最適化対象は「最速変更」でも「最大維持」でもなく、revision precision、revision recall、latency、false ignition の多目的Pareto frontierとする。

## 10. Memory

### 10.1 Residual working state

activation と evidence traces が短時間残る。

### 10.2 Workspace memory

ignition内容が容量制限付きで保持される。

### 10.3 Episodic memory — future

\[
Episode=(B(t_a),E_{a:b},G(t_b),outcome)
\]

類似状況でSparkやCoalitionを再活性化する。

### 10.4 Long-term semantic memory — future

繰り返し成立したCoalitionや関係を、再利用可能なSpark cluster / connection structureへ圧縮する。

## 11. Learning

### 11.1 Eligibility trace

\[
e_{ij}(t+1)=\lambda_e e_{ij}(t)+F_i(t)\psi_j(t)
\]

### 11.2 Reward-modulated update

\[
\Delta w_{ij}=\eta R(t)e_{ij}(t)
\]

v0.2 では最小実装のみ。これはend-to-end学習の証明ではない。

### 11.3 Learned routing — required future work

external embedding \(x\) から top-k Spark を選ぶ。

\[
R(x)=TopK(f_{route}(x,S))
\]

routing loss候補:

- task loss
- sparsity penalty
- load balancing
- consistency under perturbation
- causal intervention sensitivity

### 11.4 Structural plasticity — required future work

- rarely useful edge pruning
- co-active Spark connection growth
- Spark creation / merge / split
- organ discovery
- catastrophic dominance prevention

## 12. Time scales

| Scale | Candidate process |
|---|---|
| milliseconds / event substeps | integration, inhibition, firing |
| short cycle | coalition formation, ignition |
| seconds / episode | working memory, belief revision |
| episodes | eligibility / reward learning |
| long training | routing, semantic compression, structural plasticity |

異なる時間スケールを一つの固定tickへ無理に統合しない。

## 13. Required invariants

1. external evidence と internal propagation を区別する。
2. 同じ evidence id を独立証拠として重複計上しない。
3. no-ignition を有効状態として保持できる。
4. workspace capacity を超えた場合の退避規則が決定論的である。
5. trace取得がengine dynamicsを変えない。
6. random seed と設定が保存される。
7. baselineと比較する際、入力情報量を一致させる。
8. energy claimは実測hardwareまで保留する。

## 14. Falsification criteria

次の結果は理論の主要部を弱める。

- residual retentionを外してもrecoveryが全タスクで同等以上
- coalitionを外してもfalse ignitionとrevisionの両方が同等以上
- matched computeのGRU/Transformer/RIMが全Pareto frontierで支配
- sparse routingにすると性能が崩れ、dense executionでしか成立しない
- learned routingが手書きroutingから一般化しない
- trace上のCoalition scoreが出力決定を実際には説明しない
- hyperparameterの極小変化で挙動が不安定になり、頑健領域が存在しない

否定的結果は理論の失敗ではなく、適用境界を確定する成果とする。

## 15. Novelty boundary

既知または強く先行する要素:

- codelets / coalition / global broadcast: LIDA
- local excitation / inhibition / persistent peaks: Dynamic Field Theory
- sparse specialist modules: RIMs
- bandwidth-limited shared workspace: Shared Global Workspace
- mismatch / reset / resonance: Adaptive Resonance Theory
- prediction-error dynamics: predictive coding
- spiking competition and broadcast: prior spiking global workspace models
- semantic computation in spiking networks: NengoSPA

新規性候補は単一要素ではなく、次の統合と実証設計に置く。

> persistent competing belief states + evidence-structured coalition + loser recovery + coalition-level ignition + true event-routed execution sparsity + learnable modern ML implementation

これはまだ新規性確認済みの主張ではない。systematic review、再現実装、査読可能な比較が必要である。

## 16. References

- Franklin, S. et al. LIDA / Global Workspace cognitive architecture. Cognitive Computing Research Group, University of Memphis.
- Schöner, G., Spencer, J. P., and DFT Research Group. *Dynamic Thinking: A Primer on Dynamic Field Theory*. Oxford University Press, 2016.
- Goyal, A. et al. “Recurrent Independent Mechanisms.” arXiv:1909.10893.
- Goyal, A. et al. “Coordination Among Neural Modules Through a Shared Global Workspace.” arXiv:2103.01197; ICLR 2022.
- Grossberg, S. “Adaptive Resonance Theory.” Scholarpedia.
- Shanahan, M. “A Spiking Neuron Model of Cortical Broadcast and Competition.” *Consciousness and Cognition* 17, 2008, 288–303.
- Tschantz, A. et al. “Hybrid Predictive Coding: Inferring, Fast and Slow.” arXiv:2204.02169.
- Wilie, B. et al. “Belief Revision: The Adaptability of Large Language Models Reasoning.” EMNLP 2024. DOI: 10.18653/v1/2024.emnlp-main.586.
