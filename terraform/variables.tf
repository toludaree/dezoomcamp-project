locals {
  gcs_bucket_name = "gharchive_bucket"
}

variable "project" {
  description = "GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources"
  default = "europe-west6"
}