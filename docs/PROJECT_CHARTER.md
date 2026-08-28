# SparkBrain Project Charter — v0.3 research boundary

## v0.3 status boundary

The current package is `0.3.2.dev0`. The v0.3.2 additions are corrective engineering APIs and do
not change the accepted v0.3.1 scientific boundary.
The legacy persisted schema remains `0.2`, while C18 owns an additive explicit schema `0.3`.
C11--C18 are accepted only at their individual registered boundaries. C19 is blocked and not
evaluated. The integrated v0.3 runtime and live Brain Lab are accepted as engineering evidence,
not evidence that a scientifically supported integrated artificial brain already exists.

## 1. 目的

多数の局所的・持続的活動単位 Spark が、並列的なイベント処理、興奮、抑制、再帰、競争、連合、減衰、再活性化および学習によって認知状態を形成する計算理論を定義し、その理論を観察・操作・比較・反証可能なソフトウェアとして実装する。

コア成果物は、**一台の一般的なローカルコンピューター上で完結すること**を正式条件とする。専用ハードウェア、クラウド推論、遠隔APIは完成要件に含めない。

## 2. 最終成果物

### D1. Theory Specification

Spark、Event、Connection、Organ、Coalition、Ignition、Workspace、Memory、Learning、Brain State の形式定義、数式、状態遷移、不変条件、反証条件を含む。

形式仕様と平易な説明を分離しつつ対応づける。

- 厳密な仕様: `THEORY_SPEC_v0.3.md`
- legacy reference specification: `THEORY_SPEC_v0.2.1.md`
- 入門解説: `FOUNDATIONS_FOR_BEGINNERS.md`
- 用語単位の説明: `GLOSSARY.md`

### D2. Local Reference Engine

理論に最も忠実で、読みやすく決定論的な Python 実装。性能より説明可能性を優先し、全理論状態をtraceできること。

必須条件:

- Python 3.11以降
- CPUのみで標準動作
- 外部API不要
- ローカルファイルへ保存
- セットアップ後はオフライン実行可能

### D3. Brain Simulator

外界、時間、センサー、ノイズ、状態変化、行動、報酬を持つ複数のTest World上で、人工認知系を連続的に動かせること。

### D4. Local Brain Visualizer / Brain Lab

最低限、次を時間軸上で観察できること。

- Sparkの生成・活動・減衰・発火
- 興奮性・抑制性伝播
- 仮説間競争
- Coalitionの構成、score、安定性、矛盾
- IgnitionとGlobal Workspace
- beliefの維持、棄却、反転、復帰
- 記憶形成、接続強度変化、器官・群の形成

UIは静的HTMLまたはlocalhost上で動作し、外部CDNやSaaSを必須としない。

The existing `/api/runs*` Brain Lab is the legacy v0.2 reference UI. A v0.3 runtime must use an
explicit versioned API, preserve the legacy surface, and derive trace data from a live runtime
rather than treating the C18 manual trace artifact as live-brain evidence.

### D5. Experimental Suite

SwitchWorld、belief revision、noise robustness、delayed evidence、multi-hop relation、partial observability、continual adaptationを再現可能なseed付きで実行する。

### D6. Baseline / Ablation Suite

少なくとも次と公平に比較する。

- Evidence accumulator
- Bayesian / HMM where applicable
- Hard winner-take-all
- GRU
- Small Transformer
- RIMまたはmodular recurrent baseline
- SparkBrain without residual
- SparkBrain without coalition
- SparkBrain without inhibition
- Dense-execution SparkBrain

### D7. Benchmark Report

Accuracyだけでなく、revision precision / recall、switch latency、false ignition、unnecessary revision、recovery、calibration、active-node ratio、edge evaluations、wall-clock、memoryを報告する。

algorithmic activityと実消費電力を分離し、専用ハードウェアなしにenergy efficiencyを主張しない。

### D8. Local Learned and Spiking Backends

手書きroutingを学習可能なrouting / graph dynamicsへ置換し、その後rate-basedと同等の振る舞いを、同一ローカルPC上のPyTorch、Norse、snnTorch、Nengo等で再現する。

CPU参照経路を維持し、GPUは任意とする。

### D9. Reproducibility and Handoff

環境固定、実験設定、seed、raw results、生成レポート、Codex向け詳細指示、未解決事項、否定的結果を残す。

ローカルの一連コマンドだけで主要結果を再生成できること。

## 3. 独立拡張成果物

### XH1. Dedicated Hardware Validation

Loihi、FPGA、ASIC、専用アクセラレータへの写像、実消費電力、実レイテンシ測定は、コア完成後の独立研究とする。

XH1が未実施でも、D1〜D9が成立すればコアプロジェクトは完成とみなす。

## 4. 研究上の中心仮説

### H1: Evidence coalition

独立した複数の弱い証拠をCoalitionとして統合すると、単一強信号や単純加算よりfalse ignitionを抑えながら判断できる。

### H2: Residual loser state

敗者仮説を完全消去せず減衰状態で保持すると、世界状態が再び変化した際のrecovery latencyが短くなる。

### H3: Stability–plasticity

soft competition、contradiction、stability gateを組み合わせることで、ノイズに対する安定性と決定的反証への可塑性のPareto frontierを改善できる。

### H4: Persistent explicit belief

複数の競合beliefをfirst-class stateとして保持すると、逐次入力に対する非単調推論と監査可能性が改善する。

### H5: Execution sparsity

全Sparkを毎tick評価せず、event routingとactive neighborhoodのみを処理しても、H1〜H4の挙動を維持できる。

### H6: Emergent organ specialization

routing、local learning、structural plasticityを導入した場合、固定器官を指定しなくても再利用可能な機能群が形成される可能性がある。

H6は高リスク仮説であり、v0.xの最低成立条件には含めない。

## 5. 非目標

少なくともコア研究では、次を目標にしない。

- 人間脳の解剖学的完全再現
- 意識の存在証明
- AGIの達成宣言
- LLMの全面置換
- クラウドサービスを前提にした製品化
- 専用ハードウェアを完成条件にすること
- GPU上のwall-clockだけによる省電力性の主張
- ベンチマーク一つだけを根拠にした優位性主張

## 6. 完成レベル

### Level A — Local functional demonstrator

- 形式仕様と実装の対応が追跡可能
- belief維持、反転、復帰を可視化
- deterministic testsが通る
- baseline / ablationが再現可能
- CPUとローカルファイルだけで標準デモを実行

### Level B — Local learnable cognitive architecture

- routingとdynamicsの一部をデータから学習
- 未知のイベント組合せへ一般化
- matched-parameter neural baselinesと比較
- calibrationと計算量を報告
- 小規模学習設定をCPUで再現可能

### Level C — Local brain-like computational substrate

- rate-based版とローカルspiking simulation版を実装
- 事前定義した挙動対応を確認
- 複数Worldで連続稼働
- Brain Labから観察・介入・分岐・再生可能
- 専用ハードウェアなしで成立

### Level D — Theory established

- 用語と公理が安定
- 複数タスクで予測が再現
- 失敗条件と適用境界が明文化
- 独立再実装または外部レビューで再現
- 先行研究との差分を過大主張せず説明可能

### Extension H — Dedicated hardware validation

Level Dとは独立。実機へ移す場合のみ実施する。

## 7. v0.3 現在地

| 項目 | 状態 | 備考 |
|---|---|---|
| Theory v0.3 | working specification | v0.2.1 legacy definitions plus C11--C18 contracts |
| Beginner foundations | 完成 | 基礎理論を平易に説明 |
| Expanded glossary | 完成 | 主要用語の意味と非含意を整理 |
| Local-only policy | 完成 | コア完成条件へ固定 |
| Rate-based engine | 完成 | 標準ライブラリのみ |
| Event queue | 完成 | 決定論的priority queue |
| Coalition / ignition | 完成 | 手書きルール |
| Residual belief | 完成 | canonical testで復帰確認 |
| Visualizer | 完成 | 自己完結HTML |
| SwitchWorld | 完成 | canonical + random episode |
| Phase-0 baseline | 完成 | scalar baselinesのみ |
| Local readiness check | 完成 | 環境・依存・必須成果物の検査 |
| Learned routing | implemented | controlled evidence; no general claim upgrade |
| GRU/Transformer/RIM | implemented | reduced matched-baseline quality/compute boundary retained |
| Legacy local Brain Lab | accepted locally | v0.2 reference engine only |
| Live integrated v0.3 Brain Lab | engineering accepted | versioned runtime/API; no scientific claim upgrade |
| Local spiking backend | reduced hybrid boundary | broader equivalence remains open |
| Structural plasticity | completed negative result | C08 / C17 do not support organ formation |
| C19 external validation | blocked | truth-free adapter and new protocol required |
| Scientific novelty confirmation | 継続 | Codex C09 / systematic review |
| Dedicated hardware | 別枠 | Extension H。コア完成に不要 |

## 8. ガバナンス

- 実装結果と理論上の主張を分離する。
- 「動いた」は「一般化した」を意味しない。
- 「疎なアルゴリズム」は「省電力ハードウェア」を意味しない。
- 期待に反する結果もraw dataとともに保存する。
- 先行研究と重なる部分を新規性として扱わない。
- theory specを変更した場合、対応するtestとdecision logを同時更新する。
- コア機能へ外部API依存を追加しない。
- GPU専用経路を作る場合もCPU参照経路を残す。
- UIは外部ネットワークなしで動く配布形態を維持する。
