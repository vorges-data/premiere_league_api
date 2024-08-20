from extract.extract_scrapy import extract_data
from transform.transform_scrapy import transform_data
from load.load_scrapy import load_scrapy_data_to_bigquery

def main():

    # Extração dos dados 'even' e 'odd'
    data_even, data_odd = extract_data(total_pages=4)
    
    # Transformação dos dados
    df_final = transform_data(data_odd, data_even)
    
    # Carregamento dos dados no BigQuery na nova tabela
    load_scrapy_data_to_bigquery(df_final)

if __name__ == "__main__":
    main()
