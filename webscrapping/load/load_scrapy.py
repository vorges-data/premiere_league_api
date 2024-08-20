from google.cloud import bigquery
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

def load_scrapy_data_to_bigquery(df):
    project_id = os.getenv('PROJECT_ID')
    dataset_name = os.getenv('DATASET_NAME')
    table_name = os.getenv('SCRAPING_TABLE_NAME')
    
    table_id = f"{project_id}.{dataset_name}.{table_name}"
    
    client = bigquery.Client()

    # Verificar se a tabela já existe; se não, cria
    try:
        client.get_table(table_id)
        print(f"Tabela {table_id} já existe. Carregando dados.")
    except:
        schema = [
            bigquery.SchemaField("ranking", "INTEGER"),
            bigquery.SchemaField("player_name", "STRING"),
            bigquery.SchemaField("position", "STRING"),
            bigquery.SchemaField("age", "INTEGER"),
            bigquery.SchemaField("club_name", "STRING"),
            bigquery.SchemaField("best_value_career", "FLOAT"),
            bigquery.SchemaField("currency_best_value_career", "STRING"),
            bigquery.SchemaField("market_value", "FLOAT"),
            bigquery.SchemaField("currency_market_value", "STRING"),
            bigquery.SchemaField("player_image", "STRING"),
            bigquery.SchemaField("nation_image", "STRING"),
            bigquery.SchemaField("club_image", "STRING"),
            bigquery.SchemaField("last_update", "DATE"),
            bigquery.SchemaField("load_date", "TIMESTAMP"),  # Nova coluna adicionada ao esquema
        ]
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table)
        print(f"Tabela {table_id} criada com sucesso.")

    # Carregar os dados no BigQuery
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Aguarda o término do job de carregamento
    
    table = client.get_table(table_id)  # Obtém o schema da tabela
    print(f"Carregado {table.num_rows} linhas para a tabela {table_id}.")
