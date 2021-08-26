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

resource "google_storage_bucket" "closestfinder_src" {
  name          = "closestfinder_src"
  force_destroy = true
}

resource "google_storage_bucket_object" "closestfinder" {
  name   = "index.zip"
  bucket = "closestfinder_src"
  source = var.source_object
}

resource "google_cloudfunctions_function" "closestfinder" {
  name        = "closestfinder"
  description = "Find the closest pub by coordinates"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = "closestfinder_src"
  source_archive_object = "index.zip"
  trigger_http          = true
  entry_point           = "findclosest"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  region         = var.region
  cloud_function = "closestfinder"

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}