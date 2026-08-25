variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    default = "demo_dataset"
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    default = "project-9c55cdb0-ce48-42d5-902-terra-bucket"
}

variable "gcs_storage_class" {
    description = "Bucket Storage Class"
    default = "STANDARD"
  
}