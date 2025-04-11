import asyncio


from aiogram import F, Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery




import json

routers = Router()

@routers.message(Command("start_webapp"))
async def open_webapp(message: types.Message):
    await message.answer("Webapp opened!")
    # await message.answer_web_app("https://example.com/webapp", reply_markup=bt.webapp_keyboard())
    