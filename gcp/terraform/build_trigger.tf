# Repository must be created beforehand

resource "google_cloudbuild_trigger" "web-socket-server" {
  trigger_template {
    branch_name = "web-socket-server"
    repo_name = var.repository
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/cloudbuild/web-socket-server.yaml"
}

resource "google_cloudbuild_trigger" "client" {
  trigger_template {
    branch_name = "client"
    repo_name = var.repository
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/cloudbuild/client.yaml"
}

# resource "google_cloudbuild_trigger" "postgres" {
#   trigger_template {
#     branch_name = "postgres"
#     repo_name = var.repository
#   }
#
#   substitutions = {
#     _ZONE = var.zone
#   }
#
#   filename = "gcp/cloudbuild/postgres.yaml"
# }

resource "google_cloudbuild_trigger" "database-controller" {
  trigger_template {
    branch_name = "database-controller"
    repo_name = var.repository
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/cloudbuild/database-controller.yaml"
}

resource "google_cloudbuild_trigger" "functions_stackdriver2slack" {
  trigger_template {
    branch_name = "stackdriver2slack"
    repo_name = var.repository
  }

  filename = "gcp/cloudbuild/GCF_stackdriver2slack.yaml"
}

resource "google_cloudbuild_trigger" "reverse-proxy" {
  trigger_template {
    branch_name = "reverse-proxy"
    repo_name = var.repository
  }

  substitutions = {
    _ZONE = var.zone
  }

  filename = "gcp/cloudbuild/reverse-proxy.yaml"
}
