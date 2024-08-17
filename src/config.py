# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
PROJECT_ID = os.getenv('PROJECT_ID')
DATASET_NAME = os.getenv('DATASET_NAME')
FULL_LOAD_DATE = os.getenv('FULL_LOAD_DATE')
LEAGUE = int(os.getenv('LEAGUE'))
SEASON = int(os.getenv('SEASON'))

# Definir HEADERS aqui
HEADERS = {
    'x-rapidapi-key': API_KEY
}

endpoints = [
    {
        "table": "past_fixtures", # Nome da tabela no BigQuery
        "write_disposition": "WRITE_APPEND", # Define o método de escrita no BigQuery (append)
        "path": "fixtures", # Caminho do endpoint na API-Sports
        "quality_control": False, # Flag para controle de qualidade (não utilizado neste caso)
        "params": { # Parâmetros da requisição para a API-Sports
            "league": LEAGUE,
            "season": SEASON
        },
        "incremental_load_params": { # Parâmetros para a carga incremental
            "from": "YYYY-MM-DD", # Data de início para a carga incremental
            "to": "YYYY-MM-DD" # Data de fim para a carga incremental
        },
        "fields": [], # Campos a serem selecionados na resposta da API (não utilizado neste caso)
        "nested_fields": [ # Campos aninhados a serem extraídos da resposta da API
            "fixture.id",
            "fixture.referee",
            "fixture.timezone",
            "fixture.date",
            "fixture.timestamp",
            "fixture.periods.first",
            "fixture.periods.second",
            "fixture.venue.id",
            "fixture.venue.name",
            "fixture.venue.city",
            "fixture.status.long",
            "fixture.status.short",
            "fixture.status.elapsed",
            "league.id",
            "league.name",
            "league.country",
            "league.logo",
            "league.flag",
            "league.season",
            "league.round",
            "teams.home.id",
            "teams.home.name",
            "teams.home.logo",
            "teams.home.winner",
            "teams.away.id",
            "teams.away.name",
            "teams.away.logo",
            "teams.away.winner",
            "goals.home",
            "goals.away",
            "score.halftime.home",
            "score.halftime.away",
            "score.fulltime.home",
            "score.fulltime.away",
            "score.extratime.home",
            "score.extratime.away",
            "score.penalty.home",
            "score.penalty.away"
        ],
        "repeatable_fields": [] # Campos que se repetem na resposta da API (não utilizado neste caso)
    },
    # Próximos endpoints seguem a mesma estrutura do anterior
    {
        "table": "future_fixtures",
        "write_disposition": "WRITE_TRUNCATE", # Define o método de escrita no BigQuery (truncate)
        "path": "fixtures",
        "quality_control": False,
        "params": {
            "league": LEAGUE,
            "season": SEASON,
            "to": "2099-12-31"
        },
        "incremental_load_params": {
            "from": "YYYY-MM-DD",
        },
        "fields": [],
        "nested_fields": [
            "fixture.id",
            "fixture.timezone",
            "fixture.date",
            "fixture.timestamp",
            "fixture.venue.id",
            "fixture.venue.name",
            "fixture.venue.city",
            "fixture.status.long",
            "fixture.status.short",
            "league.id",
            "league.name",
            "league.country",
            "league.logo",
            "league.flag",
            "league.season",
            "league.round",
            "teams.home.id",
            "teams.home.name",
            "teams.home.logo",
            "teams.away.id",
            "teams.away.name",
            "teams.away.logo"
        ],
        "repeatable_fields": []
    },
    {
        "table": "players",
        "write_disposition": "WRITE_TRUNCATE", # Define o método de escrita no BigQuery (truncate)
        "path": "players",
        "quality_control": True, # Flag para controle de qualidade (não utilizado neste caso)
        "params": {
            "league": LEAGUE,
            "season": SEASON,
            "page": 1 # Número da página de resultados da API
        },
        "fields": [],
        "nested_fields": [
            "player.id",
            "player.name",
            "player.firstname",
            "player.lastname",
            "player.age",
            "player.birth.date",
            "player.birth.place",
            "player.nationality",
            "player.height",
            "player.weight",
            "player.injured",
            "player.photo"
        ],
        "repeatable_fields": []
    },
]

# Define os endpoints da API a serem consumidos de forma iterativa,
# ou seja, para cada item do endpoint principal, este endpoint será chamado
iterable_endpoints = {
    "past_fixtures": [ # Define os endpoints iteráveis para o endpoint "past_fixtures"
        {
            "table": "fixturesStatistics", # Nome da tabela no BigQuery
            "write_disposition": "WRITE_APPEND", # Define o método de escrita no BigQuery (append)
            "path": "fixtures/statistics", # Caminho do endpoint na API-Sports
            "query_param": { # Define o parâmetro da requisição para a API-Sports que será usado para iterar sobre os dados do endpoint principal
                "fixture": "fixture.id" # O valor do campo "fixture.id" do endpoint principal será usado como valor para o parâmetro "fixture" da requisição
            },
            "fixed_params": {}, # Parâmetros fixos da requisição para a API-Sports
            "fields": ["fixture"], # Campos a serem selecionados na resposta da API
            "nested_fields": [ # Campos aninhados a serem extraídos da resposta da API
                "team.id",
                "team.name",
                "team.logo"
            ],
            "repeatable_fields": [ # Campos que se repetem na resposta da API
                "statistics"
            ]
        },
        {
            "table": "fixturesLineups", # Nome da tabela no BigQuery
            "write_disposition": "WRITE_APPEND", # Define o método de escrita no BigQuery (append)
            "path": "fixtures/lineups", # Caminho do endpoint na API-Sports
            "query_param": { # Define o parâmetro da requisição para a API-Sports que será usado para iterar sobre os dados do endpoint principal
                "fixture": "fixture.id" # O valor do campo "fixture.id" do endpoint principal será usado como valor para o parâmetro "fixture" da requisição
            },
            "fixed_params": {}, # Parâmetros fixos da requisição para a API-Sports
            "fields": [ # Campos a serem selecionados na resposta da API
                "fixture",
                "formation"
            ],
            "nested_fields": [ # Campos aninhados a serem extraídos da resposta da API
                "team.id"
            ],
            "repeatable_fields": [ # Campos que se repetem na resposta da API
                "startXI"
            ]
        }
    ]
}