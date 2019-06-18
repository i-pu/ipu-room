# Repository must be created beforehand

resource "google_cloudbuild_trigger" "web-socket-server" {
  trigger_template {
    tag_name = "web-socket-server"
    repo_name = "github_i-pu_ipu"
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/web-socket-server-cloudbuild.yaml"
}

resource "google_cloudbuild_trigger" "client" {
  trigger_template {
    tag_name = "client"
    repo_name = "github_i-pu_ipu"
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/client-cloudbuild.yaml"
}

resource "google_cloudbuild_trigger" "postgres" {
  trigger_template {
    tag_name = "postgres"
    repo_name = "github_i-pu_ipu"
  }

  substitutions = {
    _ZONE = var.zone
  }

  filename = "gcp/postgres-cloudbuild.yaml"
}

resource "google_cloudbuild_trigger" "database-controller" {
  trigger_template {
    tag_name = "database-controller"
    repo_name = "github_i-pu_ipu"
  }

  substitutions = {
    _DOCKER_USERNAME = lookup(var.docker_secret, "username")
    _DOCKER_PASSWORD = lookup(var.docker_secret, "password")
    _ZONE = var.zone
  }

  filename = "gcp/database-controller-cloudbuild.yaml"
}
