from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

main_button_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="ВебПриложение",
                web_app=WebAppInfo(url=f'https://google.com')
            ),
        ],
    ]
)

