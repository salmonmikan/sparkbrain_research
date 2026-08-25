# SparkBrain Research Prototype v0.2.1

SparkBrainは、局所的で持続的な活動単位 **Spark** が、イベントに応じて発生・減衰・発火・競争・連合し、十分に安定したCoalitionだけがGlobal Workspaceへ昇格する、脳型情報処理の研究プロトタイプです。

本リポジトリは、次の二つを同時に進めるための基盤です。

1. Sparkを基礎単位とする動的認知モデルの理論形成
2. 内部状態をリアルタイム観察・操作・比較できる人工脳実験環境の実装

> **v0.2.1の正式条件:** コア成果物は、一台の一般的なローカルPCで完結させます。CPU参照実装を必須とし、実行時のクラウドサービス、遠隔LLM API、外部DB、SaaSログインを必要としません。専用ニューロモーフィックハードウェアは別枠のExtension Hです。

> **重要:** 現在のv0.2.1は「人間の脳を再現したシステム」ではありません。手書きの証拠経路を使った、rate-based・event-drivenな機能実証です。生物学的等価性、意識、汎用知能、既存モデルへの一般的優位性、実ハードウェア上の省電力性は未実証です。

## 初めて読む場合

この順で読むと理解しやすいです。

1. [`docs/START_HERE.md`](docs/START_HERE.md)
2. [`docs/FOUNDATIONS_FOR_BEGINNERS.md`](docs/FOUNDATIONS_FOR_BEGINNERS.md)
3. [`docs/GLOSSARY.md`](docs/GLOSSARY.md)
4. [`docs/THEORY_SPEC_v0.2.1.md`](docs/THEORY_SPEC_v0.2.1.md)

完成条件は [`docs/PROJECT_CHARTER.md`](docs/PROJECT_CHARTER.md)、ローカル制約は [`docs/LOCAL_EXECUTION_POLICY.md`](docs/LOCAL_EXECUTION_POLICY.md) にあります。

## SparkBrainを一文で

> 多数の小さな活動単位が、外界の証拠に反応し、競争し、協力し、時間とともに弱まり、必要なら過去の敗者が復活することで、判断・記憶・行動を形成する仕組みを、ローカルPC上で観察・介入・反証できる形にする研究です。

## 現在できること

- Sparkの活動値、閾値、減衰、refractory、homeostasis
- 興奮性・抑制性接続
- 外部証拠のID、source、支持・矛盾履歴
- soft winner-take-most型の仮説競争
- 複数証拠からのCoalition score
- threshold、margin、stability、source diversityによるIgnition
- No-Ignitionを正式な未解決状態として保持
- Global Workspace broadcast
- 棄却候補を完全消去しないresidual state
- reward-modulated eligibilityによる最小限の可塑性
- 構成・グラフ値の検証、JSON checkpoint、決定論的再開
- dynamicsを再実行しないtrace replay
- versioned JSON Schema（config / trace / state）
- SwitchWorldにおけるbelief維持・変更・復帰
- 外部通信を必要としない自己完結型HTML Visualizer
- accumulator / hard-WTA / instant classifierとのPhase-0比較
- 再現可能なtrace、JSON、CSV、Markdown report
- ローカル完結条件を検査するreadiness checker
- loopback限定でpause/step/reset、介入fork、比較、blind export/importを行うBrain Lab
- pinned Belief-R全testをofflineで評価するC06 adapter、記号的非単調stream、target-blind変換、負の外部評価結果

## ローカルで動かす

Python 3.11以上を使用します。決定論的なコア参照実装のruntime dependencyはゼロです。開発・検証用の依存だけをoptional dependencyとして導入します。

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

依存パッケージがすでにローカルへ導入済みで、ビルド時の外部取得も避けたい場合は、次を利用できます。

```bash
python -m pip install -e . --no-build-isolation
```

まずローカル条件を確認します。

```bash
python scripts/local_readiness_check.py
```

続けてデモと検証を実行します。

```bash
python scripts/run_demo.py
python scripts/checkpoint_demo.py
python scripts/replay_trace.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python -m pytest -q
python scripts/validate_bundle.py
```

対話型Brain Labはoptional extraとして起動します。

```bash
python -m pip install -e ".[lab]"
python scripts/run_brain_lab.py
```

既定URLは `http://127.0.0.1:8765` です。UI assetは同梱され、CDN、外部API、analyticsを使いません。操作、画面、介入、blind mode、artifact、性能境界は [`docs/BRAIN_LAB.md`](docs/BRAIN_LAB.md) を参照してください。

C06の外部評価基盤、Belief-Rのtest-only/ライセンス境界、取得・offline検証手順は
[`docs/EXTERNAL_VALIDATION.md`](docs/EXTERNAL_VALIDATION.md)、負の公式実測結果は
[`docs/C06_EXTERNAL_VALIDATION_RESULTS.md`](docs/C06_EXTERNAL_VALIDATION_RESULTS.md) を参照してください。

C10の再現検証は、Git履歴を検査できるrepository modeと、`.git`を含まない配布物を
固定metadataとmanifestで検査するarchive modeを分離しています。どちらも同じ限定的な
primary smoke subsetを再生成するもので、C02–C08のfull evaluationの代替ではありません。
archive modeでは、改変・欠落・予期しないファイル・revision不一致をowner license blockerと
分離してfail-closedに判定します。展開直後のpristine integrity検証を済ませてからruntime
pytestへ進む二段階契約で、利用者がbytecodeやpytest cache用の環境変数を手動設定する必要は
ありません。
手順は [`docs/CLEAN_ROOM_REPRODUCTION.md`](docs/CLEAN_ROOM_REPRODUCTION.md) を参照してください。
private review ZIPは `scripts/build_review_bundle.py` が専用manifestと外部SHA-256を生成します。
これはpublic releaseではなく、プロジェクトライセンスのowner decisionを解除しません。

生成物:

```text
artifacts/demo/visualizer.html
artifacts/demo/trace.json
artifacts/demo/summary.json
artifacts/demo/checkpoint.json
artifacts/benchmarks/benchmark_report.md
artifacts/benchmarks/benchmark_aggregate.csv
artifacts/benchmarks/benchmark_results.json
```

`artifacts/demo/visualizer.html`はサーバー不要で、そのままブラウザで開けます。外部CDNや外部APIへ接続しません。

## ローカル完結の意味

必須:

- 一台の汎用PCで実行
- CPU参照経路
- ローカルファイルへの保存
- 静的HTMLまたはlocalhost UI
- 依存導入後のオフライン実行
- 外部APIなしの標準実験

任意:

- ローカルGPU
- PyTorch / PyTorch Geometric
- Norse / snnTorch / Nengo / Brian2によるローカルSNN simulation
- Docker

別枠:

- Loihi等の専用ニューロモーフィックハードウェア
- FPGA / ASIC
- クラウドGPU・分散学習
- 実消費電力測定

詳細は [`docs/LOCAL_EXECUTION_POLICY.md`](docs/LOCAL_EXECUTION_POLICY.md) を参照してください。

## リポジトリ構成

```text
sparkbrain_research_v0_2/
├── README.md
├── CHANGELOG.md
├── docs/
│   ├── START_HERE.md
│   ├── FOUNDATIONS_FOR_BEGINNERS.md
│   ├── GLOSSARY.md
│   ├── LOCAL_EXECUTION_POLICY.md
│   ├── PROJECT_CHARTER.md
│   ├── THEORY_SPEC_v0.2.1.md
│   ├── PRIOR_ART_GAP_ANALYSIS.md
│   ├── SOFTWARE_ARCHITECTURE.md
│   ├── EXPERIMENT_PROTOCOL.md
│   ├── MASTER_ROADMAP.md
│   ├── CODEX_EXECUTION_BRIEF.md
│   ├── DECISION_LOG.md
│   └── SOURCES.md
├── src/sparkbrain/
│   ├── model.py
│   ├── engine.py
│   ├── worlds.py
│   ├── baselines/        # classic, probabilistic, bounds, optional neural baselines
│   ├── metrics.py
│   ├── benchmark.py
│   ├── visualizer.py
│   ├── serialization.py
│   ├── replay.py
│   ├── protocols.py
│   └── validation.py
├── schemas/
├── scripts/
│   └── local_readiness_check.py
├── tests/
├── artifacts/
└── archive/
```

## 現在の研究上の主張

現段階で主張できるのは次の範囲です。

> 持続する複数仮説、証拠の連合、明示的なIgnition gate、敗者のresidual retentionを備えたイベント駆動状態系を、通常のPythonだけで実装・観察・反証可能な形にできる。

まだ主張できないこと:

- Transformer / GRU / RIMより一般に高性能である
- 真の計算量・消費電力が少ない
- 器官が自律的に形成される
- Spark dynamicsが脳の神経活動を正確に再現する
- 意識が生じる
- 自由な自然言語から自律的に概念形成できる

## Phase-0の予備結果

現在の手書きSwitchWorldでは、完全版SparkBrainのall-step accuracyは約0.640で、単純accumulatorの約0.628と近い結果です。residualを外すと現設定では大きく低下しますが、これは一般的優位性の証明ではありません。

つまり現時点では、

- residualが現在のシナリオで効いている
- 即時判断と安定性にはトレードオフがある
- 単純方式が依然として競争力を持つ

という仮説生成段階です。

詳細は [`artifacts/benchmarks/benchmark_report.md`](artifacts/benchmarks/benchmark_report.md) と [`docs/RESULTS_LEDGER.md`](docs/RESULTS_LEDGER.md) にあります。

## 最終到達条件

コアの最終成果物は単一アプリではなく、次の整合した成果物群です。

1. Theory Specification
2. Python Reference Engine
3. Brain Simulator / Test Worlds
4. Local Brain Visualizer / Brain Lab
5. Experimental Suite
6. Matched Baselines and Ablations
7. Learned Routing and Local Spiking Simulation
8. Reproducible Benchmark Report
9. Local Reproduction Package
10. Codex implementation handoff and audit trail

専用ハードウェアはここに含めません。

研究上の着地点は、**Spark型動的認知モデルを、数理的・反証可能で、ローカル実装と一対一に対応する計算理論として完成させること**です。

## バージョン互換性

- package / documentation version: `0.2.1`
- persisted config / state / trace schema: `0.2`
- Phase-0 dynamics: v0.2から意図的変更なし

v0.2.1は、ローカル条件と説明文書を追加したpatch releaseです。v0.2のcheckpointとtraceを互換対象として維持します。

## Codexへ続きを依頼する

最初の依頼文:

```text
Use $sparkbrain-research. Read AGENTS.md, docs/LOCAL_EXECUTION_POLICY.md,
docs/PROJECT_STATUS.md, and docs/CODEX_EXECUTION_BRIEF.md.
Execute C01 from docs/codex/C01_ENGINE_HARDENING.md completely.
Preserve the local-only contract, run the local readiness check and all
acceptance tests, update the status/results/decision documents, and do not
start dependent tasks.
```

詳細な順序と各タスクの受入条件は [`docs/CODEX_EXECUTION_BRIEF.md`](docs/CODEX_EXECUTION_BRIEF.md) と [`docs/codex/`](docs/codex/) にあります。

## 名称

`SparkBrain`はプロジェクトのコードネームです。理論名と略称は未確定です。`SFA`は別分野でも使われるため、公開前に先行商標・論文・パッケージ名を確認して正式決定します。
