resource "google_monitoring_alert_policy" "test-alert-policy" {
    display_name = "[Test alert policy]"
    combiner = "OR"
    documentation {
        content = "hgoeajfaffa;fja"
    }
    conditions {
        display_name = "test-alert-policy conditions"
        condition_threshold {
          comparison = "COMPARISON_GT"
          filter = "metric.type=\"logging.googleapis.com/user/${google_logging_metric.server.name}\" AND resource.type=\"k8s_container\""

          threshold_value = 0.01

          trigger {
            count = 1
          }
          duration = "60s"
        }
    }

    # notification_channels = [
    #     "${google_monitoring_notification_channel.basic.id}",
    # ]
    enabled = true
}

resource "google_logging_metric" "server" {
  name = "k8s_container/server"
  # filter = "resource.type=\"k8s_container\" AND textPayload:\"error\""
  filter = "resource.type=\"k8s_container\" AND resource.labels.container_name=\"server\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type = "INT64"
  }
}

# resource "google_monitoring_notification_channel" "basic" {
#   display_name = "Test Notification Channel"
#   type = "slack"
#   labels = {
#     channel_name = "hoge"
#     auth_token = "hoge"
#   }
# }

# terraform から stackdriver のログを読み取り，
# 正規表現で特定のログを抽出し，
# 特定のSlackのチャンネルに流し込む
# 
# 旧システムと新システムの両方あるので，
# その差分を考慮してstackdriver のログとソースコードを見比べながら，
# 差分を見つけてソースコードを修正し，
# プルリクを行う
# ログの中のtextPayload 野中の文字列を正規表現で撮ってくれる
