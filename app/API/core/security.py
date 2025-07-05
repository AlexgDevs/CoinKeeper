from os import getenv
from dotenv import load_dotenv, find_dotenv
from .config import app

load_dotenv(find_dotenv())

app.config['SECRET_TOKEN'] = getenv('SECRET_TOKEN')