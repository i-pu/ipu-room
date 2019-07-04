data "template_file" "nginx-default-conf" {
  template = file("default.conf")
  vars = {
    gke_address = var.gke_address
  }
}
resource "google_compute_instance" "default" {
  name         = "ipu-room-reverse-proxy"
  machine_type = "f1-micro"
  zone         = var.zone

  tags = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "centos-cloud/centos-7"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  metadata_startup_script = <<EOF
sudo yum -y update && \
yum -y install nginx && \
echo "${data.template_file.nginx-default-conf.rendered}" > /etc/nginx/nginx.conf && \
setsebool httpd_can_network_connect on -P && \
sudo systemctl enable nginx && \
sudo systemctl start nginx
EOF

  service_account {
    scopes = []
  }
}