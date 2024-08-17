from google.cloud import bigquery
import json
import pandas as pd
from google.api_core.exceptions import NotFound
from src.config import DATASET_NAME

def create_dataset_if_not_exists(client, dataset_name):
    try:
        client.get_dataset(dataset_name)
    except NotFound:
        print(f"Dataset {dataset_name} not found. Creating...")
        client.create_dataset(dataset_name)

def get_table_schema(client, dataset_name, table_name):
    table_ref = client.dataset(dataset_name).table(table_name)
    table = client.get_table(table_ref)
    return table.schema

def load_data_to_bigquery(client, dataset_name, table_name, data, write_disposition, partition_column=None, clustering_fields=None):
    table_ref = client.dataset(dataset_name).table(table_name)

    try:
        table = client.get_table(table_ref)
        schema = table.schema
    except NotFound:
        schema = None
        print(f"Schema para a tabela {DATASET_NAME}.{table_name} não encontrada.")

    job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)
    if schema:
        job_config.schema = schema
    else:
        job_config.autodetect = True

    json_str = data.to_json(orient='records', date_format='iso')
    job = client.load_table_from_json(json.loads(json_str), table_ref, job_config=job_config)
    job.result()
    print(f"Foram carregadas {len(data)} linhas em {dataset_name}.{table_name}")

def log_update(client, now):
    table_name = f'{DATASET_NAME}.updates'
    updated_at = [{'updated_at': now}]
    load_data_to_bigquery(client, DATASET_NAME, 'updates', pd.DataFrame(updated_at), 'WRITE_APPEND')
