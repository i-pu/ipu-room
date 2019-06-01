provider "google" {
  project = "${var.project}"
  credentials = "${file("${var.credentials_file}")}"
}
