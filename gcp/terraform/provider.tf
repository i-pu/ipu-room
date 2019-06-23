provider "google" {
  project = var.project
  credentials = file(var.credentials_file)
  version = "~> 2.0"
  zone = var.zone
}
