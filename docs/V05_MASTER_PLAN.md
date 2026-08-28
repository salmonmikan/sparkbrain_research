# SparkBrain v0.5 Master Plan

**Status:** Proposed research and implementation plan  
**Baseline:** `main@dacd8b536f2ab5d7060f4a572b87ecef811d1d09`  
**Baseline system:** SparkBrain v0.4 pre-semantic temporal excitable signal field  
**Execution condition:** One general-purpose local computer; CPU reference path required; no cloud runtime or dedicated neuromorphic hardware  
**Primary principle:** Meaning is not a primitive. Build the Spark dynamics carefully first.

---

## 1. v0.5の目的

v0.4では、意味ラベルを持たないデジタル信号から次の現象を構成できた。

```text
digital change
  -> local pulse
  -> sub-threshold activity
  -> Spark / micro-spike
  -> delayed propagation
  -> local burst
  -> cascade
  -> Ignition
```

さらに、入力順序、到着タイミング、反復、入力欠落、局所的な移動方向によって、内部活動が変化することを確認した。

v0.5では、その一段先を扱う。

> **ノイズを含む時間的入力の反復経験から、特定の時系列に選択的なSpark Assemblyが自律形成され、そのAssemblyが未知の変形入力に再利用され、予測または行動に機能的な利益を与えるかを検証する。**

v0.5の中心は「意味理解」ではない。

```text
反復する時間構造
       ↓
接続・遅延・閾値の変化
       ↓
再現性のあるSpark Assembly
       ↓
未知の変形入力でも再活性化
       ↓
予測または行動に利用
```

ここまでを目標とする。

---

## 2. v0.5で使う用語

### 2.1 Sub-threshold activity

入力や内部伝播によって局所状態は変化したが、まだ外部へ伝播可能なイベントを発生させていない状態。

### 2.2 Spark

局所的な内部興奮が閾値を越え、他のunitへ伝播可能になったイベント。

Spark自体に「猫」「危険」などの意味は持たせない。

### 2.3 Burst

短い時間窓で、複数の異なるunitからSparkが発生した局所活動。

### 2.4 Cascade

SparkまたはBurstが、遅延接続を通して複数の時間bin・領域へ連続的に伝播した活動。

### 2.5 Assembly Candidate

似た時空間Cascade signatureが複数回再出現した状態。

これはまだ概念ではない。

### 2.6 Selective Temporal Assembly

特定の隠れた時間motifに対して、matched noiseや順序shuffleより選択的に再活性化するAssembly。

### 2.7 Functional Assembly

Selective Temporal Assemblyのうち、held-out入力の予測または行動成績を改善するもの。

### 2.8 Causal Functional Assembly

Functional Assemblyのうち、対象Assemblyを選択的に抑制すると対応機能が悪化し、matched random ablationでは同程度に悪化しないもの。

v0.5で最大限主張できる候補はここまでであり、これを「意味概念」「意識」「器官」とは呼ばない。

---

## 3. 研究上の中心問い

### RQ-05-1

同じ局所要素を含むが時間順序の異なるmotifに対して、異なるAssemblyを形成できるか。

### RQ-05-2

ノイズ中で反復するmotifに対し、明示的なmotif IDや意味ラベルをモデルへ与えず、選択的なAssemblyを形成できるか。

### RQ-05-3

形成されたAssemblyは、時間jitter、欠損、振幅変化、異なる背景noiseに対して再利用できるか。

### RQ-05-4

Assembly形成は、固定接続・shuffle時刻・shuffle報酬・no-plasticityと比較して有意な機能差を生むか。

### RQ-05-5

形成されたAssemblyを抑制すると、そのAssemblyが担う予測または行動だけが選択的に悪化するか。

### RQ-05-6

学習が進んでも、Fieldは全面発火または完全沈黙へ崩壊せず、有限の活動範囲を維持できるか。

---

## 4. 仮説と反証条件

## H05-1: Timing-selective assembly formation

反復する時間motifは、matched noiseより高い再現性と選択性を持つAssemblyを形成する。

**支持条件**

- motif条件のAssembly recurrenceがmatched controlsより高い
- motif内の順序shuffleで選択性が低下する
- 複数seedで同じ方向の効果が出る

**反証・弱化条件**

- motifとnoiseでrecurrence差がない
- 時刻shuffle後も同じ結果になる
- 一つの特定seedまたはtopologyにしか出ない

## H05-2: Plasticity-dependent formation

Assemblyの選択性は、時間依存可塑性または遅延適応によって増加する。

**支持条件**

- plastic版がfrozen版をheld-outで上回る
- weight shuffleまたはdelay shuffleで効果が低下する
- 学習前後の差がraw traceから再計算可能

**反証・弱化条件**

- frozen topologyでも同じ
- random driftでも同じ
- activity量の増加だけで説明できる

## H05-3: Functional reuse

形成されたAssemblyは、学習時と異なるnoise背景・jitter・部分欠損でも予測または行動へ再利用される。

**支持条件**

- trainで未使用の変形条件で性能改善
-単純な入力頻度や総振幅をmatched controlとして除外
- no-assemblyまたはrandom assemblyより改善

**反証・弱化条件**

- train配列の完全再生でしか反応しない
- 背景noise変更で崩壊する
- motif IDを外部から渡さないと使えない

## H05-4: Causal contribution

特定Assemblyを抑制すると、対応機能が選択的に低下する。

**支持条件**

- targeted ablation impairment > matched random ablation
- 他motifまたは他行動へのcollateral damageが制限内
- 複数seedで再現

**反証・弱化条件**

- random ablationと差がない
- 全機能が一様に落ちる
- Assemblyがなくても同じ性能を維持する

## H05-5: Bounded self-organization

可塑性と反復入力があっても、Fieldはrunawayまたはdead stateへ恒常的に崩壊しない。

**支持条件**

- runaway event rateが上限未満
- dead-field episode率が上限未満
- perturbation後に活動範囲へ復帰
- homeostasis ablationで悪化

**反証・弱化条件**

- tuningした一条件以外で全面発火または沈黙
-安全limitによる強制停止だけで成立
- activity budgetを外すと即崩壊する

---

## 5. v0.5アーキテクチャ

```text
Digital Source
      │
      ▼
┌──────────────────────────┐
│ Receptor / Transduction  │
│                          │
│ raw value                │
│ local delta              │
│ derivative               │
│ novelty                  │
│ omission/error           │
│ local gain control       │
│ multi-timescale traces   │
└────────────┬─────────────┘
             │ SignalPulse
             ▼
┌──────────────────────────┐
│ Temporal Excitable Field │
│                          │
│ membrane accumulation    │
│ delayed signed edges     │
│ refractory               │
│ adaptation               │
│ inhibition               │
│ homeostatic threshold    │
└────────────┬─────────────┘
             │ Sparks
             ▼
┌──────────────────────────┐
│ Burst / Cascade Layer    │
│                          │
│ causal lineage           │
│ temporal signature       │
│ spatial spread           │
│ recurrence               │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Assembly Layer           │
│                          │
│ candidate formation      │
│ recurrence tracking      │
│ selectivity evaluation   │
│ stability / decay        │
└────────────┬─────────────┘
             │
       observer first
             │
        ┌────┴────┐
        ▼         ▼
   Predictor    Action
        │         │
        └────┬────┘
             ▼
         World result
             │
             ▼
   eligibility / reward
```

### 設計原則

1. 意味ラベルをFieldへ渡さない。
2. motif IDは評価器だけが保持し、runtimeは参照しない。
3. Assembly detectorは最初はobserver-onlyとする。
4. Assemblyを予測・行動へ接続する段階は別gateにする。
5. activityが増えただけの結果を学習成功と呼ばない。
6. 接続重み、伝播遅延、閾値の変更を別ablationで評価する。
7. 固定topologyで先に検証し、構造成長は後段の条件付きtrackとする。
8. CPUで再現可能な小規模構成を必須とする。

---

## 6. 実装方針

v0.4を凍結baselineとして残し、v0.5はversioned namespaceへ追加する。

```text
src/sparkbrain/v05/
├─ __init__.py
├─ contracts.py
├─ receptors.py
├─ field.py
├─ homeostasis.py
├─ plasticity.py
├─ delay_learning.py
├─ assemblies.py
├─ prediction.py
├─ action.py
├─ brain.py
├─ worlds.py
├─ evaluation.py
├─ checkpoint.py
└─ visualizer.py
```

### v0.4再利用ルール

- 安定した`SignalPulse`、event queue、basic edge contractは再利用可
- v0.4の既存挙動を直接書き換えない
- v0.5の差分は明示的なadapterまたはsubclassで表現する
- v0.4 reference testsは不変で通す
- v0.5で新しいschemaを導入する場合はadditiveにする

---

## 7. 作業計画

## V05-00 — Baseline freeze and preregistration

### 目的

v0.4の実装・artifact・既知結果を固定し、v0.5の主要仮説と評価条件を結果を見る前に登録する。

### 成果物

- `docs/THEORY_SPEC_v0.5.md`
- `docs/V05_EXPERIMENT_PROTOCOL.md`
- `docs/V05_CLAIM_BOUNDARIES.md`
- `docs/V05_STATUS.md`
- baseline hashes
- protected negative results
- primary/secondary metrics
- seed list
- parameter search boundary

### 受入条件

- v0.4回帰テストPASS
- protocolがmotif結果を見る前に固定
- primary gateを後付け変更しない
-変更時はamendmentとして履歴保存

---

## V05-01 — Receptor and transduction refinement

### 目的

入力を単一pulseへ即変換せず、複数時間スケールの局所状態を経由させる。

### 実装

- fast / medium / slow leaky trace
- local delta
- rate of change
- novelty
- omission
- bounded gain control
- local competition
- event emission threshold
- receptor adaptation
- per-source normalization

### 実験

- 同振幅・異時間幅
- 同総量・異順序
- slow driftとabrupt change
- repeating baselineとdeviation
- amplitude-only control

### 受入条件

- 時間構造の違いがpulse列へ残る
- 総入力massだけで結果が決まらない
- sourceごとのスケール差で一方がFieldを独占しない
- 全channelを無制限に発火させない

---

## V05-02 — Stable excitable dynamics and homeostasis

### 目的

Fieldを「何でも爆発する系」「何も発火しない系」の中間に保つ。

### 実装

- unit別homeostatic threshold
- inhibitory normalization
- adaptation recovery
- burst refractory
- cascade-level cooldown
- event budget
- runaway detector
- dead-field detector
- bounded recovery mechanism

### 診断指標

- firing-rate distribution
- active-unit fraction
- cascade-size distribution
- branching-ratio proxy
- runaway episode rate
- dead episode rate
- perturbation recovery time

### 注意

branching ratioやpower-lawは診断値であり、臨界性の証明とは呼ばない。

### 受入条件

- 広い入力強度範囲で安全に継続
- homeostasisあり/なしで安定性差
- safety limitだけに依存しない
- deterministic reference pathを維持

---

## V05-03 — Timing-dependent weight and delay learning

### 目的

反復する時間関係が、接続重みと伝播遅延へ反映されるようにする。

### 実装

- bounded STDP-like update
- eligibility trace
- reward modulationは任意
- positive edge delay adaptation
- min/max weight
- min/max delay
- per-step update budget
- frozen / weight-only / delay-only / full ablation

### 受入条件

- 同じpre/post順序で決定論的更新
- reversed timingで異なる更新
- weightのみ、delayのみ、両方の効果を分離
- 学習後もrunawayしない
- checkpoint/replay一致

---

## V05-04 — Motif-in-noise Assembly formation

### 目的

意味ラベルなしに、ノイズ中の反復時系列からAssembly Candidateが形成されるかを検証する。

### Primary world

```text
background:
  random low-amplitude local events

hidden motif:
  A -> 5ms -> F -> 2ms -> C

controls:
  same elements, shuffled order
  same order, shuffled timing
  same event frequency, no motif
  pure noise
```

motif IDはevaluatorのみが保持する。

### Assembly Candidate条件

- recurrence count
- signature similarity
- temporal consistency
- participating-unit stability
- false recurrence under null
- minimum lifetime
- bounded candidate count

### 受入条件

- motif条件でselectivity上昇
- control条件で同程度のcandidate proliferationが起きない
- multiple seeds
-複数noise level
- train/test motif occurrenceを分離
- human-readable semantic labelなし

---

## V05-05 — Held-out robustness and pattern completion

### 目的

形成されたAssemblyが、完全一致以外でも再活性化するかを検証する。

### Held-out変形

- timing jitter
- amplitude scaling
- one-event omission
- additive distractor
- spatial shift
- different noise distribution
- partial observation
- time compression / expansion（secondary）

### 指標

- Assembly recall
- false activation
- detection latency
- selectivity index
- calibration
- degradation curve
- noise robustness

### 受入条件

- train配列の暗記だけでは説明できない
- moderate jitter/欠損で性能が即ゼロにならない
- matched random signatureより良い
- background変更後も再利用

---

## V05-06 — Functional prediction

### 目的

Assemblyが次の局所イベントまたは短期未来の予測に役立つかを検証する。

### 予測対象

- next receptor event
- next event timing bin
- omission probability
- local continuation
- motif completion

### 比較

- full Assembly
- no Assembly
- random Assembly
- frozen plasticity
- shuffled timing
- frequency-only baseline

### 受入条件

- held-out predictionがmatched baselineより改善
- Assemblyを利用しない場合に同じ改善が出ない
-単純なmotif頻度だけで説明できない
-予測誤差がFieldへfeedback可能

---

## V05-07 — Functional action and reward

### 目的

Assemblyを、意味ラベルではなく行動結果によって機能化する。

### World

複数のhidden motifが存在し、それぞれに異なるactionが報酬を得る。

```text
motif-X -> action-1
motif-Y -> action-2
unknown/noise -> withhold or inspect
```

runtimeへmotif IDは渡さない。

### 比較

- full plasticity
- frozen action association
- shuffled reward
- random Assembly
- no Assembly
- direct raw-input baseline

### 指標

- cumulative reward
- action accuracy
- withhold quality
- wrong-action rate
- adaptation after reversal
- extinction / relearning
- action latency

### 受入条件

- held-out motif変形でも適切なactionへ寄与
- shuffled rewardでは成立しない
- no Assemblyより改善
- reversal後に更新可能
- meaningless continuous firingを報酬獲得と誤認しない

---

## V05-08 — Causal ablation

### 目的

形成されたAssemblyが、単なる相関した活動ではなく機能に寄与するかを検証する。

### 介入

- targeted unit suppression
- targeted edge suppression
- timing disruption
- delay randomization
- matched random unit ablation
- matched random edge ablation
- sham intervention

### 指標

- target function impairment
- random-control impairment
- collateral damage
- recovery
- alternate-path compensation
- intervention specificity

### 受入条件

- targeted impairment > random impairment
- collateral damageが上限内
-複数seedで同方向
- assembly observerの表示だけを消す介入では性能が変わらない
-モデル全体破壊による見かけの因果性を除外

---

## V05-09 — Optional structural plasticity track

### 開始条件

V05-04〜V05-08で、固定topology上のweight/delay learningだけではAssembly形成が不十分と判断された場合のみ開始する。

### 実装候補

- edge growth
- edge pruning
- local rewiring
- receptor-field remapping
- unit duplication
- local resource budgets

### 制約

- growth/pruningは別protocol
- unlimited model growth禁止
-同一計算資源でbaseline比較
- topology changeを意味や器官と呼ばない

---

## V05-10 — Brain Lab, release, and audit

### Brain Lab表示

- raw receptor activity
- sub-threshold state
- Spark
- delayed arrivals
- Burst
- Cascade lineage
- Assembly Candidate
- plastic weight/delay changes
- homeostasis state
- prediction
- action
- reward
- targeted ablation
- matched-control comparison

### 保存

- raw JSONL trace
- config
- seed
- exact source revision
- checkpoint
- candidate lineage
- per-episode output
- aggregate
- static offline HTML
- artifact hashes

### Release条件

- CPU local-only
- no mandatory network
- no external CDN
- deterministic reduced reference
- test tier separation
- negative results preserved
- claim register updated
- release manifest
- clean archive reproduction

---

## 8. 実験セット

## E05-0 — Null noise

motifなしのnoiseのみ。

目的はfalse Assembly率とcandidate proliferationの上限を測ること。

## E05-1 — Single repeated motif

一つのmotifをnoise中へ反復。

Assembly Candidate形成の最小実験。

## E05-2 — Order control

同じイベント集合で順序だけshuffle。

順序選択性を測る。

## E05-3 — Timing control

順序は同じで時間間隔だけshuffle。

timing依存性を測る。

## E05-4 — Two competing motifs

一部unitを共有する二つのmotif。

一つの巨大Assemblyへ潰れず分離できるか。

## E05-5 — Jitter and partial observation

時間jitter、欠損、distractorを加える。

暗記ではなくrobust reuseを測る。

## E05-6 — Context transfer

背景noise分布または空間位置を変更。

motif構造の再利用を測る。

## E05-7 — Prediction utility

Assemblyから次eventまたはomissionを予測。

## E05-8 — Action utility

Assemblyに基づきactionを選択し、報酬で学習。

## E05-9 — Reversal and extinction

報酬対応を変更または消去。

自己訂正と再学習を測る。

## E05-10 — Causal ablation

targeted / random / shamを比較。

---

## 9. 評価指標

### Signal dynamics

- input pulse count
- active unit fraction
- spike count
- burst count
- cascade count
- cascade size
- cascade duration
- spatial spread
- event queue work
- dense inspection count
- downstream active work

### Stability

- runaway episode rate
- dead-field episode rate
- safety abort rate
- recovery time
- threshold distribution
- inhibition/excitation balance proxy

### Assembly

- candidate count
- recurrence
- within-candidate similarity
- between-candidate separation
- motif selectivity
- null false-positive rate
- candidate lifetime
- seed consistency

### Robustness

- jitter tolerance
- omission tolerance
- distractor invariance
- amplitude invariance
- context-transfer accuracy
- false activation

### Function

- prediction accuracy
- prediction calibration
- prediction error
- cumulative reward
- action accuracy
- withhold precision/recall
- reversal latency

### Causality

- targeted impairment
- matched random impairment
- effect-size difference
- collateral damage
- recovery after intervention
- alternate-path compensation

### Reproducibility

- deterministic replay
- checkpoint continuation equality
- artifact hash equality
- seed/config provenance
- no-network verification

---

## 10. Primary scientific gates

## Gate A — Engineering stability

- v0.4回帰PASS
- v0.5 unit/integration PASS
- runaway/dead-field制御
- checkpoint/replay
- local-only

## Gate B — Selective Assembly

- motif > matched noise/selectivity
- order/timing shuffleで低下
-複数seed
- false candidate率上限内

## Gate C — Held-out reuse

- jitter/欠損/異背景で再活性化
- train完全再生限定ではない
- random candidateより改善

## Gate D — Functional utility

- predictionまたはactionでbaseline改善
- no Assembly / frozen / shuffled controlより改善
- artifactから再計算可能

## Gate E — Causal contribution

- targeted ablation > matched random
- bounded collateral
- multiple seeds

### 判定ルール

- Gate Aのみ: 安定したSpark learning substrate
- Gate A+B: selective temporal assembly candidateを支持
- Gate A+B+C: reusable temporal assemblyを支持
- Gate A+B+C+D: functional temporal assemblyを支持
- Gate A+B+C+D+E: causal functional temporal assemblyを支持

Gate Eを通っても「意味概念」「器官」「意識」とは呼ばない。

---

## 11. テスト戦略

### Fast unit

目標: 60秒以内

- receptor traces
- event ordering
- decay
- refractory
- adaptation
- homeostasis
- weight/delay update
- candidate hashing
- checkpoint schema
- bounds and failure cases

### Engineering integration

目標: 3分以内

- small motif world
- noise control
- two-motif separation
- prediction smoke
- action smoke
- checkpoint continuation
- Brain Lab API

### Scientific smoke

目標: 10分以内

- 3 seed
- reduced episodes
- all primary ablations
- metric/artifact contract

### Full scientific reproduction

通常pytestから分離する。

- preregistered full seed set
- full episode count
- held-out worlds
- bootstrap/confidence interval
- artifact regeneration
- hash verification

### Release

- clean extraction
- no-network
- CPU reference
- manifest validation
- static visualizer
- tamper matrix
- archive/repository mode

---

## 12. パラメータ調整ルール

過学習と結果後調整を避けるため、調整対象を限定する。

### Train/Developmentで調整可能

- receptor time constants
- base threshold
- adaptation gain
- inhibitory strength
- STDP window
- weight bounds
- delay bounds
- Assembly similarity threshold
- homeostasis target range

### Testで変更禁止

- primary metric
- seed
- motif structure
- held-out jitter range
- success threshold
- ablation definition
- candidate acceptance criteria

### 探索方法

- bounded gridまたは事前登録したrandom search
- tuning budget固定
-最良条件だけでなく全試行を保存
- test結果を見て再調整した場合は新protocolとする

---

## 13. 成果物

### 理論

- `THEORY_SPEC_v0.5.md`
- 初学者向け説明
- Glossary追加
- claim boundaries
- falsification conditions

### 実装

- `sparkbrain.v05`
- CPU reference runtime
- configs
- worlds
- evaluation
- checkpoint
- static visualizer

### 実験

- raw traces
- per-seed results
- matched controls
- ablations
- held-out tests
- causal interventions
- negative results

### レポート

- engineering report
- scientific report
- results ledger
- decision log
- claim register addendum
- reproducibility guide

---

## 14. v0.5で扱わないもの

次はv0.5のPrimary acceptanceには含めない。

- 自然言語の意味理解
- semantic grounding
-人間が理解できる概念名
-長期計画
-自己意識
- AGI
-生物ニューロンとの等価性
-物理的な省電力性
- neuromorphic hardware
-器官形成の主張
-外部LLMとの性能比較

画像、音声、テキストはSignalPulse生成のstress inputとして利用可能だが、意味タスクをprimary benchmarkにしない。

---

## 15. 主要リスク

### 全面発火

対策:

- inhibition
- homeostasis
- adaptation
- event budget
- cascade cooldown

### 完全沈黙

対策:

- threshold floor
- bounded gain
- novelty/error input
- dead-field recovery

### Assembly候補の乱立

対策:

- null false-positive gate
- candidate decay
- minimum recurrence
- candidate budget
- matched-noise calibration

### 単なる暗記

対策:

- held-out jitter
- missing events
- context transfer
- unseen noise
- train/test separation

### ラベル漏洩

対策:

- motif IDはevaluatorのみ
- runtime contractで禁止
- static audit
- adversarial leak test

### 活動量増加を学習と誤認

対策:

- firing-rate-matched controls
- frozen plasticity
- random drift
- shuffle controls
- functional metrics必須

### 因果性の誤認

対策:

- targeted/random/sham
- collateral damage
- selective impairment
- repeated seeds

---

## 16. 完成条件

v0.5は、次の二つのどちらかで正式完了とする。

### Positive completion

- Gate A〜Eを通過
- Causal Functional Temporal Assemblyを支持
- 再現パッケージ完成
- 過大主張なし

### Negative completion

- protocolと実装が正しく動作
- matched controlsと複数seedを完走
- Assembly形成または機能獲得が支持されなかった
- 負結果と最強の反例を保存
- 次の理論修正点を特定

成功結果を得ることではなく、**Spark Assemblyが機能を獲得する仮説を反証可能に検証すること**がv0.5の完成条件である。

---

## 17. v0.5の最終到達点

v0.5の理想的な到達点は次である。

```text
意味ラベルのない局所信号
        ↓
時間的な反復経験
        ↓
Fieldの接続・遅延・閾値が変化
        ↓
特定motifに選択的なAssembly形成
        ↓
未知の変形motifでも再活性化
        ↓
予測または行動を改善
        ↓
対象Assemblyの切除で対応能力が選択的に低下
```

ここまで通れば、

> **SparkBrainは、単に信号を爆発させる媒体から、経験によって機能的な時間構造を獲得する媒体へ進んだ**

と主張できる。

それでもまだ「意味」「概念」「器官」ではない。  
意味は、その先で複数のFunctional Assemblyが世界・行動・記憶と長期的に結び付いた結果として検討する。
