# HUMAN-20260925-002 — P0 GitHub persistence incident resolution across the SparkBrain fleet

Human status: `OPEN`  
Created: `2026-09-25 JST`  
Priority: `P0 / HIGHEST OPERATIONAL PRIORITY UNTIL RESOLVED`  
Operation: `ADD`

## Intent

現在SparkBrain各所で発生している **GitHubへの書き込み不整合・partial persistence・durable publication欠落等の障害を、全SparkBrain運用上の最優先解消課題に設定する。**

この障害が解消されるまで、通常の研究・統合開発・探索・監査・補助作業よりも、GitHub persistenceの原因特定、影響範囲の把握、整合性回復、再発防止、正常復帰確認を優先する。

全ての現行SparkBrain schedulerは、自身の役割・権限・hard floorを守りながら、この障害の解消に必要な情報提供・診断・検証・修復支援へ最大限協力すること。

## Current problem class

現時点で既に観測されている症状には、少なくとも以下を含む。

- generation historyは存在するが、latest/state pointerが古いまま残る partial persistence;
- scheduler invocationは発生しているが、期待されるdurable outputがGitHubに残らない;
- worker/branchによって正常writeと欠落が混在する;
- GitHub App/repository write permission全体の消失では説明しにくい;
- direct canary write成功とscheduler-owned write失敗が併存する;
- queue delay、shared ops branch、multi-step Contents API write、stale SHA/head競合、scheduler runtime側mutation refusal等が候補に残っている。

これは現時点の障害仮説であり、確定原因として扱ってはならない。実際のHTTP/API/runtime error class、branch head変化、write sequence等を可能な限り直接観測し、推測と事実を分離する。

## Priority rule

本DirectiveがOPENかつincident未解消の間、各schedulerは通常業務の前に以下を確認する。

1. 自身または依存streamに未解消のGitHub persistence障害があるか。
2. 自身が原因特定または復旧に役立つ具体的作業を持つか。
3. 通常業務を継続するとdurable stateの不整合や追加競合を悪化させないか。
4. Control Brainが現在のincident owner、affected worker、suspension/restart条件をどう定義しているか。

具体的な障害解消作業が存在する場合は、通常の低優先度研究・探索・整理より優先する。

ただし、P0であることは科学的one-way integrity、immutable evidence、held-out隔離、FORMAL hard floor、ownership/collision safetyを解除しない。

## Fleet-wide cooperation

### Control Brain

Control Brainを本incidentの統括ownerとする。

- incident IDを発行・維持する;
- affected scheduler / branch / path / last-safe-generationを管理する;
- 必要に応じてaffected workerを `OPERATIONAL_FAULT_SUSPEND` する;
- 停止時には必ず客観的restart条件を設定する;
- 自身または適任schedulerへ原因調査を割り当てる;
- partial persistenceをreconcileする;
- canary write/read、post-restart first generationを検証する;
- 原因が解消または十分にboundedされたら速やかにworkerを再起動する;
- 単発write成功だけでincidentを閉じない;
- 影響範囲を最小化し、無関係なschedulerまで一括停止しない。

Control自身は停止しない。

### Repository Steward capability

repository / GitHub側の診断を優先する。

- repository permissions;
- rulesets / branch and tag protection;
- branch/ref topology;
- ops branch ownership;
- append-only history vs moving pointer consistency;
- commit sequence;
- concurrent writers;
- canary write/read;
- exact ref movement;
- stale mapping / protection anomaly

をread-firstで確認する。

科学結果を変更せず、修復が必要な場合はControlのincident planに従う。

### Evidence Analyst

科学判断より前に、自身のcontrol-plane persistence整合性を確認する。

特に、

- newer complete history generation;
- stale latest/state;
- authoritative generation;
- build/science allocation pointer;
- missing state transition

をreconcileし、古いmoving pointerだけを最新authorityと誤認しない。

障害解消に必要なpointer reconciliationは科学結果の再解釈と分離する。

### MAIN / Relay

通常のSCIENCE/SYSTEM_BUILD critical pathより、現在のpersistence障害が自身のdurable authorityやhandoffを壊している場合は復旧を優先する。

- write前のfresh ref/head取得;
- stale generation/collision確認;
- partial reportの有無;
- lease/latest/state/history整合性

を確認する。

Controlがfault suspensionした場合は勝手に再開しない。restart条件成立後の再起動に従う。

### Utility

P0 incident中は、通常のautonomous idle workよりGitHub persistence診断・tooling・reconciliation支援を優先してよい。

対象例:

- Contents API / Git data API差異の診断;
- atomic multi-file commit helper;
- compare-and-swap / bounded retry設計;
- stale SHA reproduction;
- write telemetry;
- branch-head race diagnostic;
- CI/tool integration;
- non-destructive persistence checker.

科学的authorityは持たない。

### Methodology

障害が科学的記録・evidence interpretationへ与える影響を監査する。

特に、

- historyは新しいがlatest/stateが古い;
- partial publicationを「結果なし」と誤解;
- duplicated generation;
- stale pointer由来の誤ったallocation;
- persistence repairが過去科学結果のrewriteになっていないか

を点検する。

運用障害の修復を過剰なscientific gateへ変換しない。

### Literature / Theory Synthesis / Audit

通常の外部研究を完全停止する必要はないが、自己streamにdurability欠落がある場合は、それを最優先で診断・報告する。

- invocationしたのにoutputなし;
- history/latest/stateの不一致;
- role-separated stream競合;
- shared branch headの変化;
- retry/error class

を可能な限り記録する。

新しいliterature/theory/audit generationを量産することより、まずdurable publicationの信頼性回復を優先する。

### Fast Forge

通常のprototype探索より、Forge自身または共有orchestrator branchのpersistence障害が関係する場合は、その診断を優先する。

ただし一般的なGitHub運用修理の主担当にはしない。Control/Steward/Utilityの調査を補助する範囲に留める。

### Current State Brief

read-onlyでincident進捗を追跡する。

- affected workers;
- intentional fault suspension;
- restart conditions;
- latest successful canary;
- partial persistence debt;
- unresolved root-cause hypotheses;
- post-restart validation

をユーザーに分かる形で報告する。

## Required technical investigation

最低限、以下を横断確認する。

1. GitHub App / repository write permissions and current rulesets.
2. Affected branchごとのrecent commit sequence.
3. 1 generation内のhistory/latest/state write ordering.
4. multi-step Contents API更新で利用したblob SHA/headのfreshness.
5. shared branch上のconcurrent writers.
6. scheduler queue delayと実際のrun overlap.
7. GitHub API error class: 403 / 409 / 422 / other.
8. scheduler/runtime-side mutation refusalの有無.
9. direct canary writeとscheduled writeの差.
10. atomic multi-file commit / Git data API pathの利用可否.
11. pointer/cache repairを安全に実行できる条件.
12. restart後first-generationの完全性.

不明な項目は `UNKNOWN` のまま残し、推測で埋めない。

## Preferred persistence target

原因調査の結果が支持する限り、将来的な標準として以下を優先的に評価する。

- append-only generation historyをprimary durable recordとする;
- latest/stateはmoving pointer/cacheとして扱う;
- history/latest/stateを可能なら1 atomic commitで更新する;
- mutation直前にbranch head / current blob SHAを再取得する;
- optimistic concurrency / compare-and-swapを用いる;
- stale head conflictではbounded retryし、newer generationを上書きしない;
- force pushしない;
- write attempt/error/head-before/head-after/retry/persistence-complete telemetryを残す。

これは現時点で確定実装を命じるものではなく、incident investigationで支持された場合の優先設計方向である。

## Suspension and restart

GitHub書き込み不整合を理由にschedulerを停止することを認める。

ただし、

> 「書けないので停止した」

だけで終えることは禁止する。

停止時にはControlが以下を記録する。

- disable reason;
- incident ID;
- affected stream;
- last safe generation/ref;
- restart conditions;
- diagnostic owner;
- max dormancy / next review.

restart条件が満たされたら速やかに再起動する。fault/collision suspensionからの復帰後は、最初のrunのdurable persistenceを確認してからHEALTHY扱いにする。

## Completion criteria

本DirectiveのP0状態を解除できるのは、最低限以下が満たされた場合。

1. principal root cause(s)が特定または十分にboundedされている;
2. affected durable streamsのpartial stateがreconcileされている;
3. write pathに再現可能な安全策が入っている、または再発条件が明確に回避されている;
4. affected workerごとにcanaryまたは実generationのdurable successが確認される;
5. history/latest/state等のauthority ruleが明確で、stale pointerが科学・build allocationを誤らせない;
6. suspended workerのrestart条件が解消され、必要なworkerが復帰している;
7. 同じfailure patternが継続的に再発していないことを少なくとも複数の関連runで確認できる。

完全な理論上の無事故証明は不要だが、単発成功だけでは解消扱いにしない。

## Scientific integrity

このDirectiveは運用障害解消の優先度を上げるものであり、以下を許可しない。

- consumed FORMAL identityのrerun / retune / rescore;
- immutable/formal/sealed/evidence refの破壊的変更;
- terminal objectの再open;
- held-out/evaluator leakage;
- stale pointer repairを利用した科学結果の書換え;
- missing durable outputを都合の良い科学結果として補完;
- schedulerのrole boundaryを無視した無秩序な同時修復write.

## Required independent handling

これはユーザーからの明示的な運用Directiveであり、GitHub persistence障害を全SparkBrain schedulerの最優先解消課題とする。

Controlは本Directiveを単なる提案待ちとして放置せず、既存のscheduler fleet authorityとincident-management authorityの範囲内で直ちに運用へ反映すること。

科学的判断を伴う変更は従来どおり各authorityを通すが、障害診断・安全停止・durable state reconciliation・canary・再起動は既に承認された運用権限の範囲で進めてよい。
