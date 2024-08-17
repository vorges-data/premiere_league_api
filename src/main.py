from google.cloud import bigquery
from datetime import datetime, timedelta
import pandas as pd
from google.api_core.exceptions import NotFound
from src.extract.extract import fetch_data, fetch_iterable_data
from src.transform.transform import prepare_dataframe
from src.load.load import create_dataset_if_not_exists, load_data_to_bigquery
from src.config import PROJECT_ID, DATASET_NAME, HEADERS, FULL_LOAD_DATE, endpoints, iterable_endpoints

def get_last_update(client, now):
    table_name = f'{PROJECT_ID}.{DATASET_NAME}.updates'
    try:
        client.get_table(table_name)
    except NotFound:
        print(f"Table {table_name} not found. Initializing with FULL_LOAD_DATE: {FULL_LOAD_DATE}")
        full_load_date = datetime.strptime(FULL_LOAD_DATE, '%Y-%m-%d')
        initial_data = [{'updated_at': full_load_date}]
        load_data_to_bigquery(client, DATASET_NAME, 'updates', pd.DataFrame(initial_data), 'WRITE_TRUNCATE')
        return full_load_date

    query = f'SELECT MAX(updated_at) AS last_update FROM `{table_name}`'
    try:
        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            print(f"Ultima data de atualização: {row.last_update}")
            return row.last_update if row.last_update else now - timedelta(days=1)
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None

def log_update(client, now):
    table_name = f'{PROJECT_ID}.{DATASET_NAME}.updates'
    updated_at = [{'updated_at': now}]
    load_data_to_bigquery(client, DATASET_NAME, 'updates', pd.DataFrame(updated_at), 'WRITE_APPEND')

def incremental_params_update(table, incremental_load_params, params, last_update, now):
    if table == "past_fixtures":
        params.update({
            'from': last_update.strftime('%Y-%m-%d'),
            'to': (now - timedelta(days=1)).strftime('%Y-%m-%d')
        })
    elif table == "future_fixtures":
        params.update({
            'from': now.strftime('%Y-%m-%d')
        })
    return params

def main():
    client = bigquery.Client(project=PROJECT_ID)
    create_dataset_if_not_exists(client, DATASET_NAME)
    now = datetime.now()
    last_update = get_last_update(client, now)
    main_endpoints = endpoints.copy()
    main_iterable_endpoints = iterable_endpoints.copy()

    for endpoint in main_endpoints:
        params = endpoint.get('params', {})
        table = endpoint.get('table')
        incremental_load_params = endpoint.get('incremental_load_params')
        path = endpoint.get('path')
        fields = endpoint.get('fields')
        nested_fields = endpoint.get('nested_fields')
        repeatable_fields = endpoint.get('repeatable_fields')
        write_disposition = endpoint.get('write_disposition')

        if incremental_load_params:
            params = incremental_params_update(table, incremental_load_params, params, last_update, now)

        raw_data = fetch_data(path, params)

        if raw_data:
            prepared_data = prepare_dataframe(raw_data, fields, nested_fields, repeatable_fields)
            load_data_to_bigquery(client, DATASET_NAME, table, prepared_data, write_disposition)

            if table in main_iterable_endpoints:
                for iterable_endpoint in main_iterable_endpoints[table]:
                    iterable_table = iterable_endpoint.get('table')
                    iterable_fields = iterable_endpoint.get('fields')
                    iterable_nested_fields = iterable_endpoint.get('nested_fields')
                    iterable_repeatable_fields = iterable_endpoint.get('repeatable_fields')
                    iterable_write_disposition = iterable_endpoint.get('write_disposition')

                    print(f"Buscando os dados iteráveis para o endpoint: {iterable_table}")
                    detailed_data = fetch_iterable_data(prepared_data, iterable_endpoint)

                    if detailed_data:
                        prepared_iterable_data = prepare_dataframe(detailed_data, iterable_fields, iterable_nested_fields, iterable_repeatable_fields)
                        load_data_to_bigquery(client, DATASET_NAME, iterable_table, prepared_iterable_data, iterable_write_disposition)
                    else:
                        print(f"Não foram encontrados dados para o endpoint: {iterable_table}")
        else:
            print(f"Não foram encontrados dados para o endpoint: {table}")

    log_update(client, now)

if __name__ == "__main__":
    main()
