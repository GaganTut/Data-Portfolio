import time
import random
from datetime import datetime
from faker import Faker
from google.cloud import bigquery
from google.oauth2 import service_account

KEY_FILE = 'clickstream/credentials.json' 
credentials = service_account.Credentials.from_service_account_file(KEY_FILE)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

table_id = f"{credentials.project_id}.clickstream_raw.events"

fake = Faker()

def generate_event():
    # Create fake user_id with 10% chance of being None to simulate dirty data
    user_id = fake.uuid4() if random.random() > 0.1 else None
    
    # Generate Fake Event Data
    event = {
        "event_id": fake.uuid4(),
        "user_id": user_id,
        "event_name": random.choice(["view_item", "add_to_cart", "checkout", "signup"]),
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "client_timestamp": datetime.now().isoformat(),
        "ip_address": fake.ipv4()
    }
    print (event)
    return event

print(f"Starting stream to {table_id}...")

while True:
    # Create 5 Fake Events
    rows_to_insert = [generate_event() for _ in range(5)]
    
    # Inserting using stream api is blocked for free sandbox projects in BigQuery
    # errors = client.insert_rows_json(table_id, rows_to_insert)
    
    # if errors:
    #     print(f"Error: {errors}")
    # else:
    #     print(f"Inserted {len(rows_to_insert)} events. Total dirty rows sent: {sum(1 for r in rows_to_insert if r['user_id'] is None)}")
    
    # # Two Second Delay to Avoid Rate Limits
    # time.sleep(2)

    # Uses batch load to get around sandbox limits
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("user_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("event_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("device", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("client_timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("ip_address", "STRING", mode="NULLABLE")
        ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    try:
        job = client.load_table_from_json(rows_to_insert, table_id, job_config=job_config)
        job.result() 
        
        dirty_count = sum(1 for r in rows_to_insert if r['user_id'] is None)
        print(f"Batch loaded! {len(rows_to_insert)} events. ({dirty_count} dirty)")
        
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(5)