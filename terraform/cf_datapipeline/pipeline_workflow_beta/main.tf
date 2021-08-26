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

provider "google-beta" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_service_account" "terra" {
  account_id   = "my-account"
  display_name = "Terra-acco"
}

resource "google_workflows_workflow" "pipeline-workflow" {
  provider = google-beta
  name            = "pipeline-workflow"
  region          = var.region
  description     = "Magic"
  service_account = google_service_account.terra.id
  source_contents = <<-EOF
  - pipeline_function:
      call: http.get
      args:
        url: https://us-central1-leo820.cloudfunctions.net/datapipeline
      result: OK
EOF
}