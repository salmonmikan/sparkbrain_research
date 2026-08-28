# SparkBrain用語集 — やさしい説明つき v0.2.1

この用語集では、日常語としての意味とSparkBrain内の技術的な意味を分ける。

## 1. 中心となる構成要素

| 用語 | やさしい説明 | SparkBrainでの厳密な扱い | そういう意味ではない |
|---|---|---|---|
| Spark | 小さな「考え・特徴・記憶の火種」 | 活動値、閾値、減衰、証拠、役割等を持つ局所状態単位 | 生物ニューロン1個そのもの |
| Event | 何かが起きたという通知 | 時刻、種類、発生元、対象、強度、証拠ID等を持つ離散状態変化 | 画面上のクリックだけ |
| Connection | Spark同士の影響経路 | 符号付き重み、遅延、可塑性、eligibilityを持つ有向辺 | 必ず物理的な神経線維 |
| Organ | 同じ機能を担うSpark群 | 共通のrouting、競争範囲、時間特性等を持つ集合 | 解剖学的な脳器官 |
| Brain State | その瞬間の人工脳全体 | Spark、接続、Coalition、Workspace、記憶、未解決仮説等の集合 | 出力文字列だけ |
| World | 人工脳が置かれる外界 | 真の状態、観測、ノイズ、行動、報酬を供給する実験環境 | 現実世界に限定 |

## 2. Sparkの動き

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Activation | Sparkの現在の勢い | 時間とイベントで変化する数値状態 | 確率とは限らない |
| Threshold | 発火に必要な境界 | activationが超えると発火条件の一部を満たす値 | 真偽の境界ではない |
| Firing | 周囲へ影響を送る活動イベント | 閾値と不応期条件を満たしたSparkの出力イベント | 最終判断の確定ではない |
| Excitation | 相手を強める | 正の強度でactivationを増やす作用 | 正しい証拠とは限らない |
| Inhibition | 相手を弱める | 負の強度でactivationを下げる内部作用 | 外部反証と同一ではない |
| Decay | 時間とともに弱まる | 経過時間に応じた活動値の減衰 | 状態が即消えることではない |
| Lazy Decay | 必要になった時だけ減衰を計算する | 最後の更新時刻から閉形式で現在値を計算 | モデル時間が止まるわけではない |
| Residual | 発火・敗北後に残る活動 | 活動値をゼロにせず一定割合残す仕組み | その仮説が正しい保証ではない |
| Refractory | 発火直後の休み | 一定時間、再発火を禁止または抑える状態 | Sparkの削除ではない |
| Homeostasis | 活動しすぎを抑える調整 | 閾値等を基準値へ適応させる仕組み | 生物学的恒常性を完全再現するものではない |
| Recurrence | 活動が循環して戻る | 接続を通じて同じ系へ再入力される処理 | 必ず無限ループになるわけではない |

## 3. 証拠と仮説

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Evidence | 外界から得た観測記録 | ID、source、時刻、符号付き強度等を持つレコード | 確定した事実とは限らない |
| Evidence ID | 同じ観測を見分ける番号 | 伝播しても同一証拠を重複計上しないための識別子 | Spark IDではない |
| Source | 証拠が来た経路 | センサー、記憶、外部チャネル等の識別 | 統計的独立性を自動保証しない |
| Support | 仮説を強める証拠関係 | evidenceからbeliefへの正の関係 | 因果的真実そのものではない |
| Contradiction | 仮説を弱める外部証拠 | evidenceからbeliefへの負の関係 | 内部の側方抑制ではない |
| Belief | 持続する課題上の仮説 | 複数同時に非ゼロで保持できるhypothesis state | 人間の主観的信念 |
| Competing Beliefs | 複数候補を同時に残す | 同一competition group内で相互抑制されるbelief群 | すべてを同時に正しいと確定すること |
| Confidence | 判断の信頼度 | calibration可能な別状態またはscoreから導く量 | activationと必ず同じではない |

## 4. 競争・連合・共有

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Competition | 候補同士のせめぎ合い | 同一group内の抑制・正規化等による相互作用 | 学習競争だけを指さない |
| Hard WTA | 一位以外を消す | Winner-Take-All | SparkBrainの標準ではない |
| Winner-Take-Most | 勝者を強めつつ敗者も少し残す | loser recoveryを許すsoft competition | 全候補を平等に残すことではない |
| Coalition | 同じ暫定内容を支える一時的な連合 | 仮説中心のSpark集合と証拠部分グラフ | 永続する固定モジュール |
| Coalition Score | 連合がどれだけ有力か | activation、support、多様性、安定、反証等の合成値 | 真実の確率そのものとは限らない |
| Source Diversity | 異なる証拠経路の数 | 重複IDを除いたsource数等の近似 | 真の独立性の証明ではない |
| Temporal Stability | 一定期間支持が続くこと | 連続評価回数や時間幅で測る | 永久に変わらないことではない |
| Ignition | 有力なCoalitionを全体共有へ上げる門 | score、margin、多様性、安定性等を満たしたgate event | 意識が発生した証明 |
| Margin | 一位と二位の差 | top Coalition scoreとrunner-upとの差 | 絶対的な正しさではない |
| No-Ignition | まだ判断しない状態 | 条件を満たすCoalitionがない正式な状態 | クラッシュ、無応答、文字列の「不明」 |
| Global Workspace | 重要内容を限られた範囲で共有する場 | 容量制限つきbroadcast state | 全部を決める中央司令官 |
| Broadcast | Workspace内容を複数機能へ送る | 内部eventとしてmemory/action等へ伝播 | 外部証拠の追加ではない |

## 5. 変更・記憶・学習

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Belief Revision | 現在の判断を新証拠で変える | Workspaceの有効仮説が時間発展で置換されること | 単なる文章の言い換えではない |
| Necessary Revision | 変えるべき時に変える | 世界変化や十分な反証に対応した更新 | 速ければ常に良いわけではない |
| Unnecessary Revision | 変えなくてよいのに変える | ノイズ等による誤更新 | 正常な柔軟性ではない |
| Recovery | 負けた仮説が再び戻る | residual beliefが後続証拠で再Ignitionする | 過去仮説が必ず正しいことではない |
| Working Memory | 短時間残る作業状態 | residual activityやWorkspace保持 | 永続記憶ではない |
| Episodic Memory | 出来事の記憶 | 状況、イベント列、判断、結果のまとまり | 現在は将来機能 |
| Semantic Memory | 一般化された知識 | 再利用可能なSpark群や接続構造 | 現在は将来機能 |
| Plasticity | 経験で構造や状態が変わる性質 | 重み、閾値、routing、Spark構造等の更新 | 何でも自由に変わることではない |
| Eligibility Trace | 直前の判断に関与した接続の印 | 後から報酬を割り当てるための減衰状態 | 証拠traceとは別 |
| Reward Modulation | 成功・失敗を学習へ反映 | rewardとeligibilityから重みを更新 | 報酬だけで知能が完成するわけではない |
| Structural Plasticity | 接続やSpark構造自体を変える | edge作成・剪定、Spark分割・統合等 | 現在は将来機能 |
| Emergent Organ | 学習から機能群が形成されること | クラスタと因果介入の両方で機能分化を確認 | 見た目の群だけで器官と断定しない |

## 6. 疎な処理と実装

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Routing | 入力を関係するSparkへ送る | eventから対象Sparkを選択する処理 | ネットワーク通信だけではない |
| Top-k | 上位k個だけ選ぶ | 関連度score上位の固定個数をactiveにする | 最適性を保証しない |
| Sparse | 全体の一部だけが活動する | active node/edgeが全体より十分少ない状態 | 自動的に高速・省電力とは限らない |
| Event-Routed | イベント対象と近傍だけ更新する | priority queue / active setによる局所実行 | 専用ハードウェアが必須という意味ではない |
| Dense Execution | 全体をまとめて計算する | 多数または全Sparkを毎step更新 | 常に悪い方式という意味ではない |
| Rate-Based | spikeではなく連続値で活動を表す | activation実数値による参照実装 | 生物学的に正確とは限らない |
| Spiking | 離散的な発火イベントで表す | LIF等を用いたローカルSNN simulation | 専用チップの利用と同義ではない |
| Backend | 同じ理論を動かす実装方式 | reference、PyTorch、SNN等の交換可能層 | 完全に同じ性能を保証しない |

## 7. 観察・検証

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Trace | 内部で何が起きたかの記録 | state、event、causal path等の時系列 | 解釈の完全な証明ではない |
| Checkpoint | 途中状態の保存 | queue、RNG、Spark、Workspace等を含む再開可能状態 | traceと同じではない |
| Replay | 保存記録を再生する | dynamicsを再計算せずtraceを閲覧 | 新しい結果の生成ではない |
| Deterministic | 同条件なら同結果になる | seed、queue順序、状態保存を固定 | 現実世界が決定論的という主張ではない |
| Baseline | 比較の基準モデル | 単純方式または既存方式 | わざと弱い相手だけでは不十分 |
| Ablation | 部品を外して効果を見る | residualなし等の切除実験 | 単なる機能削除ではなく因果検証 |
| Benchmark | 同条件で比較する実験 | data、seed、metric、budgetを固定した評価 | 一つで一般知能を測れるわけではない |
| Calibration | 自信と実正答率の一致 | confidence bin等で評価 | accuracyと同一ではない |
| Pareto Frontier | 複数目標の優良な境界 | 一方を改善すると他方が悪化する非支配解集合 | 単一ランキングではない |
| Falsifiability | 間違いと判定できること | 棄却条件を事前に明文化する性質 | 理論を否定すること自体が目的ではない |
| Functional Mimicry | 選んだ認知機能を再現する | 判断・記憶・反転等の機能模倣 | 生物学的忠実性 |
| Computational-Principle Mimicry | 計算原理を似せる | sparse、event、recurrence、興奮抑制等 | 神経学的等価性 |

## 8. ローカル実行

| 用語 | やさしい説明 | 本プロジェクトでの意味 | 注意 |
|---|---|---|---|
| Local-Only | 一台の自分のPCで完結する | 実行、保存、UI、実験、比較に外部サービスを必須としない | Python標準ライブラリだけという意味ではない |
| Offline-Capable | ネットを切っても動く | 依存導入後の主要実行が外部通信なしで成立 | 初回パッケージ取得まで禁止する意味ではない |
| CPU Reference Path | GPUなしで動く基準実装 | 正しさと説明可能性の標準経路 | 大規模学習が高速という意味ではない |
| Localhost UI | 自分のPCだけで開く画面 | 127.0.0.1または静的HTMLで動くVisualizer | 公開Webサービスではない |
| Dedicated Hardware Track | 専用チップ等の別研究 | コア完成後のExtension H | コア成果物の必須条件ではない |

## 9. v0.3の知覚・証跡・統合境界

| 用語 | やさしい説明 | 厳密な扱い | 注意 |
|---|---|---|---|
| Raw / Local Sensory Sample | ローカルで受け取る観測値 | `SensorySample` の明示的な時刻・source・modality・values | 正解ラベルや評価者truthを含めてよいわけではない |
| Sensory Field | 反復を抑え変化やgoalに反応する入口 | habituation、novelty、prediction error、bounded goal biasを記録する処理 | 全input inspectionや電力が疎になる主張ではない |
| Perceptual Spark | Sensory Fieldが発行する知覚上の活動単位 | accepted/suppressedを含むversioned record | 人間の感覚細胞ではない |
| Evidence Identity | 同じ証拠を重複計上しないためのID | source、correlation group、lineage、entity scopeを伴うrecord | 独立証拠であることをIDだけから推論しない |
| Entity Scope | 証拠がどの対象に属するか | E0/E1/E2を区別するbinding contract | E1 oracle bindingは自律発見ではない |
| Proto-concept Candidate | 反復patternの再利用候補 | label-free candidate observation | 意味概念や因果的有用性を意味しない |
| Functional Organ Candidate | 機能群かもしれない候補 | structure、reuse、causal controlで別途評価する対象 | C17のnegative結果を器官形成と呼ばない |
| v0.3 Trace / Fork | 明示状態のhash連鎖と分岐記録 | schema `0.3` のcheckpoint/replay contract | C18手動traceはlive統合runtimeの証拠ではない |
| IntegratedV03Brain | 将来の統合backend名 | `sparkbrain.v03` の明示的versioned facade | 現時点で統合人工脳が完成した意味ではない |
