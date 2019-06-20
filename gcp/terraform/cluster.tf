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

resource "google_compute_firewall" "client" {
  name = "client-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["30000"]
  }
}

resource "google_compute_firewall" "web-socket-server" {
  name = "web-socket-server-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["30008"]
  }
}

resource "google_compute_firewall" "database-controller" {
  name = "database-controller-nodeport"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["30888"]
  }
}
