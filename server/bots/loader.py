
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from os import getenv
import psycopg2

load_dotenv()


"""async def connect():
    return psycopg2.connect(

        host=getenv('BOT_DB_HOST'),
        user=getenv('BOT_USER_DB'),
        password=getenv('BOT_PASSWORD_USER'),
        dbname=getenv('BOT_POSTGRES_DB')
        
        )"""


bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()

