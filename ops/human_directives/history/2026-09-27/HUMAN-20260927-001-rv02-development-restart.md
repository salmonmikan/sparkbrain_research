# HUMAN-20260927-001 — RV02の開発再開と通常外部学習の有無による構成診断

Human status: `OPEN`  
Created: `2026-09-27 JST`  
Origin: RV02再開案の説明後、ユーザーが「その内容でディレクティブとして依頼しといて」と明示的に登録を依頼。

## Intent

RV02の開発再開を依頼する。RD005では能力段階に到達していないため、前回の失敗記録を保持した新しい開発版で構成上の問題を切り分け、評価可能な構成まで進めたい。旧実験の終了を理由に研究テーマ全体を閉じた扱いにはしない。RD004等の既存の開発段階の能力評価・否定結果は維持する。

## Context / facts to re-verify

- RD005 D1の保存結果は18条件すべてが `D1_UNREACHABLE`、観測されたhidden spikeは0。能力出力は未開封で、後続の能力試験のlearner/probeは実行されていない。これは構成・到達可能性の否定結果であり、規模拡大の有用性に対する最終判定ではない。
- 今回のコード調査では、RD003/RD004の外部入力処理には通常の外部学習が含まれる一方、RD005の構成探索は初期Fieldへの入力と時間発展のみで、その通常学習を呼び出していない条件差を確認した。
- 通常学習の追加によって内部発火やreturn gateが成立するかは未検証。この条件差を原因候補として検証し、修理成功・新規性・性能優位は前提にしない。RD004等の開発段階の能力比較が実施済みであることと、RD005能力試験が未実施であることを区別する。

## Requested development sequence

1. 保存rawと正確なソースを再照合し、通常外部学習の条件差と内部発火0の関係を小さな開発比較として定義する。新しい版・出力識別子を用い、共通の入力・初期構成・計測条件を事前に定める。
2. 検証対象であるhidden-return学習を無効にしたまま、通常の外部学習あり／なしを比較する。最初の診断では閾値・gain・刺激強度等を同時に変更せず、条件差の効果を切り分ける。結果に応じた開発変更は理由と版を記録し、既存結果を上書きしない。
3. 構成診断で内部発火と後続returnの物理的到達・適格性を確認する。gateが成立した場合は、条件を事前固定した別段階のE0（hidden-return学習なし）／E1（因果的なhidden-source対応）／ES（同じevent予算でsource対応を入れ替えた対照）で、該当結合の更新とその後の可視応答を比較する。発火だけで学習成立や能力向上と判定せず、成立しない段階も具体的な結果として残す。
4. 構成と上記の機構比較が評価可能な状態になった場合に、後続検証として1倍・3倍・10倍の規模比較へ進む。同じ外部経験と平均接続次数を保ち、各規模で資源条件を整合させたreservoirと比較する。保持範囲だけでなく、正確な経路選択、余計な活動、内部容量の利用を測る。資源整合が未完ならその限界を明示する。

## Boundaries

- RD005の消費済み実験・出力識別子、旧判定、raw、freeze/control/preserve等の証拠を変更・再利用して再試行しない。新しい開発対象として履歴を残す。
- HUMAN-20260922-005の開発反復方針に沿って進める。開発観察を独立した確認的証拠として数えず、FORMALは別の事前固定された契約・新しい評価面・既存の科学的条件に従う。
- この登録作業はディレクティブの追加に限る。スケジュールの追加・変更・停止、既存SB001への変更、実験の即時実行は含まない。

## Desired end state / routing

Control Brainで本提案を取り上げ、Evidence Analystが新しいRV02開発対象・最小比較・担当を具体化し、適切な実行担当へ渡す。単なるIDの付け替えではなく、通常学習の条件差を検証することを再開の根拠とする。

期待する報告は、通常学習の有無で何が変わったか、どこまで学習経路が成立したか、規模比較へ進めるか、または何が依然として成立しないか。

## Required independent review

Control Brainは証拠・科学的条件・現在の作業との整合を独立に確認し、`ACCEPT / MODIFY / DEFER / REJECT` とその理由を自身の記録へ残す。Evidence Analystの新規対象割当と通常の実行経路へ接続する。本Human Directiveは科学的結果や採用済み判定そのものではない。

## Evidence anchors

- [RD005 D1 terminal audit](https://github.com/salmonmikan/sparkbrain_research/blob/a02768b18fa290f249b7c488c896fad79f9ca409/docs/research/RV02_RD005_D1_TERMINAL_OUTCOME_20260914.md)
- [Frozen RD005 construction source](https://github.com/salmonmikan/sparkbrain_research/blob/c60b7fd8d3889ee969f505d921e7d31c990871e6/src/sparkbrain/research/rv02_rd005_construction_artifact.py)
- [RV02 development feasibility contract](https://github.com/salmonmikan/sparkbrain_research/blob/c6b33606850ef591690074f50ed92a4c9400b8bd/docs/research/RV02_DEVELOPMENT_FEASIBILITY_CONTRACT.md)
- [Development iteration directive](https://github.com/salmonmikan/sparkbrain_research/blob/ops/human-directives/ops/human_directives/history/HUMAN-20260922-005-development-iteration-calibration.md)
