terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "taxi-data-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "ny_taxi_dataset" {
  dataset_id                  = var.bq_dataset_name
  location                    = var.location
  friendly_name               = "taxi"
  description                 = "NYC Taxi Trips Data"
  default_table_expiration_ms = 3600000
  delete_contents_on_destroy = true
}