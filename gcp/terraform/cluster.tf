resource "google_container_cluster" "node" {
  name = "${var.project}-cluster"
  location = var.zone
  initial_node_count = 1
  logging_service = "logging.googleapis.com/kubernetes"
  monitoring_service = "monitoring.googleapis.com/kubernetes"
  node_config {
    disk_size_gb = 10
    machine_type = "g1-small"
  }
}

resource "google_compute_firewall" "server-nodeport" {
  name = "${var.project}-server-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["31420"]
  }
}

resource "google_compute_firewall" "client-nodeport" {
  name = "${var.project}-client-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["31421"]
  }
}
