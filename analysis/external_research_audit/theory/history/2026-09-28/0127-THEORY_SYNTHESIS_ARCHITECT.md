# SparkBrain Theory Synthesis R12 — NO_PROPOSAL / SB002 allocation reconciliation

- schema_version: 2
- generation_id: THEORY-20260928T012709+0900-R12-NO-PROPOSAL-SB002-ALLOCATION-84D1B6C2
- produced_at: 2026-09-28T01:27:09+09:00
- producer_run_id: external-theory-auto-THEORY-20260928T012709+0900-R12-NO-PROPOSAL-SB002-ALLOCATION-84D1B6C2
- authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
- supersedes_generation_id: THEORY-20260927T213213+0900-R11-NO-PROPOSAL-ROUTER-RESOLUTION-BOUNDARY-5A8C31D4
- role: THEORY_SYNTHESIS_ARCHITECT
- schedule_slot: 01:30 JST
- genuinely_new_information: true
- theory_status: NO_PROPOSAL
- revisit_status: NO_REVISIT_PROPOSAL
- new_sparkbrain_scientific_result: false

## 今回の統合設計

新規提案はない。Theory R6の `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001` を維持する。

新しい状態変化は、Evidence Analyst R158/R159がR6の限定部分を `BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT` としてMAINへ正式に割り当てたことである。SB002は新しい理論ではなく、既存R6ループのうち「現在観測だけによる最大2 scopeのrouting、abstention、route-local revision、checkpoint/replay」を1次元synthetic fixtureへ閉じたNON_EVIDENTIARY SYSTEM_BUILD sliceである。

## 使う既知・既存機構

- causal streaming two-centroid clustering（固定K=2）
- midpoint／out-of-support rejection
- route-local hypothesis/evidence accumulation
- copy-on-write transactionと全状態rollback
- opaque route token
- deterministic checkpoint/replay
- current-observation-only interfaceとshared-prefix invariance

いずれも既知または通常のrouting・transaction・state-management機構であり、新しい学習原理ではない。

## 何が作れるか

SB002で作る最小閉ループは次である。

`current observation + past router state -> route token or abstain -> route-local revision proposal -> validated atomic commit or complete no-write -> serializable checkpoint`

1 observationのtransaction境界にはrouter、hypothesis、evidence、checkpoint-visible sequence stateをすべて含める。routing後にrevision validationが拒否した場合も、全状態をpre-step snapshotへ戻す。

完全no-writeを要求するのは、midpoint ambiguity、out-of-support、identical-observation conflict、invalid downstream revisionである。同じhistory/checkpointのreplayではtokenを完全再現し、arrival orderが異なる比較ではtoken文字列ではなくpartitionとroute-local outcomeの同値性を見る。

## 新規性としては何を主張しないか

これは科学的証拠ではない。

- SB002 allocation ≠ build完了
- build完了 ≠ comparative support
- route-local revision動作 ≠ composition contribution
- 2-centroid routing ≠ learned latent organization
- synthetic fixture成功 ≠ real-task capability
- transaction/replay成功 ≠ scientific novelty

runtimeへlabel、正解scope/regime/episode ID、future suffix、evaluator output、held-out fieldを渡してはならない。期待fixture出力はruntime callの外側に置く。

Forgeのcausal-opportunity certificateはtime-respecting trace reachability診断であり、scope routingもrevision loopも実装しないためSB002には採用されていない。将来の別SYSTEM_BUILD入力候補であり、因果効果やtrace完全性を証明しない。

## 次のSYSTEM_BUILD案

新しいSYSTEM_BUILD案は追加しない。MAINがR158/R159どおりSB002を実装し、current-head CIと受入試験を通して公開した後、fresh Evidence Analyst reconciliationで停止するのが現在の唯一のbuild経路である。

R6全体への拡張、Kの増加、drift/merge/split、model selection、matched comparator、real task、scale sweep、科学scoreは未許可であり、Theory側から追加しない。

## Revisit handling

Revisit triggerはない。RD005はCONSUMED_ONE_WAYのまま、RD006 v1-v4はclosed/zero-creditのまま、Candidate #35を含むterminal objectは再開しない。SB001もINTEGRATED_COMPLETE / NON_EVIDENTIARY_BUILDのまま変更しない。

## Input generations and refs

- prior theory: THEORY-20260927T213213+0900-R11-NO-PROPOSAL-ROUTER-RESOLUTION-BOUNDARY-5A8C31D4
- literature: LIT-20260927T062709+0900-R45-RV02-RD006-REACHABILITY-91C4A8E2
- audit: AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91
- evidence analyst: EVA-20260928T010015+0900-R159-SB002-ATOMICITY-CLARIFICATION
- methodology: METHCAL-20260928T002022+0900-R135-SB002-ALLOCATION-CALIBRATION
- MAIN: MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT
- Control: CTRL-20260927T235243+0900-R98-RD006-V4-AUDIT-RECONCILIATION
- Forge certificate: FORGE-20260928T004156+0900-CAUSAL-OPPORTUNITY-CERTIFICATE-CI-CLEAN
- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- external-science parent before publication: c4066afb33fdb6a67d53fa1dc9eaabfc78d211a3
- evidence-analyst ref: 7e1942e8dfe5fa5333d956ab717e041f79206075
- methodology ref: 70ec61002581d55ebb29b01fc5f240b7aca4b467
- MAIN reports ref: 5568912a42644582d9fd763bd05fc94a17ecf233
- Control ref: 57fe5474dea444fe21cd4e1be9b4c81be8cd582a
- Human Directives ref: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- Forge certificate handoff: fd3b3a43e4bc8030b5f9fc33e23bb90f91611d69

No experiment, result-bearing workflow, scientific mutation, immutable-ref movement, merge/rebase or scheduler change was performed.

新しい科学結果: なし  
あなたの対応: 不要
