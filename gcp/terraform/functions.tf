resource "google_cloudfunctions_function" "stackdriver2slack" {
  name                  = "stackdriver2slack"
  description           = "slack error notification"
  runtime               = "python37"
  # us-west1 がないため
  region                 = "us-east1"

  available_memory_mb   = 128
  trigger_http          = true
  timeout               = 10
  entry_point           = "entry_point"

  source_repository {
    url = "https://source.developers.google.com/projects/${var.project}/repos/github_i-pu_ipu/moveable-aliases/stackdriver2slack/paths/gcp/functions/stackdriver2slack"
  }

  environment_variables = {
    BASICAUTH_USERNAME = var.webhook.username
    BASICAUTH_PASSWORD = var.webhook.password
    SLACK_CHANNEL = var.slack
  }
}
