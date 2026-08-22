# Spark Field Architecture (SFA) v0.1

## 目的

巨大な同期型 forward pass を中心にせず、**多数の小さな仮説・特徴・行動候補（Spark）を非同期に発生させ、
局所競争・再帰増幅・抑制を経て、一時的な連合（Coalition）が十分に安定した場合のみ
Global Workspace に昇格させる**計算モデル。

これは「脳の再現」ではなく、以下の既存概念を実装可能な形で合成した実験アーキテクチャである。

- event-driven / spiking computation
- leaky integration
- lateral inhibition / soft winner-take-most
- recurrent excitation
- predictive-error driven activation
- global-workspace-like ignition
- local plasticity / eligibility traces
- homeostatic threshold adaptation

## 1. 最小単位: Spark

各 Spark `i` は以下の状態を持つ。

```text
Spark_i
  id
  kind             # feature / hypothesis / memory / goal / action
  vector           # 必要なら埋め込み
  activation a_i
  threshold θ_i
  confidence c_i
  age
  refractory
  eligibility e_i
  source_ids[]
  last_fire_time
```

Spark は常時「正解」である必要がない。
大半は閾値未満で消えるか、短い residual trace だけを残す。

## 2. イベント入力

入力は固定長の一括 tensor ではなくイベントとして流す。

```text
Event {
  t,
  source,
  payload,
  strength,
  embedding?
}
```

イベントは関連する Spark だけを刺激する。
したがって計算量は原理的には「全ノード数」より「その時に活動した局所集合」に依存させられる。

## 3. Spark dynamics

簡略形:

```text
a_i(t+Δt)
 = decay(a_i)
 + Σ_j excitatory_weight(j,i) * spike_j
 - Σ_k inhibitory_weight(k,i) * spike_k
 + prediction_error_i
 + goal_bias_i
 + noise_i
```

発火条件:

```text
a_i >= θ_i
```

ただし発火した Spark 1 個をそのまま最終出力にはしない。

## 4. Local competition

同じ役割を持つ候補群では lateral inhibition を使う。

例:

```text
cat ─┐
dog ─┼─ compete
toy ─┘
```

強い候補は競合候補を抑制するが、完全には消さない。
これにより後から反証が来た時に仮説を反転できる。

## 5. Coalition

同一仮説を支持する異種 Spark が一時的に束になる。

```text
[fur] ─┐
[meow] ├──> coalition: CAT
[purr] ┘
```

Coalition score の例:

```text
score(C)
 = Σ activation(member)
 + diversity_bonus
 + temporal_coherence
 + recurrent_support
 - contradiction
```

単一の強い Spark よりも、独立した複数ソースが整合する連合を優先する。

## 6. Ignition / Global Workspace

以下を満たした Coalition のみ broadcast する。

```text
score(C) >= ignition_threshold
AND
stability(C, τ) >= stability_threshold
AND
margin(C, competitors) >= margin_threshold
```

broadcast 後は:

```text
                ┌-> memory
coalition ------+-> language
                +-> planner
                +-> action
                └-> critic
```

受信側は broadcast を新しい入力イベントとして扱い、さらに Spark を生成できる。

## 7. 失敗を許容する設計

失敗候補は即削除しない。

```text
winner: activation high
losers: activation decays slowly
```

残留値により、後続証拠で仮説の復活が可能になる。

したがって SFA の基本思想は:

```text
failure != exception
failure == normal search dynamics
```

## 8. 学習

### Fast learning
- eligibility trace
- short-term synaptic facilitation
- threshold adaptation

### Slow learning
- Hebbian / STDP-like update
- reward-modulated eligibility
- structural pruning / growth

概念形:

```text
Δw_ij = η * reward * eligibility_ij
```

### Homeostasis

発火しすぎる Spark は threshold を上げ、
発火しなさすぎる Spark は threshold を下げる。

これで常時同じ Spark が勝つことを防ぐ。

## 9. 推奨する階層

```text
Input/Event Layer
      ↓
Perceptual Sparks
      ↓
Concept / Hypothesis Sparks
      ↕
Memory Sparks
      ↕
Goal / Value Sparks
      ↓
Coalition Manager
      ↓
Global Workspace
      ↓
Planner / Language / Action
```

## 10. LLMとのハイブリッド

v0.x では Spark 自体を完全な SNN にしなくてもよい。

実装現実解:

```text
small encoders / tiny MLP / embedding match
            ↓
       Spark Field
            ↓
       ignition
            ↓
          LLM
```

LLM は「思考主体」ではなく、
Workspace に上がった状態の言語化・高次変換器として使う。

将来的には各 Spark cluster を tiny recurrent network / SNN に置換可能。

## 11. v0.1 の検証条件

以下が確認できれば最初の仮説は支持される。

1. 1つの誤証拠で即断しない
2. 複数の独立証拠で ignition する
3. 後から反証が来ると winner が切り替わる
4. loser が完全消去されず復帰できる
5. 全ノードを毎 tick 計算しなくても動く
6. ノイズの多い入力でも coalition により安定する

## 12. この設計で独自性が強い部分

既存要素そのものではなく、以下の統合を主眼とする。

- **single-neuron threshold ではなく coalition ignition**
- **failed sparks の residual retention**
- **winner-take-all ではなく winner-take-most**
- **output を直接生成せず workspace broadcast を挟む**
- **「失敗」を探索の通常状態として扱う**
- **semantic Spark と spiking/event dynamics の中間層**
