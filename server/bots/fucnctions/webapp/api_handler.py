import aiohttp
import requests
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


async def save_message_post(date: object) -> None:
    url = os.getenv('API_URL_SAVE_MESSAGES')
    try:
        # Асинхронный POST-запрос
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=date) as response:
                if response.status == 200:
                    print("Сообщение успешно отправлено")
                else:
                    print(f"Ошибка при отправке сообщения: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Ошибка при выполнении запроса: {e}")


async def save_photo_post(date: object, files_path: str) -> None:
    url = os.getenv('API_URL_SAVE_PHOTO')
    
    # Открываем файл с использованием контекстного менеджера
    async with aiohttp.ClientSession() as session:
        try:
            # Создаем объект FormData для отправки файла
            form_data = aiohttp.FormData()
            form_data.add_field('photo', open(files_path, 'rb'), filename=os.path.basename(files_path))
            
            # Добавляем другие данные (если они есть)
            for key, value in date.items():
                form_data.add_field(key, str(value))
            
            print(files_path, 'files_path')
            
            # Асинхронный POST-запрос
            async with session.post(url=url, data=form_data) as response:
                if response.status == 200 or 201:
                    print("Файл успешно отправлен")
                else:
                    print(f"Ошибка при отправке файла: {response.status , response.text}")  
        
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        
        finally:
            # Ждем 4 секунды перед удалением файла
            await asyncio.sleep(4)
            
            # Удаляем файл
            try:
                os.remove(files_path)
                print(f"Файл {files_path} успешно удален")
            except PermissionError as e:
                print(f"Ошибка при удалении файла: {e}")