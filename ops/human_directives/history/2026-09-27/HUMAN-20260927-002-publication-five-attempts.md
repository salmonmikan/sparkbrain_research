# HUMAN-20260927-002 — GitHub書込み・最終公開の試行上限を合計5回へ変更

Human status: `OPEN`  
Created: `2026-09-27 JST`  
Type: `EXPLICIT_USER_OPERATIONAL_CHANGE`

## Intent

全ての関連SparkBrain schedulerについて、既存権限内のGitHub書込み・永続化・最終公開の同一目的への試行上限を、初回込み合計3回から **合計5回（初回1回＋再試行最大4回）** へ変更する。P0 incident中に限らず適用する。停止中の定義も、再開時に旧3回規則へ戻らないよう整合させる。読取専用roleに新しい書込み権限は与えない。

本DirectiveはHUMAN-20260926-003のmutation retry contractにある「最大3回／3回失敗で終了」の数値規則のみを置き換える。旧Directiveの履歴と過去runの試行記録は保持する。

## Required operation

- 同一目的のattempt数は利用tool・API・書込み経路をまたいで合計5回以内とし、経路変更でcountをリセットしない。
- 再試行前に最新のtarget ref/head・file/blob・必要なPR/workflow状態を再取得し、stale SHA/head/CAS競合は最新状態から再構成する。
- 前回attemptの成否が不明なら、先にidempotence/readback確認を行い、既に成功していた処理を重複させない。
- 成功を独立readbackで確認したら直ちに終了する。5回の消化は義務ではない。
- 合計5回すべて失敗した場合は当該runの公開をfail closedし、観測したfailure layer/error classと実際のattempt数を残す。許可・integrity・非再試行条件に抵触する場合は、それ以前に停止する。
- 実際のplatform/tool/GitHub permissions・repository rules・role境界は維持する。拒否された境界を別tool/APIで迂回する許可ではない。
- force push、新しいgenerationの上書き、append-only記録の置換を引き続き禁止する。Analyst bridgeの固定target head・request/receipt・readback条件も維持する。

## Scope boundaries

対象は運用上のpersistence/publication retryのみ。実験回数、consumed FORMAL identityのrerun/retune/rescore/redispatch、科学的判定・閾値、immutable evidence、held-out隔離、schedulerの時刻・頻度・有効/停止状態は変更しない。専用canaryの実験数や対象・隔離設計も変更せず、許可された公開処理の再試行だけを整合させる。

## Required handling

ユーザーが明示的に承認した数値変更として、関連schedulerの現行prompt、mainの共通policy・persistence手順へ一貫して反映し、readbackで確認する。Controlは既存の監督・incident管理を継続する。この変更は科学的authorityや新しい実行権限を作らない。
