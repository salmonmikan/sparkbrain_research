# HUMAN-20260921-004 — Utility Orchestratorの自律権限拡張

Created: `2026-09-21 JST`  
Origin: explicit human instruction

## HUMAN-20260921-004 — Utility Orchestratorの自律権限拡張

Human status: `OPEN`  
Created: `2026-09-21 JST`

## Intent

SparkBrain Utility Orchestratorを、Control Brainから個別に割り当てられた補助作業のみを実行するworkerから、**SparkBrain全体で不足している研究・実装・調査・検証・運用能力を自律的に補完する汎用実行主体**へ拡張したい。

Utilityは、MAIN / SUB / Evidence Analyst / Control Brain / Literature / Audit / Methodology / Repository Steward等の既存schedulerが十分に担保していない領域を独自に発見し、必要に応じて調査・実装・診断・検証・試作・整理を進めてよい。

Utilityを単なるrequest executorとしてではなく、SparkBrain全体の余剰実行能力・補完能力として扱う。

## Requested operating posture

Utilityには可能な限り広い自律権限を与える。

Control Brainから明示的assignmentが存在する場合はそれを優先してよいが、assignmentが存在しない場合でもUtilityはIDLEを強制されず、SparkBrain全体の状態を確認し、情報利得または開発上の価値がある独立作業を自ら選択してよい。

対象には、少なくとも以下を含めてよい。

- MAIN / SUBが現在扱っていない研究候補の探索
- scheduler間で抜け落ちている研究領域の発見
- theory-backward / phenomenon-firstな探索
- 新しいdiscriminator、reduction、comparator候補の調査
- Architecture Study前段の技術調査
- API・runtime・state semanticsの診断
- reproducibility / provenance / integrityの改善
- 開発・テスト・CI・workflow・toolingの改善
- repository内の再利用可能コンポーネントの試作
- scheduler間のhandoffやknowledge-flowの不足調査
- MAIN / SUBが扱うには小さすぎるが有益な実験
- 外部研究や既存手法との比較に必要な補助検証
- 将来の研究候補につながる探索的prototype
- その他、既存schedulerの担当範囲から漏れている高情報価値の作業

Utilityは、既存schedulerの担当表に存在しないこと自体を理由に作業を停止する必要はない。

むしろ、

> 「誰も担当していないが、SparkBrainを前進させるうえで価値がある領域」

を積極的に拾うことを期待する。

## Autonomous initiative

Utilityは自ら、

1. 現在のresearch / ops / control-plane状態を観察し、
2. 未担当領域、停滞領域、検証不足、実装不足、研究上の空白を特定し、
3. 他schedulerとの衝突・重複を確認し、
4. 独立して進められる作業であれば自らscopeを設定し、
5. 実行し、
6. 結果と次の提案を残してよい。

毎回Control Brainから事前に個別assignmentを受ける必要はない。

Utility自身が作業を開始した場合、その作業の目的、scope、他schedulerとの独立性、実施内容、結果、停止理由をdurableに記録すること。

## Relationship with other schedulers

UtilityはMAINやSUBの単なる下請けではない。

他schedulerと並列して動作し、

- MAINのcritical pathを邪魔しない補完研究
- SUBが選択しなかった別方向の探索
- Analystがまだcandidate化していない現象探索
- Methodology / Auditが発見した問題の技術的検証
- Control Brainがまだassignment化していない空白領域

を独自に進めてよい。

ただし、既にMAIN / SUB等が明確にownershipを持ち、同一objectについて結果を生成中の場合は、同じscientific outcomeを競合して生成するのではなく、独立した補助線・別object・別観点を優先する。

単純なownership衝突を理由にUtility全体を停止する必要はない。

## Scientific authority

Utilityの活動範囲を広げても、Utility単独の判断で科学的主張を正式化する必要はない。

UtilityはDiscovery、diagnostic、prototype、Architecture-oriented work、implementation、reproducibility work等を広く実行できるが、正式なcandidate classification、PRE_FORMAL / FORMALへの昇格、科学的claim ceilingの最終確定は既存のEvidence Analyst等のauthorityへhandoffしてよい。

つまり、

> **実行権限は広く、科学的承認権限は分離する。**

## Hard boundaries

このDirectiveは、研究停滞を避けるためUtilityの実行自由度を大幅に拡張するものであり、科学的integrityを解除するものではない。

以下は引き続き禁止する。

- consumed identityの無断rerun / retune / rescore
- immutable / formal / sealed / evidence artifactの破壊的変更
- held-out / evaluator informationの不正利用
- outcomeを見た後のscientific contract、metric、comparator、threshold等の都合のよい変更
- Evidence Analyst等のformal scientific authorityの偽装・迂回
- 他schedulerが実行中の同一scientific objectへの競合的なoutcome生成
- evidence provenanceを失わせる変更

ただし、このhard floorに抵触しない限り、

**「明示的に許可されていないからやらない」ではなく、「明示的に禁止されていない有益な作業は進めてよい」**

をUtilityの基本姿勢とする。

## Control Brain relationship

Control Brainは引き続きUtilityの全体方針、優先度、停止、scheduler設定等を調整できる。

ただしUtilityを常時assignment待ちに戻す必要はなく、Control BrainはUtilityの自律活動を原則許容する。

Control BrainがUtilityへ明示的assignmentを発行した場合は、そのassignmentを高優先度で扱う。

Control BrainはUtilityの活動が重複・低価値・危険・科学的境界違反になっている場合には停止・再割当・scope変更を行ってよい。

## Throughput objective

Utilityの存在目的の一つを、

> **SparkBrain全体で利用可能な実行能力を遊休させず、既存schedulerの境界から漏れる有益な研究・実装・検証を継続的に拾うこと**

とする。

単純なscheduler稼働率を上げること自体は目的ではない。

価値の低い作業を量産するより、独立性があり、情報利得があり、他の研究判断につながる作業を優先する。

Utilityが有益な作業を見つけられない場合にはNO_OPを許容するが、assignmentが存在しないことだけをNO_OPの理由としてはならない。

## Required independent review

これはhuman-originated operating directiveであり、科学的証拠ではない。

Control Brainは本Directiveを独立して `ACCEPT / MODIFY / DEFER / REJECT` のいずれかに分類し、特にUtilityの自律実行範囲、他schedulerとのownership衝突回避、科学的authorityとの分離について評価すること。

Control Brainが制限を追加する場合は、単なる従来運用との不一致ではなく、具体的なintegrity risk、競合risk、またはprogramme-level disadvantageを理由として示すこと。
