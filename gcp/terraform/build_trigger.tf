resource "google_cloudbuild_trigger" "server" {
  trigger_template {
    tag_name = "gcb"
    repo_name = "github_i-pu_ipu"
    # Repository must be created beforehand
  }

  substitutions = {
    _DOCKER_USERNAME = "${lookup(var.docker_secret, "username")}"
    _DOCKER_PASSWORD = "${lookup(var.docker_secret, "password")}"
    _ZONE = "${var.zone}"
  }

  filename = "gcp/cloudbuild.yaml"
}
