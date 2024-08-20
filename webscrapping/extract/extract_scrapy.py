import requests
from bs4 import BeautifulSoup

def extract_data(total_pages=4):
    base_url = "https://www.transfermarkt.com.br"
    initial_page = "/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/land_id/0/plus/1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    data_even = []
    data_odd = []
    
    for page in range(1, total_pages + 1):
        if page == 1:
            url = base_url + initial_page
        else:
            url = f"{base_url}/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/land_id/0/plus/1/page/{page}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tabela = soup.find_all('table')[1]

        # Capturar linhas com classe 'even'
        rows_even = tabela.find_all('tr', attrs={'class': 'even'})
        # Capturar linhas com classe 'odd'
        rows_odd = tabela.find_all('tr', attrs={'class': 'odd'})
        
        # Processar linhas 'even'
        for row in rows_even:
            data_rows = row.findAll('td')
            img_data_src = row.find('img', {'class': 'bilderrahmen-fixed'}).get('data-src')
            img_src_flag = row.find('img', {'class': 'flaggenrahmen'}).get('src')
            img_src_club = row.find('img', {'class': ''}).get('src')
            club_name = row.find_all('a', {'title': True})[1].get('title')
            
            data_rows = [ele.text.strip() for ele in data_rows]
            data_row = [ele for ele in data_rows if ele]
            data_row.extend([img_data_src, img_src_flag, img_src_club, club_name])
            
            data_even.append(data_row)

        # Processar linhas 'odd'
        for row in rows_odd:
            data_rows = row.findAll('td')
            img_data_src = row.find('img', {'class': 'bilderrahmen-fixed'}).get('data-src')
            img_src_flag = row.find('img', {'class': 'flaggenrahmen'}).get('src')
            img_src_club = row.find('img', {'class': ''}).get('src')
            club_name = row.find_all('a', {'title': True})[1].get('title')
            
            data_rows = [ele.text.strip() for ele in data_rows]
            data_row = [ele for ele in data_rows if ele]
            data_row.extend([img_data_src, img_src_flag, img_src_club, club_name])
            
            data_odd.append(data_row)
    
    return data_even, data_odd
