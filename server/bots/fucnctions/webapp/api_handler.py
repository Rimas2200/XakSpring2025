import requests
from dotenv import load_dotenv
import os

load_dotenv()


async def save_message_post(date: object) -> None:
    url = os.getenv('API_URL_SAVE_MESSAGES')
    response = requests.post(
        url=url,
        data=date,
        )


async def save_photo_post(date: object, files_path: str) -> None:
    url = os.getenv('API_URL_SAVE_PHOTO')
    files = {'photo': open(files_path, 'rb')}

    response = requests.post(
        url=url,
        data=date,
        files=files,
        )
    
    
    