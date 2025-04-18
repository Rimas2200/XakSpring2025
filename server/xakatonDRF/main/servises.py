from ner_model import test
from connectionsbottg import models
from . import filter
from pprint import pprint
import re
from . import whatsapp
from tqdm import tqdm
import time
import os


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


def clean_text(text):
    # Защищаем даты: ДД.ММ.ГГГГ и ДД.ММ.ГГ
    text = re.sub(r'\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b', r'\1<DOT>\2<DOT>\3', text)
    # Защищаем даты: ДД.ММ (без года)
    text = re.sub(r'\b(\d{1,2})\.(\d{1,2})\b', r'\1<DOT>\2', text)
    # Защищаем дефисы между цифрой и буквой
    text = re.sub(r'(\d)-([a-zA-Zа-яА-Я])', r'\1<SAFE_HYPHEN>\2', text)
    # Защищаем слэш между цифрами (например, для дробей или дат)
    text = re.sub(r'(?<=\d)/(?=\d)', r'<SAFE_SLASH>', text)

    # Заменяем все неразрешённые символы на пробел
    text = re.sub(r'[^\w\s<SAFE_HYPHEN><DOT>]', ' ', text)

    # Восстанавливаем дефисы, точки и слэш
    text = text.replace('<SAFE_HYPHEN>', '-').replace('<DOT>', '.').replace('<SAFE_SLASH>', '/')

    # Замена вхождения "попу" в любом регистре на "По Пу"
    text = re.sub(r'(?i)\bпопу\b', 'По Пу', text)

    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text).strip()
    return text



    

def date_model(date_form: int) -> list:
    
    
    last_process = []

    # Получаем данные из базы данных
    message_database: dict = models.SavesTgMessages.objects.order_by('-id')[:int(date_form)] # randint(1,100)

    for mess in tqdm(message_database):
        group_filter_test = []
        second_lsist = []
        repit_update = []
        # очистка текста после бд 
        clear_text = clean_text(mess.message)
        # превращение в однострочную структуру 
        filter_single_line = filter.format_to_single_line(clear_text)

        # обработка в список 
        filters_message = filter.split_data_into_single_lines(filter_single_line)

        # Первичная обработка моделью t5
        primaryprocessing = test.preprocess_with_t5(filters_message)

        # отступы по ключам
        operations = re.split(r"(?=Пахота|Выравнивание|Сев|Культивация|Подкормка|Внесение|Уборка|Предпосевная|Чизлевание|Химпрополка|Первая|Сплошная|2-е|Диск)", primaryprocessing)
        
        # очистка от пустых строк
        filtered_operations = [item for item in operations if item.strip()]
        
        # Вторичная обработка моделью
        for entits in tqdm(filtered_operations):
            secondaryprocessing = test.predict_entities(entits)
            second_lsist.append(secondaryprocessing)
        # разделение на блоки 
        for date_items in tqdm(second_lsist):
            entities = test.process_subunit_and_hectare(date_items)
            entities = test.process_department(entities)
            entities = test.process_yield_total(entities)
            group = test.group_entities_by_operation(entities)
            group_filter_test.append(group)

        # проверка на пустыесписки 
        for item_filter_2 in tqdm(group_filter_test):
            if item_filter_2:
                if len(item_filter_2) == 1:
                # Если в item_filter_2 один элемент, добавляем его
                    last_process.append(item_filter_2[0])
                else:
                # Если несколько элементов, используем extend()
                    last_process.extend(item_filter_2)

    return last_process
    

def whatsapp_model(chat_name: str) -> list:

    driver = whatsapp.setup_driver()
    driver.get("https://web.whatsapp.com")
    whatsapp.wait_for_chat_load(driver)
    whatsapp.open_chat(driver, chat_name)
    whatsapp.scroll_to_top(driver)
    filter_words = [
        "попу", "аор", "тск", "мир", "восход", "ао кропоткинское",
        "колхоз прогресс", "сп коломейцево", "пу", "отд"
    ]

    result_parese = whatsapp.process_messages(driver, filter_words)
    driver.quit()

    #pprint(result_parese)
    # result_first_process = []
    
    last_process = []
    counter = 0
    
    for message in result_parese:

        group_message_ = []
        result_second_process = []

        primaryprocessing = test.preprocess_with_t5(message)
        print("Первичная обработка")
        pprint(primaryprocessing)
        print('-----------------------------------------------------------')
        operations = re.split(r"(?=Пахота|Выравнивание|Сев|Культивация|Подкормка|Внесение|Уборка|Предпосевная|Чизлевание|Химпрополка|Первая|Сплошная|2-е|Диск)", primaryprocessing)
        print("обработка после операций")
        pprint(operations)
        print('-----------------------------------------------------------')
        filtered_operations = [item for item in operations if item.strip()]
        print('filter обработка после операций t5')
        pprint(filtered_operations)
        print('-----------------------------------------------------------')
    
        for entits in filtered_operations:
            secondaryprocessing = test.predict_entities(entits) # обработка с помощью neiro
            result_second_process.append(secondaryprocessing)
        print(' первичная обработка неиро')
        pprint(result_second_process)
        print('-----------------------------------------------------------')
         # разделение на блоки 
        for date_items in tqdm(result_second_process):
            entities = test.process_subunit_and_hectare(date_items)
            entities = test.process_department(entities)
            entities = test.process_yield_total(entities)
            group = test.group_entities_by_operation(entities)
            group_message_.append(group)
            
            print('разделение на блоки')
            pprint(group)
            print('-----------------------------------------------------------')
        # проверка на пустыесписки 
        for item_filter_2 in tqdm(group_message_):
            if item_filter_2:
                if len(item_filter_2) == 1:
                # Если в item_filter_2 один элемент, добавляем его
                    last_process.append(item_filter_2[0])
                else:
                # Если несколько элементов, используем extend()
                    last_process.extend(item_filter_2)

        

        counter += 1
        print(f"Обработано сообщений: {counter}")
        
    
    return last_process

    










