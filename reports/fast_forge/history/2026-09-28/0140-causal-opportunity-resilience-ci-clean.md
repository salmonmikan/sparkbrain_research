# SparkBrain Fast Forge — causal-opportunity resilience

- schema_version: 2
- generation_id: `FORGE-20260928T014020+0900-CAUSAL-OPPORTUNITY-RESILIENCE-CI-CLEAN`
- produced_at: `2026-09-28T01:40:20+09:00`
- forge_id: `FORGE-CAUSAL-OPPORTUNITY-RESILIENCE-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

## 今回試したこと

直近のcausal-opportunity certificateが、一本の脆いtrace edgeだけに依存していないかを測る隔離Forge prototypeを作成した。

base certificateが成功した後だけ、time-respecting influence graphへunit capacityを与え、treated seed群からreadout群までのmaximum flow / minimum cutを計算する。出力はedge-disjoint path数、決定的なminimum edge cut、単一edge依存か複数routeかの分類である。

## 結果

- 単一chain: `SINGLE_EDGE_FRAGILE`、edge-disjoint path数1、minimum cut 1 edge
- diamond graph: `REDUNDANT_PATHS`、edge-disjoint path数2、minimum cut 2 edges
- 2つのtreated seedから同じreadoutへ独立route: path数2
- event/edge入力順を反転してもflowとminimum cutは同一
- treated event自体がreadoutの場合は`DIRECT_READOUT`としてedge-cut評価から分離
- incomplete、invalid、disconnected traceはbase certificate失敗を引き継ぎ、resilience claimを作らない
- focused local tests: 8/8 PASS
- local Ruff: PASS
- exact prototype head CI: Python 3.11 / 3.13 SUCCESS
- full repository test, readiness and bundle validation: SUCCESS

Prototype commit: `e165e4794d81e873328eb75f82ad51f6bcb820ff`  
CI run: `36333889368`

## 単純な説明で足りるか

足りる。これはvalidated DAG上のunit-capacity maximum-flow/minimum-cutとedge-disjoint path数であり、新しい因果推論、学習、記憶、認知原理ではない。

## 統合部品として使えるか

限定的に有用。介入probeやablationの前段で、存在証明が単一の記録edgeに依存するか、複数の独立routeを持つかを明示できる。

ただしroute冗長性は必要条件でも十分条件でもなく、単一路だから効果がないとも、複数路だから効果があるとも言えない。SYSTEM_BUILDへは別途割当がある場合だけ任意診断として使う。

## 扱い

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`。NON_EVIDENTIARY / NONCANONICAL、scientific credit 0。

MAIN R164はSB002をexact head `720e18bcff53be76c861fa8c09d24d5320b90455`へ公開しCI成功後にAnalyst待ちで停止している。本prototypeはscope routing、route-local revision、rollback、checkpointを実装せず、SB002 branch/head/filesを変更していない。

Candidate #35、RD005、RD006、SB001、科学/evidence refも変更していない。

## 注意

- callerがtrace completenessとinfluence edgeの妥当性を独立に保証する必要がある
- edge-disjointnessでありnode-disjointnessではない
- hidden/unrecorded pathsは検出しない
- edge capacity/strength、effect size、sign、readout sensitivity、ceilingを評価しない
- redundancyはcounterfactual causal contributionを証明しない
- 実タスク、resource comparison、外的妥当性は未検証
- usefulnessはcomposition contributionやscientific noveltyを確立しない

## Authoritative refs

- main: `cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- Human Directives: `3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7`
- Evidence Analyst R159: `17a58e31127f8e2e47848ef4794f53bcd3908900`
- MAIN R164 reports: `c185fba70087122131274dcc911cb2f725665bb2`
- SB002 exact head: `720e18bcff53be76c861fa8c09d24d5320b90455`
- Control R98: `57fe5474dea444fe21cd4e1be9b4c81be8cd582a`
- Methodology R135: `70ec61002581d55ebb29b01fc5f240b7aca4b467`
- Theory R12: `8f035e911bf7b1c965b97695b04834265cf415cc`
- Utility R159 lineage: `123d720717cc5efcb0adcf1a07187efe7e78caba`
- prior Forge certificate handoff: `fd3b3a43e4bc8030b5f9fc33e23bb90f91611d69`

新しい科学結果: なし  
あなたの対応: 不要
