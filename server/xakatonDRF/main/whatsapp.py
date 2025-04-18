from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import re

"""
from collections import defaultdict
from datetime import datetime
from docx import Document

"""


def transform_area_format(text):
    def replace_match(match):
        parts = match.group(0)
        numbers = re.findall(r'\d+', parts)
        result = []
        for i, num in enumerate(numbers):
            if i < len(numbers) - 1 or parts.endswith('га'):
                result.append(f"{num} га")
            else:
                result.append(num)
        return " ".join(result)

    area_pattern = r"\d+/\d+га\d*|\d+/\d+га|\d+га"
    return re.sub(area_pattern, replace_match, text)

  
def clean_text(text):
    text = re.sub(r'\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})г?\b', r'\1<DOT>\2<DOT>\3', text)
    text = re.sub(r'\b(\d{1,2})\.(\d{1,2})\b(?!\.\d{2,4})', r'\1<DOT>\2', text)
    text = re.sub(r'(\d)-([a-zA-Zа-яА-Я])', r'\1<SAFE_HYPHEN>\2', text)
    text = re.sub(r'(?<=\d)/(?=\d)', r'<SAFE_SLASH>', text)
    text = re.sub(r'[^\w\s<SAFE_HYPHEN><DOT><SAFE_SLASH>]', ' ', text)
    text = text.replace('<SAFE_HYPHEN>', '-').replace('<DOT>', '.').replace('<SAFE_SLASH>', '/')

    text = re.sub(r'(?i)\bпопу\b', 'По Пу', text)
    return text

    return re.sub(r'\s+', ' ', text).strip()

def setup_driver():
    profile_path = os.path.join(os.getcwd(), "chrome_profile")

    service = Service(ChromeDriverManager().install())
    FIXED_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={FIXED_USER_AGENT}")
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def wait_for_chat_load(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]'))
        )
        print("Чаты успешно загружены.")
    except Exception as e:
        print("Ошибка при ожидании загрузки чатов:", e)
        driver.quit()
        exit()


def open_chat(driver, contact_name):
    try:
        chat = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[contains(@title,"{contact_name}")]'))
        )
        chat.click()
        print(f"Чат с '{contact_name}' открыт.")
    except Exception as e:
        raise Exception(f"Чат с {contact_name} не найден. {str(e)}")


def scroll_to_top(driver):
    try:
        chat_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "copyable-area")]'))
        )
    except Exception as e:
        print("Контейнер сообщений не найден:", e)
        driver.quit()
        exit()

    old_message_count = 0
    while True:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class, "copyable-text")]')
        current_count = len(messages)
        if current_count == old_message_count:
            break
        old_message_count = current_count
        driver.execute_script("arguments[0].scrollTop = 0;", chat_container)
        time.sleep(2)


def process_messages(driver, filter_words):
    precess_message_list = []
    pre_text_pattern = re.compile(r"\[(\d{1,2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})] (.*?):")
    quote_text_pattern = re.compile(r'^\[\d{1,2}:\d{2}, \d{2}\.\d{2}\.\d{4}] .+?:')
    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}(?:\.\d{2,4})?\b')

    messages = driver.find_elements(By.XPATH, '//div[contains(@class, "copyable-text")]')
    print(f"\nНайдено сообщений: {len(messages)}\n")

    filtered_count = 0
    for msg in messages:
        try:
            msg.find_element(By.XPATH, './/div[contains(@data-testid, "quoted-message")]')
            continue
        except:
            pass

        msg_text = msg.text.strip()
        lines = msg_text.splitlines()

        if len(lines) >= 2 and lines[0].strip() == "Вы" and re.match(r'^\d{1,2}\.\d{1,2}$', lines[1].strip()):
            continue

        if any(quote_text_pattern.match(line.strip()) for line in lines):
            continue

        msg_text_lower = msg_text.lower()
        if any(re.search(rf"\b{re.escape(word)}\b", msg_text_lower) for word in filter_words):
            pre_text = msg.get_attribute("data-pre-plain-text")
            time_str, date_str, sender = "", "", ""
            if pre_text:
                match = pre_text_pattern.search(pre_text)
                if match:
                    time_str = match.group(1)
                    date_str = match.group(2)
                    sender = match.group(3)

            filtered_count += 1

            msg_single_line = " ".join(msg_text.splitlines())
            msg_single_line = clean_text(msg_single_line)
            msg_single_line = transform_area_format(msg_single_line)

            found_date = date_pattern.search(msg_single_line)
            if found_date:
                message_date = found_date.group(0)
                msg_single_line = msg_single_line.replace(message_date, '').strip()
            else:
                message_date = "17.04"

            match = re.match(rf'^(({re.escape(message_date)}\s+)+)', msg_single_line)
            if match:
                new_message = msg_single_line[match.end():].lstrip()
                output_line = f"{message_date} {new_message}"
            else:
                output_line = f"{message_date} {msg_single_line}"

            precess_message_list.append(output_line)

            try:
                with open('message.txt', 'a', encoding='utf-8') as file:
                    file.write(f"{output_line}\n")
                    #print(f"{filtered_count}. Отправитель: {sender} | Дата: {date_str} {time_str} | Дата из сообщения: {message_date}| Сообщение: {msg_single_line}")
            except FileNotFoundError as e:
                print(e)


    if filtered_count == 0:
        print("Сообщения, содержащие заданные слова, не найдены.")

    return precess_message_list
# Ручной запуск
"""
driver = setup_driver()
driver.get("https://web.whatsapp.com")

wait_for_chat_load(driver)

contact_name = input("Введите пользователя: ")
open_chat(driver, contact_name)

scroll_to_top(driver)

filter_words = [
    "попу", "аор", "тск", "мир", "восход", "ао кропоткинское",
    "колхоз прогресс", "сп коломейцево", "пу", "отд"
]
process_messages(driver, filter_words)

driver.quit()
"""