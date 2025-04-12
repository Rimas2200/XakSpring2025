import requests
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()



async def get_api_response(date):
    url = os.getenv('API_URL_SAVE_MESSAGES')
    print(url)
    print(date)
    requests.post(
        url=url,
        data=date,
        )
    