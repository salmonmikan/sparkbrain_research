# Start Here — SparkBrain v0.2.1

この文書は、SparkBrainを初めて読む人の入口です。

## SparkBrainを一文で

> 多数の小さな活動単位「Spark」が、証拠に反応し、競争し、協力し、時間とともに弱まり、ときには再び強くなることで、判断・記憶・行動を形成する仕組みを、ローカルPC上で観察可能なプログラムとして研究するプロジェクトです。

## 最初に理解しておくこと

SparkBrainは、現在のところ次ではありません。

- 人間の脳そのもの
- 意識を持つシステム
- 完成した汎用AI
- LLMより優れていると証明された方式
- 専用ハードウェアを必要とするプロジェクト

現在は、脳型の情報処理原理を、説明可能・反証可能な形で実装した研究プロトタイプです。

## 推奨する読み順

### まず全体像を知りたい

1. `docs/FOUNDATIONS_FOR_BEGINNERS.md`
2. `docs/GLOSSARY.md`
3. `README.md`

### 理論を確認したい

1. `docs/FOUNDATIONS_FOR_BEGINNERS.md`
2. `docs/THEORY_SPEC_v0.2.1.md`
3. `docs/HYPOTHESES_AND_FALSIFICATION.md`
4. `docs/PRIOR_ART_GAP_ANALYSIS.md`

### 実装を触りたい

1. `README.md`
2. `docs/LOCAL_EXECUTION_POLICY.md`
3. `docs/SOFTWARE_ARCHITECTURE.md`
4. `examples/minimal.py`
5. `src/sparkbrain/engine.py`

### Codexへ続きを依頼したい

1. `AGENTS.md`
2. `docs/CODEX_EXECUTION_BRIEF.md`
3. 対象の `docs/codex/Cxx_*.md`
4. `docs/codex/PROMPTS.md`

## 10分で見るデモ

Python 3.11以上を使います。

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

続けて:

```bash
python scripts/local_readiness_check.py
python scripts/run_demo.py
```

その後、次をブラウザで開きます。

```text
artifacts/demo/visualizer.html
```

画面では、各Sparkの活動値、仮説の競争、Coalition、Ignition、Workspaceへの昇格を時間順に確認できます。

## 最重要の考え方

一般的な一回の推論を、次のように表すことがあります。

```text
入力 → 巨大な計算 → 出力
```

SparkBrainが研究しているのは、次の形です。

```text
過去から残る内部状態
        ＋
新しく来たイベント
        ↓
一部のSparkだけが活動
        ↓
複数の仮説が競争
        ↓
証拠を共有するSparkがCoalitionを形成
        ↓
十分に強く安定した場合だけIgnition
        ↓
Workspaceへ共有
        ↓
記憶・行動・次の内部イベントへ
```

つまり、答えを一回で計算するというより、**内部状態が時間の中で変化し続けること自体を思考として扱う**のが中心です。

## v0.2.1で追加されたこと

- ローカルPC完結を正式な完成条件にした
- 専用ハードウェアを独立拡張トラックへ分離した
- 初学者向けの基礎理論ガイドを追加した
- 用語集を平易な説明つきで拡張した
- Codex指示にローカル実行制約を追加した
- ローカル準備状態を検査するスクリプトを追加した

## 迷ったときの基準

- 用語が分からない → `docs/GLOSSARY.md`
- 数式が分からない → `docs/FOUNDATIONS_FOR_BEGINNERS.md` の「数式の読み方」
- 何を完成とするか → `docs/PROJECT_CHARTER.md`
- ローカル条件の意味 → `docs/LOCAL_EXECUTION_POLICY.md`
- 現在どこまで動くか → `docs/PROJECT_STATUS.md`
- 次に何を作るか → `docs/MASTER_ROADMAP.md`
