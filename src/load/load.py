from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd
import json

def create_dataset_if_not_exists(client, dataset_name):
    try:
        client.get_dataset(dataset_name)
    except NotFound:
        print(f"Dataset {dataset_name} not found. Creating...")
        client.create_dataset(dataset_name)

def load_data_to_bigquery(client, dataset_name, table_name, data, write_disposition):
    table_ref = client.dataset(dataset_name).table(table_name)
    try:
        table = client.get_table(table_ref)
        schema = table.schema
    except NotFound:
        schema = None
        print(f"Schema for table {dataset_name}.{table_name} not found.")

    job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)
    if schema:
        job_config.schema = schema
    else:
        job_config.autodetect = True

    json_str = data.to_json(orient='records', date_format='iso')
    job = client.load_table_from_json(json.loads(json_str), table_ref, job_config=job_config)
    job.result()
    print(f"{len(data)} rows loaded into {dataset_name}.{table_name}")
