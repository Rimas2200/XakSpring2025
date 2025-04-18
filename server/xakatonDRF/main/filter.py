import datetime
import re
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

def format_to_single_line(data :str) -> str:
    # Удаляем лишние пробелы и переносы строк
    lines = data.splitlines()
    cleaned_lines = []

    for line in tqdm(lines):
        # Убираем лишние пробелы в начале и конце строки
        stripped_line = line.strip()
        if stripped_line:  # Добавляем только непустые строки
            cleaned_lines.append(stripped_line)

    # Объединяем все строки в одну через пробел
    single_line = " ".join(cleaned_lines)
    return single_line

def filter_data(neir_entitis : list) -> list:
    
    
    grops_date = {
        'DEPARTMENT': [],
        'DATE': [],
        'OPERATION': [],
        'CROP': [],
        'HECTARE': [],  # За день, га
        'TOTAL_YIELD': []  # Вал с начала, ц
    }
    
    

    for item in neir_entitis:
        entity = item['entity']
        text = item['text']
        
        print(f"Обрабатываем сущность: {entity}, текст: {text}")
        
        if entity == 'DEPARTMENT' or entity == 'SUBUNIT':
            grops_date['DEPARTMENT'].append(text)
        elif entity == 'DATE':
            grops_date['DATE'].append(text)
        elif entity == 'OPERATION':
            grops_date['OPERATION'].append(text)
        elif entity == 'CROP':
            grops_date['CROP'].append(text)
        elif entity == 'HECTARE':
            grops_date['HECTARE'].append(text)
            
    return grops_date


def split_data_into_single_lines(data):
    # Разделяем данные на строки
    lines = data.splitlines()

    # Инициализируем переменные
    result = []
    current_group = []

    for line in tqdm(lines):
        stripped_line = line.strip()
        if not stripped_line:
            # Пропускаем пустые строки
            continue

        # Проверяем, является ли строка началом новой операции
        if any(char.isalpha() for char in stripped_line.split()[0]):
            # Если текущая группа не пуста, добавляем её в результат
            if current_group:
                result.append(" ".join(current_group))
                current_group = []

        # Добавляем строку в текущую группу
        current_group.append(stripped_line)

    # Добавляем последнюю группу в результат
    if current_group:
        result.append(" ".join(current_group))

    return result
