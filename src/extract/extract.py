import requests
from src.config import API_URL, HEADERS

def fetch_data(path, params, headers=HEADERS):
    all_data = []
    while True:
        response = requests.get(f"{API_URL}/{path}", headers=headers, params=params)
        data = response.json()
        if 'response' in data and data['response']:
            all_data.extend(data['response'])
            if 'page' in params:
                params['page'] += 1
            else:
                break
        else:
            break
    return all_data

def fetch_iterable_data(main_data, iterable_endpoint):
    all_data = []
    for _, item in main_data.iterrows():
        query_params = {key: item[value.replace('.', '__')] for key, value in iterable_endpoint["query_param"].items()}
        params = query_params.copy()
        params.update(iterable_endpoint['fixed_params'])
        data = fetch_data(iterable_endpoint['path'], params)
        iterated_data = [{**query_params, **item} for item in data]
        all_data.extend(iterated_data)
    return all_data
