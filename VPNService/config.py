import os

from dotenv import load_dotenv

load_dotenv()
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')

TEST_DB_NAME = os.environ.get('TEST_DB_NAME')
DJANGO_KEY = os.environ.get('DJANGO_KEY')

ALLOWED_URLS = ['/vpn/register/', '/vpn/login/', '/vpn/home/']
