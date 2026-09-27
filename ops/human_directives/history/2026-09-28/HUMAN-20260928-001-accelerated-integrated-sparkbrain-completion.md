# HUMAN-20260928-001 — Accelerated Integrated SparkBrain Completion

Human status: `OPEN`  
Created: `2026-09-28 JST`  
Priority: `HIGH / SYSTEM INTEGRATION ACCELERATION`

## Intent

SparkBrain研究について、現在は個別機構の探索を増やすことよりも、既に得られた研究結果・既知機構・SYSTEM_BUILD・Fast Forge成果を利用し、**実際に連続稼働する統合SparkBrainを早期に成立させること**を優先する。

現在のscientific integrity、FORMAL one-way rule、immutable evidence、held-out isolation、consumed identityの保護は維持する。

一方で、科学的証拠を生成しない通常のSYSTEM_BUILD・integration engineering・diagnostic・toolingについては、不要な承認待ち、細粒度handoff、過度な停止を減らし、可能な限り連続的・並列的に進める。

## Primary integration target

当面の最優先成果物を、以下の閉ループを一つの連続システムとして稼働させることとする。

`external observation`
→ `persistent internal state`
→ `multiple hypotheses / scopes`
→ `competition / abstention / selection`
→ `prediction and/or action`
→ `later observation / outcome`
→ `selective revision`
→ `updated persistent state`
→ `next prediction / action`

さらに、

- checkpoint / restore / replay
- failure時のtransactional rollback
- internal state observability
- deterministic bounded test worlds
- provenance of reused mechanisms

を含める。

この状態を **Integrated Prototype Milestone 1** とする。

## Rolling SYSTEM_BUILD authority

Evidence Analystは、SYSTEM_BUILDについて、可能な場合は1回のgenerationで単一の細粒度作業だけを割り当てるのではなく、**複数の連続したbounded engineering milestonesをprospectiveに定義してよい。**

各milestoneについて、

- target capability
- permitted components
- acceptance tests
- resource limits
- stop conditions
- claim boundary

が事前に明確であり、scientific result-bearing executionを含まない場合、MAINは前段milestoneのacceptanceを満たした後、**新しいAnalyst generationを待たずに次の事前承認済みmilestoneへ継続できる運用を優先的に検討する。**

MAINが停止し fresh Analyst reconciliationを要求するのは、原則として以下のような場合に限定する方向を評価する。

1. prospective contract外の設計変更が必要;
2. target capability自体を変更する必要がある;
3. acceptance testが失敗し、結果依存のredesignが必要;
4. scientific claim / candidate creation / scientific executionへ移行する;
5. immutable / FORMAL / consumed boundaryへ接触する;
6. Evidence Analystが明示したstop boundaryへ到達する。

単に一つのengineering milestoneが成功したことだけを理由として、必ず毎回停止する必要がある運用は見直してよい。

## Parallel execution posture

MAINのcritical integration pathと衝突しない限り、他workerは並列で次工程を準備してよい。

### Fast Forge

Fast Forgeは、MAINが現在実装しているmilestoneの次または次々段で必要になりそうな、

- integration primitives
- alternative implementations
- failure guards
- state/replay mechanisms
- causal diagnostics
- component-replacement variants
- interaction-ablation tooling

を先行して試作してよい。

Forge成果は引き続きNON_EVIDENTIARY / NONCANONICALであり、MAINへの採用はAnalyst authorityに従う。

### Utility

Utilityは、MAINと競合しない範囲で、

- integration test harness
- long-run / stability diagnostics
- observability
- checkpoint / replay validation
- CI / tooling
- provenance / readback verification
- synthetic test worlds
- benchmark infrastructure

など、統合速度を上げる作業を自律的に優先してよい。

### Theory / Literature / Audit / Methodology

これらのworkerは科学的品質を維持するが、単なる形式的再確認によってSYSTEM_BUILD critical pathを停止させない。

具体的なintegrity violation、scientific overclaim、evidence contamination、irreversible riskが見つからない限り、engineering progressと並列して監査する方向を優先する。

## Information-gain and integration priority

当面の優先順位を以下とする。

1. Integrated Prototype Milestone 1の完成
2. 統合を阻害する具体的な機能不足・interface gapの解消
3. 統合後に初めて観測可能になるsystem-level phenomenaの発見
4. そのphenomenonからfresh prospective scientific questionを作る
5. 独立した新規mechanism探索

既存のterminal / reduced mechanismでも、必要な機能を提供できるならSYSTEM_BUILDへ再利用してよい。

再利用は過去のscientific resultを変更せず、scientific creditを継承しない。

## Build-to-science boundary

高速化はSYSTEM_BUILDおよびdevelopmentを対象とする。

SYSTEM_BUILDで興味深い現象が見つかっても、それ自体を科学的証拠として扱わない。

科学的主張へ進む場合は、

- fresh candidate identity
- prospective contract
- comparator / reduction ladder
- falsifier
- appropriate held-out / one-way integrity

を持つ新しいscientific objectとして改めて開始する。

Build observationからconfirmatory scientific creditを継承しない。

## Anti-idle rule

安全かつ独立して進められるSYSTEM_BUILD、Forge、Utility作業が存在する場合、`WAITING / NO_OP / IDLE`を単なる慎重さのために選択しない。

停止する場合は、

- concrete blocker
- dependency
- collision
- integrity boundary
- unavailable authority

のいずれかを明示する。

次の安全な作業がprospectively定義可能なら、それを準備または実行する。

## Completion-driven planning

Evidence AnalystとControl Brainは、現在地だけでなく、Integrated Prototype Milestone 1までの**remaining integration graph**を維持する方向を評価する。

各generationで、

- completed components
- remaining components
- current critical path
- parallelizable work
- blocking dependencies
- next 2–4 milestones

を更新し、局所的task最適化ではなく統合完成までのtotal latencyを最小化する。

## Scientific hard floor

本Directiveは以下を一切緩和しない。

- consumed FORMAL identityのrerun / retune / rescore
- immutable / frozen / sealed / formal / evidence artifactの改変
- held-out / evaluator leakage
- post-outcome scientific contract変更
- false novelty claim
- BUILD observationのscientific evidence化
- terminal candidateの偽装reopen
- provenance喪失

開発速度を上げることと、科学的証拠基準を下げることを明確に分離する。

## Relationship to existing directives

本Directiveは、既存の研究throughput改善、Utility autonomy、development iteration、Fast Forge / Slow Scienceの方針を置き換えるのではなく、**統合完成までの待ち時間と細粒度handoffを減らすための上位目的として整合させること**を意図する。

既存Directiveとoperational conflictがある場合は、単純にpermissionを積み上げずControl Brainが明示的にreconcileする。

## Requested Control disposition

Control Brainは本Directiveを `ACCEPT / MODIFY / DEFER / REJECT` で独立評価する。

採用または修正する場合は、特に以下を評価する。

- Evidence Analystによるrolling SYSTEM_BUILD contract
- MAINの複数prospective milestone連続処理
- Forge / Utilityによる次工程の先回り並列化
- Integrated Prototype Milestone 1までのremaining integration graph管理
- scientific hard floorを維持したままのhandoff latency削減

本Directiveはscientific evidenceではなく、研究・統合開発の優先順位と実行速度に関するhuman-originated strategic intentである。
