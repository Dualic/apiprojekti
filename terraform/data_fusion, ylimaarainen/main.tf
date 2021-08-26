terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.75.0"
    }
  }
}

provider "google-beta" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_data_fusion_instance" "apifusion" {
  provider = google-beta
  name = "apifusion"
  description = "Data Fusion instance"
  region = var.region
  type = "BASIC"
  enable_stackdriver_logging = true
  enable_stackdriver_monitoring = true
  private_instance = false
  version = "6.4.1"
  dataproc_service_account = data.google_app_engine_default_service_account.default.email
}

data "google_app_engine_default_service_account" "default" {
  provider = google-beta
}