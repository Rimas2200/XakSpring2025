from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import re
from collections import defaultdict
from datetime import datetime
from docx import Document

# Преобразование формата площади (например, '5/10га' -> '5 га 10')
def transform_area_format(text):
    def replace_match(match):
        parts = match.group(0)
        numbers = re.findall(r'\d+', parts)
        result = []
        for i, num in enumerate(numbers):
            # все, кроме последнего, добавляем 'га'
            if i < len(numbers) - 1 or parts.endswith('га'):
                result.append(f"{num} га")
            else:
                result.append(num)
        return " ".join(result)

    area_pattern = r"\d+/\d+га\d*|\d+/\d+га|\d+га"
    return re.sub(area_pattern, replace_match, text)

# Очистка текста: защита дат, дефисов, слэшей, замена 'попу' -> 'По Пу'
def clean_text(text):
    # Обработка даты в формате дд.мм.гг или дд.мм.гггг с необязательной буквой "г"
    text = re.sub(r'\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})г?\b', r'\1<DOT>\2<DOT>\3', text)

    # Обработка даты в формате дд.мм без года
    text = re.sub(r'\b(\d{1,2})\.(\d{1,2})\b(?!\.\d{2,4})', r'\1<DOT>\2', text)

    # Защита от разрыва чисел и букв
    text = re.sub(r'(\d)-([a-zA-Zа-яА-Я])', r'\1<SAFE_HYPHEN>\2', text)

    # Защита слэшей в числовых парах
    text = re.sub(r'(?<=\d)/(?=\d)', r'<SAFE_SLASH>', text)

    # Удаляем все символы кроме букв, цифр, пробелов и защищённых символов
    text = re.sub(r'[^\w\s<SAFE_HYPHEN><DOT><SAFE_SLASH>]', ' ', text)

    # Восстановление защищённых символов
    text = text.replace('<SAFE_HYPHEN>', '-').replace('<DOT>', '.').replace('<SAFE_SLASH>', '/')

    # Спец-замена
    text = re.sub(r'(?i)\bпопу\b', 'По Пу', text)

    # Удаляем лишние пробелы
    return re.sub(r'\s+', ' ', text).strip()

# Сохранение в отдельные .docx-файлы
def save_messages_to_word(messages, output_dir='messages'):
    os.makedirs(output_dir, exist_ok=True)
    counters = defaultdict(int)

    for msg in messages:
        sender = msg['sender']
        text = msg['text']
        dt = msg['datetime']
        counters[sender] += 1

        safe_sender = re.sub(r'[\\/:\*\?"<>|]', '_', sender)
        suffix = f"{dt.minute:02d}{dt.hour:02d}{dt.day:02d}{dt.month:02d}{dt.year}"
        filename = f"{safe_sender}_{counters[sender]}_{suffix}.docx"
        path = os.path.join(output_dir, filename)

        doc = Document()
        doc.add_paragraph(text)
        doc.save(path)
        print(f"Сохранено: {path}")

# Настройка Selenium profile и драйвера
profile_path = os.path.join(os.getcwd(), "chrome_profile")
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com")
print("Если первый запуск — отсканируйте QR-код.")

# Ждём загрузки чатов
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]'))
)

contact_name = input("Введите пользователя или группу: ")
# Открываем чат
chat = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]'))
)
chat.click()
print(f"Чат с '{contact_name}' открыт.")

# Находим контейнер сообщений и скроллим вверх
chat_container = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "copyable-area")]'))
)
old_count = 0
while True:
    msgs = driver.find_elements(By.XPATH, '//div[contains(@class, "copyable-text")]')
    if len(msgs) == old_count:
        break
    old_count = len(msgs)
    driver.execute_script("arguments[0].scrollTop = 0;", chat_container)
    time.sleep(1)

# Регулярки и фильтры
pre_pattern   = re.compile(r"\[(\d{1,2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})] (.*?):")
quote_pattern = re.compile(r'^\[\d{1,2}:\d{2}, \d{2}\.\d{2}\.\d{4}] .+?:')
date_pattern  = re.compile(r'\b\d{1,2}\.\d{1,2}(?:\.\d{2,4})?\b')
filter_words  = ["попу","аор","тск","мир","восход","ао кропоткинское",
                  "колхоз прогресс","сп коломейцево","пу","отд"]

messages_data = []
filtered = 0

for msg in driver.find_elements(By.XPATH, '//div[contains(@class, "copyable-text")]'):
    # пропускаем цитаты
    if msg.find_elements(By.XPATH, './/div[contains(@data-testid, "quoted-message")]'):
        continue

    text_raw = msg.text.strip()
    if not text_raw:
        continue

    # фильтр по словам
    if not any(re.search(rf"\b{re.escape(w)}\b", text_raw.lower()) for w in filter_words):
        continue

    pre = msg.get_attribute("data-pre-plain-text") or ""
    m = pre_pattern.search(pre)
    if not m:
        continue
    time_str, date_str, sender = m.group(1), m.group(2), m.group(3)

    # очистка и трансформация
    single = clean_text(" ".join(text_raw.splitlines()))
    single = transform_area_format(single)

    # извлечение даты из текста и обрезка в начале
    dm = date_pattern.search(single)
    if dm:
        msg_date = dm.group(0)
        single = single.replace(msg_date, "").strip()
    else:
        # если нет, то без года
        msg_date = datetime.now().strftime("%d.%m")

    # формируем строку для файла
    output_line = f"{msg_date} {single}"
    try:
        with open('message.txt', 'a', encoding='utf-8') as f:
            f.write(output_line + "\n")
        filtered += 1
        print(f"{filtered}. Отправитель: {sender} | Метка: {date_str} {time_str} | Дата сообщения: {msg_date} | Текст: {single}")
    except Exception as e:
        print("Ошибка записи message.txt:", e)

    # парсим datetime для Word
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    except:
        dt = datetime.now()

    messages_data.append({'sender': sender, 'text': single, 'datetime': dt})

# сохраняем в Word
if messages_data:
    save_messages_to_word(messages_data)
else:
    print("Нет сообщений для сохранения.")

driver.quit()
