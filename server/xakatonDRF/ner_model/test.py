import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from openpyxl import load_workbook, Workbook
import os
import re
import sys
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Указываем путь к локальной модели
# model_path = os.path.getcwd() + "/T5_model/agriculture_text_transform_model"
model_path = os.path.join(os.getcwd(), "T5_model", "agriculture_text_transform_model")
# Проверяем, существует ли путь
print(model_path)
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Модель не найдена по пути: {model_path}")

# Загружаем токенайзер и модель с локального пути
T5tokenizer = T5Tokenizer.from_pretrained(model_path, local_files_only=True)
T5model = T5ForConditionalGeneration.from_pretrained(model_path, local_files_only=True).to(torch.device('cpu') )
T5model.eval()


def transform_text(text):
    inputs = T5tokenizer(
        text,
        return_tensors='pt',
        truncation=True,
        max_length=128
    ).to(T5model.device)

    with torch.no_grad():
        outputs = T5model.generate(
            **inputs,
            max_length=128,
            num_beams=5,
            repetition_penalty=2.5,
            early_stopping=True
        )

    return T5tokenizer.decode(outputs[0], skip_special_tokens=True)

def preprocess_with_t5(text):
    transformed_text = transform_text(text)
    return transformed_text

model_path = os.path.join(os.getcwd(), "ner_model", "ner-model")
tokenizer_ner = BertTokenizerFast.from_pretrained(model_path)
model_ner = BertForTokenClassification.from_pretrained(model_path)

"""
O - символы, которые нахуй не нужны # не нужная информация

B-OPERATION - начало наименование операции
I-OPERATION - часть операции

B-CROP - начало наименования культуры
I-CROP - часть культуры

B-DATE - дата

B-SUBUNIT - начинает наименование пу
I-SUBUNIT - наименование пу

B-DEPARTMENT - начинает наименование отделения
I-DEPARTMENT - наименование отделения

B-YIELD_TOTAL - вал и все с ним связанное

B-HECTARE - га
I-HECTARE - га
"""
label_list = [
    'B-CROP', 
    'B-DATE', 
    'B-DEPARTMENT', 
    'B-HECTARE', 
    'B-OPERATION', 
    'B-SUBUNIT', 
    'B-YIELD_TOTAL', 
    
    'I-CROP', 
    'I-DEPARTMENT', 
    'I-HECTARE', 
    'I-OPERATION', 
    'I-SUBUNIT', 
    'I-YIELD_TOTAL', 
    'O'
]


department_mapping = {
    "1": "АОР",
    "3": "АОР",
    "4": "АОР",
    "5": "АОР",
    "6": "АОР",
    "7": "АОР",
    "9": "АОР",
    "10": "АОР",
    "11": "АОР",
    "12": "АОР",
    "16": "АОР",
    "17": "АОР",
    "18": "АОР",
    "19": "АОР",
    "20": "АОР",
    "Кавказ": "АОР",
    "Север": "АОР",
    "Центр": "АОР",
    "Юг": "АОР",
}

def remove_duplicate_words(text):
    seen = set()
    result = []
    for word in text.split():
        if word not in seen:
            seen.add(word)
            result.append(word)
    return " ".join(result)


def predict_entities(text):
    words = text.split()

    inputs = tokenizer_ner(
        words,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model_ner(**inputs)

    predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()

    word_ids = inputs.word_ids()
    entities = []
    current_entity = None
    current_entity_words = []
    current_entity_start = None
    last_word_idx = None

    for word_idx, label_id in zip(word_ids, predictions):
        if word_idx is None:
            continue

        last_word_idx = word_idx

        label = label_list[label_id]
        word = words[word_idx]

        if label.startswith("B-"):
            if current_entity:
                entities.append({
                    "entity": current_entity,
                    "text": " ".join(current_entity_words),
                    "start": current_entity_start,
                    "end": word_idx
                })
            current_entity = label[2:]
            current_entity_words = [word]
            current_entity_start = word_idx

        elif label.startswith("I-") and current_entity and label[2:] == current_entity:
            current_entity_words.append(word)

        else:
            if current_entity:
                entities.append({
                    "entity": current_entity,
                    "text": " ".join(current_entity_words),
                    "start": current_entity_start,
                    "end": word_idx
                })
                current_entity = None
                current_entity_words = []
                current_entity_start = None

    if current_entity and last_word_idx is not None:
        entities.append({
            "entity": current_entity,
            "text": " ".join(current_entity_words),
            "start": current_entity_start,
            "end": last_word_idx + 1
        })

    merged_entities = []
    for entity in entities:
        if not merged_entities:
            merged_entities.append(entity)
        else:
            last_entity = merged_entities[-1]
            if (last_entity['entity'] == entity['entity'] and
                    last_entity['end'] == entity['start']):
                last_entity['text'] += " " + entity['text']
                last_entity['end'] = entity['end']
            else:
                merged_entities.append(entity)

    for entity in merged_entities:
        entity['text'] = remove_duplicate_words(entity['text'])

    return merged_entities

def process_subunit_and_hectare(entities):
    subunit_value = None
    hectare_values = []

    for entity in entities:
        key = entity['entity'].upper()
        if key == "SUBUNIT":
            subunit_value = entity['text']
        elif key == "HECTARE":
            match = re.search(r'(\d+)', entity['text'])
            if match:
                hectare_values.append(int(match.group(1)))
                print("===========================")
    entities = [e for e in entities if e['entity'].upper() not in ["SUBUNIT", "HECTARE"]]

    if subunit_value and "по пу" in subunit_value.lower():
        match = re.search(r'(\d+)/(\d+)', subunit_value)
        if match:
            part1, part2 = int(match.group(1)), int(match.group(2))
            smaller = min(part1, part2)
            larger = max(part1, part2)
            entities.append({"entity": "HECTARE", "text": str(smaller)})
            entities.append({"entity": "SUBUNIT", "text": str(larger)})
        else:
            print(f"Ошибка: Не удалось найти числа в строке '{subunit_value}'.")

    print(hectare_values)
    if len(hectare_values) >= 1:
        smaller = min(hectare_values)
        larger = max(hectare_values)
        entities.append({"entity": "HECTARE", "text": str(smaller)})
        entities.append({"entity": "SUBUNIT", "text": str(larger)})
        print(smaller, larger)
    elif len(hectare_values) == 1:
        print("------------------")
        entities.append({"entity": "HECTARE", "text": str(hectare_values[0])})

    return entities


def group_entities_by_operation(entities):
    """
    Группирует сущности по операциям.
    """
    grouped_data = []
    current_group = {}
    global_data = {"DATE": "", "DEPARTMENT": ""}

    for entity in entities:
        key = entity['entity'].upper()

        if key == "OPERATION":
            if current_group:
                grouped_data.append(current_group)
                current_group = {}
            current_group[key] = entity['text']
        elif key in ["DATE", "DEPARTMENT"]:
            global_data[key] = entity['text']
        elif key in ["CROP", "HECTARE", "SUBUNIT", "YIELD_TOTAL"]:
            current_group[key] = entity['text']

    if current_group:
        grouped_data.append(current_group)

    for group in grouped_data:
        group.update(global_data)

    return grouped_data


def process_department(entities):
    """
    Обрабатывает значение DEPARTMENT
    """
    for entity in entities:
        key = entity['entity'].upper()
        if key == "DEPARTMENT":
            department_value = entity['text']
            if department_value in department_mapping:
                entity['text'] = department_mapping[department_value]
            elif "отд" in department_value.lower():
                match = re.search(r'\d+', department_value)
                if match:
                    department_number = match.group(0)
                    if department_number in department_mapping:
                        entity['text'] = department_mapping[department_number]
            elif "юг" in department_value.lower():
                entity['text'] = "АОР"
    return entities


def process_yield_total(entities):
    """
    Обрабатывает значение YIELD_TOTAL
    """
    for entity in entities:
        key = entity['entity'].upper()
        if key == "YIELD_TOTAL":
            yield_total_value = entity['text']
            match = re.search(r'(\d+)', yield_total_value)
            if match:
                entity['text'] = match.group(1)
    return entities


def write_to_excel(entities, file_name="Таблица (полевые работы).xlsx"):
    headers = [
        "Дата", "Подразделение", "Операция", "Культура",
        "За день, га", "С начала операции, га", "Вал за день, ц", "Вал с начала, ц"
    ]

    if os.path.exists(file_name):
        workbook = load_workbook(file_name)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(headers)

    entity_to_column = {
        "DATE": "Дата",
        "DEPARTMENT": "Подразделение",
        "OPERATION": "Операция",
        "CROP": "Культура",
        "HECTARE": "За день, га",
        "SUBUNIT": "С начала операции, га",
        "YIELD_TOTAL": "Вал за день, ц",
    }

    grouped_data = group_entities_by_operation(entities)

    for group in grouped_data:
        row_data = {header: "" for header in headers}
        for key, value in group.items():
            if key in entity_to_column:
                col_name = entity_to_column[key]
                row_data[col_name] = value
        sheet.append([row_data[header] for header in headers])
    workbook.save(file_name)

"""
# if __name__ == "__main__":
# example_text = "Уборка Соя товарная (семенной) Отд 11 65/65 Вал 58720 Урож 9"
# example_text = "Пахота под Соя товарная: День - 295 га От начала - 6804 га (79%) Остаток- 1774 га, ЮГ"
# example_text = "14.04 Предпосевная культивация под Пшеница озимая По ПУ 146/1217 Отд 11 146/233"
# example_text = "16.11 Мир Пахота под Кукуруза товарная 30 га, 699 га, 89%, 73 га остаток."
# example_text = "16.11 Мир Пахота под Соя товарная 30 га, 779 га, Работало 2 агрегата."
example_text = "15.10 Пахота под сах св По Пу 88/329 Отд 11 23/60 Отд 12 34/204 Отд 16 31/65"
# example_text = "15.10 2-е диск под сах св По Пу 112/817 Отд 16 112/594"
print(example_text)
entities = preprocess_with_t5(example_text)
print(entities)
entities = predict_entities(entities)
print(entities)

# print("Текст:", example_text)
# print("Извлеченные сущности:")
# for entity in entities:
#     print(f"- {entity['entity']}: '{entity['text']}'")
entities = process_subunit_and_hectare(entities)
entities = process_department(entities)
entities = process_yield_total(entities)
write_to_excel(entities)"""