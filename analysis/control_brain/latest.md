# SparkBrain Control Brain — R52

## Position

H7の運用ブロッカーだった「MAIN/Relayから一回限りのFORMAL workflowを起動できない」問題に対して、CX01と同型のGitHub Actions `workflow_dispatch` 経路を実装した。

- default branchにfail-closed登録stubをPR #150経由で追加し、main CIは成功。
- H7 scienceは不変。
- 旧controllerも不変のまま保存。
- 新しいoperational controller revisionは `workflow_dispatch` のみを追加し、CI成功。
- `ops/h7-r5-launch-bridge` はrequest-file pushを受けてGitHub Actions APIからexact controller refをdispatchする。
- bridgeのdormant smoke runは成功し、`armed=false` だったためresult-bearing dispatchは0。
- 手動tag pushは不要になった。

## Hard stop

現Evidence Analyst R110は旧controllerをbindしており、`executor_trigger_capable=false` / `effectively_executable=false` のままなので、**まだFORMAL STARTは禁止**。

次のfresh Evidence Analystが新controller `bac7402fb01b69353eb926228574cc68c2c2a2d2` とexact science `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`、main登録stub、bridge、CI、one-way namespace未使用を独立再確認する。

そのfresh generationが明示的に新controllerをbindし、trigger capable / effectively executableをtrueにしてGO_ONCEを維持した場合のみ、MAIN/Relayは `ops/h7_launch_request.json` を1回だけarmする。bridgeがworkflow_dispatchし、result-bearing controller workflow自身がidentity、STARTED/no-clobber、raw-before-score、preserve-before-read、protected evaluation、scoringを所有する。

## Scientific state

科学結果の更新なし。H7 science/comparator/threshold/runtime/scorer/preserverは変更していない。正式identity作成、STARTED、protected evaluation、result-bearing workflow、scoring、evidence mutationはすべて0。

Revisitは34/34 bootstrap完了・新規trigger 0。TH-001 current proposalは通常機構でreduced/rejectedのまま。Fast Forgeは最新NO_OP。Utilityはclean IDLE。

## User action

H7起動のための手動tag push / 手動workflow dispatchは不要。fresh Analyst後のarm/dispatchはMAIN/Relay + GitHub Actions経路で完結させる。
