# Brain Lab — localhost interactive experiment UI

Brain Labは、C01の決定論的な参照エンジンを、ローカルPC上で観察・介入・比較するC03の実験UIである。コア参照実装のruntime dependencyは増やさず、Web UI用の依存はoptional extra `lab` に分離する。

## 導入と起動

```bash
python -m pip install -e ".[lab]"
python scripts/run_brain_lab.py
```

既定URLは `http://127.0.0.1:8765` である。launcherはloopbackアドレスだけを受理し、`0.0.0.0` やLANアドレスへのbindを拒否する。認証、外部API、外部DB、analytics、CDN、hosted font、SaaS sessionは使わない。依存導入後はbundled HTML/CSS/JavaScriptだけでオフライン実行できる。

## 画面と視覚表現

単一画面に次の9領域を置く。

1. Brain Field: Sparkと接続の現在状態
2. Event Timeline: 外部event、予測、truth、内部edge、Ignition
3. Belief Panel: 現在のbeliefとNo-Ignition
4. Global Workspace: broadcast履歴とlistener
5. Spark / Connection / Coalition Inspector: activation、閾値、evidence provenance、接続、Coalition
6. Control Bar: seed、速度、blind、start、pause、step、run、reset、event注入
7. Intervention Panel: Spark/edge/organ/thresholdへの介入
8. Comparison View: 親runとforkを同じframe indexで比較
9. Export / Import: local JSON bundleの保存、取得、再読込

色は機能種別、明度と大きさはactivation、ringはfiring、破線はinhibition、edge highlightは伝播、group outlineはCoalition、Workspace転送はIgnitionを表す。これは機能図であり、生物学的な解剖配置を意味しない。No-Ignitionは欠損表示ではなく明示的な未解決状態である。

キーボードでは `Space` が1 step、`P` がpauseである。focus indicator、skip link、live status、labelを備える。色だけに依存せず、テキストと線種を併用する。

## 実行制御と決定論

- `step` はcanonical SwitchWorldの外部eventを正確に1件処理する。
- `pause` は状態を進めない。SSE接続と再接続も状態を進めない。
- `reset` は同じseed、同じイベント列、同じ介入なら同じtraceへ戻る。
- event注入は既知のSpark ID、有限の時刻と値、上限内の文字列だけを受理する。
- state表示にはpure inspectionを使い、観察自体でtraceやcounterを変えない。

## 介入とfork

介入は親runのcheckpointから子runを作り、親を変更しない。子runは親run ID、fork時checkpoint hash、介入patchを保持する。

対応patch:

- edge ablation / weight edit
- Spark clamp / ablation
- organ suppression
- Spark threshold edit

comparisonは共通のframe indexを選び、親・子のbelief、Ignition、Workspace、work counterを同期表示する。異なる長さでは短い側の最終frameを再利用せず、そのrunに存在する同じindexだけを返す。

## Blind mode

blind modeではUI、state API、trace、export bundleの全階層から `truth` を除外し、値を `null` にする。seedとイベント列は維持されるため、介入と予測の再現性は失わない。import時もblind bundleからtruthを復元しない。

## Export / Importと保存先

export bundleはschema version、run metadata、event manifest、checkpoint、trace、figure dataを含む。既定の保存先は次である。

```text
artifacts/brain_lab/runs/<run_id>/brain_lab_export.json
```

artifact root外へのpath指定は受け付けない。importは25 MiB上限とschema検証を行い、新しいrun IDとしてin-memory registryへ追加する。registryは単一process内だけであり、server再起動を越える保存にはexportが必要である。

## API契約

主なREST endpoint:

```text
POST /api/runs
GET  /api/runs/{run_id}
POST /api/runs/{run_id}/step
POST /api/runs/{run_id}/run
POST /api/runs/{run_id}/pause
POST /api/runs/{run_id}/reset
POST /api/runs/{run_id}/events
POST /api/runs/{run_id}/fork
POST /api/comparisons
POST /api/runs/{run_id}/export
POST /api/import
GET  /api/runs/{run_id}/events/stream
```

不明ID、不正な数値、範囲外値、未知のpatch kindは4xxで拒否する。SSEは現在frameを1件通知する有限streamであり、background simulation queueではない。

## 性能境界

`python scripts/measure_brain_lab.py` は2,000 Sparks / 10,000 edgesの合成graphから、表示に必要な250 Sparks / 600 edgesをactive-firstで抽出する時間を測る。2026-08-23のlocal測定値は0.9654 msで、60 FPSの16.6667 ms preparation budget内だった。これはbrowser paint、end-to-end frame time、GPU性能、消費電力の測定ではない。

大規模graphは全要素を毎frame描画せずrelevant subsetを表示する。元のengine state、trace、研究用artifactは間引かない。

## Static fallback

FastAPIを導入しない場合も、`python scripts/run_demo.py` が生成する `artifacts/demo/visualizer.html` を直接開ける。既存の静的Visualizerはreference fallbackおよび回帰oracleとして維持する。

## Optional dependencies and licenses

- FastAPI: MIT License — <https://github.com/fastapi/fastapi/blob/master/LICENSE>
- Uvicorn: BSD 3-Clause License — <https://github.com/Kludex/uvicorn/blob/main/LICENSE.md>

frontend graphはthird-party libraryを追加せずnative SVGで描画する。これによりbundled assetとoffline条件を小さく保つ。

受入検証で使用したversion pinとdirect dependency noticeは `requirements-lab.lock` と `docs/THIRD_PARTY_NOTICES.md` に記録する。
