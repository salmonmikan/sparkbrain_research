# SparkBrain Research Prototype v0.2

SparkBrain は、局所的で持続的な活動単位 **Spark** が、イベントに応じて発生・減衰・発火・競争・連合し、十分に安定した Coalition のみが Global Workspace に昇格する、脳型情報処理の研究プロトタイプです。

本リポジトリは、次の二つを同時に進めるための基盤です。

1. Spark を基礎単位とする動的認知モデルの理論形成
2. 内部状態をリアルタイム観察・操作・比較できる人工脳実験環境の実装

> **重要:** 現在の v0.2 は「人間の脳を再現したシステム」ではありません。手書きの証拠経路を使った、rate-based・event-driven な機能実証です。生物学的等価性、意識、汎用知能、ハードウェア上の省電力性は未実証です。

## 現在できること

- Spark の活動値、閾値、減衰、refractory、homeostasis
- 興奮性・抑制性接続
- 外部証拠の支持・矛盾履歴
- soft winner-take-most 型の仮説競争
- 複数証拠からの Coalition score
- threshold・margin・stability・source diversity による Ignition
- Global Workspace broadcast
- 棄却候補を完全消去しない residual state
- reward-modulated eligibility による最小限の可塑性
- 構成・グラフ値の検証、JSON checkpoint、決定論的再開
- dynamicsを再実行しないtrace replay
- versioned JSON Schema（config / trace / state）
- SwitchWorld における belief 維持・変更・復帰
- 自己完結型 HTML Visualizer
- accumulator / hard-WTA / instant classifier との Phase-0 比較
- 再現可能な trace、JSON、CSV、Markdown report

## すぐ動かす

Python 3.11 以上を使用します。コア実装に外部依存はありません。

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"

python scripts/run_demo.py
python scripts/checkpoint_demo.py
python scripts/replay_trace.py
python scripts/run_benchmark.py --episodes 50 --steps 30
python scripts/validate_bundle.py
pytest
```

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

`visualizer.html` はサーバー不要で、そのままブラウザで開けます。

## リポジトリ構成

```text
sparkbrain_research_v0_2/
├── docs/
│   ├── PROJECT_CHARTER.md
│   ├── THEORY_SPEC_v0.2.md
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
│   ├── baselines.py
│   ├── metrics.py
│   ├── benchmark.py
│   ├── visualizer.py
│   ├── serialization.py
│   ├── replay.py
│   ├── protocols.py
│   └── validation.py
├── schemas/
├── scripts/
├── tests/
└── artifacts/
```

## 現在の研究上の主張

現段階で主張できるのは、次の範囲だけです。

> 持続する複数仮説、証拠の連合、明示的な ignition gate、敗者の residual retention を備えたイベント駆動状態系を、通常の Python だけで実装・観察・反証可能な形にできる。

まだ主張できないこと:

- Transformer / GRU / RIM より一般に高性能である
- 真の計算量・消費電力が少ない
- 器官が自律的に形成される
- Spark dynamics が脳の神経活動を正確に再現する
- 意識が生じる

## 研究の到達条件

このプロジェクトの最終成果物は単一アプリではなく、以下の整合した成果物群です。

1. Theory Specification
2. Reference Engine
3. Brain Simulator / Test Worlds
4. Brain Visualizer
5. Experimental Suite
6. Matched Baselines and Ablations
7. Reproducible Benchmark Report
8. Spiking / neuromorphic backend
9. Codex implementation handoff and audit trail

詳細は `docs/PROJECT_CHARTER.md` と `docs/MASTER_ROADMAP.md` を参照してください。

## 名称

`SparkBrain` はプロジェクトのコードネームです。理論名と略称は未確定です。`SFA` は別分野でも使われるため、公開前に先行商標・論文・パッケージ名を確認して正式決定します。
