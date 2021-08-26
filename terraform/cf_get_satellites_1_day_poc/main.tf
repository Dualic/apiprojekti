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

resource "google_storage_bucket" "get_satellites_1_src" {
  name          = "get_satellites_1_src"
  force_destroy = true
}

resource "google_storage_bucket_object" "get_satellites_1" {
  name   = "index.zip"
  bucket = "get_satellites_1_src"
  source = var.source_object
}

resource "google_cloudfunctions_function" "get_satellites_1_days" {
  name        = "get_satellites_1_days"
  description = "Get some"
  runtime     = "python37"

  available_memory_mb   = 256
  source_archive_bucket = "get_satellites_1_src"
  source_archive_object = "index.zip"
  trigger_http          = true
  entry_point           = "get_satellites"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  region         = var.region
  cloud_function = "get_satellites_1_days"

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}