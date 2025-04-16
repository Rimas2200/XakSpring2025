from ner_model import test
from connectionsbottg import models
from . import filter
from pprint import pprint
import datetime



class ProcessingByModel:
    def __init__(self):
        pass
    
    
current_row : dict = {
        'DATE': '', # Дата операции
        'DEPARTMENT': '', # Подразделение SUBUNIT
        
        'OPERATION': '',
        'CROP': '',
        'HECTARE': '', # За день, га
        
        'TOTAL_HECTARE': '',  # С начала операции, га
        'DAY_YIELD': '',  # Вал за день, ц
        'YIELD_TOTAL': ''  # Вал с начала, ц
    }

def date_model() -> list:
    # Получаем данные из базы данных
    message_database: str = models.SavesTgMessages.objects.get(id=92).message # 92
    filters_message = filter.split_data_into_single_lines(message_database)

    pprint(filters_message)

    grouped_data = []  # Для хранения всех заполненных словарей
    current_operation = None  # Текущая операция
    current_crop = None  # Текущая культура
    current_date = None  # Текущая дата
    current_yield_total = None  # Вал с начала

    for element_message in filters_message:
        print(f"Обрабатываем сообщение: {element_message}")
        
        # Первичная обработка моделью
        primaryprocessing = test.preprocess_with_t5(element_message)
        # Вторичная обработка моделью
        secondaryprocessing = test.predict_entities(primaryprocessing)
        
        # Печатаем результат обработки
        pprint(secondaryprocessing)

        # Проверяем, содержит ли текущее сообщение OPERATION
        if any(entity.get("entity", "") == "OPERATION" for entity in secondaryprocessing):
            # Сохраняем новую операцию и культуру
            operation_entity = next((entity for entity in secondaryprocessing if entity["entity"] == "OPERATION"), None)
            crop_entity = next((entity for entity in secondaryprocessing if entity["entity"] == "CROP"), None)

            if operation_entity:
                current_operation = operation_entity["text"]
            if crop_entity:
                current_crop = crop_entity["text"]

            # Сбрасываем YIELD_TOTAL при новой операции
            current_yield_total = None

        # Если это подразделение или площадь, создаем новый словарь
        for entity in secondaryprocessing:
            entity_type = entity["entity"]
            entity_text = entity["text"]

            if entity_type in ["SUBUNIT", "DEPARTMENT"]:
                # Создаем новый словарь для текущего подразделения
                hectare_entity = next((e for e in secondaryprocessing if e["entity"] == "HECTARE"), None)

                new_row = {
                    'DATE': current_date or datetime.datetime.now().date(),  # Дата операции без времени
                    'DEPARTMENT': entity_text,  # Подразделение SUBUNIT
                    'OPERATION': current_operation or '',
                    'CROP': current_crop or '',
                    'HECTARE': hectare_entity["text"] if hectare_entity else '',  # За день, га
                    'YIELD_TOTAL': current_yield_total or ''  # Вал с начала, ц
                }

                # Добавляем словарь в список
                grouped_data.append(new_row)

            elif entity_type == "YIELD_TOTAL":
                # Сохраняем YIELD_TOTAL для текущей операции
                current_yield_total = entity_text

                # Обновляем последнюю строку в grouped_data, если она существует
                if grouped_data:
                    grouped_data[-1]['YIELD_TOTAL'] = current_yield_total
    pprint(grouped_data)
    return grouped_data








