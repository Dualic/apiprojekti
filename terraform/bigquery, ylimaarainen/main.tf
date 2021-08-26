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

resource "google_bigquery_dataset" "breweries" {
  dataset_id                  = "Breweries"
  description                 = "This is a test description"
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

  schema = <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "street",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "city",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "longitude",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "latitude",
    "type": "FLOAT",
    "mode": "NULLABLE"
  }
]
EOF

}