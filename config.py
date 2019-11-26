import re
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

POOL_COUNT = 2

BOT_TOKEN = os.environ['token']
PROD_MODE = os.environ.get('mode') == 'prod'

REDIS_CONFIG = {
    "host": '127.0.0.1',
    "port": 6379,
    "password": '',
    "db": os.environ['redis_db']
}

INFO_PSQL_DB_CONFIG = {
    "DB_TYPE": "postgresql",
    "USER": "",
    "PASSWORD": "",
    "HOST": "localhost",
    "PORT": "5432",
    "DB": "info_psql",
    "echo": not PROD_MODE,
    "pool_recycle": 7200
}

BOT_PSQL_DB_CONFIG = {
    "DB_TYPE": "postgresql",
    "USER": "",
    "PASSWORD": "",
    "HOST": "localhost",
    "PORT": "5432",
    "DB": "info_bot",
    "echo": not PROD_MODE,
    "pool_recycle": 7200
# pool_recycle - По умолчанию соединение с БД через 8 часов простоя обрывается. Чтобы это не случилось нужно добавить опцию

}

BOT_ID_HANDLE_PATTERN = "^\/id_\d{1,}$"

USER_ID_HANDLE_PATTERN = "^\/user_\d{1,}$"

DEFAULT_LOCALE = 'ua'

PAGINATE_PAGE_LEN = 5
PAGINATE_MAX_LEN = 100

CSV_PATH = join(dirname(__file__), 'csvs')

if not os.path.exists(CSV_PATH):
    os.makedirs(CSV_PATH)
