resource "google_cloudbuild_trigger" "web-socket-server" {
  trigger_template {
    repo_name = google_sourcerepo_repository.ipu-room.name
    branch_name = "web-socket-server"
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
    repo_name = google_sourcerepo_repository.ipu-room.name
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
    repo_name = google_sourcerepo_repository.ipu-room.name
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
    repo_name = google_sourcerepo_repository.ipu-room.name
  }

  filename = "gcp/cloudbuild/GCF_stackdriver2slack.yaml"
}

resource "google_cloudbuild_trigger" "reverse-proxy" {
  trigger_template {
    branch_name = "reverse-proxy"
    repo_name = google_sourcerepo_repository.ipu-room.name
  }

  substitutions = {
    _ZONE = var.zone
  }

  filename = "gcp/cloudbuild/reverse-proxy.yaml"
}

resource "google_cloudbuild_trigger" "backend" {
  trigger_template {
    branch_name = "backend"
    repo_name = google_sourcerepo_repository.ipu-room.name
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/cloudbuild/backend.yaml"
}
