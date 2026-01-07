# 1. Setup the Google Provider

provider "google" {
  credentials = file("clickstream/credentials.json")
  project     = "gagan-data-portfolio"
  region      = "us-central1"
}

# 2. Create Dataset for Raw Data

resource "google_bigquery_dataset" "raw_data" {
  dataset_id                  = "clickstream_raw"
  friendly_name               = "Raw Clickstream Data"
  description                 = "Raw JSON logs"
  location                    = "US"
  
  default_table_expiration_ms = 86400000
  default_partition_expiration_ms = 86400000
  
  labels = {
    env = "dev"
    finops = "free-tier"
  }
}

# 3. Create Dataset for CLeaned Data

resource "google_bigquery_dataset" "marts" {
  dataset_id                  = "clickstream_marts"
  friendly_name               = "Clickstream Marts"
  description                 = "Business intelligence ready tables"
  location                    = "US"
  
  default_table_expiration_ms = 86400000
  default_partition_expiration_ms = 86400000
}

# 4. Create Events Table

resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.raw_data.dataset_id
  table_id   = "events"
  deletion_protection = false 

  schema = jsonencode([
    {
      name = "event_id",
      type = "STRING",
      mode = "REQUIRED",
      description = "Unique ID for event"
    },
    {
      name = "user_id",
      type = "STRING",
      mode = "NULLABLE", 
      description = "User ID (null for guest users)"
    },
    {
      name = "event_name",
      type = "STRING",
      mode = "REQUIRED"
    },
    {
      name = "device",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "client_timestamp",
      type = "TIMESTAMP",
      mode = "REQUIRED"
    },
    {
      name = "ip_address",
      type = "STRING",
      mode = "NULLABLE"
    }
  ])
}