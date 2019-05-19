provider "google" {
  project = "ipu-project"
  credentials = "${file("${var.credentials_file}")}"
}

resource "google_container_cluster" "node" {
  name = "ipu-cluster"
  location = "${var.zone}"
  initial_node_count = 1
  node_config {
    disk_size_gb = 10
    machine_type = "g1-small"
  }
}

resource "google_compute_firewall" "server-nodeport" {
  name = "ipu-server-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["31420"]
  }
}

resource "google_compute_firewall" "client-nodeport" {
  name = "ipu-client-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["31421"]
  }
}
