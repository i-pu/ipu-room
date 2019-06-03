resource "google_monitoring_alert_policy" "test-alert-policy" {
  display_name = "[Test alert policy]"
  combiner = "OR"
  documentation {
    content = "hgoeajfaffa;fja"
  }
  conditions {
    display_name = "test-alert-policy conditions"
    condition_threshold {
      filter = <<EOF
metric.type="logging.googleapis.com/user/${google_logging_metric.web-socket-server.name}" AND
resource.type="k8s_container"
metric.label.textPayload: "error"
EOF

      duration = "0s"
      comparison = "COMPARISON_GT"
      threshold_value = 0.01
      trigger {
        count = 1
      }

      aggregations {
        per_series_aligner = "ALIGN_DELTA"
        cross_series_reducer = "REDUCE_NONE"
        alignment_period = "60s"
      }
    }
  }

  notification_channels = [
    google_monitoring_notification_channel.email.id,
  ]
  enabled = true
}

resource "google_logging_metric" "web-socket-server" {
  name = "k8s_container/web-socket-server"
  filter = <<EOF
resource.type="k8s_container" AND
resource.labels.container_name="web-socket-server"
textPayload: "error"
EOF
  description = "catch error, then label"

  metric_descriptor {
    metric_kind = "DELTA"
    value_type = "INT64"
    labels {
      key         = "textPayload"
      value_type  = "STRING"
      description = "This label is textPayload that include \"error\" in textPayload"
    }
  }
  label_extractors = {
    textPayload = "REGEXP_EXTRACT(textPayload, \"(.*)\")"
  }
}

resource "google_monitoring_notification_channel" "email" {
  display_name = "Test Notification Channel"
  type = "email"
  labels = {
    email_address = "kafu.h1998@gmail.com"
  }
}

# terraform から stackdriver のログを読み取り，
# 正規表現で特定のログを抽出し，
# 特定のSlackのチャンネルに流し込む
# 
# 旧システムと新システムの両方あるので，
# その差分を考慮してstackdriver のログとソースコードを見比べながら，
# 差分を見つけてソースコードを修正し，
# プルリクを行う
# ログの中のtextPayload 野中の文字列を正規表現で撮ってくれる
