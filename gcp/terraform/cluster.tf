provider "google" {
  project = "cka-practice-kafu"
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

resource "google_compute_firewall" "nodeport" {
  name = "ipu-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["31420"]
  }
}
