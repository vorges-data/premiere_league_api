import pandas as pd
import re

def transform_data(data_odd, data_even):
    # Converter as listas em DataFrames
    df_odd = pd.DataFrame(data_odd)
    df_even = pd.DataFrame(data_even)

    # Concatenar os DataFrames 'odd' e 'even'
    df_final = pd.concat([df_odd, df_even], ignore_index=True)
    
    # Renomear as colunas
    df_final.columns = [
        'ranking', 'name_and_position', 'player_name', 'position', 'age', 
        'best_value_career', 'last_update', 'market_value', 'player_image', 
        'nation_image', 'club_image', 'club_name'
    ]

    # Remover a coluna 'name_and_position'
    df_final = df_final.drop("name_and_position", axis=1, errors="ignore")

    # Função para extrair dados com regex
    def extrair_dados(valor):
        match = re.match(r'(\d+,\d+) mi. €', valor)
        if match:
            return match.group(1)
        else:
            return None

    # Aplicar a função para extrair dados em ambas as colunas
    df_final['best_value_career'] = df_final['best_value_career'].apply(extrair_dados)
    df_final['market_value'] = df_final['market_value'].apply(extrair_dados)

    # Criar as colunas de moeda
    df_final['currency_best_value_career'] = 'mi. €'
    df_final['currency_market_value'] = 'mi. €'

    # Adicionar a coluna com a data de carregamento
    df_final['load_date'] = pd.Timestamp.now()

    # Reordenar as colunas conforme a ordem desejada
    new_columns = [
        'ranking', 'player_name', 'position', 'age', 'club_name', 
        'best_value_career', 'currency_best_value_career', 
        'market_value', 'currency_market_value', 'player_image', 
        'nation_image', 'club_image', 'last_update', 'load_date'
    ]
    df_final = df_final[new_columns]

    # Função para transformar as colunas
    def transformar_colunas(df):
        # Substituir vírgula por ponto nos valores
        df['best_value_career'] = df['best_value_career'].str.replace(',','.')
        df['market_value'] = df['market_value'].str.replace(',','.')

        # Converter os dados para tipos numéricos e de data
        df['ranking'] = pd.to_numeric(df['ranking'])
        df['age'] = pd.to_numeric(df['age'])
        df['best_value_career'] = pd.to_numeric(df['best_value_career'])
        df['market_value'] = pd.to_numeric(df['market_value'])
        df['last_update'] = pd.to_datetime(df['last_update'], format='%d/%m/%Y')

        return df

    # Aplicar a transformação nas colunas
    df_final = transformar_colunas(df_final)

    # Ordenar o DataFrame pelo ranking e resetar o índice
    df_final = df_final.sort_values('ranking', ascending=True).reset_index(drop=True)

    return df_final
