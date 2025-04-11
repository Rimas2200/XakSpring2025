from aiogram import types
from aiogram.types import CallbackQuery, InputFile, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import json

from .webapp.api_handler import get_api_response
from . import mainbutton as bt

from loader import bot

routers = Router()


@routers.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!", reply_markup=bt.main_button_menu
        )


@routers.message(F.text)
async def save_messages(message: types.Message):
    message_obj = {
        "sender": message.from_user.username,
        "message": message.text,
        "userid": message.from_user.id,
        "chat_id": message.chat.id
        }
    print(message_obj)
    await get_api_response(message_obj)
    await message.answer("Сообщение сохранено в БД")

    

    
    






    
    
