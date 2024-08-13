import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
PROJECT_ID = os.getenv('PROJECT_ID')
DATASET_NAME = os.getenv('DATASET_NAME')
FULL_LOAD_DATE = os.getenv('FULL_LOAD_DATE')
LEAGUE = int(os.getenv('LEAGUE'))
SEASON = int(os.getenv('SEASON'))

HEADERS = {
    'x-rapidapi-key': API_KEY
}
