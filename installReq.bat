@echo off
:: Этот скрипт создает виртуальную среду, устанавливает зависимости и активирует её.

:: 1. Создаем виртуальное окружение

python -m venv .venv

:: 2. Активируем виртуальную среду
call .venv\Scripts\activate

:: 3. Устанавливаем зависимости из requirements.txt
if exist req.txt (
    pip install -r req.txt
) else (
    echo file req.txt in not dir.

)

cd server
cd xakatonDRF

:: Проверка наличия Python

:: Проверка файла .env
if not exist .env (
    echo File The .env was not found. Do you want to create it?
    set /p choice=
    if /i "%choice%"=="Y" (
        echo SECRET_KEY= > .env
        echo DEBUG=True >> .env
        echo DATABASE_NAME= >> .env
        echo DATABASE_USER= >> .env
        echo DATABASE_PASSWORD= >> .env
        echo DATABASE_HOST=localhost >> .env
        echo DATABASE_PORT=5432 >> .env
        echo BOT_TOKEN= >> .env
        
        echo API_URL_SAVE_MESSAGES= >> .env
        echo API_URL_SAVE_PHOTO= >> .env

        echo file create.

    ) else (
        echo OPERATION EXIT
        pause
        exit /b 1
    )
)
