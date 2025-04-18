import asyncio
from aiogram import types
from aiogram.types import CallbackQuery, InputFile, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import os
from .webapp.api_handler import save_message_post, save_photo_post

from loader import bot

routers = Router()


@routers.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!"
        )


@routers.message(F.text)
async def save_messages(message: types.Message):
    print(message, 'message.text)')

    message_obj = {
        "sender": message.from_user.username,
        "message": message.text,
        "userid": message.from_user.id,
        "chat_id": message.chat.id
        }
    

    print(message_obj)
    await save_message_post(message_obj)
    


@routers.message(F.photo)
async def save_photo(message: types.Message):
    
    DOWNLOADS_DIR = 'download'
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

    photo = message.photo[-1]
    message_caption = message.caption if message.caption else "No caption"
    

    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    download_path = os.path.join(DOWNLOADS_DIR, f"{file_id}.jpg")
    
    message_obj = {
        "sender": message.from_user.username,
        "message": message_caption,
        "userid": message.from_user.id,
        "chat_id": message.chat.id
        }
    await bot.download_file(file_path, download_path)
    await asyncio.sleep(16)
    await save_photo_post(date=message_obj, files_path=download_path)
    
    



    
    








    
    
