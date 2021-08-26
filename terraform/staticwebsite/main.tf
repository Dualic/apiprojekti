terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_storage_bucket" "publicstaticwebsite" {
  name          = "publicstaticwebsite"
  force_destroy = true
}

resource "google_storage_bucket_object" "get_satellites" {
  name   = "index.html"
  bucket = "publicstaticwebsite"
  source = var.source_object
}