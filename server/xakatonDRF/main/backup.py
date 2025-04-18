from ner_model import test
from connectionsbottg import models
from . import filter
from pprint import pprint
from datetime import datetime
from . import models as main_models
from random import randint



class ProcessingByModel:
    def __init__(self):
        pass
"""current_row : dict = {
        'DATE': '', # Дата операции
        'DEPARTMENT': '', # Подразделение SUBUNIT
        
        'OPERATION': '',
        'CROP': '',
        'HECTARE': '', # За день, га
        
        'TOTAL_HECTARE': '',  # С начала операции, га
        'DAY_YIELD': '',  # Вал за день, ц
        'YIELD_TOTAL': ''  # Вал с начала, ц
}  """
    

def list_to_dict(messege_processing: list, poss_operation_list: list ) -> dict:
    temp_block = []
    operations = []
    operation_blocks = []
    
    current_operation = None
    
    for entity in messege_processing:
        if entity['entity'] == 'OPERATION':
            if temp_block:
                operation_blocks.append(temp_block)
            temp_block = [entity]
        else:
            temp_block.append(entity)
    if temp_block:
        operation_blocks.append(temp_block)
    pprint(operation_blocks)
    
def process_entities_final(entities):
    # Получаем текущую дату в формате DD.MM.YYYY
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    # Собираем все глобальные подразделения (до первой операции)
    global_departments = []
    
    # Ищем подразделения, указанные до первой операции
    has_operation = False
    for entity in entities:
        if entity['entity'] == 'OPERATION':
            has_operation = True
            break
        elif entity['entity'] in ['DEPARTMENT', 'SUBUNIT']:
            global_departments.append(entity['text'])
    
    # Если операций не было вообще, создаем одну запись
    if not has_operation:
        entry = {
            'DATE': current_date,  # Заполняем текущей датой по умолчанию
            'DEPARTMENT': ', '.join(global_departments) if global_departments else '',
            'OPERATION': '',
            'CROP': '',
            'HECTARE': '',
            'TOTAL_HECTARE': '',
            'DAY_YIELD': '',
            'YIELD_TOTAL': ''
        }
        
        # Добавляем остальные данные (если есть дата - перезапишем)
        for entity in entities:
            if entity['entity'] not in ['DEPARTMENT', 'SUBUNIT']:
                entry[entity['entity']] = entity['text']
        
        return [entry]
    
    # Обрабатываем операции
    result = []
    current_operation = None
    current_departments = []
    other_data = {}
    
    for entity in entities:
        entity_type = entity['entity']
        text = entity['text']
        
        if entity_type == 'OPERATION':
            # Сохраняем предыдущую операцию (если есть)
            if current_operation is not None:
                departments = current_departments if current_departments else global_departments
                if not departments:
                    departments = ['']
                
                for dept in departments:
                    entry = {
                        'DATE': other_data.get('DATE', current_date),  # Текущая дата по умолчанию
                        'DEPARTMENT': dept,
                        'OPERATION': current_operation,
                        'CROP': other_data.get('CROP', ''),
                        'HECTARE': other_data.get('HECTARE', ''),
                        'TOTAL_HECTARE': other_data.get('TOTAL_HECTARE', ''),
                        'DAY_YIELD': other_data.get('DAY_YIELD', ''),
                        'YIELD_TOTAL': other_data.get('YIELD_TOTAL', '')
                    }
                    result.append(entry)
            
            # Начинаем новую операцию
            current_operation = text
            current_departments = []
            other_data = {}
        
        elif entity_type in ['DEPARTMENT', 'SUBUNIT']:
            current_departments.append(text)
        else:
            other_data[entity_type] = text
    
    # Добавляем последнюю операцию
    if current_operation is not None:
        departments = current_departments if current_departments else global_departments
        if not departments:
            departments = ['']
        
        for dept in departments:
            entry = {
                'DATE': other_data.get('DATE', current_date),  # Текущая дата по умолчанию
                'DEPARTMENT': dept,
                'OPERATION': current_operation,
                'CROP': other_data.get('CROP', ''),
                'HECTARE': other_data.get('HECTARE', ''),
                'TOTAL_HECTARE': other_data.get('TOTAL_HECTARE', ''),
                'DAY_YIELD': other_data.get('DAY_YIELD', ''),
                'YIELD_TOTAL': other_data.get('YIELD_TOTAL', '')
            }
            result.append(entry)
    
    return result

def date_model() -> list:
    # Получаем данные из базы данных
    
    message_database: dict = models.SavesTgMessages.objects.get(id=randint(1,100)) # 92
    
    filters_message = filter.split_data_into_single_lines(message_database.message)
    print('-----------------------------------------------------------')
    print('Исходные сообщения:', message_database.id)
    pprint(filters_message)
    print('-----------------------------------------------------------')

    messege_processing = []
    poss_operation_list = []
    counter = 0
    for element_message in filters_message:
        # print(f"Обрабатываем сообщение: {element_message}")
        
        # Первичная обработка моделью
        primaryprocessing = test.preprocess_with_t5(element_message)
        # Вторичная обработка моделью
        secondaryprocessing = test.predict_entities(primaryprocessing)
        
        for element in secondaryprocessing:
            if element['entity'] == 'OPERATION':
                poss_operation_list.append(counter)
            messege_processing.append(element)
        counter += 1
    print('-----------------------------------------------------------')
    print('Обработанные сообщения:')
    pprint(messege_processing)
    print('-----------------------------------------------------------')
    #print(poss_operation_list)
    #list_to_dict(messege_processing, poss_operation_list)
    return process_entities_final(messege_processing)
    
    











