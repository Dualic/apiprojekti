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

resource "google_storage_bucket" "datapipeline_src" {
  name          = "datapipeline_src"
  force_destroy = true
}

resource "google_storage_bucket_object" "datapipeline" {
  name   = "index.zip"
  bucket = "datapipeline_src"
  source = var.source_object
}

resource "google_storage_bucket" "breweries_data" {
  name          = "breweries_data"
  force_destroy = true
}

resource "google_bigquery_dataset" "breweries" {
  dataset_id                  = "Breweries"
  description                 = "Dataset for breweries"
  default_table_expiration_ms = 3600000

  labels = {
    env = "breweries"
  }
}

resource "google_bigquery_table" "names" {
  dataset_id = google_bigquery_dataset.breweries.dataset_id
  table_id   = "names"

  labels = {
    env = "names"
  }
}


resource "google_cloudfunctions_function" "datapipeline" {
  name        = "datapipeline"
  description = "Data from db to storage to BQ"
  runtime     = "python37"

  available_memory_mb   = 256
  source_archive_bucket = "datapipeline_src"
  source_archive_object = "index.zip"
  trigger_http          = true
  entry_point           = "main"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  region         = var.region
  cloud_function = "datapipeline"

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}