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

resource "google_api_gateway_api" "pub-api" {
  provider = google-beta
  api_id   = "pub-api"
}

resource "google_api_gateway_api_config" "api-config" {
  provider      = google-beta
  api           = "pub-api"
  api_config_id = "api-config"

  openapi_documents {
    document {
      path     = var.path
      contents = filebase64(var.contents_file)
    }
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "api-gw-gw" {
  provider   = google-beta
  api_config = google_api_gateway_api_config.api-config.id
  gateway_id = "api-gw-gw"
}
