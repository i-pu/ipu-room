# Repository must be created beforehand

resource "google_cloudbuild_trigger" "web-socket-server" {
  trigger_template {
    tag_name = "web-socket-server-cd"
    repo_name = "github_i-pu_ipu"
  }

  substitutions = {
    _DOCKER_USERNAME = "${lookup(var.docker_secret, "username")}"
    _DOCKER_PASSWORD = "${lookup(var.docker_secret, "password")}"
    _ZONE = "${var.zone}"
  }

  filename = "gcp/web-socket-server-cd-cloudbuild.yaml"
}

resource "google_cloudbuild_trigger" "client" {
  trigger_template {
    tag_name = "client-cd"
    repo_name = "github_i-pu_ipu"
  }

  substitutions = {
    _DOCKER_USERNAME = "${lookup(var.docker_secret, "username")}"
    _DOCKER_PASSWORD = "${lookup(var.docker_secret, "password")}"
    _ZONE = "${var.zone}"
  }

  filename = "gcp/client-cd-cloudbuild.yaml"
}
