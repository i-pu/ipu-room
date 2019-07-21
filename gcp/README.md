# Tips
- gcr
    - ライフサイクルを設定してもすぐに反映されるわけではない
- google cloud run
    - ポートを環境変数として必要があるが
    - その際に，80 ポートだとだめなので注意
    - https://medium.com/google-cloud/google-cloud-run-or-how-to-run-your-static-website-in-5-minutes-and-much-more-dbe8f2804395

- gcp alert policy 
    - <https://cloud.google.com/monitoring/alerts/policies-in-json>  
しきい値のタイプのアラートポリシーはconditionThreshold という

## google sourcerepo repositoryの注意点
すべての権限をrevokeして，全てのアカウントをログアウトしてから作成する
普通にやるとできない
[see also](https://serverfault.com/questions/966583/mirror-github-to-cloud-source-repositories)