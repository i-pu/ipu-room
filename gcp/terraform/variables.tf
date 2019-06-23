variable "project" {}

variable "docker_secret" {
  type = "map"
}

variable "credentials_file" {}

variable "zone" {}

variable "webhook" {
  type = "map"
}

variable "slack" {}
