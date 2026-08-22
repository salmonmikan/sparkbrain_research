# SparkBrain Project Charter

## 1. 目的

多数の局所的・持続的活動単位 Spark が、並列的なイベント処理、興奮、抑制、再帰、競争、連合、減衰、再活性化および学習によって認知状態を形成する計算理論を定義し、その理論を観察・操作・比較・反証可能なソフトウェアとして実装する。

## 2. 最終成果物

### D1. Theory Specification

Spark、Event、Connection、Organ、Coalition、Ignition、Workspace、Memory、Learning、Brain State の形式定義、数式、状態遷移、不変条件、反証条件を含む。

### D2. Reference Engine

理論に最も忠実で、読みやすく決定論的な Python 実装。性能より説明可能性を優先し、全状態を trace できること。

### D3. Brain Simulator

外界、時間、センサー、ノイズ、状態変化、行動、報酬を持つ複数の Test World 上で、連続的に人工認知系を動かせること。

### D4. Brain Visualizer

最低限、次を時間軸上で観察できること。

- Spark の生成・活動・減衰・発火
- 興奮性・抑制性伝播
- 仮説間競争
- Coalition の構成、score、安定性、矛盾
- Ignition と Global Workspace
- belief の維持、棄却、反転、復帰
- 記憶形成、接続強度変化、器官・群の形成

### D5. Experimental Suite

SwitchWorld、belief revision、noise robustness、delayed evidence、multi-hop relation、partial observability、continual adaptation を再現可能な seed 付きで実行する。

### D6. Baseline / Ablation Suite

少なくとも次と公平に比較する。

- Evidence accumulator
- Hard winner-take-all
- GRU
- Small Transformer
- RIM または modular recurrent baseline
- SparkBrain without residual
- SparkBrain without coalition
- SparkBrain without inhibition
- Dense-execution SparkBrain

### D7. Benchmark Report

Accuracy だけでなく、revision precision / recall、switch latency、false ignition、unnecessary revision、recovery、calibration、active-node ratio、edge evaluations、wall-clock、memory、energy proxy を報告する。

### D8. Learned and Spiking Backends

手書き routing を学習可能な routing / graph dynamics に置換し、その後 rate-based と同等の振る舞いを Norse / snnTorch / Nengo 等で再現する。neuromorphic hardware 上の実測は独立した最終段階とする。

### D9. Reproducibility and Handoff

環境固定、実験設定、seed、raw results、生成レポート、Codex向け詳細指示、未解決事項、否定的結果を残す。

## 3. 研究上の中心仮説

### H1: Evidence coalition

独立した複数の弱い証拠を Coalition として統合すると、単一強信号や単純加算より false ignition を抑えながら判断できる。

### H2: Residual loser state

敗者仮説を完全消去せず減衰状態で保持すると、世界状態が再び変化した際の recovery latency が短くなる。

### H3: Stability–plasticity

soft competition、contradiction、stability gate を組み合わせることで、ノイズに対する安定性と決定的反証への可塑性の Pareto frontier を改善できる。

### H4: Persistent explicit belief

複数の競合 belief を first-class state として保持すると、逐次入力に対する非単調推論と監査可能性が改善する。

### H5: Execution sparsity

全 Spark を毎tick評価せず、event routing と active-neighborhood のみを処理しても、H1–H4 の挙動を維持できる。

### H6: Emergent organ specialization

routing、local learning、structural plasticityを導入した場合、固定器官を指定しなくても再利用可能な機能群が形成される可能性がある。

H6 は高リスク仮説であり、v0.x の成立条件には含めない。

## 4. 非目標

少なくとも初期段階では、次を目標にしない。

- 人間脳の解剖学的完全再現
- 意識の存在証明
- AGI の達成宣言
- LLM の全面置換
- GPU上のwall-clockだけによる省電力性の主張
- ベンチマーク一つだけを根拠にした優位性主張

## 5. 完成レベル

### Level A — Functional demonstrator

- 形式仕様と実装の対応が追跡可能
- belief維持、反転、復帰を可視化
- deterministic tests が通る
- baseline / ablation が再現可能

### Level B — Learnable cognitive architecture

- routing と dynamics の一部をデータから学習
- 未知のイベント組合せへ一般化
- matched-parameter neural baselines と比較
- calibration と計算量を報告

### Level C — Brain-like computational substrate

- spike/event dynamics に置換
- rate-based 版との挙動対応を確認
- neuromorphic backend で実行
- 実消費エネルギーとレイテンシを測定

### Level D — Theory established

- 用語と公理が安定
- 複数タスクで予測が再現
- 失敗条件と適用境界が明文化
- 独立再実装または外部レビューで再現
- 先行研究との差分を過大主張せず説明可能

## 6. v0.2 現在地

| 項目 | 状態 | 備考 |
|---|---|---|
| Theory draft | 部分完成 | 形式定義と仮説を文書化 |
| Rate-based engine | 完成 | 標準ライブラリのみ |
| Event queue | 完成 | 決定論的 priority queue |
| Coalition / ignition | 完成 | 手書きルール |
| Residual belief | 完成 | canonical testで復帰確認 |
| Visualizer | 完成 | 自己完結HTML |
| SwitchWorld | 完成 | canonical + random episode |
| Phase-0 baseline | 完成 | scalar baselinesのみ |
| Learned routing | 未着手 | Codex Task C1 |
| GRU/Transformer/RIM | 未着手 | Codex Task C2 |
| Rich web UI | 未着手 | Codex Task C3 |
| Spiking backend | 未着手 | Codex Task C4 |
| Structural plasticity | 未着手 | Codex Task C5 |
| External datasets | 未着手 | Codex Task C6 |
| Scientific novelty confirmation | 継続 | systematic reviewが必要 |

## 7. ガバナンス

- 実装結果と理論上の主張を分離する。
- 「動いた」は「一般化した」を意味しない。
- 「疎なアルゴリズム」は「省電力ハードウェア」を意味しない。
- 期待に反する結果も raw data とともに保存する。
- 先行研究と重なる部分を新規性として扱わない。
- theory spec を変更した場合、対応する test と decision log を同時更新する。
