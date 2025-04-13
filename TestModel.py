import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re
from openpyxl import Workbook
from openpyxl.styles import Font

model_path = "agriculture_text_transform_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path).cuda()
model.eval()


def transform_text(text):
    inputs = tokenizer(
        text,
        return_tensors='pt',
        truncation=True,
        max_length=128
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=128,
            num_beams=5,
            repetition_penalty=2.5,
            early_stopping=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# while True:
#     user_input = input("\nтекст: ").strip()
#
#     if user_input.lower() in ['q']:
#         break
#
#     transformed_text = transform_text(user_input)
#     print(f"Исходный текст: {user_input}")
#     print(f"Преобразованный текст: {transformed_text}")


DEPARTMENTS = {
    "АОР": {
        "Кавказ": [18, 19],
        "Север": [3, 7, 10, 20],
        "Центр": [1, 4, 5, 6, 9],
        "Юг": [11, 12, 16, 17]
    },
    "ТСК": {"Нет ПУ": ["Нет отделения"]},
    "АО Кропоткинское": {"Нет ПУ": ["Нет отделения"]},
    "Восход": {"Нет ПУ": ["Нет отделения"]},
    "Колхоз Прогресс": {"Нет ПУ": ["Нет отделения"]},
    "Мир": {"Нет ПУ": ["Нет отделения"]},
    "СП Коломейцево": {"Нет ПУ": ["Нет отделения"]}
}

OPERATIONS = [
    "1-я междурядная культивация",
    "2-я междурядная культивация",
    "Боронование довсходовое",
    "Внесение минеральных удобрений",
    "Выравнивание зяби",
    "2-е Выравнивание зяби",
    "Гербицидная обработка",
    "1 Гербицидная обработка",
    "2 Гербицидная обработка",
    "3 Гербицидная обработка",
    "4 Гербицидная обработка",
    "Дискование",
    "2-е Дискование",
    "Инсектицидная обработка",
    "Культивация",
    "Пахота",
    "Подкормка",
    "Предпосевная культивация",
    "Прикатывание посевов",
    "Сев",
    "Сплошная культивация",
    "Уборка",
    "Фунгицидная обработка",
    "Чизлевание"
]

CULTURES = [
    "Вика+Тритикале",
    "Горох на зерно",
    "Горох товарный",
    "Гуар",
    "Конопля",
    "Кориандр",
    "Кукуруза кормовая",
    "Кукуруза семенная",
    "Кукуруза товарная",
    "Люцерна",
    "Многолетние злаковые травы",
    "Многолетние травы",
    "Многолетние травы прошлых лет",
    "Многолетние травы текущего года",
    "Овес",
    "Подсолнечник кондитерский",
    "Подсолнечник семенной",
    "Подсолнечник товарный",
    "Просо",
    "Пшеница озимая на зеленый корм",
    "Пшеница озимая семенная",
    "Пшеница озимая товарная",
    "Рапс озимый",
    "Рапс яровой",
    "Свекла сахарная",
    "Сорго",
    "Сорго кормовой",
    "Сорго-суданковый гибрид",
    "Соя семенная",
    "Соя товарная",
    "Чистый пар",
    "Чумиза",
    "Ячмень озимый",
    "Ячмень озимый семенной"
]


def find_operation(text):
    """Находит операцию в начале строки"""
    for op in sorted(OPERATIONS, key=len, reverse=True):
        if text.startswith(op):
            return op
    return None


def find_culture(text):
    """Извлекает культуру после слова 'под'"""
    match = re.search(r"под\s+([А-Яа-яЁё\s-]+)(?=\s+По|$)", text)
    if match:
        culture = match.group(1).strip()
        for c in CULTURES:
            if culture in c or c.startswith(culture):
                return c
    return None


def find_department(text):
    """Определяет подразделение по номеру отделения"""
    otd_match = re.search(r"Отд\s+(\d+)", text)
    if otd_match:
        otd_num = int(otd_match.group(1))
        for pu, otd_list in DEPARTMENTS["АОР"].items():
            if otd_num in otd_list:
                return "АОР"

    if "ТСК" in text:
        return "ТСК"
    elif "Кропоткинское" in text:
        return "АО Кропоткинское"

    return None


def find_areas(text):
    """Извлекает площади в формате XX/XXX"""
    areas = re.findall(r"\b(\d+)/(\d+)\b", text)
    if areas:
        return list(map(int, areas[0]))
    return [0, 0]


def parse_agro_string(input_string):
    """Основная функция разбора строки"""
    result = {
        "Операция": None,
        "Культура": None,
        "Подразделение": None,
        "За день, га": 0,
        "С начала операции, га": 0
    }

    clean_str = ' '.join(input_string.split())

    result["Операция"] = find_operation(clean_str)
    result["Культура"] = find_culture(clean_str)
    result["Подразделение"] = find_department(clean_str)
    day_area, total_area = find_areas(clean_str)
    result["За день, га"] = day_area
    result["С начала операции, га"] = total_area

    return result


def save_to_xlsx(data_list, filename="agro_operations.xlsx"):
    """Сохраняет данные в XLSX файл"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Агрооперации"

    headers = ["Операция", "Культура", "Подразделение", "За день, га", "С начала операции, га"]
    ws.append(headers)

    bold_font = Font(bold=True)
    for cell in ws[1]:
        cell.font = bold_font

    for data in data_list:
        ws.append([
            data["Операция"],
            data["Культура"],
            data["Подразделение"],
            data["За день, га"],
            data["С начала операции, га"]
        ])

    # Автонастройка ширины столбцов
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    wb.save(filename)
    print(f"Данные сохранены в файл: {filename}")



if __name__ == "__main__":
    test_string = """пш"""
    # Пахота зяби под мн тр По Пу 26/488 Отд 12 26/221
    # Предп культ под оз пш По Пу 215/1015 Отд 12 128/317 Отд 16 123/529
    # 2-е диск сах св под пш По Пу 22/627 Отд 11 22/217
    # 2-е диск сои под оз пш По Пу 45/1907 Отд 12 45/299
    transformed_text = transform_text(test_string)
    print(transformed_text)

    parsed_data = parse_agro_string(transformed_text)
    print("Результат разбора:")
    for key, value in parsed_data.items():
        print(f"{key}: {value}")

    # save_to_xlsx([parsed_data])