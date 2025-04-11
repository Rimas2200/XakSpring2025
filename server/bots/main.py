import logging
import asyncio

#from functions.datebase_scripts import create_table_scipts
from fucnctions.handlers import routers as router_main
#from functions.authorizations import author_handlers
#from functions.sending.sending_hendlers import routers as sending_routers
#from functions.admin.admin_handler import routers as admin_router


import loader
dp = loader.dp
bot = loader.bot

dp.include_router(router=router_main)
#dp.include_router(router=author_handlers.routers)
#dp.include_router(router=sending_routers)
#dp.include_router(router=admin_router)

async def start():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        
if __name__ == '__main__':
    try:
        # create_table_scipts.check_create()
        logging.basicConfig(level=logging.INFO)
        asyncio.run(start())

    except Exception as _ex:
        print("Ошибка при работе", _ex)
