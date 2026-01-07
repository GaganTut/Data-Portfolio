# Basic Clickstream Analytics Pipeline (GCP + dbt)

## Overview
A simple end-to-end ELT pipeline built on **Google Cloud Platform**. Takes fake (for now) raw clickstream logs using Python micro-service (Faker), stores data in **BigQuery**, and then transforms them into "Daily Active User" metrics using **dbt**.

## Architecture
**Infrastructure:** Terraform
**Ingestion:** Python -> BigQuery
**Transformation:** dbt|

## Data Lineage
1.  **Raw Layer:** `clickstream_raw.events` (JSON logs, contains fake NULL user_ids as well)
2.  **Staging:** `clickstream_staging.stg_events` (Cleaned, typed, NULL user_ids removed)
3.  **Marts:** `clickstream_marts.daily_metrics` (Event Counts, Metrics)

## How to Run
1.  **Deploy Infra:** `terraform apply`
2.  **Start Stream:** `python ingest.py`
3.  **Transform:** `cd clickstream && dbt run`