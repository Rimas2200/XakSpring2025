import pandas as pd

# Функция для удаления квадратных скобок
def remove_brackets(text):
    if isinstance(text, str):  # Проверяем, что значение является строкой
        return text.replace('[', '').replace(']', '')
    return text  # Если не строка, возвращаем как есть

# Путь к файлу
input_file = 'date.xlsx'
output_file = 'cleaned_data.xlsx'

# Чтение файла
try:
    df = pd.read_excel(input_file)
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    exit()

# Вывод информации о структуре файла
print("Структура файла:")
print(df.info())

# Вывод первых строк файла
print("\nПервые строки файла:")
print(df.head())

# Проверка наличия второго столбца
if len(df.columns) > 1:
    column_name = df.columns[1]  # Второй столбец по порядку
    print(f"Обрабатываем столбец: {column_name}")

    # Применение функции к столбцу
    df[column_name] = df[column_name].apply(remove_brackets)

    # Сохранение результата
    df.to_excel(output_file, index=False)
    print(f"Файл успешно сохранен: {output_file}")
else:
    print("В файле меньше двух столбцов.")