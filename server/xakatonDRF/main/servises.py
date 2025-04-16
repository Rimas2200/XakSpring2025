from ner_model import test
from connectionsbottg import models
from . import filter
from pprint import pprint
from datetime import datetime
from . import models as main_models
from random import randint
import re
from . import backup

from tqdm import tqdm

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



    

def date_model() -> list:
    
    
    last_process = []

    # Получаем данные из базы данных
    message_database: dict = models.SavesTgMessages.objects.order_by('-id')[:2] # randint(1,100)
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
        
        # повторная обработка моделью t5
        for items in tqdm(filtered_operations):
            repit_until = test.preprocess_with_t5(items)
            repit_update.append(repit_until)
        
        # Вторичная обработка моделью
        for entits in tqdm(repit_update):
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
    
    











