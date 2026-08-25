terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.45.0"
    }
  }
}

provider "google" {
  project = "project-9c55cdb0-ce48-42d5-902"
  region  = "asia-east1"
  zone    = "asia-east1-a"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "project-9c55cdb0-ce48-42d5-902-terra-bucket"
  location      = "asia-east1"
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