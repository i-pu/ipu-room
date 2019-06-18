resource "google_kms_key_ring" "gcb" {
  name     = "gcb"
  project = var.project
  location = "global"
}

resource "google_kms_crypto_key" "helm" {
  name            = "helm"
  key_ring        = google_kms_key_ring.gcb.self_link
}