resource "google_monitoring_alert_policy" "web-socket-server-error" {
  display_name = "[Test alert policy]"
  combiner = "OR"
  documentation {
    content = "k8s error including error"
  }
  conditions {
    display_name = "test-alert-policy conditions"
    condition_threshold {
      filter = <<EOF
metric.type="logging.googleapis.com/user/${google_logging_metric.web-socket-server-error.name}" AND
resource.type="k8s_container"
EOF

      duration = "0s"
      comparison = "COMPARISON_GT"
      threshold_value = 0.01
      trigger {
        count = 1
      }

      aggregations {
        per_series_aligner = "ALIGN_DELTA"
        cross_series_reducer = "REDUCE_SUM"
        alignment_period = "60s"
      }
    }
  }

  notification_channels = [
    google_monitoring_notification_channel.email.id,
  ]
  enabled = true
  depends_on = [google_logging_metric.web-socket-server-error]
}

resource "google_logging_metric" "web-socket-server-error" {
  name = "k8s_container/web-socket-server"
  filter = <<EOF
resource.type="k8s_container" AND
resource.labels.container_name="web-socket-server"
textPayload: "error"
EOF
  description = "textPayload including error"

  metric_descriptor {
    metric_kind = "DELTA"
    value_type = "INT64"
  }
}

resource "google_monitoring_notification_channel" "email" {
  display_name = "kafu email"
  type = "email"
  labels = {
    email_address = "kafu.h1998@gmail.com"
  }
}
