# HUMAN-20260926-003 — P0 accelerated resolution and full scheduler-fleet restoration

Human status: `OPEN`  
Created: `2026-09-26 JST`  
Priority: `P0 / IMMEDIATE RECOVERY OVERRIDE`

## Intent

現在のGitHub persistence / scheduler-runtime P0問題について、**速やかな解決と全SparkBrain schedulerの正常復旧を最優先する。**

HUMAN-20260925-002を置き換えるのではなく、同Directiveを強化する追加指示として扱う。

## Required operating posture

- P0の調査・修復・検証・scheduler復旧を、通常研究・整理・低優先度ガバナンスより優先する。
- 過度に保守的な停止・様子見・単発canary待ちを常態化させない。
- 原因が完全には確定していなくても、十分に合理的な回避策・再試行・復旧経路がある場合は前進する。
- **運用上の確信度や診断精度を多少犠牲にしてでも、P0解消とfleet復旧を優先してよい。**
- ただし、この加速方針は科学結果の捏造・改変、consumed FORMAL identityのrerun/retune/rescore、immutable/formal/sealed/evidenceの破壊的変更、held-out漏洩を許可するものではない。正確性より解決を優先する対象はP0の運用判断・診断・復旧手順であり、科学的証拠そのものではない。
- workerを停止したまま「安全」とするより、boundedな回避策を導入して可能な限り早く再稼働させる。
- Control Brainは、既存のincident-scoped prompt mutation / fleet enable-disable / canary / blue-green recovery authorityを積極的に使用し、**全managed SparkBrain schedulerの復旧を完了状態として目指す。**

## Fleet-wide GitHub mutation retry contract

GitHubへのwrite / mutationが失敗した場合、関連schedulerは原則として次を適用する。

1. 初回attemptを含め、**同一目的のmutationは合計最大3 attemptまで**許可する。
2. OpenAI runtime / safety layerでGitHub到達前に拒否された場合もretry対象とする。
3. stale branch head / blob SHA / compare-and-swap conflictの場合は、最新head/SHAを再取得してmutationを再構成してからretryする。
4. 各retry前に、必要な最新branch head / target stateを再取得する。
5. force pushは禁止のままとする。
6. 3 attemptすべて失敗した場合は、そのrunではfail closedし、観測したfailure layer / error class / retry countを記録またはuser-facing outputへ残す。
7. 成功時はreadbackで実際のbranch/file/ref状態を検証する。
8. retryは同一科学結果を再実行する意味ではない。GitHub persistence / publication operationの再試行に限定する。

## Recovery completion expectation

Control Brainは本Directiveを受理後、P0解消とfleet復旧を単なる長期課題として扱わず、直近runから具体的に進めること。

- retry contractを必要なwriter schedulerへ反映する;
- stopped/fault-suspended workerのrestart条件を再評価する;
- 過度に保守的な条件だけが復旧を妨げている場合は緩和する;
- canary単発成功を過大評価しない一方、完全な原因証明を待ち続けない;
- boundedな成功証拠が得られたworkerから順次復旧する;
- 全managed schedulerが期待状態へ戻るまでP0を継続管理する。

## Required handling

これはユーザーによる明示的な運用Directiveであり、P0 recovery scopeにおいて即時反映を要請する。
Control Brainは独立評価を行ってよいが、単なる保守性・不確実性のみを理由に長期DEFERしてはならない。
科学的hard floorとの具体的衝突がない限り、P0解決速度とscheduler復旧を優先する。
