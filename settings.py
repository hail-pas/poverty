import logging
import os
import sys

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.redis import RedisIntegration
from starlette.templating import Jinja2Templates

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = os.getenv('DEBUG') == 'True'
ADMIN_SECRET = os.getenv("ADMIN_SECRET")
API_SECRET = os.getenv("API_SECRET")

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', 3306)
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Tortoise

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': DB_HOST,
                'port': DB_PORT,
                'user': DB_USER,
                'password': DB_PASSWORD,
                'database': DB_NAME,
                'echo': os.getenv('DB_ECHO') == 'True',
                'maxsize': 10,
            }
        },
    },
    'apps': {
        'models': {
            'models': ['db.models'],
            'default_connection': 'default',
        }
    }
}

# redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

REDIS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
    'db': 2,
    'encoding': 'utf-8'
}

ARQ = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
    'database': 1,
}

# log
LOGGER = logging.getLogger('apps')
if DEBUG:
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
LOGGER.addHandler(sh)

# Templates
templates = Jinja2Templates(directory="templates")

SERVER_URL = os.getenv("SERVER_URL")
