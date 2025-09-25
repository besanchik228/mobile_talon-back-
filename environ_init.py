from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

SECRET_KEY = getenv('SECRET_KEY')
if not SECRET_KEY: SECRET_KEY = None

ACCESS_TOKEN_TIME = getenv('ACCESS_TOKEN_TIME')
if not ACCESS_TOKEN_TIME: ACCESS_TOKEN_TIME = None

ALGORITHM = getenv('ALGORITHM')
if not ALGORITHM: ALGORITHM = None

DATA_ADDRESS = getenv('DATA_ADDRESS')
if not DATA_ADDRESS: DATA_ADDRESS = None
